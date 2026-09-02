"""Tests for specs, the store, SPEC §4 validation and the compiled pool."""
import json
import random
import time
from pathlib import Path

import pytest

from engine.challenges import (ChallengeSpec, ChallengeStore, CompiledPool, ValidationReport,
                               load_pool, validate)
from engine.config import GameConfig
from engine.sandbox import InProcessSandbox, Sandbox, SandboxError

ROOT = Path(__file__).resolve().parents[2]
PP_PATH = ROOT / "challenges" / "PP.json"

# A minimal challenge that passes every check: solution is "R" + reversed clue,
# so the clue itself is never accepted and junk always scores 0.
GEN = "def generate(seed):\n    r = random.Random(seed)\n    return str(r.randrange(1000, 9999))\n"
SOL = "def solve(clue):\n    return 'R' + clue[::-1]\n"
SCO = "def score(clue, solution):\n    return int(solution == 'R' + clue[::-1])\n"


def spec(name="T", generate=GEN, solve=SOL, score=SCO, description="notes", author="tester"):
    return ChallengeSpec(name=name, author=author, description=description,
                         generate=generate, solve=solve, score=score)


@pytest.fixture(scope="module")
def config():
    # few seeds + short caps keep the failing fixtures fast
    return GameConfig(validation_seeds=5, max_generate_ms=100, max_score_ms=50, max_solve_ms=300)


@pytest.fixture
def sb(config):
    s = Sandbox(config)
    try:
        yield s
    finally:
        s.close()


def check(sb, config, **kw):
    return validate(spec(**kw), config, sb)


def has_error(report, needle):
    return any(needle in e for e in report.errors), report.errors


# ------------------------------------------------------------------ spec/store
def test_spec_roundtrip(tmp_path):
    s = spec(name="RT")
    path = tmp_path / "RT.json"
    s.to_file(path)
    again = ChallengeSpec.from_file(path)
    assert again == s
    assert ChallengeSpec.from_dict(s.to_dict()) == s
    assert set(s.to_dict()) == {"name", "author", "description", "generate", "solve", "score"}


def test_spec_from_dict_tolerates_missing_fields():
    s = ChallengeSpec.from_dict({"name": "X"})
    assert s.author == "" and s.generate == "" and s.description == ""


def test_store_crud(tmp_path):
    store = ChallengeStore(tmp_path)
    assert store.list() == [] and store.names() == []
    store.put(spec(name="B"))
    store.put(spec(name="A").to_dict())
    assert store.names() == ["A", "B"]
    assert [s.name for s in store.list()] == ["A", "B"]
    assert store.get("A").score == SCO
    assert store.exists("A") and not store.exists("ZZ")
    with pytest.raises(KeyError):
        store.get("ZZ")
    assert store.delete("A") is True
    assert store.delete("A") is False
    assert store.names() == ["B"]


def test_store_rejects_dodgy_names(tmp_path):
    store = ChallengeStore(tmp_path)
    for bad in ("../etc/passwd", "with space", "", "toooooooooooooolong_name"):
        with pytest.raises(ValueError):
            store.put(spec(name=bad))


def test_store_skips_unreadable_files(tmp_path):
    store = ChallengeStore(tmp_path)
    store.put(spec(name="GOOD"))
    (tmp_path / "BROKEN.json").write_text("{not json")
    assert [s.name for s in store.list()] == ["GOOD"]


# ------------------------------------------------------------------ happy path
def test_pp_validates_ok(sb, config):
    report = validate(ChallengeSpec.from_file(PP_PATH), config, sb)
    assert report.ok, report.errors
    assert report.name == "PP"
    assert 0 < report.timings["generate_ms_max"] <= config.max_generate_ms
    assert report.timings["score_ms_max"] <= config.max_score_ms
    assert 1 <= len(report.samples) <= 3
    s = report.samples[0]
    assert s["clue"] in s["solution"]


def test_report_is_json_serialisable(sb, config):
    report = validate(spec(), config, sb)
    assert report.ok, report.errors
    d = report.to_dict()
    assert json.loads(json.dumps(d)) == d
    assert ValidationReport.from_dict(d).to_dict() == d
    assert "OK" in report.summary()


def test_validate_works_without_an_explicit_sandbox(config):
    assert validate(spec(), config).ok


def test_validate_accepts_a_plain_dict(sb, config):
    assert validate(spec().to_dict(), config, sb).ok


def test_inprocess_and_subprocess_validation_agree(sb, config):
    a = validate(ChallengeSpec.from_file(PP_PATH), config, sb)
    b = validate(ChallengeSpec.from_file(PP_PATH), config, InProcessSandbox(config))
    assert a.ok == b.ok is True
    assert [s["clue"] for s in a.samples] == [s["clue"] for s in b.samples]


# ------------------------------------------------------- §4.1 metadata + sizes
@pytest.mark.parametrize("name", ["", "has space", "way-too-long-a-name", "bad/name", "!"])
def test_bad_names_rejected(sb, config, name):
    assert has_error(check(sb, config, name=name), "name must match")[0]


