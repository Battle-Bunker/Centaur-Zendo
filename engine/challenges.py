"""Challenge specs, the on-disk store, load-time validation and the compiled pool
(SPEC §2 and §4).

The validation implemented here is the same algorithm as ``tools/quickcheck.py``
(the dependency-free CLI challenge authors run), but every call to challenge code
goes through a `Sandbox`, so the time limits are enforced by the worker process
and a runaway generator cannot wedge the server.
"""
from __future__ import annotations

import json
import logging
import random
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from engine.config import GameConfig
from engine.sandbox import SandboxError, SandboxTimeout, type_name_of

log = logging.getLogger("centaur.challenges")

__all__ = [
    "NAME_RE", "ChallengeSpec", "ChallengeStore", "ValidationReport",
    "validate", "load_pool", "CompiledPool",
]

NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,16}$")

#: how many (seed, clue, solution) samples a report carries
MAX_SAMPLES = 3


# ---------------------------------------------------------------- the spec
@dataclass
class ChallengeSpec:
    """One challenge generator: three Python sources plus metadata (SPEC §2)."""

    name: str = ""
    author: str = ""
    description: str = ""
    generate: str = ""
    solve: str = ""
    score: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ChallengeSpec":
        return cls(
            name=str(data.get("name", "") or ""),
            author=str(data.get("author", "") or ""),
            description=str(data.get("description", "") or ""),
            generate=data.get("generate", "") or "",
            solve=data.get("solve", "") or "",
            score=data.get("score", "") or "",
        )

    @classmethod
    def from_file(cls, path: "str | Path") -> "ChallengeSpec":
        data = json.loads(Path(path).read_text())
        if not isinstance(data, dict):
            raise ValueError(f"{path}: challenge JSON must be an object")
        return cls.from_dict(data)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "author": self.author, "description": self.description,
                "generate": self.generate, "solve": self.solve, "score": self.score}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_file(self, path: "str | Path") -> None:
        Path(path).write_text(self.to_json() + "\n")

    def public_name(self) -> str:
        """The only thing players ever see about a challenge besides its clues."""
        return self.name


# ---------------------------------------------------------------- the store
class ChallengeStore:
    """A directory of ``<name>.json`` challenge documents (SPEC §4)."""

    def __init__(self, directory: "str | Path" = "challenges"):
        self.dir = Path(directory)

    # -- helpers --------------------------------------------------------------
    def _check_name(self, name: str) -> str:
        if not isinstance(name, str) or not NAME_RE.match(name):
            raise ValueError(f"invalid challenge name {name!r} (must match {NAME_RE.pattern})")
        return name

    def path_for(self, name: str) -> Path:
        return self.dir / f"{self._check_name(name)}.json"

    def exists(self, name: str) -> bool:
        return self.path_for(name).is_file()

    # -- CRUD -----------------------------------------------------------------
    def names(self) -> list[str]:
        if not self.dir.is_dir():
            return []
        return sorted(p.stem for p in self.dir.glob("*.json"))

    def list(self) -> list[ChallengeSpec]:
        """Every readable challenge in the directory, sorted by name.

        Unreadable/invalid files are logged and skipped so one bad file cannot
        stop the pool from loading.
        """
        specs: list[ChallengeSpec] = []
        if not self.dir.is_dir():
            return specs
        for path in sorted(self.dir.glob("*.json")):
            try:
                spec = ChallengeSpec.from_file(path)
            except Exception as e:
                log.error("challenge file %s is not readable JSON: %s", path, e)
                continue
            if not spec.name:
                spec.name = path.stem
            specs.append(spec)
        return sorted(specs, key=lambda s: s.name)

    def get(self, name: str) -> ChallengeSpec:
        path = self.path_for(name)
        if not path.is_file():
            raise KeyError(name)
        return ChallengeSpec.from_file(path)

    def put(self, spec: "ChallengeSpec | Mapping[str, Any]") -> ChallengeSpec:
        if isinstance(spec, Mapping):
            spec = ChallengeSpec.from_dict(spec)
        self._check_name(spec.name)
        self.dir.mkdir(parents=True, exist_ok=True)
        spec.to_file(self.path_for(spec.name))
        return spec

    def delete(self, name: str) -> bool:
        path = self.path_for(name)
        if not path.is_file():
            return False
        path.unlink()
        return True


