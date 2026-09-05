# NOTES — tovel3a

Pool: basten, fennick, garrow, kelmar, norvel, tovel, virel (each ~13-15% of items)

Round 1 = pure skip harvest: 581 presented, 0 answered. Clue formats collected in an/*.txt.

## HOUSE FORMAT (learned from 2 demos)
Answer = the clue's PICTURE with the edit applied, WITHOUT the trailing parameter line.
(kelmar demo: 3 lines returned, "2" dropped. basten demo: 6 lines, "4" dropped.)

## Per class
### tovel (calendar + `L/k/d`)  — CONF HIGH-ish, no demo
Month calendar, every day printed as "%2d." — the '.' is an empty slot.
k in 1..5, d in 4..28, L random letter. Hypothesis: mark days d, d+k, d+2k... by
replacing that day's '.' with L. Probe variants t0..t5.

### virel (`[--][][-][----][-]` + N) — CONF MED, no demo
Boxes (4 or 5) each holding 0..4 dashes (cap looks like 4); N=2..7 items to add.
Which boxes? probe: emptiest-first / leftmost-first / round-robin / rightmost.

### norvel (kick line + empty snare line + `n =`) — shape CERTAIN, rule unknown
Fill the snare line. n in {2,3,4}; with n=4 the kick only uses even bars (call/response).
Probe: echo delayed by n steps / n bars, complement, fill-empty-bars, etc.

### fennick (letter bar chart + `N fall`) — shape likely, rule unknown
Columns = bars of a repeated letter, '_' marks the cell just above each bar, '.' = empty
column at ground, then a `====` rule line. N in {0,4,5,6,7,8}; N=0 in 13/89 cases
=> for N=0 the answer is probably the picture UNCHANGED (free format probe).

### garrow (`s3` + pond of 3-char fish `sss`) — shape likely, rule unknown
Pond bordered by #, water ~, species tokens aaa/bbb/ccc/mmm/ooo/ppp/sss/ttt (4-6 of each).
Code = species letter + number 1..3. Probe: swim that species N cells right/left,
mark/remove the N-th one.

### kelmar (2-3 dot rows + baseline of `_`,`Y`,`*` + N) — DEMO TAKEN
demo: N=2, 2 sky rows, baseline `______Y_____*__Y__Y____*__*__`
      -> both sky rows = `....|||......|||||...||||....`
Blocks [4..6] w3, [13..17] w5, [21..24] w4; marks Y6 *12 Y15 Y18 *23 *26.
Learned: answer = solid `|` blocks in the sky, N = ? (block height fits: 2 rows all filled).
Alternate marks (1st,3rd,5th) sit inside blocks; the geometry is not yet cracked.

### basten (water `~` / posts `|` / floor `#` + N) — DEMO TAKEN
demo N=4, posts col4 h3, col12 h3, col17 h1, col22 h3
  -> 6 FISH added: `><>` (right) and `<><` (left), 3 chars, placed in the water,
     never overlapping a post, every fish adjacent to a post (side or above).
     row1 (above all posts): ><> at 4-6; row2: ><> 1-3 and <>< 23-25;
     row3: ><> 1-3, <>< 9-11, <>< 13-15; bottom row: none.
N=4 but 6 fish -> N is not the fish count. Rule not cracked.

## Demo plan
Spent: kelmar, basten (the two whose answers I could not even guess the CHARACTERS for).
Reserve: 1 demo, to be spent after round 2 on whichever of norvel/garrow/fennick
my probes fail on.

## After round 2 (380 answered, 10 correct)
Variant hit table: basten v1 4/7 (ALL of them N=3, all N=4 failed);
fennick v1/v4/v5 hits were exactly the 5 clues with `0 fall` (echo) => format confirmed;
norvel v0 1/7 (the one n=2 clue whose +2 echo had no collision with a kick hit);
tovel/virel/garrow/kelmar 0.

* basten: RULE FOUND for N=3 -> one `><>` per body row, pushed right until it hits the
  first post (right-aligned in the leftmost gap; in a post-free row it ends at the wall).
  N=4/5 must differ somehow (glyph? direction? count?) - probe.
* fennick: answer = picture + `====` line, unchanged when N=0.
* norvel: snare = kick echoed n steps later; echoes that would land ON a kick hit are
  probably suppressed (the failing n=2 clue had exactly one such collision).
* tovel DEMO: `M/5/13` -> EVERY day cell gets a letter (4 letters used: M Z C A).
  The Tuesday column (6,13,20,27) is all M and 13 is a Tuesday: k=5 = every 5th
  WORKING day (Mon-Fri) from d, in both directions. Other days carry other letters that
  the clue never names => the checker must be lenient about them. Probe: all-L vs
  L-on-its-days-plus-filler vs leave-others-blank.
* virel: N is neither items-to-add (N can exceed free space at cap 4) nor items-to-remove
  (N can exceed the total). Probe repacking-into-N-boxes / boxes-of-capacity-N.

## Round 4 + FINAL
Round 4: kept the two known rules, probed basten(N!=3) x8, virel x8, garrow x8,
fennick(N>0) x8, norvel(n!=2) x4; skipped tovel+kelmar to buy more items.
Result: basten known 16/16, fennick echo 6/6, norvel +2 echo (n=2) 7/14, everything
else 0/~200. No new rule found.

FINAL (3 s): presented 3717, answered 406, CORRECT 306, skipped 3312.
  basten 184 answered / 183 correct   (only the N=3 third of the class attempted)
  fennick 62 / 62                     (only the N=0 clues attempted)
  norvel 160 / 61                     (only n=2 attempted; the rule is ~40% right)
  garrow, kelmar, tovel, virel: deliberately skipped (0 answered) - skipping is
  instant, scores the same as a wrong answer and protects the fewer-answers tiebreak.
The single basten miss: posts at 4,9,15,20,25, my fish 1-3 in the post rows.
