"""Restricted execution model + sandbox workers (SPEC §3).

Two layers live here:

* the **exec model** -- `make_namespace()` / `compile_source()` / `timed_call()`.
  This is byte-for-byte the model implemented by ``tools/quickcheck.py`` (same
  allowed builtins, same pre-imported modules, same restricted ``__import__``);
  ``engine/tests/test_sandbox.py`` asserts the two agree.
* the **workers** -- `Sandbox` (one forked subprocess talking over a pipe, with
  per-call `signal.setitimer` limits inside and a hard kill from the parent at
  ``timeout + 250 ms``), `InProcessSandbox` (same API, no subprocess, for tests
  and tools) and `SandboxPool` (N workers with an async API so the aiohttp event
  loop is never blocked).

Honesty note: this is a *game* sandbox -- restricted builtins, wall-clock limits
and process isolation. It is not a security boundary against a determined
attacker. Challenge submissions must be reviewed by an organiser before being
loaded into a live pool.
"""
from __future__ import annotations

import asyncio
import atexit
import builtins as _b
import contextlib
import logging
import multiprocessing
import os
import signal
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping, Sequence

from engine.config import GameConfig

log = logging.getLogger("centaur.sandbox")

__all__ = [
    "ALLOWED_MODULES", "ALLOWED_BUILTINS", "SandboxError", "SandboxTimeout",
    "make_namespace", "compile_source", "timed_call", "Unpicklable",
    "Sandbox", "InProcessSandbox", "SandboxPool", "AsyncSandbox",
]

# ---------------------------------------------------------------- exec model
# NOTE: these two lists must stay identical to tools/quickcheck.py.
ALLOWED_MODULES = ("math re random itertools functools collections string hashlib json heapq "
                   "bisect operator fractions statistics array struct base64 decimal").split()
ALLOWED_BUILTINS = ("abs all any ascii bin bool bytearray bytes callable chr complex dict divmod "
                    "enumerate filter float format frozenset getattr hasattr hash hex id int isinstance "
                    "issubclass iter len list map max min next object oct ord pow print range repr "
                    "reversed round set setattr slice sorted str sum tuple type zip True False None "
                    "Exception ValueError TypeError KeyError IndexError ZeroDivisionError ArithmeticError "
                    "StopIteration RuntimeError AssertionError OverflowError LookupError RecursionError").split()

#: grace period the parent adds on top of a call's own limit before killing the worker
KILL_GRACE_S = 0.25

KINDS = ("generate", "solve", "score")


class SandboxError(Exception):
    """Any failure of challenge code: exception, bad type, dead worker."""


class SandboxTimeout(SandboxError):
    """Challenge code exceeded its wall-clock limit."""


@dataclass
class Unpicklable:
    """Stand-in for a return value that cannot cross the pipe (wrong type anyway)."""
    type_name: str
    repr: str = ""

    def __str__(self) -> str:  # pragma: no cover - debugging aid
        return f"<{self.type_name} {self.repr}>"


def type_name_of(value: Any) -> str:
    """Name of the type a challenge function actually returned."""
    return value.type_name if isinstance(value, Unpicklable) else type(value).__name__


def _restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".")[0]
    if root not in ALLOWED_MODULES:
        raise ImportError(f"import of {name!r} is not allowed in challenge code")
    return __import__(name, globals, locals, fromlist, level)


def make_namespace() -> dict[str, Any]:
    """A fresh globals dict for challenge code: restricted builtins + pre-imported modules."""
    bi = {k: getattr(_b, k) for k in ALLOWED_BUILTINS if hasattr(_b, k)}
    bi["True"], bi["False"], bi["None"] = True, False, None
    bi["__import__"] = _restricted_import
    ns = {"__builtins__": bi, "__name__": "challenge"}
    for m in ALLOWED_MODULES:
        ns[m] = __import__(m)
    return ns