# ---------------------------------------------------------------- validation
@dataclass
class ValidationReport:
    """Outcome of `validate` (SPEC §4)."""

    name: str = ""
    ok: bool = False
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    timings: dict[str, float] = field(default_factory=lambda: {
        "generate_ms_max": 0.0, "score_ms_max": 0.0, "solve_ms_max": 0.0})
    samples: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "ok": self.ok, "errors": list(self.errors),
                "warnings": list(self.warnings), "timings": dict(self.timings),
                "samples": [dict(s) for s in self.samples]}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ValidationReport":
        return cls(name=data.get("name", ""), ok=bool(data.get("ok")),
                   errors=list(data.get("errors", [])), warnings=list(data.get("warnings", [])),
                   timings=dict(data.get("timings", {})), samples=list(data.get("samples", [])))

    def summary(self) -> str:
        t = self.timings
        return (f"{'OK  ' if self.ok else 'FAIL'} {self.name:<10} "
                f"gen={t.get('generate_ms_max', 0)}ms score={t.get('score_ms_max', 0)}ms "
                f"solve={t.get('solve_ms_max', 0)}ms "
                f"({len(self.errors)} errors, {len(self.warnings)} warnings)")


def validate(spec: "ChallengeSpec | Mapping[str, Any]", config: GameConfig | None = None,
             sandbox: Any = None, existing_names: Iterable[str] | None = None) -> ValidationReport:
    """Run every SPEC §4 check for one challenge through `sandbox`.

    `sandbox` must expose the `engine.sandbox` API (`add`, `generate_timed`,
    `solve_timed`, `score_timed`); an `InProcessSandbox` is created if omitted.
    Checks are grouped and the first failing group stops the run.
    """
    if isinstance(spec, Mapping):
        spec = ChallengeSpec.from_dict(spec)
    config = config or GameConfig()
    if sandbox is None:
        from engine.sandbox import InProcessSandbox
        sandbox = InProcessSandbox(config)

    rp = ValidationReport(name=spec.name if isinstance(spec.name, str) else "")
    errors, warnings, samples, timings = rp.errors, rp.warnings, rp.samples, rp.timings

    def finish(ok: bool) -> ValidationReport:
        for k in timings:
            timings[k] = round(timings[k], 2)
        _dedupe_warnings(warnings)
        rp.ok = ok
        return rp

    # -- group 1: metadata + sizes -------------------------------------------
    name = spec.name
    if not isinstance(name, str) or not NAME_RE.match(name):
        errors.append("name must match [A-Za-z0-9_-]{1,16}")
    elif existing_names is not None and name in set(existing_names):
        errors.append(f"a challenge named {name!r} already exists in this pool")
    if not spec.description:
        warnings.append("description is empty (private notes for organisers)")
    for kind, cap_name in (("generate", "max_generate_code_chars"), ("solve", "max_solve_code_chars"),
                           ("score", "max_score_code_chars")):
        src = getattr(spec, kind)
        cap = getattr(config, cap_name)
        if not isinstance(src, str) or not src.strip():
            errors.append(f"missing {kind} source")
        elif len(src) > cap:
            errors.append(f"{kind} source is {len(src)} chars, cap is {cap}")
    if errors:
        return finish(False)

    # -- group 2: compile + exec + required callable --------------------------
    try:
        compile_errors = sandbox.add(spec)
    except SandboxError as e:
        errors.append(f"sandbox could not load the challenge: {e}")
        return finish(False)
    for kind in ("generate", "solve", "score"):
        if kind in compile_errors:
            errors.append(f"{kind}: {compile_errors[kind]}")
    if errors:
        return finish(False)

    # -- group 3: behaviour over validation_seeds -----------------------------
    def call_score(clue: str, sol: str, label: str):
        """Returns the value, ('exc', msg) if score raised, or None on timeout (fatal)."""
        try:
            v, ms = sandbox.score_timed(name, clue, sol)
        except SandboxTimeout as e:
            errors.append(f"score timed out on {label}: {e}")
            return None
        except SandboxError as e:
            return ("exc", str(e))
        timings["score_ms_max"] = max(timings["score_ms_max"], ms)
        return v

    rng = random.Random(config.validation_seed)
    accepted_junk_everything = True
    for _ in range(config.validation_seeds):
        seed = rng.getrandbits(32)
        tag = f"seed {seed}"
        try:
            clue, ms = sandbox.generate_timed(name, seed)
        except SandboxError as e:
            errors.append(f"generate({tag}) failed: {e}")
            break
        timings["generate_ms_max"] = max(timings["generate_ms_max"], ms)
        if not isinstance(clue, str) or not clue:
            errors.append(f"generate({tag}) must return a non-empty str, got {type_name_of(clue)}")
            break
        if len(clue) > config.max_clue_chars:
            errors.append(f"generate({tag}) clue is {len(clue)} chars, cap {config.max_clue_chars}")
            break
        try:
            clue2, _ = sandbox.generate_timed(name, seed)
        except SandboxError as e:
            errors.append(f"generate({tag}) second call failed: {e}")
            break
        if clue2 != clue:
            errors.append(f"generate({tag}) is not deterministic")
            break
        try:
            sol, ms = sandbox.solve_timed(name, clue)
        except SandboxError as e:
            errors.append(f"solve({tag}) failed: {e}\n  clue={clue[:200]!r}")
            break
        timings["solve_ms_max"] = max(timings["solve_ms_max"], ms)
        if not isinstance(sol, str):
            errors.append(f"solve({tag}) must return str, got {type_name_of(sol)}")
            break
        if len(sol) > config.max_solution_chars:
            errors.append(f"solve({tag}) solution is {len(sol)} chars, cap {config.max_solution_chars}")
            break

        v = call_score(clue, sol, f"solve output ({tag})")
        if v is None:
            break
        if isinstance(v, tuple):
            errors.append(f"score raised on solve output ({tag}): {v[1]}")
            break
        if v != 1:
            errors.append(f"score(clue, solve(clue)) != 1 for {tag}: got {v!r}\n"
                          f"  clue={clue[:200]!r}\n  sol={sol[:200]!r}")
            break

        v = call_score(clue, "", f"empty solution ({tag})")
        if v is None:
            break
        if isinstance(v, tuple):
            warnings.append(f"score raised on empty solution ({tag}): {v[1]} (treated as 0)")
        elif v != 0:
            errors.append(f"score(clue, '') must be 0 for {tag}, got {v!r}")
            break

        junk = ["0", "1", "x", "1" * 100, clue,
                "".join(rng.sample(sol, len(sol))) if len(sol) > 1 else "zz"]
        for j in junk:
            v = call_score(clue, j, f"junk {j[:20]!r} ({tag})")
            if v is None:
                break
            if isinstance(v, tuple):
                warnings.append(f"score raised on junk {j[:20]!r} ({tag}): {v[1]} (treated as 0)")
                v = 0
            if v not in (0, 1):
                errors.append(f"score must return 0 or 1, got {v!r} on junk {j[:20]!r}")
                break
            if v == 0:
                accepted_junk_everything = False
            elif j == clue:
                warnings.append(f"score accepts the clue itself as a solution ({tag})")
        if errors:
            break
        if len(samples) < MAX_SAMPLES:
            samples.append({"seed": seed, "clue": clue, "solution": sol})

    # -- group 4: cross-seed judgements + soft warnings ------------------------
    if not errors and accepted_junk_everything:
        errors.append("score returned 1 for every junk input — the scorer accepts anything")
    if not errors:
        if timings["solve_ms_max"] > 0.25 * config.max_solve_ms:
            warnings.append(f"solve is slowish ({timings['solve_ms_max']:.0f} ms; cap {config.max_solve_ms})")
        if timings["generate_ms_max"] > 0.5 * config.max_generate_ms:
            warnings.append(f"generate is slowish ({timings['generate_ms_max']:.0f} ms; "
                            f"cap {config.max_generate_ms})")
    return finish(not errors)


