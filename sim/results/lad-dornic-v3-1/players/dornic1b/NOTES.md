# dornic1b — notes

## The shared shape (found in round 1, confirmed by all 3 demos)
Every one of the 7 classes is the SAME puzzle in a different costume:

    <positive example>            (sometimes two positives: kaldrin, ospren)
    <NEGATIVE example>            <- always the LAST line of the first block
    (blank line)
    <5 candidates>                (ospren numbers them 1..5 because grids are multi-line)

Answer = the winning candidate's own TEXT (never its number). Exactly one
candidate obeys the hidden rule. The hidden rule changes every instance.

The pos/negative split was NOT guessable from the clue — the tavrik demo settled
it: for `tommy / heat -> unity`, ~1000 predicates were tested and ZERO were true
of both tommy and heat while singling out unity; but "ends in y" is true of
tommy, false of heat, and true of unity alone.

## Method
Enumerate ~1000 cheap boolean properties per item; keep those true of every
positive and false of the negative; every such property that singles out exactly
ONE candidate votes for it, weighted by a per-class prior on that KIND of rule.
Deterministic, ~0.3 ms/challenge. Priors were re-fitted from 109 known-correct
answers by asking "which properties explain the answers I got right?".

## Per-class rule families (from that fit)
| class | it IS | it is NOT |
|---|---|---|
| tavrik  | contains / starts with / ends with letter X; number of vowels | letter-sum, positional-letter, alphabet-half tricks |
| tresk   | contains substring; run lengths; colour counts & equalities | almost nothing else |
| wisbek  | DIGIT rules: digit sum, repeated digit, hour digit inside minutes, minutes past 30, on a 5-mark | clock-hand geometry (angles) — tested, never once |
| dornic  | a named rank or exact card; suit counts; pair/flush/all-even | sum totals |
| mestrel | a named tile; how many of a pip; biggest/smallest pip | chain/adjacency (rare) |
| kaldrin | which goods repeat; what follows what; position of the ^ marks | length |
| ospren  | full/empty rows & columns, symmetry, filled-count | (flat weights beat tuned ones) |

## Results
r1 harvest 0/137 · r2 37/131 28.2% · r3 34/140 24.3% · r4 35/115 30.4%
FINAL 194/794 = 24.4%
