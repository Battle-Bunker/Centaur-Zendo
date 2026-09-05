"""Centaur Zendo game state machine (SPEC §5).

Pure asyncio, no network code.  The challenge pool is *injected* and only has to
be duck-typed:

    pool.names                                  -> list[str]
    await pool.generate(name, seed) -> str
    await pool.score(name, clue, solution) -> int   (0/1, never raises)
    await pool.solve(name, clue) -> str

Optionally a pool may expose ``lease()`` returning an async context manager that
yields an object with the same three coroutine methods.  When present, a round
takes one lease for its whole duration so concurrent teams never contend for the
same sandbox worker.  ``SandboxPoolAdapter`` (bottom of this file) wraps the
engine's ``CompiledPool`` + ``SandboxPool`` into exactly that shape.
"""
from __future__ import annotations

import asyncio
import contextlib
import inspect
import json
import logging
import os
import random
import secrets
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - the real dataclass lives in engine/config.py
    from engine.config import GameConfig

log = logging.getLogger("zendo.game")

DEMO_REDRAWS = 8  # demo(): re-draw a seed this many times to avoid an identity (n = 0) example


def _norm(text: Any) -> str:
    return "\n".join(line.rstrip() for line in str(text).strip().splitlines())


LOBBY = "lobby"
TRAINING = "training"
FINAL = "final"
FINISHED = "finished"

# Defaults mirror SPEC §5; they are only used when a config object omits a field,
# which keeps the engine running against a partially-implemented GameConfig.
_DEFAULTS = {
    "round_seconds": 1.0,
    "final_seconds": 3.0,
    "cooldown_seconds": 300.0,
    "max_training_rounds": 4,
    "training_seconds": None,
    "final_window_seconds": 600.0,
    "max_demos": 3,
    "pool_size": None,
    "pool_seed": None,
    "open_registration": True,
    "challenge_dir": "challenges",
    "event_log": "events.jsonl",
    "sandbox_workers": 4,
    "final_shared_sequence": True,
    "max_solution_chars": 4096,
    "max_clue_chars": 1024,
    "validation_seed": 12345,
    "admin_token": "",
}


def conf(config: Any, key: str, default: Any = None) -> Any:
    """Read ``key`` off a GameConfig-ish object, falling back to the SPEC default."""
    if default is None:
        default = _DEFAULTS.get(key)
    if config is None:
        return default
    if isinstance(config, dict):
        value = config.get(key, default)
    else:
        value = getattr(config, key, default)
    return value


class GameError(Exception):
    """A refusal that maps 1:1 onto the protocol's ``error`` frame."""

    def __init__(self, code: str, message: str, retry_at: Optional[float] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.retry_at = retry_at

    def to_message(self) -> dict:
        msg = {"type": "error", "code": self.code, "message": self.message}
        if self.retry_at is not None:
            msg["retry_at"] = self.retry_at
        return msg

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"GameError({self.code!r}, {self.message!r}, retry_at={self.retry_at!r})"


@dataclass
class Item:
    """One challenge presented inside a round."""

    index: int
    name: str
    clue: str
    solution: Optional[str] = None
    score: int = 0
    answered: bool = False
    resolved: bool = False
    sent_at: float = 0.0
    resolved_at: float = 0.0

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "name": self.name,
            "clue": self.clue,
            "solution": self.solution,
            "score": self.score,
        }


@dataclass
class Team:
    name: str
    token: str
    rounds_used: int = 0
    last_round_started_at: Optional[float] = None
    demos_used: int = 0
    final_score: Optional[int] = None
    final_answered: int = 0
    final_done: bool = False
    history: list = field(default_factory=list)
    created_at: float = 0.0
    current_round: Optional["Round"] = None

    @property
    def busy(self) -> bool:
        return self.current_round is not None


