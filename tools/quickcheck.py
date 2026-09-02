#!/usr/bin/env python3
"""Reference validator for Centaur Zendo challenge generators (see SPEC.md §2–§4).

Usage:  python tools/quickcheck.py challenges/PP.json [more.json ...] [--seeds 20] [--verbose]

This is the *reference* exec model: engine/sandbox.py must behave identically
(restricted builtins, pre-imported modules, per-call wall-clock limits).
It is deliberately dependency-free so challenge authors can run it anywhere.
"""
import sys, json, time, random, signal, re, os, argparse, builtins as _b

# ---- caps (mirror GameConfig defaults) ---------------------------------------
CAPS = dict(
    max_score_code_chars=512, max_clue_chars=1024, max_generate_code_chars=50_000,
    max_solve_code_chars=5_000, max_solution_chars=1024,
    max_generate_ms=100, max_score_ms=50, max_solve_ms=2000,
    validation_seeds=20, validation_seed=12345,
)
NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,16}$")

ALLOWED_MODULES = ("math re random itertools functools collections string hashlib json heapq "
                   "bisect operator fractions statistics array struct base64 decimal words").split()
ALLOWED_BUILTINS = ("abs all any ascii bin bool bytearray bytes callable chr complex dict divmod "
                    "enumerate filter float format frozenset getattr hasattr hash hex id int isinstance "
                    "issubclass iter len list map max min next object oct ord pow print range repr "
                    "reversed round set setattr slice sorted str sum tuple type zip True False None "
                    "Exception ValueError TypeError KeyError IndexError ZeroDivisionError ArithmeticError "
                    "StopIteration RuntimeError AssertionError OverflowError LookupError RecursionError").split()


class SandboxTimeout(Exception):
    pass


def _load_module(name):
    """Import an allow-listed module; `words` is the engine's English word-list module."""
    if name == "words":
        try:
            import engine.words as words_mod
        except ImportError:
            import sys as _sys, os as _os
            _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
            import engine.words as words_mod
        return words_mod
    return __import__(name)


def _restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".")[0]
    if root not in ALLOWED_MODULES:
        raise ImportError(f"import of {name!r} is not allowed in challenge code")
    if root == "words":
        return _load_module("words")
    return __import__(name, globals, locals, fromlist, level)


def make_namespace():
    bi = {k: getattr(_b, k) for k in ALLOWED_BUILTINS if hasattr(_b, k)}
    bi["True"], bi["False"], bi["None"] = True, False, None
    bi["__import__"] = _restricted_import
    ns = {"__builtins__": bi, "__name__": "challenge"}
    for m in ALLOWED_MODULES:
        ns[m] = _load_module(m)
    return ns


def compile_source(src, name, kind, fn):
    ns = make_namespace()
    code = compile(src, f"<{name}.{kind}>", "exec")
    exec(code, ns)
    f = ns.get(fn)
    if not callable(f):
        raise ValueError(f"{kind} source must define a function named {fn}()")
    return f


def timed_call(f, args, limit_ms):
    """Call f(*args) with a wall-clock limit. Returns (value, elapsed_ms). Raises on timeout/error."""
    def handler(signum, frame):
        raise SandboxTimeout(f"exceeded {limit_ms} ms")
    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, limit_ms / 1000.0)
    t0 = time.perf_counter()
    try:
        return f(*args), (time.perf_counter() - t0) * 1000
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