def compile_source(src: str, name: str, kind: str, fn: str | None = None) -> Callable[..., Any]:
    """Compile+exec one challenge source and return the required callable.

    Raises SyntaxError / ValueError / whatever the module body raises.
    """
    fn = fn or kind
    ns = make_namespace()
    code = compile(src, f"<{name}.{kind}>", "exec")
    exec(code, ns)
    f = ns.get(fn)
    if not callable(f):
        raise ValueError(f"{kind} source must define a function named {fn}()")
    return f


def timed_call(f: Callable[..., Any], args: Sequence[Any], limit_ms: float) -> tuple[Any, float]:
    """Call ``f(*args)`` under a wall-clock limit; returns ``(value, elapsed_ms)``.

    Raises `SandboxTimeout` when the limit is hit (via ``SIGALRM``) and lets any
    exception from ``f`` propagate. ``SIGALRM`` can only be armed on the main
    thread; off the main thread the call is timed but not interrupted (the
    subprocess parent still hard-kills a runaway worker).
    """
    def handler(signum, frame):
        raise SandboxTimeout(f"exceeded {limit_ms:g} ms")

    on_main = threading.current_thread() is threading.main_thread()
    old = signal.signal(signal.SIGALRM, handler) if on_main else None
    if on_main:
        signal.setitimer(signal.ITIMER_REAL, limit_ms / 1000.0)
    t0 = time.perf_counter()
    try:
        value = f(*args)
        elapsed = (time.perf_counter() - t0) * 1000
    finally:
        if on_main:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)
    if not on_main and elapsed > limit_ms:
        raise SandboxTimeout(f"exceeded {limit_ms:g} ms (uninterruptible: not the main thread)")
    return value, elapsed


def _wire(value: Any) -> Any:
    """Make a return value safe to pickle back to the parent."""
    if isinstance(value, (str, int, float, bool, bytes)) or value is None:
        return value
    try:
        r = repr(value)[:200]
    except Exception:  # pragma: no cover - hostile __repr__
        r = "<unrepresentable>"
    return Unpicklable(type(value).__name__, r)


def _limit_for(config: GameConfig, op: str) -> float:
    return float({"generate": config.max_generate_ms,
                  "solve": config.max_solve_ms,
                  "score": config.max_score_ms}[op])


def _spec_to_dict(spec: Any) -> dict[str, Any]:
    """Accept a ChallengeSpec, a mapping, or anything with .to_dict()."""
    if isinstance(spec, Mapping):
        d = dict(spec)
    elif hasattr(spec, "to_dict"):
        d = dict(spec.to_dict())
    else:  # pragma: no cover - defensive
        raise TypeError(f"cannot use {type(spec).__name__} as a challenge spec")
    return {"name": d.get("name", ""), "generate": d.get("generate", ""),
            "solve": d.get("solve", ""), "score": d.get("score", "")}


# ---------------------------------------------------------------- the worker
def _compile_spec(spec: dict[str, Any]) -> tuple[dict[str, Callable[..., Any]], dict[str, str]]:
    """Compile all three sources of one spec. Returns (functions, {kind: error})."""
    fns: dict[str, Callable[..., Any]] = {}
    errs: dict[str, str] = {}
    name = spec.get("name") or "?"
    for kind in KINDS:
        src = spec.get(kind)
        if not isinstance(src, str) or not src.strip():
            errs[kind] = f"missing {kind} source"
            continue
        try:
            fns[kind] = compile_source(src, name, kind)
        except Exception as e:
            errs[kind] = f"{type(e).__name__}: {e}"
    return fns, errs


