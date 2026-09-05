# Centaur Zendo notes - team kelmar1a

Pool: basten(89) durnel(81) tovel(80) fennick(70) kelmar(66) virel(66) norvel(61)  [round-1 counts]

Free finding from round 1: for fennick/durnel/kelmar the clue ends "N <verb>"; when N=0
echoing the clue verbatim scores 1. So the answer = clue picture with N edits.

## durnel  -- SOLVED (no demo)
Picture: cars on a road `MM>` (rightward) `<HH` (leftward); above each car a column of its
letter = its height; `###` runs floating in the air = low bridges, clearance = (ground_row-r-1).
Rule: a car turns round (arrow flips, `MM>`->`<MM`) if somewhere ahead of it in its own
direction there is a bridge whose clearance < car height. Verified on 6/6 clues (N matched).

## fennick -- DEMO TAKEN
Picture: columns of stacked letters, `_` cap above each stack. Rule (verified on the demo,
5 fallers exactly): a stack falls sideways into an adjacent EMPTY column of width exactly 1
if the stack on the far side of that 1-wide gap is STRICTLY taller. Falling = every row
above the ground row shifts one column that way; the `_` cap becomes `\` (left) or `/` (right).

## kelmar -- DEMO TAKEN
Trees `(~~~)` + trunks `'''''` of varying height, ground line of `_ * Y`.
Demo: 2 `*` became `\`; both were the `*` immediately to the RIGHT of the two tallest trees
(h=3); `*` next to h=1 trees did not lean. Hypothesis: the N `*` nearest/next to the tallest
trees lean toward the tree. Direction char for a tree on the right is untested -> variants.

## virel -- DEMO TAKEN
Rows of `[..]` bricks, each row same total width; trailing number N.
Demo: answer = the clue rows with ONE NEW ROW PREPENDED (and the number line dropped).
What constrains the new row is unknown (the demo row shares joints with the row below, so it
is not running bond). N=1 there. -> variants.

## basten -- no demo
Underwater: `~` surface, `#` seabed, `|` plants of height 1..3, trailing number N in 3..5,
always >= tallest plant and <= water depth. Hypothesis B1: grow every plant to height N.

## tovel -- no demo
Month calendar, every day number followed by `.` (a slot to fill). Code `X/n/d`.
Hypothesis T1: write letter X in the slot of days d, d+n, d+2n, ... -> variants.

## norvel -- no demo
`kick` line of `x` in 4-step bars, empty `snare` line to fill, `n = 2..4`.
Kick hits cluster every ~2n steps. Hypothesis: snare on the offbeats, halfway between kicks.

## Demo choices
virel (could not guess the answer format at all), fennick and kelmar (knew it was
"picture with N edits" but had no idea what one edit looked like).
Deliberately left without a demo: durnel (already cracked from clues), basten and tovel
(answer shape obvious from the clue: grow the plants / fill the dots) and norvel
(answer shape obvious: fill the snare row) - those get probed by cycling variants instead.

## FINAL (score 1949 / 3268 presented, 2457 answered, rank 1)
durnel 512/512, fennick 448/448, kelmar 477/477, virel 438/438,
norvel 54/459 (only n=2 understood), tovel 20/437, basten 0/497 (skipped).

Rules as finally understood:
* durnel  - a car turns if a bridge ahead of it has clearance < the car's height.
* fennick - a stack leans into a 1-wide gap when it is propped on the other side and
            the stack across the gap is strictly taller; cap `_` becomes `\` or `/`.
* kelmar  - every `*`/`Y` touching a full-height tree leans (`\` toward the tree).
* virel   - add a course on top with exactly N bricks coinciding with bricks below;
            the trailing number line must be dropped.
* norvel  - for n=2 the snare is the kick rotated n steps (50%); n=3,4 never cracked.
* tovel   - "every n days from d, code line dropped" scored once in 13; rule still wrong.
* basten  - never cracked. N (3..5) is independent of the picture (all 9 combinations of
            N x water-depth occur, max plant height is always 3), so it is not a height,
            a depth or a count of anything visible. 15 rules tried, 0/790.
