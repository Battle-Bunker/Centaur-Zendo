# murn — SOLVED

Clue: `<row>|<N>` where row is a string over `. o #` (width 9..16) and N is 3..25.

Answer: a grid of lines, all of width W, whose **last line is the clue row**,
containing **exactly N `#` above that last line**.

Legality of a cell above the bottom line: let k = number of non-`.` cells in the
line directly BELOW it, within +-1 column (clipped at the edges).
  k == 1  -> the cell may be `o`
  k == 2  -> the cell may be `#`
  k == 0 or 3 -> must be `.`
  `.` is always allowed.
Also observed (and always respected by the solver): a non-`.` cell never sits
directly on top of the same symbol.

Solver: build upward from the clue with bitmasks. Each row take every k==2 slot
as `#` until N are placed; if more rows are needed, also fill every k==1 slot
with `o` to keep the structure growing. ~7 us/clue, answers avg 52 chars.

## Evidence trail
- r1 (skip-only): 936 clues harvested; all clues distinct, no caching possible.
- r2: 32 naive formats (bare row, N, grids with N '#') -> 0/540.
- demos 1-3: `#` count above the clue row == N in every demo (4/4 with demo 4).
- Statistic scan found vertical pairs `oo` and `##` NEVER occur (v_oo=v_##=0).
- r3: grids with N '#' + no vertical repeats -> 0/481. Missing something.
- demo 4 (sparse) revealed: every non-`.` cell has a non-`.` cell below within
  +-1 column. Support rule.
- r4: sweep of support-respecting grids -> 2/490. The 2 winners plus the 4 demos
  tabulated cleanly as k -> symbol: k=1 -> `o`, k=2 -> `#`, k=0/3 -> `.`.
- r5: 477/477. r6: 438/438.
