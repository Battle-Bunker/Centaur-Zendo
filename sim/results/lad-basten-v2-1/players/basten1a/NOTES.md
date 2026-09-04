# basten — running notes

## Clue / answer format (confident)
clue = `<seabed line>/<N>`; seabed is dots with digits 1-3.
answer = ASCII aquarium, W = len(seabed):
  row 0      : '~' * W          (water surface)
  rows 1..H  : water, '.' background, seaweed '|' growing UP from the floor,
               stem at each digit column, height = the digit
  last row   : '#' * W          (gravel)
  fish '><>' (right) / '<><' (left) swim in the water rows.
Confirmed by 2 demos + ~2500 scored answers.

## What N means — UNSOLVED
* N is statistically independent of the seabed, except N != (number of stems).
* N is NOT the fish count: demo1 N=4 -> 7 fish, demo2 N=6 -> 8 fish, and
  "exactly N fish" scored 0/240 across rounds.
* No measured statistic equals N on every scoring answer: fish per row, top-row
  fish, fish adjacent to stems, stems with a fish, blobs, gaps with fish,
  rows with fish, chars, mod-arithmetic — all searched, all rejected.
* Tank height is not fixed: demos used maxh+2 and maxh+1; both score.

## What the scores do say
* Height must be >= maxh+1 (H = maxh scored 0/43); H = maxh+1 or +2 both work.
* Fish are required: an empty tank scored 0/53.
* Fish must be allowed next to stems: forbidding stem-adjacent fish scored
  0/160 (rounds 4 and 5 V3) while every other layout scored ~20%.
* Otherwise acceptance looks like a ~20-30% coin flip per item, tilted by N:
  few fish per row is better for small N, a packed tank better for N = 6-7.

## Round log
r1 probes (data only) 0/637 | r2 factorial H x fish 9/587 | r3 what-does-N-do
53/600 | r4 fish barred from stems 0/635 | r5 placement isolation 113/637
| r6 exactly-N hugging stems 43/464.

## Final config
H = maxh+1 (N=2,4,8) or maxh+2 (N=3,5); N fish per row, evenly spread;
N=6,7: pack every free slot. ~30% expected.
