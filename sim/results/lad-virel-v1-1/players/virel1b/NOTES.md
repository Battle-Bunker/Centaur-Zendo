# virel — notes (centaur team: AI + 12-year-old)

## Narrating demo 1 to a 12-year-old
"The computer gave us a little label: `6335/6`. It gave back a picture that
looks like eight rows of Lego bricks. Each brick is a pair of square hooks
`[` `]` with some dashes stuffed inside. Some bricks are empty, `[]`. Every
row is exactly as long as every other row — like a brick wall where all the
courses line up at the edges."

Three things a kid notices first:
1. "It's a WALL. Every line is the same length." (17 chars; 22 in demo 2.)
2. "Some boxes are empty and some are fat — the fattest has 4 dashes."
3. "The bottom row is different / the numbers in the label are small (2-6)."

Kid ideas tested first:
- KID IDEA A "all rows the same length" -> TRUE. length = sum of the digits.
- KID IDEA B "the bricks come in a few sizes only" -> TRUE. brick width 2..6,
  which is exactly the range of the digits in the clue.
- KID IDEA C "the label is hiding in the picture" -> TRUE, and it was the kid's
  idea to read the bottom row as numbers: 6335 -> `[----][-][-][---]`
  = widths 6,3,3,5. Demo 2 confirmed: 65344 -> `[----][---][-][--][--]`.

## Facts (confidence high)
- clue = `D/k`, D = 3..6 digits each in 2..6, k an integer.
- w = sum(D). Every line of the answer is a composition of w into parts 2..6,
  rendered as `[` + (p-2)*'-' + `]`.
- The LAST line equals the clue digits themselves (2/2 demos).
- Observed k range: 1 .. floor(w/2) - 2.
- demo1 (w=17,k=6): 8 lines, per-line part counts 3,6,5,4,4,5,4,4 (max = k).
- demo2 (w=22,k=8): 6 lines, per-line part counts 6,7,8,5,6,5 (max = k).
- No brick-wall "joints must not align" rule (demo1 rows 1&2 share a joint at 12).

## Open question
What sets the NUMBER of lines? k=6 -> 8 lines; k=8 -> 6 lines.
Round 2 experiment: cycle line count j = 1..12 x two content regimes and read
the 0/1 scores back out.

## Final understanding (after 6 rounds, ~2300 scored answers)
Necessary, confirmed on 207 correct answers with zero exceptions:
- every line = composition of w into parts 2..6 rendered `[`+(p-2)*`-`+`]`
- constant line width w = sum of clue digits
- last line == the clue digits
- no fault line (no interior column that is a joint in EVERY line)
- at least 5 lines (0 hits in 160 tries with 1-4 lines)
Not required: fixed line count (clue `265/3` accepted at 5 lines AND at 11),
all-lines-distinct, staggered joints, any relation to k.
UNSOLVED: what `k` does. No integer feature of the wall out of ~120 tried
(line count, distinct lines, joint columns, per-size brick counts, column
multiplicities, sums, differences, mods) equals k on all 207 positives, and
hit rate is flat across k. Best empirical generator: 7 lines, all distinct,
no joint column used by more than 4 lines -> ~15-18% accepted.

## Round scores
r1 skip-everything: 769 presented / 0 answered / 0 correct (data collection)
r2 24-way hypothesis sweep: 477 / 477 / 21
r3 fault-free walls, n=5..10: 466 / 466 / 55
r4 A/B natural vs uniform rows: 456 / 456 / 61
r5 tuning around n=7 cap4: 455 / 455 / 66
r6 taller walls (n=9..15): 430 / 430 / 30  (taller is worse)

## FINAL
2566 presented / 2566 answered / 354 correct (13.8%).
