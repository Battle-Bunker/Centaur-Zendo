# orlan — notes

Pool: a single challenge class, `orlan`.

## What the clue is
A rectangular grid (5x5, 5x6, 6x5, 6x6) of `.` `o` `x` `#`.
Generator stats over 707 clues: 3-4 `o`, 2-4 `x`, 1-10 `#`, no clue ever repeats.

## What an answer is (confirmed)
`r,c>r2,c2` — 0-based (row, col). Source is ALWAYS an `o`, destination ALWAYS a `.`,
and they ALWAYS share a row or a column. The path may be blocked (demo 4 moved
(5,4)->(1,4) straight through a `#`), so it is not a rook slide — it is
"pick an o, put it on any empty cell in its own row or column".
Mean 23.7 such moves per grid; exactly ONE scores 1 (uniform random = 4.2%, measured 4-6%).

## The underlying rule: NOT cracked
Exhaustively searched ~150 hand features (neighbourhood composition, line-of-sight
/attack graphs under 4 blocking rules, pairwise distance histograms, connectivity,
coverage predicates, collinearity, row/col occupancy, symmetry, dead-ends,
lexicographic board order). No single feature, feature pair, or necessary condition
separates the correct move. Best necessary condition had selectivity 0.90 — useless.

## What worked instead: a learned ranker
45 cheap per-move features (after-state), z-scored within each grid, scored by a
margin-averaged ranking perceptron trained on harvested (grid, correct move) pairs.
Positives came from demos + every answer that scored 1 in training rounds.
Accuracy scales strongly with the number of positives:
  26 pos  -> 17.6% live
  55 pos  -> 28.2% live
 101 pos  -> 33.0% live
 172 pos  -> 28.6% live (final, 1357 items)
Cost 0.62 ms/challenge, which still allowed ~450 challenges/second.
