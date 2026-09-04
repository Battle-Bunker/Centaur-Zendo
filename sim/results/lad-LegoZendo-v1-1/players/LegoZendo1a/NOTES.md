# LegoZendo — notes (team LegoZendo1a)

## The class
One class only: `LegoZendo`. Clue = `LETTER + NUMBER`, letter A–Z, number 0–12.
Answer = an ASCII "wall": rows of equal length, letters = brick colours, one
repeated filler char = empty. Bricks are 2x3 / 3x2 (6 cells); a region that
cannot be tiled by those (e.g. an isolated 3x3) makes the whole wall invalid
and every clue then scores 0.

Rule (working model, confidence high on behaviour, medium on semantics):
`Xn` = "a valid wall in which colour X has structural score n", where the score
is **additive over the separated same-colour regions**, is **independent of the
other colours**, and a lone "staircase pair" (two same-orientation bricks offset
by one column so they overlap by one) is worth exactly **1**.
Nothing I tried predicts every demo exactly (vertical same-orientation contacts
fit G2/X12/E3 but not I10/A5), so I stopped reverse-engineering the formula and
worked with measured, additive building blocks instead.

## What was measured
* n=0 is satisfied by any valid wall (23/23, 28/28) — a monochrome wall of
  isolated 2x3 bricks is enough. An empty wall is not.
* Grids of my own design never scored for n>=1 — stacked/aligned/offset/vertical
  brick pairs of a single colour all gave 0 (round 4: 32/408, all n=0).
* Recolouring a demo wall so the clue's letter takes the key colour's place
  preserves the value (round 5: n in {0,2,3,12} 103/103).
* Erasing every other colour, cropping, mirroring: value unchanged (round 6).
* Concatenating two walls adds their values (2+2=4, 2+3=5, 3+3=6: 100%).
* Deleting one region of the key colour subtracts that region's contribution
  (D1 2 -> 1, D2 12 -> 11, D4 10 -> 8).

## Final answer table (all verified in training except 7 and 9)
0 monochrome wall | 1 D1 minus G-region#2 | 2 D1 | 3 D3 | 4 D1+D1 | 5 D1+D3 |
6 D3/D3 stacked | 7 seven staircase units | 8 D4 minus I-region#2 |
9 nine staircase units | 10 D4 | 11 D2 minus X-region#4 | 12 D2.
All 338 (letter, n) answers precomputed in on_round_start; solve() is a dict
lookup (0.8 us).

## Result
Final: 1972 presented / 1972 answered / **1972 correct (100%)**.
