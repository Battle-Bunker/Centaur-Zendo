# LegoZendo — notebook

Only one challenge class: `LegoZendo`. Clue = one capital letter + a number 0..12
(e.g. `Q9`). Answer = an ASCII picture.

## Narrating the first demo to a 12-year-old
"It's a wall of coloured Lego, seen from the side, with holes in it. Every brick
is the same size — six studs — some lying down (3 across, 2 tall) and some
standing up (2 across, 3 tall). The letters are the colours."

The three things a kid notices first:
1. **Purple (`Q`) is everywhere** — way more of it than any other colour.
2. **Some bricks are lying down and some are standing up.**
3. **Bricks of the same colour bump into each other at the corners, like stairs.**

Kid-idea #1 ("count the purple ones") → tested and killed: Q had 25 bricks, but
the clue said 9. Kid-idea #3 ("stairs") turned out to be the whole rule.

## The rule (CONFIRMED, 100%)
`Xn` → the picture must contain exactly **n staircase joins of colour X**:
pairs of same-colour bricks with the **same orientation** that meet along
**exactly one cell edge** (offset by (±2, ±2)). Everything else is free —
grid size, background character, other colours, and every other kind of join
(stacked flush, offset by one, side by side, mixed orientation, corner-only).

Evidence: 3 demos (Q9→9, G3→3, X4→4) and 1221 scored answers, zero mismatches.

## How it was found
- R1: answered every clue with the demo grid. 23/294. The 13 clues that scored
  pinned the demo grid's hidden value for each letter: E0, Y0, **L1**, and Q9
  from the demo. E and Y are *in* the picture yet score 0 → not a colour count.
- R2: sent 26 hand-built probe grids, one configuration per clue letter
  (1 brick, k isolated bricks, stacked flush, offset 1, offset 2, side by side,
  mixed orientation, glued blocks, edge-touching, corner-touching...).
  Exactly one configuration had value 1: **two same-orientation bricks offset
  by (2,2)**. Everything else was 0.
- That single fact reproduced L=1, Q=9 in demo 1 and G=3 in demo 2 exactly.

## Solver
`n` well-separated staircase pairs of the clue colour (plus two lone filler
bricks of another colour), smallest grid that fits, all 26×31 answers
precomputed in `on_round_start`. ~0.23 µs per answer.
