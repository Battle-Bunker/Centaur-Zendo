# Direction: food and the kitchen (kitchen agent)

Brief: recipes and measuring cups, a lunch tray, a pizza cut into slices with toppings, a
table set for dinner, a fridge with shelves, a cake with candles, a row of jars, a tray of
biscuits. The demo must be a picture a kid names instantly; the clue is tiny and pins an
arbitrary-but-natural *measurement* that has no name and is not the object's famous
operation.

## What the ladder says worked, and what I took from it

Read before brainstorming: `ladder/REPORT.md`, `ladder/STARS.md`, `challenges/lab/NOTES_game.md`
(conclusion), `sim/DESIGN_LOOP.md`.

* The three classes in or near the target band (**virel** 57 %, **tovel** 66 %, **LegoZendo**)
  share exactly three properties:
  1. **a picture a kid names instantly** (a brick wall, a month page, a pile of Lego),
  2. **a seed from the clue visible inside the answer** (the bottom course, the month's
     shape) — this is what kills the degenerate witness, and
  3. **a count of an unnameable relationship between two drawn things** (a brick resting on
     its twin; two marks two days apart in the same school week; two same-letter bricks
     joined by one pin).
* The failures split into two kinds:
  * **abstract** — `quaich` (a stroke grammar) and `OKRIN` (letters in a knitted pattern):
    the "object" is notation, so a kid has nothing to hold onto and the models fall back on
    statistics.
  * **drawn so the object is not recognised** — `fennick` was a *bookcase*, but because the
    free variable was the heights it renders as a **bar chart**; players and the kid judge
    read columns of letters, not books. 1 % final, kid score 3.4.
  * `NOTES_game.md`'s conclusion: a 0/1 channel only tests hypotheses the player already
    generates. **The hidden quantity must be countable by eye in the demo picture.**

So the bar for every candidate below is: (T1) a kid names the object from ONE demo *as
drawn in ASCII*, not as described in words; (T2) the counted relationship is between two
things you can point at in the picture, and has no name; (T3) the clue seeds the answer so
that a well-formed picture is not enough; (T4) I can verify it in ≤ 512 scorer characters.

## Brainstorm (12 candidates)

1. **Tray pizza cut into slices.** The clue *is* the uncut pizza (crust border, cheese
   dots, two-cell toppings `mm`, `oo`, `pp`) plus a topping letter and a number. The answer
   is the same pizza with the cuts drawn in, `|` straight down through every row, so a
   topping the knife goes through is literally drawn as `m|m`. Count = **slices that hold
   two or more mushrooms, where a mushroom the knife cut in half counts for the slice on
   both sides of the cut**.
   T1: pizza/tray bake, instantly — the cuts are what make it a pizza rather than a grid.
   T2: no name; the famous operation of a pizza (cut it into equal slices / fair division)
   is *not* the rule, and equal slices are actively falsified in the demos. T3: the answer
   must reproduce the clue picture exactly, so the only freedom is where the knife goes —
   the completion shape of DESIGN_LOOP lever 1. T4: the scorer is a string comparison plus a
   run count. **Best candidate — implemented as `garrow`.**

2. **Fridge with shelves.** Shelves of fixed width, packed with boxes/jars of various
   widths; count boxes standing directly on a box of the same width. T1 fine. T2/T3 fine but
   this is **virel with jam jars** — same tiling-of-rows object, same twin-stack
   measurement. *Reject: duplicates a class already in the band.*

3. **Cake with candles.** Candles on top of a cake, cake cut into slices, count the slices
   whose candle count is odd / higher than both neighbours. T1 good. T2 **fail** — parity
   and local maxima are named, and single-row numeric strings pull every model hypothesis
   towards arithmetic. *Reject.*

4. **Layer-cake / club-sandwich cross section.** Stacked slabs (`bread/ham/cheese`), count
   layers of the same kind with exactly one layer in between. T1 good, T2 marginal, and it
   is **tovel's distance-2 relation** on a 1-D strip. *Reject as a re-skin.*

