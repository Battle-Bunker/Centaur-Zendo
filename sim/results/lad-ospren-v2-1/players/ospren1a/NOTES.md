# ospren1a — working notes

## Shape of the pool
7 classes. 6 of them are "rule-family" classes: 2-4 positive examples, a blank line,
then 4 candidates; exactly one candidate obeys the hidden rule, and the rule is
DIFFERENT for every clue (drawn from a per-class family). fennick is a picture class.

Answer format (confirmed by demo + round 2):
* borsel/dornic/tavrik/tresk/wisbek -> the candidate line, verbatim.
* ospren -> candidates are numbered; BOTH "3" and the raw 5x5 grid score 1 (tested by
  alternating on memory['_index'] in round 2: index 15/16, grid 21/21).
* fennick -> the whole picture (grid + '=' rule + "N fall" line) with the edit applied.

## Solver
Generic engine: enumerate simple predicates (feature==value) over a per-class feature
bank; keep those true for ALL positives and true for EXACTLY ONE candidate; rank by
surprise -log P(observation | base rate) with base rates estimated from every clue seen
so far; answer the argmax. Feature banks per class in strategy.py.

fennick (cracked without guessing): each column is a tree of h identical letters with a
'_' cap one cell above it; '.' on the ground row = empty column. For every gap exactly
ONE column wide whose two neighbours are both trees of DIFFERENT heights, the shorter
neighbour topples into the gap — but only if its far side is also a tree. Everything
above the ground row shifts one column into the gap and the '_' cap becomes '\' (fell
left) or '/' (fell right). Validated: predicted "N fall" exactly on all 49 round-1
clues, and reproduced the demo byte-for-byte. 100% in every round.

## Demos (3 used)
1. fennick — clue format unreadable, 16% of the pool. Paid off: 100% thereafter.
2. dornic — settled the answer format for all five text classes, and gave one worked
   rule ("hand contains no queen").
3. borsel — the weakest class; one extra worked example ("contains a 4").
Deliberately NOT demoed: tavrik, tresk, wisbek, ospren — all four were probeable from
the clue alone and ended 82-89%.

## Round log
r1 skip-everything (306 clue formats harvested, 0 answers)
r2 79.8%  r3 83.9% (borsel A/B on feature bank)  r4 80.7% (A/B on learned key weights)
final 1155/1433 = 80.6%
