"""A tiny stand-in for engine/server.py that speaks SPEC §6 exactly.

Two challenge classes:
    ADD  — clue "3+4",  correct answer "7"
    ECHO — clue "abc",  correct answer "abc"
Deterministic: the sequence of (name, clue) per round comes from a fixed seed,
and a round ends after `items_per_round` items (or at the deadline, whichever
comes first) so tests do not depend on wall-clock speed.
"""
from __future__ import annotations

import asyncio
import json
import random
import time
import uuid

import websockets


class FakeServer:
    def __init__(self, *, items_per_round=6, round_seconds=5.0, final_seconds=5.0,
                 cooldown_seconds=0.0, max_training_rounds=12,
                 max_solution_chars=16, phase="training", seed=7,
                 next_round_delay=0.0, refuse_first_round=None,
                 lobby_opens_in=None, close_after=None):
        self.items_per_round = items_per_round
        self.round_seconds = round_seconds
        self.final_seconds = final_seconds
        self.cooldown_seconds = cooldown_seconds
        self.max_training_rounds = max_training_rounds
        self.max_solution_chars = max_solution_chars
        self.phase = phase
        self.seed = seed
        self.next_round_delay = next_round_delay
        self.refuse_first_round = refuse_first_round   # None or "cooldown"
        self.lobby_opens_in = lobby_opens_in           # seconds until phase=training
        self.opens_at = None
        self.close_after = close_after      # drop the socket after N items
        self.rounds_used = 0
        self.demo_available = True
        self.final_score = None
        self.final_done = False
        self.next_round_available_at = 0.0
        self.inbox: list[dict] = []                    # everything the client sent
        self.answers: list[dict] = []
        self.server = None
        self.url = None

    # -------- challenge generation --------
    def gen(self, rng):
        if rng.random() < 0.5:
            a, b = rng.randrange(10), rng.randrange(10)
            return "ADD", f"{a}+{b}", str(a + b)
        w = "".join(rng.choice("abcdefgh") for _ in range(rng.randint(2, 5)))
        return "ECHO", w, w

    # -------- lifecycle --------
    async def start(self):
        self.server = await websockets.serve(self.handler, "127.0.0.1", 0)
        port = next(iter(self.server.sockets)).getsockname()[1]
        self.url = f"ws://127.0.0.1:{port}/ws"
        return self.url

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()

    async def send(self, ws, msg):
        await ws.send(json.dumps(msg))

    def welcome(self):
        return {
            "type": "welcome", "team": self.team, "phase": self.phase,
            "challenges": ["ADD", "ECHO"],
            "config": {"round_seconds": self.round_seconds,
                       "final_seconds": self.final_seconds,
                       "cooldown_seconds": self.cooldown_seconds,
                       "max_training_rounds": self.max_training_rounds,
                       "max_solution_chars": self.max_solution_chars,
                       "max_clue_chars": 1024,
                       "training_ends_at": time.time() + 3600,
                       "final_ends_at": time.time() + 4200},
            "rounds_used": self.rounds_used,
            "next_round_available_at": self.next_round_available_at,
            "demo_available": self.demo_available,
            "server_time": time.time(),
        }

    # -------- protocol --------
    async def handler(self, ws):
        self.team = "?"
        try:
            async for raw in ws:
                msg = json.loads(raw)
                self.inbox.append(msg)
                t = msg.get("type")
                if t == "join":
                    self.team = msg.get("team", "?")
                    if self.lobby_opens_in is not None and self.opens_at is None:
                        self.opens_at = time.time() + self.lobby_opens_in
                    if self.next_round_delay:
                        self.next_round_available_at = (time.time()
                                                        + self.next_round_delay)
                    await self.send(ws, self.welcome())
                elif t == "ping":
                    await self.send(ws, {"type": "pong",
                                         "server_time": time.time()})
                elif t == "status":
                    await self.send(ws, {
                        "type": "status", "phase": self.phase,
                        "server_time": time.time(),
                        "training_ends_at": time.time() + 3600,
                        "final_ends_at": time.time() + 4200,
                        "rounds_used": self.rounds_used,
                        "next_round_available_at": self.next_round_available_at,
                        "demo_available": self.demo_available,
                        "final_score": self.final_score,
                        "leaderboard": [{"team": self.team, "final_score": 0}]})
                elif t == "demo":
                    await self.handle_demo(ws, msg)
                elif t == "start_round":
                    await self.handle_round(ws, "training")
                elif t == "start_final":
                    await self.handle_round(ws, "final")
                else:
                    await self.send(ws, {"type": "error", "code": "unknown",
                                         "message": f"unknown type {t}"})
        except websockets.exceptions.ConnectionClosed:
            pass

    async def handle_demo(self, ws, msg):
        name = msg.get("name")
        if not self.demo_available:
            await self.send(ws, {"type": "error", "code": "demo",
                                 "message": "no demo available"})
            return
        if name not in ("ADD", "ECHO"):
            await self.send(ws, {"type": "error", "code": "unknown_challenge",
                                 "message": f"no challenge {name}"})
            return
        self.demo_available = False
        clue, sol = ("3+4", "7") if name == "ADD" else ("abc", "abc")
        await self.send(ws, {"type": "demo_result", "name": name, "clue": clue,
                             "solution": sol, "score": 1})

    async def handle_round(self, ws, kind):
        now = time.time()
        if self.phase == "lobby":
            if self.opens_at is not None and now >= self.opens_at:
                self.phase = "training"
            else:
                await self.send(ws, {"type": "error", "code": "phase",
                                     "message": "the game has not started",
                                     "retry_at": self.opens_at})
                return
        if self.refuse_first_round and self.rounds_used == 0:
            self.refuse_first_round = None
            await self.send(ws, {"type": "error", "code": "cooldown",
                                 "message": "too soon",
                                 "retry_at": now + 0.2})
            return
        if kind == "training" and self.rounds_used >= self.max_training_rounds:
            await self.send(ws, {"type": "error", "code": "round_cap",
                                 "message": "no rounds left"})
            return
        if kind == "training" and now < self.next_round_available_at:
            await self.send(ws, {"type": "error", "code": "cooldown",
                                 "message": "cooldown",
                                 "retry_at": self.next_round_available_at})
            return
        if kind == "final" and self.final_done:
            await self.send(ws, {"type": "error", "code": "phase",
                                 "message": "final already run"})
            return

        duration = self.round_seconds if kind == "training" else self.final_seconds
        round_id = str(uuid.uuid4())
        started = time.time()
        deadline = started + duration
        self.demo_available = False
        rng = random.Random(self.seed + self.rounds_used)
        await self.send(ws, {"type": "round_started", "round_id": round_id,
                             "kind": kind, "duration_ms": int(duration * 1000),
                             "started_at": started, "deadline": deadline})
        items, presented, answered, correct = [], 0, 0, 0
        for index in range(self.items_per_round):
            if time.time() >= deadline:
                break
            if self.close_after is not None and index >= self.close_after:
                await ws.close()
                return
            name, clue, want = self.gen(rng)
            presented += 1
            await self.send(ws, {"type": "challenge", "round_id": round_id,
                                 "index": index, "name": name, "clue": clue})
            try:
                reply = json.loads(await asyncio.wait_for(
                    ws.recv(), timeout=max(0.01, deadline - time.time())))
            except (asyncio.TimeoutError, TimeoutError):
                presented -= 1
                break
            self.inbox.append(reply)
            self.answers.append(reply)
            if reply.get("round_id") != round_id or reply.get("index") != index:
                await self.send(ws, {"type": "error", "code": "stale",
                                     "message": "stale answer"})
                continue
            if reply.get("type") == "skip":
                sol, score = "", 0
            else:
                sol = str(reply.get("solution", ""))[: self.max_solution_chars]
                score = int(sol == want)
                answered += 1
            correct += score
            items.append({"index": index, "name": name, "clue": clue,
                          "solution": sol, "score": score})
            await self.send(ws, {"type": "result", "round_id": round_id,
                                 "index": index, "score": score})
        if kind == "training":
            self.rounds_used += 1
            self.next_round_available_at = time.time() + self.cooldown_seconds
        else:
            self.final_done = True
            self.final_score = correct
        self.demo_available = True
        await self.send(ws, {"type": "round_over", "round_id": round_id,
                             "kind": kind, "presented": presented,
                             "answered": answered, "correct": correct,
                             "items": items, "rounds_used": self.rounds_used,
                             "next_round_available_at":
                                 self.next_round_available_at,
                             "demo_available": self.demo_available})