def _worker_main(conn, caps: dict[str, Any]) -> None:  # pragma: no cover - runs in child
    """Child process main loop. Speaks the little request/response protocol below.

    request:  ("load", [spec,...]) | ("add", spec) | ("call", op, name, args, limit_ms) | ("ping",) | ("close",)
    response: ("ok", value, elapsed_ms) | ("err", {"timeout": bool, "type": str, "msg": str})
    """
    with contextlib.suppress(Exception):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    registry: dict[str, dict[str, Callable[..., Any]]] = {}
    while True:
        try:
            msg = conn.recv()
        except (EOFError, KeyboardInterrupt, OSError):
            break
        op = msg[0]
        try:
            if op == "close":
                break
            if op == "ping":
                conn.send(("ok", None, 0.0))
                continue
            if op == "load":
                registry.clear()
                report: dict[str, dict[str, str]] = {}
                for spec in msg[1]:
                    fns, errs = _compile_spec(spec)
                    if errs:
                        report[spec.get("name", "?")] = errs
                    else:
                        registry[spec["name"]] = fns
                conn.send(("ok", report, 0.0))
                continue
            if op == "add":
                spec = msg[1]
                fns, errs = _compile_spec(spec)
                if not errs:
                    registry[spec["name"]] = fns
                else:
                    registry.pop(spec.get("name", ""), None)
                conn.send(("ok", errs, 0.0))
                continue
            if op == "call":
                _, call_op, name, args, limit_ms = msg
                entry = registry.get(name)
                if entry is None:
                    conn.send(("err", {"timeout": False, "type": "KeyError",
                                       "msg": f"challenge {name!r} is not loaded in this worker"}))
                    continue
                try:
                    value, ms = timed_call(entry[call_op], args, limit_ms)
                except SandboxTimeout as e:
                    conn.send(("err", {"timeout": True, "type": "SandboxTimeout", "msg": str(e)}))
                    continue
                except BaseException as e:
                    conn.send(("err", {"timeout": False, "type": type(e).__name__, "msg": str(e)[:500]}))
                    continue
                conn.send(("ok", _wire(value), ms))
                continue
            conn.send(("err", {"timeout": False, "type": "ValueError", "msg": f"unknown op {op!r}"}))
        except (BrokenPipeError, EOFError, OSError):
            break
        except BaseException as e:  # never let the worker die silently
            with contextlib.suppress(Exception):
                conn.send(("err", {"timeout": False, "type": type(e).__name__, "msg": str(e)[:500]}))
    with contextlib.suppress(Exception):
        conn.close()
    os._exit(0)


def _mp_context():
    """'fork' where available (fast, ~1 ms per worker), else 'spawn'."""
    for method in ("fork", "spawn"):
        try:
            return multiprocessing.get_context(method)
        except ValueError:  # pragma: no cover - platform dependent
            continue
    return multiprocessing.get_context()  # pragma: no cover


# ---------------------------------------------------------------- parent side
class _SandboxBase:
    """Shared behaviour of Sandbox and InProcessSandbox."""

    config: GameConfig

    # -- subclasses implement -------------------------------------------------
    def load(self, specs: Iterable[Any]) -> dict[str, dict[str, str]]: ...
    def add(self, spec: Any) -> dict[str, str]: ...
    def call_timed(self, op: str, name: str, args: Sequence[Any]) -> tuple[Any, float]: ...
    def close(self) -> None: ...

    # -- the SPEC §3 API ------------------------------------------------------
    def generate(self, name: str, seed: int) -> str:
        value, _ = self.generate_timed(name, seed)
        if not isinstance(value, str):
            raise SandboxError(f"{name}.generate returned {type_name_of(value)}, expected str")
        return value

    def generate_timed(self, name: str, seed: int) -> tuple[Any, float]:
        return self.call_timed("generate", name, (int(seed),))

    def solve(self, name: str, clue: str) -> str:
        value, _ = self.solve_timed(name, clue)
        if not isinstance(value, str):
            raise SandboxError(f"{name}.solve returned {type_name_of(value)}, expected str")
        return value

    def solve_timed(self, name: str, clue: str) -> tuple[Any, float]:
        return self.call_timed("solve", name, (clue,))

    def score(self, name: str, clue: str, solution: str) -> int:
        """Never raises: any failure, timeout or non-0/1 return counts as 0 (SPEC §2)."""
        try:
            value, _ = self.score_timed(name, clue, solution)
        except Exception as e:
            log.debug("score(%s) failed: %s", name, e)
            return 0
        return 1 if value is True or value == 1 else 0

    def score_timed(self, name: str, clue: str, solution: str) -> tuple[Any, float]:
        """Like `score` but raises SandboxError/SandboxTimeout — used by validation."""
        return self.call_timed("score", name, (clue, solution))

    # -- convenience ----------------------------------------------------------
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


