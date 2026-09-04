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