class Round:
    """Drives the challenge stream for one team (SPEC §5 "Round loop").

    Server usage::

        r = game.start_round(team, "training")
        await r.open()                     # takes a sandbox lease, starts the clock
        send round_started(r.started_message())
        while True:
            item = await r.next_challenge()
            if item is None:
                break
            send challenge(...)
            solution = await wait_for_answer(deadline=r.deadline)   # None => skip
            if timed_out:
                break
            score = await r.submit(item.index, solution)
            send result(...)
            if r.expired():
                break
        send round_over(await r.finish())

    ``result`` for index *i* is therefore always sent before ``challenge`` for
    *i+1*.  The next challenge is generated in the background while the server
    waits for the current answer, so ``next_challenge()`` normally returns
    instantly and the answer→challenge turnaround is one ``score`` call.
    """

    MAX_GENERATE_TRIES = 3

    def __init__(self, game: "Game", team: Team, kind: str, seed: int, duration: float):
        self.game = game
        self.team = team
        self.kind = kind
        self.round_id = uuid.uuid4().hex
        self.seed = seed
        self.duration = float(duration)
        self.rng = random.Random(seed)
        self.created_at = game.clock()
        self.started_at: Optional[float] = None
        self.deadline: Optional[float] = None
        self.ended_at: Optional[float] = None
        self.items: list[Item] = []
        self.finished = False
        self.aborted = False
        self.end_reason: Optional[str] = None
        self._pending: Optional[Item] = None
        self._next_index = 0
        self._prefetch: Optional[asyncio.Task] = None
        self._lease_cm = None
        self._sb = None
        self._generate_failures = 0

    # -- lifecycle ---------------------------------------------------------
    async def open(self) -> "Round":
        """Acquire a sandbox worker (if the pool leases them) and start the clock."""
        if self.started_at is not None:
            return self
        pool = self.game.pool
        lease = getattr(pool, "lease", None)
        if callable(lease):
            self._lease_cm = lease()
            self._sb = await self._lease_cm.__aenter__()
        else:
            self._sb = pool
        self.started_at = self.game.clock()
        self.deadline = self.started_at + self.duration
        self.team.last_round_started_at = self.started_at
        return self

    def expired(self) -> bool:
        return self.deadline is not None and self.game.clock() >= self.deadline

    def started_message(self) -> dict:
        return {
            "type": "round_started",
            "round_id": self.round_id,
            "kind": self.kind,
            "duration_ms": int(round(self.duration * 1000)),
            "started_at": self.started_at,
            "deadline": self.deadline,
        }

    # -- challenge stream --------------------------------------------------
    async def _make_item(self, index: int) -> Optional[Item]:
        """Draw (name, seed) and generate a clue; retries a few times on sandbox errors."""
        names = list(self.game.pool.names)
        if not names:
            return None
        for _ in range(self.MAX_GENERATE_TRIES):
            name = self.rng.choice(names)
            seed = self.rng.getrandbits(32)
            try:
                clue = await self._sb.generate(name, seed)
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # SandboxError & friends: log and pick again
                self._generate_failures += 1
                log.warning("generate(%s, %s) failed in round %s: %s", name, seed, self.round_id, exc)
                continue
            if not isinstance(clue, str) or not clue:
                self._generate_failures += 1
                log.warning("generate(%s, %s) returned a bad clue in round %s", name, seed, self.round_id)
                continue
            return Item(index=index, name=name, clue=clue)
        return None

    async def next_challenge(self) -> Optional[Item]:
        """Return the next challenge, or None when the round is over."""
        await self.open()
        if self.finished or self.aborted or self.expired():
            return None
        if self._pending is not None:
            raise RuntimeError("next_challenge() called while an answer is still pending")

        task, self._prefetch = self._prefetch, None
        if task is not None:
            try:
                item = await task
            except asyncio.CancelledError:
                item = None
        else:
            item = await self._make_item(self._next_index)
        if item is None:
            return None

        item.index = self._next_index
        self._next_index += 1
        item.sent_at = self.game.clock()
        self.items.append(item)
        self._pending = item
        if not self.expired():
            self._prefetch = asyncio.ensure_future(self._make_item(self._next_index))
        return item

    async def submit(self, index: int, solution: Optional[str]) -> int:
        """Score (or skip) the pending challenge.  Raises GameError('stale') for
        anything that is not the challenge currently awaiting an answer, and for
        anything arriving at/after the deadline."""
        if self.finished or self.aborted:
            raise GameError("stale", "round is over")
        item = self._pending
        if item is None or item.index != index:
            raise GameError("stale", f"no challenge {index} is awaiting an answer")
        now = self.game.clock()
        if self.deadline is not None and now >= self.deadline:
            raise GameError("stale", "answer arrived after the round deadline")

        if solution is None:
            item.solution = None
            item.answered = False
            item.score = 0
        else:
            cap = int(conf(self.game.config, "max_solution_chars"))
            sol = str(solution)[:cap]
            item.solution = sol
            item.answered = True
            try:
                raw = await self._sb.score(item.name, item.clue, sol)
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # a scorer must never break a round
                log.warning("score(%s) failed in round %s: %s", item.name, self.round_id, exc)
                raw = 0
            item.score = 1 if raw == 1 else 0
        item.resolved = True
        item.resolved_at = now
        self._pending = None
        return item.score

    # -- teardown ----------------------------------------------------------
    @property
    def resolved_items(self) -> list[Item]:
        return [i for i in self.items if i.resolved]

    def counts(self) -> tuple[int, int, int]:
        done = self.resolved_items
        presented = len(done)
        answered = sum(1 for i in done if i.answered)
        correct = sum(i.score for i in done)
        return presented, answered, correct

    async def _release(self) -> None:
        task, self._prefetch = self._prefetch, None
        if task is not None:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await task
        if self._lease_cm is not None:
            cm, self._lease_cm = self._lease_cm, None
            with contextlib.suppress(Exception):
                await cm.__aexit__(None, None, None)
        self._sb = None

    async def finish(self, reason: str = "deadline") -> dict:
        """End the round, release the sandbox and return the round_over payload."""
        if self.finished:
            return self.summary()
        self.finished = True
        self.end_reason = reason
        self.ended_at = self.game.clock()
        self._pending = None
        await self._release()
        self.game._round_ended(self)
        return self.summary()

    async def abort(self, reason: str = "aborted") -> dict:
        self.aborted = True
        return await self.finish(reason)

    def summary(self) -> dict:
        presented, answered, correct = self.counts()
        return {
            "round_id": self.round_id,
            "kind": self.kind,
            "presented": presented,
            "answered": answered,
            "correct": correct,
            "items": [i.to_dict() for i in self.resolved_items],
        }

    def record(self) -> dict:
        """Fuller summary for the event log / team history."""
        rec = self.summary()
        rec.update(
            {
                "team": self.team.name,
                "seed": self.seed,
                "started_at": self.started_at,
                "ended_at": self.ended_at,
                "duration": self.duration,
                "end_reason": self.end_reason,
                "aborted": self.aborted,
                "generate_failures": self._generate_failures,
            }
        )
        return rec


