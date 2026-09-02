"""Centaur Zendo server: one aiohttp process, HTTP + WebSocket on one port.

    python -m engine.server --config game.json [--host H] [--port N]
                            [--challenge-dir challenges] [--start-now]

Routes (SPEC §5/§6)
    GET  /             small status + leaderboard page
    GET  /api/state    public state (phase, timings, leaderboard, challenge names)
    GET  /ws           the player protocol
    POST /admin/start        {"at": ts?}      lobby -> training
    POST /admin/force_final
    POST /admin/reload_pool
    GET  /admin/state        full state
    GET  /admin/reports      load-time validation reports
    /submit/*          the challenge submission web app (if webapp/ is present)
"""
from __future__ import annotations

import argparse
import asyncio
import contextlib
import html
import json
import logging
import os
import sys
import time
from typing import Any, Optional

from aiohttp import WSMsgType, web

from engine.config import GameConfig
from engine.game import FINAL, TRAINING, Game, GameError, SandboxPoolAdapter

log = logging.getLogger("zendo.server")

GAME = web.AppKey("game", object)
CONFIG = web.AppKey("config", object)
POOL = web.AppKey("pool", object)
REPORTS = web.AppKey("reports", dict)
SANDBOX = web.AppKey("sandbox", object)
SANDBOX_POOL = web.AppKey("sandbox_pool", object)
STORE = web.AppKey("store", object)
CONNS = web.AppKey("connections", dict)


