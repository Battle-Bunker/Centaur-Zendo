# NOTES — direction: transport, maps and journeys (designer, 2026-09-05)

Brief: new format (7 classes, 4 rounds × 0.5 s, 3 demos per team per game). Copy what makes
fennick v3 work: **the clue is the drawn object plus a caption naming the verb and a number**;
**the rule is ONE physical clause a kid says in a breath**; **the answer is the clue's picture
edited**, unique; every demo shows the positive case beside its near-misses; the caption is a
checksum a player can verify offline; the degenerate "return the clue unchanged" witness must
pay only on the caption's zero cases.

## The 12-year-old test applied to 11 ideas

| # | idea | object a kid names? | rule in one breath? | rule *not* nameable by a model? | edit unique? | verdict |
|---|---|---|---|---|---|---|
| 1 | **Low bridges on a road**: lorries of different heights on a road, `#` beams overhead at different clearances, each lorry has a nose arrow. Caption `3 turn`. A lorry turns round iff somewhere **ahead of it, in the direction it faces**, there is a beam too low for it. Edit: flip the nose. | yes — "lorries and a bridge" | "it turns back if there's a bridge ahead it can't fit under" | the *famous* fact (lorry vs low bridge) gives the theme, not the rule: which beams count (all ahead, not just the next; direction-dependent; equal height fits) is the arbitrary part | yes, N arrows flip | **CHOSEN** |
| 2 | **Kerbside parking**: cars of different lengths parked in a row; a car can pull out iff the gap in front of it is at least as long as the car. Edit: the car lifts into the road row. | yes | yes | "will it fit in the gap" is the first hypothesis any model writes; and it is a purely local, one-comparison rule with no direction-of-travel wrinkle | yes | strong runner-up; kept as the lever if #1 is too hard |
| 3 | **Car park, which cars are blocked in**: bays two deep off an aisle; a car is stuck iff another car is between it and the aisle. | yes | yes | **no** — this is the obvious rule, an Opus player writes it before the demo renders | yes | reject (too easy) |
| 4 | **Bus route**: stops along a road with queue heights; the bus stops iff the queue is bigger than the last one it served. | yes | no — *stateful*, needs a walk along the route and the state is invisible | — | yes | reject (not one clause; the scorer must simulate) |
| 5 | **Lift and floors**: people waiting on landings, the lift stops where. | yes | same statefulness problem as #4 | — | yes | reject |
| 6 | **Railway points**: wagons roll into sidings depending on how the points are set. | half — the drawing of a junction in ASCII is muddy | yes | maybe | yes | reject (the object is not legible in 40 columns) |
| 7 | **Boats at a jetty, the tide drops**: a boat grounds iff the water under it is shallower than its hull. | yes | yes | it is fennick's "compare two numbers across the picture" with a new skin; also the water depth has to be drawn as a second profile, which crowds the picture | yes | reject (re-skin of fennick) |
| 8 | **Treasure map, where to dig**: landmarks on a grid; dig halfway between two of the same kind. Caption `3 dig`. | yes | yes | midpoint-of-two-landmarks is a geometry chestnut, and the "same kind" pairing is the only arbitrary bit | yes (add `x`s) | reject (geometry, not physics; weak near-miss family) |
| 9 | **Hopscotch**: which squares you land on with one foot. | yes | yes | **no** — the rule *is* the game's rule | yes | reject |
| 10 | **Roundabout, who gives way**: give way to the right. | yes | yes | **no** — famous | yes | reject |
| 11 | **Zebra crossing**: kids cross where the gap between cars is wide enough. | yes | yes | same shape as #2 with two moving parts and a messier picture | yes | reject (dominated by #2) |

## Why #1 wins

* **The object is instant.** Lorries with arrows on a road, `#` beams over it, `====` tarmac.
  A kid names it from one glance; the caption `3 turn` names the verb and gives the count.
* **The rule is a journey, not a neighbour.** fennick's rule is local (look one and two slots
  either side); this one asks *can it get to the end of the road that way?* — the player has to
  scan the whole road **on one side only**, the side the lorry is pointing. That is the same kind
  of "arbitrary-but-natural measurement" fennick has (which of the plausible quantifiers?) but a
  structurally different one, so the collection gains a genuinely new shape.
