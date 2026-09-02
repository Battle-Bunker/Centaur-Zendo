"""Tests for client/player.py against a fake SPEC §6 server (fake_server.py)."""
from __future__ import annotations

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

CLIENT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CLIENT_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import player                                    # noqa: E402
from fake_server import FakeServer               # noqa: E402


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
PERFECT = '''
def solve(name, clue, memory):
    memory["seen"] = memory.get("seen", 0) + 1
    if name == "ADD":
        a, b = clue.split("+")
        return str(int(a) + int(b))
    return clue
'''

CRASHER = '''
def solve(name, clue, memory):
    raise ValueError("boom")
'''

SLOPPY = '''
def solve(name, clue, memory):
    if name == "ADD":
        return 7 + 0            # not a string on purpose
    return "z" * 5000           # far too long on purpose
'''

HOOKED = '''
def on_round_start(memory):
    memory["starts"] = memory.get("starts", 0) + 1

def solve(name, clue, memory):
    return clue

def on_round_end(items, memory):
    memory["ended_with"] = len(items)
'''


def write_strategy(tmp_path: Path, src: str, name="strategy.py") -> Path:
    p = tmp_path / name
    p.write_text(src)
    return p


def run_client(argv, tmp_path, strategy_src=PERFECT):
    """Run player.main(argv) in-process, in a sandbox directory."""
    sp = write_strategy(tmp_path, strategy_src)
    full = ["--strategy", str(sp), "--log-dir", str(tmp_path / "logs"),
            "--memory", str(tmp_path / "memory.json")] + argv
    return player.main(full)


def with_server(fn, **server_kw):
    """Start a FakeServer, run `fn(server)` (a coroutine fn), stop the server."""
    async def go():
        srv = FakeServer(**server_kw)
        url = await srv.start()
        try:
            return await fn(srv, url)
        finally:
            await srv.stop()
    return asyncio.run(go())


def play(argv, tmp_path, strategy_src=PERFECT, **server_kw):
    """Run one client command against a fresh fake server; return (rc, server)."""
    holder = {}

    async def fn(srv, url):
        loop = asyncio.get_running_loop()
        rc = await loop.run_in_executor(
            None, run_client,
            ["--url", url, "--team", "T", "--token", "S"] + argv,
            tmp_path, strategy_src)
        holder["rc"] = rc
        return srv

    srv = with_server(fn, **server_kw)
    return holder["rc"], srv


def read_logs(tmp_path, label="1"):
    d = tmp_path / "logs"
    jsonl = [json.loads(l) for l in
             (d / f"round_{label}.jsonl").read_text().splitlines() if l.strip()]
    return jsonl, (d / f"round_{label}.txt").read_text(), \
        (d / "summary.txt").read_text()


