# LegoZendo2 — solved

## Clue format
`<A><B><N>` — two uppercase colour letters (A-Z, uniform; A==B never seen in 1229 clues)
and N in 0..12.

## Answer format
An ASCII grid, newline-separated, `_` = empty (server also emits `.`; any width/height
accepted — a 4-row grid works). The grid is tiled with 6-cell LEGO pieces, each a
2x3 or 3x2 rectangle. Pieces may float; gravity/connectivity are NOT required.

## The rule (confidence: certain — 4459/4459 answers correct once implemented)
Score 1 iff the number of **staggered left-right contacts between an A piece and a
B piece equals N**: an A piece whose right edge touches a B piece sitting exactly one
row lower, i.e. a contact of length 2.

Ruled out by experiment:
* aligned side-by-side (contact 3)  -> counts as 0
* vertical stacking (A on B, B on A) -> counts as 0
* empty string / unparseable answer  -> scores 0 even for N=0
* piece counts, colour counts, plain adjacency, cell-level contact counts

## Construction used
N>=1: 4 rows x (5N-1) cols; unit k at col 5k: A as 3x2 at rows 0-2, B as 3x2 at
rows 1-3 shifted 2 cols right. One blank column between units.
N==0: 3x6 grid `AA__BB` — non-touching A and B piece.

All 8788 possible answers precomputed in `on_round_start` (0.12 s, free);
`solve()` is a dict lookup at ~0.2 us.

## Round log
| round | strategy | correct/answered |
|---|---|---|
| 1 | constant demo grid | 26/344 |
| 2 | aligned A-left-of-B | 37/485 |
| 3 | 6-way probe (diagnostic on N=0 clues) | 142/400 |
| 4 | staggered, 12x32 | 587/587 |
| 5 | staggered, trimmed grid | 598/598 |
| 6 | same (confirmation) | 594/594 |
| final | same | **3280/3280** |
