# dornic1a — notes (final score 863)

Method: round 1 = 660 pure skips (harvest every clue). Then a **version-space**
solver for the five rule-family classes: a large library of candidate predicates
per class, AND the predicates true of every clue line, then return the first item
of a candidate universe that satisfies all of them (guaranteed right whenever the
hidden rule is somewhere in the library). Rounds 2-4 were controlled experiments
that cycled answer variants by a per-name counter and read the per-variant scores.

Measured variant results (training):
* ECHO a clue line: 0/40 — repeats are always rejected.
* RAND item from the universe: 2/40 — base rate ~5%, so the solver's score is real.
* curated (lift-selected) version space beat the full library on tavrik/tresk/wisbek;
  the full library beat it on borsel.
* ordering the candidate universe **corpus-first** (real lines harvested from other
  clues before synthetic items) roughly doubled wisbek (0.21 -> 0.57) and tresk
  (0.13 -> 0.47): real instances are in-distribution, synthetic extremes are not.
* dornic: only the suit-relabelling mutation (H<->D, C<->S) of a clue line, filtered
  through the version space, ever scored (0.17-0.25); everything else 0.
* basten: fish that **touch a weed** 8/14 vs greedy placement 1/10.
* kelmar: `num` evenly spaced 3-wide bands, glyph `|`, 5/18 on num=2 clues; 0 elsewhere.