* **Every demo carries its own near-misses**, and they are all plantable by construction:
  * a lorry that turns because of the **second** beam ahead (the first one it clears) → kills
    "it only looks at the next bridge";
  * a lorry standing with a too-low beam **behind** it → kills "any low bridge in the picture"
    and kills the mirrored rule;
  * a lorry standing under a beam of **exactly** its height → kills `<` vs `≤`;
  * a lorry standing with plenty of clearance ahead → kills "a bridge ahead is enough";
  * a **standing lorry taller than a turning one** → kills "the N tallest turn".
* **The edit is minimal and unique**: exactly the turning lorries' noses swap ends. The diff
  between the demo's two pictures *is* the rule.
* **The foothold is the same as fennick's**: ~12 % of clues say `0 turn`, and there the correct
  answer is the clue returned unchanged, so a demo-less player who echoes the picture banks the
  zero cases and nothing else.

## Design decisions taken while implementing (see the JSON's description for the record)

* Nose on the **bottom row only** (`AA>` / `<AA`) so a turn changes two characters and the
  scorer's check is "everything above the ground row is untouched".
* Lorries never share a column with a beam (a gap of ≥ 1 column between every drawn item), so
  a lorry's height is simply the number of non-space cells in its middle column. This keeps the
  scorer under 512 chars and removes any parsing ambiguity.
* Clearance `k` = the number of free rows under a beam; a lorry of height `h` passes iff
  `h <= k`. The equal case *passes* — deliberately, and every clue plants one.
* Both ends of the road are empty tarmac, so "is the outside of the picture a wall?" never has
  to be guessed and the scorer indexes safely.
* Heights are **given by the drawing** (as in fennick v3): there is no height formula to hunt,
  which is the red herring that ate fennick v2's losing player.
* N is 0 (≈12 %) or 2–5; never all the lorries.

## Levers if it drifts

* **Too easy**: (a) require the caption dropped, which removes the identity foothold and the
  offline checksum; (b) count only lorries that would have to reverse *past* another lorry;
  (c) put a beam directly over a lorry so the "no shared columns" regularity disappears and the
  height read costs a probe; (d) let a lorry be blocked by another lorry facing it.
* **Too hard**: draw one already-turned lorry into the clue as a worked instance, or drop to two
  beams so the "second beam ahead" case is the only subtlety.

## Implementation record — `durnel` v1 (2026-09-05)

Shipped as `challenges/lab/durnel.json` (private notes in its `description`). No arena run: the
brief stopped at self-testing.

* `python tools/quickcheck.py challenges/lab/durnel.json --seeds 200` → **OK**
  (`gen=0.85 ms score=0.56 ms solve=0.08 ms` worst-call in the sandbox; one warning,
  "score accepts the clue itself" — that is the intended `0 turn` foothold, exactly as fennick).
* 4000 fresh seeds: generate mean 0.20 ms / p99 0.74 / max 1.38, 0 fallback uses, all deterministic,
  3000/3000 distinct clues; solve 0.026 ms; score 0.051 ms real / 0.025 ms junk.
  Sizes: score **497**/512, solve 1336/5000, clue 167–414/1024, solution 167–414/1024.
* Plant audit over 4000 clues: every `n>0` clue carries all five near-misses (later-beam turner,
  low-beam-behind stander, exact-fit stander, roomy stander, a stander taller than a turner) and
  turners/standers facing both ways. `n=0` on 11.7 % of clues.
* Attack table (2000 fresh clues): top rival 30.7 % ("only beams within a dozen columns count"),
  then 18.4 % (clearance off-by-one), then the ~12 % family that is really just the foothold
  (clue unchanged / N tallest / N shortest / next-beam-only). Everything that ignores the nose is
  0.0 %. True rule 100 %.

### What was tuned during the build

1. **The zero-branch coin flip must be drawn before the rejection loop.** Drawing it inside meant
   `n=0` layouts were accepted far more often than `n>0` ones and the foothold ran at 45.7 %.
2. **Beam clearances start at 2, not 1.** With clearance 1 nearly every lorry had to be one row
   tall to stand, and the road came out flat and unreadable.
3. **Blank rows above the tallest object are trimmed**, so the clue never opens with an empty line.
4. **Re-roll only the free lorries, and memoise the ahead/behind clearances per (lorry, direction)**:
   mean attempts 6.2 → 1.8 and generate 0.39 ms → 0.20 ms.
5. **Scorer 572 → 497 chars**: read the picture column-wise once (`zip(*P)`), let `rfind('#') == -1`
   supply the "no beam" sentinel for free, and compare right-stripped rows on both sides instead of
   padding the answer.