def validate(spec, caps=CAPS, verbose=False):
    errors, warnings, samples = [], [], []
    timings = {"generate_ms_max": 0.0, "score_ms_max": 0.0, "solve_ms_max": 0.0}
    rep = lambda ok: dict(ok=ok, errors=errors, warnings=warnings, timings=timings, samples=samples)

    name = spec.get("name", "")
    if not isinstance(name, str) or not NAME_RE.match(name):
        errors.append("name must match [A-Za-z0-9_-]{1,16}")
    if not spec.get("description"):
        warnings.append("description is empty (private notes for organisers)")
    for kind, cap in (("generate", "max_generate_code_chars"), ("solve", "max_solve_code_chars"),
                      ("score", "max_score_code_chars")):
        src = spec.get(kind)
        if not isinstance(src, str) or not src.strip():
            errors.append(f"missing {kind} source")
        elif len(src) > caps[cap]:
            errors.append(f"{kind} source is {len(src)} chars, cap is {caps[cap]}")
    if errors:
        return rep(False)

    fns = {}
    for kind in ("generate", "solve", "score"):
        try:
            fns[kind] = compile_source(spec[kind], name, kind, kind)
        except Exception as e:
            errors.append(f"{kind}: {type(e).__name__}: {e}")
    if errors:
        return rep(False)
    gen, solve, score = fns["generate"], fns["solve"], fns["score"]

    def call_score(clue, sol, label):
        try:
            v, ms = timed_call(score, (clue, sol), caps["max_score_ms"])
        except SandboxTimeout as e:
            errors.append(f"score timed out on {label}: {e}")
            return None
        except Exception as e:
            return ("exc", f"{type(e).__name__}: {e}")
        timings["score_ms_max"] = max(timings["score_ms_max"], ms)
        return v

    rng = random.Random(caps["validation_seed"])
    accepted_junk_everything = True
    for i in range(caps["validation_seeds"]):
        seed = rng.getrandbits(32)
        tag = f"seed {seed}"
        try:
            clue, ms = timed_call(gen, (seed,), caps["max_generate_ms"])
        except Exception as e:
            errors.append(f"generate({tag}) failed: {type(e).__name__}: {e}")
            break
        timings["generate_ms_max"] = max(timings["generate_ms_max"], ms)
        if not isinstance(clue, str) or not clue:
            errors.append(f"generate({tag}) must return a non-empty str, got {type(clue).__name__}")
            break
        if len(clue) > caps["max_clue_chars"]:
            errors.append(f"generate({tag}) clue is {len(clue)} chars, cap {caps['max_clue_chars']}")
            break
        try:
            clue2, _ = timed_call(gen, (seed,), caps["max_generate_ms"])
        except Exception as e:
            errors.append(f"generate({tag}) second call failed: {e}")
            break
        if clue2 != clue:
            errors.append(f"generate({tag}) is not deterministic")
            break
        try:
            sol, ms = timed_call(solve, (clue,), caps["max_solve_ms"])
        except Exception as e:
            errors.append(f"solve({tag}) failed: {type(e).__name__}: {e}\n  clue={clue[:200]!r}")
            break
        timings["solve_ms_max"] = max(timings["solve_ms_max"], ms)
        if not isinstance(sol, str):
            errors.append(f"solve({tag}) must return str, got {type(sol).__name__}")
            break
        if len(sol) > caps["max_solution_chars"]:
            errors.append(f"solve({tag}) solution is {len(sol)} chars, cap {caps['max_solution_chars']}")
            break
        v = call_score(clue, sol, f"solve output ({tag})")
        if v != 1:
            errors.append(f"score(clue, solve(clue)) != 1 for {tag}: got {v!r}\n  clue={clue[:200]!r}\n  sol={sol[:200]!r}")
            break
        v = call_score(clue, "", f"empty solution ({tag})")
        if isinstance(v, tuple):
            warnings.append(f"score raised on empty solution ({tag}): {v[1]} (treated as 0)")
        elif v != 0:
            errors.append(f"score(clue, '') must be 0 for {tag}, got {v!r}")
            break
        junk = ["0", "1", "x", "1" * 100, clue, "".join(rng.sample(sol, len(sol))) if len(sol) > 1 else "zz"]
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
        if len(samples) < 3:
            samples.append({"seed": seed, "clue": clue, "solution": sol})
        if verbose:
            print(f"  ok {tag}: clue={clue[:60]!r} sol={sol[:60]!r}")
    if not errors and accepted_junk_everything:
        errors.append("score returned 1 for every junk input — the scorer accepts anything")
    if not errors:
        if timings["solve_ms_max"] > 0.25 * caps["max_solve_ms"]:
            warnings.append(f"solve is slowish ({timings['solve_ms_max']:.0f} ms; cap {caps['max_solve_ms']})")
        if timings["generate_ms_max"] > 0.5 * caps["max_generate_ms"]:
            warnings.append(f"generate is slowish ({timings['generate_ms_max']:.0f} ms; cap {caps['max_generate_ms']})")
    for k in timings:
        timings[k] = round(timings[k], 2)
    # de-duplicate warnings that differ only by seed
    seen, uniq = set(), []
    for w in warnings:
        key = re.sub(r"\(seed \d+\)", "", w)
        if key not in seen:
            seen.add(key); uniq.append(w)
    warnings[:] = uniq
    return rep(not errors)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--seeds", type=int, default=CAPS["validation_seeds"])
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--json", action="store_true", help="print reports as JSON")
    ap.add_argument("--cap", action="append", default=[], metavar="KEY=VALUE",
                    help="override a cap, e.g. --cap max_score_code_chars=1024")
    a = ap.parse_args(argv)
    caps = dict(CAPS, validation_seeds=a.seeds)
    for kv in a.cap:
        k, v = kv.split("=", 1)
        caps[k] = type(CAPS[k])(v)
    bad = 0
    for path in a.files:
        with open(path) as f:
            spec = json.load(f)
        r = validate(spec, caps, a.verbose)
        if a.json:
            print(json.dumps({"file": path, **r}, indent=1))
            continue
        status = "OK  " if r["ok"] else "FAIL"
        print(f"{status} {spec.get('name','?'):<10} {path}  gen={r['timings']['generate_ms_max']}ms "
              f"score={r['timings']['score_ms_max']}ms solve={r['timings']['solve_ms_max']}ms")
        for e in r["errors"]:
            print("   ERROR:", e)
        for w in r["warnings"]:
            print("   warn :", w)
        if r["ok"] and a.verbose:
            for s in r["samples"]:
                print(f"   sample seed={s['seed']}: clue={s['clue']!r}\n                 sol={s['solution']!r}")
        bad += not r["ok"]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
