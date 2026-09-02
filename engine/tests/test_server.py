"""Protocol tests for engine/server.py (SPEC §5/§6).

The aiohttp app is assembled directly around a Game backed by the same FakePool
the game tests use, so the whole protocol table can be exercised in ~2 seconds
without spawning sandbox processes.
"""
from __future__ import annotations

import asyncio
import json

import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from engine import server as srv
from engine.game import Game
from engine.tests.test_game import FakePool, make_config, solver


ROUND_S = 0.25


def build_app(**cfg) -> web.Application:
    values = dict(round_seconds=ROUND_S, final_seconds=ROUND_S, cooldown_seconds=0.0,
                  training_seconds=10_000, final_window_seconds=60, event_log="")
    values.update(cfg)
    config = make_config(**values)
    pool = FakePool()
    game = Game(config, pool)
    app = web.Application()
    app[srv.CONFIG] = config
    app[srv.GAME] = game
    app[srv.POOL] = pool
    app[srv.REPORTS] = {}
    app[srv.SANDBOX] = None
    app[srv.SANDBOX_POOL] = None
    app[srv.STORE] = None
    app[srv.CONNS] = {}
    srv.attach_routes(app)
    return app


@pytest_asyncio.fixture
async def client():
    app = build_app()
    c = TestClient(TestServer(app))
    await c.start_server()
    c.game = app[srv.GAME]
    try:
        yield c
    finally:
        await c.close()


async def recv(ws, timeout=5.0, skip_stale=True):
    """Receive one frame.

    A client that answers the very last challenge of a round races the deadline,
    so a trailing `error{code:"stale"}` after `round_over` is normal and every
    real client has to tolerate it; tests skip it unless they are looking for it.
    """
    while True:
        msg = await asyncio.wait_for(ws.receive_json(), timeout)
        if skip_stale and msg.get("type") == "error" and msg.get("code") == "stale":
            continue
        return msg


async def join(client, team="alpha", token="tok"):
    ws = await client.ws_connect("/ws")
    await ws.send_json({"type": "join", "team": team, "token": token})
    welcome = await recv(ws)
    return ws, welcome


async def play_round(ws, kind="start_round", answer=solver, skip_every=0):
    """Drive one round to round_over; returns (messages, round_over)."""
    await ws.send_json({"type": kind})
    msgs = []
    started = await recv(ws)
    msgs.append(started)
    assert started["type"] == "round_started"
    rid = started["round_id"]
    while True:
        msg = await recv(ws)
        msgs.append(msg)
        if msg["type"] == "round_over":
            return msgs, msg
        if msg["type"] == "challenge":
            i = msg["index"]
            if skip_every and i % skip_every == 0:
                await ws.send_json({"type": "skip", "round_id": rid, "index": i})
            else:
                class _It:  # solver() only needs .name/.clue/.index
                    name, clue, index = msg["name"], msg["clue"], i
                await ws.send_json({"type": "answer", "round_id": rid, "index": i,
                                    "solution": answer(_It)})


# ------------------------------------------------------------------ HTTP pages
@pytest.mark.asyncio
async def test_index_and_api_state(client):
    r = await client.get("/")
    assert r.status == 200 and "Centaur Zendo" in await r.text()
    r = await client.get("/api/state")
    body = await r.json()
    assert body["phase"] == "lobby" and body["challenges"] == ["ADD", "ECHO"]
    assert body["leaderboard"] == []


@pytest.mark.asyncio
async def test_admin_endpoints_are_open_without_a_token(client):
    r = await client.post("/admin/start")
    assert r.status == 200 and (await r.json())["phase"] == "training"
    r = await client.get("/admin/state")
    assert r.status == 200 and "teams" in await r.json()
    r = await client.get("/admin/reports")
    assert r.status == 200
    r = await client.post("/admin/force_final")
    assert (await r.json())["phase"] == "final"


@pytest.mark.asyncio
async def test_admin_token_is_enforced_when_set():
    app = build_app(admin_token="letmein")
    c = TestClient(TestServer(app))
    await c.start_server()
    try:
        assert (await c.post("/admin/start")).status == 401
        assert (await c.get("/admin/state", headers={"X-Admin-Token": "nope"})).status == 401
        r = await c.post("/admin/start", headers={"X-Admin-Token": "letmein"})
        assert r.status == 200
        assert app[srv.GAME].phase == "training"
    finally:
        await c.close()


@pytest.mark.asyncio
async def test_admin_start_accepts_a_timestamp(client):
    later = client.game.clock() + 3600
    r = await client.post("/admin/start", json={"at": later})
    body = await r.json()
    assert body["phase"] == "lobby" and body["started_at"] == pytest.approx(later)


