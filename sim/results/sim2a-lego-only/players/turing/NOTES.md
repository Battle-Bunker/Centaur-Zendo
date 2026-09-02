# LegoZendo — solved

Pool has exactly ONE challenge class: `LegoZendo`.

## Clue format
`<LETTER><N>` — LETTER in A..Z, N in {0,2,3,4,5,6,7,8,9,10,11,12} (N=1 never observed).
312 possible clues, 283 distinct seen in one round.

## Rule (confidence: very high)
The answer is an ASCII picture of a Lego structure.
* 1 stud = 3 chars wide x 2 rows tall; background = any non-letter filler char
  (`*`, `_`, `~`, `.` all accepted — the reference solver itself varies it).
* The whole structure must be a SINGLE connected blob (disconnected pieces fail).
* The **largest connected group of cells of the clue LETTER must be exactly N studs.**
  - Not total area: the reference demos always add a stray 1-stud decoy of the
    clue letter elsewhere (A6 -> components of 6 and 1 studs), and n = 6.
  - N = 0 means the structure contains no brick of that letter at all.

## Evidence
| round | test | result |
|---|---|---|
| 2 | replay demo grids w/ letter substitutions | letter irrelevant; hits exactly at N = studs of clue-letter blob (0/5/6/10 for the 5 variants) |
| 3 | `v_min` bare `L*3N` x2 rows | 182/182 |
| 3 | `v_canvas` 10-row padded canvas | 182/182 |
| 3 | `v_stack` two-level L-shape summing to N | 182/182 |
| 3 | `v_twin` two disjoint N-stud blobs | 0/161 (N>0) -> structure must be connected |
| 3 | `v_decoy` N-stud L blob + separate other-letter blob | 0/156 (N>0) -> same |

## Final answer construction
N >= 1 : two identical rows of `LETTER * (3*N)`
N == 0 : two rows of `QQQ` (any letter != clue letter)
Precomputed lookup table, ~0.12 us/call.

## Result
FINAL: 2733 presented / 2733 answered / **2733 correct (100%)** — rank 1.
Training rounds 4-12 were also 100% (8107 consecutive correct before the final).
