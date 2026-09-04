# NOTES — team basten1b, class `basten` (the only class in the pool)

## The one demo (spent immediately, window 0)

clue    : `...2.......3...3.....2......./7`
solution:
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.............................
<><.............<><..........
.................><>.........
........<><|><>|.............
><>|....><>|...|<><..|<><....
...|....><>|><>|.....|.......
#############################
```
score 1.

Measurements (done by hand before any theorising):
* clue before the `/` is 29 characters. Every solution line is 29 characters. -> width
* solution is 8 lines. depth number is 7. -> lines = depth + 1
* digits sit at columns 3, 11, 15, 21 with values 2, 3, 3, 2.
* `|` appears at exactly columns 3, 11, 15, 21 — nowhere else.
  * col 3  : rows 5,6      (2 cells) = digit 2
  * col 11 : rows 4,5,6    (3 cells) = digit 3
  * col 15 : rows 4,5,6    (3 cells) = digit 3
  * col 21 : rows 5,6      (2 cells) = digit 2
  Every bar column touches row 6, the row just above the `#` row.
* 11 fish: `<><` at (2,0) (2,16) (4,8) (5,16) (5,22); `><>` at (3,17) (4,12) (5,0) (5,8) (6,8) (6,12).
  11 is not 7, not 4, not the digit sum (10). Nothing in the clue predicts 11.

## TEN HYPOTHESES, phrased for a 12-year-old (written before any probing)

1. It is a picture of a river seen from the side, like a cross-section of a fish tank.
2. The top line of squiggles `~` is the surface of the water and the bottom line of
   `#` is the muddy riverbed. Both are as wide as the clue is long.
3. Every digit in the clue is a reed (water weed). It grows in that column, straight
   up out of the mud, and the digit says how many squares tall it is. It is drawn `|`.
4. A dot in the clue means nothing grows in that column — just water.
5. The number after the slash is how deep the river is: that many rows of water
   (counting the wavy surface row), and then one row of mud underneath. So the whole
   picture is depth + 1 lines tall.
6. The fish are only decoration. You can draw the river with no fish at all and still
   be right, because nothing in the clue says how many fish there should be.
7. Or the opposite: the fish are the point and `/7` is really about fish somehow, and
   the reeds are the decoration. (Against it: 11 fish, and the bars match the digits
   perfectly, so the reeds are clearly the thing the clue is describing.)
8. Fish never sit on top of a reed — no square is both `|` and part of a fish — so if
   fish are checked at all they have to squeeze into the gaps between the reeds.
9. Fish never sit on the wavy surface row or in the mud; they only swim in between.
10. The answer is a picture with real newlines in it, not a number and not JSON —
    the demo answer is a drawing, so a drawing is what is wanted.

Extra: reeds are drawn bottom-up, resting on the mud, never hanging from the surface.

## WHAT ROUND 1 IS FOR (probe to discriminate, not to score)

Only hypotheses 5 (exact line count) and 6 (are fish required?) are still open;
everything else is nailed down by the demo. So round 1 cycles 8 renderings by
challenge index and I read off which ones scored 1:

  v0 base: depth+1 lines, `~` top, `#` bottom, reeds resting on mud, no fish
  v1 depth+2 lines            (line-count off-by-one up)
  v2 depth lines              (line-count off-by-one down)
  v3 base + trailing newline
  v4 base but reeds hang from the surface instead of growing from the mud
  v5 no `~` surface row
  v6 base + fish drawn in the gaps
  v7 no `#` mud row

## RUNNING LOG
(round results appended below)

## After rounds 1-3 + three demos

Demos (clue -> lines, reeds, fish):
1. `...2.......3...3.....2......./7`      8 lines, 4 reeds, 11 fish
2. `...2...2.........2....2......3...../2` 8 lines, 5 reeds,  6 fish
3. `...2....2....3........3...../2`        7 lines, 4 reeds,  6 fish

* mask = one column each; digit = reed of that height growing up off the bed, drawn `|`.
* width = len(mask). Reeds ALWAYS rest on the `#` row. `~` on top.
* **fish = N + 4 in all three demos** (11=7+4, 6=2+4, 6=2+4).
* the picture HEIGHT is not N+1 and is not constant: 8, 8, 7 for the same kind of clue.
* round1 (no fish at all)         : 0/702  -> fish are required
* round2 (height N+1, fish swept) : 37/488, only ever at N=5,6,7 i.e. heights 6,7,8
* round3 (height 8, fish swept)   : 67/566, ~20% whenever fish >= N+2, ~3% otherwise
  -> two conditions: enough fish (>= N+2) AND the height has to be the right one.
  Round2 is explained too: heights 3,4,5 and 9 never scored, 6/7/8 did.
* Round 4 pins the height: fish fixed at N+4 (the reference count), height swept 5..9.


## FINAL
final: 2867 presented, 2867 answered, 1194 correct (41.6%). Rank 1 of 2.
By N: 2->77%, 3->55%, 4->36%, 5->63%, 6->30%, 7->8%, 8->21%.

Final rule as I understand it:
  clue "mask/N": width = len(mask); picture is 8 lines (6/7/8 all accepted,
  5 and 9 never); row0 all '~', last row all '#'; each digit = a reed of that
  height standing on the bed, drawn '|'.  Fish '><>'/'<><' swim in the water,
  never overlapping a reed.  The scored quantity is how many fish stand right
  beside a reed: it must be at least N (0 hits in 499 counter-examples below N)
  and the sweet spot is N+2 for small N, higher for big N -- my count of
  "beside a reed" is clearly a bit coarser than the checker's, which is why
  the tuned offset drifts up and why large N stayed hard.