5. **Table set for dinner: passing the dishes.** People round a long table, dishes on it;
   you can reach your own side within one place, or straight across from you, and the count
   is the dishes nobody can reach (they have to be passed). T1 good if drawn with seats
   above and below the table. T2 *marginal*: "reach = distance ≤ 1" is a threshold rule and
   distance-to-nearest-thing is high in a model's prior for any board. T4: three different
   line kinds to parse in 512 chars. *Keep as the fallback if pizza drifts easy.*

6. **Row of jars with lids.** Jars of different widths, lids drawn as `___` above them;
   count jars wearing a lid that belongs to a jar next door. T1 fine but the drawing is
   widths-above-widths, i.e. **exactly fennick's failure mode** — it renders as two rows of
   bars. *Reject.*

7. **Recipes and measuring cups.** Ingredient amounts and a set of cups; count the
   ingredients you can measure exactly. T2 **fail** — this is coin change / numerical
   semigroups, straight out of the RLVR anti-pattern list. *Reject.*

8. **Tray of biscuits that spread while baking.** Dough balls of different sizes on a tray;
   count the pairs that merge in the oven. T1 good. T2 **fail** — "distance < sum of radii"
   is a named geometric predicate and is the first thing a model tries on a scatter of
   points. *Reject.*

9. **Egg box.** A 2×6 carton, some eggs missing; count something about the holes. T1 fine,
   but 12 cells carry almost no information: the whole answer space fits in a lookup table.
   *Reject: unique-answer classes starve the channel.*

