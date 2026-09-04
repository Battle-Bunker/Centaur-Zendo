# garrow — notes (team garrow1a)

Pool has exactly ONE class: `garrow`.

## Clue / answer format (certain)
```
b2c2                                  <- head: L1 d1 L2 d2, digits 1..3
##################################    <- 6 rows, W = 28..34, '#' border
#..aa....bb...............cc..bb.#    <- 4 interior rows
... 4 rows of two-cell tokens (aa,bb,cc,mm,oo,pp,ss,tt); every letter run is
    exactly 2 cells; 16-20 tokens per grid; exactly 4 distinct letters per grid;
    the two head letters are always among them.
```
Answer = the same 6 rows with vertical `|` cuts inserted at the same columns in
every row, splitting the grid into column pieces. Verified on both demos.

## What is established (from 2 demos + 6 rounds + final = ~3600 scored answers)
* A token counts for a piece if **any of its two cells** lies in the piece
  (a token cut by a `|` counts for BOTH sides). Left-cell / right-cell / fully-
  contained conventions all contradict at least one demo.
* An answer with **no piece holding exactly d1 of L1 and d2 of L2** scores ~6-12%;
  an answer with such a piece scores ~29%. So it is necessary-ish, not sufficient.
* **2- and 3-piece answers never score** (0/310). 4 pieces is best, 5 close behind,
  6+ worse.
* The narrower the matching piece, the better: width 3 -> 37%, width 8 -> 25%,
  width 12+ -> ~17%. Min piece width >= 5 anywhere is fatal (~1%).
* Difficulty is clue-driven: d1+d2 = 3 -> 43% correct, = 6 -> 7%.
* Actively unhelpful: preferring a matching piece that holds ONLY the two clue
  letters (24% vs 27%); preferring cuts that do not slice an L1/L2 token
  (14% vs 27%) — so slicing tokens at the piece edges is fine/good.
* Content targeting alone is worth little: in round 3, purely RANDOM 4-piece cuts
  scored 9.5% vs 5-13% for content-targeted 2-4 piece cuts. Geometry (4 pieces,
  narrow matching piece, one big remainder) is what moved the number.

## Ruled out (tested against 1640-3600 labelled answers, precision never > 0.43)
exists/all-pieces variants of: exactly / at-most / at-least d of L per piece;
counting by cells, by rows, by intact tokens; "two rarest letters of a piece
describe it"; number of pieces = f(d1,d2,n1,n2,W,ntok); unique dominant letter
per piece; system of distinct representatives; cut-splits-exactly-d-tokens;
the matching piece being the widest / narrowest / most-token piece.

## Final policy
Narrowest window (width >= 3) whose overlap counts are exactly (d1,d2); make it
one piece; fill the rest with 3-wide pieces plus one big remainder, 4 pieces
total; fall back to a window matching one letter; never crash; 0.03 ms/clue.

## Results
round 1  skip-all data collection      0/0     (423 clues harvested)
round 2  first content model          26/344   7.6%
round 3  ablation (random vs targeted) 17/295  random 9.5%, targeted 5-8%
round 4  shape ablation               61/329   4 pieces + narrow fillers 27.5%
round 5  narrow-target ablation       81/331   narrowest w>=3, n=4 -> 33%
round 6  refinement ablation          68/339   control 27%, refinements worse
FINAL                                551/1955  28.2%
