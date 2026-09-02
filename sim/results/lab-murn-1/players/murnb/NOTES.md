# murn — SOLVED

Clue: `<row>|<N>`  (row over alphabet `.o#`, width 9..16; N = 3..29)

Answer: a grid of newline-separated rows, all width W, whose **last row is the clue row**
and which contains exactly **N `#` in total**. Grid height is free.

Legality rule (necessary AND sufficient — verified 65 positives / 1041 negatives, zero errors):
for every cell above the bottom row, count the non-`.` cells among the three
directly below it (c-1, c, c+1, in-bounds):
  * `#` requires **exactly 2**   (a heavy block needs two support points)
  * `o` requires **exactly 1**   (a light block needs one)
  * `.` unconstrained

Consequences: above a clue run of length L>=2 only its two END columns have
support 2; a run of length 1 supports nothing. An adjacent pair of filled cells
is self-sustaining (2 `#` per level forever), so an unlimited number of `#`
can always be stacked.

Solver (strategy.py): level by level upward — place `#` on every support-2
column (or just the `rem` still needed), and if more are still needed make sure
the new row keeps an adjacent pair (adding an `o` on a support-1 column when
required). ~20 us/clue, 3032/3032 logged clues solved and locally validated.

Round history: 1 skip-only (data) | 2 0.6% | 3 2% | 4 26% (policy probe found the
rule) | 5 598/598 | 6 459/459.
