# Direction: toys and building — SECOND pass (2026-09-05)

First pass: `NOTES_toys.md` (14 candidates, chose **virel** — a brick wall, "a brick resting on
its twin"). None of its 14 candidates is re-used here, and the class below shares nothing with
virel: different object, different geometry (a half-offset triangular lattice, not courses),
different verb, and the answer is an *edit of the clue's picture* rather than a new row.

House style this pass must obey (`sim/DESIGN_LOOP.md`, "The checksum caption", measured over 12
Opus finals):

1. the clue is the FINISHED object, named in two seconds;
2. the answer is that picture with the smallest physical edit, governed by ONE clause;
3. the caption names the verb and COUNTS the edits, so it is an offline checksum;
4. ~12 % of clues have n = 0, so the echoed clue scores (the format foothold);
5. **the RENDERING of the edit must need the demo** — this is where durnel v1 (arrow swap, 100 %
   blind) and molvic (swap edit, 100 %/100 % blind) died and where fennick (11 % blind, ~95 %
   with one) lives;
6. every demo shows the positive case beside its near-misses in one picture.

## Brainstorm (11 candidates, each against the 12-year-old test)

T1 = a kid names the object in two seconds. T2 = the pinned relation has no name and is not the
toy's famous operation. T3 (new this pass) = **could a player who guesses the rule from the
picture still not draw the answer?**

1. **Marble run — which marbles reach the cup.** T1 9/10. T2 **fail**: tracing a ball down a
   run *is* the toy's famous operation and a stock puzzle genre; and the answer is not a small
   edit (every marble moves). Rejected in the first pass too. *Reject.*
2. **Domino run with gaps — which dominoes fall before the chain breaks.** T1 10/10, T2 fail
   (chain simulation, and "a taller domino reaches further" is the famous fact), T3 fail (the
   rendering is a tilt mark — fennick's, already in the pool). Also the verb "fall" is taken.
   *Reject.*
3. **Skittles and a ball — which fall.** Same three problems as 2, plus the answer depends on an
   invisible ball path. *Reject.*
4. **Tower of stacked blocks — which overhang and topple.** T1 10/10; T2 marginal — the
   measurement a model reaches for is centre-of-mass overhang, which is the famous fact, and any
   arbitrary substitute ("it is standing on a wobbly one") still renders as a column of
   rectangles, i.e. **virel's picture**. *Reject on collection diversity.*
5. **Jenga tower — which blocks can be pulled.** T1 7/10 (a plan view reads as a table, and the
   rule "the layer above must be complete" is the game's own rule). *Reject.*
6. **Train set with points — which carriages get shunted to the siding.** T2 ok, but transport is
   durnel's direction and kaldrin is already a goods train. *Reject on crowding.*
7. **Jigsaw with a piece the wrong way round.** T3 excellent (a rotated 2×2 block is the least
   guessable rendering in the whole brainstorm), but T1 drops to 6/10 (a grid of tab/blank glyphs
   reads as a table — the salience failure that scored molvic v2 2.67 with the judge), and "the
   pieces that break the pattern" is nameable. *Reject; best of the rejects.*
8. **Kite-string tangle / spinning top.** T1 fine, but neither draws in ASCII as a thing with
   countable parts. *Reject.*
9. **Toy crane lifting what fits its hook.** T1 8/10, T3 good (a lifted crate is drawn hanging),
   but one hook means one edit per picture, so there is no count and no checksum. *Reject.*
10. **Stack of nesting cups — which cups go inside their neighbour.** T2 fail: "it fits if it is
    smaller" is *sorting*, a named property. *Reject.*
11. **A PYRAMID OF PLASTIC CUPS, some cups taken away — which cups slide into the gap under
    them.** T1 10/10 (a party/speed-stacking cup pyramid; the picture is a triangle, a geometry
    no class in the collection uses). T2 good: "a cup with a gap under one side and nothing
    sitting on top of it" is not a named property, and it is *not* the famous fact about stacks
    (which is about the whole thing collapsing). T3 **very** good: three independent surprises in
    the rendering — the cup moves DOWN into the gap rather than falling over where it stands, it
    ends up **on its side**, and the glyph says which way it went (`<__|` / `|__>`).
    **CHOSEN — `felsim`.**

## Chosen: `felsim` (neutral name; not a word, no pun, unique in `challenges/` + `challenges/lab/`)

### The picture

Cups sit on a half-offset lattice: the bottom row is on the table and always full, and row *k*
(0 at the table) starts at column 2*k*, its slot *j* occupying columns 2*k*+4*j* … +3. A cup is
`\__/`, an empty slot four spaces. Six rows, 11–13 cups along the bottom, 44–52 columns wide.
Nothing is ever drawn with *both* slots under it empty, and rows never get wider going up, so the
picture is always a physically possible pyramid with cups missing.

### The rule (one clause a kid says in one breath)

> **A cup with a gap under one side and nothing sitting on top of it slides into that gap and
> ends up on its side.**

It leaves its slot empty and appears in the gap as `<__|` if it slid left, `|__>` if it slid
right. A cup on the table row has no supports at all, so "exactly one missing" is false and it
never tips — no extra clause needed. Everything is judged from the clue in **one pass**: one bump
of the table, not a chain.

### One demo as it renders (seed 507)

```
clue                                          answer
              \__/        \__/                              \__/
            \__/\__/\__/    \__/                          \__/\__/    <__|\__/
      \__/\__/\__/\__/    \__/    \__/              \__/\__/\__/\__/|__>\__/
    \__/\__/    \__/\__/\__/\__/    \__/          \__/\__/    \__/\__/\__/\__/<__|\__/
  \__/\__/\__/\__/\__/\__/    \__/\__/\__/      \__/\__/\__/\__/\__/\__/    \__/\__/\__/
\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/  \__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/
============================================  ============================================
3 tip                                         3 tip
```

Three cups move, and the same picture carries every near-miss:

* row 5 slot 4 → slides **left** into row 4 slot 4 (`<__|`); row 4 slot 3 → slides **right** into
  row 3 slot 4 (`|__>`); row 3 slot 7 → slides **left** into row 2 slot 7 (`<__|`).
* **stays**: row 4 slot 5 is missing a support, but the cup on top of it is row 5 slot 4 — the
  cup that just slid away. A chain reaction would take it next; one bump does not. (Planted in
  100 % of clues with n > 0.)
* **stays**: row 3 slots 1 and 2, row 2 slots 5 and 6 — each missing a support, each weighed down
  by a cup that stays put.
* **stays**: cups on two supports standing right beside a gap in their own row (100 % of clues).

### Intended discovery path

1. The caption names the verb and counts the edits, so a player harvests ~70 clues in round 1 and
   tests candidate rules offline. Measured over 4000 clues, no rival statistic reproduces *n* in
   more than 16 % of clues, so ten harvested clues kill every one of them: the rule is findable
   from the clue alone.
2. But the *drawing* is not. The true rule drawn upright in the gap, or as `/--\`, or tipped in
   place, or with the cup simply removed, all score 13.5 % — i.e. the `0 tip` clues and nothing
   else. One demo shows the whole convention in one look.
3. So the split the format wants: a demo-less player banks the foothold and can even hold the
   right rule and still score 13–17 %; a player who spends a demo here should crack it.

### Witness table (2000 fresh clues, shipped scorer, quickcheck exec model)

Every template is drawn with the TRUE convention, i.e. it models a player who has seen a demo.

| template | score |
|---|---|
| the true rule (`solve`), caption kept / dropped / padded / +newline | **100.0 %** |
| the clue echoed unchanged (= the `0 tip` clues) | **13.5 %** ← the foothold |
| any cup missing a support, no weight clause | 0.0 % |
| any cup with nothing on top | 0.0 % |
| a gap beside it in its own row | 0.0 % |
| only the top row tips | 13.5 % |
| n random cups | 13.6 % |
| they keep settling, tipped cups inert (**the chain**) | **19.5 %** ← best rival |
| they keep settling, a tipped cup can slide again | 15.5 % |
| they keep settling, one cup at a time | 14.8 % |
| TRUE rule drawn upright in the gap / as `/--\` / as `/~~\` | 13.5 % |
| TRUE rule, always `<__|` / always `|__>` | 16.9 / 17.1 % |
| TRUE rule, slide marks mirrored | 13.5 % |
| TRUE rule, tipped in place / kept as well / simply removed | 13.5 % |
| wrong rule AND obvious rendering (missing support, upright) | 0.0 % |
| demo replay (a fixed answer, with or without this caption) | 0.1 % |
| another clue's answer | 0.0 % |
| mirrored / upside down / row dropped / row doubled / shifted a column | 0.0 % |
| no table row / junk line added / spaces squeezed or stripped / double spaced / upper-cased | 0.0 % |
| `_` swapped for `-` / caption twice / blank line in front | 0.0 % |
| empty, `x`, `0`, `1`×100, 4000 junk chars, the caption, the table row | 0.0 % |

Nothing exceeds 19.5 %, and the two rungs above the foothold (the chain reading at 19.5 %, a
fixed slide mark at 17 %) are both "nearly there", which is the gradient lever 7 asks for.

### The caption as an offline checksum (4000 fresh clues)

How often each rival statistic equals *n*: cups on two supports with nothing on top 16.1 %, cups
missing a support in the top row 11.5 %, the chain-reaction count 11.5 %, weighed-down precarious
cups 10.0 %, rows that have a gap 8.0 %; gaps in the picture, cups in the picture, cups with
nothing on top, cups in the top row, gaps in the top row, cups missing a support, cups with a gap
beside them, gaps a cup could slide into — all **0.0 %**. Over ten harvested clues every rival is
below 0.0001 %.

### What one demo shows (share of clues with n > 0)

a weighed-down precarious cup that does not tip **100 %**; a cup a chain would take next that does
not move **100 %**; a cup on two supports, nothing on top, beside a gap **100 %**; a tip below the
top row **100 %**; both slide directions **91.3 %** (n = 1 clues cannot show both). `generate`
also rejects two cups tipping into the same gap and any answer row that would come out empty.

### Validation

`python tools/quickcheck.py challenges/lab/felsim.json --seeds 200` → `OK felsim`, one warning
("score accepts the clue itself" — that is the `0 tip` foothold, deliberate). Sources: generate
4912, solve 764, score **501**/512 chars. 8000 fresh seeds: generate mean **0.66 ms** (p50 0.45,
p99 2.6, max 4.8 — measured while the box was at load average 6), 0 fallbacks, 7994/8000 distinct,
deterministic; solve mean 0.065 ms; score mean 0.063 ms on real answers and ≤ 0.073 ms on junk
(empty, 4 KB of junk, a 60-row picture). Clue 254–346 chars, solution 246–346. n spread:
0 12.8 %, 1 7.3 %, 2 25.4 %, 3 31.2 %, 4 14.5 %, 5 8.1 %, 6 0.7 %. `solve()` was cross-checked
against an independent, un-golfed re-implementation (parse → truth → render): identical on
300/300 clues, and the caption equals that model's tip count on 300/300. `solve()` emits nothing
but the edited picture — no template, no constant decoration, and another clue's answer scores 0.

### If it drifts

* **cracked without a demo** (the durnel v1 / molvic failure) ⇒ the rendering was guessed: make
  the slide mark carry more information — e.g. the cup lands *upside down* when it slides onto
  the table row and *on its side* higher up — or stop the caption saying `tip` and let it count
  something the picture does not name.
* **cracked by everyone with a demo and by nobody without** at rates above 80 % ⇒ harden by
  salience first: let the reach depend on the cup (a cup only slides if the gap is on its
  *downhill* side, i.e. towards the nearer edge of the pyramid), or count only cups that are not
  themselves standing on a gap.
* **nobody cracks it with a demo** ⇒ soften by drawing one cup already lying in its gap in the
  clue as a worked instance (fennick's and basten's lever), not by touching the rule.
