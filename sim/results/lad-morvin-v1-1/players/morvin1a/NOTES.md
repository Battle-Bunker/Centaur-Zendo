# morvin — notes

Pool has exactly ONE class: `morvin`. Cooldown 5s, round 0.5s, 6 rounds, final 3s.

## Demo (window 0)
clue: `959/6`
solution:
```
 9     5     9
o...  ...o  ....
 ...   ooo   ...
  ..    ..    .o
   .     o     .
```
score 1.

### Structure decoded
- 3 blocks side by side, each 4 chars wide, separated by 2 spaces.
- Header line: digit at offset 1 of each block -> "9 5 9" == digits of the
  clue numerator 959.
- Each block is an upper-right triangle of 10 cells:
  row0 cols0-3, row1 cols1-3, row2 cols2-3, row3 col3 (T(4)=10).
- Cells are '.' or 'o'.  Counts:
  block1: 9 dots / 1 o   (header 9)
  block2: 5 dots / 5 o   (header 5)
  block3: 9 dots / 1 o   (header 9)
  => number of DOTS == the digit.  10 cells lets 0..9 be shown.
- The POSITIONS of the o's differ between the two '9' blocks
  (b1 o at reading-index 0; b3 o at reading-index 8), so placement looks
  random / not a function of the digit.  => grader probably counts dots
  rather than matching the string exactly.  (Guide: "some classes may
  accept more than one correct answer".)
- Unknown: what the `/6` does.  Header digits == numerator digits, so it is
  NOT a quotient (959//6=159) or remainder (5).  Hypotheses: seed for the o
  placement; a red herring; or it varies and drives something I can't see
  from one example.

## Round 1 plan — controlled experiment, 10 variants cycled by _index % 10
0 dots=d, o's first (reading order)      <- demo-replication, main hypothesis
1 dots=d first, o's at the end
2 o's=d (inverted meaning)
3 dots=d then SPACES (no o filler)
4 picture of N//k
5 picture of N%k
6 header line only
7 plain "N"
8 plain "N//k"
9 plain "N%k"
Also: record every clue seen so I can learn the clue grammar.

## RULE CRACKED (after round 1 + 2 demos)
Clue `N/k`.  Answer = the picture of N (header digits, one 10-cell upper-triangular
block per digit, `digit` dots and the rest 'o').  The o-placement is NOT free:

    k == sum over blocks of [ (# vertical pairs '.' directly above 'o')
                              + (1 if the block's top-left cell is '.') ]

Evidence: fits both demos and separates my 100 correctly-encoded round-1 answers
perfectly (13 true positives, 0 false positives, 0 false negatives, 87 true
negatives).  The 44 formula-satisfying rejects all encoded the WRONG digits
(variants that drew N//k, N%k, or used o-count instead of dot-count).
The value is additive per block, so precompute for each digit d and each
achievable t one block worth exactly t, then spend k greedily left to right.
Achievable t per digit: 0:0  1:0-1  2:0-2  3:0-3  4:0-4  5:0-5  6:0-5  7:0-4
8:0-3  9:0-2.  Every k in the 495 round-1 clues was reachable.

## Final rule (rounds 2-6)
`k == sum of per-block values` is NECESSARY but NOT sufficient: within a block,
only certain arrangements of a given value are accepted.  Block contributions
ADD across blocks (verified: 497/497, 320/320, 189/189 on library-only answers),
so I probed with answers that changed exactly ONE block (the rest canonical /
already-confirmed) — each result then attributes cleanly to that block.
That produced a library of server-confirmed (digit, value) -> arrangement.
Achievable values: 0:0  1:0-1  2:0-2  3:0-3  4:0-4  5:0-5  6:0-4  7:0-4
8:0-3  9:0,2 .  Confirmed impossible: (6,5) 0/59, (9,1) 0/45, and one-above-max
for every digit 0/501.  Residual 0.26% of clues need (6,5)-style values and are
skipped (skips are free and help the fewer-answers tiebreak).
Final solver = DP that splits k across blocks using only confirmed arrangements.
