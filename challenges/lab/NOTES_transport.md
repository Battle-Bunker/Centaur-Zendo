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


## Refinement record — `durnel` v2 (2026-09-05, refiner)

### What the players did to v1 (`sim/results/lad-kelmar-v3-1/`)

Both Opus players finished **100 % / 100 % on durnel without spending a demo** (512/512 and
620/779 in training, 100 % of the final). Neither of them probed it: player a's NOTES say
"durnel — SOLVED (no demo) … Verified on 6/6 clues (N matched)" and it appears in the
"deliberately left without a demo: durnel (already cracked from clues)" list; player b's
`strategy.py` header says "durnel — a car whose load would hit a bridge ahead turns round
(100 %)" and calls the moment it recognised lorries-versus-low-bridges the best part of the game.
The mechanism was exactly the one DESIGN_LOOP's new "checksum caption" section describes: the
`n turn` caption is a checksum on the answer, so a rule can be falsified offline against ~80
harvested clues with no training cost — and the very first sensible rule (the famous fact: a
lorry too tall for a bridge ahead of it) reproduced n on 81/81 clues. The edit (swap the nose end
for end) was guessable from the picture alone, so knowing the rule was the whole game. Measured
now against v1's shipped scorer over 1500 fresh clues: **that blind reading scores 100.0 %.**

### The v2 change (levers (a) + (b) of the brief, in one physical story)

A lorry cannot turn round on a narrow road — **it turns round in a lay-by**. The road now carries
four lay-bys drawn `\_/` in the tarmac, and the rule is one clause a kid says in a breath:

> there's a bridge ahead it can't get under, so it pulls into the first lay-by it comes to and
> turns round.

* **(a) the edit is no longer guessable.** The turning lorry is *erased* from where it stood (its
  three columns become plain road) and *redrawn whole* in the lay-by, nose at the other end. A
  blind player cannot render that: the caption tells them how many turn, never where they end up.
* **(b) the rule is no longer the famous fact.** If the bridge it cannot fit under comes *before*
  any lay-by, the lorry never reaches one: it just stops and **nothing changes**. Every clue
  plants such a lorry (100 %, audited over 4000 clues), so "too tall for a bridge ahead" no longer
  reproduces n — the offline checksum now *falsifies* the first sensible rule instead of
  confirming it. With a demo the checksum is a full 100 % verifier again, which is what it is for.

Everything that made v1 legible is kept: the object (a road, lorries with noses, `#` bridges), the
caption `n turn`, heights given by the drawing, the ~12 % `0 turn` foothold, and the whole family
of near-miss plants (later bridge, bridge behind, exact fit, room to spare, a stander taller than a
turner), plus two new ones: a turner that drives **past a second lay-by** (it takes the first), and
the blocked-with-no-lay-by lorry above.

### Witness table, before → after (1500 fresh clues each, shipped scorers)

