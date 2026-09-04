"""Unit tests for engine/game.py (SPEC §5).

Everything runs against a tiny in-test FakePool (no sandbox, no network) and a
fake clock, so cooldowns / training limits / deadlines are exact.
"""
from __future__ import annotations

import asyncio
import json
import random

import pytest

from engine.game import FINAL, FINISHED, LOBBY, TRAINING, Game, GameError, Round

try:  # the real config; a tiny stand-in keeps these tests runnable on their own
    from engine.config import GameConfig
except Exception:  # pragma: no cover
    GameConfig = None


DEFAULTS = dict(
    round_seconds=1.0,
    final_seconds=3.0,
    cooldown_seconds=300.0,
    max_training_rounds=12,
    training_seconds=None,
    final_window_seconds=600.0,
    max_demos=3,
    open_registration=True,
    event_log="",
    final_shared_sequence=True,
    final_seed=4242,
    max_solution_chars=4096,
    max_clue_chars=1024,
)


class _FallbackConfig:
    """Minimal local GameConfig stand-in (used only if engine.config is absent)."""

    def __init__(self, **kw):
        for k, v in {**DEFAULTS, **kw}.items():
            setattr(self, k, v)
        if self.training_seconds is None:
            self.training_seconds = self.max_training_rounds * self.cooldown_seconds + 60.0


def make_config(**kw):
    values = {**DEFAULTS, **kw}
    if GameConfig is not None:
        try:
            return GameConfig(**values)
        except TypeError:  # pragma: no cover - interface drift
            pass
    return _FallbackConfig(**values)


class Clock:
    def __init__(self, t: float = 1_000_000.0):
        self.t = float(t)

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += float(dt)


class FakePool:
    """Two challenges: ADD ("a+b" -> the sum) and ECHO (clue -> the clue)."""

    def __init__(self, names=("ADD", "ECHO")):
        self.names = list(names)
        self.generate_calls = 0
        self.score_calls = 0
        self.solve_calls = 0
        self.generated: list[tuple[str, int]] = []

    async def generate(self, name: str, seed: int) -> str:
        self.generate_calls += 1
        self.generated.append((name, seed))
        r = random.Random(seed)
        if name == "ADD":
            return f"{r.randrange(1, 50)}+{r.randrange(1, 50)}"
        return "".join(r.choice("abcdefgh") for _ in range(5))

    async def score(self, name: str, clue: str, solution: str) -> int:
        self.score_calls += 1
        if not solution:
            return 0
        if name == "ADD":
            a, b = clue.split("+")
            return 1 if solution.strip() == str(int(a) + int(b)) else 0
        return 1 if solution == clue else 0

    async def solve(self, name: str, clue: str) -> str:
        self.solve_calls += 1
        if name == "ADD":
            a, b = clue.split("+")
            return str(int(a) + int(b))
        return clue


