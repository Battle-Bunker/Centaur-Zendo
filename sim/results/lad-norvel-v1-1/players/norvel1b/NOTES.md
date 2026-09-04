# NOTES — team norvel1b — challenge class: `norvel` (the only class in the pool)

## Demo 1 (spent before round 0, because the demo window is consumed by starting a round)
clue    : `x..xxx...x...x..x..xx..x/2`
solution:
```
  bass |x..x|xx..|.x..|.x..|x..x|x..x|
  clap |.xx.|x.xx|x.xx|....|xxx.|..xx|
shaker |..x.|.xxx|x.xx|x..x|.xx.|.xx.|
```

## Narrating the picture to my 12-year-old partner
"It's a drum machine. Three rows of little boxes, one row per drum: bass, clap,
shaker. An `x` means 'hit that drum right now', a dot means 'stay quiet'. Time
runs left to right, 24 tiny moments, chopped into six boxes of four so you can
count 1-2-3-4, 1-2-3-4 like a song. The clue is a strip of x's and dots with a
`/2` stuck on the end."

### The three things a kid notices first
1. **"The top row IS the clue."** The bass row, with the `|` walls rubbed out,
   is character-for-character the clue. (Confirmed by script.)
2. **"There's never more than two x's stacked on top of each other"** — and the
   clue says `/2`. Never a column of three.
3. **"One box is completely empty"** (clap, bar 4 = `....`), and there is exactly
   one moment (step 14) where *no* drum plays at all.

### Kid-first hypotheses (test these before my own)
* K1 (from #1): the bass row is just the clue copied out. -> looks certain.
* K2 (from #2): the number after the slash is **how many drums may hit at the
  same moment**. -> main hypothesis.
* K3 (from #3): silence is allowed, so there is no "every moment must have a
  drum" rule; and the clap/shaker rows look *doodled*, not copied — so probably
  many answers are accepted.

## Current hypothesis (confidence)
- Format: `{label:>6} |xxxx|xxxx|...|` one line per track, `\n`-joined. (high)
- bass == clue pattern. (high)
- `/N` = max simultaneous onsets. (medium) — rival: `/N` = number of *extra*
  tracks beyond the bass (also fits N=2, 3 rows). Need clues with N != 2.

## Next test (round 1)
Cycle 8 answer variants by index, all in the demo's exact format, to separate:
all-quiet vs exactly-N-columns vs over-N columns vs dense-random-capped.

---

## Final state (all 6 rounds + final used)

| round | presented | answered | correct | hit-rate |
|---|---|---|---|---|
| 1 (8 blind variants) | 464 | 464 | 1 | 0.2% |
| 2 (family sweep: rows, column cap, density) | 463 | 463 | 14 | 3.0% |
| 3 (no-silence cap-2 builder, (p1,p2) sweep) | 656 | 656 | 69 | 10.5% |
| 4 (fine (p1,p2) sweep) | 620 | 620 | 151 | 24.4% |
| 5 (controlled kick-accompaniment) | 462 | 462 | 117 | 25.3% |
| 6 (two knobs, 2x samples) | 581 | 581 | 195 | 33.6% |
| **FINAL** | 2861 | 2861 | **1022** | 35.7% |

## What `norvel` is (final belief)
Clue `<kick>/<N>`: a 16/20/24/28-step kick pattern (always starts on `x`,
~40% density) and an integer N in 2..5 (independent of the pattern — the same
pattern turns up with different N).
Answer: a **three-voice drum grid**, `label |xxxx|xxxx|...|` per line. Labels,
padding and even a bar-number header line are ignored by the checker (the three
reference demos used `bass/clap/shaker`, `K/S/H` and `thump/snap/tick`+header).

Confirmed by experiment (each from a family that scored 0 out of ~60):
* row 1 must be **exactly the kick pattern** (high confidence)
* **exactly 3 voices** — 2 rows: 0/58, 4 rows: 0/58 (high)
* **never 3 voices in one column** — column-cap-3 family 0/58; across 1467
  answers, 0 hits at maxcol 1 and 0 hits at maxcol 3, 84 hits at maxcol 2 (high)
* **no completely silent step** — 81/84 early hits had zero silent columns (high,
  though demo 1 itself has one, so it is a strong preference, not absolute)
* the rest is a softer "groove" judgement I never pinned down: best random
  generator tops out near 36%, and one demo violates almost every crisp rule I
  fitted. What helps, measured: ~30-45% of kicks doubled by one other voice and
  shared between them; both other voices playing together on most kick rests;
  when only one of them plays on a rest, always the same one. What N does is
  still unknown (medium-low confidence) — early on, hit-rate fell like p^N, but
  once the generator was right the N-dependence largely disappeared.

## Demos used (3, one per window; all spent on `norvel` — the only class)
1. before round 1 — collapsed "no idea" to "drum grid, row 1 = clue".
2. after round 1 — different labels (K/S/H) proved labels are cosmetic, and N=4
   with still 3 rows killed "N = number of voices" / "N = column cap".
3. after round 2 — third label set plus a bar-number header proved the checker
   only reads the x/. rows; gave a third known-good grid for the feature search.