_LIVE: "set[Sandbox]" = set()


@atexit.register
def _close_live_sandboxes() -> None:  # pragma: no cover - interpreter shutdown
    for sb in list(_LIVE):
        with contextlib.suppress(Exception):
            sb.close()


class Sandbox(_SandboxBase):
    """One challenge-code worker process.

    Calls are synchronous and *not* thread-safe as a unit — a lock serialises
    them so a misuse degrades into queueing rather than a corrupted pipe. Use
    `SandboxPool` for concurrency.
    """

    def __init__(self, config: GameConfig | None = None, *, start: bool = True):
        self.config = config or GameConfig()
        self._specs: list[dict[str, Any]] = []
        self._ctx = _mp_context()
        self._proc = None
        self._conn = None
        self._lock = threading.RLock()
        self._closed = False
        self.restarts = 0
        _LIVE.add(self)
        if start:
            self._spawn()

    # ---- process lifecycle --------------------------------------------------
    @property
    def alive(self) -> bool:
        return bool(self._proc is not None and self._proc.is_alive())

    def _spawn(self) -> None:
        parent, child = self._ctx.Pipe(duplex=True)
        proc = self._ctx.Process(target=_worker_main, args=(child, self.config.caps_dict()),
                                 name="zendo-sandbox", daemon=True)
        proc.start()
        child.close()
        self._proc, self._conn = proc, parent
        self._closed = False

    def _kill(self) -> None:
        proc, conn = self._proc, self._conn
        self._proc, self._conn = None, None
        if conn is not None:
            with contextlib.suppress(Exception):
                conn.close()
        if proc is not None:
            with contextlib.suppress(Exception):
                if proc.is_alive():
                    proc.terminate()
                    proc.join(0.2)
                if proc.is_alive():
                    proc.kill()
                    proc.join(0.5)
            with contextlib.suppress(Exception):
                proc.close()

    def restart(self) -> None:
        """Kill the worker, spawn a fresh one and re-load the current specs."""
        with self._lock:
            self._kill()
            self.restarts += 1
            self._spawn()
            if self._specs:
                self._send_recv(("load", self._specs), timeout=30.0)

    def close(self) -> None:
        with self._lock:
            if self._proc is not None and self._conn is not None:
                with contextlib.suppress(Exception):
                    self._conn.send(("close",))
                    self._proc.join(0.5)
            self._kill()
            self._closed = True
        _LIVE.discard(self)

    # ---- pipe plumbing ------------------------------------------------------
    def _send_recv(self, msg: tuple, timeout: float) -> tuple:
        """Send one request, wait `timeout` seconds for the reply.

        On silence the worker is killed, respawned (and re-loaded) and a
        SandboxTimeout is raised.
        """
        if self._closed:
            raise SandboxError("sandbox is closed")
        if not self.alive:
            self.restart()
        try:
            self._conn.send(msg)
        except (BrokenPipeError, OSError) as e:
            self.restart()
            raise SandboxError(f"sandbox worker died: {e}") from None
        try:
            ready = self._conn.poll(timeout)
        except (BrokenPipeError, OSError) as e:
            self.restart()
            raise SandboxError(f"sandbox worker died: {e}") from None
        if not ready:
            self.restart()
            raise SandboxTimeout(f"worker unresponsive after {timeout * 1000:.0f} ms; killed and respawned")
        try:
            return self._conn.recv()
        except (EOFError, OSError) as e:
            self.restart()
            raise SandboxError(f"sandbox worker died: {e}") from None

    # ---- API ----------------------------------------------------------------
    def load(self, specs: Iterable[Any]) -> dict[str, dict[str, str]]:
        """Compile every spec in the worker. Returns {name: {kind: error}} for failures."""
        payload = [_spec_to_dict(s) for s in specs]
        with self._lock:
            self._specs = payload
            kind, report, _ms = self._send_recv(("load", payload), timeout=60.0)
            if kind != "ok":
                raise SandboxError(f"load failed: {report}")
            return report

    def add(self, spec: Any) -> dict[str, str]:
        """Compile one extra spec into the worker. Returns {kind: error} (empty = ok)."""
        payload = _spec_to_dict(spec)
        with self._lock:
            self._specs = [s for s in self._specs if s["name"] != payload["name"]] + [payload]
            kind, errs, _ms = self._send_recv(("add", payload), timeout=60.0)
            if kind != "ok":
                raise SandboxError(f"add failed: {errs}")
            return errs

    def ping(self) -> bool:
        with self._lock:
            try:
                return self._send_recv(("ping",), timeout=5.0)[0] == "ok"
            except SandboxError:
                return False

    def call_timed(self, op: str, name: str, args: Sequence[Any]) -> tuple[Any, float]:
        limit_ms = _limit_for(self.config, op)
        with self._lock:
            reply = self._send_recv(("call", op, name, tuple(args), limit_ms),
                                    timeout=limit_ms / 1000.0 + KILL_GRACE_S)
        if reply[0] == "ok":
            return reply[1], reply[2]
        info = reply[1]
        msg = f"{name}.{op}: {info['type']}: {info['msg']}"
        raise (SandboxTimeout if info.get("timeout") else SandboxError)(msg)

    @property
    def names(self) -> list[str]:
        return [s["name"] for s in self._specs]


