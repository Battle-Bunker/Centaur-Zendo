# NOTES_nature — direction: animals and nature

Brainstorm for a new class in the "animals and nature" direction (garden with flowers and
bees, pond with frogs on lily pads, birds on telephone wires, trees casting shadows, ant
trail, beehive cells, footprints in snow, flock in V formation, fish in a tank, vegetable
patch in rows).

Constraints carried in from the ladder so far (in order of importance):

1. **The OBJECT must be recognised from the raw ASCII of ONE demo, with the name giving no
   help.** `fennick` drew books as bars and `garrow` drew a pizza as a bordered grid; both
   lost the object-recognition half of the kid rubric and both players hallucinated a
   different object. Draw the thing with the cues a kid uses: a fish is `><>`, a bird is
   `v` on a wire `-----`, a plant is a stalk growing out of `#` gravel.
2. **The measurement must be a relationship between DRAWN things a kid would notice**
   ("do the bricks line up", "one sticker is much more common") **and must have no name.**
3. **Close degenerate witnesses AND transfer leaks.** If an answer can be recoloured,
   relabelled or concatenated so that one demo is reusable for other clues (LegoZendo,
   tovel), the class is farmable. Tie the count to the *identity or position* of something
   the clue fixes.
4. **Keep it small**: <= 12 rows x 40 cols, countable by eye.

---

## The eight (plus) ideas

### 1. Birds on telephone wires — "birds sitting right on top of each other"
Picture: poles `|`, wires `----`, birds `v`. Count birds that have a bird in the same column
on the wire below.
*Kid test:* object 5/5 (unmistakable). Measurement: **this is virel's twin-stack with birds
on it** — same "same-column coincidence between two rows" measurement that is already the
star of the ladder. Rejected as a re-skin.

### 2. Birds on wires — "pairs of birds with exactly one empty spot between them"
Count neighbouring birds separated by exactly one space ("they left room for a friend").
*Kid test:* object 5/5, measurement kid-natural. **Rejected**: the hypothesis space is a
single small integer (gap = 0,1,2,3,...), so a player who has the format sweeps five values
in one round of probes. No lateral step.

### 3. Frogs on lily pads — "an empty pad squeezed between two frogs"
Picture `~~~ (_) (@) (_) ~~~`. Count empty pads whose left and right pad neighbours in the
same row both carry a frog.
*Kid test:* object 4/5 (`(@)` reads as a frog only once you're told it's a pond); the
measurement is nice but is one of the first three things anyone says about a row of
occupied/empty slots. **Rejected** as too easy on measurement.

### 4. Trees casting shadows — "trees standing in another tree's shadow"
Trees `/|\` on a ground line, each casting a shadow of length = its height to the right.
*Kid test:* object 4/5, measurement 3/5 — "in the shade" is a nameable, physical concept and
the sun-angle physics is exactly the kind of thing a model proposes first. Also the shadow
length is a *function* of the drawing, so the drawing is over-determined and the answer has
little freedom. **Rejected.**

### 5. Beehive cells — "cells with honey that touch exactly two other honey cells"
Hex comb drawn `/  \__/  \__`. *Kid test:* object 5/5, gorgeous. Measurement **rejected**:
counting the full neighbours of a cell in a grid is *cellular automata / Minesweeper*, a
top-of-the-list model prior, and hex adjacency is hard to count by eye.

### 6. Ant trail — "loaded ants that meet an empty ant coming the other way"
*Kid test:* object 3/5 — an ant trail in ASCII is a row of letters, i.e. fennick's failure
mode. Also essentially one-dimensional, so the picture carries almost no structure.
**Rejected.**

### 7. Footprints in snow — "steps where the stride got longer"
Two staggered rows of prints; count the strides longer than the previous one.
*Kid test:* object 3/5 (dots in a field are ambiguous), measurement 4/5. **Rejected** on
object recognition — this is precisely the mistake fennick made.

### 8. Flock in V formation — anything about a V
The V fixes almost every position, so the answer set is tiny and a unique-answer class
starves the 0/1 channel (SPEC design principles). **Rejected.**

### 9. Vegetable patch in rows — "the same vegetable twice in a column"
A grid of letters. **Rejected**: object recognition 2/5 (a letter grid is not a picture),
and the measurement is again virel's same-column coincidence.

### 10. Garden with flowers and bees — "bees hovering over a flower"
*Kid test:* object 4/5, measurement 2/5 — "is the bee over a flower or over a gap" is the
first hypothesis anyone forms, and it is nameable. **Rejected.**

### 11. Fish in a tank — "fish nose-to-tail behind another fish"  (runner-up)
Fish are `><>` and `<><`; count neighbouring same-row pairs swimming the same way.
*Kid test:* object 5/5, measurement 4/5 — reading the fish's *direction* is a genuinely
kid-first move and nothing on the ladder uses orientation. **Not chosen**: reduced to the
direction bits alone it is "number of adjacent equal symbols in an R/L string", which is
about the fifth statistic a model tries, and it does not touch anything the clue fixes, so
one demo transfers to any clue with the same shape.

### 12. **Fish in a tank — "the fish that have their nose right up against a plant"  (CHOSEN)**
Same tank, but the counted relation is between a fish and the *weeds the clue fixes*: a fish
counts iff the cell immediately in front of its nose (right of `><>`, left of `<><`) is a
plant segment.
*Kid test:* **object 5/5** — `~~~~` surface, `####` gravel, `|` stalks growing out of it,
`><>` fish; every kid names it. **Measurement 5/5** — "these ones are nibbling the weeds" is
exactly a playground observation, it has no name, and it is a relation between two *drawn*
things. It needs three ideas at once (the fish has a direction; the plants matter; only the
pointy end counts), which is the lateral step. And because the plant columns come from the
clue, **no answer transfers between clues**, which closes the LegoZendo/tovel farming leak.

