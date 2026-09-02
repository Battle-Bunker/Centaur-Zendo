#!/usr/bin/env python3
"""Challenge-submission web app for Centaur Zendo (SPEC.md §8).

Two ways to run it:

* mounted:    ``engine/server.py`` calls ``make_subapp(store, config, sandbox)``
              and mounts the result at ``/submit``.
* standalone: ``python -m webapp.app --challenge-dir challenges --port 8081``.

Everything the app needs is injected: a ``ChallengeStore`` (engine/challenges.py),
a ``GameConfig`` (engine/config.py) and a ``Sandbox`` (engine/sandbox.py).  The
validator defaults to ``engine.challenges.validate``.  Because challenge code is
hostile-by-accident (a ``while True`` scorer is a normal beginner bug) every
validation runs through the sandbox, on a dedicated single worker thread, behind
a lock so one submission cannot corrupt another's sandbox state.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from aiohttp import web

REPO_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = Path(__file__).resolve().parent / "static"
NAME_PATTERN = r"^[A-Za-z0-9_-]{1,16}$"   # SPEC §2; engine.challenges.NAME_RE agrees
NAME_RE = re.compile(NAME_PATTERN)
CODE_FIELDS = ("generate", "solve", "score")
DOC_FIELDS = ("name", "author", "description") + CODE_FIELDS

# Typed application keys (aiohttp >= 3.9): everything the sub-app carries.
STORE = web.AppKey("store", object)
CONFIG = web.AppKey("config", object)
SANDBOX = web.AppKey("sandbox", object)
VALIDATE = web.AppKey("validate", object)
SPEC_CLS = web.AppKey("spec_cls", object)
OK_CACHE = web.AppKey("ok_cache", dict)
LOCK = web.AppKey("sandbox_lock", asyncio.Lock)
EXECUTOR = web.AppKey("executor", ThreadPoolExecutor)
MAIN_THREAD = web.AppKey("main_thread_validation", bool)

CAP_FIELDS = (
    "max_generate_code_chars",
    "max_solve_code_chars",
    "max_score_code_chars",
    "max_clue_chars",
    "max_solution_chars",
    "max_generate_ms",
    "max_score_ms",
    "max_solve_ms",
)
CAP_DEFAULTS = {
    "max_generate_code_chars": 50_000,
    "max_solve_code_chars": 5_000,
    "max_score_code_chars": 256,
    "max_clue_chars": 1024,
    "max_solution_chars": 4096,
    "max_generate_ms": 100,
    "max_score_ms": 50,
    "max_solve_ms": 2000,
}


# --------------------------------------------------------------------------
# small adapters over the engine's objects (SPEC §2/§4 shapes, duck-typed)
# --------------------------------------------------------------------------
def caps_of(config) -> dict:
    """The character/time caps of a GameConfig, as a plain dict."""
    getter = getattr(config, "caps_dict", None)
    if callable(getter):
        return dict(getter())
    return {k: getattr(config, k, CAP_DEFAULTS[k]) for k in CAP_FIELDS}


def unwrap_sandbox(sandbox):
    """Accept an AsyncSandbox facade as well as a plain Sandbox."""
    return getattr(sandbox, "sync", sandbox)


def needs_main_thread(sandbox) -> bool:
    """True for InProcessSandbox, whose SIGALRM limits only work on the main thread.

    The subprocess `Sandbox` enforces its limits inside the child (and kills it
    from the parent), so it is happy on a worker thread; `InProcessSandbox` is
    not, and quietly turns "signal only works in main thread" into a validation
    error if we call it from one.  `restart()` exists only on the subprocess one.
    """
    return not hasattr(sandbox, "restart")


def spec_to_doc(spec) -> dict:
    """Normalise a ChallengeSpec (dataclass, mapping or object) to a JSON doc."""
    if spec is None:
        return {}
    if isinstance(spec, dict):
        src = spec
    elif hasattr(spec, "to_dict"):
        src = spec.to_dict()
    elif hasattr(spec, "__dict__") and spec.__dict__:
        src = dict(spec.__dict__)
    else:  # dataclass with __slots__, namedtuple, ...
        src = {f: getattr(spec, f, None) for f in DOC_FIELDS}
    doc = {f: src.get(f) for f in DOC_FIELDS}
    doc["name"] = doc.get("name") or ""
    for f in ("author", "description"):
        doc[f] = doc.get(f) or ""
    for f in CODE_FIELDS:
        doc[f] = doc.get(f) or ""
    return doc


def doc_to_spec(doc: dict, spec_cls):
    """Build the engine's ChallengeSpec from a JSON doc (dict if there is none)."""
    if spec_cls is None:
        return dict(doc)
    from_dict = getattr(spec_cls, "from_dict", None)
    return from_dict(doc) if callable(from_dict) else spec_cls(**doc)


