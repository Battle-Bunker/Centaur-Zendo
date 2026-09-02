# lab-velk-1 — arena is up, players not run

`sim/DESIGN_LOOP.md` step 3 is done; step 4 (spawning the two player agents) needs the
Agent tool, which this designer session does not have. The orchestrator runs the players
and sends the results back for iteration 2.

* run: `lab-velk-1`, pool = **only** `challenges/lab/velk.json` (1 challenge, accepted)
* server: **running**, `127.0.0.1:43871`, phase `training`
* config: 6 training rounds x 0.5 s, 5 s cooldown, 1 demo per window, 3 s final
* arena root: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-velk-1`

Team directories (each contains `PLAYER_GUIDE.md`, `player.py`, `strategy.py`,
`connection.txt` — and nothing about the challenge):

```
velka  /tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-velk-1/players/velka
velkb  /tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-velk-1/players/velkb
```

Filled-in player briefs (give each agent ONLY its own file's text, nothing else):
`sim/results/lab-velk-1/BRIEF_velka.md`, `sim/results/lab-velk-1/BRIEF_velkb.md`
(`{TEAM_DIR}` substituted, `{ROUNDS}`=6, `{COOLDOWN}`=5, `{ROUND_SECONDS}`=0.5).

Spawn both in parallel (`subagent_type: general-purpose`, `model: opus`,
`run_in_background: true`), wait for both, then:

```
python sim/arena.py teardown --run lab-velk-1
python sim/arena.py report   --run lab-velk-1
```

and read `sim/results/lab-velk-1/REPORT.md` plus each player's `NOTES.md`, `strategy.py`
and round logs.

## Smoke test (separate throwaway arena `lab-velk-smoke`, already torn down)
* pool loaded 1 accepted / 0 rejected;
* one 0.5 s round presents **634 velk challenges**; the default random strategy scores
  **0/634**; client answer latency 0.12 ms mean;
* `python player.py demo velk` returns a clue, a plait and `score: 1`.

## What to look for in the results (classification, DESIGN_LOOP step 6)
`velk` is all-or-nothing once cracked (the exact rule scores 100.0 % with a one-pass
greedy at 0.03 ms), so a final hit-rate near 100 % = **cracked**. The interesting middle
band is 3–22 %: those rates correspond to specific partial hypotheses, and the mapping is
in `challenges/lab/NOTES_crafts.md` (e.g. ~22 % = the count plus "no two crossings at the
same gap" but not "no strand in front twice running"; ~10 % = both laws but the count
ignored; ~3 % = the right count with neither law). Please capture, per player: which
rule they believed, how many demos they spent, and the round at which their score moved.
