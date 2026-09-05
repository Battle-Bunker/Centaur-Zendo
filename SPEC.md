# Centaur Zendo — Engine Specification (v1)

Centaur Zendo is a game that teaches kids to code in the age of AI. Teams write a
bot (with AI help) that plays purely automated **one-second rounds** against a game
server. Each round is a stream of small computational challenges. Teams do not know
what the challenges are; like Zendo's "guess nature's rule", they must infer what
each challenge class wants from obscure names, obscure clues, and 0/1 feedback,
improving their bot between rounds. At the end, a single **three-second final test**
counts how many challenges the bot answers correctly.

Everything is Python 3.11. The server is one `aiohttp` process (HTTP + WebSocket on
one port, Replit-friendly). Challenge generators are **data** (JSON documents
containing Python source strings), validated at run-time when a pool is loaded, and
only the accepted ones are compiled into the running pool.

---------------------------------------------------------------------------
## 1. Repository layout

```
SPEC.md                      this document (master spec; all components conform to it)
docs/PLAYER_GUIDE.md         player-facing rules + protocol (NO challenge secrets)
docs/CHALLENGE_AUTHORING.md  how to write a challenge generator
engine/config.py             GameConfig dataclass + JSON loading (all caps/timings live here)
engine/sandbox.py            restricted exec model + subprocess worker w/ timeouts
engine/challenges.py         ChallengeSpec, store (load/save JSON), validation, CompiledPool
engine/game.py               Game state machine: teams, phases, rounds, cooldowns, demo, final, leaderboard, event log
engine/server.py             aiohttp app: /ws player protocol, admin HTTP API, status page; mounts webapp at /submit
engine/tests/                pytest tests
webapp/app.py                challenge-submission web app (aiohttp sub-app + standalone runner)
webapp/static/index.html     UI: code editor boxes per interface method, validate + submit
client/player.py             reference player client (websocket), logs everything
client/strategy.py           the ONE file players edit: solve(name, clue, memory) -> str
client/README.md
challenges/*.json            challenge generator pool (one JSON document per challenge)
tools/quickcheck.py          reference validator CLI (same exec model as the engine)
sim/                         simulation harness + results
game.example.json            example GameConfig
requirements.txt             aiohttp, websockets, pytest
.replit                      Replit run config (python -m engine.server)
```

---------------------------------------------------------------------------
## 2. Challenge generator interface (data format)

A challenge generator is a JSON document:

```json
{
  "name": "PP",
  "author": "someone",
  "description": "Palindromic prime containing the clue as a substring. (PRIVATE: never shown to players)",
  "generate": "def generate(seed):\n    r = random.Random(seed)\n    return str(r.randrange(10**4, 10**5))\n",
  "solve":    "def solve(clue):\n    ... return a correct solution string ...\n",
  "score":    "def score(clue, solution):\n    ... return 1 or 0 ...\n"
}
```

Field rules
* `name`: 1–16 chars, `[A-Za-z0-9_-]`, unique within a pool. This is the ONLY thing
  players see besides the clue, so it may be obscure ("PP", "Z7", "gloam").
* `description`: private notes; never sent to players.
* `generate`, `solve`, `score`: Python **module source** strings. Each is exec'd in its
  own fresh namespace (see §3) and must define the named top-level function:
  * `generate(seed: int) -> str`  — deterministic: same seed ⇒ same clue string.
  * `solve(clue: str) -> str`     — reference solver; returns a solution that scores 1.
    Used for load-time validation and for the player "demo" ability. Never sent to players
    except as a demo output.
  * `score(clue: str, solution: str) -> int` — returns exactly `1` (success) or `0`.
    Must return 0 for the empty string. Any exception or non-0/1 return counts as 0.

Character caps (measured as `len(source_string)`, all configurable in `GameConfig`):

| cap                          | default | applies to                       |
|------------------------------|---------|----------------------------------|
| `max_score_code_chars`       | 1024    | `score` source (512 until 2026-09-05; picture classes still aim for ≤ 512) |
| `max_clue_chars`             | 1024    | every string returned by generate|
| `max_generate_code_chars`    | 50000   | `generate` source                |
| `max_solve_code_chars`       | 5000    | `solve` source                   |
| `max_solution_chars`         | 1024    | solutions (from players & solve) |

Time caps (wall-clock per call; configurable):

| cap                 | default | note                                              |
|---------------------|---------|---------------------------------------------------|
| `max_generate_ms`   | 100     | must hold for every validation seed               |
| `max_score_ms`      | 50      | must hold for solve() output, "" and junk inputs  |
| `max_solve_ms`      | 2000    | only used at validation time and for demos        |

`validation_seeds` (default 20): number of seeds sampled at load time.

