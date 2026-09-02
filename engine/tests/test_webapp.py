"""Tests for the challenge-submission web app (webapp/app.py, SPEC §8).

Everything runs against the real engine objects (GameConfig, ChallengeStore,
InProcessSandbox, validate) through an aiohttp test client, so a change to the
validator or the store shows up here.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import pytest_asyncio
from aiohttp.test_utils import TestClient, TestServer

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.challenges import ChallengeStore, validate  # noqa: E402
from engine.config import GameConfig  # noqa: E402
from engine.sandbox import InProcessSandbox  # noqa: E402
from webapp.app import make_subapp  # noqa: E402

ADMIN_TOKEN = "open-sesame"
PP = json.loads((ROOT / "challenges" / "PP.json").read_text())


def doc(**over):
    d = dict(PP)
    d.update(over)
    return d


@pytest.fixture
def challenge_dir(tmp_path):
    d = tmp_path / "challenges"
    d.mkdir()
    (d / "PP.json").write_text(json.dumps(PP, indent=1))
    return d


@pytest.fixture
def config(challenge_dir):
    # 4 seeds instead of 20: same code paths, much faster tests.
    return GameConfig(
        challenge_dir=str(challenge_dir),
        admin_token=ADMIN_TOKEN,
        validation_seeds=4,
    )


@pytest_asyncio.fixture
async def client(config, challenge_dir):
    sandbox = InProcessSandbox(config)
    app = make_subapp(ChallengeStore(challenge_dir), config, sandbox, validate=validate)
    c = TestClient(TestServer(app))
    await c.start_server()
    try:
        yield c
    finally:
        await c.close()
        sandbox.close()


# --------------------------------------------------------------------- page
@pytest.mark.asyncio
async def test_index_page_serves(client):
    r = await client.get("/")
    assert r.status == 200
    assert "text/html" in r.headers["Content-Type"]
    body = await r.text()
    assert "Organisers only" in body
    assert "generate(seed)" in body


# ------------------------------------------------------------------- config
@pytest.mark.asyncio
async def test_config_endpoint_reports_caps(client, config):
    r = await client.get("/api/config")
    assert r.status == 200
    j = await r.json()
    assert j["validation_seeds"] == 4
    assert j["caps"]["max_score_code_chars"] == config.max_score_code_chars
    assert j["caps"]["max_generate_code_chars"] == 50_000
    assert j["caps"]["max_solve_ms"] == 2000
    assert j["admin_required"] is True
    assert j["name_pattern"] == "^[A-Za-z0-9_-]{1,16}$"


# ----------------------------------------------------------------- validate
@pytest.mark.asyncio
async def test_validate_ok_for_pp(client):
    r = await client.post("/api/validate", json=PP)
    assert r.status == 200
    j = await r.json()
    assert j["ok"] is True, j["errors"]
    assert j["errors"] == []
    assert 0 < len(j["samples"]) <= 3
    s = j["samples"][0]
    assert s["clue"] and s["clue"] in s["solution"]
    assert j["timings"]["generate_ms_max"] >= 0


@pytest.mark.asyncio
async def test_validate_does_not_save(client, challenge_dir):
    r = await client.post("/api/validate", json=doc(name="DRYRUN"))
    assert (await r.json())["ok"] is True
    assert not (challenge_dir / "DRYRUN.json").exists()


@pytest.mark.asyncio
async def test_validate_fails_on_oversized_scorer(client, config):
    fat = PP["score"] + "\n" + "#" * config.max_score_code_chars
    r = await client.post("/api/validate", json=doc(name="FAT", score=fat))
    assert r.status == 200
    j = await r.json()
    assert j["ok"] is False
    assert any("score" in e and "cap" in e for e in j["errors"]), j["errors"]


@pytest.mark.asyncio
async def test_validate_fails_on_nondeterministic_generate(client):
    wobbly = "def generate(seed):\n    return str(random.random())\n"
    r = await client.post("/api/validate", json=doc(name="WOBBLY", generate=wobbly))
    j = await r.json()
    assert j["ok"] is False
    assert any("determin" in e.lower() for e in j["errors"]), j["errors"]


@pytest.mark.asyncio
async def test_validate_rejects_bad_name(client):
    r = await client.post("/api/validate", json=doc(name="way too long and spaced"))
    assert r.status == 400
    assert (await r.json())["error"] == "bad_name"


@pytest.mark.asyncio
async def test_runaway_scorer_does_not_hang_the_server(client):
    """A `while True` scorer must come back as a report, not a wedged event loop."""
    r = await client.post("/api/validate", json=doc(
        name="SPIN", score="def score(c,s):\n while 1: pass\n"))
    j = await r.json()
    assert j["ok"] is False
    # the server is still answering
    assert (await client.get("/api/config")).status == 200


# ----------------------------------------------------- submit / list / get
@pytest.mark.asyncio
async def test_submit_then_list_then_get(client, challenge_dir):
    r = await client.post("/api/challenges", json=doc(name="PP2", author="kid"))
    assert r.status == 201, await r.text()
    j = await r.json()
    assert j["saved"] is True and j["report"]["ok"] is True
    assert (challenge_dir / "PP2.json").exists()

    r = await client.get("/api/challenges")
    names = {c["name"]: c for c in (await r.json())["challenges"]}
    assert set(names) == {"PP", "PP2"}
    assert names["PP2"]["author"] == "kid"
    assert names["PP2"]["ok"] is True

    r = await client.get("/api/challenges/PP2")
    got = await r.json()
    assert got["score"] == PP["score"]
    assert got["generate"] == PP["generate"]


@pytest.mark.asyncio
async def test_submit_rejects_invalid_challenge(client, challenge_dir):
    r = await client.post("/api/challenges", json=doc(
        name="BROKEN", solve="def solve(clue):\n    return ''\n"))
    assert r.status == 400
    j = await r.json()
    assert j["saved"] is False and j["report"]["ok"] is False
    assert not (challenge_dir / "BROKEN.json").exists()


@pytest.mark.asyncio
async def test_get_unknown_challenge_is_404(client):
    r = await client.get("/api/challenges/nope")
    assert r.status == 404
    assert (await r.json())["error"] == "not_found"


# ------------------------------------------------------------ duplicates
@pytest.mark.asyncio
async def test_duplicate_name_is_409_then_overwrite_with_token(client):
    r = await client.post("/api/challenges", json=doc(author="someone else"))
    assert r.status == 409
    assert (await r.json())["error"] == "exists"

    r = await client.post("/api/challenges?overwrite=1", json=doc(author="nobody"))
    assert r.status == 403, "overwriting an existing name needs the admin token"

    r = await client.post("/api/challenges?overwrite=1", json=doc(author="organiser"),
                          headers={"X-Admin-Token": ADMIN_TOKEN})
    assert r.status == 201
    j = await r.json()
    assert j["saved"] is True and j["overwritten"] is True

    r = await client.get("/api/challenges/PP")
    assert (await r.json())["author"] == "organiser"


# ---------------------------------------------------------------- delete
@pytest.mark.asyncio
async def test_delete_requires_admin_token(client, challenge_dir):
    r = await client.delete("/api/challenges/PP")
    assert r.status == 403
    assert (challenge_dir / "PP.json").exists()

    r = await client.delete("/api/challenges/PP", headers={"X-Admin-Token": "wrong"})
    assert r.status == 403

    r = await client.delete("/api/challenges/PP", headers={"X-Admin-Token": ADMIN_TOKEN})
    assert r.status == 200
    assert (await r.json())["deleted"] == "PP"
    assert not (challenge_dir / "PP.json").exists()
    assert (await client.get("/api/challenges/PP")).status == 404


@pytest.mark.asyncio
async def test_delete_is_open_when_no_admin_token_configured(challenge_dir):
    config = GameConfig(challenge_dir=str(challenge_dir), validation_seeds=2)
    sandbox = InProcessSandbox(config)
    app = make_subapp(ChallengeStore(challenge_dir), config, sandbox, validate=validate)
    c = TestClient(TestServer(app))
    await c.start_server()
    try:
        assert (await c.delete("/api/challenges/PP")).status == 200
    finally:
        await c.close()
        sandbox.close()


# ------------------------------------------------------- the production path
@pytest.mark.asyncio
async def test_subprocess_sandbox_validates_without_blocking(challenge_dir):
    """With the real (subprocess) Sandbox validation runs on a worker thread."""
    import asyncio

    from engine.sandbox import Sandbox

    from webapp.app import MAIN_THREAD

    config = GameConfig(challenge_dir=str(challenge_dir), validation_seeds=3)
    sandbox = Sandbox(config)
    app = make_subapp(ChallengeStore(challenge_dir), config, sandbox, validate=validate)
    assert app[MAIN_THREAD] is False
    c = TestClient(TestServer(app))
    await c.start_server()
    try:
        slow, ping = await asyncio.gather(
            c.post("/api/validate", json=PP),
            c.get("/api/config"),
        )
        assert ping.status == 200, "the event loop kept serving during validation"
        assert (await slow.json())["ok"] is True
    finally:
        await c.close()
        sandbox.close()
