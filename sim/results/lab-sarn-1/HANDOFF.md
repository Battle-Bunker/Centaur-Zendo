# lab-sarn-1 — handoff to the orchestrator (players not run by the designer)

Arena is **up** and in `training`. Pool = `sarn` alone, so each team can spend all six demos
on this one class.

* config: 6 training rounds x 0.5 s, 5 s cooldown, 1 demo per window, 3 s final
* port 60703, server pid 3496
* team dirs (each contains player.py, strategy.py, PLAYER_GUIDE.md, connection.txt):
  * `sarna` -> `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-sarn-1/players/sarna`
  * `sarnb` -> `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-sarn-1/players/sarnb`

Run two player agents in parallel (opus, background) with the text of
`sim/PLAYER_AGENT_BRIEF.md`, `{TEAM_DIR}` = the directory above, `{ROUNDS}`=6,
`{COOLDOWN}`=5, `{ROUND_SECONDS}`=0.5, and nothing else. Then:

```
python sim/arena.py teardown --run lab-sarn-1
python sim/arena.py report   --run lab-sarn-1
```

and send the designer `sim/results/lab-sarn-1/REPORT.md` plus each player's `NOTES.md`,
`strategy.py` and their written report.

What to look for when classifying (private, do not show players): the rule is
"every word starts with the clue letter; word i's QWERTY **row travel** equals digit i",
where row travel sums `|row(a)-row(b)|` over neighbouring letters with rows
`qwertyuiop`/`asdfghjkl`/`zxcvbnm`. A player scoring 1-3 % is counting row *changes*
(the near miss); 0.2-0.6 % means a fitted letter-weight model; ~0 % means no keyboard idea
at all. See `challenges/lab/NOTES_wordplay.md` for the full design record.
