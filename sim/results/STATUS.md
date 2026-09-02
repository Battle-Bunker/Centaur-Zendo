# Lab status (paused by the spend limit; resumable)

Cadence for all runs: 6 rounds × 0.5 s, 5 s cooldown, 1 demo per window, 3 s final. Two fresh Opus
players per class per iteration. Classification per player: cracked ≥ 90 % in the final, partial
10–90 %, failed < 10 %.

## Calibrated so far (in `challenges/`)
| class | evidence | verdict |
|---|---|---|
| quaich | crack r5–6 + partial 23 % | on target |
| OKRIN | crack r4 + partial 73 % | on target |
| murn (v2) | crack r5 + fail 3 % | on target |
| LegoZendo2 | crack r4 (2 demos, N=0 sabotage trick) + interrupted at 3 % after r2 | likely on target; re-run b |
| LegoZendo (v3) | both players interrupted after r5 at 8–9 % (35/373, 37/410); neither had the rule | leaning hard; re-run to see the final |
| Wordz | interrupted: a at 23 % (r3), b at 38 % (r4) and climbing with "rule confirmed" | leaning easy; re-run |

## Untested lab classes (built, validated, arenas torn down — re-run `sim/arena.py setup`)
velk (plait over/under), virel (block wall twins), sarn (QWERTY row travel), tovel (calendar
page), fennick (leaning books). Pool dirs: `$SCRATCH/pool-<name>-1/`; challenge JSON in
`challenges/lab/`.

## Queue for the next quota window (≤ 4 agents at a time)
1. velk a/b   2. virel a/b   3. sarn a/b   4. tovel a/b   5. fennick a/b
6. LegoZendo a/b (repeat)   7. Wordz a/b (repeat)   8. LegoZendo2 b (repeat)
Then: send each designer its results (agents can be resumed by name), iterate once, promote
on-target classes, and move the too-easy textbook classes out of the main pool.