Chosen. Implemented as `challenges/lab/basten.json`.

---

## Why the chosen measurement should sit in the partial band

Rivals a player will try first, all of which the generator falsifies in *every* shipped
demo (rejection filter in `solve`): total fish, right-facing fish, left-facing fish, fish
whose **tail** touches a plant, fish touching a plant on **either** side, fish not touching
anything, number of plants, plant cells, number of water rows, fish in the bottom row, fish
in the top row, the busiest row, neighbouring same-direction pairs, nose-to-nose pairs,
tail-to-tail pairs, plants with a fish beside them, and fish-count minus depth.

Every demo is also forced to contain **at least two fish that touch a plant with their tail**
and **at least two fish that touch nothing**, so "any fish next to a plant" is visibly wrong
rather than invisibly wrong, and both orientations always appear at least twice.

## Measured numbers

Full per-attack witness table is in the report and in `basten.json`'s `description`.
Headline: 400 fresh clues, attacker assumed to know the well-formedness format perfectly and
to build a legal tank satisfying its hypothesis.

| attacker's law | score |
|---|---|
| random legal tank | 0.5 % |
| **the true rule** (N nibbled spots, one spot eaten from both sides) | **100 %** |
| N nibbled spots, third clause unknown | 12.0 % |
| N nibbled spots, deliberately no double | 0.0 % |
| N nibbling FISH (the n-gram reading of the picture) | 0.0 % |
| N nibbling fish plus a double | 0.0 % |
| N nibbled plant *columns* | 5.0 % |
| every other rival counted above | 0.0-1.2 % |

**Law-family sweep.** Over a 94-law family — every "count the fish that have character X on
one side and Y on the other" pattern (both orientations, and the two merged) plus 19
structural statistics of the tank — the mean number of laws consistent with the demos is
3.98 after one demo, 1.43 after two, 1.08 after three and exactly 1.00 after six, and the
sole survivor is the true clause-2 law. So the demo channel *is* decisive for the count once
a player has the right family in mind; the difficulty is (a) getting the picture format
exactly right, (b) generating "count the leaves being nibbled" rather than "count the fish
that are nibbling", and (c) clause 3, which is a positive-only clause and therefore invisible
to any law-fitting over demos.

## basten v1 ladder run `lad-basten-v1-1` (2026-09-04, 6×0.5 s, 2 players)

| team | profile | final | demos | note |
|---|---|---|---|---|
| basten1a | opus-default | 6% | 7 | 0/1880 for five rounds, then isolated-fish builder 3/478 |
| basten1b | opus-kidproxy | 7% | 3 | found "both orientations required", "fish not touching", height free |

