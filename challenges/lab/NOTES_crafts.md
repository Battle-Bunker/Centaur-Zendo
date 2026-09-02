# Direction: crafts and hands-on physical intuition (crafts-agent)

Braids and plaits, shoelaces and knots as over/under crossings, folded-and-cut paper,
stacked cups, shadows, mirror lines, poured water, balance scales.

Target shape, from `sim/DESIGN_LOOP.md` and the two prior landings (`murn` on target,
`orlan` too hard):

* the demo is a **little ASCII picture a kid names instantly**;
* the clue is **tiny** and pins an **arbitrary-but-natural measurement** of that picture,
  never the object's famous operation and never something with a name;
* the answer is a **whole picture the player must build**, seeded by the clue, so the
  minimal witness is not a constant string;
* a **local, invisible-in-positives law** supplies the depth (murn's "exactly two
  supports, and nothing rests on its own kind"), because demos only ever show
  satisfying examples;
* and — the `orlan` lesson — the hidden quantity must be **something the player can see
  in the picture**. A 0/1 channel only tests hypotheses the player already generates.
  Put the quantity on the page; take the difficulty back in the law and in the count.

## Brainstorm (12), each against the 12-year-old test

The test has two halves: **(A)** a kid names the object from one demo; **(B)** once named,
the pinned pattern still has no name and takes real experimentation.

1. **Plait / braid of K lettered strands, drawn as crossings** — *chosen, `velk`.*
   Picture: a row of strand letters, then alternating "crossing" rows and strand rows.
   A crossing row carries one `\` or `/` in the gap between the two strands that swap,
   `|` for the strands standing still. The drawn diagonal is the strand you can *see* —
   i.e. the one in front (the standard knot-diagram convention: the unbroken line is over).
   **(A)** letters swapping places with a slash showing who slid in front: "the strands
   are crossing over each other, that's a plait". **(B)** the clue pins *how many times the
   strand that starts on the far left comes out in front*, and two sequencing laws
   ("you can't be the front strand twice running", "you can't cross the same pair twice
   running") that positive examples can never reveal. None of the three is nameable, none
   is the braid's famous operation (which would be "undo it" / "Artin generators" /
   "what permutation does it make"). The picture is a strict grid ⇒ cheap to verify.

2. **Weaving / plain-weave mat** — grid of `|` (warp over) and `-` (weft over); laws "no
   thread floats over more than two" and "every thread is tied down somewhere"; clue pins
   e.g. the number of single-cell pokes. **(A)** excellent — `|-|-|-` really does look
   woven. **(B)** weak: a binary grid with run-length constraints plus a motif count is
   read by any model as a nonogram/Binairo CSP, which DESIGN_LOOP names as an anti-pattern,
   and once framed that way it is solved by search rather than insight. **Rejected**, kept
   as a fallback flavour for the same skeleton if 1 turns out unrecognisable.

3. **Folded-and-cut paper (snowflake)** — answer: the unfolded sheet as `#`/`.`; laws:
   mirror-symmetric about the fold, no hole may touch the outside edge (or the snowflake
   falls apart), paper stays in one piece; clue pins how many hole cells sit on the fold.
   **(A)** superb, instant. **(B)** fails: the unfolding *is* the famous operation, so
   demo 1 hands over the symmetry law, and what remains ("count the holes on the fold") is
   a one-hypothesis guess. The connectivity clause that would restore depth needs a flood
   fill, which does not fit a 512-char scorer. **Rejected.**

4. **Shoe lacing** — two columns of eyelets, the lace zig-zagging, crossings drawn over/
   under. **(A)** instant. **(B)** good in principle ("how many crossings does the lace
   that starts at the bottom-left make in front"), but the picture is a *path*, and
   verifying that an arbitrary drawing is one continuous lace threading each eyelet once
   is path-tracing — well over 512 chars. **Rejected on the scorer budget**; idea 1 is the
   same physics on a grid that parses in one pass.

5. **Shadows from a lamp** — objects on a shelf, a lamp, shadows on the floor; clue pins
   how many objects have a shadow touching another's shadow. The *measurement* is lovely
   and genuinely unnameable. But the law is either the real projection rule (recognised
   from the first demo — it is the famous operation) or an invented ray law, which is
   geometry/arithmetic wearing a craft hat. **Rejected**, measurement noted as reusable.

6. **Mirror line** — a picture plus a mirror; draw the reflection. The famous operation
   *is* the whole rule; one demo ends it. Making the mirror lie (offset, delayed, colour-
   swapping) is arbitrary rather than worldly. **Rejected.**

7. **Water poured between cups** — vessels of different sizes, a pour sequence, clue pins
   how many end up exactly full. This is the jug/measuring-pour puzzle; every model has it
   memorised, and the search is small. **Rejected** (also rejected by the physics agent for
   the same reason).

8. **Balance scale with drawn objects** — clue pins the tilt or a torque. Any non-obvious
   weight table is a 26-entry lookup nobody can infer from six demos; alphabet-position
   weights are the arithmetic version we are told to avoid. **Rejected** (agrees with
   NOTES_physics.md #4).

9. **Stacking cups / plates** — nested trapezoids `\___/`; law: a cup may only sit on one
   at least two wider; clue pins how many rims are exposed. **(A)** good. **(B)** the whole
   object collapses to a list of widths — a numeric rule, not a picture — and the drawing
   is expensive to parse. **Rejected** (the same failure as the physics agent's "angle of
   repose").

10. **Friendship-bracelet knot chart** — the 4-knot chart (forward, backward, fw-bw,
    bw-fw) on a diagonal grid. **(A)** a kid who makes bracelets names it instantly; most
    do not. **(B)** the knot table is knowledge, not insight — exactly the "obscure
    knowledge" DESIGN_LOOP forbids. **Rejected.**

11. **Paper chain / cut-out dolls** — a strip folded, one figure cut, unfolded to a row of
    joined figures; law: the figures must stay joined at the fold. Same defect as 3 (the
    operation is the rule) and the answer is almost determined by the clue, so the scorer
    degenerates into an equality check rather than a property test. **Rejected.**

12. **Knitting: rows of knit/purl** — clue pins how many stitches are worked into the
    stitch below of the other kind. **(A)** weaker than 2 (rows of `V` and `-` do not
    read as knitting to a non-knitter). **(B)** reduces to the same binary-grid CSP as 2.
    **Rejected.**

## Why 1 wins

* It is a **picture of a physical thing** whose glyphs are self-describing: letters are
  strand names, `|` is a strand standing still, `\` and `/` are the strand you can see
  sliding in front. Nothing has to be memorised to read it.
* The clue is **6 characters** (`KQRM|3`) and everything the scorer needs is in it.
* **Three independent things to discover**, none of them nameable, none of them the
  braid's famous operation:
  1. what `\` and `/` mean (which of the two strands is in front) — a *semantic* layer
     that a positive example alone cannot settle, since both marks occur in every demo;
  2. the two sequencing laws — "the strand that came out in front may not come out in
     front again at the very next crossing" and "the same neighbouring pair may not cross
     twice running" — invisible in positive examples, and the first of them **kills the
     naive minimal witness** (a braid whose crossings are all "X in front");
  3. the count — *how many crossings does the strand named by the clue's first letter come
     out in front of*, with two decoy families in every demo (crossings where that strand
     goes **under**, and crossings it is not part of at all).
* Per the `orlan` post-mortem, the hidden quantity is **drawn on the page**: over/under is
  visible in every crossing of every demo, so the hypothesis is one a player can actually
  generate. The difficulty is in the laws and in *which* crossings are counted.
* The answer is anchored on the clue (row 0 is the clue's letters spaced out), so no
  constant string, no reused demo, and every answer must be built.
* The picture is a strict grid ⇒ the scorer is a single forward pass, no search.

---------------------------------------------------------------------------
## `velk` — the rule (private)

Clue `LETTERS|n`: 4 or 5 distinct capitals (the strands, left to right at the top of the
plait) and a number `n` in 2..6.

Answer: the plait, as text rows.
* Row 0 is the strands spaced out, exactly the clue's letters: `K Q R M`.
* Then, repeating: a **crossing row**, then the new **strand row**.
* A crossing row has exactly one mark, `\` or `/`, in the gap column between the two
  neighbouring strands that cross; every other strand shows `|` at its own column; the two
  crossing strands show nothing at their own columns (they are in the crossing). The
  strand row underneath is the row above with those two letters swapped.
* **`\` means the left strand of the pair passes in front; `/` means the right one does.**
  (The line you can see is the one in front — the knot-diagram convention.)
* **Law 1**: the strand that passes in front at one crossing may not pass in front at the
  next crossing.
* **Law 2**: two consecutive crossings may not be at the same gap (no unpicking).
* **Count**: exactly `n` of the crossings must have the strand named by the clue's **first
  letter** passing in front.

```
K Q R M          <- the four strands
 \  | |          <- K and Q cross; K is in front (the visible line goes down-right)
Q K R M
| |  /           <- R and M cross; M is in front
Q K M R
|  \  |
Q M K R
```

Intended discovery path: demo 1 gives the layout and the clue-row anchoring; the swap
consistency follows immediately. `n` is then the hunt — "number of crossings" and "number
of `\`" both die on their first probe, and "crossings involving the first letter" dies
soon after; only "crossings where that strand is in front" survives, and that requires
reading `\`/`/` as over/under rather than as decoration. Laws 1 and 2 never show up in a
demo, only in a 0 for an otherwise well-formed answer.

Degenerate witnesses closed: the empty string, the clue, the clue row alone (needs at
least one crossing and `n >= 2`), any constant picture (row 0 must match the clue), the
demo answer re-sent for a different clue, and — the important one — "make exactly `n`
crossings and put the clue's strand in front every time", which Law 1 forbids outright,
so a scoring answer must interleave crossings that do **not** count.

(Implementation, validation, self-tests and arena details are appended below as the
iterations run.)

---------------------------------------------------------------------------
## velk v1 — implementation, validation and self-test (iteration 1)

`challenges/lab/velk.json`.
`python tools/quickcheck.py challenges/lab/velk.json --seeds 400`
→ `OK velk  gen=0.08ms score=0.06ms solve=0.34ms`, **no warnings**.
Sizes: **score 493/512**, solve 2233/5000, generate 167/50000; clue ≤ 8 chars;
answers 7–43 rows, ≤ 489 chars.

What a player sees (a real demo, clue `PYDGE|3`, tail):

```
P Y D G E
| |  /  |
P Y G D E
 /  | | |
Y P G D E
| | |  /
Y P G E D
| |  \  |
Y P E G D
 \  | | |
P Y E G D
```

Generator: 4/5/6 distinct capitals (uniform-ish 40/40/20) and `n` uniform in 2..6; every
(strand set, n) pair in that range is satisfiable (checked exhaustively for K=4..5,
n=2..8, 60 random letter sets each: 0 failures). `solve()` chooses the plait length at
random and places the `n` counting crossings as a **uniformly random non-adjacent subset**
of the positions (the standard gap bijection), so they are spread through the picture
instead of clustering at the front, and every demo also shows the counted strand going
**under** and **standing aside** — the two decoy families.

### Adversarial self-test (1500 fresh clues, `$SCRATCH/velk/adv.py`)

Hypotheses a player might hold, each solving *its own* version of the puzzle:

| answer built from | scores 1 |
|---|---|
| **the exact rule, one-pass greedy — fairness floor** | **100.00 %** (0.03 ms/answer) |
| right count + law 2 only (no same gap twice, but a strand may lead twice) | 21.80 % |
| right count + law 1 only (no strand in front twice running) | 18.60 % |
| "n = crossings where the LAST strand is in front" + both laws | 12.33 % |
| both laws, count ignored | 9.67 % |
| "n = crossings involving the 1st strand" + both laws | 8.87 % |
| "n = crossings where the 1st strand goes UNDER" + both laws | 7.73 % |
| "n = number of `\` marks" + both laws | 6.87 % |
| right count, neither law | 3.33 % |
| both laws + count, but `\` read as *right*-over (mark semantics inverted) | 2.80 % |
| format only (legal-looking swaps, no laws, count ignored) | 0.47 % |
| "n = number of crossings" (a plait of exactly n crossings) | **0.00 %** |
| naive minimal witness: n crossings, the 1st strand in front every time | **0.00 %** |
| best constant answer (60 candidates x 400 clues) | 0.25 % |
| a demo answer replayed under the next clue | 0.00 % |
| `""`, `" "`, `"0"`, `"x"`, `"1"*100`, `"0"*1024`, `"\n\n\n"`, `"?"*400`, the clue itself, the strand row alone, the strand row + one crossing row, that pair repeated 4x, 128 copies of a strand row, 128 copies of a crossing row, non-ASCII | 0.00 % |

Nothing short of the exact rule reaches 22 %, and the 3–22 % band is a genuine gradient: a
player who has found *the count* but neither law already sees 3 %, and each law found
roughly doubles it, so there is something to climb — the failure mode that killed `orlan`
(no signal at all until the whole law is right) does not apply here.

The two 0.00 % rows are the ones the design is built around. **Law 1 makes the naive
minimal witness impossible**: "make exactly `n` crossings and put the clue's strand in
front every time" needs `n` consecutive crossings led by the same strand, which the law
forbids for every `n >= 2`, so any scoring plait must interleave crossings that do not
count and is at least `2n-1` crossings long.

### Correctness and robustness
* **Cross-check**: an independent re-implementation of the intended rule (written from the
  prose, not from the 493-char scorer) agrees with the shipped scorer on **8400
  (clue, answer) pairs** — reference answers plus 21 mutations each (mark flips, row
  reversal, truncation, character substitutions, filler swaps, case changes, CRLF,
  padding) — **0 disagreements**.
* **Cosmetic tolerance**, 300/300 accepted for each of: trailing newline, trailing blank
  lines, leading newline, CRLF, trailing spaces on every row, blank lines at both ends.
  Leading indentation is *not* tolerated (deliberately strict; every demo shows the exact
  layout).
* **Junk**: never raises, never returns non-0/1, never scores 1. Worst single `score`
  call over all junk and 1024-char inputs: **0.022 ms** (cap 50 ms).
* `generate` is deterministic (checked by quickcheck over 400 seeds) and 0.08 ms.
* End-to-end on the real engine (throwaway arena, torn down): pool loaded 1 accepted /
  0 rejected, one 0.5 s round presents **634 velk challenges**, the default random
  strategy scores **0/634**, and `player.py demo velk` returns a scoring plait.

### Hardening dials held in reserve (if both players crack it early)
1. **Narrow the count to a direction**: `n` = crossings where the clue's strand passes in
   front **of a strand to its right** (mark `\` *and* it is the left one) — a LegoZendo-
   style intersection of two conditions, with three decoy families instead of two.
2. **Make law 1 per-strand**: every strand must alternate front/behind over the crossings
   it takes part in (masonry-style, the analogue of murn's staggering) — this invalidates
   whole families of placement policies rather than single moves.
3. **Anchor the finish too**: require the bottom strand row to be a given permutation,
   pushing the answer from "a legal walk of the right length" to "a legal walk that also
   lands somewhere", at the cost of ~5 clue characters.

### Softening dials (if neither player gets traction)
1. Draw the counted strand's crossings with the strand's **letter** in the gap instead of
   `\`/`/` — the quantity then reads straight off the page (the `orlan` post-mortem's
   option (b)), leaving all the difficulty in the two laws.
2. Drop law 2, or lengthen `solve()`'s plaits so the laws are easier to see as invariants.

### Iteration-1 arena status
Arena `lab-velk-1` is set up and the server is **running**; the Agent tool for spawning
player agents is not available in this designer session, so per the `sim/DESIGN_LOOP.md`
fallback the loop stops after step 3. Everything the orchestrator needs (team directories,
filled-in briefs, teardown/report commands, and how to read the resulting hit-rates) is in
`sim/results/lab-velk-1/HANDOFF.md`.
