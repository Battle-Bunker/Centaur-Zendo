# Centaur Zendo — reference client

Players: read **[../docs/PLAYER_GUIDE.md](../docs/PLAYER_GUIDE.md)** first. It has
the rules, the strategy advice and the protocol. This file is just the usage.

## Install

```bash
pip install -r requirements.txt      # websockets
```

## Run

```bash
export ZENDO_URL=ws://localhost:8080/ws
export ZENDO_TEAM=our-team
export ZENDO_TOKEN=our-secret

python player.py status         # phase, rounds used, next round time, demo
python player.py round          # play one training round now
python player.py wait-round     # sleep until the cooldown ends, then play one
python player.py watch          # keep playing rounds until they run out
python player.py demo PP        # spend the demo ability on challenge PP
python player.py final          # run the 3-second final test (once)
```

Without the environment variables, pass them explicitly:

```bash
python player.py --url ws://host:8080/ws --team T --token S round
```

## Flags

| flag | default | meaning |
|---|---|---|
| `--url` | `$ZENDO_URL` or `ws://localhost:8080/ws` | server websocket |
| `--team` | `$ZENDO_TEAM` | team name |
| `--token` | `$ZENDO_TOKEN` | team token |
| `--strategy` | `strategy.py` next to `player.py` | the brain to load |
| `--log-dir` | `logs/` next to the strategy | where logs go |
| `--memory` | `memory.json` next to the strategy | persistent state |
| `--max-rounds` | 0 (unlimited) | `watch`: stop after N rounds |

Because `--log-dir` and `--memory` follow the strategy file, several bots can
live side by side (`sim/players/<team>/strategy.py` gets its own logs and memory)
without any extra flags.

Exit codes: `0` ok, `2` refused (cooldown / phase / round cap) or bad arguments,
`3` connection problem, `130` interrupted.

## What you edit

`strategy.py` — one required function and two optional hooks:

```python
def solve(name, clue, memory) -> str    # required
def on_round_start(memory)              # optional: precompute here, it is free
def on_round_end(items, memory)         # optional: items from `round_over`
```

`memory` is a dict, loaded from `memory.json` before each round and written back
after it. An exception inside `solve` makes the client send `skip` and keep
going; the traceback text is recorded in the round log.

## What you get back

```
logs/round_<n>.jsonl   every message in/out with timestamps (n = rounds_used)
logs/round_<n>.txt     header, per-item table, per-name tally with hit-rates
logs/round_final.*     the same, for the final test
logs/round_partial.*   a round the connection dropped in the middle of
logs/summary.txt       one line per round + running per-name hit-rate
logs/demos.jsonl       every demo result
memory.json            whatever your strategy chose to remember
```

Nothing is printed or written to disk during a round: messages are buffered in
memory and flushed after `round_over`, so the answer loop stays fast. The client
reports its own mean/median/max answer latency (challenge received → answer sent)
after every round.

## Tests

```bash
python -m pytest client/tests -q
```

The tests run the client against `client/tests/fake_server.py`, a small
in-process server that speaks the §6 protocol with two toy challenges
(`ADD`: clue `"3+4"` → `"7"`, and `ECHO`: clue → clue).
