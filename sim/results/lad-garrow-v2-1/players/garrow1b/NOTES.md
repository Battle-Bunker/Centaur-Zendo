# NOTES — class `garrow` (the only class in the pool)  — SOLVED

## The rule (confidence: certain — 1956/1956 in the final)
Clue = header `L1n1L2n2` (letters from a,b,c,m,o,p,s,t; counts 1-3) then a
walled field (28-34 wide, 4 inner rows) holding 16-20 animals, each drawn as a
two-cell doubled letter (`tt`, `oo`, ...).

Answer = the SAME grid (no header line) with vertical fences `|` inserted at
identical column gaps in every row, border rows included. Pure insertion.

An answer scores 1 iff all three hold:
 1. for each `(L, n)` in the header, exactly `n` pens hold **2 or more**
    L-animals, where an animal counts for **every pen it touches** (a fence may
    cut an animal in half; then it counts for both pens);
 2. the number of pens is between **4 and 8** inclusive;
 3. **no pen is empty** — every pen is touched by at least one animal.
Nothing else matters: fences may split animals, pens may be any width, other
letters are unconstrained, and many answers per clue are accepted.

## How it was found
- 5 demos gave clue+correct-answer pairs. A scan of ~60 candidate statistics
  over those 10 (letter, count) constraints found exactly one match:
  "#pens containing >=2 L, touch-counting" == n.
- That rule alone was necessary but not sufficient (plain no-fence answers that
  satisfied it scored 0 in round 1), so round 5 played 8 differently-shaped
  rule-satisfying partitions; cross-tabulating 272 scored answers gave a clean
  separation: rule AND 4<=pens<=8 AND no empty pen -> 108/108; anything else
  -> 0/164.

## Solver
`garrow_core.solve` — DFS over pen boundaries with a dead-state memo, prefix
sums for the touch counts, monotone pruning. 0.13 ms/clue, solves 100% of the
1878 logged clues with a minimum pen width of 3.
