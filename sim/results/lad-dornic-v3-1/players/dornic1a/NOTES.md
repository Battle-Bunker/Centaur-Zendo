# dornic1a — Centaur Zendo notebook

## The meta-discovery (round 1)
All 7 classes share ONE clue layout:

    <positive example>          (2 examples, occasionally 3)
    <positive example>
    <blank>
    <5 candidate instances>     (ospren numbers its blocks, others are one per line)

Exactly one candidate obeys a hidden rule.  Answer = that candidate's TEXT
(confirmed by the first ospren demo: the solution was the grid, not "5").
Round 2 (cycling option index) scored 25/130 = 19.2% -> confirms 1-of-5.

## Method
Parameter-free feature voting (`zen.py` + `strategy.py`):
 * ~180-340 boolean features per class;
 * a feature true for EVERY positive and for EXACTLY ONE candidate is a possible
   statement of the rule -> one vote for that candidate;
 * ties / no-vote clues fall back to (a) conjunctions of two 2-candidate
   features that meet in one candidate, then (b) "shares most positive-consistent
   features".  Measured ~50-58% on no-vote clues vs 20% blind.
Never skips: a blind answer is worth 20%, a skip 0.

## Per class
| class | instances | rule family (evidence: features that isolate the true answer) | conf | demo | hit |
|---|---|---|---|---|---|
| dornic  | 5 poker cards | "contains a card of rank R", "no cards of suit S", "exactly k picture cards" | med | no | 49% |
| kaldrin | train `[E]=[cargo^]=...` | "the flagged wagons are contiguous" (6x), "exactly k different cargoes", "exactly one flagged", "first cargo = last cargo" | high | no | 55% |
| mestrel | domino run `[a|b]` | "no doubles", "a tile repeats", "exactly k distinct pips" | low | YES | 26% |
| ospren  | 5x5 `#`/`.` grid | "all four corners filled", "mirror symmetric", "two rows identical" | low | YES x2 | 41% |
| tavrik  | lower-case words | "has a double letter", "first letter is alphabetically smallest", "letter repeats non-adjacently", "contains letter X" | high | no | 63% |
| tresk   | R/G/B bead string | "exactly k of one colour", "longest run >= k", "colour counts all different" | med | no | 44% |
| wisbek  | clock times h:mm | "the hour's digit appears in the minutes", "the minute digits are equal", "hour and minutes both divisible by 3", "hour and minutes have the same parity" | high | no | 49% |

## Demos (3 of 3 spent)
1. ospren  - before any hypothesis; bought the ANSWER FORMAT for the whole game
             (option text, not the index).  Best-value demo by far.
2. mestrel - the weakest class (25-29%); its clue shape was already readable, so
             the demo was spent on the rule, and did not crack it.
3. ospren  - second look at the other weak class; also did not crack it.
Deliberately NOT demoed: dornic, kaldrin, tavrik, tresk, wisbek - all were being
probed successfully by feature voting (44-63%), so an example was worth less
there than on the two classes the voter could not reach.

## Rounds
| round | strategy | correct/answered |
|---|---|---|
| 1 | identity (echo the clue) - pure clue harvest | 0/138 |
| 2 | cycle option index - labelled data + 1-of-5 proof | 25/130 (19.2%) |
| 3 | feature voting v1 | 63/133 (47.4%) |
| 4 | + 3-positive parse fix, more features, similarity/conjunction fallback | 60/130 (46.2%) |
| final | same brain as round 4 | **368/779 (47.2%)** |

Per-class final: wisbek 56.7%, kaldrin 52.6%, ospren 47.2%, tavrik 46.6%,
tresk 45.0%, dornic 43.0%, mestrel 40.4%.  Every class beat the 20% blind
baseline; nothing was skipped (779 answers, 779 presented).