def test_duplicate_name_rejected(sb, config):
    report = validate(spec(name="DUP"), config, sb, existing_names=["DUP"])
    assert has_error(report, "already exists")[0]


def test_empty_description_is_a_warning_only(sb, config):
    report = check(sb, config, description="")
    assert report.ok
    assert any("description is empty" in w for w in report.warnings)


def test_oversized_score_source_rejected(sb, config):
    padded = SCO + "#" + "x" * config.max_score_code_chars
    assert has_error(check(sb, config, score=padded), "score source is")[0]


def test_oversized_generate_and_solve_sources_rejected(sb, config):
    big = GEN + "#" + "x" * config.max_generate_code_chars
    assert has_error(check(sb, config, generate=big), "generate source is")[0]
    big = SOL + "#" + "x" * config.max_solve_code_chars
    assert has_error(check(sb, config, solve=big), "solve source is")[0]


def test_missing_source_rejected(sb, config):
    assert has_error(check(sb, config, solve="   "), "missing solve source")[0]


# ------------------------------------------------------- §4.2 compile and exec
def test_syntax_error_rejected(sb, config):
    assert has_error(check(sb, config, generate="def generate(:\n"), "SyntaxError")[0]


def test_missing_required_function_rejected(sb, config):
    report = check(sb, config, score="def scorer(c, s):\n    return 1\n")
    assert has_error(report, "must define a function named score()")[0]


def test_module_body_exception_rejected(sb, config):
    report = check(sb, config, generate="import os\n" + GEN)
    assert has_error(report, "ImportError")[0]


def test_banned_builtin_in_module_body_rejected(sb, config):
    report = check(sb, config, generate="X = open('/etc/passwd').read()\n" + GEN)
    assert has_error(report, "NameError")[0]


# ------------------------------------------------------- §4.3 generate checks
def test_generate_non_string_rejected(sb, config):
    report = check(sb, config, generate="def generate(seed):\n    return seed\n")
    assert has_error(report, "must return a non-empty str, got int")[0]


def test_generate_empty_clue_rejected(sb, config):
    report = check(sb, config, generate="def generate(seed):\n    return ''\n")
    assert has_error(report, "non-empty str")[0]


def test_generate_overlong_clue_rejected(sb, config):
    report = check(sb, config, generate=f"def generate(seed):\n    return 'x' * {config.max_clue_chars + 1}\n")
    assert has_error(report, "clue is")[0]


def test_generate_timeout_rejected(sb, config):
    report = check(sb, config, generate="def generate(seed):\n    while True:\n        pass\n")
    assert has_error(report, "generate(seed")[0]
    assert has_error(report, "SandboxTimeout")[0]


def test_generate_exception_rejected(sb, config):
    report = check(sb, config, generate="def generate(seed):\n    return str(1 // 0)\n")
    assert has_error(report, "ZeroDivisionError")[0]


def test_non_deterministic_generate_rejected(sb, config):
    report = check(sb, config, generate="def generate(seed):\n    return str(random.random())\n")
    assert has_error(report, "not deterministic")[0]


# ---------------------------------------------------------- §4.3 solve checks
def test_solve_exception_rejected(sb, config):
    report = check(sb, config, solve="def solve(clue):\n    raise ValueError('nope')\n")
    assert has_error(report, "ValueError")[0]


def test_solve_non_string_rejected(sb, config):
    report = check(sb, config, solve="def solve(clue):\n    return len(clue)\n")
    assert has_error(report, "must return str, got int")[0]


def test_solve_overlong_rejected(sb, config):
    report = check(sb, config, solve=f"def solve(clue):\n    return 'x' * {config.max_solution_chars + 1}\n")
    assert has_error(report, "solution is")[0]


def test_solve_timeout_rejected(sb, config):
    report = check(sb, config, solve="def solve(clue):\n    while True:\n        pass\n")
    assert has_error(report, "solve(seed")[0]


# ---------------------------------------------------------- §4.3 score checks
def test_score_rejects_the_reference_solution(sb, config):
    report = check(sb, config, score="def score(clue, solution):\n    return 0\n")
    assert has_error(report, "score(clue, solve(clue)) != 1")[0]


def test_score_must_reject_the_empty_string(sb, config):
    report = check(sb, config, score="def score(clue, solution):\n    return 1\n")
    assert has_error(report, "score(clue, '') must be 0")[0]


def test_score_must_return_zero_or_one(sb, config):
    src = "def score(clue, solution):\n    return 2 if solution == '0' else int(solution == 'R' + clue[::-1])\n"
    report = check(sb, config, score=src)
    assert has_error(report, "score must return 0 or 1")[0]


def test_score_timeout_rejected(sb, config):
    src = "def score(clue, solution):\n    while True:\n        pass\n"
    report = check(sb, config, score=src)
    assert has_error(report, "score timed out")[0]


