#!/usr/bin/env python3
"""End-to-end smoke test: real server, real sandbox, two scripted players.

    python sim/smoke.py            # < 90 s, exits non-zero if anything is off

It writes a throwaway config (2 s cooldown, 3 training rounds, 30 s of training,
a 20 s final window), starts `python -m engine.server` in a subprocess on a free
port, then plays the whole game with two `websockets` clients:

  * alpha  answers every challenge with "" as fast as it can (a latency probe)
  * beta   tries to solve PP by naive search and skips everything else

Along the way it checks the SPEC §5/§6 invariants (frame order, round_id on
every round frame, result(i) before challenge(i+1), cooldown / round-cap
refusals, demo, the shared final sequence) and prints a latency report.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import socket
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websockets

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

COOLDOWN = 2.0
ROUNDS = 3
TRAINING_SECONDS = 30.0
FINAL_WINDOW = 20.0
ADMIN_TOKEN = "smoke-admin"

failures: list[str] = []


def check(ok: bool, what: str) -> bool:
    if not ok:
        failures.append(what)
        print(f"  !! FAILED: {what}")
    return ok


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def write_config(path: Path, event_log: Path) -> dict:
    cfg = {
        "round_seconds": 1.0,
        "final_seconds": 3.0,
        "cooldown_seconds": COOLDOWN,
        "max_training_rounds": ROUNDS,
        "training_seconds": TRAINING_SECONDS,
        "final_window_seconds": FINAL_WINDOW,
        "demo_per_window": 1,
        "open_registration": True,
        "challenge_dir": "challenges",
        "event_log": str(event_log),
        "sandbox_workers": 4,
        "final_shared_sequence": True,
        "final_seed": 20250601,
        "admin_token": ADMIN_TOKEN,
        "host": "127.0.0.1",
    }
    path.write_text(json.dumps(cfg, indent=2))
    return cfg


def http_json(url: str, timeout: float = 5.0):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode())


def wait_for_server(port: int, proc: subprocess.Popen, timeout: float = 60.0) -> dict:
    url = f"http://127.0.0.1:{port}/api/state"
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"server exited early with code {proc.returncode}")
        try:
            return http_json(url, timeout=2.0)
        except Exception:
            time.sleep(0.25)
    raise RuntimeError(f"server did not answer {url} within {timeout}s")


# --------------------------------------------------------------------------
# player strategies
# --------------------------------------------------------------------------
def strategy_blank(name: str, clue: str) -> str | None:
    """Answer everything instantly with the empty string (always scores 0)."""
    return ""


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True


def strategy_pp(name: str, clue: str, budget: float = 0.20) -> str | None:
    """Naive palindromic-prime search for PP; skip everything else."""
    if name != "PP" or not clue.isdigit():
        return None
    end = time.time() + budget
    n = int(clue) if clue[0] != "0" else 1
    while time.time() < end:
        s = str(n)
        if s == s[::-1] and clue in s and _is_prime(n):
            return s
        n += 1
    return None


# --------------------------------------------------------------------------
# player
# --------------------------------------------------------------------------
class Player:
    def __init__(self, url: str, team: str, token: str, strategy):
        self.url = url
        self.team = team
        self.token = token
        self.strategy = strategy
        self.ws = None
        self.rounds: list[dict] = []
        self.demos: list[dict] = []
        self.gap_ms: list[float] = []       # answer sent -> next challenge received
        self.result_ms: list[float] = []    # answer sent -> its result received
        self.stale = 0
        self.errors: list[dict] = []
        self.welcome = None
        self.status = None

    async def send(self, msg: dict) -> None:
        await self.ws.send(json.dumps(msg))

    async def recv(self, timeout: float = 20.0) -> dict:
        raw = await asyncio.wait_for(self.ws.recv(), timeout)
        return json.loads(raw)

    async def recv_skipping_stale(self, timeout: float = 20.0) -> dict:
        while True:
            msg = await self.recv(timeout)
            if msg.get("type") == "error" and msg.get("code") == "stale":
                self.stale += 1     # racing the deadline with the last answer: normal
                continue
            return msg

    async def connect(self) -> None:
        self.ws = await websockets.connect(self.url, max_size=8 * 1024 * 1024)
        await self.send({"type": "join", "team": self.team, "token": self.token})
        self.welcome = await self.recv_skipping_stale()
        check(self.welcome.get("type") == "welcome", f"{self.team}: first frame is welcome")
        for key in ("team", "phase", "challenges", "config", "rounds_used",
                    "next_round_available_at", "demo_available", "server_time"):
            check(key in self.welcome, f"{self.team}: welcome has {key}")
        for key in ("round_seconds", "final_seconds", "cooldown_seconds", "max_training_rounds",
                    "max_solution_chars", "max_clue_chars", "training_ends_at", "final_ends_at"):
            check(key in self.welcome["config"], f"{self.team}: welcome.config has {key}")

    async def close(self) -> None:
        if self.ws is not None:
            await self.ws.close()

    async def ping(self) -> None:
        await self.send({"type": "ping"})
        msg = await self.recv_skipping_stale()
        check(msg.get("type") == "pong" and "server_time" in msg, f"{self.team}: pong")

    async def demo(self, name: str) -> dict | None:
        await self.send({"type": "demo", "name": name})
        msg = await self.recv_skipping_stale()
        if msg.get("type") == "demo_result":
            check(msg["score"] == 1, f"{self.team}: the reference solve() scores 1 on demo {name}")
            check(bool(msg.get("clue")) and msg.get("solution") is not None,
                  f"{self.team}: demo carries clue+solution")
            self.demos.append(msg)
            return msg
        self.errors.append(msg)
        return None

    async def play(self, kind: str = "start_round", retries: int = 6) -> dict | None:
        """Run one round; waits out a cooldown refusal.  Returns round_over."""
        for _ in range(retries):
            await self.send({"type": kind})
            msg = await self.recv_skipping_stale()
            if msg.get("type") == "round_started":
                return await self._round_loop(msg)
            if msg.get("type") == "error" and msg.get("code") == "cooldown":
                retry_at = msg.get("retry_at") or 0
                check(retry_at > 0, f"{self.team}: cooldown error carries retry_at")
                delay = max(0.05, retry_at - time.time()) + 0.05
                await asyncio.sleep(min(delay, COOLDOWN + 1))
                continue
            self.errors.append(msg)
            return None
        return None

    async def _round_loop(self, started: dict) -> dict:
        rid = started["round_id"]
        check(started.get("kind") in ("training", "final"), f"{self.team}: round kind")
        check(started.get("duration_ms", 0) > 0, f"{self.team}: duration_ms")
        check(abs((started["deadline"] - started["started_at"])
                  - started["duration_ms"] / 1000) < 1e-6, f"{self.team}: deadline = start+duration")
        seq: list[tuple[str, int]] = []
        answered_at: dict[int, float] = {}
        sent_at = None
        while True:
            msg = await self.recv(timeout=30.0)
            kind = msg.get("type")
            if kind == "error":
                if msg.get("code") == "stale":
                    self.stale += 1
                    continue
                self.errors.append(msg)
                continue
            check(msg.get("round_id") == rid, f"{self.team}: {kind} carries the round_id")
            if kind == "challenge":
                if sent_at is not None:
                    self.gap_ms.append((time.time() - sent_at) * 1000)
                seq.append(("challenge", msg["index"]))
                solution = self.strategy(msg["name"], msg["clue"])
                sent_at = time.time()
                answered_at[msg["index"]] = sent_at
                if solution is None:
                    await self.send({"type": "skip", "round_id": rid, "index": msg["index"]})
                else:
                    await self.send({"type": "answer", "round_id": rid,
                                     "index": msg["index"], "solution": solution})
            elif kind == "result":
                seq.append(("result", msg["index"]))
                t0 = answered_at.get(msg["index"])
                if t0 is not None:
                    self.result_ms.append((time.time() - t0) * 1000)
                check(msg["score"] in (0, 1), f"{self.team}: result score is 0/1")
            elif kind == "round_over":
                self._check_round(msg, seq, started)
                self.rounds.append(msg)
                return msg

    def _check_round(self, over: dict, seq, started) -> None:
        t = self.team
        # result(i) is always sent before challenge(i+1)
        for a, b in zip(seq, seq[1:]):
            if a[0] == "challenge":
                check(b == ("result", a[1]), f"{t}: result {a[1]} follows challenge {a[1]}")
            else:
                check(b == ("challenge", a[1] + 1), f"{t}: challenge {a[1]+1} follows result {a[1]}")
        idx = [i for k, i in seq if k == "challenge"]
        check(idx == list(range(len(idx))), f"{t}: challenge indices are 0..n-1")
        results = [i for k, i in seq if k == "result"]
        check(over["presented"] == len(results), f"{t}: presented == number of results")
        check(over["presented"] == len(over["items"]), f"{t}: presented == len(items)")
        check(over["correct"] == sum(i["score"] for i in over["items"]), f"{t}: correct == sum(scores)")
        check(over["answered"] <= over["presented"], f"{t}: answered <= presented")
        check(over["kind"] == started["kind"], f"{t}: round_over kind matches")
        for key in ("rounds_used", "next_round_available_at", "demo_available"):
            check(key in over, f"{t}: round_over has {key}")
        for item in over["items"]:
            check(set(item) == {"index", "name", "clue", "solution", "score"},
                  f"{t}: item fields")

    async def get_status(self) -> dict:
        await self.send({"type": "status"})
        msg = await self.recv_skipping_stale()
        check(msg.get("type") == "status", f"{self.team}: status frame")
        self.status = msg
        return msg

    async def expect_error(self, message: dict, code) -> None:
        codes = (code,) if isinstance(code, str) else tuple(code)
        await self.send(message)
        msg = await self.recv_skipping_stale()
        check(msg.get("type") == "error" and msg.get("code") in codes,
              f"{self.team}: {message['type']} -> error {'/'.join(codes)} "
              f"(got {msg.get('code', msg.get('type'))})")


# --------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------
async def play_game(url: str, port: int, pool_names: list[str]) -> tuple[Player, Player]:
    alpha = Player(url, "alpha", "tok-a", strategy_blank)
    beta = Player(url, "beta", "tok-b", strategy_pp)
    await asyncio.gather(alpha.connect(), beta.connect())
    await asyncio.gather(alpha.ping(), beta.ping())

    demo_name = "PP" if "PP" in pool_names else pool_names[0]

    async def training(p: Player):
        await p.demo(demo_name)                       # one demo per window
        await p.expect_error({"type": "demo", "name": demo_name}, "no_demo")
        for _ in range(ROUNDS):
            await p.play()
        await p.expect_error({"type": "start_round"}, "round_cap")

    await asyncio.gather(training(alpha), training(beta))
    print(f"  training done for both teams after {ROUNDS} rounds each")

    # wait for training -> final (driven by the clock, not by an admin call)
    deadline = time.time() + TRAINING_SECONDS + 15
    while time.time() < deadline:
        state = http_json(f"http://127.0.0.1:{port}/api/state")
        if state["phase"] == "final":
            break
        await asyncio.sleep(0.5)
    check(state["phase"] == "final", "training rolled over into the final on its own")

    await asyncio.gather(alpha.play("start_final"), beta.play("start_final"))
    # by now both teams are done, so the game may already have moved to
    # "finished"; either refusal is correct.
    await asyncio.gather(alpha.expect_error({"type": "start_final"}, ("final_done", "phase")),
                         beta.expect_error({"type": "start_final"}, ("final_done", "phase")))
    await asyncio.gather(alpha.get_status(), beta.get_status())
    await asyncio.gather(alpha.close(), beta.close())
    return alpha, beta


def server_side_latency(lines: list[dict]) -> dict[str, dict[str, list[float]]]:
    """Server-side turnaround, straight out of the event log.

    For every inbound answer/skip: how long until the `result` frame went out,
    and how long until the *next* `challenge` frame went out.  This excludes the
    loopback round trip and the client's own work, so it is the number the SPEC
    latency budget is about.
    """
    out: dict[str, dict[str, list[float]]] = {}
    pending: dict[str, float] = {}
    for line in lines:
        team, direction, msg = line.get("team"), line.get("dir"), line.get("msg") or {}
        if not team or not isinstance(msg, dict):
            continue
        bucket = out.setdefault(team, {"result": [], "challenge": []})
        kind = msg.get("type")
        if direction == "in" and kind in ("answer", "skip"):
            pending[team] = line["ts"]
        elif direction == "out" and team in pending:
            if kind == "result":
                bucket["result"].append((line["ts"] - pending[team]) * 1000)
            elif kind == "challenge":
                bucket["challenge"].append((line["ts"] - pending[team]) * 1000)
                pending.pop(team, None)
            else:
                # round_over, a stale error, anything else: the turn is over, so
                # a late answer is never paired with the next round's challenge.
                pending.pop(team, None)
    return out


def stats(values: list[float]) -> str:
    if not values:
        return "n/a"
    ordered = sorted(values)
    p95 = ordered[min(len(ordered) - 1, int(0.95 * len(ordered)))]
    return (f"n={len(values)} median={statistics.median(ordered):.2f}ms "
            f"p95={p95:.2f}ms max={ordered[-1]:.2f}ms")


def report(alpha: Player, beta: Player, port: int, elapsed: float,
           lines: list[dict] | None = None) -> None:
    print("\n=== rounds =======================================================")
    for p in (alpha, beta):
        for r in p.rounds:
            print(f"  {p.team:<6} {r['kind']:<8} presented={r['presented']:<4} "
                  f"answered={r['answered']:<4} correct={r['correct']:<4} "
                  f"rounds_used={r['rounds_used']}")
    print("\n=== per-message latency (client-side, includes loopback RTT) =====")
    for p in (alpha, beta):
        print(f"  {p.team:<6} answer -> next challenge : {stats(p.gap_ms)}")
        print(f"  {p.team:<6} answer -> its result     : {stats(p.result_ms)}")
    print(f"\n  (late-answer 'stale' frames: alpha={alpha.stale} beta={beta.stale})")

    server = server_side_latency(lines or [])
    if server:
        print("\n=== server-side turnaround (from the event log) ==================")
        for team, b in server.items():
            print(f"  {team:<6} answer in -> result out    : {stats(b['result'])}")
            print(f"  {team:<6} answer in -> challenge out : {stats(b['challenge'])}")

    print("\n=== demos ========================================================")
    for p in (alpha, beta):
        for d in p.demos:
            print(f"  {p.team:<6} {d['name']:<10} clue={d['clue'][:28]!r} "
                  f"solution={d['solution'][:28]!r} score={d['score']}")

    state = http_json(f"http://127.0.0.1:{port}/api/state")
    print("\n=== leaderboard ==================================================")
    for row in state["leaderboard"]:
        print(f"  {row['rank']}. {row['team']:<8} final={row['final_score']} "
              f"answered={row['answered']} rounds={row['rounds_used']}")
    print(f"\n  phase={state['phase']}  challenges={len(state['challenges'])}  "
          f"wall clock={elapsed:.1f}s")


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    started = time.time()
    tmp = Path(tempfile.mkdtemp(prefix="zendo-smoke-"))
    cfg_path = tmp / "smoke.json"
    event_log = tmp / "events.jsonl"
    write_config(cfg_path, event_log)
    port = free_port()
    url = f"ws://127.0.0.1:{port}/ws"

    print(f"smoke: config={cfg_path} port={port}")
    proc = subprocess.Popen(
        [sys.executable, "-m", "engine.server", "--config", str(cfg_path),
         "--port", str(port), "--start-now", "--log-level", "WARNING"],
        cwd=str(ROOT),
    )
    try:
        state = wait_for_server(port, proc)
        names = state["challenges"]
        print(f"  server up: phase={state['phase']} challenges={len(names)}")
        check(bool(names), "the pool loaded at least one challenge")
        check(state["phase"] == "training", "--start-now put the game in training")

        alpha, beta = asyncio.run(play_game(url, port, names))

        # the final is one shared (name, seed) sequence for everybody
        fa = [r for r in alpha.rounds if r["kind"] == "final"]
        fb = [r for r in beta.rounds if r["kind"] == "final"]
        check(len(fa) == 1 and len(fb) == 1, "each team ran exactly one final")
        if fa and fb:
            n = min(len(fa[0]["items"]), len(fb[0]["items"]))
            check(n > 0, "the final presented at least one challenge")
            check([(i["name"], i["clue"]) for i in fa[0]["items"]][:n]
                  == [(i["name"], i["clue"]) for i in fb[0]["items"]][:n],
                  "both teams faced the same final sequence")
        check(all(len([r for r in p.rounds if r["kind"] == "training"]) == ROUNDS
                  for p in (alpha, beta)), f"each team ran {ROUNDS} training rounds")
        check(alpha.rounds[0]["rounds_used"] == 1, "rounds_used starts at 1")
        check(beta.demos and beta.demos[0]["score"] == 1, "demo returned a scoring solution")

        lb = http_json(f"http://127.0.0.1:{port}/api/state")["leaderboard"]
        check(len(lb) == 2, "both teams are on the leaderboard")
        check([r["rank"] for r in lb] == [1, 2], "leaderboard is ranked")
        check(lb[0]["final_score"] >= lb[1]["final_score"], "leaderboard is sorted by score")

        lines = [json.loads(l) for l in event_log.read_text().splitlines()] if event_log.exists() else []
        check(bool(lines), "the event log has JSONL lines")
        check(all({"ts", "team", "dir", "msg"} <= set(l) for l in lines),
              "event log lines have ts/team/dir/msg")
        check(any(l["dir"] == "round" for l in lines), "the event log has round summaries")

        report(alpha, beta, port, time.time() - started, lines)
        print(f"\n  event log: {len(lines)} lines")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:  # pragma: no cover
            proc.kill()
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n==================================================================")
    if failures:
        print(f"SMOKE FAILED: {len(failures)} invariant(s) broken")
        for f in dict.fromkeys(failures):
            print("  -", f)
        return 1
    print(f"SMOKE OK in {time.time() - started:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