# ------------------------------------------------------------------- handshake
@pytest.mark.asyncio
async def test_join_welcome_and_ping(client):
    ws, w = await join(client)
    assert w["type"] == "welcome" and w["team"] == "alpha" and w["phase"] == "lobby"
    assert w["challenges"] == ["ADD", "ECHO"]
    assert set(w["config"]) >= {"round_seconds", "final_seconds", "cooldown_seconds",
                                "max_training_rounds", "max_solution_chars",
                                "max_clue_chars", "training_ends_at", "final_ends_at"}
    assert w["rounds_used"] == 0 and w["demo_available"] is True and w["server_time"] > 0
    await ws.send_json({"type": "ping"})
    assert (await recv(ws))["type"] == "pong"
    await ws.close()


@pytest.mark.asyncio
async def test_errors_before_join_and_on_bad_frames(client):
    ws = await client.ws_connect("/ws")
    await ws.send_json({"type": "start_round"})
    assert (await recv(ws))["code"] == "not_joined"
    await ws.send_str("this is not json")
    assert (await recv(ws))["code"] == "bad_message"
    await ws.send_json({"type": "join", "team": "a", "token": "t"})
    await recv(ws)
    await ws.send_json({"type": "wat"})
    assert (await recv(ws))["code"] == "unknown_type"
    await ws.close()


@pytest.mark.asyncio
async def test_wrong_token_is_rejected(client):
    ws, _ = await join(client, "alpha", "right")
    ws2 = await client.ws_connect("/ws")
    await ws2.send_json({"type": "join", "team": "alpha", "token": "wrong"})
    err = await recv(ws2)
    assert err["type"] == "error" and err["code"] == "auth"
    await ws.close()
    await ws2.close()


@pytest.mark.asyncio
async def test_second_join_replaces_the_socket(client):
    await client.post("/admin/start")
    ws1, _ = await join(client)
    ws2, w2 = await join(client)
    assert w2["type"] == "welcome"
    err = await recv(ws1)
    assert err["code"] == "replaced"
    assert (await ws1.receive()).type.name in ("CLOSE", "CLOSED", "CLOSING")
    await ws2.close()


@pytest.mark.asyncio
async def test_join_during_a_round_aborts_it(client):
    await client.post("/admin/start")
    ws1, _ = await join(client)
    await ws1.send_json({"type": "start_round"})
    assert (await recv(ws1))["type"] == "round_started"
    await recv(ws1)                                   # first challenge, left unanswered
    ws2, _ = await join(client)                       # takes over
    team = client.game.teams["alpha"]
    assert team.current_round is None                 # in-flight round was aborted
    assert team.history[-1]["aborted"] is True
    await ws2.close()


# ----------------------------------------------------------------- round loop
@pytest.mark.asyncio
async def test_full_training_round(client):
    await client.post("/admin/start")
    ws, _ = await join(client)
    msgs, over = await play_round(ws)

    rid = msgs[0]["round_id"]
    assert msgs[0]["duration_ms"] == int(ROUND_S * 1000)
    assert msgs[0]["deadline"] == pytest.approx(msgs[0]["started_at"] + ROUND_S)
    assert all(m.get("round_id") == rid for m in msgs)

    # result(i) is always sent before challenge(i+1), and every result matches
    # the challenge that preceded it.
    seq = [(m["type"], m["index"]) for m in msgs if m["type"] in ("challenge", "result")]
    for a, b in zip(seq, seq[1:]):
        if a[0] == "challenge":
            assert b == ("result", a[1])
        else:
            assert b == ("challenge", a[1] + 1)

    assert over["type"] == "round_over"
    assert over["presented"] == over["answered"] == over["correct"] > 3
    assert over["presented"] == len(over["items"])
    assert over["rounds_used"] == 1 and over["demo_available"] is True
    assert over["next_round_available_at"] is not None
    assert all(set(i) == {"index", "name", "clue", "solution", "score"} for i in over["items"])


@pytest.mark.asyncio
async def test_wrong_answers_and_skips(client):
    await client.post("/admin/start")
    ws, _ = await join(client)
    _msgs, over = await play_round(ws, answer=lambda i: "nonsense", skip_every=2)
    assert over["correct"] == 0
    assert over["answered"] < over["presented"]       # the skipped items
    assert any(i["solution"] is None for i in over["items"])


@pytest.mark.asyncio
async def test_stale_answers_are_rejected(client):
    await client.post("/admin/start")
    ws, _ = await join(client)
    await ws.send_json({"type": "start_round"})
    started = await recv(ws)
    ch = await recv(ws)
    rid = started["round_id"]

    await ws.send_json({"type": "answer", "round_id": rid, "index": 99, "solution": "x"})
    await ws.send_json({"type": "answer", "round_id": "nope", "index": 0, "solution": "x"})
    errs = [await recv(ws, skip_stale=False), await recv(ws, skip_stale=False)]
    assert [e["code"] for e in errs] == ["stale", "stale"]

    await ws.send_json({"type": "answer", "round_id": rid, "index": ch["index"],
                        "solution": solver(type("I", (), ch))})
    assert (await recv(ws))["type"] == "result"
    # answering the same index twice is stale as well
    await ws.send_json({"type": "answer", "round_id": rid, "index": ch["index"], "solution": "x"})
    while True:
        m = await recv(ws, skip_stale=False)
        if m["type"] == "error":
            assert m["code"] == "stale"
            break
        if m["type"] == "round_over":
            pytest.fail("expected a stale error")


