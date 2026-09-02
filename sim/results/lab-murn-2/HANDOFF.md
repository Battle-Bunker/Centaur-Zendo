# lab-murn-2 — murn v2 (hardened one notch), ready for player agents

Server **running**, pool = 1 challenge (`murn` v2), engine validation: ok, no errors, no
warnings (gen 0.21 ms / score 0.06 ms / solve 0.33 ms).

* run: `lab-murn-2`  port 37247  |  6 training rounds, 5 s cooldown, 0.5 s rounds, 3 s final
* team dirs:
  * murn2a: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-murn-2/players/murn2a`
  * murn2b: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-murn-2/players/murn2b`
* briefs to hand the agents verbatim (and nothing else):
  `sim/results/lab-murn-2/BRIEF_murn2a.md`, `sim/results/lab-murn-2/BRIEF_murn2b.md`
* afterwards: `python sim/arena.py teardown --run lab-murn-2` then
  `python sim/arena.py report --run lab-murn-2`

## What changed from v1 (two coupled changes, both must be found)
1. **The support law is now material-typed**: nothing may rest directly on its own kind.
   A stone still needs exactly two of the three cells below occupied, wood exactly one, but
   a stone may not have a stone immediately below it (S) and wood may not have wood
   immediately below it (staggered joints, as in masonry running bond).
2. **n now counts only the stones ABOVE the ground row** (v1 counted the whole picture).

## Classification bands (measured over 1500 clues, so the report is readable)
| what the player believes | final hit-rate |
|---|---|
| the exact v2 law (one-pass greedy is enough) | **100.0 %** |
| v1's law verbatim (untyped support counts, n = total stones) | 0.1 % |
| v1 law + v2 quota, or v2 law + v1 quota (only one change found) | 2.0 % / 1.6 % |
| "no stone on stone" only, or "no wood on wood" only | 17.4 % / 5.7 % |
| staggering found but "at least two / at least one" | 19.7 % |
| "it rests on the cell directly below" | 0.1 % |

So: **>=90 % = cracked**, 10-90 % = has most of the law but not the "exactly" or not both
staggering clauses, <10 % = failed. Nothing degenerate reaches 90 % — the ground row alone,
solid pyramids, wood-only towers, recolourings, upside-down answers, off-by-one counts, the
ground row repeated k times, the empty string, the clue itself and 1024-char junk all score 0 %.

v1 is kept for the record at `challenges/lab/murn.v1.json`.
