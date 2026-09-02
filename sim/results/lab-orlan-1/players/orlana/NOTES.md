# orlan — notes

Pool has ONE class: `orlan`.

## Clue / answer format
Clue = rectangular grid (5x5..6x6 seen) of `.` empty, `#` wall, `x`, `o`.
Answer = `r,c>r,c` (0-indexed row,col; from > to).

## Established facts (from 281 confirmed-correct examples)
1. Source is always an `o`; destination is always `.`.
2. The move is always a **hop**: from the o, travel in one of the 4 orthogonal
   directions and land on the FIRST empty cell (may pass over `#`, `x`, `o`).
   Confirmed: random hops score 9.0%, = 1/(avg 11.2 hops) -> exactly ONE
   correct move per grid.
3. Destination ALWAYS shares a row or column with some `x`, at line-distance
   <= 3 (0/387 violations). Line need not be clear.
4. Correct moves never increase total x mobility.
5. No simple predicate/argmax selects the right hop among the ~4.6 that pass
   (3): tested captures (custodian, checkers-jump, wall/edge hostile),
   connectivity, lines-of-3, trapping, blocking, mobility, chase/flee.
   Underlying rule NOT identified — likely a planted-unique-solution puzzle
   whose criterion I could not name.

## Working solver
Filter hops by (3), score each with a linear model over 37 hand features,
answer the argmax. Trained by softmax (structured) regression on all confirmed
correct moves. 0.34 ms/challenge.

Measured live accuracy: random hop 9.0% -> aligned-random 13.5% -> model(67
examples) 31.8% / 37.4% -> model(204 examples) 39.5%. Final uses 281 examples.

Failed experiments: bucketed one-hot features + bandit loss on wrong answers
(21.5% in A/B, worse than plain).