class InProcessSandbox(_SandboxBase):
    """Same API as `Sandbox` with no subprocess — for tests, tools and the webapp.

    Time limits still apply (SIGALRM on the main thread), but a C-level hang
    cannot be interrupted and there is no memory/process isolation. Never use
    this for code you have not read.
    """

    def __init__(self, config: GameConfig | None = None):
        self.config = config or GameConfig()
        self._fns: dict[str, dict[str, Callable[..., Any]]] = {}
        self._specs: dict[str, dict[str, Any]] = {}

    def load(self, specs: Iterable[Any]) -> dict[str, dict[str, str]]:
        self._fns.clear()
        self._specs.clear()
        report: dict[str, dict[str, str]] = {}
        for spec in specs:
            errs = self.add(spec)
            if errs:
                report[_spec_to_dict(spec)["name"]] = errs
        return report

    def add(self, spec: Any) -> dict[str, str]:
        payload = _spec_to_dict(spec)
        fns, errs = _compile_spec(payload)
        if errs:
            self._fns.pop(payload["name"], None)
            self._specs.pop(payload["name"], None)
        else:
            self._fns[payload["name"]] = fns
            self._specs[payload["name"]] = payload
        return errs

    def call_timed(self, op: str, name: str, args: Sequence[Any]) -> tuple[Any, float]:
        entry = self._fns.get(name)
        if entry is None:
            raise SandboxError(f"challenge {name!r} is not loaded")
        limit_ms = _limit_for(self.config, op)
        try:
            value, ms = timed_call(entry[op], args, limit_ms)
        except SandboxTimeout:
            raise
        except BaseException as e:
            raise SandboxError(f"{name}.{op}: {type(e).__name__}: {e}") from None
        return _wire(value), ms

    def ping(self) -> bool:
        return True

    def close(self) -> None:
        self._fns.clear()
        self._specs.clear()

    @property
    def names(self) -> list[str]:
        return sorted(self._specs)


# ---------------------------------------------------------------- async layer
class AsyncSandbox:
    """Async facade over one `Sandbox`: every call runs in a worker thread."""

    def __init__(self, sandbox: _SandboxBase, executor: ThreadPoolExecutor):
        self.sync = sandbox
        self._executor = executor

    async def _run(self, fn, *args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, fn, *args)

    async def generate(self, name: str, seed: int) -> str:
        return await self._run(self.sync.generate, name, seed)

    async def solve(self, name: str, clue: str) -> str:
        return await self._run(self.sync.solve, name, clue)

    async def score(self, name: str, clue: str, solution: str) -> int:
        return await self._run(self.sync.score, name, clue, solution)

    async def generate_timed(self, name: str, seed: int):
        return await self._run(self.sync.generate_timed, name, seed)

    async def solve_timed(self, name: str, clue: str):
        return await self._run(self.sync.solve_timed, name, clue)

    async def score_timed(self, name: str, clue: str, solution: str):
        return await self._run(self.sync.score_timed, name, clue, solution)

    async def load(self, specs: Iterable[Any]):
        return await self._run(self.sync.load, list(specs))

    async def add(self, spec: Any):
        return await self._run(self.sync.add, spec)

    @property
    def names(self) -> list[str]:
        return self.sync.names