def _dedupe_warnings(warnings: list[str]) -> None:
    """Collapse warnings that differ only by which seed produced them."""
    seen, uniq = set(), []
    for w in warnings:
        key = re.sub(r"\(seed \d+\)", "", w)
        if key not in seen:
            seen.add(key)
            uniq.append(w)
    warnings[:] = uniq


# ---------------------------------------------------------------- the pool
class CompiledPool:
    """The accepted challenges of a game, bound to a sandbox for execution."""

    def __init__(self, specs: Sequence[ChallengeSpec], config: GameConfig | None = None,
                 sandbox: Any = None):
        self.config = config or GameConfig()
        self.specs: dict[str, ChallengeSpec] = {s.name: s for s in specs}
        self.names: list[str] = sorted(self.specs)
        self.sandbox = sandbox

    # -- container-ish --------------------------------------------------------
    def __len__(self) -> int:
        return len(self.names)

    def __contains__(self, name: object) -> bool:
        return name in self.specs

    def __iter__(self):
        return iter(self.names)

    def __repr__(self) -> str:
        return f"<CompiledPool {len(self.names)} challenges: {', '.join(self.names[:8])}>"

    @property
    def spec_list(self) -> list[ChallengeSpec]:
        return [self.specs[n] for n in self.names]

    # -- wiring ---------------------------------------------------------------
    def bind(self, sandbox: Any) -> "CompiledPool":
        """Point the pass-through helpers at `sandbox` (returns self)."""
        self.sandbox = sandbox
        return self

    def load_into(self, sandbox: Any) -> dict[str, dict[str, str]]:
        """Compile this pool's specs into another sandbox (or pool of them)."""
        return sandbox.load(self.spec_list)

    def _sb(self):
        if self.sandbox is None:
            raise SandboxError("this CompiledPool is not bound to a sandbox")
        return self.sandbox

    # -- pass-throughs --------------------------------------------------------
    def generate(self, name: str, seed: int) -> str:
        return self._sb().generate(name, seed)

    def solve(self, name: str, clue: str) -> str:
        return self._sb().solve(name, clue)

    def score(self, name: str, clue: str, solution: str) -> int:
        return self._sb().score(name, clue, solution)

    # -- round helper ---------------------------------------------------------
    def random_challenge(self, rng: random.Random) -> tuple[str, int]:
        """Pick the next ``(name, seed)`` of a round (SPEC §5 round loop)."""
        if not self.names:
            raise SandboxError("challenge pool is empty")
        return rng.choice(self.names), rng.getrandbits(32)


