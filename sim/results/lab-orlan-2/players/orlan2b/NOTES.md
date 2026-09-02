# orlan — notes

Single challenge class in the pool: `orlan`.

Clue: 5x5 / 5x6 / 6x5 / 6x6 grid of `.` `#` `o` `x`. Answer: `r,c>r,c` (row,col).

## Confirmed (48/48 observed correct answers, incl. 5 demos)
- source is always `o`, destination always `.`
- move is always orthogonal (uniform sample of diagonal moves: 0/21)
- destination is the **2nd empty cell** along the ray — occupied cells are
  transparent and do not count as steps. 1st-empty moves: 0/78.
  (Lines-of-Action-style "distance = pieces on the line" was refuted by demos 3 & 4.)

## Not cracked
Which of the ~8 candidates is wanted. Uniform choice ≈ 14%.
Weak but independently-supported preferences (uniform-sampled data):
- source NOT orthogonally adjacent to another `o`: correct 25% vs wrong 50%
- destination orthogonally adjacent to an `x`:     correct 75% vs wrong 20%
Lexicographic (lone, dst_x) → ~37% on held-out positives, 127/517 = 25% in the final.
