# tresk1a notes

Final score 1176 / 1742 presented (1509 answered).

## Round log
| round | presented | answered | correct | note |
|---|---|---|---|---|
| 1 | 358 | 0 | 0 | skip-only harvest of all 7 clue formats |
| 2 | 295 | 203 | 136 | generic rule engine on the 5 "pick 1 of 4" classes |
| 3 | 269 | 269 | 157 | + fennick v1 (left-to-right topple), garrow probes |
| 4 | 257 | 257 | 168 | + fennick v2 (correct eligibility rule) |
| final | 1742 | 1509 | 1176 | garrow skipped |

## Classes
* borsel / dornic / tavrik / tresk / wisbek — rule-family: k example lines,
  blank line, 4 candidates; each clue has its own hidden rule. Solved by a
  generic engine: ~60 features per item, keep every feature whose value is
  shared by all examples, group predicates by the candidate-subset they pick,
  vote for the candidate that a uniquely-selecting predicate points at.
  Feature reliabilities estimated from round-2/3 0/1 feedback.
* fennick — bar chart + "N fall". SOLVED exactly (demo spent here).
  A bar topples into an adjacent empty column iff the empty column has bars on
  both sides, the two heights differ, and the shorter bar is not itself
  isolated (it must have a bar on its far side). N always equals the number of
  such bars, so the picture determines the answer completely.
  Toppling: the h-1 cells above the base shift one column toward the gap and
  the "_" cap becomes "/" (right) or "\" (left) in the gap column.
* garrow — NOT solved. "a2"-style code + 4 rows x 3 blobs on ~ water.
  count(header letter) is 4..6, n is 1..3, count >= n always, but no
  deterministic n found. 9 answer-shape hypotheses tried, 0/65. Skipped in
  the final (precision tiebreak).