# --------------------------------------------------------------------------- #
# tests
# --------------------------------------------------------------------------- #
def test_status_command(tmp_path, capsys):
    rc, srv = play(["status"], tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert "phase" in out and "training" in out
    assert "ADD" in out and "ECHO" in out
    assert [m["type"] for m in srv.inbox] == ["join", "status"]


def test_round_perfect_score_and_protocol(tmp_path, capsys):
    rc, srv = play(["round"], tmp_path, items_per_round=6)
    out = capsys.readouterr().out
    assert rc == 0
    assert srv.rounds_used == 1
    # every challenge got an `answer` with the right round_id/index
    answers = [a for a in srv.answers if a["type"] == "answer"]
    assert len(answers) == 6
    assert [a["index"] for a in answers] == list(range(6))
    assert len({a["round_id"] for a in answers}) == 1
    assert "correct=6" in out
    assert "latency" in out


def test_logs_written(tmp_path):
    play(["round"], tmp_path, items_per_round=5)
    jsonl, txt, summary = read_logs(tmp_path)
    kinds = [r["msg"]["type"] for r in jsonl]
    assert kinds[0] == "join" and kinds[1] == "welcome"
    assert kinds.count("challenge") == 5
    assert kinds.count("answer") == 5
    assert kinds.count("result") == 5
    assert kinds[-1] == "round_over"
    assert all(isinstance(r["ts"], float) and r["dir"] in ("in", "out")
               for r in jsonl)
    # human readable summary
    assert "presented=5" in txt and "correct=5" in txt
    assert "idx" in txt and "clue" in txt and "score" in txt
    assert "per-name tally" in txt
    assert "100.0%" in txt
    # rolling summary
    assert "running per-name hit-rate" in summary
    assert "ECHO" in summary or "ADD" in summary


def test_memory_persists_between_rounds(tmp_path):
    async def fn(srv, url):
        loop = asyncio.get_running_loop()
        for _ in range(2):
            await loop.run_in_executor(
                None, run_client,
                ["--url", url, "--team", "T", "--token", "S", "round"],
                tmp_path, PERFECT)
        return srv

    srv = with_server(fn, items_per_round=4, cooldown_seconds=0.0)
    mem = json.loads((tmp_path / "memory.json").read_text())
    assert mem["seen"] == 8                      # 4 in round 1 + 4 in round 2
    assert srv.rounds_used == 2
    assert (tmp_path / "logs" / "round_1.txt").exists()
    assert (tmp_path / "logs" / "round_2.txt").exists()
    summary = (tmp_path / "logs" / "summary.txt").read_text()
    assert "\n     1 " in summary and "\n     2 " in summary


def test_hooks_are_called(tmp_path):
    play(["round"], tmp_path, HOOKED, items_per_round=3)
    mem = json.loads((tmp_path / "memory.json").read_text())
    assert mem["starts"] == 1
    assert mem["ended_with"] == 3


def test_strategy_exception_becomes_skip(tmp_path, capsys):
    rc, srv = play(["round"], tmp_path, CRASHER, items_per_round=4)
    out = capsys.readouterr().out
    assert rc == 0
    assert [a["type"] for a in srv.answers] == ["skip"] * 4
    assert all("solution" not in a for a in srv.answers)
    assert "skipped=4" in out
    txt = (tmp_path / "logs" / "round_1.txt").read_text()
    assert "boom" in txt                          # the crash is reported in the log


def test_solution_coerced_and_truncated(tmp_path):
    rc, srv = play(["round"], tmp_path, SLOPPY, items_per_round=6,
                   max_solution_chars=16)
    answers = [a for a in srv.answers if a["type"] == "answer"]
    assert answers, "expected answers"
    for a in answers:
        assert isinstance(a["solution"], str)
        # the client honours the max_solution_chars the server advertised
        assert len(a["solution"]) <= 16
    assert any(a["solution"] == "7" for a in answers)     # int coerced to str
    assert any(len(a["solution"]) == 16 for a in answers)  # long one truncated


def test_default_strategy_is_random_and_records(tmp_path):
    """The shipped strategy.py must survive a whole round and fill memory."""
    src = (CLIENT_DIR / "strategy.py").read_text()
    rc, srv = play(["round"], tmp_path, src, items_per_round=8)
    assert rc == 0
    answers = [a for a in srv.answers if a["type"] == "answer"]
    assert len(answers) == 8
    mem = json.loads((tmp_path / "memory.json").read_text())
    assert mem["rounds_played"] == 1
    assert sum(len(v) for v in mem["examples"].values()) == 8
    for bucket in mem["examples"].values():
        assert {"clue", "answer", "score"} <= set(bucket[0])


def test_demo(tmp_path, capsys):
    rc, srv = play(["demo", "ADD"], tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert "3+4" in out and "7" in out and "score" in out
    assert srv.demo_available is False
    demos = (tmp_path / "logs" / "demos.jsonl").read_text()
    assert "ADD" in demos


def test_demo_unknown_challenge_is_reported(tmp_path, capsys):
    rc, srv = play(["demo", "NOPE"], tmp_path)
    assert rc == 0
    assert "unknown_challenge" in capsys.readouterr().out


def test_final(tmp_path, capsys):
    rc, srv = play(["final"], tmp_path, items_per_round=5)
    out = capsys.readouterr().out
    assert rc == 0
    assert srv.final_done and srv.final_score == 5
    assert srv.rounds_used == 0                    # a final is not a training round
    assert "final" in out
    assert (tmp_path / "logs" / "round_final.txt").exists()
    assert (tmp_path / "logs" / "round_final.jsonl").exists()


def test_cooldown_refusal_is_reported(tmp_path, capsys):
    rc, srv = play(["round"], tmp_path, refuse_first_round="cooldown")
    out = capsys.readouterr().out
    assert rc == 2
    assert "cooldown" in out and "retry_at" in out
    assert srv.rounds_used == 0


def test_wait_round_waits_then_plays(tmp_path, capsys):
    t0 = time.time()
    rc, srv = play(["wait-round"], tmp_path, items_per_round=3,
                   next_round_delay=0.6)
    elapsed = time.time() - t0
    out = capsys.readouterr().out
    assert rc == 0
    assert "waiting" in out
    assert elapsed >= 0.5
    assert srv.rounds_used == 1


def test_wait_round_retries_after_cooldown_refusal(tmp_path, capsys):
    rc, srv = play(["wait-round"], tmp_path, items_per_round=3,
                   refuse_first_round="cooldown")
    out = capsys.readouterr().out
    assert rc == 0
    assert "cooldown" in out
    assert srv.rounds_used == 1                   # it retried and played


def test_watch_plays_until_round_cap(tmp_path, capsys):
    rc, srv = play(["watch"], tmp_path, items_per_round=2,
                   max_training_rounds=3, cooldown_seconds=0.0)
    out = capsys.readouterr().out
    assert rc == 0
    assert srv.rounds_used == 3
    assert "training rounds used" in out
    for n in (1, 2, 3):
        assert (tmp_path / "logs" / f"round_{n}.txt").exists()
    summary = (tmp_path / "logs" / "summary.txt").read_text()
    assert summary.count("training") >= 3


def test_watch_honours_max_rounds_flag(tmp_path):
    rc, srv = play(["--max-rounds", "2", "watch"], tmp_path, items_per_round=2,
                   max_training_rounds=12)
    assert rc == 0
    assert srv.rounds_used == 2


def test_latency_is_small(tmp_path, capsys):
    play(["round"], tmp_path, items_per_round=20)
    out = capsys.readouterr().out
    line = [l for l in out.splitlines() if "client answer latency" in l][0]
    mean_ms = float(line.split("mean ")[1].split(" ms")[0])
    assert mean_ms < 5.0, line                     # hot loop must stay sub-5ms


def test_cli_via_subprocess(tmp_path):
    """The documented command line works end to end in a real process."""
    async def fn(srv, url):
        loop = asyncio.get_running_loop()
        sp = write_strategy(tmp_path, PERFECT)
        cmd = [sys.executable, str(CLIENT_DIR / "player.py"),
               "--url", url, "--team", "T", "--token", "S",
               "--strategy", str(sp), "--log-dir", str(tmp_path / "logs"),
               "--memory", str(tmp_path / "memory.json"), "round"]
        proc = await loop.run_in_executor(
            None, lambda: subprocess.run(cmd, capture_output=True, text=True,
                                         timeout=60))
        return proc

    proc = with_server(fn, items_per_round=4)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "correct=4" in proc.stdout


def test_env_var_defaults(monkeypatch, tmp_path):
    monkeypatch.setenv("ZENDO_URL", "ws://example/ws")
    monkeypatch.setenv("ZENDO_TEAM", "envteam")
    monkeypatch.setenv("ZENDO_TOKEN", "envtoken")
    args = player.build_parser().parse_args(["status"])
    assert (args.url, args.team, args.token) == ("ws://example/ws", "envteam",
                                                 "envtoken")


def test_missing_strategy_is_a_clean_error(tmp_path, capsys):
    rc = player.main(["--strategy", str(tmp_path / "nope.py"),
                      "--url", "ws://127.0.0.1:1/ws", "round"])
    assert rc == 2
    assert "cannot load strategy" in capsys.readouterr().out


def test_unknown_refusal_code_does_not_hang(tmp_path, capsys):
    """A second `final` is refused with code `final_done` (not in the §5 list);
    the client must report it and exit instead of waiting forever."""
    async def fn(srv, url):
        loop = asyncio.get_running_loop()
        rcs = []
        for _ in range(2):
            rcs.append(await asyncio.wait_for(loop.run_in_executor(
                None, run_client,
                ["--url", url, "--team", "T", "--token", "S", "final"],
                tmp_path, PERFECT), timeout=20))
        return rcs

    rcs = with_server(fn, items_per_round=2)
    out = capsys.readouterr().out
    assert rcs == [0, 2]
    assert "final already run" in out


def test_wait_round_uses_retry_at_from_a_phase_refusal(tmp_path, capsys):
    """Started before the game opens: the client sleeps until `retry_at`."""
    async def fn(srv, url):
        loop = asyncio.get_running_loop()
        rc = await loop.run_in_executor(
            None, run_client,
            ["--url", url, "--team", "T", "--token", "S", "wait-round"],
            tmp_path, PERFECT)
        return rc, srv

    rc, srv = with_server(fn, items_per_round=2, phase="lobby",
                          lobby_opens_in=0.4)
    out = capsys.readouterr().out
    assert "phase" in out and "waiting" in out
    assert rc == 0 and srv.rounds_used == 1


def test_connection_dropped_mid_round_still_writes_a_log(tmp_path, capsys):
    rc, srv = play(["round"], tmp_path, items_per_round=6, close_after=3)
    out = capsys.readouterr().out
    assert rc == 3                                   # reported as a connection drop
    assert "connection closed mid-round" in out
    txt = (tmp_path / "logs" / "round_partial.txt").read_text()
    assert "presented=3" in txt and "correct=3" in txt
    assert (tmp_path / "logs" / "round_partial.jsonl").exists()
    # a cut-off round must not pollute the running summary
    assert not (tmp_path / "logs" / "summary.txt").exists()
