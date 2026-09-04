# NOTES — crandel1b

Pool (round-1 counts): Wordz 98, kelmar 88, crandel 84, virel 82, quaich 80, LegoZendo 67, fennick 66.
Round 1: 564 presented, 424 answered, 0 correct (cheap probes: clue, reversed clue, "", "0", "1", "yes", skip).

## Ten hypotheses written from the clues alone (12-year-old phrasing)

1. **Wordz `4423`** — "The numbers are how long each word is. Send back that many real
   words, in order, with those lengths." (4-letter, 4-letter, 2-letter, 3-letter.)
2. **Wordz** alt — "It's one long word chopped up; give the word whose pieces are those sizes."
3. **LegoZendo `A6`** — "A letter and how many steps to slide it along the alphabet: A slid 6 is G."
4. **LegoZendo** alt — "A brick labelled A with 6 studs: write A six times."
5. **LegoZendo** alt2 — "Square A6 on a board: draw the grid and put a mark there."
6. **quaich `RRGRGGBBGRRB`** — "A line of coloured beads. Squash them together two at a time:
   two the same make that colour, two different make the third. Say the colour you end with."
7. **quaich** alt — "Tidy the row: say how many of each colour / which colour wins."
8. **kelmar `___*__Y__*.../ *3Y1`** — "A path with lamp-posts (*) and trees (Y). The end says
   how many of each you want. Point at the shortest bit of path with exactly that many."
9. **fennick `DM.D.MM../N:1 T:2 U:1 M:1`** — "Bags of letters separated by dots (a dot is a new
   bag). Pick some bags so you end up with exactly 1 N, 2 T, 1 U, 1 M."
10. **crandel `343/433/3` and virel `3545/6`** — "Some things described by numbers, then how many
    of something you must make/choose from them." (crandel groups are always 3 digits with ranges
    a in 2..6, b in 2..4, c in 0..4, so a group is a *thing with three measurements*, not a colour.)

## Facts measured from round 1
- Wordz: digits 1..7, 3..6 digits.
- crandel: 2 or 3 groups of exactly 3 digits + a final number 2..6. Positional digit ranges
  pos0 2..6, pos1 2..4, pos2 0..4.
- virel: 3..6 digits, each 2..6, then a number 1..10. No simple function of the digits
  (inversions, distinct, sum, max-min, ...) reproduces the number — so it is a *target*, not a fact.
- kelmar: track of `_ * Y` (length 42..51) then `/ *a Y b` with a,b in 1..3; real counts of * and Y
  in the track are 4..7, so the legend is a *request*, not a description.
- fennick: track of letters+dots (len ~35..38), then 4 letters with values 0..2. The letters named
  are 4 of the ~6 letters present; a 0 means "none of these".
- LegoZendo: one letter A..Z + number 0..12.
- quaich: R/G/B string, even length 12..18.

## Demo plan
Opaque and un-probeable: crandel, virel, fennick, kelmar (4 classes, 3 demos).
kelmar and fennick look like the *same family* (track + legend); crandel and virel look like
another family (numbers + /target). So buy one demo per family first and try to transfer:
  demo 1 = kelmar  (same family as fennick, and the most frequent of the four)
  demo 2 = virel or crandel (decide after seeing kelmar)
  demo 3 = held back until after round 2, spent on whichever family failed to transfer.
Wordz / LegoZendo / quaich are left without a demo on purpose: their answer *shape* is readable
off the clue, so they can be cracked by probing many cheap candidate answers in one round
(each class appears ~80 times per round, so ~15 hypotheses x ~5 samples each).

## Round 2 result: 0 correct out of 378 answered (645 presented)
15-16 candidate formats each for Wordz / LegoZendo / quaich / virel, ~5 samples each: nothing scored.
Combined with the three demos (all of which returned multi-line ASCII pictures), the working
conclusion is that **every class in this pool wants a drawing**, not a word/number/string.

### Demo 1 — kelmar  `__Y____*__Y__Y___________*___Y_____*__Y__*__*____/*1Y1`
```
###   ####                   #####  #######
|||   ||||                   |||||  |||||||
|||   ||||                   |||||  |||||||
<the track, unchanged, as the ground line>
```
Houses (roof `#`, walls `|`, 3 rows tall) at columns [0-2] w3, [6-9] w4, [29-33] w5, [36-42] w7.
Marks: `*` at 7,25,35,41,44 and `Y` at 2,10,13,29,38. I could not find the placement rule:
widths are 3,4,5,7 (strictly increasing), each house covers exactly one mark except the last
(which covers a Y and a `*`), and they match neither the gaps nor any window with the legend's counts.

### Demo 2 — fennick `RRB.AJ.WA.PPR..B..PAB.P.RJ.BB..WRP.PP/B:1 P:2 A:1 J:1`
A bar chart: the track is the second-to-last line, a `=====` rule is the last line, and every one
of the 24 letters gets a 1-wide bar above it filled with its own letter, topped by `_`, or by `/`
when the next bar is taller and `\` when the previous one is. Bar heights (in track order) are
4,3,2,1,3,4,4,2,4,2,3,2,3,2,3,4,3,3,3,4,3,1,3,1 — the first segment `RRB` fits "1 + letters left
in this segment" but later ones do not, and five bars are drawn one column off (into a neighbouring
`.`), which I could not explain.

### Demo 3 — crandel `432/333/5`
Three shelves separated by ruler lines of `=` with `v` at the first and last column of every block;
blocks are letter-filled rectangles on a `.` background. Shelf heights 4, 3, 5 = the maximum digit
of each of the three clue fields. Canvas 28 wide, 14 blocks of sizes 2..6 wide and 2..5 tall, with
arbitrary-looking letters D/V/S/P — which suggests the checker *parses* the picture rather than
string-matching it, i.e. many drawings score 1. Packing rule not recovered.

## Round 4: 1 correct out of 445 — quaich cracked (partly)
The hit was hypothesis "counts bar chart": three columns R, G, B, each bar drawn with its own
letter, `.` for empty cells, `===` baseline. Two other samples of the same shape failed; the one
that scored was the one where the tallest bar reached len(clue)//2 exactly. Across all 335 distinct
quaich clues seen, no colour count ever exceeds len//2 — so I read that as a fixed axis of height
len//2 and went all in on it for the final.

## Final: 71 correct, 750 answered, 5549 presented (rank 1; the other team scored 40)
Only quaich was answered; the six unknown classes were skipped, because a skip costs ~0.39 ms and an
answer ~1.05 ms (fitted from the four training rounds), so skipping them raised throughput from
~2900 to 5549 challenges in the 3 s and roughly doubled the number of quaich challenges seen.

### What the 750 graded quaich answers say (post-mortem)
score = 1 **exactly** when the G bar is the strict tallest AND equals len//2 (71/71); every case with
R or B tallest failed even when it reached len//2 (152 such failures), and every case with a shorter
tallest bar failed (527). Columns really are R, G, B and the fill letters are right. So the axis is
NOT len//2; the two surviving readings are
  (a) the chart's height is the **G count**, or
  (b) the height is the tallest bar and the columns are re-ordered so the **tallest bar sits in the
      middle** (which for a G-max clue is already R,G,B).
(b) is the prettier picture — the beads are arranged into a little hill. With one more training round
this was a single experiment away; I ran out of rounds one step short.
