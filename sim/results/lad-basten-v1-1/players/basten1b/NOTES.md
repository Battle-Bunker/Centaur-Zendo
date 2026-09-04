# NOTES — team basten1b — challenge pool: ["basten"] (ONE class only)

## Demo 1 (spent before round 0, because there is only one class and no reason to wait)

clue    : `.....3....3.....2.....3......2..../6`
solution:
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.<><........><>...................
.....|....|<><........|<><..<><...
.....|.><>|<><..|<><..|......|><>.
<><..|.<><|<><..|..><>|...<><|....
##################################
```

### Narrating the picture to my 12-year-old partner (plain words)
"It's a fish tank seen from the side. The squiggly line across the top is the
surface of the water. The row of hashes at the bottom is the gravel. Sticking up
out of the gravel are some straight tall weeds — the `|` sticks. And swimming
about in between are little fish: `<><` is one facing left, `><>` is one facing
right."

### The three things the kid noticed first
1. **"It's a fish tank."** Water on top (`~`), mud on the bottom (`#`), fish in between.
2. **"The numbers say where the weeds are and how tall they are."** The clue has
   digits at certain positions; the weeds stand in exactly those columns and are
   exactly that many squares tall, growing up from the gravel.
3. **"There are more fish the further down you go."** Top water row has 2 fish,
   next 3, next 4, bottom water row 5. Neat staircase 2,3,4,5.

The kid also said "the fish never sit on a weed" — true in the demo.

### What I verified myself (arithmetic)
- clue = `<column spec>/<height>`; height 6 = number of lines.
- width 34 = len(column spec) = width of every line.
- digits at columns 5,10,16,22,29 with values 3,3,2,3,2.
- weeds: column 5 has `|` on rows 2,3,4 (3 tall), col 16 has `|` on rows 3,4 (2
  tall). So a weed of height d occupies the d rows directly above the gravel row.
- row 0 = all `~`, row H-1 = all `#`, everything else `.` unless weed or fish.
- 14 fish total. Per water row top→bottom: 2,3,4,5.
- no trailing newline in the solution.

## Open question (the whole game, now)
Do the fish matter, and if so what is the rule?
Candidates:
 (K1 - kid's idea, test FIRST) fish count per water row = (row index from top)+1 → 2,3,4,5
 (K2) fish count = row index from top → 1,2,3,4
 (K3) fish are pure decoration; only water/gravel/weeds are checked
 (K4) orientation of the fish matters
 (K5) positions of the fish matter (they looked random)

## Plan
Only ONE class exists, so every challenge in a round is a `basten`. That means a
round is a free A/B test rig: cycle a different candidate answer per challenge
index and read off which variants score 1.

## After round 1 (4/464) and round 2 (2/467)
Demo 2 killed the "height = N" reading: clue `/2` but the picture is 8 rows.
Demo 3 (`.../4`) is 7 rows.  So across the three demos:
    N = 6 -> 6 rows ;  N = 4 -> 7 rows ;  N = 2 -> 8 rows
i.e. **rows = 9 - N//2** (equivalently: the free water above the tallest weed is
(8-N)/2 rows).  That is the only clean relation I can find, and it is exactly the
thing I got wrong in rounds 1 and 2 (I used rows = N).

The fish are plainly random in all three demos (per-row counts 2,3,4,5 /
3,2,4,4,4,4 / 2,1,3,6,1 — no pattern, no matching total, no matching
orientation split), so I now believe the checker does not care where the fish
go, only that the tank is the right size with the right weeds.

The 6 stray 1s I have scored contradict every rule I can write down, so round 3
also spends one bucket answering literal garbage ("x") to find out whether the
server ever awards a 1 by accident.  If garbage ever scores, my 6 "hits" were
noise and I should trust the demos alone.

## The kid's contribution this round
Shown demo 2 and demo 3 next to demo 1, the 12-year-old said straight away:
"the tanks are different heights" — which is the thing I had assumed was fixed
by the number after the slash. That single observation is what unlocked it.

## Result
Final: 190 correct out of 2576 answered in 3 s (rank 1 on the board; basten1a 185).

## Final understanding of `basten`
CONFIRMED (all three demos + 48 scoring answers):
* clue = `<column spec>/<N>`, width = len(spec).
* a digit d at column c is a seaweed stalk in column c, exactly d cells tall,
  growing up off the gravel.  Row 0 is all `~`, the bottom row all `#`.
* fish are `<><` and `><>` in the water; at least one blank column between them
  (touching fish score 0/57) and BOTH orientations must be present (all-left
  0/58 and all-right 0/58 against 6/58 for the same picture with a mixed crew).
* the height is NOT N: heights maxweed+3 and maxweed+4 score, maxweed+2 and
  maxweed+6 never do.
UNSOLVED: what `/N` means.  It is independent of the spec, it is not the height,
not the fish count, not any of ~350 statistics of the picture I tested against
32 scoring pictures.  Whatever it constrains, dense tanks satisfy it ~9% of the
time for N>=6 and almost never for N<=3.
