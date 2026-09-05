# wisbek2a — notes

All 7 classes are the "hidden rule + multiple choice" paradigm (guide §5b):
2-3 positive examples, blank line, then 4-5 candidates, exactly one of which fits.
Both answer formats work (verbatim candidate text, or its 1-based number) —
verified experimentally on ospren in round 2 (6/9 numeric, 5/9 verbatim).

## Method
- Round 1: skip-everything harvest (155 clues, 0 answers) to read every clue format.
- Per class, a feature extractor (50-220 features) -> auto-generated predicates
  (==, >=, <=, in-set, mod 2/3/4/5, boolean T/F).
- A predicate "fires" on a clue iff it holds for ALL examples and for EXACTLY ONE
  candidate. That candidate gets the predicate's weight; argmax wins.
- Weights learned from (a) structural precision P(unique | consistent) over all
  1277 clues seen, and (b) hit/miss counts from 378 labelled answers.
  One vote per feature (max-weight firing predicate) to stop correlated
  predicates double-counting. 3-fold CV chose the label prior strength (a=2.5).

## Per-class rule families (confidence)
- borsel  (4-5 dice, 1-6): "all dice the same" (7/7 clean), "contains at least one N"
  (N=3,4 seen often), "exactly k different values", "lowest die is N",
  "the step pattern reads the same both ways". HIGH.
- kaldrin (train of cargo wagons, some flagged ^): "first and last wagon carry the same
  cargo" (10/10 clean), "exactly k flagged wagons", "an even number of flags",
  "every milk/coal wagon is flagged", "no coal / no wool". HIGH.
- mestrel (row of dominoes): "the two outer ends show the same number" (11/11 clean),
  "exactly k doubles", "value 5 never appears", "the flat end values differ by k".
  Notably NOT a legal domino chain (never once the rule). HIGH on the ends rule.
- ospren  (5x5 # grids): "exactly k corners filled" / "all four corners" (6/6),
  "mirror symmetry left-right or top-bottom" (3/3 each), "row totals are the column
  totals rearranged", "exactly k full rows". MEDIUM-HIGH.
- tresk   (R/G/B strings): "exactly k blues", "the commonest colour appears k times",
  "a run of 4+ of one colour", "colour X never immediately followed by colour Y"
  (no_BR 4/5). MEDIUM.
- wisbek  (clock times h:mm): relations between the HOUR and the mark the MINUTE hand
  points at: "the minute hand points at the number next to the hour" (7/7 clean),
  "hour + minute-mark = 12", "hands a quarter turn apart", "a digit is repeated".
  Pure minute rules alone are never enough. MEDIUM-LOW.
- dornic  (5-card hands): "the highest card is rank X", "contains exactly k aces/queens",
  "an even number of clubs", "exactly one court card". Poker shapes (flush, straight)
  are NEVER used — deliberately excluded. LOW (33%).

## Demos spent: wisbek, dornic, tresk (the three worst hit-rates after round 2).
Deliberately not spent on: borsel/ospren (already 25-60% and probeable), mestrel and
kaldrin (a single 100%-precision structural rule was already visible in the statistics).