def load_pool(dir_or_specs: "str | Path | Iterable[Any]", config: GameConfig | None = None,
              sandbox: Any = None) -> tuple[CompiledPool, dict[str, ValidationReport]]:
    """Validate every challenge and build a `CompiledPool` of the accepted ones.

    Rejected challenges are logged with their report; loading never raises just
    because a challenge is broken (SPEC §4).
    """
    config = config or GameConfig()
    own_sandbox = False
    if sandbox is None:
        from engine.sandbox import Sandbox
        sandbox = Sandbox(config)
        own_sandbox = True

    if isinstance(dir_or_specs, (str, Path)):
        specs = ChallengeStore(dir_or_specs).list()
    else:
        specs = [s if isinstance(s, ChallengeSpec) else ChallengeSpec.from_dict(s) for s in dir_or_specs]

    reports: dict[str, ValidationReport] = {}
    accepted: list[ChallengeSpec] = []
    for spec in specs:
        key = spec.name or "<unnamed>"
        report = validate(spec, config, sandbox, existing_names=[s.name for s in accepted])
        reports[key] = report
        if report.ok:
            accepted.append(spec)
            if report.warnings:
                log.info("challenge %s accepted with warnings: %s", key, "; ".join(report.warnings))
        else:
            log.error("challenge %s REJECTED: %s", key, "; ".join(report.errors))

    try:
        sandbox.load(accepted)
    except SandboxError as e:  # pragma: no cover - only if the worker dies mid-load
        log.error("loading accepted challenges into the sandbox failed: %s", e)
        if own_sandbox:
            sandbox.close()
        raise
    pool = CompiledPool(accepted, config, sandbox)
    log.info("pool loaded: %d accepted, %d rejected", len(accepted), len(reports) - len(accepted))
    return pool, reports
