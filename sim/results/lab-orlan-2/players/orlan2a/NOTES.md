# orlan — findings

Single challenge class in the pool: `orlan`.

## Clue / answer format
Clue is a 5x5 / 5x6 / 6x6 grid, rows separated by `\n`, characters
`o` (our stones), `x` (enemy stones), `#` (walls), `.` (empty).
Answer is `r,c>r,c`, zero-indexed **row,col**, source > destination.

## Move model — SOLVED (confidence: high)
An `o` moves **two non-wall steps** in one of the four orthogonal directions.
`#` is *transparent*: it is skipped, it neither blocks the move nor counts as
a step. Both the intermediate non-wall cell and the landing cell must be `.`.

Evidence: all 60 known-correct answers (7 demos + 53 scored hits) lie in this
move set; a uniform random pick inside it scored 8/45 = 17.8% in round 6,
exactly the predicted mean(1/ncand) = 0.172. Distance is usually 2, and is 3
exactly when one `#` sits in the path (demos 5 and 6).

Rejected along the way: Lines of Action (distance = pieces on the line),
slide-until-blocked, zone-of-control slide, custodial capture — each fitted
the first few demos and was then refuted.

## Selection rule — NOT solved (confidence: low)
Roughly 4-9 legal moves per clue; exactly one is accepted. No lexicographic
rule over ~45 board features fitted all positives. Real but weak signals:

* source stone orthogonally adjacent to an `x`: 50% of answers vs 22% of
  candidates (2.3x enrichment, ~3.7 sigma) — "a threatened stone moves".
* answers are ~2x enriched at the *last* candidate in row-major scan order.

Shipped heuristic: minimise `(-srcx4, -r, c, -dir)` with dir = up,down,left,right.
Fit sample 57%, actual final 23% — substantially overfit but still well above
the 17% uniform baseline.

## Per-round record
| round | strategy | correct/answered |
|---|---|---|
| 1 | slide-move hypothesis bake-off (8 arms) | 1/89 |
| 2 | Lines-of-Action rankers (8 arms) | 5/85 |
| 3 | dist-2 jumps, line-count filter (overfit) | 12/91 |
| 4 | dist-2 jumps, uniform random (unbiased sample) | 12/87 |
| 5 | move-model bake-off (jump2 / zoc-slide / rook / rook<=3) | 3/84 |
| 6 | A/B: uniform vs enemy-approach ranker | 8/45 vs 9/45 |
| final | threat + positional ranker | 127/551 (23.0%) |