| template (rendered with the true drawing convention unless marked BLIND) | v1 | v2 |
|---|---|---|
| **BLIND: famous fact + v1's edit (swap the nose where it stands)** | **100.0 %** | **0.0 %** |
| BLIND: famous fact + a lay-by ahead, nose swapped in place | — | 1.1 % |
| clue returned unchanged (the foothold) | 13.9 % | 12.1 % |
| clue unchanged, caption dropped | 11.9 % | 12.1 % |
| famous fact, rendered as a move into the first lay-by | — | 12.5 % |
| true rule, moved but not turned round | — | 12.1 % |
| true rule, turned round on the spot (no move) | — | 12.1 % |
| true rule, into the LAST lay-by before the bridge | — | 12.1 % |
| an equal-height bridge blocks too (`<=`) | 0.0 % | 0.0 % |
| a lorry can squeeze under a bridge one row too low | 18.4 % | 15.2 % |
| only the NEXT bridge ahead counts | 11.9 % | 12.1 % |
| only the first bridge PAST the lay-by counts | — | 9.5 % |
| mirrored: look behind instead of ahead | 0.0 % | 0.0 % |
| any too-low bridge anywhere (direction ignored) | 0.0 % | 3.2 % |
| a lorry ahead / a lorry coming the other way stops you | — | 12.5 / 10.5 % |
| a lay-by then ANY bridge ahead (heights ignored) | — | 0.0 % |
| every lorry with a lay-by ahead | — | 0.0 % |
| the n tallest / n shortest | 11.9 / 11.9 % | 12.1 / 12.3 % |
| the first n, left to right | 15.6 % | 14.2 % |
| n random lorries | 16.7 % | 17.0 % |
| blocked by a beam within 12 columns (v1's top rival) | **30.7 %** | n/a |
| each lorry moves with probability 1/2 | 0.9 % | 3.3 % |
| true rule, vacated slot blanked with spaces | — | 12.1 % |
| true rule, lorry copied into the lay-by (not moved) | — | 12.1 % |
| caption forced to `0 turn` | 11.9 % | 12.1 % |
| demo replay / junk / empty / half the picture / the caption | 0.0 % | 0.0 % |
| **TRUE RULE (solve), caption kept / dropped / rows padded** | 100 % | **100 %** |

Twenty well-formedness attacks (no tarmac, two tarmac rows, dashes, one column short, blank row on
top, rows reversed, picture mirrored, all noses flipped, lowercased, beams erased, lay-bys erased,
caption count changed, junk line appended, 4000 chars of junk, noses as `v`, road dots as spaces,
caption alone, empty string) all score 0.0 %; trailing newlines, trailing whitespace per row and
the caption present-or-absent are the declared leniencies and score 100 %.

### One rendered demo (clue, then the answer solve() returns)

                 CCC                 SSS ###              ###
     ###         CCC LLL      ####   SSS                      HHH
                 CCC LLL             SSS                      HHH
         GGG     CCC LLL             SSS                      HHH
    .....<GG.JJ>.<CC.LL>.\_/.........<SS.....\_/.\_/..\_/.....<HH.
    ==============================================================
    2 turn

                 CCC                 SSS ###              ###
     ###         CCC     LLL  ####   SSS              HHH
                 CCC     LLL         SSS              HHH
         GGG     CCC     LLL         SSS              HHH
    .....<GG.JJ>.<CC.....<LL.........<SS.....\_/.\_/..HH>.........
    ==============================================================
    2 turn

`LL>` cannot fit under the `####` further right, and the first lay-by it reaches is the one just
past it, so it sits there as `<LL`; `<HH` is stopped by the bridge on its left and turns round in
the lay-by it passed, becoming `HH>`. `<CC` and `<SS` are as tall but every bridge that would stop
them lies before any lay-by they could use — they stand still. `JJ>` fits under everything.

### Engineering (4000 fresh seeds)

generate mean 0.83 ms, p99 3.6, max 5.0, **0 fallback uses**, 3000/3000 clues distinct and
deterministic; solve 0.037 ms; score 0.037 ms real / 0.036 ms junk; **scorer 506/512 chars**,
solve 1492, clue 260–519 chars, 1500/1500 answers distinct. `n` is 0 (12.2 %) or 2–4; no two
lorries ever want the same lay-by (generation rejects it, so the answer stays unique — the first
version of the check compared *relative* item indices and let two lorries merge in one lay-by on
34 % of clues, which is the one real bug this build found).
`python tools/quickcheck.py challenges/lab/durnel.json --seeds 200` → **OK**
(`gen=4.58 ms score=0.13 ms solve=0.14 ms` worst call in the sandbox; the single warning "score
accepts the clue itself" is the intended `0 turn` foothold, exactly as fennick).

### Prediction

**testing → calibrated, on fennick's profile: ~12 % without a demo, ~100 % with one** (mean ≈ 50 %
over two players in a 7-class pool where one of them spends a demo here). The risk is the other
way now: the demo-holder must read four things off one picture pair (which lorries, the move, the
first-vs-last lay-by, the nose flip). If a pair of demo-holders comes back at 0–10 %, soften with
the "too hard" levers in the JSON: draw one lorry already sitting in a lay-by in the clue as a
worked instance, or drop the nose flip so the edit is only "it moves into the lay-by".
