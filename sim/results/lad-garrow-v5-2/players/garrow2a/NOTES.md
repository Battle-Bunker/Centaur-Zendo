# garrow2a — final notes

All 7 classes are pictures with a trailing (garrow: leading) "N <verb>" line.
Round 1 (answer = clue verbatim) established the master key: **N is the number of
times an operation is applied, and N==0 means the answer is the clue unchanged**
for 6 of 7 classes. virel was the exception (identity never scored) -> demo #1.

| class | rule | confidence | demo | final |
|---|---|---|---|---|
| virel | prepend a row of `[...]` boxes tiling the same width whose (start,width) spans coincide with EXACTLY N spans of the clue's top row. Answer is non-unique; any such row scores. Verified on 77/77 offline + 44/44 + 29/29 live. | certain | yes | 100% |
| durnel | cart `XX>` / `<XX` rolls onto the first pit `\_/` ahead of it, fills it (pit vanishes) and reverses. Pits resolved right-to-left, left-approaching cart wins, a cargo-less cart blocks its pit, `###` bridges block carts whose cargo tower is too tall. N = number of such falls. | mechanism certain, tie-break wrong ~3/4 of the time | yes | 24% |
| molvic | fill the first empty `___` shelf slot with that shelf's own stock found on another shelf; repeat N times. Right at N<=1, wrong above. | partial | no | 15% |
| garrow | `X N slices`: answer is the loaf with `|` cut marks inserted (demo showed 5 cuts for N=3, cutting through tokens). Cut placement never found. | format only | yes | 14% (N=0 only) |
| fennick | columns of uniform-letter stacks, `_` marks one above each top. 20 "fall" hypotheses (topple, decay, grow, sandpile, flatten, slide) all scored 0. | none | no | 12% (N=0 only) |
| tovel | month calendar, letters = events. 20 "bump" hypotheses (+1 day, +7, cascade, letter-increment, weekend, delete, swap) all 0. | none | no | 15% (N=0 only) |
| norvel | hat/snare/kick 16th-note grid. 20 "slip" hypotheses (rotate all/one row/per bar/bars, shift, note-nudge) all 0. | none | no | 14% (N=0 only) |

Final: 582 correct / 1079 answered / 2142 presented (27.2%). Rank 2 of 2.
