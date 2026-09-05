# Centaur Zendo — tavrik1a notes

## Structure discovered (round 1, skip-only harvest, 211 clues)
6 of 7 classes are MULTIPLE CHOICE "rule family" classes:
  clue = <positive examples>  blank line  <candidate instances>
  answer = the one candidate obeying the hidden rule.
  The server accepts EITHER the candidate's text OR its 1-based index (verified in round 2).
1 class (norvel) is a picture-edit class.

| class  | objects                    | pos | cands |
|--------|----------------------------|-----|-------|
| borsel | rows of small ints (dice)  | 2-3 | 4     |
| dornic | card hands "AS 3C 5S"      | 3   | 4     |
| ospren | 5x5 #/. grids (numbered)   | 2   | 5     |
| tavrik | English words              | 2   | 5     |
| tresk  | R/B/G strings              | 2   | 5     |
| wisbek | clock times h:mm           | 2   | 5     |
| norvel | 3-line drum grid + "N slip"| -   | -     |

## norvel — SOLVED (100%), the one demo
A "slip" = a snare hit with NO hat and NO kick on the same step.
The count in "N slip" equals the number of such hits (verified 33/33 on round-1 clues).
The edit: each slipped snare hit slides RIGHT until the step where the hat plays
(stopping before the next snare hit); the steps it crosses become '-'. Other rows
and the trailing text line are unchanged.

## Engine for the MC classes
For each class a feature library maps an object -> set of predicate strings.
consistent = intersection of the positives' feature sets.
For each consistent feature satisfied by h of the k candidates (0<h<k),
each satisfying candidate gets prior(f) * learned(family(f)) / h^2. Argmax wins.
Learned family weights fitted by gradient ascent on the 0/1 feedback from
rounds 2-4 (both "this was right" and "this was wrong" labels used).
dornic uses plain 1/h^2 (live A/B said weights hurt it).

## Rules actually confirmed by hand from labelled data
tresk : "exactly k of colour C"; "longest run == k"; "contains CCC".
wisbek: "minutes divisible by k"; "minutes = c x hours"; "(h+m) divisible by 6";
        "digit sum even"; "both minute digits equal".
tavrik: "contains letter X"; "ends with X"; "has a doubled letter";
        "a letter repeats at distance d"; "no front vowel (e/i)".
ospren: left-right / up-down mirror symmetry; full rows/cols; component counts.
borsel: "contains value v"; "some adjacent pair ascends by 1"; max/min value.