class ActivePool:
    """A view of the loaded challenge pool restricted to the classes drawn for THIS game.

    SPEC §5: a game uses `pool_size` classes (default 7) drawn once at game creation with
    `pool_seed`; every other attribute (generate/solve/score/lease...) is delegated to the
    underlying pool, which may hold many more classes than are in play.
    """

    def __init__(self, pool: Any, pool_size: Optional[int], pool_seed: Optional[int]):
        self._pool = pool
        names = sorted(getattr(pool, "names", []) or [])
        if pool_size is not None and 0 < int(pool_size) < len(names):
            rng = random.Random(int(pool_seed) if pool_seed is not None else secrets.randbits(32))
            names = sorted(rng.sample(names, int(pool_size)))
        self.names: list[str] = names

    def __getattr__(self, item):
        return getattr(self._pool, item)

    def __len__(self) -> int:
        return len(self.names)

    def __iter__(self):
        return iter(self.names)


class Game:
    """Teams, phases, rounds, cooldowns, demos, the final and the leaderboard."""

    def __init__(
        self,
        config: "GameConfig",
        pool: Any,
        clock: Callable[[], float] = time.time,
        event_log: Optional[str] = None,
    ):
        self.config = config
        self.pool = ActivePool(pool, conf(config, "pool_size", None), conf(config, "pool_seed", None))
        self.clock = clock
        self.teams: dict[str, Team] = {}
        self.phase = LOBBY
        self.created_at = clock()
        self.started_at: Optional[float] = None
        self.training_ends_at: Optional[float] = None
        self.final_ends_at: Optional[float] = None
        self.round_counter = 0
        path = event_log if event_log is not None else conf(config, "event_log")
        self.event_log_path: Optional[str] = path or None
        self._event_fh = None
        self._rng = random.Random()
        # SPEC §5: the final uses one shared (name, seed) sequence for every team.
        # config.final_seed = None means "pick one at random", but it must still be
        # the *same* one for everybody, so it is drawn once here.
        seed = conf(config, "final_seed", None)
        self.final_seed = int(seed) if seed is not None else self._rng.getrandbits(32)

    # -- config helpers ----------------------------------------------------
    @property
    def cooldown_seconds(self) -> float:
        return float(conf(self.config, "cooldown_seconds"))

    @property
    def max_training_rounds(self) -> int:
        return int(conf(self.config, "max_training_rounds"))

    @property
    def training_duration(self) -> float:
        """SPEC §5: None ⇒ max_training_rounds * cooldown_seconds + 60."""
        value = conf(self.config, "training_seconds")
        if value is None:
            value = self.max_training_rounds * self.cooldown_seconds + 60
        return float(value)

    @property
    def final_window_seconds(self) -> float:
        return float(conf(self.config, "final_window_seconds"))

    @property
    def max_demos(self) -> int:
        return int(conf(self.config, "max_demos"))

    def demos_remaining(self, team: Team) -> int:
        return max(0, self.max_demos - team.demos_used)

    # -- event log ---------------------------------------------------------
    def log_event(self, team: Optional[str], direction: str, msg: Any) -> None:
        if not self.event_log_path:
            return
        try:
            if self._event_fh is None:
                self._event_fh = open(self.event_log_path, "a", encoding="utf-8")
            line = json.dumps({"ts": self.clock(), "team": team, "dir": direction, "msg": msg},
                              default=str)
            self._event_fh.write(line + "\n")
            self._event_fh.flush()
        except Exception as exc:  # logging must never take the server down
            log.warning("event log write failed: %s", exc)

    def close(self) -> None:
        if self._event_fh is not None:
            with contextlib.suppress(Exception):
                self._event_fh.close()
            self._event_fh = None

    # -- phases ------------------------------------------------------------
    def refresh(self) -> str:
        now = self.clock()
        if self.phase == LOBBY:
            if self.started_at is not None and now >= self.started_at:
                self.phase = TRAINING
        if self.phase == TRAINING and self.training_ends_at is not None and now >= self.training_ends_at:
            self.phase = FINAL
        if self.phase == TRAINING and self.teams and all(t.final_done for t in self.teams.values()) \
                and not any(t.busy for t in self.teams.values()):
            self.phase = FINISHED  # everyone finished early
        if self.phase == FINAL:
            window_closed = self.final_ends_at is not None and now >= self.final_ends_at
            everyone_done = bool(self.teams) and all(t.final_done for t in self.teams.values())
            nobody_running = not any(t.busy for t in self.teams.values())
            if window_closed or (everyone_done and nobody_running):
                self.phase = FINISHED
        return self.phase

    def start_training(self, at: Optional[float] = None) -> dict:
        """lobby → training now, or at the given unix timestamp."""
        now = self.clock()
        self.started_at = float(at) if at is not None else now
        self.training_ends_at = self.started_at + self.training_duration
        self.final_ends_at = self.training_ends_at + self.final_window_seconds
        if self.phase in (FINAL, FINISHED):
            self.phase = LOBBY
        self.refresh()
        self.log_event(None, "admin", {"action": "start_training", "at": self.started_at})
        return self.timings()

    def force_final(self) -> dict:
        now = self.clock()
        if self.started_at is None:
            self.started_at = now
        self.training_ends_at = now
        self.final_ends_at = now + self.final_window_seconds
        self.phase = TRAINING
        self.refresh()
        self.log_event(None, "admin", {"action": "force_final", "at": now})
        return self.timings()

    def timings(self) -> dict:
        return {
            "phase": self.phase,
            "server_time": self.clock(),
            "started_at": self.started_at,
            "training_ends_at": self.training_ends_at,
            "final_ends_at": self.final_ends_at,
        }

    # -- teams -------------------------------------------------------------
    def join(self, team_name: str, token: str) -> Team:
        self.refresh()
        if not isinstance(team_name, str) or not team_name.strip():
            raise GameError("bad_request", "team must be a non-empty string")
        name = team_name.strip()[:32]
        token = "" if token is None else str(token)
        team = self.teams.get(name)
        if team is None:
            if not conf(self.config, "open_registration"):
                raise GameError("unknown_team", f"team {name!r} is not registered")
            team = Team(name=name, token=token, created_at=self.clock())
            self.teams[name] = team
            self.log_event(name, "admin", {"action": "register", "team": name})
            return team
        if team.token != token:
            raise GameError("auth", "wrong token for this team")
        return team

    def get_team(self, name: str) -> Optional[Team]:
        return self.teams.get(name)

    def demo_available(self, team: Team) -> bool:
        return (not team.busy) and team.demos_used < self.max_demos

    def next_round_available_at(self, team: Team) -> Optional[float]:
        self.refresh()
        if team.rounds_used >= self.max_training_rounds:
            return None
        if team.last_round_started_at is None:
            return self.started_at if self.phase == LOBBY else self.clock()
        return team.last_round_started_at + self.cooldown_seconds

    # -- rounds ------------------------------------------------------------
    def start_round(self, team: Team, kind: str = TRAINING) -> Round:
        """Validate the SPEC §5 rules and hand back a Round the server can drive."""
        self.refresh()
        now = self.clock()
        if kind not in (TRAINING, FINAL):
            raise GameError("bad_request", f"unknown round kind {kind!r}")
        if team.busy:
            raise GameError("busy", "a round is already running for this team")

        if kind == TRAINING:
            if self.phase != TRAINING:
                raise GameError(
                    "phase",
                    f"training rounds are not available in phase {self.phase!r}",
                    retry_at=self.started_at if self.phase == LOBBY else None,
                )
            if self.training_ends_at is not None and now >= self.training_ends_at:
                raise GameError("phase", "training time is over")
            if team.rounds_used >= self.max_training_rounds:
                raise GameError("round_cap", f"all {self.max_training_rounds} training rounds used")
            if team.last_round_started_at is not None:
                ready_at = team.last_round_started_at + self.cooldown_seconds
                if now < ready_at:
                    raise GameError(
                        "cooldown",
                        f"{ready_at - now:.1f}s left on the cooldown",
                        retry_at=ready_at,
                    )
            duration = float(conf(self.config, "round_seconds"))
            seed = self._rng.getrandbits(32)
        else:
            early_ok = (
                self.phase == TRAINING
                and bool(conf(self.config, "allow_early_final"))
                and team.rounds_used >= self.max_training_rounds
            )
            if self.phase != FINAL and not early_ok:
                raise GameError(
                    "phase",
                    f"the final is not open in phase {self.phase!r}"
                    + (" (use all your training rounds to unlock it early)" if self.phase == TRAINING else ""),
                    retry_at=self.training_ends_at if self.phase in (LOBBY, TRAINING) else None,
                )
            if team.final_done:
                raise GameError("final_done", "this team has already run its final")
            if self.final_ends_at is not None and now >= self.final_ends_at:
                raise GameError("phase", "the final window has closed")
            duration = float(conf(self.config, "final_seconds"))
            if conf(self.config, "final_shared_sequence"):
                seed = self.final_seed
            else:
                seed = self._rng.getrandbits(32)

        if not list(self.pool.names):
            raise GameError("internal", "no challenges are loaded")

        rnd = Round(self, team, kind, seed, duration)
        team.current_round = rnd
        team.last_round_started_at = now
        if kind == TRAINING:
            team.rounds_used += 1
        self.round_counter += 1
        self.log_event(team.name, "round", {"event": "round_start", "round_id": rnd.round_id,
                                            "kind": kind, "seed": seed})
        return rnd

    def start_final(self, team: Team) -> Round:
        return self.start_round(team, FINAL)

    def _round_ended(self, rnd: Round) -> None:
        """Called by Round.finish(); updates team bookkeeping and the log."""
        team = rnd.team
        if team.current_round is rnd:
            team.current_round = None
        presented, answered, correct = rnd.counts()
        team.history.append(rnd.record())
        if rnd.kind == FINAL:
            team.final_done = True
            team.final_score = correct
            team.final_answered = answered
        self.log_event(team.name, "round", rnd.record())
        self.refresh()

    async def abort_round(self, team: Team, reason: str = "socket_replaced") -> None:
        rnd = team.current_round
        if rnd is not None:
            await rnd.abort(reason)

    # -- demo --------------------------------------------------------------
    async def demo(self, team: Team, name: str) -> dict:
        self.refresh()
        if self.phase != TRAINING:
            raise GameError("phase", f"demos are only available during training (phase={self.phase!r})")
        if team.busy:
            raise GameError("busy", "a round is running")
        if not self.demo_available(team):
            raise GameError("no_demo", f"all {self.max_demos} demo requests of this game are used")
        if name not in set(self.pool.names):
            raise GameError("unknown_challenge", f"no challenge named {name!r}")
        # A demo whose answer is the clue unchanged (an "n = 0" instance) teaches nothing, and a
        # team has only three of them: draw again, a few times, until the answer differs.
        lease = getattr(self.pool, "lease", None)
        for _attempt in range(DEMO_REDRAWS):
            seed = self._rng.getrandbits(32)
            if callable(lease):
                async with lease() as sb:
                    clue, solution, score = await self._demo_calls(sb, name, seed)
            else:
                clue, solution, score = await self._demo_calls(self.pool, name, seed)
            if _norm(solution) != _norm(clue):
                break
        team.demos_used += 1
        result = {"type": "demo_result", "name": name, "clue": clue,
                  "solution": solution, "score": score}
        self.log_event(team.name, "round", {"event": "demo", **result})
        return result

    async def _demo_calls(self, sb, name: str, seed: int):
        try:
            clue = await sb.generate(name, seed)
        except Exception as exc:
            raise GameError("internal", f"generate failed for {name}: {exc}")
        try:
            solution = await sb.solve(name, clue)
        except Exception as exc:
            raise GameError("internal", f"solve failed for {name}: {exc}")
        try:
            score = await sb.score(name, clue, solution)
        except Exception:
            score = 0
        return clue, solution, (1 if score == 1 else 0)

    # -- views -------------------------------------------------------------
    def leaderboard(self) -> list[dict]:
        """final_done first, then final_score desc, answered asc (precision wins ties), then name."""
        self.refresh()
        rows = [
            {
                "team": t.name,
                "final_score": t.final_score,
                "answered": t.final_answered,
                "rounds_used": t.rounds_used,
                "final_done": t.final_done,
            }
            for t in self.teams.values()
        ]
        rows.sort(key=lambda r: (not r["final_done"], -(r["final_score"] or 0), r["answered"], r["team"]))
        for i, row in enumerate(rows, 1):
            row["rank"] = i
        return rows

    def team_state(self, team: Team) -> dict:
        return {
            "team": team.name,
            "rounds_used": team.rounds_used,
            "next_round_available_at": self.next_round_available_at(team),
            "demo_available": self.demo_available(team),
            "demos_remaining": self.demos_remaining(team),
            "final_score": team.final_score,
            "final_done": team.final_done,
        }

    def client_config(self) -> dict:
        pub = getattr(self.config, "public_dict", None)
        if callable(pub):
            return pub(self.training_ends_at, self.final_ends_at)
        return {
            "round_seconds": float(conf(self.config, "round_seconds")),
            "final_seconds": float(conf(self.config, "final_seconds")),
            "cooldown_seconds": self.cooldown_seconds,
            "max_training_rounds": self.max_training_rounds,
            "max_demos": self.max_demos,
            "max_solution_chars": int(conf(self.config, "max_solution_chars")),
            "max_clue_chars": int(conf(self.config, "max_clue_chars")),
            "training_ends_at": self.training_ends_at,
            "final_ends_at": self.final_ends_at,
        }

    def welcome(self, team: Team) -> dict:
        self.refresh()
        return {
            "type": "welcome",
            "team": team.name,
            "phase": self.phase,
            "challenges": sorted(self.pool.names),
            "config": self.client_config(),
            "rounds_used": team.rounds_used,
            "next_round_available_at": self.next_round_available_at(team),
            "demo_available": self.demo_available(team),
            "demos_remaining": self.demos_remaining(team),
            "server_time": self.clock(),
        }

    def status(self, team: Optional[Team]) -> dict:
        self.refresh()
        msg = {
            "type": "status",
            "phase": self.phase,
            "server_time": self.clock(),
            "training_ends_at": self.training_ends_at,
            "final_ends_at": self.final_ends_at,
            "rounds_used": team.rounds_used if team else 0,
            "next_round_available_at": self.next_round_available_at(team) if team else None,
            "demo_available": self.demo_available(team) if team else False,
            "demos_remaining": self.demos_remaining(team) if team else None,
            "final_score": team.final_score if team else None,
            "leaderboard": self.leaderboard(),
        }
        return msg

    def public_state(self) -> dict:
        self.refresh()
        return {
            **self.timings(),
            "challenges": sorted(self.pool.names),
            "teams": len(self.teams),
            "leaderboard": self.leaderboard(),
        }

    def admin_state(self) -> dict:
        self.refresh()
        return {
            **self.timings(),
            "challenges": sorted(self.pool.names),
            "config": self.client_config(),
            "rounds_started": self.round_counter,
            "leaderboard": self.leaderboard(),
            "teams": [
                {
                    **self.team_state(t),
                    "token": t.token,
                    "created_at": t.created_at,
                    "last_round_started_at": t.last_round_started_at,
                    "busy": t.busy,
                    "final_answered": t.final_answered,
                    "history": t.history,
                }
                for t in self.teams.values()
            ],
        }


