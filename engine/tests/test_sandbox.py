"""Tests for the exec model and the sandbox workers (SPEC §3)."""
import asyncio
import importlib.util
import json
import sys
import time
from pathlib import Path

import pytest

from engine.config import GameConfig
from engine.sandbox import (ALLOWED_BUILTINS, ALLOWED_MODULES, InProcessSandbox, Sandbox,
                            SandboxError, SandboxPool, SandboxTimeout, compile_source,
                            make_namespace)

ROOT = Path(__file__).resolve().parents[2]

# ------------------------------------------------------------------ fixtures
TRIVIAL = {
    "name": "TRIV",
    "generate": "def generate(seed):\n    r = random.Random(seed)\n    return str(r.randrange(100, 999))\n",
    "solve": "def solve(clue):\n    return clue[::-1]\n",
    "score": "def score(clue, solution):\n    return int(solution == clue[::-1])\n",
}


def spec(name="T", generate=None, solve=None, score=None):
    return {"name": name,
            "generate": generate or TRIVIAL["generate"],
            "solve": solve or TRIVIAL["solve"],
            "score": score or TRIVIAL["score"]}


def gen_returning(expr):
    return f"def generate(seed):\n    return {expr}\n"


@pytest.fixture(scope="module")
def config():
    return GameConfig(max_generate_ms=100, max_score_ms=50, max_solve_ms=300)


@pytest.fixture
def sb(config):
    s = Sandbox(config)
    try:
        yield s
    finally:
        s.close()


@pytest.fixture(scope="module")
def quickcheck():
    """tools/quickcheck.py imported by path (it must stay import-free of engine)."""
    path = ROOT / "tools" / "quickcheck.py"
    spec_ = importlib.util.spec_from_file_location("quickcheck_ref", path)
    mod = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------ exec model
def test_exec_model_matches_quickcheck(quickcheck):
    """The engine and the standalone author tool must sandbox identically."""
    assert ALLOWED_BUILTINS == quickcheck.ALLOWED_BUILTINS
    assert ALLOWED_MODULES == quickcheck.ALLOWED_MODULES
    ours, theirs = make_namespace(), quickcheck.make_namespace()
    assert sorted(ours) == sorted(theirs)
    assert sorted(ours["__builtins__"]) == sorted(theirs["__builtins__"])


def test_quickcheck_runs_standalone(tmp_path):
    """quickcheck must work for authors who only have the tool and their JSON file."""
    import subprocess
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "quickcheck.py"),
                        str(ROOT / "challenges" / "PP.json")],
                       cwd=tmp_path, capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin", "HOME": str(tmp_path)})
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK" in r.stdout


def test_namespace_preimports_modules():
    ns = make_namespace()
    for m in ALLOWED_MODULES:
        assert m in ns, f"{m} should be pre-imported"
    assert "os" not in ns and "sys" not in ns


@pytest.mark.parametrize("banned", ["open", "eval", "exec", "compile", "input",
                                    "globals", "locals", "vars", "__import__"])
def test_banned_builtins_absent_from_namespace(banned):
    ns = make_namespace()
    if banned == "__import__":
        assert ns["__builtins__"]["__import__"] is not __import__  # restricted version
    else:
        assert banned not in ns["__builtins__"]


@pytest.mark.parametrize("expr", [
    "open('/etc/passwd').read()",
    "eval('1+1')",
    "exec('x=1')",
    "compile('1', 'x', 'eval')",
    "globals()",
    "vars()",
])
def test_restricted_builtins_blocked_at_runtime(sb, expr):
    sb.load([spec(generate=gen_returning(expr))])
    with pytest.raises(SandboxError) as e:
        sb.generate("T", 1)
    assert "NameError" in str(e.value)


def test_import_os_blocked(sb):
    sb.load([spec(generate="def generate(seed):\n    import os\n    return os.getcwd()\n")])
    with pytest.raises(SandboxError) as e:
        sb.generate("T", 1)
    assert "ImportError" in str(e.value)


def test_import_of_allowed_modules_works(sb):
    src = ("def generate(seed):\n"
           "    import hashlib, itertools\n"
           "    h = hashlib.sha256(str(seed).encode()).hexdigest()[:8]\n"
           "    return h + str(len(list(itertools.permutations('abc'))))\n")
    sb.load([spec(generate=src)])
    assert sb.generate("T", 7).endswith("6")


def test_all_allowed_modules_are_usable(sb):
    src = "def generate(seed):\n    return str(len([" + ", ".join(ALLOWED_MODULES) + "]))\n"
    sb.load([spec(generate=src)])
    assert sb.generate("T", 1) == str(len(ALLOWED_MODULES))