def test_score_accepting_everything_rejected(sb, config):
    """Scores 1 for all junk but 0 for '' — caught by the 'accepts anything' rule."""
    report = check(sb, config, score="def score(clue, solution):\n    return int(solution != '')\n")
    assert has_error(report, "accepts anything")[0]


def test_score_raising_on_junk_is_only_a_warning(sb, config):
    src = ("def score(clue, solution):\n"
           "    if solution == 'x':\n"
           "        raise ValueError('junk')\n"
           "    return int(solution == 'R' + clue[::-1])\n")
    report = check(sb, config, score=src)
    assert report.ok, report.errors
    assert any("score raised on junk" in w for w in report.warnings)


def test_score_raising_on_the_reference_solution_is_fatal(sb, config):
    src = ("def score(clue, solution):\n"
           "    if solution.startswith('R'):\n"
           "        raise ValueError('boom')\n"
           "    return 0\n")
    report = check(sb, config, score=src)
    assert has_error(report, "score raised on solve output")[0]


# ------------------------------------------------------------- §4.4 warnings
def test_scorer_accepting_the_clue_is_a_warning(sb, config):
    src = ("def score(clue, solution):\n"
           "    return int(solution in ('R' + clue[::-1], clue))\n")
    report = check(sb, config, score=src)
    assert report.ok, report.errors
    assert any("accepts the clue itself" in w for w in report.warnings)


def test_slow_solve_is_a_warning(sb, config):
    """Cap is calibrated to this machine so the workload lands between 25% and 100%."""
    work = "def solve(clue):\n    t = 0\n    for i in range(400000):\n        t += i\n    return 'R' + clue[::-1]\n"
    ns = {}
    exec(work.replace("clue[::-1]", "''"), {}, ns)
    t0 = time.perf_counter()
    ns["solve"]("")
    local_ms = (time.perf_counter() - t0) * 1000
    cfg = config.replace(max_solve_ms=max(4, int(local_ms * 2.5)))
    report = validate(spec(solve=work), cfg, InProcessSandbox(cfg))
    assert report.ok, report.errors
    assert any("solve is slowish" in w for w in report.warnings)


def test_warnings_are_deduplicated_across_seeds(sb, config):
    report = check(sb, config, description="")
    assert len(report.warnings) == len(set(report.warnings))


# ------------------------------------------------------------------ the pool
def test_load_pool_from_specs_keeps_only_accepted(sb, config):
    good, bad = spec(name="GOOD"), spec(name="BAD", score="def score(c, s):\n    return 1\n")
    pool, reports = load_pool([good, bad], config, sb)
    assert pool.names == ["GOOD"]
    assert set(reports) == {"GOOD", "BAD"}
    assert reports["GOOD"].ok and not reports["BAD"].ok
    assert len(pool) == 1 and "GOOD" in pool and "BAD" not in pool
    clue = pool.generate("GOOD", 3)
    assert pool.score("GOOD", clue, pool.solve("GOOD", clue)) == 1


def test_load_pool_from_a_directory(tmp_path, sb, config):
    store = ChallengeStore(tmp_path)
    store.put(spec(name="A"))
    store.put(spec(name="B", generate="def generate(seed):\n    return ''\n"))
    store.put(ChallengeSpec.from_file(PP_PATH))
    pool, reports = load_pool(tmp_path, config, sb)
    assert pool.names == ["A", "PP"]
    assert not reports["B"].ok
    assert pool.specs["PP"].author


def test_real_challenge_directory_loads_pp(sb, config):
    pool, reports = load_pool(ROOT / "challenges", config, sb)
    assert "PP" in pool.names, {n: r.errors for n, r in reports.items()}


def test_load_pool_rejects_duplicate_names(sb, config):
    pool, reports = load_pool([spec(name="DUP"), spec(name="DUP")], config, sb)
    assert pool.names == ["DUP"] and len(pool) == 1


def test_random_challenge_is_seeded_and_in_pool(sb, config):
    pool, _ = load_pool([spec(name="A"), spec(name="B"), spec(name="C")], config, sb)
    picks = [pool.random_challenge(random.Random(7)) for _ in range(3)]
    assert len(set(picks)) == 1                     # same rng seed => same pick
    name, seed = picks[0]
    assert name in pool.names and 0 <= seed < 2 ** 32
    rng = random.Random(1)
    many = [pool.random_challenge(rng) for _ in range(60)]
    assert {n for n, _ in many} == {"A", "B", "C"}
    assert len({s for _, s in many}) > 50


def test_empty_pool_raises_on_random_challenge(config):
    with pytest.raises(SandboxError):
        CompiledPool([], config).random_challenge(random.Random(1))


def test_unbound_pool_raises_on_execution(config):
    pool = CompiledPool([spec(name="A")], config)
    with pytest.raises(SandboxError):
        pool.generate("A", 1)
    ip = InProcessSandbox(config)
    pool.bind(ip)
    pool.load_into(ip)
    assert pool.generate("A", 1)