def report_to_dict(report) -> dict:
    """Normalise a ValidationReport to JSON (ok/errors/warnings/timings/samples)."""
    if isinstance(report, dict):
        src = report
    elif hasattr(report, "to_dict"):
        src = report.to_dict()
    elif hasattr(report, "_asdict"):
        src = report._asdict()
    elif hasattr(report, "__dict__") and report.__dict__:
        src = dict(report.__dict__)
    else:
        src = {
            k: getattr(report, k, None)
            for k in ("ok", "errors", "warnings", "timings", "samples")
        }
    return {
        "name": src.get("name", ""),
        "ok": bool(src.get("ok")),
        "errors": list(src.get("errors") or []),
        "warnings": list(src.get("warnings") or []),
        "timings": dict(src.get("timings") or {}),
        "samples": [dict(s) for s in (src.get("samples") or [])][:3],
    }


def store_names(store) -> list[str]:
    """Names in the store (ChallengeStore.list() yields specs, not names)."""
    lister = getattr(store, "names", None)
    if callable(lister):
        return list(lister())
    out = []
    for item in store.list():
        out.append(item if isinstance(item, str) else spec_to_doc(item).get("name", ""))
    return [n for n in out if n]


def store_get_doc(store, name: str) -> dict | None:
    try:
        spec = store.get(name)
    except (KeyError, FileNotFoundError, ValueError):
        return None
    if spec is None:
        return None
    return spec_to_doc(spec)


# --------------------------------------------------------------------------
# request helpers
# --------------------------------------------------------------------------
class ApiError(web.HTTPException):
    """A JSON error response; the code is carried in the body as well."""

    def __init__(self, status: int, code: str, message: str, **extra):
        self.status_code = status
        body = {"error": code, "message": message, **extra}
        super().__init__(
            text=json.dumps(body, indent=1), content_type="application/json"
        )


async def read_doc(request: web.Request) -> dict:
    """Parse + shape-check the submitted challenge document."""
    try:
        raw = await request.json()
    except Exception:
        raise ApiError(400, "bad_json", "request body is not valid JSON")
    if not isinstance(raw, dict):
        raise ApiError(400, "bad_json", "request body must be a JSON object")
    doc = {}
    for f in DOC_FIELDS:
        v = raw.get(f, "")
        if v is None:
            v = ""
        if not isinstance(v, str):
            raise ApiError(400, "bad_field", f"field {f!r} must be a string")
        doc[f] = v
    doc["name"] = doc["name"].strip()
    if not NAME_RE.match(doc["name"]):
        raise ApiError(
            400, "bad_name", f"name must match {NAME_PATTERN}", field="name"
        )
    return doc


def require_admin(request: web.Request) -> None:
    """No-op when config.admin_token is empty (a local organiser laptop)."""
    token = getattr(request.app[CONFIG], "admin_token", "") or ""
    if not token:
        return
    if request.headers.get("X-Admin-Token", "") != token:
        raise ApiError(403, "forbidden", "X-Admin-Token header required")


