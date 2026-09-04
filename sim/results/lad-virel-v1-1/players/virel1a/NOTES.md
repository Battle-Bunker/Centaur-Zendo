# virel — notes

Pool has exactly ONE class: `virel`.

## Clue format
`DIGITS/N`  e.g. `33655/4`, `534562/6`
- DIGITS: 3..6 chars, each digit in 2..6
- N: 1..10, larger N more likely with longer DIGITS

## Demo 1: 33655/4
9 lines, each exactly 22 chars = sum(3,3,6,5,5).
Tokens `[` + '-'*k + `]`, width = k+2 in 2..6.
LAST line token widths = 3,3,6,5,5 = the clue digits exactly.
Joint sets of all 9 rows intersect to EMPTY -> "crack-free wall" (PE215 style).
Adjacent rows DO share joints, so only full-height cracks are forbidden.

## Demo 2: 534562/6
8 lines, each 25 chars = sum(5,3,4,5,6,2).
LAST line = 5,3,4,5,6,2 = clue. Crack-free overall (intersection empty at row 4).

## Open question: what is N?
Not height (9 vs N=4; 8 vs N=6). Not #bricks, not #distinct lengths,
not longest crack run. Height may simply be free.

## Round 2 experiment
Cycle 16 variants by memory['_index'] % 16: heights R, R+1, R+2, R+3, 2,3,4,5,6,8,9,12
plus controls (not crack-free / clue row first / no clue row / adjacent-disjoint).

## RULE FOUND (round 2 analysis)
Answer = brick wall, rows = compositions of W = sum(clue digits) into parts 2..6,
rendered `[`+'-'*(L-2)+`]`, rows joined by '\n'.
1. LAST row must be exactly the clue digits (clue-first / absent scored 0/58).
2. Total number of bricks occupying the *identical* (start,length) position in
   two VERTICALLY ADJACENT rows must equal N exactly.
   round2: adjbrick_tot-N == 0 -> 29 wins / 45; any other offset -> 0 wins / 419.
   All three demos: adjbrick_tot == N (4, 6, 4).
3. Height H >= 5. The only abt==N & clue-last losers were H=3,4 (10 of them).
   Wins observed at H = 5,6,7,8,9,12.
4. Crack-free (no vertical line is a joint in every row) — all demos and all
   winners satisfy it; not independently tested, so keep enforcing it.

## Result
round 1 skip-all harvest (1036 clues) -> round 2 16-way controlled experiment
(29/464) -> rule identified -> rounds 3-6 all 100%.
FINAL: 2707 presented / 2707 answered / 2707 correct.
Final code = strategy.py (H=5 first, escalate on generation failure),
backups: strategy_v1_confirmed.py, strategy_v2_confirmed.py, strategy_v3_adaptive.py.