Mean 7%: leaning too_hard (2 finals). Both players rebuilt the tank grammar completely (surface,
gravel, digit → stalk height, fish spacing, both orientations present, height free) and both
declared N "undiscoverable": 1a tested ~90 picture statistics and all two-term integer
combinations; 1b ~350. Neither ever tested a statistic about **what a fish's nose touches**. The
kid-proxy's imagined child said "it's a fish tank" and "the tanks are different heights" but not
"that fish is eating the weed". 1a's post-mortem: "a kid would count something concrete and
physical … instead of the abstract statistics I ground through" — but the physical reading it
listed was fish-in-compartments, not nibbling.

Diagnosis: the nose-to-leaf relationship is drawn (`><>|`) but nothing in the demos makes it the
headline. With 13–23 fish per picture and only N nibbling spots, the nibblers are lost in the
shoal. Judge advice was the same: widen the fish-minus-leaf gap so the mismatch is visible.
Softening levers for v2 (in order): (a) far fewer fish per picture (say N+2..N+4) so most fish are
nibblers and the demo reads "fish eating weeds"; (b) draw the nibbled cell differently — but only
if that is what a tank would look like (e.g. a bite taken out: `><>:`), never a marker; (c) drop
clause 3 (the both-sides double) which nobody got near; it can return once (a) lands.
Both players praised the object and the demo mechanic; both called N unfair — the same complaint
garrow got, and for the same reason: the counted relationship is drawn but not salient.

## basten v2 — refinement after `lad-basten-v1-1` (2026-09-04)

**Diagnosis carried in.** v1 mean final 7% (6% / 7%) over two Opus players ⇒ leaning `too_hard`;
kid judge 4.4/5 with one note: *"the double-nibble clause is positive-only and easy to miss;
widen the fish-minus-leaf gap so the nose/tail-vs-both-sides distinction reads as the headline
discovery."* Both players rebuilt the entire tank grammar and then ground through ~90 (1a) and
~350 (1b) picture statistics without ever testing a statistic about **what a fish's nose
touches**. The relation was drawn but not salient: 13–23 fish per picture, only N of them
nibbling, so the nibblers were lost in the shoal. v1's own witness table already showed the
floor was wrong-shaped: a format-only player scored ~0.5%, so 6–7% was "format plus luck".

**Changes (all softening; the object now tells the story).**

1. **Far fewer fish.** `solve()` ships `N+2..N+5` fish (was 13–23). Mean fraction of the fish
   that are nibbling is now 0.56 (0.32 at N=2, 0.72 at N=8). A demo now reads *"a few fish, and
   most of them have their nose in a weed"* instead of *"a shoal"*. This is the whole fix.
2. **Clause 3 (the both-sides double) dropped.** Reasoning, recorded because it was a real
   choice: the clause is *positive-only*. Demos only ever show satisfying examples, so no
   number of demos — however prominent the `><>|<><` in them — can tell a player that a double
   is **required**; a prominent double only shows that it is **allowed**. In v1 it cost the
   player who had the right idea 88% of their score ("N nibbled leaves" scored 12%) and bought
   nothing on the discovery path, and no v1 player ever got close enough to be taxed by it. The
   brief's condition ("keep it only if every demo shows it prominently *and* it doesn't stop a
   player who has the nose/leaf idea from scoring") cannot be met by a positive-only clause, so
   it goes. It is the **first hardening lever** if v2 overshoots.
3. **Count fish, not leaves.** With clause 3 gone the leaf/fish distinction survives only as a
   trap, so the scorer counts nibbling **fish** — the n-gram reading (`><>|` / `|<><`) that a
   player will actually implement — and `solve()` never emits a double-nibbled leaf, so the two
   readings agree on every demo. A leaf-counter who never draws a double scores 100%; only a
   leaf-counter who *deliberately* doubles is bitten, and nothing in any demo suggests that.
   Rolling this back (count distinct nibbled cells + require one double) is a two-line change.
4. **"At least one fish per water row" dropped** from the format. With 4–13 fish a depth-6 tank
   would otherwise be forced dense again, and 1b burned a round on this rule.
5. **No new markers.** The picture is still `~` water, `#` gravel, `|` stalks, `><>` / `<><`
   fish and `.` open water — nothing was added that a real tank would not have. The bite-mark
   idea (`><>:`) from the v1 lever list was **not** used: it is a marker, not a tank.