# --------------------------------------------------------------------------
# validation plumbing
# --------------------------------------------------------------------------
async def run_validation(app: web.Application, doc: dict) -> dict:
    """Validate one document in the sandbox without blocking the event loop.

    The sandbox is a single shared resource, so calls are serialised with a lock
    and executed on one dedicated worker thread.  If the injected sandbox turns
    out to be signal-based and therefore main-thread-only, we fall back to an
    inline call (correctness over concurrency; a real subprocess Sandbox does not
    hit this path).
    """
    spec = doc_to_spec(doc, app[SPEC_CLS])
    validate = app[VALIDATE]
    config, sandbox = app[CONFIG], app[SANDBOX]

    def work():
        # engine.challenges.validate does its own sandbox.add(spec), which only
        # touches this one name — challenges the server already has stay loaded.
        return validate(spec, config, sandbox)

    async with app[LOCK]:
        loop = asyncio.get_running_loop()
        try:
            if app[MAIN_THREAD]:
                report = work()
            else:
                report = await loop.run_in_executor(app[EXECUTOR], work)
        except ValueError as e:  # "signal only works in main thread of the main interpreter"
            if "main thread" not in str(e):
                raise
            app[MAIN_THREAD] = True
            report = work()
        except Exception as e:
            return {
                "ok": False,
                "errors": [f"validator crashed: {type(e).__name__}: {e}"],
                "warnings": [],
                "timings": {},
                "samples": [],
            }
    out = report_to_dict(report)
    app[OK_CACHE][doc["name"]] = out["ok"]
    return out


# --------------------------------------------------------------------------
# handlers
# --------------------------------------------------------------------------
async def get_index(request: web.Request) -> web.StreamResponse:
    index = STATIC_DIR / "index.html"
    if not index.exists():
        raise ApiError(500, "no_ui", "webapp/static/index.html is missing")
    return web.FileResponse(index, headers={"Cache-Control": "no-cache"})


async def get_config(request: web.Request) -> web.Response:
    config = request.app[CONFIG]
    return web.json_response(
        {
            "caps": caps_of(config),
            "validation_seeds": getattr(config, "validation_seeds", 20),
            "sandbox": type(request.app[SANDBOX]).__name__,
            "validation_seed": getattr(config, "validation_seed", 12345),
            "name_pattern": NAME_PATTERN,
            "admin_required": bool(getattr(config, "admin_token", "") or ""),
            "challenge_dir": str(getattr(config, "challenge_dir", "challenges")),
        }
    )


async def post_validate(request: web.Request) -> web.Response:
    doc = await read_doc(request)
    return web.json_response(await run_validation(request.app, doc))


async def list_challenges(request: web.Request) -> web.Response:
    app = request.app
    out = []
    for name in sorted(store_names(app[STORE]), key=str.lower):
        doc = store_get_doc(app[STORE], name) or {}
        out.append(
            {
                "name": name,
                "author": doc.get("author", ""),
                "ok": app[OK_CACHE].get(name),
            }
        )
    return web.json_response({"challenges": out})


async def post_challenges(request: web.Request) -> web.Response:
    app = request.app
    doc = await read_doc(request)
    name = doc["name"]
    overwrite = request.query.get("overwrite", "") in ("1", "true", "yes")
    exists = name in store_names(app[STORE])
    if exists and not overwrite:
        raise ApiError(
            409,
            "exists",
            f"a challenge named {name!r} already exists; "
            "resubmit with ?overwrite=1 to replace it",
            name=name,
        )
    if exists and overwrite:
        require_admin(request)

    report = await run_validation(app, doc)
    if not report["ok"]:
        return web.json_response(
            {"saved": False, "name": name, "report": report}, status=400
        )
    app[STORE].put(doc_to_spec(doc, app[SPEC_CLS]))
    app[OK_CACHE][name] = True
    return web.json_response(
        {"saved": True, "name": name, "overwritten": exists, "report": report},
        status=201,
    )


async def get_challenge(request: web.Request) -> web.Response:
    name = request.match_info["name"]
    doc = store_get_doc(request.app[STORE], name)
    if doc is None:
        raise ApiError(404, "not_found", f"no challenge named {name!r}")
    doc["ok"] = request.app[OK_CACHE].get(name)
    return web.json_response(doc)


