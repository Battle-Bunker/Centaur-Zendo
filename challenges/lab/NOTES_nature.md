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
