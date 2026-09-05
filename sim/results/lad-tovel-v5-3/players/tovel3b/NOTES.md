# tovel3b — notes

Pool: basten fennick garrow kelmar norvel tovel virel

## Round log
| round | presented | answered | correct |
|---|---|---|---|
| 1 (skip-only harvest) | 604 | 0 | 0 |
| 2 (probe wave 1, ~14 hypotheses/class) | 433 | 433 | 77 |
| 3 (probe wave 2, ~18 hypotheses/class) | 361 | 361 | 81 |
| 4 (probe wave 3 + measurement) | 430 | 430 | 73 |
| FINAL | 3070 | 1385 | **787** |

## Demos spent: fennick, basten, kelmar

## fennick — SOLVED (100%)
A row of trees drawn as columns of a repeated letter, `_` capping each, `.` = a bare
patch, `===` ground line, `N fall`.  Rule: for every gap exactly one column wide, the
SHORTER of the two neighbouring trees topples into it (equal heights -> neither moves);
a tree with a bare patch on both sides never falls.  A falling tree keeps its base
letter, shifts every cell above the ground one column into the gap, and its `_` cap
becomes `/` (right) or `\` (left).  Verified 89/89 against the `N fall` checksum and
byte-exact against the demo.

## basten — PARTIAL (47%)
Pond: `~` surface, `.` water, `|` weeds, `#` bed, trailing number.  Answer = the picture
with `<><` fish (always 3 chars) added to the bottom water row.  Count = (max fish that
fit with one blank between them) + num - 4.  num=4 75%, num=3 55%, num=5 15%.
Placement is scored leniently; the COUNT is what matters.

## kelmar — PARTIAL (20%)
Ground line with `Y` and `*`, blank rows above, number.  Answer = vertical stripes of
`'` (grass) and `.` repeated on every blank row: 3 on / 3 off, phase anchored at the
right edge ((W+1)%6).  num=1 never scores with this -> different period.  The demo's
true answer was a stripe on the right that broke up near the left where markers were
dense, so the real rule is stripe + a marker-driven perturbation I never cracked.

## garrow / norvel / tovel / virel — UNSOLVED (skipped in the final)
~60 hypotheses each tested across rounds 2-4, all zero.
* garrow `o3` + tank of 3-char creatures: tried slide/wrap/gravity/remove/add/mark/count/coords.
* norvel kick+empty snare+`n`: kick onsets sit ~2n-1 apart with 1-3 hit bursts; tried 40
  snare rules (grids, echoes, complements, gap fills, backbeats) - none.
* tovel calendar + `LETTER/n/day`: tried marking rules x mark characters, plus numeric answers.
* virel `[---][--][][----]` + n: tried pours, repartitions, splits, merges, marks, numbers.