@pytest.mark.asyncio
async def test_late_answers_are_ignored(client):
    await client.post("/admin/start")
    ws, _ = await join(client)
    await ws.send_json({"type": "start_round"})
    started = await recv(ws)
    ch = await recv(ws)
    await asyncio.sleep(ROUND_S + 0.05)               # let the round time out
    over = None
    while over is None:
        m = await recv(ws)
        if m["type"] == "round_over":
            over = m
    assert over["presented"] == 0                     # nothing was ever answered
    await ws.send_json({"type": "answer", "round_id": started["round_id"],
                        "index": ch["index"], "solution": "late"})
    assert (await recv(ws, skip_stale=False))["code"] == "stale"


@pytest.mark.asyncio
async def test_cooldown_and_phase_errors(client):
    app = build_app(cooldown_seconds=300)
    c = TestClient(TestServer(app))
    await c.start_server()
    try:
        ws, _ = await join(c)
        await ws.send_json({"type": "start_round"})   # still in the lobby
        err = await recv(ws)
        assert err["type"] == "error" and err["code"] == "phase"

        await c.post("/admin/start")
        _msgs, over = await play_round(ws)
        await ws.send_json({"type": "start_round"})
        err = await recv(ws)
        assert err["code"] == "cooldown" and err["retry_at"] > 0
        assert err["retry_at"] == pytest.approx(over["next_round_available_at"])
    finally:
        await c.close()


@pytest.mark.asyncio
async def test_round_cap(client):
    app = build_app(cooldown_seconds=0.0, max_training_rounds=2)
    c = TestClient(TestServer(app))
    await c.start_server()
    try:
        await c.post("/admin/start")
        ws, _ = await join(c)
        for _ in range(2):
            await play_round(ws)
        await ws.send_json({"type": "start_round"})
        err = await recv(ws)
        assert err["code"] == "round_cap"
    finally:
        await c.close()


# ---------------------------------------------------------------- demo + final
@pytest.mark.asyncio
async def test_demo(client):
    await client.post("/admin/start")
    ws, _ = await join(client)
    await ws.send_json({"type": "demo", "name": "ADD"})
    d = await recv(ws)
    assert d["type"] == "demo_result" and d["name"] == "ADD" and d["score"] == 1
    assert "+" in d["clue"] and d["solution"]

    await ws.send_json({"type": "demo", "name": "ADD"})
    assert (await recv(ws))["code"] == "no_demo"

    await play_round(ws)                              # a finished round refreshes it
    await ws.send_json({"type": "demo", "name": "ECHO"})
    assert (await recv(ws))["type"] == "demo_result"

    await ws.send_json({"type": "demo", "name": "NOPE"})
    assert (await recv(ws))["code"] in ("no_demo", "unknown_challenge")


@pytest.mark.asyncio
async def test_final_and_status_and_leaderboard(client):
    await client.post("/admin/start")
    ws_a, _ = await join(client, "alpha", "t")
    ws_b, _ = await join(client, "beta", "t")

    await ws_a.send_json({"type": "start_final"})
    assert (await recv(ws_a))["code"] == "phase"      # the final is not open yet

    await client.post("/admin/force_final")
    _msgs, over_a = await play_round(ws_a, kind="start_final")
    assert over_a["kind"] == "final" and over_a["correct"] > 0
    _msgs, over_b = await play_round(ws_b, kind="start_final",
                                     answer=lambda i: "junk")
    assert over_b["correct"] == 0

    # both teams saw the same shared (name, clue) sequence
    n = min(len(over_a["items"]), len(over_b["items"]))
    assert [(i["name"], i["clue"]) for i in over_a["items"]][:n] == \
           [(i["name"], i["clue"]) for i in over_b["items"]][:n]

    await ws_a.send_json({"type": "start_final"})
    assert (await recv(ws_a))["code"] in ("final_done", "phase")

    await ws_a.send_json({"type": "status"})
    st = await recv(ws_a)
    assert st["type"] == "status" and st["final_score"] == over_a["correct"]
    assert [r["team"] for r in st["leaderboard"]] == ["alpha", "beta"]
    assert st["phase"] in ("final", "finished")

    r = await client.get("/api/state")
    assert (await r.json())["leaderboard"][0]["team"] == "alpha"
    await ws_a.close()
    await ws_b.close()
