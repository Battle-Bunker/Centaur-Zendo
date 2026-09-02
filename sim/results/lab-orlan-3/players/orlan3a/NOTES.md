# orlan — notes

Pool has exactly ONE class: `orlan`.

## Clue / answer format (confidence: certain)
Clue = a 5x5..6x6 ASCII grid of `.` `#` `o` `x` (rows joined by `\n`).
Answer = `r1,c1>r2,c2`, 0-indexed **(row, col)** — proved because demo 1 used
row index 5 on a 5-column grid.
`(r1,c1)` is always an `o`; `(r2,c2)` is always a `.`. Reads as "move this o here".

## Confirmed constraints on the correct move (66 confirmed-correct examples)
1. Straight orthogonal line (never diagonal; 0/12 diagonal answers scored).  certain
2. No `o` between source and destination; `#` and `x` MAY be crossed
   (so it is NOT a slide/gravity/line-of-sight move).                        high
3. Destination is within **Manhattan distance 2 of an `x`** — 66/66, base
   rate 54%.                                                                 high
4. Exactly ONE move per grid is correct (~21 legal line-moves per grid;
   a uniformly random legal move scored 7%, matching 1/candidates).          high

## Not the rule (tested and rejected)
gravity / sliding, custodial (Tafl) capture, Othello flips, checkers jumps,
Lines-of-Action step counts, path connectivity, board-global invariants
(o-adjacency, distinct rows/cols, o/x balance), distance == count-of-X.
No conjunction or 2/3-key lexicographic ordering over ~35 features separates
the truth from the other ~20 legal moves — the selection rule was not found.

## Best heuristic shipped (measured 24% in the final)
candidates = straight moves o -> '.', not through an `o`, dest within
Manhattan 2 of an `x`; rank by (most `x` exactly 2 away in a straight line,
fewest adjacent `o`, reading order).  ~0.025 ms per challenge.

## Demos used (6)
All on `orlan` (only class). Each is a guaranteed-correct example — the
cheapest source of ground truth in the game.
