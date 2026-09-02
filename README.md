# Centaur Zendo

A game that teaches kids to code in the age of AI.

Teams write a bot — with an AI assistant helping them — that plays fully automated
**one-second rounds** against a game server. Each round is a stream of small
computational challenges. Nobody tells the teams what the challenges *are*: like
Zendo's "guess nature's rule", they only see an obscure name (`PP`, `krom`,
`hanjie`), an obscure clue string, and a 0/1 score per answer. Between rounds they
improve the bot. At the end, one shared **three-second final test** counts how many
challenges each bot answers correctly.

A round is deliberately short and the cooldown between rounds is long (5 minutes by
default): the time is meant to be spent *thinking and coding*, not grinding.

* Rules and protocol for players: [`docs/PLAYER_GUIDE.md`](docs/PLAYER_GUIDE.md)
* Writing challenges: [`docs/CHALLENGE_AUTHORING.md`](docs/CHALLENGE_AUTHORING.md)
* The master specification everything conforms to: [`SPEC.md`](SPEC.md)

## Layout

```
engine/config.py       GameConfig: every cap and timing, loaded from one JSON file
engine/sandbox.py      restricted-exec subprocess sandbox + worker pool
engine/challenges.py   ChallengeSpec/Store, load-time validation, CompiledPool
engine/game.py         the state machine: teams, phases, rounds, demos, final, log
engine/server.py       aiohttp app: /ws protocol, admin API, status page, /submit
webapp/                challenge-submission web app (mounted at /submit)
client/                reference player bot; players edit client/strategy.py
challenges/*.json      the challenge pool (one JSON document per challenge)
tools/quickcheck.py    dependency-free validator CLI for challenge authors
sim/smoke.py           end-to-end test: real server, two scripted players
game.example.json      example config (copy it to game.json)
```

## Install

```bash
pip install -r requirements.txt        # aiohttp, websockets, pytest, pytest-asyncio
```
Python 3.11+.

## Run the server

```bash
cp game.example.json game.json         # then edit admin_token, cooldown, ...
python -m engine.server --config game.json --start-now
```

| flag | meaning |
|------|---------|
| `--config PATH` | GameConfig JSON (default `game.json`; falls back to `game.example.json`) |
| `--host` / `--port` | override the config; `$PORT` also overrides the port |
| `--challenge-dir DIR` | where the `*.json` challenges live (default `challenges/`) |
| `--start-now` | begin the training phase immediately instead of waiting for `/admin/start` |
| `--admin-token T` | set/override the admin token |

At start-up every challenge is validated in the sandbox; only the ones that pass are
served, and the rejected ones are logged with their errors. Then:

* `http://localhost:8080/` — status page and live leaderboard
* `http://localhost:8080/api/state` — the same thing as JSON
* `ws://localhost:8080/ws` — the player protocol
* `http://localhost:8080/submit` — the challenge submission app

Admin API (send `X-Admin-Token: <admin_token>`; **if `admin_token` is empty these
endpoints are open to anyone and the server logs a warning**):

```bash
curl -XPOST localhost:8080/admin/start        -H "X-Admin-Token: $T"   # lobby -> training
curl -XPOST localhost:8080/admin/start        -H "X-Admin-Token: $T" -d '{"at": 1788000000}'
curl -XPOST localhost:8080/admin/force_final  -H "X-Admin-Token: $T"
curl -XPOST localhost:8080/admin/reload_pool  -H "X-Admin-Token: $T"   # re-validate challenges/
curl       localhost:8080/admin/state         -H "X-Admin-Token: $T"
curl       localhost:8080/admin/reports       -H "X-Admin-Token: $T"   # validation reports
```

Every frame in and out (except pings) plus a summary of every round is appended to
`events.jsonl` (`{ts, team, dir, msg}` per line) for post-game analysis.

## Run a player

```bash
python client/player.py --url ws://localhost:8080/ws --team T --token S status
python client/player.py --url ws://localhost:8080/ws --team T --token S round
python client/player.py ... demo PP        # spend the demo on one challenge
python client/player.py ... final          # the one 3-second final test
```

Teams only ever edit `client/strategy.py` (`solve(name, clue, memory) -> str`); the
client logs every clue, answer and score to `client/logs/` so they can look for the
pattern. See [`client/README.md`](client/README.md).

## Run the submission web app

It is mounted inside the server at `/submit`, or standalone:

```bash
python -m webapp.app --challenge-dir challenges --port 8081
```

Authors paste `generate` / `solve` / `score` sources, hit **Validate** (the same
checks the server runs at load time) and **Submit**. From the command line,
`python tools/quickcheck.py challenges/PP.json -v` does the same validation with no
dependencies.

> The sandbox (restricted builtins, no `open`/`eval`/`import` outside an allow-list,
> wall-clock limits, separate processes) is a *game* sandbox, not a security
> boundary. An organiser should read submitted challenges before loading them.

## Tests

```bash
python -m pytest engine/tests -q      # unit + protocol tests
python sim/smoke.py                   # end-to-end: real server, 2 bots, ~35 s
```

`sim/smoke.py` starts a real server on a free port with a fast config (2 s cooldown,
3 training rounds, 30 s of training), plays two scripted teams through training,
demos and the final, checks the protocol invariants and prints per-message latency
and the leaderboard.

## Deploy on Replit

1. Import this repository into a Replit **Python 3.11** Repl.
2. `cp game.example.json game.json` and set `admin_token` to something private.
   Leave `"host": "0.0.0.0"`; the port comes from `$PORT` (8080).
3. Press **Run**. `.replit` runs `python -m engine.server --config game.json`, and
   the webview shows the status page. Deploy (Autoscale/Cloud Run target) to get a
   stable public URL; players then connect to `wss://<your-repl>.repl.co/ws`.
4. Start the game from the admin API (or run with `--start-now`).

Replit's filesystem is persistent per Repl, so `challenges/` and `events.jsonl`
survive restarts — but a redeploy restarts the process, which resets the in-memory
game state (teams, rounds, leaderboard). Start the game only once you are ready.
