# morvin — solved

Clue: `N/K`  (N = 3–5 decimal digits, K = 0..12, never equal to len(N))

## Rule
Render each digit d of N as a right-leaning triangle of 10 cells,
rows of 4/3/2/1, row r indented by r, blocks 4 wide separated by 2 spaces,
with the digit centred above its block (offset +1). Header line first.

* exactly **d** cells are `.`, the other 10-d are `o`
* a `.` is **floating** if it is NOT in the bottom row and has no `.`
  immediately beneath it — neither (r+1,c) nor (r+1,c+1)
* the picture must contain exactly **K** floating dots in total

Any placement satisfying both counts scores 1 (the reference solver itself
uses varied placements — two equal digits in one number look different).

## Achievable floating counts per digit
0:[0] 1:[0,1] 2:[0..2] 3:[0..3] 4:[0..4] 5:[0..5] 6:[0,1,2,3,4,6] 7:[0..4] 8:[0..3] 9:[0..2]
(note digit 6 cannot make exactly 5)

## Evidence
predicted score on all 487 labelled round-2 items: 0 mispredictions.
All 6 demos reproduce K exactly. Rounds 3–6 and the final: 100%.
