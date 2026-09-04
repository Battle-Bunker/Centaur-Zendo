# garrow — notes

## The picture (how I described it to my 12-year-old partner)
"A long thin fenced-in strip, four lines tall, with little two-letter blobs
(`aa`, `pp`, `bb`, `ss`…) scattered inside like sweets in a tray. The answer is
the same tray chopped into chunks with up-and-down lines, like cutting a
chocolate bar. Some sweets get chopped in half by a cut (`a|a`)."

Kid's first three noticings:
1. it's the same picture, just cut into pieces;
2. the letters always come in twos;
3. the cuts sometimes slice a pair down the middle, and the pieces are
   different sizes.

## Rule (confidence: high for the counting, low for "is that all")
Clue line 1 = `<X><n><Y><m>` (e.g. `a5p3`). Answer = the strip with `|` cuts.
For each slice count the X letters and the Y letters:
  more X  -> the slice belongs to X
  more Y  -> belongs to Y
  equal but non-zero -> belongs to whichever of X/Y appears first in reading
                        order (this always came out as Y in the examples)
  no X and no Y at all -> spare slice, belongs to nobody
Require exactly n X-slices and m Y-slices. The number of slices is NOT fixed:
demo 4 (`o2p4`) had 7 slices for n+m = 6.
Verified against all 4 demo answers and every answer that scored 1.

## The unsolved part
Every answer I sent satisfied that rule exactly, and only ~5% scored 1.
Tried and ruled out (each contradicted by a demo answer or by a scoring hit):
exact match to a canonical answer; pair-based counting (whole / left-cell /
right-cell / touching); row-vote; column-count; overall-most-common-letter
dominance; near-uniform slice widths; widths in [3,8]; cuts that split no pair;
cuts that all split a pair; margins; "each slice must hold a whole pair";
answer length; metric-robust labelling (all six metrics agreeing).
Hit rate stayed 2–12% for every one of five different answer-shaping strategies,
which is what you'd see if acceptance depended on the *clue* rather than on my
answer.

## Round log
1 skip-all (data)   0/0     2 counting rule      3/52
3 four-arm probe    1/52    4 generator-shaped   3/52
5 robust labelling  1/40    6 counting rule      6/49
final                       17/291
