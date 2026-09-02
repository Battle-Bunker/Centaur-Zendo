# NOTES — class `orlan` (the only class in the pool)

## Demo (taken before round 0)
clue (6x6 grid):
```
...o.x
.#..x.
#..o..
.....o
xx###.
.ooo#.
```
solution: `5,3>5,0`  score 1

## Reading
Coordinates must be `col,row` (x,y), origin top-left:
 - (5,3)=col5,row3='o'; (5,0)=col5,row0='x'; path (5,2),(5,1) empty. Clean rook move up, capturing an x.
 - Under row,col it would be row5col3='o' -> row5col0='.', but path blocked by two o's. So col,row it is.

## Hypothesis H1 (confidence: high on mechanics, medium on selection)
Rook-style move by an `o` along a row/column over `.` cells, landing on an `x` (capture).
`#` = wall. Answer format `c1,r1>c2,r2`.

Candidate captures in the demo grid: (3,0)>(5,0) d=2, (5,3)>(5,0) d=3, (1,5)>(1,4) d=1.
Demo chose the LONGEST (d=3). So either
  (a) any capture is accepted -> max-distance also works, or
  (b) the longest capture is required -> max-distance is required.
Either way MAX DISTANCE is the safe pick.

## Round 1 plan
Cycle 3 variants by index%3 to discriminate:
 0 -> max-distance capture
 1 -> first capture in reading order of source
 2 -> min-distance capture

## After round 1 (1/176) + demo 2
Demo2 clue 5 rows x 6 cols, solution `3,1>3,5` -> second component reaches 5,
which only exists as a COLUMN. So the format is **row,col>row,col**.

All three known-correct answers:
 d1 `5,3>5,0` grid r5=`.ooo#.`  S=(5,3)'o' T=(5,0)'.'
 d2 `3,1>3,5` grid r3=`oo#.o.`  S=(3,1)'o' T=(3,5)'.'
 r1 `0,4>0,3` grid r0=`.o..o`   S=(0,4)'o' T=(0,3)'.'
=> source is always 'o', target always '.', always the SAME ROW.
=> the chosen row is always the row with the MOST 'o's (unique max in all 3).
Path is NOT clear in d1 (o's between) or d2 ('#' between) -> not a slide/rook move.

Unknown: which o in that row, and which empty cell.
Round 2 = uniform sampling experiment to harvest positives.

## Final state of knowledge (after 6 rounds, 6 demos)
CERTAIN (66 correct answers agree, 6 of them from unbiased demos):
 * clue = grid of '.', '#', 'o', 'x'; answer = "r1,c1>r2,c2", 0-indexed ROW,COL.
 * (r1,c1) always holds 'o'; (r2,c2) always holds '.'; they always share a row
   or a column (19/20 row, occasionally column).  The path between them may be
   blocked by anything - it is not a slide/rook/jump move.
 * ~23 such (o, empty) pairs exist per grid and essentially exactly one is
   accepted (uniform guessing scores 1/23 ~ 4.3%, measured 3.7-5%).
UNKNOWN: which pair.  Ruled out by experiment or by exhaustive search over
 ~55 features / 3600 lexicographic rules / 28 after-state goal predicates:
   - row/line with most o's (looked perfect on 20 biased positives; a controlled
     round showed ZERO lift -> it was pure sampling bias)
   - max/min move distance, clear path, spread, contiguity, 3-in-a-row,
     custodial capture, reversi flanking, column balancing, symmetry,
     connectivity, "T is an extreme empty", peg-solitaire jumps, LOA distance.
BEST AVAILABLE: an 8-feature conditional-logit ranker over the candidate pairs
 (T near the border, T near an x, S near another o, o-count of T's row, ...).
 Measured live: 10.2% over 246 answers (vs 4% random).  That is what the final ran.