def test_class_definitions_do_not_work(sb):
    """__build_class__ is not exposed — documented consequence of the exec model."""
    src = "class Foo:\n    pass\n\ndef generate(seed):\n    return 'x'\n"
    report = sb.load([spec(generate=src)])
    assert "generate" in report["T"] and "NameError" in report["T"]["generate"]


def test_compile_source_requires_the_named_function():
    with pytest.raises(ValueError):
        compile_source("def nope(x):\n    return x\n", "T", "generate")
    with pytest.raises(SyntaxError):
        compile_source("def generate(:\n", "T", "generate")


# ------------------------------------------------------------------ basic API
def test_generate_solve_score_roundtrip(sb):
    sb.load([spec()])
    clue = sb.generate("T", 42)
    assert clue == sb.generate("T", 42)          # determinism
    sol = sb.solve("T", clue)
    assert sb.score("T", clue, sol) == 1
    assert sb.score("T", clue, "") == 0


def test_pp_challenge_runs_in_the_sandbox(sb):
    pp = json.loads((ROOT / "challenges" / "PP.json").read_text())
    assert sb.load([pp]) == {}
    clue = sb.generate("PP", 12345)
    sol = sb.solve("PP", clue)
    assert clue in sol and sb.score("PP", clue, sol) == 1


def test_score_never_raises(sb):
    sb.load([
        spec("BOOM", score="def score(c, s):\n    raise ValueError('boom')\n"),
        spec("SLOW", score="def score(c, s):\n    while True:\n        pass\n"),
        spec("WEIRD", score="def score(c, s):\n    return 'yes'\n"),
    ])
    assert sb.score("BOOM", "a", "b") == 0
    assert sb.score("SLOW", "a", "b") == 0        # timeout inside the worker
    assert sb.score("WEIRD", "a", "b") == 0       # non-0/1 return
    assert sb.score("NOPE", "a", "b") == 0        # unknown challenge
    assert sb.generate("BOOM", 1)                 # worker still healthy


def test_wrong_return_types_raise(sb):
    sb.load([spec("INT", generate=gen_returning("42")),
             spec("OBJ", generate=gen_returning("object()"))])
    for name, expected in (("INT", "int"), ("OBJ", "object")):
        with pytest.raises(SandboxError) as e:
            sb.generate(name, 1)
        assert expected in str(e.value)


def test_load_reports_compile_errors_without_raising(sb):
    report = sb.load([spec("GOOD"), spec("BAD", generate="def generate(:\n")])
    assert "GOOD" not in report
    assert "SyntaxError" in report["BAD"]["generate"]
    assert sb.generate("GOOD", 1)                 # the good one still loaded


# ------------------------------------------------------------------ timeouts
def test_python_level_timeout_and_recovery(sb):
    """A pure-Python infinite loop is stopped by SIGALRM inside the worker."""
    sb.load([spec("HANG", generate="def generate(seed):\n    while True:\n        pass\n"),
             spec("OK")])
    before = sb.restarts
    t0 = time.perf_counter()
    with pytest.raises(SandboxTimeout):
        sb.generate("HANG", 1)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert elapsed_ms < 400, f"took {elapsed_ms:.0f} ms, should stop at ~100 ms"
    assert sb.restarts == before                  # no kill needed
    assert sb.generate("OK", 1)                   # same worker still usable


def test_c_level_hang_is_killed_by_the_parent(sb):
    """`sum(range(10**12))` never runs bytecode, so only the parent can stop it."""
    sb.load([spec("CHANG", generate="def generate(seed):\n    return str(sum(range(10 ** 12)))\n"),
             spec("OK")])
    before = sb.restarts
    t0 = time.perf_counter()
    with pytest.raises(SandboxTimeout) as e:
        sb.generate("CHANG", 1)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert "unresponsive" in str(e.value)
    assert elapsed_ms < 1500, f"parent took {elapsed_ms:.0f} ms to kill the worker"
    assert sb.restarts == before + 1              # killed and respawned
    assert sb.alive and sb.ping()
    assert sb.generate("OK", 1)                   # specs were re-loaded into the new worker
    assert sb.score("OK", "abc", "cba") == 1


def test_catastrophic_regex_is_also_survivable(sb):
    src = ("def generate(seed):\n"
           "    return str(bool(re.match(r'(a+)+b$', 'a' * 40)))\n")
    sb.load([spec("RE", generate=src), spec("OK")])
    with pytest.raises(SandboxTimeout):
        sb.generate("RE", 1)
    assert sb.generate("OK", 1)


