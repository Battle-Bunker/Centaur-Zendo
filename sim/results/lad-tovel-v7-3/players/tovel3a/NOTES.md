# Centaur Zendo — tovel3a notes

Universal discovery (round 1): every clue ends with a line `<N> <verb>`.
N is the number of edits the answer needs; **N == 0 means the clue itself is the answer**
(100% hit rate, ~13% of all items). Everything else is "which N things, and what happens to them".

Method: harvest clues -> for each class build a structured parse -> search for a counting
predicate whose per-picture total equals N, using exact rational least squares over
counts of local patterns (`lsq.py`). A predicate that matches N on 100+ pictures is the rule.

| class | rule (what N counts) | edit | status |
|---|---|---|---|
| molvic | shop shelves; item X sits in row Y and row Y's item sits in row X in the SAME column (a swap pair), and X's own row has a blank | the swapped-in item moves to the first blank of its home row | SOLVED 100% |
| kelmar | trees + ground plants; plants (`*`/`Y`) immediately beside a **tallest** tree | left neighbour -> `/`, right neighbour -> `\` (leans toward the tree) | SOLVED 100% |
| durnel | carts with stacked cargo on a road, `\_/` = empty bay, `###` = low bridge; a cart turns if a bridge its cargo would hit lies ahead in its facing direction | it moves (cargo and all) to the nearest reachable bay in that direction and reverses its arrow | SOLVED 100% |
| felsim | stack of `\__/` cups; a cup with nothing above it resting on exactly ONE cup below | UNKNOWN (11 edits tried) | count certain, edit unknown |
| norvel | hat/snare/kick grid; columns with a snare hit and no hat and no kick (never more than one per bar) | UNKNOWN (11 edits tried) | count certain, edit unknown |
| tovel | calendar; a busy day with busy days on both sides (middle of 3 in a row) | UNKNOWN (11 edits tried) | count certain, edit unknown |
| basten | river with reeds `|` (rooted on the bed) and fish `><>`/`<><` | UNKNOWN | count never found |

Demos spent: molvic, durnel, kelmar (the three whose scene I could not read off the clue).
Deliberately left without a demo: felsim, norvel, tovel (counting rules found by analysis) and
basten. In hindsight the demo should have gone to a class where I had the count but not the edit.
