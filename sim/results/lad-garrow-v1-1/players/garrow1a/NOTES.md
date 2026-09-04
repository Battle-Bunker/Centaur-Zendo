# garrow — notes (team garrow1a)

## The class (single class in the pool: `garrow`)
Clue = `"<L1><n1><L2><n2>\n"` + a 6-line grid: 2 all-`#` border rows and 4 content
rows, each 32–38 chars wide, `#` at both ends, filled with 2-character dominoes
(`aa bb cc mm oo pp ss tt`) separated by dots. Every run of a letter is exactly 2
long. L1/L2 are always the two most frequent letters in the grid; n1,n2 ∈ 1..5.

Answer = the same grid with `|` inserted at chosen columns, i.e. a vertical
guillotine partition of the strip into pieces (bars in the border rows too).

## What was established
* Answer format confirmed by 5 reference demos; a valid answer must reproduce the
  grid exactly with bars inserted.
* The quantity the clue numbers track is **severed(L)** = number of L-dominoes a
  cut passes through. All 10 reference letter-instances satisfy severed(L) ≤ n_L;
  demos 1–4 had severed = n-1 for both letters, demo 5 had (n, n-1).
* Reference piece counts: 7,7,7,8,5; piece widths 3..10.
* Measured hit rates over 255 scored training answers (7 pieces, widths 3–7):
  severed == n : 6/21 = 29% ; severed == n-1 : 21/179 = 12% ;
  severed ≤ n-2 : 0/27 ; non-7 piece counts: 0/11.
* NOT the rule (all falsified against demos and/or ~255 labelled answers):
  intact == n, pieces-containing-L == n, cuts-severing-L (+1) == n, minimum
  total severance, most/least balanced widths, matching the reference's severed
  set, per-piece caps, empty-piece rules, clue-side predictors of the piece count.
  A linear fit over {sev, intact, tot, piecesIntact, npc, …} has NO solution over
  the 10 reference instances, so the residual constraint is positional and was
  not identified.

## Final strategy
Uniformly sample (exact DP counting + weighted descent) a partition with 6 cuts /
7 pieces, widths 3–7, severed(L1)=n1 and severed(L2)=n2; fall back to n-1, then to
6 or 8 pieces, then to any partition. ~0.5 ms/answer.

## Result
Final: 305 presented, 305 answered, **77 correct** (25.2%). Within the final,
severed==n scored 70/256 (27%) vs severed==n-1 7/48 (15%) — the arm choice was
worth ~35 points.