def test_solve_timeout_uses_the_solve_cap(sb, config):
    sb.load([spec("SHANG", solve="def solve(clue):\n    while True:\n        pass\n")])
    t0 = time.perf_counter()
    with pytest.raises(SandboxTimeout):
        sb.solve("SHANG", "abc")
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert config.max_solve_ms * 0.5 < elapsed_ms < config.max_solve_ms + 600


# ------------------------------------------------------------------ overhead
def test_per_call_overhead_is_small(sb, capsys):
    """Target from the spec discussion: < 0.5 ms round trip on a warm worker."""
    sb.load([{"name": "NOP",
              "generate": "def generate(seed):\n    return 'c'\n",
              "solve": "def solve(clue):\n    return clue\n",
              "score": "def score(clue, solution):\n    return 1\n"}])
    for _ in range(50):                            # warm up
        sb.score("NOP", "c", "c")
    n = 400
    t0 = time.perf_counter()
    for i in range(n):
        sb.generate("NOP", i)
    gen_us = (time.perf_counter() - t0) / n * 1e6
    t0 = time.perf_counter()
    for _ in range(n):
        sb.score("NOP", "c", "c")
    score_us = (time.perf_counter() - t0) / n * 1e6
    with capsys.disabled():
        print(f"\n[sandbox overhead] generate {gen_us:.0f} us/call, score {score_us:.0f} us/call "
              f"({n} calls each, warm forked worker)")
    assert gen_us < 1500 and score_us < 1500       # generous CI headroom; typically ~60 us


# ------------------------------------------------------------------ in-process
def test_inprocess_sandbox_matches_subprocess(sb, config):
    ip = InProcessSandbox(config)
    pp = json.loads((ROOT / "challenges" / "PP.json").read_text())
    assert ip.load([pp]) == {} and sb.load([pp]) == {}
    for seed in (1, 2, 3):
        clue = ip.generate("PP", seed)
        assert clue == sb.generate("PP", seed)
        sol = ip.solve("PP", clue)
        assert ip.score("PP", clue, sol) == sb.score("PP", clue, sol) == 1
    ip.close()


def test_inprocess_sandbox_enforces_limits_and_never_raises_in_score(config):
    ip = InProcessSandbox(config)
    ip.load([spec("HANG", generate="def generate(seed):\n    while True:\n        pass\n")])
    with pytest.raises(SandboxTimeout):
        ip.generate("HANG", 1)
    assert ip.score("HANG", "a", "b") == 0
    ip.close()


# ------------------------------------------------------------------ async pool
def test_pool_runs_concurrently_without_blocking_the_loop(config):
    slow = ("def solve(clue):\n"
            "    t = 0\n"
            "    for i in range(200000):\n"
            "        t += i\n"
            "    return clue[::-1]\n")

    async def main():
        pool = SandboxPool(config, size=3)
        await pool.load([spec("A"), spec("SLOW", solve=slow)])
        try:
            ticks = 0
            stop = False

            async def heartbeat():
                nonlocal ticks
                while not stop:
                    await asyncio.sleep(0.005)
                    ticks += 1

            hb = asyncio.create_task(heartbeat())
            t0 = time.perf_counter()
            clues = await asyncio.gather(*(pool.generate("A", i) for i in range(9)))
            sols = await asyncio.gather(*(pool.solve("SLOW", c) for c in clues))
            scores = await asyncio.gather(*(pool.score("A", c, s) for c, s in zip(clues, sols)))
            elapsed = time.perf_counter() - t0
            stop = True
            await hb
            assert all(s == 1 for s in scores)
            assert len(set(clues)) > 1
            assert ticks > 0, "event loop was blocked while the sandbox worked"

            # one worker per acquire, released back to the pool afterwards
            async with pool.acquire() as sb1:
                async with pool.acquire() as sb2:
                    assert sb1 is not sb2
                    assert await sb1.generate("A", 5) == await sb2.generate("A", 5)
            return elapsed
        finally:
            await pool.close()

    asyncio.run(main())


def test_pool_survives_a_wedged_worker(config):
    async def main():
        pool = SandboxPool(config, size=2)
        await pool.load([spec("CHANG", generate="def generate(seed):\n    return str(sum(range(10 ** 12)))\n"),
                         spec("OK")])
        try:
            with pytest.raises(SandboxTimeout):
                await pool.generate("CHANG", 1)
            assert await pool.generate("OK", 1)
            assert await pool.score("OK", "abc", "cba") == 1
        finally:
            await pool.close()

    asyncio.run(main())
