#!/usr/bin/env python3
"""Centaur Zendo — reference player client (SPEC.md §6/§7).

Usage
    python player.py --url ws://localhost:8080/ws --team T --token S <command>

Commands
    round        run one training round
    final        run the 3-second final test
    demo NAME    spend the demo ability on challenge NAME
    status       print the server status
    wait-round   sleep until next_round_available_at, then run one round
    watch        loop wait-round until the rounds are exhausted

Environment defaults: ZENDO_URL, ZENDO_TEAM, ZENDO_TOKEN.

The answer loop is deliberately boring and tight: receive -> strategy.solve ->
send.  Nothing is printed or written to disk while a round is running; every
message is buffered in memory and flushed to logs/ after `round_over`.
"""
from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import websockets

DEFAULT_MAX_SOLUTION_CHARS = 4096


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def iso(ts: float | None) -> str:
    if not ts:
        return "-"
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def cell(s: object, width: int) -> str:
    t = str(s).replace("\n", "\\n").replace("\t", " ")
    if len(t) > width:
        t = t[: width - 1] + "\u2026"
    return t.ljust(width)


def load_strategy(path: Path):
    """Import the player's strategy module from an arbitrary file path."""
    spec = importlib.util.spec_from_file_location("zendo_strategy", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load strategy from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["zendo_strategy"] = mod
    spec.loader.exec_module(mod)
    if not hasattr(mod, "solve"):
        raise RuntimeError(f"{path} does not define solve(name, clue, memory)")
    return mod


# --------------------------------------------------------------------------- #
# the client
# --------------------------------------------------------------------------- #

class _Skip(Exception):
    """Raised internally when strategy.solve returns None (= skip this challenge)."""

class Player:
    def __init__(self, args, strategy):
        self.args = args
        self.strategy = strategy
        self.log_dir = Path(args.log_dir)
        self.memory_path = Path(args.memory)
        self.history_path = self.log_dir / "_history.json"

        self.records: list[dict] = []          # buffered protocol log for one round
        self.notes: list[str] = []             # buffered warnings (strategy crashes...)
        self.max_solution_chars = DEFAULT_MAX_SOLUTION_CHARS

        self.phase = None
        self.rounds_used = 0
        self.max_training_rounds = None
        self.next_round_available_at = None
        self.demo_available = False
        self.challenges: list[str] = []
        self.clock_offset = 0.0                # server_time - local time
        self.last_refusal = None               # last error that blocked a round

    # ---------------- clock ----------------
    def server_now(self) -> float:
        return time.time() + self.clock_offset

    def to_local(self, server_ts: float) -> float:
        return server_ts - self.clock_offset

    # ---------------- memory ----------------
    def load_memory(self) -> dict:
        try:
            with open(self.memory_path, "r", encoding="utf-8") as fh:
                mem = json.load(fh)
            return mem if isinstance(mem, dict) else {}
        except FileNotFoundError:
            return {}
        except Exception as exc:                                  # corrupt file
            print(f"[warn] memory.json unreadable ({exc}); starting empty")
            return {}

    def save_memory(self, memory: dict) -> None:
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.memory_path.with_suffix(".json.tmp")
        try:
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(memory, fh, indent=1, default=str)
            tmp.replace(self.memory_path)
        except Exception as exc:
            print(f"[warn] could not save memory.json: {exc}")

    # ---------------- protocol I/O ----------------
    async def send(self, ws, msg: dict) -> None:
        self.records.append({"ts": time.time(), "dir": "out", "msg": msg})
        await ws.send(json.dumps(msg))

    async def recv(self, ws) -> dict:
        raw = await ws.recv()
        msg = json.loads(raw)
        self.records.append({"ts": time.time(), "dir": "in", "msg": msg})
        return msg

    def absorb(self, msg: dict) -> None:
        """Track the mutable bits of team state that several messages carry."""
        for key in ("phase", "rounds_used", "next_round_available_at",
                    "demo_available"):
            if key in msg:
                setattr(self, key, msg[key])
        if msg.get("type") == "welcome":
            self.challenges = list(msg.get("challenges") or [])
            cfg = msg.get("config") or {}
            self.max_solution_chars = int(
                cfg.get("max_solution_chars") or DEFAULT_MAX_SOLUTION_CHARS
            )
            self.max_training_rounds = cfg.get("max_training_rounds")
            st = msg.get("server_time")
            if isinstance(st, (int, float)):
                self.clock_offset = st - time.time()

    async def join(self, ws) -> dict:
        await self.send(ws, {"type": "join", "team": self.args.team,
                             "token": self.args.token})
        while True:
            msg = await self.recv(ws)
            self.absorb(msg)
            if msg.get("type") == "welcome":
                return msg
            if msg.get("type") == "error":
                raise RuntimeError(f"join refused: {msg.get('code')}: "
                                   f"{msg.get('message')}")

    # ---------------- the round ----------------
    async def run_round(self, ws, kind: str = "training") -> dict | None:
        """Play one round.  Returns the round_over message, or None if refused."""
        self.records = [r for r in self.records
                        if r["msg"].get("type") in ("join", "welcome")]
        self.notes = []
        memory = self.load_memory()
        hook = getattr(self.strategy, "on_round_start", None)
        if hook:
            try:
                hook(memory)
            except Exception as exc:
                self.notes.append(f"on_round_start raised: {exc!r}")

        solve = self.strategy.solve
        cap = self.max_solution_chars
        latencies: list[float] = []
        skips = 0
        started = False
        self.last_refusal = None

        await self.send(ws, {"type": "start_round" if kind == "training"
                             else "start_final"})

        # ---- hot loop: no printing, no disk I/O ----
        round_over, closed_exc = None, None
        try:
            while True:
                raw = await ws.recv()
                t0 = time.perf_counter()
                msg = json.loads(raw)
                self.records.append({"ts": time.time(), "dir": "in", "msg": msg})
                mtype = msg.get("type")

                if mtype == "challenge":
                    try:
                        memory["_index"] = msg["index"]
                        solution = solve(msg["name"], msg["clue"], memory)
                        if solution is None:
                            raise _Skip()
                        if not isinstance(solution, str):
                            solution = str(solution)
                        if len(solution) > cap:
                            solution = solution[:cap]
                        out = {"type": "answer", "round_id": msg["round_id"],
                               "index": msg["index"], "solution": solution}
                    except Exception as exc:                       # never die mid-round
                        skips += 1
                        if len(self.notes) < 20 and not isinstance(exc, _Skip):
                            self.notes.append(
                                f"solve({msg.get('name')!r}) raised: {exc!r} -> skip")
                        out = {"type": "skip", "round_id": msg["round_id"],
                               "index": msg["index"]}
                    self.records.append({"ts": time.time(), "dir": "out", "msg": out})
                    await ws.send(json.dumps(out))
                    latencies.append(time.perf_counter() - t0)

                elif mtype == "result":
                    continue
                elif mtype == "round_over":
                    round_over = msg
                    break
                elif mtype == "round_started":
                    started = True
                    continue
                elif mtype == "error":
                    if msg.get("code") == "stale":
                        continue             # a leftover reply to a late answer from an earlier round
                    if not started:          # the round never began: cooldown/phase/...
                        self.last_refusal = msg
                        self.report_refusal(msg)
                        return None
                    continue                 # mid-round noise, e.g. code "stale"
                elif mtype == "pong":
                    continue
        except websockets.exceptions.ConnectionClosed as exc:
            # the socket died mid-round (another `join` for this team, a server
            # restart...).  Salvage the log rather than losing the round.
            self.notes.append(f"connection closed mid-round: {exc!r}")
            round_over, closed_exc = self.salvage(kind), exc
        # ---- end hot loop ----

        self.absorb(round_over)
        items = round_over.get("items") or []
        hook = getattr(self.strategy, "on_round_end", None)
        if hook:
            try:
                hook(items, memory)
            except Exception as exc:
                self.notes.append(f"on_round_end raised: {exc!r}")
        self.save_memory(memory)

        stats = self.latency_stats(latencies)
        self.write_logs(round_over, stats, skips)
        self.print_round(round_over, stats, skips)
        if closed_exc is not None:            # logs are safe; now report the drop
            raise closed_exc
        return round_over

    def salvage(self, kind: str) -> dict:
        """Rebuild a round_over-shaped summary from the buffered messages."""
        chal, ans, res, rid = {}, {}, {}, None
        for rec in self.records:
            m = rec["msg"]
            t = m.get("type")
            if t == "challenge":
                chal[m["index"]] = m
                rid = m.get("round_id")
            elif t in ("answer", "skip"):
                ans[m["index"]] = m.get("solution", "")
            elif t == "result":
                res[m["index"]] = m.get("score", 0)
        items = [{"index": i, "name": chal[i].get("name"),
                  "clue": chal[i].get("clue"), "solution": ans.get(i, ""),
                  "score": res.get(i, 0)}
                 for i in sorted(res) if i in chal]
        return {"type": "round_over", "round_id": rid, "kind": kind,
                "presented": len(items),
                "answered": sum(1 for i in res if ans.get(i)),
                "correct": sum(res.values()), "items": items, "_partial": True}

    @staticmethod
    def latency_stats(latencies: list[float]) -> dict:
        if not latencies:
            return {"n": 0, "mean_ms": 0.0, "max_ms": 0.0, "p50_ms": 0.0}
        ms = sorted(x * 1000.0 for x in latencies)
        return {
            "n": len(ms),
            "mean_ms": sum(ms) / len(ms),
            "max_ms": ms[-1],
            "p50_ms": ms[len(ms) // 2],
        }

    def report_refusal(self, msg: dict) -> None:
        retry_at = msg.get("retry_at")
        line = f"[server] {msg.get('code')}: {msg.get('message')}"
        if retry_at:
            wait = max(0.0, self.to_local(retry_at) - time.time())
            line += f"  retry_at={iso(retry_at)} (in {wait:.0f}s)"
        print(line)

    # ---------------- reporting ----------------
    def round_label(self, round_over: dict) -> str:
        if round_over.get("_partial"):
            return "partial"
        if round_over.get("kind") == "final":
            return "final"
        n = round_over.get("rounds_used")
        if n is None:                       # server did not say; count locally
            self.rounds_used = (self.rounds_used or 0) + 1
            n = self.rounds_used
        return str(n)

    def print_round(self, ro: dict, stats: dict, skips: int) -> None:
        label = self.round_label(ro)
        pres = ro.get("presented", 0)
        print(f"round {label} ({ro.get('kind')}): presented={pres} "
              f"answered={ro.get('answered', 0)} correct={ro.get('correct', 0)}"
              + (f" skipped={skips}" if skips else ""))
        print(f"client answer latency: mean {stats['mean_ms']:.3f} ms, "
              f"median {stats['p50_ms']:.3f} ms, max {stats['max_ms']:.3f} ms "
              f"(n={stats['n']})")
        for note in self.notes[:5]:
            print(f"[warn] {note}")
        nxt = ro.get("next_round_available_at")
        if nxt and ro.get("kind") != "final":
            print(f"next round available at {iso(nxt)}")
        print(f"logs: {self.log_dir/('round_' + label + '.txt')}")

    def write_logs(self, ro: dict, stats: dict, skips: int) -> None:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        label = self.round_label(ro)

        with open(self.log_dir / f"round_{label}.jsonl", "w", encoding="utf-8") as fh:
            for rec in self.records:
                fh.write(json.dumps(rec, default=str) + "\n")

        items = ro.get("items") or []
        tally: dict[str, list[int]] = {}
        for it in items:
            t = tally.setdefault(it.get("name", "?"), [0, 0])
            t[0] += 1
            t[1] += int(it.get("score") or 0)

        lines = []
        lines.append(f"Centaur Zendo round {label} ({ro.get('kind')})")
        lines.append(f"round_id : {ro.get('round_id')}")
        lines.append(f"written  : {iso(time.time())}")
        lines.append(f"presented={ro.get('presented', 0)}  "
                     f"answered={ro.get('answered', 0)}  "
                     f"correct={ro.get('correct', 0)}  skipped={skips}")
        lines.append(f"client answer latency: mean {stats['mean_ms']:.3f} ms  "
                     f"median {stats['p50_ms']:.3f} ms  max {stats['max_ms']:.3f} ms  "
                     f"(n={stats['n']})")
        for note in self.notes:
            lines.append(f"warn: {note}")
        lines.append("")
        lines.append(f"{'idx':>4}  {cell('name', 12)}  {cell('clue', 40)}  "
                     f"{cell('answer', 40)}  score")
        lines.append("-" * 108)
        for it in items:
            lines.append(f"{it.get('index', -1):>4}  {cell(it.get('name'), 12)}  "
                         f"{cell(it.get('clue'), 40)}  "
                         f"{cell(it.get('solution'), 40)}  "
                         f"{it.get('score')}")
        lines.append("")
        lines.append("per-name tally this round")
        lines.append(f"{cell('name', 16)} {'presented':>9} {'correct':>7} {'hit-rate':>9}")
        for name in sorted(tally):
            pres, corr = tally[name]
            lines.append(f"{cell(name, 16)} {pres:>9} {corr:>7} "
                         f"{100.0 * corr / pres:>8.1f}%")
        lines.append("")
        with open(self.log_dir / f"round_{label}.txt", "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))

        if not ro.get("_partial"):        # a cut-off round is not a real result
            self.update_summary(ro, stats, skips, tally)

    def update_summary(self, ro: dict, stats: dict, skips: int, tally: dict) -> None:
        try:
            with open(self.history_path, "r", encoding="utf-8") as fh:
                hist = json.load(fh)
        except Exception:
            hist = {"rounds": [], "names": {}}
        hist.setdefault("rounds", [])
        hist.setdefault("names", {})

        label = self.round_label(ro)
        hist["rounds"] = [r for r in hist["rounds"] if r.get("label") != label]
        hist["rounds"].append({
            "label": label, "kind": ro.get("kind"), "ts": time.time(),
            "presented": ro.get("presented", 0), "answered": ro.get("answered", 0),
            "correct": ro.get("correct", 0), "skipped": skips,
            "mean_ms": round(stats["mean_ms"], 3),
        })
        for name, (pres, corr) in tally.items():
            slot = hist["names"].setdefault(name, {"presented": 0, "correct": 0})
            slot["presented"] += pres
            slot["correct"] += corr
        with open(self.history_path, "w", encoding="utf-8") as fh:
            json.dump(hist, fh, indent=1)

        out = [f"Centaur Zendo — team {self.args.team} — updated {iso(time.time())}",
               "",
               f"{'round':>6} {cell('kind', 9)} {'presented':>9} {'answered':>8} "
               f"{'correct':>7} {'hit-rate':>9} {'skipped':>7} {'mean_ms':>8}",
               "-" * 76]
        for r in hist["rounds"]:
            hr = (100.0 * r["correct"] / r["presented"]) if r["presented"] else 0.0
            out.append(f"{r['label']:>6} {cell(r['kind'], 9)} {r['presented']:>9} "
                       f"{r['answered']:>8} {r['correct']:>7} {hr:>8.1f}% "
                       f"{r.get('skipped', 0):>7} {r.get('mean_ms', 0):>8.3f}")
        out += ["", "running per-name hit-rate (all rounds)",
                f"{cell('name', 16)} {'presented':>9} {'correct':>7} {'hit-rate':>9}",
                "-" * 45]
        for name in sorted(hist["names"],
                           key=lambda n: (-hist["names"][n]["presented"], n)):
            s = hist["names"][name]
            hr = (100.0 * s["correct"] / s["presented"]) if s["presented"] else 0.0
            out.append(f"{cell(name, 16)} {s['presented']:>9} {s['correct']:>7} "
                       f"{hr:>8.1f}%")
        out.append("")
        with open(self.log_dir / "summary.txt", "w", encoding="utf-8") as fh:
            fh.write("\n".join(out))

    # ---------------- commands ----------------
    async def cmd_status(self, ws) -> None:
        await self.send(ws, {"type": "status"})
        while True:
            msg = await self.recv(ws)
            self.absorb(msg)
            if msg.get("type") == "status":
                print(f"phase              : {msg.get('phase')}")
                print(f"server_time        : {iso(msg.get('server_time'))}")
                print(f"training_ends_at   : {iso(msg.get('training_ends_at'))}")
                print(f"final_ends_at      : {iso(msg.get('final_ends_at'))}")
                print(f"rounds_used        : {msg.get('rounds_used')}"
                      + (f" / {self.max_training_rounds}"
                         if self.max_training_rounds else ""))
                print(f"next round at      : {iso(msg.get('next_round_available_at'))}")
                print(f"demo_available     : {msg.get('demo_available')}")
                print(f"final_score        : {msg.get('final_score')}")
                print(f"challenge names    : {', '.join(self.challenges) or '-'}")
                lb = msg.get("leaderboard") or []
                if lb:
                    print("leaderboard        :")
                    for row in lb:
                        print(f"   {row}")
                return
            if msg.get("type") == "error":
                self.report_refusal(msg)
                return

    async def cmd_demo(self, ws, name: str) -> None:
        await self.send(ws, {"type": "demo", "name": name})
        while True:
            msg = await self.recv(ws)
            self.absorb(msg)
            if msg.get("type") == "demo_result":
                print(f"demo {msg.get('name')}")
                print(f"  clue    : {msg.get('clue')}")
                print(f"  solution: {msg.get('solution')}")
                print(f"  score   : {msg.get('score')}")
                self.log_dir.mkdir(parents=True, exist_ok=True)
                with open(self.log_dir / "demos.jsonl", "a", encoding="utf-8") as fh:
                    fh.write(json.dumps({"ts": time.time(), "demo": msg}) + "\n")
                print(f"logs: {self.log_dir/'demos.jsonl'}")
                return
            if msg.get("type") == "error":
                self.report_refusal(msg)
                return

    async def wait_until(self, server_ts: float | None, label: str = "") -> None:
        if not server_ts:
            return
        delay = self.to_local(server_ts) - time.time()
        if delay <= 0:
            return
        print(f"waiting {delay:.0f}s until {iso(server_ts)}{label}")
        await asyncio.sleep(delay)

    async def cmd_wait_round(self, ws) -> dict | None:
        """Sleep until we are allowed to start, then run one training round."""
        for attempt in range(6):
            await self.wait_until(self.next_round_available_at, " (cooldown)")
            ro = await self.run_round(ws, "training")
            if ro is not None:
                return ro
            ref = self.last_refusal or {}
            code, retry_at = ref.get("code"), ref.get("retry_at")
            if code == "round_cap":
                print("no training rounds left — when the final window opens, "
                      "run:  python player.py final")
                return None
            if code == "phase" and not retry_at:
                print(f"training is not open (phase={self.phase}); nothing to wait "
                      f"for")
                return None
            if retry_at:
                self.next_round_available_at = retry_at
            else:
                await asyncio.sleep(1.0 + attempt)
        print("gave up waiting for a round slot")
        return None

    async def cmd_watch(self, ws) -> None:
        played = 0
        while True:
            if self.max_training_rounds is not None and \
                    self.rounds_used >= self.max_training_rounds:
                print(f"all {self.max_training_rounds} training rounds used — "
                      f"when the final window opens, run:  "
                      f"python player.py final")
                return
            if self.args.max_rounds and played >= self.args.max_rounds:
                print(f"played {played} rounds (--max-rounds)")
                return
            ro = await self.cmd_wait_round(ws)
            if ro is None:
                return
            played += 1

    # ---------------- driver ----------------
    async def main(self) -> int:
        async with websockets.connect(self.args.url, open_timeout=10,
                                      max_size=2 ** 22) as ws:
            welcome = await self.join(ws)
            print(f"joined as {welcome.get('team')} — phase={welcome.get('phase')} "
                  f"rounds_used={welcome.get('rounds_used')} "
                  f"challenges={len(self.challenges)}")
            cmd = self.args.command
            if cmd == "status":
                await self.cmd_status(ws)
            elif cmd == "round":
                if await self.run_round(ws, "training") is None:
                    return 2
            elif cmd == "final":
                if await self.run_round(ws, "final") is None:
                    return 2
            elif cmd == "demo":
                if not self.args.name:
                    print("demo needs a challenge name")
                    return 2
                await self.cmd_demo(ws, self.args.name)
            elif cmd == "wait-round":
                if await self.cmd_wait_round(ws) is None:
                    return 2
            elif cmd == "watch":
                await self.cmd_watch(ws)
        return 0


def build_parser() -> argparse.ArgumentParser:
    here = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(
        prog="player.py", description="Centaur Zendo reference player client")
    p.add_argument("--url", default=os.environ.get("ZENDO_URL",
                                                   "ws://localhost:8080/ws"))
    p.add_argument("--team", default=os.environ.get("ZENDO_TEAM", "team"))
    p.add_argument("--token", default=os.environ.get("ZENDO_TOKEN", "secret"))
    p.add_argument("--strategy", default=str(here / "strategy.py"),
                   help="path to the strategy module (default: strategy.py "
                        "next to player.py)")
    p.add_argument("--log-dir", default=None,
                   help="default: logs/ next to the strategy file")
    p.add_argument("--memory", default=None,
                   help="default: memory.json next to the strategy file")
    p.add_argument("--max-rounds", type=int, default=0,
                   help="watch: stop after this many rounds (0 = no limit)")
    p.add_argument("command", choices=["round", "final", "demo", "status",
                                       "wait-round", "watch"])
    p.add_argument("name", nargs="?", help="challenge name, for `demo`")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    strategy_path = Path(args.strategy).resolve()
    base = strategy_path.parent
    if args.log_dir is None:
        args.log_dir = str(base / "logs")
    if args.memory is None:
        args.memory = str(base / "memory.json")
    try:
        strategy = load_strategy(strategy_path)
    except Exception as exc:
        print(f"[fatal] cannot load strategy {strategy_path}: {exc!r}")
        return 2
    player = Player(args, strategy)
    try:
        return asyncio.run(player.main())
    except KeyboardInterrupt:
        return 130
    except BrokenPipeError:                      # e.g. `player.py status | head`
        try:
            sys.stdout.close()
        except Exception:
            pass
        return 0
    except (OSError, websockets.exceptions.WebSocketException) as exc:
        print(f"[fatal] connection problem: {exc!r}")
        return 3
    except RuntimeError as exc:
        print(f"[fatal] {exc}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