Unchanged: the clue (`<plants>/<N>`, N never the plant count nor the total height), the free
depth 4–6, both orientations ≥2, the rejection filter that falsifies ~18 rival statistics in
every shipped demo, and the anchoring of the count to the clue's plant columns (so no answer
transfers between clues).

**Witness table, 400 fresh clues, same attacker model both sides** (knows the format perfectly,
builds a legal tank satisfying its own hypothesis; every builder also satisfies v1's
one-fish-per-row rule so the columns are comparable):

| attacker's law | v1 | v2 |
|---|---|---|
| random legal tank | 0.2% | 6.2% |
| N fish | 0.0% | 0.2% |
| N fish beside a plant (either end) — the nose/tail near miss | 0.0% | 6.8% |
| N fish with the TAIL on a plant | 0.0% | 0.0% |
| N fish in the bottom row | 5.9% | 16.0% |
| **N nibbling FISH (nose on a leaf)** | 0.0% | **100.0%** |
| N nibbled LEAVES, no double | 0.0% | 100.0% |
| **N nibbled LEAVES, one double** (the v1 rule) | **100.0%** | 0.0% |
| N nibbled plant COLUMNS | 0.0% | 100.0% |
| that version's own `solve()` | 100.0% | 100.0% |
| the other version's solution | 0.0% | 0.0% |
| previous demo replayed on the next clue | 0.0% | 0.0% |
| empty / clue echoed / `"1"*100` / no fish / plants only | 0.0% | 0.0% |
| one fixed real answer for every clue | 0.0% | 0.2% |

The headline swap is the two bold rows: the reading a player will actually write down goes from
0% to 100%. The cost is a higher noise floor — a player with only the format now scores ~6%
instead of ~0.5%, which is exactly what v1's two players scored, so **anything above ~10% in v2
is real progress**. "N fish in the bottom row" picks up 16% by accident (the bottom row is where
the plants are), but the rejection filter falsifies it in every shipped demo.

**Validation.** `quickcheck --seeds 200` OK; 6000 clues, `solve()` scores 1 on every one, mean
6.2 ms / worst 208 ms; `generate` deterministic, < 0.2 ms; `score` 449 chars, 0.02 ms real /
0.033 ms worst on junk, always 0/1. Scorer cross-checked against an independent
re-implementation on 11 600 (clue, answer) pairs — whitespace/case/reversal variants and
structural mutations — with 0 disagreements.

**Typical v2 demo** (clue `...2.....2.......3......3..../2`, N=2, six fish, two of them nibbling,
one with its tail against a weed, three swimming free):

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
....................><>......
.............................
...<><.......................
<><...........><>|...><>|....
...|..<><|.......|......|....
...|.....|.......|......|....
#############################
```

**Predicted classification:** on target, with overshoot the real risk — expect one crack and one
partial/high-partial rather than two failures. **Predicted kid score:** 4.5–4.8/5 (the object was
already 5/5; the measurement is now visible in the picture instead of hidden in a shoal).
Previous version kept byte-identical at `challenges/lab/basten.v1.json`.

## basten v2 ladder run `lad-basten-v2-1` (2026-09-04, 6×0.5 s, 2 players)

| team | profile | final | demos | reading |
|---|---|---|---|---|
| basten1a | opus-lowdemo | 25% | 2 | "fish are hiding in the weeds" — placement matters, never the nose |
| basten1b | opus-theorist | 42% | 3 | "how many fish are standing right next to a reed, at least N" — tuned an offset per N |

Mean 33% (v1 was 7%). The softening worked as intended: both players now see the fish/weed
relationship, and 1b's reading ("fish next to a reed") is one step from the rule ("fish with its
NOSE on a reed"). Neither took that step; 1b treated the residual as checker noise ("my count is
slightly coarser than the checker's"), which is precisely nose-vs-tail. 1b's own kid line:
"the fish are all hiding next to the weeds" — said the kid would say it straight away.

Status: testing, 4 finals over 2 versions; v2 alone is 25/42, on the low side of the band but a
real gradient (0 → 5 → 12 → 23 → 35 → 42 over six rounds). Leave v2 as is; the next two finals
decide. If both land 20–45% again, the lever is not the rule but the demo: make every demo carry a
tail-on-reed fish right next to a nose-on-reed fish so the asymmetry is the first thing seen (v2
already forces ≥1 tail-touching fish; raise it to 2–3 and put them beside a nibbler).