# ---------------------------------------------------------------------------
# websocket connection
# ---------------------------------------------------------------------------
class Connection:
    """One player socket.  At most one per team; a new join replaces the old."""

    def __init__(self, app: web.Application, ws: web.WebSocketResponse):
        self.app = app
        self.ws = ws
        self.game: Game = app[GAME]
        self.team = None
        self.pending: dict[tuple[str, int], asyncio.Future] = {}
        self.round_task: Optional[asyncio.Task] = None
        self.round: Any = None
        self._send_lock = asyncio.Lock()
        self.closing = False

    # -- io ----------------------------------------------------------------
    async def send(self, msg: dict, log_it: bool = True) -> None:
        if self.ws.closed:
            return
        payload = json.dumps(msg)
        try:
            async with self._send_lock:
                await self.ws.send_str(payload)
        except (ConnectionResetError, RuntimeError) as exc:  # socket died mid-round
            log.debug("send failed: %s", exc)
            return
        if log_it:
            self.game.log_event(self.team.name if self.team else None, "out", msg)

    async def error(self, code: str, message: str, retry_at: Optional[float] = None) -> None:
        msg = {"type": "error", "code": code, "message": message}
        if retry_at is not None:
            msg["retry_at"] = retry_at
        await self.send(msg)

    # -- lifecycle ---------------------------------------------------------
    async def cancel_round(self, reason: str = "aborted") -> None:
        task, self.round_task = self.round_task, None
        if task is not None and not task.done():
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await task
        if self.team is not None:
            await self.game.abort_round(self.team, reason)
        for fut in list(self.pending.values()):
            if not fut.done():
                fut.cancel()
        self.pending.clear()

    async def replaced_by(self, other: "Connection") -> None:
        """A second join for the same team took over this socket."""
        self.closing = True
        await self.cancel_round("socket_replaced")
        await self.error("replaced", "another socket joined as this team")
        with contextlib.suppress(Exception):
            await self.ws.close(code=4000, message=b"replaced")

    async def close(self) -> None:
        await self.cancel_round("disconnected")
        conns = self.app[CONNS]
        if self.team is not None and conns.get(self.team.name) is self:
            conns.pop(self.team.name, None)

    # -- dispatch ----------------------------------------------------------
    async def handle_raw(self, raw: str) -> None:
        try:
            data = json.loads(raw)
        except Exception:
            await self.error("bad_message", "frames must be JSON objects")
            return
        if not isinstance(data, dict):
            await self.error("bad_message", "frames must be JSON objects")
            return
        kind = data.get("type")
        if kind == "ping":  # pings are deliberately not logged (SPEC §5)
            await self.send({"type": "pong", "server_time": self.game.clock()}, log_it=False)
            return
        self.game.log_event(self.team.name if self.team else None, "in", data)
        try:
            await self.dispatch(kind, data)
        except GameError as exc:
            await self.send(exc.to_message())
        except Exception as exc:  # never kill the socket on a bad frame
            log.exception("error handling %r", kind)
            await self.error("internal", f"{type(exc).__name__}: {exc}")

    async def dispatch(self, kind: Any, data: dict) -> None:
        if kind == "join":
            await self.do_join(data)
            return
        if self.team is None:
            await self.error("not_joined", "send join{team, token} first")
            return
        if kind == "start_round":
            await self.start_round(TRAINING)
        elif kind == "start_final":
            await self.start_round(FINAL)
        elif kind in ("answer", "skip"):
            self.deliver(kind, data)
        elif kind == "demo":
            result = await self.game.demo(self.team, data.get("name"))
            await self.send(result)
        elif kind == "status":
            await self.send(self.game.status(self.team))
        else:
            await self.error("unknown_type", f"unknown message type {kind!r}")

    async def do_join(self, data: dict) -> None:
        team = self.game.join(data.get("team"), data.get("token", ""))
        conns = self.app[CONNS]
        old = conns.get(team.name)
        if old is not None and old is not self:
            await old.replaced_by(self)
        if self.team is not None and self.team is not team:
            await self.cancel_round("rejoined")
        self.team = team
        conns[team.name] = self
        await self.send(self.game.welcome(team))

    async def start_round(self, kind: str) -> None:
        if self.round_task is not None and not self.round_task.done():
            raise GameError("busy", "a round is already running for this team")
        self.round_task = asyncio.ensure_future(run_round(self, kind))

    def deliver(self, kind: str, data: dict) -> None:
        """Route an answer/skip to the round coroutine waiting for it."""
        key = (data.get("round_id"), data.get("index"))
        fut = self.pending.get(key)
        if fut is None or fut.done():
            rnd = self.round
            round_over = rnd is None or getattr(rnd, "finished", False) or getattr(rnd, "aborted", False) \
                or rnd.expired()
            if round_over and data.get("round_id") == getattr(self, "last_round_id", None):
                return  # SPEC §5: a message arriving after the deadline is ignored silently
            asyncio.ensure_future(
                self.error("stale", "no challenge is waiting for that (round_id, index)")
            )
            return
        if kind == "skip":
            fut.set_result(None)
        else:
            solution = data.get("solution", "")
            fut.set_result("" if solution is None else str(solution))


async def run_round(conn: Connection, kind: str) -> None:
    """The SPEC §5 round loop: result(i) always precedes challenge(i+1)."""
    game, team = conn.game, conn.team
    try:
        rnd = game.start_round(team, kind)
    except GameError as exc:
        await conn.send(exc.to_message())
        return
    conn.round = rnd
    conn.last_round_id = rnd.round_id
    try:
        await rnd.open()
        await conn.send(rnd.started_message())
        while True:
            item = await rnd.next_challenge()
            if item is None:
                break
            key = (rnd.round_id, item.index)
            fut = asyncio.get_running_loop().create_future()
            conn.pending[key] = fut
            await conn.send({"type": "challenge", "round_id": rnd.round_id,
                             "index": item.index, "name": item.name, "clue": item.clue})
            timeout = rnd.deadline - game.clock()
            if timeout <= 0:
                break
            try:
                solution = await asyncio.wait_for(fut, timeout)
            except (asyncio.TimeoutError, TimeoutError):
                break
            finally:
                conn.pending.pop(key, None)
            try:
                score = await rnd.submit(item.index, solution)
            except GameError as exc:
                await conn.send(exc.to_message())
                break
            await conn.send({"type": "result", "round_id": rnd.round_id,
                             "index": item.index, "score": score})
            if rnd.expired():
                break
        summary = await rnd.finish()
        await conn.send({
            "type": "round_over",
            **summary,
            "rounds_used": team.rounds_used,
            "next_round_available_at": game.next_round_available_at(team),
            "demo_available": game.demo_available(team),
        })
    except asyncio.CancelledError:
        with contextlib.suppress(Exception):
            await rnd.abort("cancelled")
        raise
    except Exception as exc:
        log.exception("round %s failed", rnd.round_id)
        with contextlib.suppress(Exception):
            await rnd.finish("error")
        await conn.error("internal", f"round failed: {type(exc).__name__}: {exc}")
    finally:
        conn.round = None
        if not rnd.finished:
            with contextlib.suppress(Exception):
                await rnd.finish("error")


