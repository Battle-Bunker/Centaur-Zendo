# Challenge Workshop (`webapp/`)

The page organisers use to write, validate and save Centaur Zendo challenge
generators (SPEC §8). It is one HTML file plus one aiohttp module; there is no
build step and no JavaScript dependency beyond CodeMirror 5 loaded from cdnjs
(if the CDN is blocked the three editors fall back to plain textareas).

> **Organisers only.** Every page and every API response here shows challenge
> sources — `generate`, `solve` and `score`. Players must only ever see a
> challenge *name* and a *clue*. Do not expose this app to players.

## Running it

Standalone (its own port, its own sandbox):

```bash
python -m webapp.app --challenge-dir challenges --port 8081
# then open http://localhost:8081/
```

| flag | meaning |
|------|---------|
| `--challenge-dir DIR` | directory of `<name>.json` documents (default `challenges`) |
| `--host` / `--port`   | default `0.0.0.0:8081` |
| `--config FILE`       | a `GameConfig` JSON file (caps, timings, `admin_token`) |
| `--admin-token TOK`   | require `X-Admin-Token: TOK` for DELETE and for overwriting a name |
| `--in-process`        | use `InProcessSandbox` instead of the subprocess `Sandbox` (no isolation) |
| `--fallback-validator`| validate by shelling out to `tools/quickcheck.py` instead of the engine |

Mounted inside the game server (`engine/server.py`), which is the normal way to
run it:

```python
from webapp.app import make_subapp
app.add_subapp("/submit", make_subapp(store, config, sandbox))
```

`make_subapp(store, config, sandbox, *, validate=None, spec_cls=None)` takes
`engine.challenges.ChallengeStore`, `engine.config.GameConfig` and an
`engine.sandbox.Sandbox` (an `AsyncSandbox` facade is unwrapped automatically).
`validate` defaults to `engine.challenges.validate`. Both `/submit` and
`/submit/` serve the page; the page derives its API base from `location.pathname`
so it works mounted or standalone.

## HTTP API

| method | path | notes |
|--------|------|-------|
| `GET`  | `/` | the page |
| `GET`  | `/api/config` | `{caps, validation_seeds, name_pattern, admin_required, sandbox, challenge_dir}` |
| `POST` | `/api/validate` | body = challenge document → `ValidationReport` JSON. Never saves. |
| `GET`  | `/api/challenges` | `{challenges: [{name, author, ok}]}` |
| `POST` | `/api/challenges` | validate, then save. `201` saved / `400` + report if invalid / `409` if the name exists |
| `GET`  | `/api/challenges/{name}` | the full document (sources included) |
| `DELETE` | `/api/challenges/{name}` | deletes; needs the admin token |

A challenge document is exactly the on-disk format:
`{name, author, description, generate, solve, score}` (SPEC §2).

`POST /api/challenges?overwrite=1` replaces an existing name and always requires
the admin token when one is configured. `DELETE` requires it too. When
`config.admin_token` is empty (a laptop at a workshop) both are open — that is
the documented default, not an oversight.

The `ok` flag in the list is what this process last saw when validating that
name; it is `null` for challenges nobody has validated since the server started.
Nothing is re-validated behind your back — validation costs real sandbox time.

## How validation stays safe

Challenge code is hostile by accident: a `while True` in `score` is a normal
beginner bug. So the app never runs submitted code itself. It hands the spec to
`engine.challenges.validate`, which drives the injected sandbox; the subprocess
`Sandbox` enforces per-call limits inside the child and the parent kills a wedged
worker after `timeout + 250 ms`. The app calls it on a single dedicated worker
thread behind a lock, so one submission cannot corrupt another's sandbox state
and the event loop keeps serving.

`InProcessSandbox` is the exception: its limits are `SIGALRM`, which only works
on the main thread, so the app detects it and validates inline instead — correct,
but a runaway generator blocks the server for the length of one call. Prefer the
subprocess sandbox for anything but tests.

As SPEC §3 says, this is a *game* sandbox, not a security boundary. An organiser
should read a submission before it goes into a live pool.

## Tests

```bash
python -m pytest engine/tests/test_webapp.py -q
```

They exercise the real `GameConfig`, `ChallengeStore`, `validate` and both
sandboxes through an aiohttp test client.
