# NOTES — challenge class `velk` (the only class in the pool)

## Demo 1 (spent before round 0, because there is only one class)
clue: `XMFPE|2`
solution (score 1):
```
X M F P E
 /  | | |
M X F P E
| |  /  |
M X P F E
| | |  \
M X P E F
| |  \  |
M X E P F
 /  | | |
X M E P F
| | |  \
X M E F P
|  /  | |
X E M F P
 \  | | |
E X M F P
```

## Narrating it to a 12-year-old
"It's a ladder made of letters. The top rung is the word from the clue. Every
other line is the same five letters again, but two next-door letters have
traded places. Between the rungs there are little walls `|` where a letter
stands still, and one slanted stick `/` or `\` exactly where the two letters
swapped. So it's like five ropes hanging down, and now and then two ropes
cross over each other. At the very bottom the letters are in a new order."

### The three things a kid notices first
1. **The E walks all the way from the end to the front.** (E is at the right on
   the top line and at the left on the bottom line.)
2. **Some letters swap and then swap BACK** (X and M trade, then trade again;
   F and P too) — so those moves were pointless. A kid would say "they did some
   moves for nothing".
3. **The sticks lean two different ways, `/` and `\`,** and the leaning doesn't
   seem to follow any rule you can see.

### Kid-driven hypotheses (test these first)
* K1: the point is "get the smallest letter (E) to the front" — bottom row =
  clue with min moved to the front.  (Equivalent here to "rotate right by 1"
  because E happened to be last.)
* K2: the pointless swaps are decoration; only the top row, the bottom row and
  "each step swaps two neighbours" matter.
* K3: the `/` vs `\` lean is decoration too (a kid sees no rule; probably the
  server rolled a dice).

## What the number after `|` means — UNKNOWN
clue `XMFPE|2`, 8 crossings, 5 letters, bottom row = min-to-front.
Candidates: pairs that cross twice (=2 here); rotate amount (doesn't fit: the
rotation is 1); passes of a sort (only 1 pass happened); a seed.

## Plan
Round 1: cycle 11 target hypotheses x 2 lean styles, keyed on the challenge
index, to see which target rule scores.  Also harvest the clue distribution
(word lengths, values of N).

## SOLVED (rounds 5 and 6: 475/475 and 487/487)
Clue `WORD|N` (word 4-6 letters, N in 2..6).  Answer: the ladder picture.
Accepted construction: rotate the word RIGHT by k=2 with the minimal adjacent
swaps, then append q = N-2 repetitions of the four swaps [0,2,0,2] (which put
everything back).  Every crossing drawn as '\'.  100% in all 15 (L,N) cells.

Confidence: very high (677/677 scored answers with this family).
What the number N does: it fixes how many crossings the picture must contain
for a given permutation - with the rotate-right-2 shape the picture must have
exactly 2*(L-2) + 4*(N-2) crossings.  N is NOT the permutation and NOT simply
the number of crossings; the true underlying invariant was never pinned down
(no linear formula in (C, pairs, inversions, left-movers, fixed points) fits
all five demos plus my scored answers).
Dead ends: '/' instead of '\' scores 0 everywhere; padding at the front, or at
[1,3,1,3], or [2,0,2,0], or [0,0]-style padding all fail; rotate right by 1 or
by L-1 fails; block permutations with the "right" number of left-movers fail.
