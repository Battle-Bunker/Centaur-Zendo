# fennick1b notes

Pool: basten, fennick, garrow, kelmar, norvel, tovel, virel.
Round 1: skip-everything harvest -> 541 clues, ~77 per class.

## Demos (3 of 3 spent, all before round 2)
Chosen: **virel, garrow, fennick** - the three classes whose clue told me nothing at
all about the *shape* of the answer. Deliberately left without a demo: tovel, norvel,
basten, kelmar - each of those clues contains a canvas with obvious empty slots
('.' after each calendar day, an empty `snare` row, rows of dots above a ground line),
so the format is readable and I can probe the rule with 0/1 feedback instead.

### virel demo
clue `[--][-][][-][-]` + `6`; answer = 5 lines of bracket-rows.
Kid would notice first: (1) "the answer is just more rows of the same boxes";
(2) "the very last row is exactly the row from the clue"; (3) "every row has the same
number of little dashes (5), just parked in different boxes".
Kid's rule -> shuffle the dashes between the boxes, several ways. Invariants: same
number of boxes, same total dashes. Open question: how many lines (n=6 but 5 lines;
5 = number of boxes = total dashes = n-1 - all three coincide). PROBING.

### garrow demo
clue `m2` + fish tank; answer = the tank with three `|` columns inserted, no header.
Kid would notice: (1) "someone drew walls straight down through the tank";
(2) "the walls chop the m-fish in half - one letter left, two right";
(3) "there are 3 walls but the label says 2".
Kid's rule -> the walls cut the m's, and the "2" says where in the fish to cut.
Exact rule found: for each ROW that contains the header letter, take that row's
RIGHTMOST blob of it and cut just before its N-th character. Reproduces the demo
byte-for-byte. Confidence high, ordering of "rightmost" untested.

### fennick demo
clue = letter-bars standing on a ground row + `4 fall`; answer = same picture with
4 bars toppled sideways, `_` cap becoming `/` or `\`.
Kid would notice: (1) "some of the little trees have fallen over";
(2) "the cap turned into a slash pointing the way it fell";
(3) "the ones that fell were the short ones, and they fell into the gap next door".
Kid's rule -> short trees fall into the empty space beside them.
Exact rule found: a tree may fall into direction d only if (c+d) is a gap, (c+2d) is
another tree (i.e. a one-wide slot), and (c-d) is a tree (it is not free-standing);
take the n such trees with the smallest height (ties by column). Reproduces the demo
byte-for-byte. Rendering: everything above the base row shifts one column in d, the
`_` cap becomes `/` (right) or `\` (left); the base letter stays put.

## Read off the clue alone (no demo needed)
* tovel - calendar; every day is printed `NN.` and that trailing dot is the slot.
  Params `L/a/b` -> mark days b, b+a, b+2a... (or every a weeks) with letter L.
* norvel - kick row is full, snare row is empty: fill the snare row. Gap analysis of
  the kick shows a pulse every 2n slots (n=2 -> gaps 1/3/4, n=3 -> 1/5/6/7,
  n=4 -> 1/7/8/9), so the snare almost certainly goes on the off-beat, slot n mod 2n.
* basten / kelmar - dot canvas above a ground line + a number; answer is that picture
  edited, but the rule is a pure guess. Lowest priority.

## Round 2 = probe round
Every class cycles through 5-8 candidate answer builders; `memory['probe']` records
index -> variant so the per-item scores identify the winner.

## Final result (2026-09-05)
score **707** (2946 presented, 1381 answered, 1565 skipped), rank 1 of 2.
per class: fennick 455/455 100% | garrow 139/397 35% | virel 63/396 16% |
norvel 50/417 12% (only the n=2 clues were answered) | basten/kelmar/tovel skipped.

### What each class turned out to be
* **fennick** (SOLVED, exact): letter bars standing on a ground row, `k fall`.
  A bar topples into the empty column beside it iff that gap is exactly one wide,
  the tree across the gap is TALLER, and the bar has another tree on its far side
  (a lone bar never falls). Exactly k bars qualify - the k in the clue is a
  statement, not a budget. Toppling shifts everything above the ground row one
  column, and the `_` cap becomes `/` or `\`. Verified: candidate count == k on
  all 143 clues seen; 592/592 correct once implemented.
* **garrow** (partly): insert `|` columns into the tank; one cut per ROW that
  contains the header letter, placed just before the N-th character of one of
  that row's blobs of it. Which blob, when a row has two, was never cracked -
  "the rightmost" is right about 68% of the rows, 35% of the clues.
* **virel**: answer is several rows of re-packed boxes - same number of boxes,
  same total dashes, no box wider than 4, and the clue repeated as the last row.
  The required number of rows was never pinned down (successes at 5,6,7,8 rows
  with contradictory (k,T,n); same clue shape scored both 0 and 1) - ~15% luck.
* **norvel**: snare row = kick row delayed by n slots. Right about a third of the
  time when n=2 and never for n=3/4, so only n=2 was answered in the final.
* **tovel / basten / kelmar**: never cracked. Best tovel evidence: b is always a
  Mon/Tue/Wed and b + 3a <= days-in-month, i.e. there are always at least four
  marks b, b+a, b+2a, b+3a - but neither "four marks" nor "every a days to the
  month's end" nor any of ~15 other rule/format pairs ever scored.