10. **Lunch tray compartments.** A fixed tray template with foods in the wells; count wells
    whose food also appears in the neighbouring well. T1 good, T3 weak — the template is
    fixed, so a player copies one demo and only edits letters; the clue carries almost
    nothing. *Reject (low information, and it is LegoZendo's adjacency relation).*

11. **Shopping list vs the pantry.** Words: ingredients you have, a recipe you want; count
    the recipes you can cook. T1 **fail** — a list of words is not a picture, and the object
    is set covering. *Reject (quaich's failure: notation, not an object).*

12. **Stack of plates / pots and lids nesting.** Plates of decreasing diameter, count the
    plates resting on a plate exactly one size bigger. T1 good, T2 fine, but again this is
    virel's twin relation with round brackets instead of square ones, and a monotone stack
    has almost no free structure. *Reject.*

## Chosen: candidate 1 → `garrow`

The pizza is the only candidate that is simultaneously (a) a picture whose *identity comes
from the cuts* — a rectangle of dots and letters is a grid, but a rectangle of dots and
letters with knife lines through it and a crust is a pizza; (b) a completion task where the
clue is the object itself, so "well-formed picture" is worth nothing and only the knife
positions are free; and (c) host to a relation that is invisible to the naming instinct:
*two of the same topping ending up on one slice, with a halved topping belonging to both
sides.* A kid says "that slice got two mushrooms — and that one got cut in half so they both
get some". A model says "number of cuts / number of slices / how many mushrooms did the
knife go through", all of which are falsified in every demo by construction.

### The three clauses a player must find
1. **Format**: the answer is the clue picture with `|` inserted straight down through every
   row (same positions in every row). Visible from one demo — the kid-easy half.
2. **Well-formedness**: 4–8 slices, every slice at least 3 characters wide, and every slice
   has at least one topping on it ("nobody gets a plain slice"). Rejection-only clauses;
   demos never show a violation, so these cost probes.
3. **The count**: slices holding ≥ 2 pieces of the clue's topping, a cut piece counting for
   both slices. Every demo is rejection-filtered so that 16 rival readings differ from k.

### The trap that produces the partial tier
The natural core hypothesis, "slices with two or more mushrooms", is *false on every demo*
unless the halves convention is adopted, because every demo contains at least one mushroom
the knife went through and the no-halves count is forced to differ from k. A player who
tries the core hypothesis, sees it fail, and abandons the family lands nowhere; a player who
tries it and asks "what about the one that got cut?" finishes. That is the intended
gradient, and it is the same gradient as virel's "what is N counting?".

### Levers if it drifts
* **Too easy**: count only slices with ≥ 2 of the clue topping *and* nothing else on them;
  or forbid two cuts from being the same distance apart; or drop the letter from the clue
  and count over whichever topping is most common.
* **Too hard**: raise k's allowed frequency band (make the target count less rare among
  valid cuttings), or drop the "every slice has a topping" clause so the format gate is one
  clause shallower.

## Iteration record

* **v1 (`garrow`)** — built, validated and self-tested (see the report). No arena run in
  this session: the orchestrator opens it.

## garrow v1 ladder run `lad-garrow-v1-1` (2026-09-04, 6×0.5 s, 2 players)

| team | profile | final | demos | best training round |
|---|---|---|---|---|
| garrow1a | opus-default | 25% | 5 | 14% |
| garrow1b | opus-kidproxy | 6% | 4 | 12% |

Mean 15%: leaning too_hard, not yet classified (2 finals). Neither player found the rule.
Both read the numbers as something about the knife cutting pieces: 1a as "severed(L) = how many
L-dominoes a cut passes through" (empirically severed = n gives 29%, n−1 gives 12%), 1b as
"slices where L outnumbers the other topping". Both are shadows of the real count (slices holding
two or more pieces of L, a halved piece belonging to both sides) — 1a even wrote "the cut lines
slice *through* the little pairs, and it's the slicing that the clue is counting" without taking
the next step to "…so that slice now holds two". 1b called the scorer buggy because its own
(wrong) rule fitted all demos; the scorer is fine.

Both players said the kid-reading they missed was "the pieces don't have to be the same size" and
"why does *this* cut count?". Both also hard-coded 7 slices / widths 3–7 from two neat demos.
Softening levers if the next two finals stay low: (a) draw reference cuts with wildly uneven widths
so neatness is visibly irrelevant; (b) make the digit small (1–2) so a kid can point at the one
slice "with two mushrooms"; (c) let demos carry a halved piece next to a whole one of the same letter
in the same slice so "two of the same on one slice" is the headline picture.
Throughput note: ~50 challenges per 0.5 s round for both teams versus 400-800 on other classes. score() is 0.05 ms and
the server only calls generate() per item, so the bottleneck is generate() in the sandbox; worth profiling before the next run.

## garrow v2 — refinement after `lad-garrow-v1-1` (2026-09-04)

v1 kept as `challenges/lab/garrow.v1.json` (byte-identical copy); v2 is `challenges/lab/garrow.json`.
**The rule and the scorer are unchanged** (the scorer string is byte-identical to v1's). Everything
that changed is in `generate()` and `solve()` — i.e. in what the picture and the demos say out loud.

### What the two players actually did (from `sim/results/lad-garrow-v1-1/`)
Both got the object and both got the *neighbourhood* of the measurement, and neither took the last step.

* **garrow1a (opus-default, 25 % final, 5 demos)** settled on `severed(L)` = how many L-dominoes a
  cut passes through, with `severed == n` scoring 29 % in training and `severed == n-1` 12 %. Their
  own notes contain "the cut lines slice *through* the little pairs, and it's the slicing that the
  clue is counting" — one sentence short of "…so that slice now holds two". They then hunted for a
  "residual positional constraint" that does not exist, because in four of their five demos
  `severed == n-1` held exactly. **That off-by-one near-miss was the trap that ate the run.**
* **garrow1b (opus-kidproxy, 6 % final, 4 demos)** read the digits as "slices where L outnumbers the
  other named topping", verified it against every demo, and concluded the scorer was buggy. It is
  not: the belief is satisfiable but only worth ~7 %.
* Both hard-coded **7 slices and widths 3–7** from two neat demos; 1a's final search was over
  7-piece partitions with widths 3–7 only.
* Both named the same missed kid-reading: "the pieces don't have to be the same size" and
  "why does *this* cut count?".

### What v2 changes (softening levers, in the order the brief asked for)
* **(a) wildly uneven demo widths.** `solve()` now draws a cutting uniformly from all compositions
  of the tray width into n parts ≥ 3 (v1 sprinkled the surplus one column at a time, which piles up
  near-equal slices), and a grade-0 demo must have a slice ≥ 5 columns wider than its thinnest and a
  slice ≤ 4 wide. Demo width spread is now 8.1 columns on average, 98 % of demos ≥ 5, and all of
  4/5/6/7/8 slices occur (29/29/23/14/5 % of 600 demos). Hard-coding "7 slices, widths 3–7" is dead.
* **(b) small digits.** Both digits are 1–3 (389/435/376 over 600 clues; v1 ran to 6 with mode 3).
  "Two slices got two mushrooms" is pointable; "five slices got two mushrooms" is a miscount.
* **(c) the headline picture in every demo.** A grade-0 demo must show, in at least one *counted*
  slice, a halved piece sitting beside a whole piece of the same letter (`m|m` … `mm`). 94.5 % of
  demos are grade-0; 3.5 % fall back to a weaker demo. The intended sentence is now drawn, not
  inferred.
* **(d) the second topping is KEPT — measured, not assumed.** On v1 clues, a player who has only the
  format and cuts at random satisfies **one** count 25.3 % of the time and **both** counts 3.0 %. A
  one-letter/one-digit clue would hand a player who never gets past "bars in the picture" a 25 %
  floor — as much as v1's better player scored with a whole theory — and no witness table could stay
  clean. The two digits cost the kid nothing (they are two instances of the same sentence, not a
  second rule), so they stay, with both digits small.
* **(e) equal slices are never an answer.** `generate()` rejects any (k,j) pair that some equal-width
  cutting (3 roundings × 4–8 slices) achieves. The pizza's famous operation is falsified by
  construction: 11.2 % → 0.00 %.
* **(f) the severed shadow is killed inside a single demo.** v1 only forbade `severed == k`, which is
  how `severed == k-1` came to hold in 4/5 of 1a's demos. v2 requires the two named toppings to have
  *different* severed-minus-digit offsets, in the witness `generate()` keeps and in every grade-0
  demo, so no "severed = digit + c" law survives even one demo.
* **(g) a less busy tray:** 28–34 wide (was 30–38), 4–5 pieces a row (was 5–6), named letters with
  4–7 pieces (was 5–9). The judge's v1 advice ("does not read as pizza on sight") is only partly
  addressable without markers or text, which are out of bounds; a less crowded tray with visibly
  hand-cut slices is what is left.

### Witness table, 600 fresh clues per version, identical harness
| strategy | v1 | v2 |
|---|---|---|
| true rule (`solve`) | 100.0 % | 100.0 % |
| equal-width slices, best of 4–8 | 11.17 % | **0.00 %** |
| severed = n | 22.83 % | 11.33 % |
| severed = n−1 | 14.33 % | 6.50 % |
| L outnumbers the other topping | 7.50 % | 9.83 % |
| random well-formed cutting, 4–8 slices | 2.17 % | 3.50 % |
| one constant answer for every clue | 0.17 % | 0.17 % |
| demo replay (previous clue's answer) | 0.00 % | 0.00 % |

A second blind sampler drawing widths the way `solve()` does (uniform compositions) scores 4.1 % on
v2, so the floor is 3–4 %. Wrong-family theories are now worth 2–3× the floor instead of v1's 10×,
and the nearly-right ones are worth more: **3–4 % (no idea) → 8–12 % (the knife family) → 15–22 %
(right measurement, wrong halves convention) → 100 % (the rule)**. Rival table on v2 (250 clues,
built/scores): halves counted left-only 44/22.4 %, halves counted nowhere 34/14.8 %, any-x 30/3.6 %,
x severed 96/11.6 %, other severed 97/2.8 %, slices with no x 90/1.6 %, 2+ of any topping 26/0.0 %,
outnumbers 92/7.6 %. Junk and shape attacks are unchanged from v1 (same scorer) and re-confirmed at
0 % / 100 % on 300 clues.

### Timings (the arena served only ~50 items per 0.5 s round on v1 — generate() was the whole of it)
| | v1 | v2 |
|---|---|---|
| `generate` mean / median / max | 8.7 / 7.8 / 38.3 ms | **0.54 / 0.42 / 11.6 ms** (3000 seeds; 0.52/0.40/2.1 on the 600-clue run) |
| `solve` mean / median / max | 85.7 / 36.5 / 336.6 ms | 13.2 / 1.6 / 322 ms |

v1's `generate()` was doing solve-like work: 420 sampled cuttings per attempt, each scored piece by
piece with a bisect per piece, plus a 19-rival pass on each survivor. v2 keeps prefix sums of piece
columns, so one candidate cutting costs O(slices) instead of O(pieces); it samples 48, takes the
rarest qualifying count-pair, and does the rival work once. 3000 seeds: no empty clue, and
`score(clue, solve(clue)) == 1` on every one. `quickcheck --seeds 300`: OK, gen 2.09 ms max,
score 0.10 ms, solve 200 ms max. Sizes: scorer 474, solve 4997 (cap 5000), clue ≤ 214, solution ≤ 251.

### Prediction and what to do next
Predicted classification for the next 2-player run: **testing / on-target**, mean final 35–55 % —
one player crack (the headline picture is now in every demo and the severed decoy dies in demo 1)
and one partial at 15–25 % (right measurement, wrong halves convention). Predicted kid score **3.8–4.2**
(object still capped near 3 — a bordered grid of dots reads as a tray only once the hand-cut slices
are in; rule_statable, kid_contributes and fun all improve with digits of 1–3 and a drawn `m|m` next
to `mm`). Risk to watch: v2 pays wrong theories *less* than v1 did (severed 22.8 → 11.3 %), so if the
insight still does not land the measured mean can come out **below** v1's 15 % while the class is
genuinely easier to understand — read the players' NOTES, not just the number.

Levers left if it is still too hard: drop the "every slice has a topping" clause (worth ~2 % of the
format gate); force the two counted pieces of one letter into the **same row** in a demo
(`mm...mm` inside one slice) so the pair is readable along a line; force one digit to 1 always.
If it comes out too easy: raise the rarity band in `generate()` (currently the rarest count-pair
seen in 48 samples), or require the counted slice to hold nothing but that topping.

## garrow v2 ladder run `lad-garrow-v2-1` (2026-09-04, 6×0.5 s, 2 players)

| team | profile | final | demos | cracked |
|---|---|---|---|---|
| garrow1a | opus-lowdemo | 28% | 2 | no — geometry heuristics (4 pieces, narrow matching piece) |
| garrow1b | opus-theorist | 100% | 6 | round 5, by insight: "exactly n pens hold 2 or more L-animals, a cut animal counts for both" |

Mean 64% (v1 was 15%). First earned crack on this class. The theorist read the picture as a field
with fenced pens and animals (not pizza — the object is read consistently as "field + fences", which
is fine: the story is the same). Its kid lines: "You cut the sheep in half!" (took two rounds to
accept the game does not care) and "some pens have two of the same animal in them and some don't"
— the rule verbatim. The lowdemo player with 2 demos read the two clue pairs as describing ONE
piece, and its 28% is geometry (v2's softening made wrong theories pay less, as predicted).
Both again praised the grammar and asked for the index-cycling A/B trick to be in the guide (it is,
under `memory["_index"]`; make it more prominent).

Status: testing, mean over v2 64% (2 finals), over all versions 40% (4). One more Opus pair on v2
and it may calibrate. The 4–8 pens / no-empty-pen clauses were the theorist's only complaint
("why four to eight?") — a v3 could drop the pen-count bound if it stays clean.

## garrow v3 — the demo-economy pass for the 7-class / 3-demo format (2026-09-05)

v2 kept as `challenges/lab/garrow.v2.json` (byte-identical copy); v3 is `challenges/lab/garrow.json`.
**The rule is again unchanged** — every version of this class has changed only what the picture says
out loud. What changed is the budget the class asks for. v2's 64 % was earned under 6×0.5 s rounds
with 6 demos and a 272-answer designed experiment; the new format gives a class ~60 probes a round
for 4 rounds and a team only 3 demo requests for 7 classes, so v2 as it stood was unreachable.

### What v3 changes

* **One topping, one digit.** The clue is now `m2` over the tray. v2 kept two letters and two digits
  because on v1 clues a player who had only the format and cut at random satisfied one count 25 % of
  the time. Re-measured on v3: **8.6 %** (n drawn at random), 13.2 % (n = 6 always), 15.4 % (n = 5
  always). The 25 % is gone because `generate()` now picks, for each tray, a count that is *rare
  among random cuttings of that tray* — it histograms 48 sampled cuttings and keeps only counts
  occurring on 2–15 of them (4–31 %), rarest first. So the blind floor sits in the 5–30 % foothold
  band with a single digit, and the second letter/digit — the thing that made the clue look like a
  code — is dropped.
* **Every demo shows the counted relation in one look.** `generate()` keeps a tray only if it can be
  cut so that a counted slice holds **exactly two** pieces of the named topping with one of them
  halved by the knife, the neighbouring slice holds **just the other half**, and the slices are
  visibly hand-cut (one ≤ 4 wide, spread ≥ 5 between widest and thinnest). 97 % of demos are that
  picture with every rival reading dead; `solve()` additionally prefers (46 % of demos) a cutting
  that has a slice holding *three*, so "exactly two" is visibly not the rule.
  Requiring exactly-two on the counted slice is also what kills two rivals for free: that slice has
  only one whole piece, so "slices with two **whole** pieces" and "slices the topping touches at all"
  can no longer come to k in a demo. Severed ≠ k is required explicitly (v1's trap).
* **The 4–8 slice bound is gone.** The theorist's only complaint about v2 was "why four to eight?".
  The scorer now says only *at least four slices, each at least three wide*; the upper bound is
  whatever the tray allows (10–12) and demos run 4–9 slices. The table stayed clean: equal-width
  slices are still **0.00 %**, because `generate()` rejects any count achieved by *any* equal cutting
  of that tray for every n from 4 to width//3 (restricting that check to n ≤ 8 was tried: the
  equal-width row jumps to 12.7 % at n = 9–11, so the full range stays).
  The "no plain slice" clause is gone too — one clause fewer to discover, and demos now sometimes
  show a slice of pure cheese.
* **The tray reads as food.** Cheese is `~` instead of `.`, the crust is two columns thick at each
  end plus a solid row above and below, and toppings are 3 cells wide with three of them a row
  (v2: 2 cells, 4–5 a row). Fewer, bigger pieces on a textured base; no labels, no legend.

### One demo as it renders (seed 77)

```
clue:                                   answer:
b1                                      ###|###############|######|#####|###|####
####################################    ##~|~~~~ttt~~~~~~oo|o~~~~~|~~~~~|~oo|o~##
##~~~~~ttt~~~~~~ooo~~~~~~~~~~~ooo~##    ##~|~~~~ooo~~~~~~~~|~~~ooo|~~~~~|~~t|tt##
##~~~~~ooo~~~~~~~~~~~ooo~~~~~~~ttt##    ##b|bb~~~~~~~~~~~~~|~ttt~~|~~~~~|~bb|b~##
##bbb~~~~~~~~~~~~~~ttt~~~~~~~~bbb~##    ##~|~~ttt~~bbb~~~~~|~bbb~~|~~~~~|~~~|~~##
##~~~ttt~~bbb~~~~~~bbb~~~~~~~~~~~~##    ###|###############|######|#####|###|####
####################################
```
Slice widths 3/15/6/5/3/4; pieces of `b` per slice 1/2/1/0/1/1 → one slice holds two → `b1`. The
headline is the first cut: `##b|bb` — the knife halves a bacon, slice 1 gets the single half and
nothing else, slice 2 gets the other half *plus* a whole `bbb`, and that is the slice the digit
counts. Slice 4 is plain cheese (legal now), and the six slices are wildly uneven.

### Witness table (500 fresh clues, seeds 100000–100499)

A strategy "builds" an answer by searching up to 400 well-formed cuttings for one satisfying its own
law, then is scored by the real scorer; "built" is how often such a cutting was found at all.

| strategy | v3 |
|---|---|
| true rule (`solve`) | 100.00 % |
| **clue returned uncut** | **0.00 %** |
| **equal-width slices, any n, any rounding** | **0.00 %** |
| **random cut positions, n random** | **8.60 %** ← the blind floor |
| random cut positions, n = 6 always | 13.20 % |
| random cut positions, n = 5 always | 15.40 % |
| **"severed = n"** (v1's trap) | **9.80 %** (built 100 %) |
| **"slices the topping touches at all = n"** | **27.20 %** (built 92 %) |
| **"slices with two whole pieces = n"** (halves not counted) | **33.60 %** (built 34 %) |
| "2+, a half counting only for its left slice = n" | 44.20 % (built 46 %) |
| "slices with two of any one topping = n" | 13.20 % (built 100 %) |
| "slices with two pieces of anything = n" | 25.80 % (built 93 %) |
| "number of slices = n" / "number of cuts = n" | 6.20 % / 8.60 % |
| "slices with three or more = n" | 10.00 % (built 8 %) |
| "slices with none of it = n" | 6.60 % |
| "the fullest slice holds n" | 10.00 % |
| "slices with **exactly** two = n" | 86.20 % (built 91 %) |
| **demo replay** (previous clue's answer) | **0.00 %** |
| one constant answer for every clue | 0.20 % |
| junk: empty / whitespace / 4000 chars / the clue itself | 0.00 % |

No template exceeds ~50 % except the last, and that one is **not a rival law but a synonym**: a
player counting "slices with exactly two, a halved piece counting for both sides" has the whole
insight — object, format, measurement and halves convention — and differs from the rule only on
slices holding three or more. (v2's equivalent row was 52.8 %; it rose because v3's digit is 2 or 3
far more often than 1: k = 1 needs two severed pieces to keep the severed decoy dead, so it is only
~2 % of clues. This is why `solve()` puts a slice of three in 46 % of demos.) The ladder that matters
is the one below it: **8.6–15 % (well-formed, no idea) → 10 % (the knife family) → 26–34 % (right
family, wrong readout) → 34–44 % (right measurement, wrong halves convention) → 100 %.**

Shape and junk attacks on an otherwise correct answer (300 clues): reference 100 %; trailing spaces,
crust rows removed, blank lines inserted, an extra header line — all 100 % (forgiving about form).
All cuts removed, one cut missing in one row, cuts shifted by one in one row, an extra cut at the far
left, a dough row deleted, a dough row duplicated, upper-cased, cheese turned to spaces, a topping
moved one cell, reversed left-right, dough rows reordered — all 0.00 %. An extra cut added in the
middle of every row: 16 % (that is simply another cutting; it lands on the count about as often as a
blind one does).

### Speed and size

| | v2 | v3 |
|---|---|---|
| `generate` mean / median / p99 / max | 0.54 / 0.42 / 1.5 / 11.6 ms | **1.08 / 0.79 / 4.3 / 9.4 ms** (20000 seeds, no empty clue) |
| `solve` mean / median / max | 13.2 / 1.6 / 322 ms | 8.0 / 8.6 / 80 ms |
| scorer / solve / clue / solution chars | 474 / 4997 / 214 / 251 | **379 / 3820 / 224 / 269** |

`quickcheck --seeds 200`: OK, gen 4.9 ms max, score 0.1 ms, solve 75.7 ms max. `generate()` draws one
tray size and its 48 sample cuttings per batch and reuses them across attempts, keeps prefix sums so
one candidate cutting costs O(slices), and does the equal-cutting rejection before any sampling.
The median is under the 1 ms target; the mean is 1.08 ms, paid almost entirely for the equal-cutting
filter (dropping it to n ≤ 8 buys 0.25 ms and costs the 0.00 % row above — not worth it).

### What a demo-less player can infer about the answer's shape

Everything except the rule: the clue *is* the tray, so the answer is a picture of the same six lines,
same characters, same order, with something added — and the only thing anyone adds to a tray bake is
cuts. Bars down the picture at a few columns is a well-formed answer and scores **8.6–15 %** by
accident, which is the foothold that stops a team concluding the grader is exact-match. What they
cannot get without a demo is *which* cuts: that the digit counts slices, that it counts slices with
two of the clue's letter, and above all that a topping the knife goes through belongs to both sides.

### Prediction

Two Opus players in a 7-class pool: the one who spends a demo here cracks it in round 2–3 about half
the time (one demo now carries the whole sentence, and ~120 probes are enough to fix the halves
convention because the wrong convention scores 34–44 % rather than 0); the one who does not sits at
8–15 % from the foothold. Predicted mean final 40–60 %. Kid score should move off v2's 3.2 object
score: the tray now has a thick crust, cheese texture and three fat toppings a row, and the demo
draws "that slice has two mushrooms, one of them cut in half" instead of implying it.
Levers left if it is too hard: force one of the two pieces on the counted slice to be whole (costs
generate 1.08 → 1.73 ms); allow k = 1 more often by dropping the severed requirement there. If too
easy: narrow the rarity band to 2–8 of 48 (blind floor ~5 %), or require the counted slice to hold
nothing but that topping.