class LeasingPool(FakePool):
    """FakePool that hands out a lease, like SandboxPool.acquire()."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.leases_open = 0
        self.leases_max = 0
        self.leases_total = 0

    def lease(self):
        pool = self

        class _L:
            async def __aenter__(self):
                pool.leases_open += 1
                pool.leases_total += 1
                pool.leases_max = max(pool.leases_max, pool.leases_open)
                return pool

            async def __aexit__(self, *exc):
                pool.leases_open -= 1
                return False

        return _L()


def solver(item):
    """A perfect answer for a FakePool item."""
    if item.name == "ADD":
        a, b = item.clue.split("+")
        return str(int(a) + int(b))
    return item.clue


def make_game(clock=None, pool=None, **cfg):
    clock = clock or Clock()
    pool = pool if pool is not None else FakePool()
    game = Game(make_config(**cfg), pool, clock=clock)
    return game, pool, clock


async def drive(game, team, kind=TRAINING, answer=solver, per_item=0.25, clock=None,
                max_items=100):
    """Run a whole round the way the server does, advancing a fake clock per item."""
    clock = clock or game.clock
    rnd = game.start_round(team, kind)
    await rnd.open()
    order = []
    while len(order) < max_items:
        item = await rnd.next_challenge()
        if item is None:
            break
        order.append(("challenge", item.index))
        clock.advance(per_item)
        if rnd.expired():  # the server's "waited until the deadline" branch
            break
        sol = answer(item)
        score = await rnd.submit(item.index, sol)
        order.append(("result", item.index, score))
        if rnd.expired():
            break
    summary = await rnd.finish()
    return rnd, summary, order


# --------------------------------------------------------------------------- join
def test_join_creates_team_and_checks_token():
    game, _pool, _clock = make_game()
    t = game.join("alpha", "s3cret")
    assert t.name == "alpha" and t.rounds_used == 0
    assert game.join("alpha", "s3cret") is t
    with pytest.raises(GameError) as e:
        game.join("alpha", "wrong")
    assert e.value.code == "auth"


def test_join_closed_registration():
    game, _pool, _clock = make_game(open_registration=False)
    with pytest.raises(GameError) as e:
        game.join("ghost", "x")
    assert e.value.code == "unknown_team"


def test_welcome_message_shape():
    game, _pool, _clock = make_game()
    team = game.join("alpha", "t")
    w = game.welcome(team)
    assert w["type"] == "welcome" and w["team"] == "alpha" and w["phase"] == LOBBY
    assert w["challenges"] == ["ADD", "ECHO"]
    for key in ("round_seconds", "final_seconds", "cooldown_seconds", "max_training_rounds",
                "max_solution_chars", "max_clue_chars", "training_ends_at", "final_ends_at"):
        assert key in w["config"]
    assert w["demo_available"] is True and w["rounds_used"] == 0


# -------------------------------------------------------------------------- phases
def test_phase_transitions_follow_the_clock():
    game, _pool, clock = make_game(cooldown_seconds=10, max_training_rounds=3,
                                   training_seconds=100, final_window_seconds=20)
    assert game.refresh() == LOBBY
    game.start_training()
    assert game.refresh() == TRAINING
    assert game.training_ends_at == clock.t + 100
    clock.advance(100)
    assert game.refresh() == FINAL
    clock.advance(20)
    assert game.refresh() == FINISHED


def test_start_training_in_the_future_stays_in_lobby():
    game, _pool, clock = make_game()
    game.start_training(at=clock.t + 50)
    assert game.refresh() == LOBBY
    clock.advance(50)
    assert game.refresh() == TRAINING


def test_default_training_seconds_is_rounds_times_cooldown_plus_60():
    game, _pool, clock = make_game(cooldown_seconds=300, max_training_rounds=12,
                                   training_seconds=None)
    game.start_training()
    assert game.training_ends_at == pytest.approx(clock.t + 12 * 300 + 60)


def test_force_final():
    game, _pool, clock = make_game(final_window_seconds=30)
    game.start_training()
    game.force_final()
    assert game.refresh() == FINAL
    assert game.final_ends_at == pytest.approx(clock.t + 30)


def test_round_refused_outside_training():
    game, _pool, _clock = make_game()
    team = game.join("a", "t")
    with pytest.raises(GameError) as e:
        game.start_round(team, TRAINING)
    assert e.value.code == "phase"


# -------------------------------------------------------------------------- rounds
@pytest.mark.asyncio
async def test_round_loop_orders_result_before_next_challenge():
    game, pool, clock = make_game()
    game.start_training()
    team = game.join("a", "t")
    rnd, summary, order = await drive(game, team, per_item=0.25, clock=clock)
    # 1.0s round, 0.25s per item => 3 answered, the 4th times out
    assert summary["presented"] == 3
    assert summary["answered"] == 3
    assert summary["correct"] == 3
    assert order == [("challenge", 0), ("result", 0, 1),
                     ("challenge", 1), ("result", 1, 1),
                     ("challenge", 2), ("result", 2, 1),
                     ("challenge", 3)]
    assert [i["index"] for i in summary["items"]] == [0, 1, 2]
    assert summary["round_id"] == rnd.round_id and summary["kind"] == TRAINING
    assert team.history[-1]["correct"] == 3


@pytest.mark.asyncio
async def test_wrong_answers_score_zero_and_skip_does_not_call_score():
    game, pool, clock = make_game()
    game.start_training()
    team = game.join("a", "t")
    rnd = game.start_round(team, TRAINING)
    await rnd.open()

    item = await rnd.next_challenge()
    assert await rnd.submit(item.index, "definitely-wrong") == 0
    calls_after_wrong = pool.score_calls
    assert calls_after_wrong == 1

    item = await rnd.next_challenge()
    assert await rnd.submit(item.index, None) == 0        # skip
    assert pool.score_calls == calls_after_wrong          # score() was NOT called

    summary = await rnd.finish()
    assert summary["presented"] == 2 and summary["answered"] == 1 and summary["correct"] == 0
    assert summary["items"][1]["solution"] is None


@pytest.mark.asyncio
async def test_stale_and_late_answers():
    game, _pool, clock = make_game()
    game.start_training()
    team = game.join("a", "t")
    rnd = game.start_round(team, TRAINING)
    await rnd.open()
    item = await rnd.next_challenge()

    with pytest.raises(GameError) as e:
        await rnd.submit(item.index + 5, "x")
    assert e.value.code == "stale"

    assert await rnd.submit(item.index, "x") == 0
    with pytest.raises(GameError) as e:      # answering the same index twice
        await rnd.submit(item.index, "x")
    assert e.value.code == "stale"

    item = await rnd.next_challenge()
    clock.advance(5.0)                        # past the deadline
    with pytest.raises(GameError) as e:
        await rnd.submit(item.index, "x")
    assert e.value.code == "stale"

    summary = await rnd.finish()
    assert summary["presented"] == 1          # the timed-out item is not counted


@pytest.mark.asyncio
async def test_deadline_is_strict():
    game, _pool, clock = make_game()
    game.start_training()
    team = game.join("a", "t")
    rnd = game.start_round(team, TRAINING)
    await rnd.open()
    item = await rnd.next_challenge()
    clock.advance(1.0)                        # exactly at the deadline
    assert rnd.expired()
    with pytest.raises(GameError):
        await rnd.submit(item.index, solver(item))
    assert await rnd.next_challenge() is None
    await rnd.finish()


@pytest.mark.asyncio
async def test_next_challenge_refuses_to_run_ahead_of_a_result():
    game, _pool, _clock = make_game()
    game.start_training()
    team = game.join("a", "t")
    rnd = game.start_round(team, TRAINING)
    await rnd.open()
    await rnd.next_challenge()
    with pytest.raises(RuntimeError):
        await rnd.next_challenge()
    await rnd.finish()


@pytest.mark.asyncio
async def test_busy_and_abort():
    game, _pool, _clock = make_game()
    game.start_training()
    team = game.join("a", "t")
    rnd = game.start_round(team, TRAINING)
    await rnd.open()
    with pytest.raises(GameError) as e:
        game.start_round(team, TRAINING)
    assert e.value.code == "busy"
    await game.abort_round(team)
    assert team.current_round is None
    assert team.history[-1]["aborted"] is True
    assert team.rounds_used == 1              # an aborted round still counts


@pytest.mark.asyncio
async def test_one_lease_per_round():
    clock = Clock()
    pool = LeasingPool()
    game, _p, _c = make_game(clock=clock, pool=pool)
    game.start_training()
    team = game.join("a", "t")
    await drive(game, team, clock=clock)
    assert pool.leases_total == 1            # exactly one worker for the whole round
    assert pool.leases_open == 0             # released at the end
    assert pool.leases_max == 1


# ------------------------------------------------------------------ cooldown/caps
@pytest.mark.asyncio
async def test_cooldown_is_measured_start_to_start():
    clock = Clock()
    game, _pool, _c = make_game(clock=clock, cooldown_seconds=60, training_seconds=10_000)
    game.start_training()
    team = game.join("a", "t")
    start = clock.t
    await drive(game, team, clock=clock)
    with pytest.raises(GameError) as e:
        game.start_round(team, TRAINING)
    assert e.value.code == "cooldown"
    assert e.value.retry_at == pytest.approx(start + 60)
    assert game.next_round_available_at(team) == pytest.approx(start + 60)
    clock.t = start + 59.9
    with pytest.raises(GameError):
        game.start_round(team, TRAINING)
    clock.t = start + 60
    rnd = game.start_round(team, TRAINING)    # exactly on the boundary is allowed
    await rnd.open()
    await rnd.finish()


@pytest.mark.asyncio
async def test_round_cap():
    clock = Clock()
    game, _pool, _c = make_game(clock=clock, cooldown_seconds=10, max_training_rounds=3,
                                training_seconds=10_000)
    game.start_training()
    team = game.join("a", "t")
    for _ in range(3):
        await drive(game, team, clock=clock)
        clock.advance(10)
    assert team.rounds_used == 3
    with pytest.raises(GameError) as e:
        game.start_round(team, TRAINING)
    assert e.value.code == "round_cap"
    assert game.next_round_available_at(team) is None


@pytest.mark.asyncio
async def test_training_time_limit():
    clock = Clock()
    game, _pool, _c = make_game(clock=clock, cooldown_seconds=5, max_training_rounds=10,
                                training_seconds=30)
    game.start_training()
    team = game.join("a", "t")
    await drive(game, team, clock=clock)
    clock.advance(40)                         # training window has closed
    with pytest.raises(GameError) as e:
        game.start_round(team, TRAINING)
    assert e.value.code == "phase"
    assert game.phase == FINAL


# ----------------------------------------------------------------------- demo
@pytest.mark.asyncio
async def test_demo_budget_is_per_game():
    """SPEC §5: a team has max_demos demo requests for the whole game, usable at any time
    during training when no round is running; rounds neither consume nor grant them."""
    clock = Clock()
    game, pool, _c = make_game(clock=clock, cooldown_seconds=10, training_seconds=10_000, max_demos=3)
    game.start_training()
    team = game.join("a", "t")
    assert game.demo_available(team) is True and game.demos_remaining(team) == 3

    res = await game.demo(team, "ADD")
    assert res["type"] == "demo_result" and res["name"] == "ADD" and res["score"] == 1
    assert res["solution"] and res["clue"]
    assert game.demos_remaining(team) == 2

    await drive(game, team, clock=clock)       # a round does not change the budget
    assert game.demos_remaining(team) == 2 and game.demo_available(team) is True

    await game.demo(team, "ECHO")
    await game.demo(team, "ADD")
    assert game.demos_remaining(team) == 0 and game.demo_available(team) is False
    with pytest.raises(GameError) as e:
        await game.demo(team, "ADD")
    assert e.value.code == "no_demo"

    clock.advance(10)
    await drive(game, team, clock=clock)       # still none after another round
    assert game.demo_available(team) is False

    with pytest.raises(GameError) as e:
        await game.demo(game.join("b", "t2"), "NOPE")
    assert e.value.code == "unknown_challenge"


@pytest.mark.asyncio
async def test_demo_refused_while_a_round_is_running():
    clock = Clock()
    game, _pool, _c = make_game(clock=clock, training_seconds=10_000)
    game.start_training()
    team = game.join("a", "t")
    rnd = game.start_round(team, TRAINING)
    await rnd.open()
    assert game.demo_available(team) is False
    with pytest.raises(GameError) as e:
        await game.demo(team, "ADD")
    assert e.value.code == "busy"
    await rnd.finish()
    assert game.demo_available(team) is True and game.demos_remaining(team) == 3


def test_pool_size_draws_a_fixed_subset():
    """SPEC §5: a game plays pool_size classes drawn once with pool_seed."""
    class BigPool(FakePool):
        pass
    big = BigPool()
    big.names = [f"C{i}" for i in range(20)]
    g1 = Game(make_config(pool_size=7, pool_seed=5), big, clock=Clock())
    g2 = Game(make_config(pool_size=7, pool_seed=5), big, clock=Clock())
    g3 = Game(make_config(pool_size=7, pool_seed=6), big, clock=Clock())
    assert len(g1.pool.names) == 7 and g1.pool.names == g2.pool.names
    assert set(g1.pool.names) <= set(big.names) and g3.pool.names != g1.pool.names
    g_all = Game(make_config(pool_size=None), big, clock=Clock())
    assert len(g_all.pool.names) == 20


@pytest.mark.asyncio
async def test_demo_refused_outside_training():
    game, _pool, _clock = make_game()
    team = game.join("a", "t")
    with pytest.raises(GameError) as e:
        await game.demo(team, "ADD")
    assert e.value.code == "phase"


# ----------------------------------------------------------------------- final
@pytest.mark.asyncio
async def test_final_is_a_shared_sequence_and_scores():
    clock = Clock()
    pool = FakePool()
    game, _p, _c = make_game(clock=clock, pool=pool, final_seconds=2.0,
                             training_seconds=10, final_window_seconds=100)
    game.start_training()
    a = game.join("a", "t")
    b = game.join("b", "t")
    game.join("c", "t")          # registered but never runs: keeps the phase open
    clock.advance(11)
    assert game.refresh() == FINAL

    t0 = clock.t
    _r, sa, _o = await drive(game, a, FINAL, per_item=0.5, clock=clock)
    clock.t = t0
    _r, sb, _o = await drive(game, b, FINAL, answer=lambda i: "junk", per_item=0.5, clock=clock)

    seq_a = [(i["name"], i["clue"]) for i in sa["items"]]
    seq_b = [(i["name"], i["clue"]) for i in sb["items"]]
    assert seq_a == seq_b and len(seq_a) == 3        # 2.0s / 0.5s
    assert a.final_score == 3 and b.final_score == 0
    assert a.final_done and b.final_done

    assert game.refresh() == FINAL
    with pytest.raises(GameError) as e:
        game.start_round(a, FINAL)
    assert e.value.code == "final_done"
    clock.advance(200)           # the window closes with c still missing
    assert game.refresh() == FINISHED


@pytest.mark.asyncio
async def test_final_refused_before_and_after_its_window():
    clock = Clock()
    game, _pool, _c = make_game(clock=clock, training_seconds=10, final_window_seconds=5)
    game.start_training()
    team = game.join("a", "t")
    with pytest.raises(GameError) as e:
        game.start_final(team)
    assert e.value.code == "phase"
    clock.advance(20)                              # window already closed
    with pytest.raises(GameError) as e:
        game.start_final(team)
    assert e.value.code == "phase"
    assert game.refresh() == FINISHED


@pytest.mark.asyncio
async def test_leaderboard_ordering_and_tiebreak():
    clock = Clock()
    game, _pool, _c = make_game(clock=clock, final_seconds=3.0, training_seconds=10,
                                final_window_seconds=100)
    game.start_training()
    teams = [game.join(n, "t") for n in ("carol", "alice", "bob", "dan")]
    clock.advance(11)

    # alice: 4 right out of 4 answered.  bob: 4 right out of 5 answered.
    # carol: 0.  dan: 0 but never runs a final.
    t0 = clock.t
    await drive(game, teams[1], FINAL, per_item=0.7, clock=clock)
    clock.t = t0
    await drive(game, teams[2], FINAL, per_item=0.5, clock=clock,
                answer=lambda i: solver(i) if i.index < 4 else "junk")
    clock.t = t0
    await drive(game, teams[0], FINAL, answer=lambda i: "x", per_item=1.0, clock=clock)

    lb = game.leaderboard()
    assert (lb[0]["final_score"], lb[0]["answered"]) == (4, 4)
    assert (lb[1]["final_score"], lb[1]["answered"]) == (4, 5)
    assert [r["team"] for r in lb][:2] == ["alice", "bob"]  # equal score, fewer answers wins
    assert lb[0]["final_score"] == lb[1]["final_score"]
    assert lb[0]["answered"] < lb[1]["answered"]
    # both on 0, but a team that actually ran its final (carol) always ranks above
    # a no-show (dan), regardless of the fewer-answers tiebreak.
    assert [r["team"] for r in lb][2:] == ["carol", "dan"]
    assert [r["rank"] for r in lb] == [1, 2, 3, 4]


# ----------------------------------------------------------------- state + log
@pytest.mark.asyncio
async def test_event_log_is_jsonl(tmp_path):
    clock = Clock()
    path = tmp_path / "events.jsonl"
    pool = FakePool()
    game = Game(make_config(training_seconds=10_000), pool, clock=clock, event_log=str(path))
    game.start_training()
    team = game.join("a", "t")
    game.log_event("a", "in", {"type": "start_round"})
    await drive(game, team, clock=clock)
    game.close()

    lines = [json.loads(l) for l in path.read_text().splitlines()]
    assert lines and all({"ts", "team", "dir", "msg"} <= set(l) for l in lines)
    assert any(l["dir"] == "in" and l["msg"]["type"] == "start_round" for l in lines)
    rounds = [l for l in lines if l["dir"] == "round" and l["msg"].get("round_id")]
    assert any("items" in l["msg"] for l in rounds)


@pytest.mark.asyncio
async def test_public_and_admin_state():
    clock = Clock()
    game, _pool, _c = make_game(clock=clock, training_seconds=10_000)
    game.start_training()
    team = game.join("a", "secret")
    await drive(game, team, clock=clock)

    pub = game.public_state()
    assert pub["phase"] == TRAINING and pub["challenges"] == ["ADD", "ECHO"] and pub["teams"] == 1
    assert "secret" not in json.dumps(pub)

    adm = game.admin_state()
    assert adm["teams"][0]["token"] == "secret"
    assert adm["teams"][0]["rounds_used"] == 1
    assert adm["teams"][0]["history"]
    json.dumps(adm)  # must be serialisable

    st = game.status(team)
    assert st["type"] == "status" and st["phase"] == TRAINING
    assert st["leaderboard"] and st["demo_available"] is True


@pytest.mark.asyncio
async def test_generate_failures_are_retried():
    class FlakyPool(FakePool):
        def __init__(self):
            super().__init__()
            self.fails = 2

        async def generate(self, name, seed):
            if self.fails > 0:
                self.fails -= 1
                raise RuntimeError("sandbox died")
            return await super().generate(name, seed)

    clock = Clock()
    pool = FlakyPool()
    game, _p, _c = make_game(clock=clock, pool=pool, training_seconds=10_000)
    game.start_training()
    team = game.join("a", "t")
    rnd = game.start_round(team, TRAINING)
    await rnd.open()
    item = await rnd.next_challenge()
    assert item is not None and pool.fails == 0
    await rnd.submit(item.index, solver(item))
    await rnd.finish()


# --------------------------------------------------------------------------- early final

@pytest.mark.asyncio
async def test_early_final_unlocks_after_all_training_rounds():
    game, pool, clock = make_game(max_training_rounds=2, cooldown_seconds=1, training_seconds=10_000)
    game.start_training()
    t = game.join("early", "tok")
    with pytest.raises(GameError) as e:
        game.start_round(t, FINAL)
    assert e.value.code == "phase"
    for _ in range(2):
        await drive(game, t, TRAINING, per_item=0.5, clock=clock)
        clock.advance(2)
    assert game.phase == TRAINING
    rnd, summary, _ = await drive(game, t, FINAL, per_item=0.5, clock=clock)
    assert t.final_done and t.final_score == summary["correct"]
    assert game.refresh() == FINISHED  # every registered team finished early


@pytest.mark.asyncio
async def test_early_final_can_be_disabled():
    game, pool, clock = make_game(max_training_rounds=1, cooldown_seconds=1, training_seconds=10_000,
                                  allow_early_final=False)
    game.start_training()
    t = game.join("late", "tok")
    await drive(game, t, TRAINING, per_item=0.5, clock=clock)
    with pytest.raises(GameError) as e:
        game.start_round(t, FINAL)
    assert e.value.code == "phase"