# ---------------------------------------------------------------------------
# Adapter: engine CompiledPool + SandboxPool -> the duck-typed pool above.
# ---------------------------------------------------------------------------
async def _acall(fn, *args):
    """Await ``fn`` whether it is a coroutine function or a blocking one."""
    if fn is None:
        raise RuntimeError("sandbox method is missing")
    if inspect.iscoroutinefunction(fn):
        return await fn(*args)
    result = fn(*args)
    if inspect.isawaitable(result):
        return await result
    return result


class _SandboxView:
    """Async facade over one (possibly blocking) Sandbox worker."""

    def __init__(self, sandbox, executor=None):
        self._sb = sandbox
        self._executor = executor

    async def _run(self, method: str, *args):
        fn = getattr(self._sb, method)
        if inspect.iscoroutinefunction(fn):
            return await fn(*args)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, fn, *args)

    async def generate(self, name: str, seed: int) -> str:
        return await self._run("generate", name, seed)

    async def score(self, name: str, clue: str, solution: str) -> int:
        try:
            return await self._run("score", name, clue, solution)
        except Exception as exc:
            log.warning("score(%s) failed: %s", name, exc)
            return 0

    async def solve(self, name: str, clue: str) -> str:
        return await self._run("solve", name, clue)


class SandboxPoolAdapter:
    """Wraps ``CompiledPool`` (names) + ``SandboxPool`` (workers) for the Game.

    ``lease()`` yields one worker for a whole round, so concurrent teams never
    share a sandbox process.
    """

    def __init__(self, compiled_pool: Any, sandbox_pool: Any, executor=None):
        self.compiled = compiled_pool
        self.sandbox_pool = sandbox_pool
        self.executor = executor

    @property
    def names(self) -> list[str]:
        names = getattr(self.compiled, "names", None)
        if names is None:
            return []
        if callable(names):
            names = names()
        return list(names)

    def lease(self):
        return _PoolLease(self.sandbox_pool, self.executor)

    async def generate(self, name: str, seed: int) -> str:
        async with self.lease() as sb:
            return await sb.generate(name, seed)

    async def score(self, name: str, clue: str, solution: str) -> int:
        async with self.lease() as sb:
            return await sb.score(name, clue, solution)

    async def solve(self, name: str, clue: str) -> str:
        async with self.lease() as sb:
            return await sb.solve(name, clue)


class _PoolLease:
    """`async with pool.lease() as sb:` over SandboxPool.acquire() (sync or async)."""

    def __init__(self, sandbox_pool, executor=None):
        self._pool = sandbox_pool
        self._executor = executor
        self._cm = None

    async def __aenter__(self):
        acquire = getattr(self._pool, "acquire", None)
        if acquire is None:
            return _SandboxView(self._pool, self._executor)
        cm = acquire()
        if hasattr(cm, "__aenter__"):
            self._cm = cm
            sb = await cm.__aenter__()
        elif hasattr(cm, "__enter__"):
            self._cm = cm
            sb = cm.__enter__()
        elif inspect.isawaitable(cm):
            sb = await cm
        else:
            sb = cm
        return _SandboxView(sb, self._executor)

    async def __aexit__(self, *exc):
        cm, self._cm = self._cm, None
        if cm is None:
            return False
        if hasattr(cm, "__aexit__"):
            return await cm.__aexit__(*exc)
        return cm.__exit__(*exc)
