# tovel2b — notebook

Final: 491 correct / 1245 answered / 2869 presented (rank 1; tovel2a scored 238).

## Method
Round 1 = pure skip harvest (645 clues, no compute) to see all seven clue formats.
Then: read every clue family, look for a *derived number* in the clue (fennick's
"N fall" turned out to be a checksum of the transformation, which let me validate a
rule against 91 clues offline with zero rounds spent). Rounds 2-4 were hypothesis
sweeps: 12-151 candidate answer-rules per class, cycled deterministically so each
scoring answer could be traced back to the rule that produced it.

## Per class

### fennick — SOLVED (446/446 in the final)
Picture = a row of trees: each column is a letter-trunk of height 1-5 with a `_` cap,
`.` = bare ground at the bottom row. A tree LEANS into an adjacent one-column gap if
(a) exactly one of its neighbours is empty, (b) that gap is exactly one wide, and
(c) the tree across the gap is strictly taller. Leaning = everything above the ground
row shifts one column that way; the cap `_` becomes `\` (left) or `/` (right).
The clue's "N fall" is exactly the number of leaning trees — verified 91/91 on round-1
clues before I ever spent a round on it. Demo #1 spent here; worth every bit.

### kelmar — structure solved, one binary choice missing (8.7%)
Answer = the sky rows filled with `'`/`.` in alternating bands, ground row kept, the
trailing number dropped. Boundary after symbol i is at  p_i + 1 - (count of type-A
symbols up to i), i.e. one symbol type is "zero width". All 19 solved examples fit
that model exactly — but *which* type is A (`Y` or `*`), and whether the leftmost band
is `'` or `.`, varies per clue and I never found the discriminator (it is not the
sequence of types: two clues with identical Y/* sequences disagreed). Best single
guess (A=`*`, start marked) ≈ 19%. Demo #3 spent here.

### virel — partially solved (2.3%)
Answer = several lines, each a re-packing of the SAME total shelf width (each box is
`[` + dashes + `]`, so 2 + size). Every scoring answer had exactly n new lines with the
same box-count as the clue plus the clue itself; but only ~12% of structurally
identical answers scored, so a further hidden constraint on which packings count
remains unknown. Demo #2 spent here — it revealed the multi-line format, which no
amount of probing would have found.

### basten, garrow, norvel, tovel — NOT solved (0%)
* basten: `~` ceiling, `#` floor, poles of height 1-3 at least 5 apart, n∈{3,4,5} is
  not a function of the picture (so it is a free parameter). 45 rules tried: growing,
  flooding, trapping rain water, toppling, stalactites, planting. All 0.
* garrow: fish tank, 3 species, exactly 3 fish per row, header `t2` = letter+count.
  n is *usually* (count of that species) - 2 but not always, so it is a count of some
  property of those fish I never identified. 73 rules tried (swim n / 3n / 1, wrap or
  clamp, remove, keep, add, sink, promote). All 0.
* norvel: drum grid, kick given, snare empty, n∈{2,3,4}; the kick pulses roughly every
  2n sixteenths with jitter. 53 snare rules tried (echo/delay, backbeat, gap
  midpoints, complements, grids, mirrors). All 0.
* tovel: a month calendar plus `L/k/d`. Strong structural finding: weekday(d) is
  always Mon/Tue/Wed and d+k-1 never leaves the month, so days d..d+k-1 always sit in
  one calendar row — the intended object is certainly that horizontal run. But 46
  marking styles x day-sets (letter in the dot, over the digits, whole cell, blanking,
  inverting, the row alone, a week earlier/later) all scored 0.

## Demo allocation and why
Demos were taken AFTER round 1 (never before seeing the clues), on the three classes
whose clue told me least about the answer's *shape*: fennick, virel, kelmar.
Deliberately left without a demo: tovel (the calendar's `.` placeholders looked like an
obvious mark slot — wrong, and it cost me the class), garrow and norvel (the edit
looked guessable: move the fish / write the snare), basten (looked like the guide's own
"n pebbles" example). In hindsight tovel or garrow deserved kelmar's demo: kelmar gave
me a rule I could only half-use, while a tovel demo would probably have been decisive.