---------------------------------------------------------------------------
## 3. Execution model (engine/sandbox.py — and tools/quickcheck.py must match)

Each of the three sources is compiled with `compile(src, f"<{name}.{kind}>", "exec")`
and exec'd into a fresh dict whose `__builtins__` is a **restricted builtins** dict:

Allowed builtins: `abs all any ascii bin bool bytearray bytes callable chr complex dict
divmod enumerate filter float format frozenset getattr hasattr hash hex id int isinstance
issubclass iter len list map max min next object oct ord pow print range repr reversed
round set setattr slice sorted str sum tuple type zip True False None` plus the standard
exception classes (`Exception ValueError TypeError KeyError IndexError ZeroDivisionError
ArithmeticError StopIteration RuntimeError AssertionError OverflowError LookupError
RecursionError`) and a restricted `__import__` that only permits the allow-listed modules
below. `open`, `eval`, `exec`, `compile`, `input`, `globals`, `locals`, `vars`, `__build_class__`
... are NOT available (class definitions therefore don't work; use functions/dicts/tuples).
`print` is available but writes to the sandbox worker's stderr.

Pre-imported modules present in every namespace (no `import` needed, but allowed):
`math re random itertools functools collections string hashlib json heapq bisect
operator fractions statistics array struct base64 decimal words`. `words` is the engine's English
word-list module (`words.WORDS`, `words.COMMON`, `is_word`, `vowels`, `consonants`, `pick`; see
`engine/words.py`), backed by the `english-words` and `wordfreq` packages with a bundled fallback.
Import of anything else raises `ImportError`.

Time limits inside the worker are enforced with `signal.setitimer(ITIMER_REAL)` raising
`SandboxTimeout`; if a worker becomes unresponsive (C-level loop) the parent kills it
after `timeout + 250ms` and spawns a fresh one. The caller sees a `SandboxError`.

Sandbox worker API (engine/sandbox.py):

```python
class Sandbox:
    def __init__(self, config: GameConfig): ...
    def load(self, specs: list[ChallengeSpec]) -> None       # compile all three sources of each spec in the worker
    def generate(self, name: str, seed: int) -> str          # raises SandboxError on failure/timeout
    def score(self, name: str, clue: str, solution: str) -> int   # NEVER raises; returns 0 on any failure/timeout
    def solve(self, name: str, clue: str) -> str             # raises SandboxError
    def close(self) -> None
class SandboxPool:   # N workers, `async with pool.acquire() as sb:`; each active round holds one
```
The worker is a `multiprocessing` process (spawn or fork) talking over pipes; calls are
synchronous in the worker and awaited via `loop.run_in_executor` (or an equivalent
async-safe wrapper) in the server so concurrent rounds don't block the event loop.

Honesty note: this is a *game* sandbox (restricted builtins + timeouts + subprocess), not a
security boundary against a determined attacker. Challenge submissions should be reviewed by
an adult/organiser before being loaded into a live pool. Document this.

---------------------------------------------------------------------------
## 4. Load-time validation (engine/challenges.py)

`validate(spec, config, sandbox) -> ValidationReport` with fields
`ok: bool, errors: list[str], warnings: list[str], timings: {generate_ms_max, score_ms_max, solve_ms_max}, samples: [{seed, clue, solution}]` (≤3 samples).

Checks, in order (stop at first fatal group):
1. name/regex/unique; description present (warning if empty); code sizes within caps.
2. Each source compiles and exec's, and defines the required callable.
3. For each of `validation_seeds` random seeds (from `random.Random(config.validation_seed)`):
   * `clue = generate(seed)` is a `str`, non-empty, `len ≤ max_clue_chars`, within `max_generate_ms`.
   * `generate(seed)` a second time returns an identical string (determinism).
   * `sol = solve(clue)` is a `str`, `len ≤ max_solution_chars`, within `max_solve_ms`.
   * `score(clue, sol) == 1` within `max_score_ms`.
   * `score(clue, "") == 0`; `score(clue, junk)` for a few junk strings ("0", "x", "1"*100,
     clue itself, a shuffled solution) returns 0 or 1 without exceeding `max_score_ms`
     (an exception in score on junk is a *warning*, not an error).
   * At least one junk input must score 0 (otherwise "score accepts anything" → error).
4. Warnings (non-fatal): scorer accepts the clue itself; solve is slow (>25% of cap); etc.

`load_pool(dir_or_specs, config, sandbox) -> (CompiledPool, {name: ValidationReport})`
loads every `*.json`, validates, and builds a `CompiledPool` holding only accepted names.
Rejected challenges are logged with their reports; the server keeps running.

`ChallengeStore` (webapp + engine): `list()`, `get(name)`, `put(spec)`, `delete(name)` over a
directory of JSON files (`challenges/` by default).

---------------------------------------------------------------------------
## 5. Game rules & state machine (engine/game.py)

Phases: `lobby → training → final → finished`.

GameConfig (engine/config.py, JSON-loadable, all fields have these defaults):
```
round_seconds = 1.0            training round length
final_seconds = 3.0            final test round length
cooldown_seconds = 300         min gap between a team's consecutive training rounds (measured start→start)
max_training_rounds = 4        hard cap per team
training_seconds = None        None ⇒ max_training_rounds * cooldown_seconds + 60  (300s ⇒ 1260s = 21 min)
final_window_seconds = 600     after training ends, teams have this long to run their final
max_demos = 3                  demo requests per team per GAME (each names one class and returns one solved example)
pool_size = 7                  classes drawn into a game's pool from everything loaded (None = all)
pool_seed = None               seed of that draw (None ⇒ random at game creation; the draw is fixed for the game)
open_registration = True       unknown team names in `join` are auto-created with the supplied token
challenge_dir = "challenges"
event_log = "events.jsonl"     append-only JSONL log of every message/round for later analysis
sandbox_workers = 4
final_shared_sequence = True   all teams face the same (name, seed) sequence in the final
allow_early_final = True       a team that has used all its training rounds may start its final before training ends
+ all caps from §2/§3, validation_seeds=20, validation_seed=12345, host="0.0.0.0", port=8080, admin_token=""
```

Teams: `{name, token, rounds_used, last_round_started_at, demos_used, demo_available: bool,
final_score, history: [RoundSummary]}`.

Pool: at game creation the server draws `pool_size` classes (default 7) from the loaded set
with `pool_seed`; only those appear in `welcome.challenges`, in rounds, in demos and in the
final. A production organiser loads the whole collection and lets each game draw its seven.

**Training round** (`start_round`): allowed iff phase==training, now < training_ends_at,
`rounds_used < max_training_rounds`, and `now - last_round_started_at >= cooldown_seconds`
(no cooldown before the first round). Rounds neither grant nor consume demos.
**Demo** (`demo`): allowed iff phase==training, no round running, `demos_used < max_demos`;
the server draws a fresh seed, and re-draws (up to `DEMO_REDRAWS` = 8 times) while the
reference solution equals the clue, so a demo never shows an identity ("n = 0") example.
Refusals return `error{code: "cooldown"|"phase"|"round_cap"|"busy", retry_at}`.

Round loop (server side, per team, one at a time):
```
round_id = uuid; rng = Random(round_seed)      # training: random; final: shared config/final seed
deadline = started_at + duration
send round_started
loop:
    name = rng.choice(pool.names); seed = rng.getrandbits(32)
    clue = sandbox.generate(name, seed)        # on SandboxError: log, pick again (max 3 tries)
    send challenge{index, name, clue}
    wait for answer/skip for this (round_id,index) until deadline
    if timed out: break (unanswered item is not counted as presented-and-answered)
    score = 0 if skip else sandbox.score(name, clue, solution[:max_solution_chars])
    send result{index, score}
    if now >= deadline: break
send round_over{... items ...}
```
Answers for a stale/unknown (round_id, index) are ignored with an `error{code:"stale"}`.
A message arriving after the deadline is ignored. Timestamps are server unix-time floats.
The `challenge` for index i+1 is sent immediately after `result` for index i.

**Demo** (`demo{name}`): allowed iff phase == training, no round is running, `demos_used <
max_demos` and `name` in pool. Server picks a random seed, `clue=generate`, `solution=solve`,
`score=score(...)`, returns `demo_result{name, clue, solution, score}` and increments
`demos_used`. A team therefore has `max_demos` (default 3) demo requests for the whole game,
each on a single class of its choosing, usable at any time between rounds; with 7 classes in
the pool, choosing which classes to ask about is the scarce strategic resource of the game.
`demo_available` = (not busy and demos remain); `demos_remaining` is reported alongside it.

**Final** (`start_final`): allowed iff phase==final (i.e. now ≥ training_ends_at, or admin
forced it) — or phase==training with `allow_early_final` and all training rounds used — the team
has not run its final, and now < final_ends_at. Same loop with
`final_seconds`. `final_score = correct`. When every registered team has run its final or
the window closes, phase → `finished`. Leaderboard = teams sorted by final_score desc, then
answered asc (fewer wasted answers wins ties), then name.

Event log: every inbound/outbound message (except pings) and each round summary is appended
as one JSON line `{ts, team, dir: "in"|"out"|"round", msg}`.

Admin HTTP (header `X-Admin-Token`): `POST /admin/start` (lobby→training now, or
`{"at": ts}`), `POST /admin/force_final`, `POST /admin/reload_pool`, `GET /admin/state`
(full JSON), `GET /admin/reports` (validation reports). `GET /` renders a small status /
leaderboard HTML page; `GET /api/state` public summary (phase, timings, leaderboard, names).

---------------------------------------------------------------------------
## 6. WebSocket protocol (`/ws`, JSON text frames, one object per frame)

Client → Server
| type          | fields                                  |
|---------------|-----------------------------------------|
| `join`        | `team`, `token`                         |
| `start_round` | —                                       |
| `answer`      | `round_id`, `index`, `solution` (str)   |
| `skip`        | `round_id`, `index`                     |
| `demo`        | `name`                                  |
| `start_final` | —                                       |
| `status`      | —                                       |
| `ping`        | —                                       |

Server → Client
| type            | fields |
|-----------------|--------|
| `welcome`       | `team`, `phase`, `challenges: [names]`, `config: {round_seconds, final_seconds, cooldown_seconds, max_training_rounds, max_demos, max_solution_chars, max_clue_chars, training_ends_at, final_ends_at}`, `rounds_used`, `next_round_available_at`, `demo_available`, `demos_remaining`, `server_time` |
| `round_started` | `round_id`, `kind: "training"|"final"`, `duration_ms`, `started_at`, `deadline` |
| `challenge`     | `round_id`, `index`, `name`, `clue` |
| `result`        | `round_id`, `index`, `score` |
| `round_over`    | `round_id`, `kind`, `presented`, `answered`, `correct`, `items: [{index,name,clue,solution,score}]`, `rounds_used`, `next_round_available_at`, `demo_available`, `demos_remaining` |
| `demo_result`   | `name`, `clue`, `solution`, `score` |
| `status`        | `phase`, `server_time`, `training_ends_at`, `final_ends_at`, `rounds_used`, `next_round_available_at`, `demo_available`, `demos_remaining`, `final_score`, `leaderboard` |
| `error`         | `code`, `message`, optional `retry_at` |
| `pong`          | `server_time` |

One socket per team at a time (a new `join` for the same team replaces the old socket and
aborts any in-flight round). All server messages that belong to a round carry `round_id`.

---------------------------------------------------------------------------
## 7. Reference client (client/)

`python client/player.py --url ws://localhost:8080/ws --team T --token S round`
runs one training round; `demo NAME`, `final`, `status` subcommands. During a round it
calls `strategy.solve(name, clue, memory) -> str` for each challenge (memory is a dict
persisted to `memory.json` between rounds so players can keep state across rounds), sends
the answer, and appends every event to `logs/round_<n>.jsonl` plus a human-readable
`logs/round_<n>.txt` summary (name, clue, answer, score per item; per-name tallies).
Default `strategy.py` returns random short strings and records everything — the intended
"round zero" behaviour. It must be robust: an exception in `solve` ⇒ send `skip`.

---------------------------------------------------------------------------
## 8. Web app (webapp/)

`/submit` page: fields name, author, description; three code editors (CodeMirror from
cdnjs, python mode, falling back to textareas) pre-filled with skeletons for `generate`,
`solve`, `score`, each showing live char count vs cap; **Validate** (POST `/api/validate`
→ ValidationReport JSON, rendered: errors/warnings/timings/samples) and **Submit** (POST
`/api/challenges` → saves to the store only if validation passes; returns the report).
`GET /api/challenges` lists names+authors+ok; `GET /api/challenges/{name}`,
`DELETE /api/challenges/{name}` (admin token). `GET /api/config` returns the caps.
Standalone: `python -m webapp.app --challenge-dir challenges --port 8081`.

---------------------------------------------------------------------------
## 9. Judgement calls (declared for the organiser)
* Solutions and clues are strings; structured data is JSON-encoded by convention.
* No hidden "secret" channel from generate to score: a clue must carry everything the
  scorer needs (verify-easy / find-hard). Keeps the short scorer honest and Zendo-like.
* Training-time limit = 4×cooldown+60s and a hard cap of 4 rounds, both enforced
  (21 minutes at the 5-minute cooldown; 30 s cooldown ⇒ 3 min).
* Three demo requests per team per game (any time between rounds, one class each); seven
  classes per game drawn at game creation. Balanced classes sit on the edge of needing a
  demo: the clue must reveal the *shape* of an answer (what kind of data to send) so that a
  team can score without a demo, while the rule itself usually needs the example.
* Final test uses a shared (name, seed) sequence for all teams for fairness.
* Teams that ran their final rank above no-shows; ties broken by fewer answers (precision), then name.
* Sandbox is a game-grade sandbox, not a security boundary; organisers review submissions.