class _Acquire:
    """Async context manager returned by `SandboxPool.acquire()`."""

    def __init__(self, pool: "SandboxPool"):
        self._pool = pool
        self._sb: AsyncSandbox | None = None

    async def __aenter__(self) -> AsyncSandbox:
        self._sb = await self._pool._take()
        return self._sb

    async def __aexit__(self, *exc):
        if self._sb is not None:
            self._pool._give_back(self._sb)
            self._sb = None
        return False

    def __await__(self):  # pragma: no cover - `sb = await pool.acquire()` also works
        return self.__aenter__().__await__()


class SandboxPool:
    """`config.sandbox_workers` sandbox processes with an async API.

        async with pool.acquire() as sb:      # one round holds one worker
            clue = await sb.generate(name, seed)

        score = await pool.score(name, clue, solution)   # acquire+call+release
    """

    def __init__(self, config: GameConfig | None = None, size: int | None = None, *,
                 sandbox_factory: Callable[[GameConfig], _SandboxBase] | None = None):
        self.config = config or GameConfig()
        self.size = int(size or self.config.sandbox_workers)
        self._factory = sandbox_factory or (lambda cfg: Sandbox(cfg))
        self._executor = ThreadPoolExecutor(max_workers=self.size, thread_name_prefix="sandbox")
        self._sandboxes: list[AsyncSandbox] = []
        self._free: asyncio.LifoQueue | None = None
        self._start_lock = asyncio.Lock()
        self._specs: list[Any] = []
        self._closed = False

    # ---- lifecycle ----------------------------------------------------------
    async def start(self) -> None:
        if self._free is not None:
            return
        async with self._start_lock:
            if self._free is not None:
                return
            queue: asyncio.LifoQueue = asyncio.LifoQueue()
            for _ in range(self.size):
                sb = AsyncSandbox(self._factory(self.config), self._executor)
                self._sandboxes.append(sb)
                queue.put_nowait(sb)
            self._free = queue

    async def load(self, specs: Iterable[Any]) -> dict[str, dict[str, str]]:
        """Load the same specs into every worker; returns one merged failure report."""
        await self.start()
        self._specs = list(specs)
        reports = await asyncio.gather(*(sb.load(self._specs) for sb in self._sandboxes))
        merged: dict[str, dict[str, str]] = {}
        for r in reports:
            merged.update(r)
        return merged

    async def close(self) -> None:
        self._closed = True
        for sb in self._sandboxes:
            with contextlib.suppress(Exception):
                sb.sync.close()
        self._sandboxes.clear()
        self._free = None
        self._executor.shutdown(wait=False)

    # ---- acquisition --------------------------------------------------------
    def acquire(self) -> _Acquire:
        return _Acquire(self)

    async def _take(self) -> AsyncSandbox:
        if self._closed:
            raise SandboxError("pool is closed")
        await self.start()
        assert self._free is not None
        return await self._free.get()

    def _give_back(self, sb: AsyncSandbox) -> None:
        if self._free is not None:
            self._free.put_nowait(sb)

    # ---- one-shot helpers ---------------------------------------------------
    async def generate(self, name: str, seed: int) -> str:
        async with self.acquire() as sb:
            return await sb.generate(name, seed)

    async def solve(self, name: str, clue: str) -> str:
        async with self.acquire() as sb:
            return await sb.solve(name, clue)

    async def score(self, name: str, clue: str, solution: str) -> int:
        async with self.acquire() as sb:
            return await sb.score(name, clue, solution)

    @property
    def names(self) -> list[str]:
        return self._sandboxes[0].names if self._sandboxes else []
