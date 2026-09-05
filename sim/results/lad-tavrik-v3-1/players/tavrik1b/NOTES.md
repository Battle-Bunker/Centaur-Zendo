# tavrik1b notes

Pool: borsel, dornic, norvel, ospren, tavrik, tresk, wisbek.

## Structure
6 of 7 classes are multiple-choice rule classes: clue = block of 2-3 POSITIVE examples,
blank line, then a block of 4-5 CANDIDATES. Answer = the candidate that also obeys the
hidden rule (ospren numbers its options 1..5; both the number and the grid text score).
norvel is a picture class (drum grid edited).

## norvel  (SOLVED, 100%)
hat/snare/kick rows of 4-step bars + "N slip".
N = number of snare hits that have NO hat and NO kick on the same step (verified 63/63).
Answer = clue with the snare row edited: every such lonely snare hit slides RIGHT to the
next step where the HAT plays; the vacated steps (original .. target-1) become '-'.
Confirmed by 2 demos + 57/57 live hits.

## Multiple-choice engine
Per class a feature vector; for every feature take [lo,hi] over the positives and test
"==lo" (when lo==hi), ">=lo", "<=hi". A predicate that selects exactly ONE candidate votes
for it, weighted by a hand prior. Weighted vote + small similarity tiebreak.
Params M_EQ=1.0 M_GE=0.5 M_LE=1.0 M_SIM=0.1.

## Families identified (from 3 demos + ~170 labelled instances)
borsel (dice rows) : min==v, max==v, exactly k distinct, k-of-a-kind (mode), a doubled
                     neighbour pair, contains value v, range.
tresk  (RGB words) : exactly k of a colour, longest run == k.
tavrik (words)     : has a double letter (very common), a given letter's count, last letter,
                     vowel counts.
dornic (card hands): rank span, highest/lowest rank, a pair, suit counts, #red.
ospren (5x5 grids) : empty row/column, full row/column, mirror symmetry, corners, runs.
wisbek (clock times): a repeated digit; digits strictly increasing; digit sum < 10;
                     minutes divisible by k; hour and minutes same parity; m == 5*h;
                     (m-5h) mod 10 == 0 (minute hand on a number of the hour's parity).

## Round scores
r1 skip-only (harvest), r2 39%, r3 48.8%, r4 53.2%.