async def delete_challenge(request: web.Request) -> web.Response:
    require_admin(request)
    app = request.app
    name = request.match_info["name"]
    if name not in store_names(app[STORE]):
        raise ApiError(404, "not_found", f"no challenge named {name!r}")
    app[STORE].delete(name)
    app[OK_CACHE].pop(name, None)
    return web.json_response({"deleted": name})


# --------------------------------------------------------------------------
# app construction
# --------------------------------------------------------------------------
def default_validate():
    """engine.challenges.validate, imported lazily so webapp can be built first."""
    from engine.challenges import validate  # noqa: PLC0415

    return validate


def default_spec_cls():
    try:
        from engine.challenges import ChallengeSpec  # noqa: PLC0415

        return ChallengeSpec
    except Exception:
        return None


def make_subapp(store, config, sandbox, *, validate=None, spec_cls=None) -> web.Application:
    """Build the /submit sub-application.

    store    engine.challenges.ChallengeStore  (list/get/put/delete)
    config   engine.config.GameConfig          (caps, validation_seeds, admin_token)
    sandbox  engine.sandbox.Sandbox            (used by validate)
    """
    app = web.Application()
    app[STORE] = store
    app[CONFIG] = config
    app[SANDBOX] = unwrap_sandbox(sandbox)
    app[VALIDATE] = validate or default_validate()
    app[SPEC_CLS] = spec_cls if spec_cls is not None else default_spec_cls()
    app[OK_CACHE] = {}
    app[LOCK] = asyncio.Lock()
    app[EXECUTOR] = ThreadPoolExecutor(max_workers=1, thread_name_prefix="validate")
    # InProcessSandbox must be driven from the main thread (SIGALRM); it is then
    # the caller's job to keep hostile code out of a live server (see README).
    app[MAIN_THREAD] = needs_main_thread(app[SANDBOX])

    app.router.add_get("", get_index)
    app.router.add_get("/", get_index)
    app.router.add_get("/api/config", get_config)
    app.router.add_post("/api/validate", post_validate)
    app.router.add_get("/api/challenges", list_challenges)
    app.router.add_post("/api/challenges", post_challenges)
    app.router.add_get("/api/challenges/{name}", get_challenge)
    app.router.add_delete("/api/challenges/{name}", delete_challenge)
    if STATIC_DIR.is_dir():
        app.router.add_static("/static/", STATIC_DIR, name="static")

    async def _shutdown(a):
        a[EXECUTOR].shutdown(wait=False, cancel_futures=True)

    app.on_cleanup.append(_shutdown)
    return app


# --------------------------------------------------------------------------
# quickcheck fallback backend (--fallback-validator)
# --------------------------------------------------------------------------
class QuickcheckConfig:
    """Minimal stand-in for GameConfig backed by tools/quickcheck.py's caps."""

    def __init__(self, challenge_dir="challenges", admin_token=""):
        for k, v in CAP_DEFAULTS.items():
            setattr(self, k, v)
        self.validation_seeds = 20
        self.validation_seed = 12345
        self.challenge_dir = challenge_dir
        self.admin_token = admin_token


class QuickcheckStore:
    """Minimal stand-in for ChallengeStore: a directory of JSON documents."""

    def __init__(self, directory):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name):
        if not NAME_RE.match(name or ""):
            raise KeyError(name)
        return self.dir / f"{name}.json"

    def list(self):
        return sorted(p.stem for p in self.dir.glob("*.json"))

    def get(self, name):
        p = self._path(name)
        if not p.exists():
            raise KeyError(name)
        return json.loads(p.read_text())

    def put(self, spec):
        doc = spec_to_doc(spec)
        self._path(doc["name"]).write_text(json.dumps(doc, indent=1) + "\n")
        return doc

    def delete(self, name):
        p = self._path(name)
        if p.exists():
            p.unlink()


