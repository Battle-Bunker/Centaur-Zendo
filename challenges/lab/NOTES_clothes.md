# NOTES — direction: clothes, dressing and packing

Designer run 2026-09-04. Target: a class Opus centaur players crack ~half the time in
6x0.5 s rounds with 6 demos; a 12-year-old recognises the object from one demo and can
contribute hypotheses. Small drawing (a judge penalised 30-line demos). The counted
relationship must be the **headline** of every demo.

Constraints I took from the measured runs before drawing anything:
* Players rebuild the picture grammar perfectly from 1-2 demos, then hunt **statistics**.
  So the difficulty must live in *which* statistic, and every neighbouring statistic must
  be visibly false in every demo (virel, basten, garrow all do this).
* A rule outside the players' natural hypothesis space is unreachable at this cadence
  (NOTES_game conclusion: nobody ever proposed "the leap length is the mover's neighbour
  count" in six runs). So the quantity must be *pointable in the picture*, and the
  difficulty must be the last refinement step, not the whole idea.
* Named operations are read instantly (three-word test). For clothes the famous operations
  are: pairing socks, buttoning in order, folding, "does it fit in the case" (knapsack),
  "what goes on before what" (topological sort). All of those are banned.
* Counting rules protect themselves *if* hitting the exact count needs the rule, but the
  noise floor (a player who copies the format and draws at random) must be measured.

## The eight-plus ideas

| # | object (what the kid sees) | the measurement | 12-year-old test | verdict |
|---|---|---|---|---|
| 1 | **washing line with pegs** — one line, garments hung side by side | pegs that hold two garments at once | object 5/5. But "a peg does double duty" is exactly "two garments touch", the most obvious adjacency statistic on a 1-D row | **reject: too easy**, reduces to touching neighbours |
| 2 | **towel rail** — garments draped over one rail, part above, part below | garments hanging equally far above and below the rail | object 5/5, rule pointable ("that one's even, that one's lopsided"). But `above==below` is a top-3 comparison for any model given two numbers per item | **reject: too easy** (per-item equality, no relation) |
| 3 | **suitcase** — bordered box, clothes as letter rectangles packed inside | items completely hidden under exactly one other item | object 4/5, rule nice ("how many things do you have to lift?"). But the picture is a letter-rectangle grid = LegoZendo/murn/virel again | **reject: duplicates the collection's dominant object** |
| 4 | **folded stack in a drawer** | items that overhang the one below | virel's measurement with a new skin | **reject: duplicate rule** |
| 5 | **shirt front** — buttons `o` on one side, holes on the other | buttons that end up one hole out | object 5/5 but the rule IS the famous mistake; three-word test fails ("done up wrong") | **reject: nameable** |
| 6 | **packing list / outfit table** — days x garments | days that repeat yesterday's trousers | tables are the *detour* reading (fennick: "the picture reading is the rule, the table reading is the detour"); models regress tables instantly | **reject** |
| 7 | **socks on a line** — a row of letters | pairs of matching socks with exactly one thing between them | object 5/5, but "same letter at distance 2" is the first string statistic any model tries | **reject: too easy** |
| 8 | **shoe with laces** — eyelets and crossings | crossings that pass over rather than under | not drawable small; semi-famous (lacing patterns) | **reject** |
| 9 | **cloakroom pegs** — coats spilling onto the neighbouring peg | coats that cover a peg that already has a coat | object 5/5 and very social ("your coat's on my peg"), but overlapping blocks cannot be drawn in ASCII without collision | **reject: undrawable** |
| 10 | **drying rack / lines one above the other** — several lines, clothes hanging under each | garments long enough to **reach the line below** that have something hanging **directly underneath** them = "how many things are dripping on something" | object 5/5 (washing on lines, one lot above another). The rule is a conjunction of two facts a kid can point at, has no name, is not the famous operation, and sits one step past two obvious rivals ("count the long ones", "count the ones with something below") | **PICK** |
| 11 | **wardrobe rail with hangers** | garments wider than the gap to the next hanger | needs invisible geometry (hanger pitch), not pointable | reject |
| 12 | **laundry basket / ironing pile** | items ironed since last worn | invisible state, no picture | reject |
| 13 | **knitted jumper stripes** | colour changes | nameable (run-length) | reject |
| 14 | **paper doll layers** (vest, shirt, jumper, coat) | which layer is on top | topological sort, textbook | reject |

## Why #10 wins the 12-year-old test

*Object.* Three or four washing lines strung one above the other, each with clothes pegged
under it, drawn small (≤ 14 lines, ≤ 30 columns). Every kid has seen this. The pegs are
drawn on the lines (`==v===vv==`), the clothes are blocks of a letter (T-shirts, socks,
pants, jeans, dresses) of different widths and different lengths.

*Rule.* A **drip** is a garment that hangs all the way down to the line below it **and**
has a garment hanging directly under it (their columns overlap). The clue names how many
drips the picture must have. "Which ones are dripping on the washing underneath?" is a
sentence a 12-year-old says out loud; it has no name in any textbook; it is not what
washing lines are famous for.

*Why it is not free for a model.* The two obvious neighbours — "count the long ones" and
"count the ones with something under them" — are both forced to be false in **every**
shipped demo, along with ~14 other statistics of the same picture (see the witness table).
The last step, "it has to be BOTH", is what has to be paid for with a round of falsifying
probes, because demos only ever show satisfying pictures.

*Kid contribution.* The child's sentence — "that towel's so long it's touching the next
line, and it's dripping on the shirt" — is the rule. The model's sentence — "the number of
garments whose depth equals the inter-rail spacing" — is half of it.
