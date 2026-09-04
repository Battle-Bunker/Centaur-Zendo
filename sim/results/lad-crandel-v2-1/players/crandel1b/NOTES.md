# crandel — solved

## Clue grammar
`(ddd/)+ d`, i.e. k groups of three digits then one lone digit.
Observed: 2 groups (9 chars, 86%) or 3 groups (13 chars, 14%).
Digit ranges: 1st digit of a group h ∈ 2..6, 2nd a ∈ 2..4, 3rd b ∈ 2..4 with the
hard structural law **b ∈ {a-2, a-1}** (verified over 2192 groups).

## Answer format
An ASCII picture. `#parts(clue) == #blocks(picture)`. Each block is:
* one **separator row** — `=` everywhere, `v` on the first *and* last column of
  every item in that block's **top** row;
* `h` **content rows**. Items are rectangles of one repeated capital letter,
  **top-aligned** (they hang from the separator), separated by at least one `.`.
All rows in a picture have the same width.

## The rule (confirmed 100%)
For block *i* (all but the last):
* `h` = number of content rows (= tallest item in the block)
* `a` = number of items reaching the block's **bottom** row (full-height items)
* `b` = how many of those `a` items **horizontally overlap (≥1 column) an item
  of the block directly below**

The last block has nothing below it, so only its height is specified; its
contents are free. Letters, item widths, gap widths and the picture width are
all free — the checker only re-derives `h/a/b`.

## Construction used
Slot grid, pitch 2, item width 1 (so items in different blocks overlap iff they
share a slot). Block i takes slot interval [o_i, o_i+a_i-1] with
`o_{i+1} = o_i + (a_i - b_i)` → exactly `b_i` shared slots. If block i+1 is too
narrow to absorb b_i overlaps (only possible when b_i=3, a_{i+1}=2) it gets
height-1 filler items on the leftover slots of block i — fillers do not touch
its own `a`. Last block gets `max(1, b_{m-1})` items.
Verified on 189,650 synthetic clues + all 778 observed clues: 0 mismatches,
max answer length 699 ≤ 1024, ~14 µs/answer.

## Rounds
| round | strategy | answered | correct |
|---|---|---|---|
| 1 | skip everything (harvest 1026 clues) | 0 | 0 |
| 2 | wrong model (a=bottom count, b=#gaps≥3) + 4 diagnostic variants | 406 | 9 |
| 3 | correct model, item width 2 pitch 3 | 459 | 459 |
| 4 | width2/pitch3 vs width1/pitch2, alternating | 615 | 615 |

Round 2's 9 accidental hits were the key: they told me *which* block layouts my
wrong model got right, and the pattern (block1 needed exactly 3 wide gaps,
block2 exactly 2) only made sense as a relation *between* neighbouring blocks.

## Demos spent
1. before round 1 — the whole format (blocks, separator rows, top-aligned items)
2. after round 1 — a second (clue, picture) pair; comparing the two fixed
   `h` = block height and `a` = bottom-row item count, and gave me the four
   labelled blocks I fitted `b` against.