async def ws_handler(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse(heartbeat=30.0, max_msg_size=4 * 1024 * 1024)
    await ws.prepare(request)
    conn = Connection(request.app, ws)
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                await conn.handle_raw(msg.data)
            elif msg.type == WSMsgType.ERROR:  # pragma: no cover
                log.warning("ws error: %s", ws.exception())
                break
    finally:
        await conn.close()
    return ws


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
def _fmt_time(ts: Optional[float]) -> str:
    if not ts:
        return "—"
    return time.strftime("%H:%M:%S", time.localtime(ts))


async def index(request: web.Request) -> web.Response:
    game: Game = request.app[GAME]
    state = game.public_state()
    rows = "".join(
        f"<tr><td>{r['rank']}</td><td>{html.escape(r['team'])}</td>"
        f"<td class=n>{'—' if r['final_score'] is None else r['final_score']}</td>"
        f"<td class=n>{r['answered']}</td><td class=n>{r['rounds_used']}</td></tr>"
        for r in state["leaderboard"]
    ) or "<tr><td colspan=5><i>no teams yet</i></td></tr>"
    names = ", ".join(html.escape(n) for n in state["challenges"]) or "<i>none loaded</i>"
    body = f"""<!doctype html><meta charset=utf-8><meta http-equiv=refresh content=5>
<title>Centaur Zendo</title>
<style>
body{{font:15px/1.5 system-ui,sans-serif;margin:2rem auto;max-width:44rem;padding:0 1rem}}
table{{border-collapse:collapse;width:100%;margin:.5rem 0}}
th,td{{border-bottom:1px solid #ddd;padding:.35rem .5rem;text-align:left}}
td.n,th.n{{text-align:right}} code{{background:#f4f4f4;padding:.1rem .3rem;border-radius:3px}}
.phase{{font-weight:600}} .muted{{color:#666}}
</style>
<h1>Centaur Zendo</h1>
<p>Phase: <span class=phase>{state['phase']}</span> &middot;
server time {_fmt_time(state['server_time'])} &middot;
training ends {_fmt_time(state['training_ends_at'])} &middot;
final ends {_fmt_time(state['final_ends_at'])}</p>
<h2>Leaderboard</h2>
<table><tr><th>#</th><th>team</th><th class=n>final</th><th class=n>answered</th>
<th class=n>rounds</th></tr>{rows}</table>
<h2>Challenges ({len(state['challenges'])})</h2><p>{names}</p>
<p class=muted>Play: <code>ws://&lt;host&gt;/ws</code> &middot;
<a href="/api/state">/api/state</a> &middot; <a href="/submit/">submit a challenge</a></p>
"""
    return web.Response(text=body, content_type="text/html")


async def api_state(request: web.Request) -> web.Response:
    return web.json_response(request.app[GAME].public_state())


def check_admin(request: web.Request) -> None:
    token = getattr(request.app[CONFIG], "admin_token", "") or ""
    if not token:
        return  # open admin: warned about at startup
    if request.headers.get("X-Admin-Token", "") != token:
        raise web.HTTPUnauthorized(text=json.dumps({"error": "bad admin token"}),
                                   content_type="application/json")


async def admin_start(request: web.Request) -> web.Response:
    check_admin(request)
    at = None
    with contextlib.suppress(Exception):
        body = await request.json()
        if isinstance(body, dict) and body.get("at") is not None:
            at = float(body["at"])
    return web.json_response(request.app[GAME].start_training(at))


async def admin_force_final(request: web.Request) -> web.Response:
    check_admin(request)
    return web.json_response(request.app[GAME].force_final())


async def admin_state(request: web.Request) -> web.Response:
    check_admin(request)
    return web.json_response(request.app[GAME].admin_state())


async def admin_reports(request: web.Request) -> web.Response:
    check_admin(request)
    return web.json_response(reports_json(request.app[REPORTS]))


async def admin_reload_pool(request: web.Request) -> web.Response:
    check_admin(request)
    app = request.app
    config = app[CONFIG]
    from engine.challenges import load_pool

    loop = asyncio.get_running_loop()
    compiled, reports = await loop.run_in_executor(
        None, lambda: load_pool(config.challenge_dir, config, app[SANDBOX])
    )
    await app[SANDBOX_POOL].load(compiled.spec_list)
    app[POOL].compiled = compiled
    app[REPORTS] = reports
    log.info("pool reloaded: %s", pool_summary(compiled, reports))
    return web.json_response({"ok": True, "challenges": list(compiled.names),
                             "reports": reports_json(reports)})


def reports_json(reports: dict) -> dict:
    out = {}
    for name, rep in (reports or {}).items():
        to_dict = getattr(rep, "to_dict", None)
        out[name] = to_dict() if callable(to_dict) else rep
    return out


def pool_summary(compiled: Any, reports: dict) -> str:
    accepted = list(getattr(compiled, "names", []))
    rejected = [n for n, r in (reports or {}).items() if not getattr(r, "ok", True)]
    return f"{len(accepted)} accepted ({', '.join(accepted) or '-'}), {len(rejected)} rejected"


def log_validation_summary(compiled: Any, reports: dict) -> None:
    accepted = list(getattr(compiled, "names", []))
    log.info("challenge pool: %d accepted: %s", len(accepted), ", ".join(accepted) or "(none)")
    for name, rep in (reports or {}).items():
        ok = getattr(rep, "ok", True)
        errors = getattr(rep, "errors", []) or []
        warnings = getattr(rep, "warnings", []) or []
        if not ok:
            log.warning("  REJECTED %-16s %s", name, "; ".join(errors))
        elif warnings:
            log.info("  accepted %-16s (warnings: %s)", name, "; ".join(warnings))
    if not accepted:
        log.error("no challenges were accepted — rounds cannot start")


# ---------------------------------------------------------------------------
# app construction
# ---------------------------------------------------------------------------
def attach_routes(app: web.Application) -> web.Application:
    """Register every route on an app that already carries GAME/CONFIG/... keys."""
    app.router.add_get("/", index)
    app.router.add_get("/api/state", api_state)
    app.router.add_get("/ws", ws_handler)
    app.router.add_post("/admin/start", admin_start)
    app.router.add_post("/admin/force_final", admin_force_final)
    app.router.add_post("/admin/reload_pool", admin_reload_pool)
    app.router.add_get("/admin/state", admin_state)
    app.router.add_get("/admin/reports", admin_reports)
    return app


def mount_webapp(app: web.Application, store: Any, config: Any, sandbox: Any) -> bool:
    """Mount webapp/ at /submit if it is present (it is written independently)."""
    try:
        from webapp.app import make_subapp
    except Exception as exc:
        log.info("submission web app not mounted (%s)", exc)
        return False
    try:
        app.add_subapp("/submit", make_subapp(store, config, sandbox))
    except Exception:
        log.exception("submission web app failed to mount")
        return False
    log.info("submission web app mounted at /submit")
    return True


async def build_app(config: GameConfig, start_now: bool = False) -> web.Application:
    from engine.challenges import ChallengeStore, load_pool
    from engine.sandbox import Sandbox, SandboxPool

    app = web.Application()
    app[CONFIG] = config

    # One plain Sandbox validates the pool at load time and backs /submit;
    # a SandboxPool of `sandbox_workers` serves the rounds (one worker per round).
    sandbox = Sandbox(config)
    loop = asyncio.get_running_loop()
    compiled, reports = await loop.run_in_executor(
        None, lambda: load_pool(config.challenge_dir, config, sandbox)
    )
    log_validation_summary(compiled, reports)

    sbpool = SandboxPool(config)
    await sbpool.start()
    await sbpool.load(compiled.spec_list)

    pool = SandboxPoolAdapter(compiled, sbpool)
    game = Game(config, pool)
    if start_now:
        game.start_training()
        log.info("training started (--start-now); it ends at %s", _fmt_time(game.training_ends_at))

    app[GAME] = game
    app[POOL] = pool
    app[REPORTS] = reports
    app[SANDBOX] = sandbox
    app[SANDBOX_POOL] = sbpool
    app[STORE] = ChallengeStore(config.challenge_dir)
    app[CONNS] = {}

    attach_routes(app)
    mount_webapp(app, app[STORE], config, sandbox)

    if not (getattr(config, "admin_token", "") or ""):
        log.warning("admin_token is empty: /admin/* endpoints are OPEN to anyone")

    async def _cleanup(a: web.Application) -> None:
        for conn in list(a[CONNS].values()):
            with contextlib.suppress(Exception):
                await conn.cancel_round("shutdown")
        with contextlib.suppress(Exception):
            await a[SANDBOX_POOL].close()
        with contextlib.suppress(Exception):
            a[SANDBOX].close()
        a[GAME].close()

    app.on_cleanup.append(_cleanup)
    return app


def load_config(path: Optional[str]) -> GameConfig:
    if not path:
        return GameConfig()
    if os.path.exists(path):
        return GameConfig.load(path)
    fallback = "game.example.json"
    if os.path.exists(fallback):
        log.warning("%s not found; falling back to %s", path, fallback)
        return GameConfig.load(fallback)
    log.warning("%s not found; using built-in defaults", path)
    return GameConfig()


def parse_args(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(prog="python -m engine.server",
                                 description="Centaur Zendo game server")
    ap.add_argument("--config", default="game.json", help="GameConfig JSON (default: game.json)")
    ap.add_argument("--host", default=None)
    ap.add_argument("--port", type=int, default=None)
    ap.add_argument("--challenge-dir", default=None)
    ap.add_argument("--admin-token", default=None)
    ap.add_argument("--event-log", default=None)
    ap.add_argument("--start-now", action="store_true",
                    help="go straight to the training phase instead of waiting for /admin/start")
    ap.add_argument("--log-level", default="INFO")
    return ap.parse_args(argv)


def config_from_args(args: argparse.Namespace) -> GameConfig:
    config = load_config(args.config)
    if args.host:
        config.host = args.host
    if args.challenge_dir:
        config.challenge_dir = args.challenge_dir
    if args.admin_token is not None:
        config.admin_token = args.admin_token
    if args.event_log is not None:
        config.event_log = args.event_log
    # Replit (and most PaaS) hand the port over in $PORT.
    env_port = os.environ.get("PORT")
    if args.port:
        config.port = args.port
    elif env_port and env_port.isdigit():
        config.port = int(env_port)
    return config


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, str(args.log_level).upper(), logging.INFO),
                        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")
    config = config_from_args(args)
    log.info("Centaur Zendo on http://%s:%s  (challenges=%s, workers=%d)",
             config.host, config.port, config.challenge_dir, config.sandbox_workers)
    web.run_app(build_app(config, start_now=args.start_now),
                host=config.host, port=config.port, print=None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
