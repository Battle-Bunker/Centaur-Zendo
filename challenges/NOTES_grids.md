# Brainstorm — grids, mazes & spatial puzzles (grids-agent)

Twelve candidates. `verify` = what the 256-char scorer has to do.

1. **warren** — ASCII perfect maze, `#`/`.`/`S`/`E`, rows newline-joined. Solution = move string `UDLR`.
   verify: walk from `S` in the flat clue string using stride `w=index('\n')+1`; newlines act as walls so no
   wrap check is needed; score 1 iff every step is legal and we land on `E`. Fun: instantly readable, huge
   partial-progress gradient (wrong letter alphabet vs wrong direction convention vs off-by-one). PICKED (easy).
2. **skerry** — grid of `#`/`.`; answer = number of 4-connected islands (decimal).
   verify: generator guarantees the `#` set is a *forest* (never place a cell with >=2 `#` neighbours), so
   components = V - E, which is two `sum(...)` comprehensions. Classic "count the islands". PICKED (easy).
3. **volute** — grid of letters; answer = the letters read in a clockwise inward spiral.
   verify: recompute the spiral with the peel-and-rotate one-liner `g=[''.join(x)for x in zip(*g[1:])][::-1]`.
   Rule space (row-major / column-major / boustrophedon / diagonal / spiral CW-CCW / outward) gives real
   hypothesis testing; one demo pins it. PICKED (medium).
4. **regina** — n x n board (n=6..8) with `X` blocked cells; answer = n digits, digit i = row of the queen in
   column i. verify: three `len(set(...))==n` checks (rows, both diagonals) + blocked-cell lookup. PICKED (medium).
5. **hanjie** — nonogram: clue is `rowruns\ncolruns` (`/` between lines, `,` between runs); answer = the grid.
   verify: recompute run lengths from the answer with `re.findall('#+',row)` for rows and `zip(*g)` for columns
   and string-compare to the clue. Perfect verify-easy/find-hard. PICKED (hard).
6. **erewhon** — Conway's Life *predecessor*: clue = 6x6 target, answer = a 6x6 grid that steps to it.
   verify: apply one Life step to the answer and compare to the clue (8 offsets, newline-safe). Genuinely hard
   to find (row DP over 2^6 masks), trivial to check. Name reads backwards. PICKED (hard).
7. **minesweeper reconstruct** — clue = grid of digits and `?`; answer = same grid with `?` filled as `.`/`*`
   consistent with every digit. verify ~= 265 chars (shape check + 8-neighbour count). REJECTED: 10 chars over
   cap once the "only `?` cells may change" guard is included. Would be a great 300-char challenge.
8. **lights out** — 0/1 grid, answer = press list `rcrcrc...`; verify toggles a mutable copy. ~250 chars but needs
   a digit guard and a mutable board; overlaps `erewhon` thematically (binary grid + neighbourhood). Rejected.
9. **8-puzzle** — 3x3 tiles, answer = blank-move string; verify simulates. Fits (~230) but the "walk a move string"
   idea is already spent by `warren`, and the answer is a search problem rather than a spatial one. Rejected.
10. **knight's tour** — n x n, answer = `rcrcrc...` cell list; verify: all cells once, each step a (1,2) jump,
    in bounds, correct start. ~270 chars with the bounds guard. REJECTED on the cap (see report).
11. **Manhattan meeting point** — grid with `*` marks, answer = a cell minimising total Manhattan distance;
    verify must itself minimise over all cells (~200 chars, fine) but it is a pure-arithmetic task that the
    numbers agent covers better. Rejected for overlap.
12. **line of sight / guard post** — grid with walls, answer = a cell that sees every floor cell. Verification is
    ray casting over all pairs; no chance in 256 chars and >50 ms. Rejected.

Also considered and dropped: polyomino exact cover (piece list + board would need a full cover checker plus a
piece-shape parser, ~400 chars), shortest-path-with-length-bound (same scorer as `warren` plus `len(s)<=k`, but
0/1 feedback gives almost no gradient between "walked a legal path" and "walked the shortest one"), and
flood-fill-area-of-region (verification = the whole solve, and unlike `skerry` there is no V-E shortcut).