class QuickcheckSandbox:
    """quickcheck.py owns its own exec model, so there is nothing to hold here."""

    def __init__(self, config=None):
        self.config = config

    def load(self, specs):
        return None

    def close(self):
        return None


def quickcheck_validate(spec, config, sandbox):
    """Run tools/quickcheck.py in a subprocess (isolates timeouts and C-level loops)."""
    doc = spec_to_doc(spec)
    seeds = getattr(config, "validation_seeds", 20)
    budget = 30 + seeds * (getattr(config, "max_solve_ms", 2000) / 1000.0) * 8
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(doc, f)
        path = f.name
    try:
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "quickcheck.py"),
             path, "--json", "--seeds", str(seeds)],
            capture_output=True, text=True, timeout=budget,
        )
        try:
            return json.loads(proc.stdout)
        except Exception:
            return {
                "ok": False,
                "errors": [f"quickcheck failed: {(proc.stderr or proc.stdout)[-800:]}"],
                "warnings": [], "timings": {}, "samples": [],
            }
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "errors": [f"validation did not finish within {budget:.0f}s (runaway code?)"],
            "warnings": [], "timings": {}, "samples": [],
        }
    finally:
        Path(path).unlink(missing_ok=True)


# --------------------------------------------------------------------------
# standalone runner
# --------------------------------------------------------------------------
def build_standalone(args) -> web.Application:
    if args.fallback_validator:
        config = QuickcheckConfig(args.challenge_dir, args.admin_token)
        store = QuickcheckStore(args.challenge_dir)
        sandbox = QuickcheckSandbox(config)
        return make_subapp(
            store, config, sandbox,
            validate=quickcheck_validate, spec_cls=None,
        )

    from engine.config import GameConfig  # noqa: PLC0415
    from engine.challenges import ChallengeStore  # noqa: PLC0415
    from engine import sandbox as sandbox_mod  # noqa: PLC0415

    if args.config:
        loader = getattr(GameConfig, "load", None) or getattr(GameConfig, "from_file", None)
        config = loader(args.config) if loader else GameConfig(**json.loads(Path(args.config).read_text()))
    else:
        config = GameConfig()
    if args.challenge_dir:
        config.challenge_dir = args.challenge_dir
    if args.admin_token:
        config.admin_token = args.admin_token

    store = ChallengeStore(config.challenge_dir)
    # The subprocess Sandbox is the default: a `while True` scorer then costs one
    # killed worker instead of a wedged web server.
    sandbox_cls = (sandbox_mod.InProcessSandbox if args.in_process
                   else getattr(sandbox_mod, "Sandbox", None) or sandbox_mod.InProcessSandbox)
    sandbox = sandbox_cls(config)
    app = make_subapp(store, config, sandbox)

    async def _close(a):
        try:
            a[SANDBOX].close()
        except Exception:
            pass

    app.on_cleanup.append(_close)
    return app


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Centaur Zendo challenge submission app")
    ap.add_argument("--challenge-dir", default="challenges")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8081)
    ap.add_argument("--config", default=None, help="game config JSON (engine.config.GameConfig)")
    ap.add_argument("--admin-token", default="", help="required by DELETE and by overwrite")
    ap.add_argument(
        "--in-process",
        action="store_true",
        help="use engine.sandbox.InProcessSandbox instead of the subprocess Sandbox "
             "(no isolation: a runaway scorer blocks the server)",
    )
    ap.add_argument(
        "--fallback-validator",
        action="store_true",
        help="validate with tools/quickcheck.py in a subprocess instead of the engine "
             "(useful before engine/ is available)",
    )
    args = ap.parse_args(argv)

    if not args.fallback_validator:
        sys.path.insert(0, str(REPO_ROOT))
    app = build_standalone(args)
    print(f"Centaur Zendo submission app: http://{args.host}:{args.port}/  "
          f"(challenges in {args.challenge_dir})", file=sys.stderr)
    web.run_app(app, host=args.host, port=args.port, print=None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
