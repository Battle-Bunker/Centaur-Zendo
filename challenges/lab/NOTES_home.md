# Direction: school and home life (designer: school-home)

Brief: the demo must be a small ASCII picture or table a kid recognises instantly; the clue
is tiny and pins an arbitrary-but-natural *measurement* of that picture; no name for the
measurement; close every degenerate witness.

Two constraints I took from the earlier lab rounds before writing a line of code:

* **NOTES_game.md conclusion** — a 0/1 channel only tests hypotheses the player already
  generates. `orlan` failed (3 versions, 6 Opus runs, never cracked) because the hidden
  quantity ("the mover's own occupied-neighbour count") was never *proposed* by any player.
  Its own v4 recommendation: put the hidden quantity somewhere the player can see it and
  take the difficulty back elsewhere. So: the free variable of my answer must be visibly the
  only free variable, and the measurement must be a relation *between things that are drawn*.
* **NOTES_everyday.md conclusion** — `quilm` was cracked 4/4 because recognising the object
  was sufficient: the rule was the object's famous operation. So: recognition must be
  necessary but not sufficient; and well-formedness constraints belong in `generate()`
  (or in the *clue*), not as surprise clauses in `score()`.

That gives the shape I wanted: **the clue hands over a half-finished picture; the answer is
the completed picture; the only thing the player chooses is one number per object; the rule
is a three-conjunct measurement over those numbers and the picture's holes.** Completion
also kills the LegoZendo failure mode (players submitted the minimal witness and never
learned the rule) for free — you cannot submit a small picture when the clue dictates the
picture's footprint.

---------------------------------------------------------------------------
## Brainstorm (10 ideas, each against the 12-year-old test)

Test half 1: *would a bright 12-year-old name the object from one demo?*
Test half 2: *once named, is the pinned pattern still unnameable — not the object's famous
operation?*

**1. Bookshelf, leaning books.**  Answer is a shelf of book spines drawn as bottom-aligned
bars of letters with `.` for empty slots and an `=====` shelf under them. Clue = the slot
row (letters + holes) + a tiny per-letter tally. Measurement: a book *tips* when there is a
gap on exactly one side (the packed side pushes it over) and it *leans* only if the book
across that gap is taller than it.
*Half 1*: yes — bars of different heights standing on a `=` line with gaps read as books
instantly; every kid has seen the book at the end of a half-empty shelf flop over.
*Half 2*: yes — "gap on exactly one side AND the book two slots away is strictly taller"
has no name; the famous bookshelf operations (sorting by height, alphabetising, "how many
fit") are all excluded by the fact that the order is given in the clue.
**Keep — strongest on both halves.**

**2. Class seating plan.** Grid of desks with pupils' initials, aisles as gaps. Measurement:
how many pupils sit between two friends (same initial) in the same row.
*Half 1*: yes. *Half 2*: weak — "between two of the same letter in a row" is a substring
pattern; an LLM's first three hypotheses about a letter grid are exactly substring patterns.
Also the answer is a free 2-D letter grid, so a minimal witness (one row) is hard to exclude
without arbitrary size clauses in the scorer. *Reject.*

**3. Sports league table, invented scoring.** Answer = a consistent table (P W D L F A Pts),
clue pins the points column under an invented formula.
*Half 1*: yes, instantly. *Half 2*: **no.** "Invented scoring" is a linear formula over five
columns; six demos is a linear system and an Opus player solves it by least squares in one
round. The consistency constraints (ΣW=ΣL, ΣF=ΣA) are a nice construction but they are the
*easy* half. *Reject — it is a fitting exercise, not a lateral one.*

**4. Clapped rhythm.** Bars of `X . x` beats. Measurement: claps that fall on a beat whose
bar-mate ... .
*Half 1*: yes. *Half 2*: **no.** Music has a name for everything the player will try —
downbeat, offbeat, syncopation, upbeat, tie — and models carry all of it. Any measurement I
invent will be one keyword away from a real term, and the model will land on the real term
and be right often enough to score. *Reject: named-genre risk.*

**5. Piano keyboard, pressed keys.** ASCII white/black keys, some pressed. Measurement:
pressed white keys with a black key immediately to their right.
*Half 1*: yes, very strong. *Half 2*: **no** — every relation between two keys is an
*interval*, and intervals are the single most over-trained musical prior there is. The
model will enumerate semitone distances and hit it. *Reject* (same failure as 4).

**6. Traffic lights / pedestrian crossing.** Cars on a road, lights, a zebra crossing.
*Half 1*: yes. *Half 2*: the natural measurements ("which cars can move") reproduce Rush
Hour / traffic-jam puzzles, which are named and heavily trained. *Reject.*

**7. Lunch tray.** Compartments with foods; measurement over what touches what.
*Half 1*: medium — an ASCII tray is a box with boxes in it; without colour it reads as
"a grid", not "a tray". *Half 2*: fine. *Reject on half 1* — the picture does not evoke.

**8. Chore rota.** Names × days grid, chores as letters. Measurement: people who do the same
chore two days running.
*Half 1*: yes (it is a table). *Half 2*: weak — "same symbol twice in a row" is the first
thing anyone tests on a grid of letters. Same failure as 2. *Reject.*

**9. Measuring cups / recipe.** Clue = an amount; answer = a set of scoops.
*Half 2*: **no** — this is change-making, a named algorithm with a Wikipedia page, and the
greedy answer is the intended one. Exactly the anti-pattern the loop document warns about.
*Reject.*

**10. Pocket money with invented coin values.** Same objection as 9 plus "invented values"
turns it into a small Diophantine problem — number theory by the back door. *Reject.*

### Two modifiers considered for whichever object won
* **(M1) Per-letter tallies instead of one count.** The clue pins the measurement for 3–4
  named letters at once rather than one. Same single rule to discover (no extra insight
  needed, so no extra unfairness), but a blind answer must hit 3–4 counts simultaneously,
  which takes coincidental scoring from ~25 % to ~2 %. **Adopted** — this is the one thing
  that stops "I understand the picture format but not the rule" from paying.
* **(M2) Deliberate decoy geometry.** Plant, in every instance, the three configurations
  that separate the true rule from its nearest neighbours: isolated objects (gap on *both*
  sides), double-width gaps (nothing within reach to lean on), and equal-height pairs
  (strict vs non-strict comparison). **Adopted** — this is what makes recognition
  insufficient: three separate yes/no questions must each be resolved, each costing a probe
  cycle, and every one of them is a *natural* question, so a player who gets them wrong is
  wrong for a reason they can find.

---------------------------------------------------------------------------
## Chosen: idea 1 + M1 + M2, named `fennick` (neutral, random-looking, no pun)

### Rule (private)

Clue is `LAYOUT/TALLY`, e.g. `ABB.CCA.DE.BB.AAC.DD.BA/A2B0C3D1`.

* `LAYOUT` is one row of slots: an uppercase letter = a book standing in that slot, `.` =
  an empty slot. The first and last two slots are always books (the ends are anchored, so
  "is the outside of the shelf a wall or a hole?" never has to be guessed).
* `TALLY` is letter/digit pairs.

The answer is the finished bookcase: `max(h)` rows of `W` characters, then one row of `=`.
Book *j* is drawn as a solid bottom-aligned bar of `h_j` copies of its letter with `.`
above it. The bottom text row therefore *is* `LAYOUT`. The player chooses only the heights.

A book **leans** iff

1. exactly one of its two neighbouring slots is empty (a book with books on both sides is
   held up; a book with holes on both sides has nothing pushing it over), **and**
2. the slot two along in that direction holds a book (a one-slot gap — across a two-slot
   gap there is nothing within reach), **and**
3. that book is **strictly taller** than it (you can only lean on something taller; equal
   heights and both books stay up).

`score` returns 1 iff the drawing is well-formed, its bottom row equals `LAYOUT`, and for
every letter named in `TALLY` the number of leaning books of that letter equals its digit.
Letters not named in the tally are unconstrained decoys.

### Why this is the right shape

* **The measurement is a relation between two drawn things** (this book, the book across
  the gap), so it is inside the players' hypothesis space — the `orlan` failure mode is
  avoided — but it is a *three*-conjunct relation, so being inside the space is not enough.
* **Structure is given, values are free.** There is exactly one free variable per book, and
  the player can see that. All the difficulty is in "which books does the tally count?".
* **Nice emergent mechanic**: the two books flanking a one-slot gap point at each other, so
  exactly one of them leans — whichever is shorter — or neither, if you make them equal.
  So the player who has the rule controls the tally exactly, and the player who has it
  *nearly* right systematically overshoots. It is also a genuinely charming fact for a kid:
  "make them the same height and they both stay up".
* **Three natural ambiguities**, each costing a probe cycle and each planted in every
  instance by `generate()`: strict vs non-strict height comparison; one-slot gap only vs
  nearest book beyond any gap; do books with holes on both sides count.

### Degenerate witnesses and how each is closed

| witness | closed by |
|---|---|
| empty string, junk, the clue itself | no `=` row / row-width check |
| a minimal picture (one book, one gap) | bottom row must equal `LAYOUT`, which `generate` makes 22–34 slots wide |
| all books height 1 (or all heights equal) | that makes every tally 0; `generate` never emits a clue whose named tallies are all 0 (it requires ≥ 2 named letters with a non-zero tally) |
| "make nothing lean" (any flat/equal drawing) | same as above |
| all heights distinct / monotone / random | must hit 3–4 tallies at once (M1) — measured below |
| ignoring the letters, hitting only the total | tallies are per letter |
| copying a demo's heights | the layout changes every instance |

Measurements for all of these are in the *Anti-witness* table further down.

---------------------------------------------------------------------------
## Iteration 1 — `challenges/lab/fennick.json` (shipped), arena live, players NOT run

### Clue / answer, concretely

```
clue  EU.J.JE.UR.RR..WRU.W.T..R.ET.EU..E.ET..ER.U..JJ..UW.WR.TW/U1E2R2W1

answer (one demo output)
.........R...................E...........................
.........R.......U...T.......E......T.....U..............
......E..R.......U...T.......E......T.....U..............
E.....E..R..R....U...T.......E...E..T.....U..JJ...W......
E.....E.UR..R..W.U...T..R....E...E..T..E..U..JJ...W......
E.....E.UR.RR..W.U...T..R..T.EU..E..T..E..U..JJ...W..R.T.
EU.J..E.UR.RR..WRU...T..R..T.EU..E.ET..E..U..JJ...W..R.T.
EU.J.JE.UR.RR..WRU.W.T..R.ET.EU..E.ET..ER.U..JJ..UW.WR.TW
=========================================================
```

Exactly one U book, two E books, two R books and one W book must be *leaning*, where a book
leans iff exactly one neighbouring slot is a hole, the slot two along that way holds a book,
and that book is strictly taller.

### Validation

`python tools/quickcheck.py challenges/lab/fennick.json -v` → **OK, no warnings**;
`--seeds 200` → **OK, no warnings** (gen 1.05 ms, score 0.22 ms, solve 8.87 ms worst case).
Engine pool load through `sim/arena.py setup`: `1 accepted, 0 rejected`.

### Engineering (3000 fresh seeds, `$SCRATCH/home/`)

| quantity | value | cap |
|---|---|---|
| `score` source | **483** chars | 512 |
| `solve` / `generate` source | 1253 / 2695 | 5000 / 50000 |
| clue length | 64–70 chars (shelf 55–62 slots) | 1024 |
| solution length | 335–609 chars | 1024 |
| generate | avg 0.19 ms, p99 0.63, **max 0.89 ms** | 100 ms |
| solve | avg 1.10 ms, p99 5.8, **max 17.6 ms** | 2000 ms |
| score | avg 0.078 ms, **max 0.57 ms**; 0.018 ms on junk | 50 ms |
| determinism / distinctness | 3000/3000 identical on re-call, 3000/3000 distinct clues, 0 generator fallbacks | |
| `score(clue, solve(clue))` | 1 on 3000/3000 | |
| cross-check vs an independent re-implementation | **0 disagreements / 9250** (clue, answer) pairs incl. malformed | |
| tally shape | per letter 0–5 (mode 2), 0 or 1 zeros per clue, total 5–12 | |

### Anti-witness table (800 fresh clues unless noted; shipped scorer)

| attack | hit rate |
|---|---|
| empty string / whitespace / `"x"` / `"1"*100` / the clue itself | **0.00 %** |
| shuffled solution (quickcheck's junk) | 0.00 % (0/300) |
| layout row + shelf, i.e. every book height 1 | **0.00 %** |
| any flat picture (all books height 2 / height 4) | **0.00 %** |
| right-size picture on a *shuffled* layout row | **0.00 %** |
| blind random heights 1..9 / 1..3 | 1.12 % / 0.50 % |
| sawtooth heights up / down the shelf | 1.00 % / 0.75 % |
| correct answer with two rows swapped (breaks bottom-alignment) | 0.50 % |
| 22 hand-built well-formedness attacks (floating book, two letters in a column, book standing in a declared hole, missing book, wrong/absent/extra shelf row, ragged row, trailing space, mirrored picture, 4000-char junk) | **0/22 accepted**, and the 3 that *should* be accepted (blank rows above, trailing newline, 55 blank rows) all accepted |
| correct answer + one blank row on top (must be 1) | 100.00 % |
| **near-miss R = `>=` instead of `>`** | **31.1 %** |
| near-miss R = "nearest book beyond the hole, however wide" | 17.9 % |
| near-miss R = "holes on both sides count too" | 13.1 % |
| near-miss R = "shorter than a book two away, ignoring holes" | 6.3 % |
| near-miss R = "shorter than the right-hand neighbour" | 0.9 % (and infeasible for 35 % of clues) |
| near-miss R = "next to exactly one hole, heights irrelevant" | 0.0 % (**infeasible for 100 % of clues**) |

"near-miss R = X" means: a player holding rule X runs a local search for heights that satisfy
*their* rule's tally, and submits that. It is the honest measure of what 90 %-of-the-way
insight is worth.

### How fast do demos kill the near-misses?

Fraction of demo pictures on which each near-miss rule still reproduces the clue's tally
(low = one demo falsifies it):

| rule | agrees with the tally on a demo |
|---|---|
| the true rule (sanity) | 100.00 % |
| `>=` instead of `>` | 17.0 % |
| nearest book beyond the hole | 10.5 % |
| holes on both sides count | 8.2 % |
| shorter than a book two away | 1.7 % |
| shorter than the right-hand neighbour | 0.8 % |
| next to exactly one hole (heights ignored) | 0.0 % |

### Fairness floor — hypothesis-elimination surrogate (`hyp.py`)

Catalogue of **75 laws** = {which books are counted: exactly one hole side / at least one hole
side / holes irrelevant} × {what it is compared with: the book two along, the next book beyond
the hole however wide, the book on the packed side, the tallest book on the shelf, the book
three along} × {`>` `>=` `<` `<=` `==`}. Feeding demos in random order until only the true law
survives:

* **median 1 demo, max 5, 0 failures in 100 random orders.**
* On a single demo the strongest survivor other than the truth is `>=` at 19 %.

So the evidence channel is not the bottleneck — a team that *generates* the right catalogue
cracks this in one to five demos, comfortably inside the six-demo budget. The whole difficulty
is lateral: does anyone propose "a hole on exactly one side, the book two along, taller"?
This is exactly the lever `orlan` lacked (there the hidden quantity was invisible); here the
quantity is a relation between two *drawn* objects, so it is inside the players' hypothesis
space, but it is a three-conjunct relation, so being inside the space is not sufficient.

### Witness leaks closed by construction (not by scorer clauses)

* `generate()` never emits a clue whose named tallies are all zero (≥ 3 non-zero, total ≥ 5),
  so "draw it flat" — the one universal, rule-free answer — is worth 0.00 %.
* The clue dictates a 55–62 slot footprint, so the LegoZendo failure ("submit the minimal
  witness and never learn the rule") cannot happen: there is no small answer.
* Every instance carries ≥ 4 isolated books and ≥ 4 books beside a two-slot hole, and those
  decoy slots are dealt to the four *named* letters, so each near-miss rule changes a named
  tally in most instances. This is what took the near-miss rates from 41/58/66 % (first build,
  measured) down to 31/18/13 %.
* Candidate slots are dealt round-robin over a cycle in which the four named letters appear
  twice and the two decoy letters once, so every named letter always owns ≥ 2 candidates and
  its tally is always reachable. No unreachable clue is ever emitted (0 solve failures/3000).
* Declared artifacts, for honesty: (a) isolated books and two-hole-neighbours are biased
  towards named letters — visible, but it tells a player nothing about the rule; (b) exactly
  one named letter has tally 0 in 37 % of clues and none in the rest; (c) the tally constrains
  only ~18 of ~40 books, so 86 % of single-book height edits of a correct answer still score 1
  — the accepted set is large, which is not a witness (you still need the rule to build one)
  but is worth knowing when reading the players' hit rates.

### Arena (DESIGN_LOOP step 3) — players not run by me

```
pool     $SCRATCH/pool-fennick-1/fennick.json
setup    python sim/arena.py setup --run lab-fennick-1 --teams fennicka,fennickb \
                --challenge-dir $SCRATCH/pool-fennick-1 --arena-root $SCRATCH/lab-fennick-1
server   127.0.0.1:41241   pool loaded: 1 accepted, 0 rejected   phase=training
teams    $SCRATCH/lab-fennick-1/players/fennicka
         $SCRATCH/lab-fennick-1/players/fennickb
cadence  6 rounds x 0.5 s, 5 s cooldown, 1 demo per window, 3 s final (arena defaults)
```
($SCRATCH = `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad`)

I cannot spawn player agents, so I stop here. After the orchestrator runs both players:
`python sim/arena.py teardown --run lab-fennick-1` then `report --run lab-fennick-1`.

### What to read in the results, and the pre-registered response

| observed | reading | change for iteration 2 |
|---|---|---|
| both ≥ 90 % | recognition was sufficient; the three-conjunct relation is inside their default catalogue | harden: drop the layout's *letters* from the clue (give holes only, `..#.#..`, and let the player choose letters too) so the tally's candidate set is no longer readable off the clue |
| one ≥ 90 %, one 10–90 % | **on target — stop** | — |
| both 10–90 % with `>=`-shaped notes | they found the geometry and missed strictness | nothing structural; that is the designed near-miss tier (31 %) |
| both < 10 % | holes were never brought into a hypothesis | soften: make `solve()` emit, once per demo, a shelf whose *only* books are the leaning ones' pairs (a 6-slot cameo appended under the shelf line) — a positive instance of the law itself, per the `orlan` v4(d) recommendation |

---------------------------------------------------------------------------
## Iteration 2 — 2026-09-04 — `fennick` v2 (refiner; v1 kept as `fennick.v1.json`)

### What the players actually did with v1 (run `lad-fennick-v1-1`, 2 Opus finals)

| player | final | what they believed |
|---|---|---|
| fennick1a | **20/2610 = 0.8 %** | *"the class wants an **ASCII bar chart**: rows top-to-bottom, each column c holding letter row[c] repeated height[c] times upward from the baseline… I could not identify the statistic (every height-subset count, every neighbour/order statistic and every per-letter aggregate I could construct was falsified), so the heights are sampled uniformly from 1..4 — the distribution whose measured hit-rate was highest (~1.6 %)."* |
| fennick1b | **22/1406 = 0.7 %** (1801 skips) | *"H rows, each row's letters a subset of the next row's… **ink soaking through nested rows**… the layer assignment looks genuinely random per clue; only ~8 bits arrive in the params, far too few to encode ~35 letters' layers. **Not reconstructible.**"* Final strategy: *"Skip unless max(param digit) == 2; otherwise emit 6 nested rows (pseudo-random reveal order)."* |

Mean final rate **1 %** over 2 finals → `too_hard`. The kid judge scored **3.4** and warned the
drawing reads as a skyline, not a lean.

Diagnosis. This is **not** a rule problem — it is an **object** problem, and it is the failure
mode this class was supposed to be immune to. Neither player ever saw *a bookshelf*: 1a saw a
bar chart, 1b saw ink soaking through nested rows. "Leaning" was therefore never in either
hypothesis space, so the three-conjunct law was never even a candidate; both players instead
reverse-engineered the *checker's* leniency (1b: "scores only ever happen when max(param
digit) == 2 → 0/~300 for max 3 or 4; H = 6 is the best row count") and farmed the ~1 % that
v1's blind-random-heights witness paid out. The v1 pre-registered response for "both < 10 %"
was a law-cameo; the real problem is one level below that, so I fixed the picture instead.

Why v1's picture failed the 12-year-old test, concretely (v1 demo, same seed):

```
C......W...C....WV....W.....C...U.......U...............
CR.....W...C....WV....W...V.C...U.......UR......R..C....
CR....RW...C....WV....W.VVV.C...U.......UR......RV.C.U..
CRU.W.RW.RRC..G.WV..G.W.VVV.CVC.U.R.UG.VUR..UCR.RV.C.U..
========================================================
```
56 slots wide, dot-filled everywhere, no book tops, and — fatally — **the leaning is
invisible**: a leaning book looks exactly like a standing one. The only thing the picture
shows is heights, so "heights" is all anyone hypothesises about.

### v2 — the same rule, a legible object

The law is untouched (three conjuncts: exactly one neighbouring gap, a book two along that
way, strictly taller). Four changes, all to the drawing and the clue's surface:

1. **Books look like books.** Air is now a SPACE, not `.`, and every book gets a `_` cap one
   row above its spine. The shelf row `=` stays; the bottom text row is still exactly the
   clue's LAYOUT (dots mark the empty slots), so "the answer is this shelf drawn with heights
   I choose" is still readable straight off the first demo.
2. **Leaning books are drawn leaning.** A book that leans keeps its foot in its own slot on
   the bottom row and its remaining letters *plus its cap* are drawn one column across, inside
   the gap it is falling into; the cap becomes `/` (leaning right) or `\` (leaning left). You
   can see the book propped against the taller book beyond the gap.
3. **Half the width.** 34–42 slots instead of 55–62 (clue 51–56 chars), pictures 5–7 rows.
   A whole shelf now fits in one glance.
4. **The tally reads as a sentence, not a code**: `U:1 E:2 R:2 W:1` instead of `U1E2R2W1` —
   "one U fell over, two Es fell over".

Same seed, v2:

```
clue: RCV.R.WU.RRU..V.CC..WUW.GUR.VRU.U.UV/V:1 R:1 W:1 U:2
      __   _        _   _ _     _
 __ _ WU\  U    __  W_  G R\ _ /U\ _
_CV R WUR _U  _ CC  WU /G_RV R UUU V
RCV.R.WU.RRU..V.CC..WUW.GUR.VRU.U.UV
====================================
```
`/U\` at the right is two books fallen inwards against the tall `U` between two gaps; `R\` and
`WU\` are books propped on their taller neighbours. Every instance shows at least four.

### The move this buys, and the price

The tilts are **not free decoration**: the scorer reads one height per book out of the columns,
recomputes from the rule which books lean, re-renders the whole picture, and demands the
submission back character for character. So **the picture is the hypothesis** — draw the tilts
by the wrong rule and you score 0. Two consequences, in opposite directions:

* *Harder*: the rule-free witness is gone. "Random heights, everything drawn upright" pays
  **0.00 %** where v1's equivalent paid 1.1 %. A player with no theory of leaning now scores
  exactly zero instead of farming ~1 %, which is also what made v1's runs uninformative.
* *Softer (the point)*: every demo now displays the true lean set explicitly, so the law is
  learnable from the demos rather than only from four tally digits. Against the 75-law
  catalogue, demos in random order: **median 1 demo, max 4, 0 failures/100** using the drawn
  tilts (v1's tally-only channel: median 2, max 6).

### Witness table, v1 → v2

| attack | v1 | v2 |
|---|---|---|
| empty / whitespace / `"1"*100` / the clue itself | 0.00 % | 0.00 % |
| layout row + shelf only (every book height 1) | 0.00 % | 0.00 % |
| any flat picture (all heights equal) | 0.00 % | 0.00 % |
| right-size picture on a shuffled layout | 0.00 % | 0.00 % |
| **random heights, nothing drawn leaning** (the rule-free attack) | **1.1 %** | **0.00 %** |
| blind random heights 1..9 / 1..3, *tilts drawn correctly* | 1.1 % / 0.5 % | 3.0 % / 3.7 % |
| sawtooth up / down, *tilts drawn correctly* | 1.0 % / 0.8 % | 2.3 % / 4.7 % |
| hand-built well-formedness attacks | 0/22 | **0/28** |
| near-miss `>=` instead of `>` | 31 % | 23.5 % |
| near-miss "gaps on both sides count too" | 13 % | 29.0 % |
| near-miss "nearest book beyond any gap" | 18 % | 17.0 % |
| near-miss "two away, gaps irrelevant" | 6 % | 8.0 % |
| near-miss "shorter than the right neighbour" | 0.9 % | 0.0 % |
| near-miss "one gap, heights irrelevant" | 0 % | 0.0 % |

The two v2 rows that went *up* (blind heights, sawtooth) are measured **with the true
renderer**, i.e. they are only reachable by a player who already has the law and simply did not
bother to search the heights; the narrower shelf and smaller tallies (total 4–8, mean 4.8) make
that lazy player luckier. The v2 near-miss figures are also stricter than v1's: a player holding
rule X now draws the tilts by X too, so X has to reproduce the *whole* lean set, not just four
digits.

New well-formedness attacks all rejected: tilt marks straightened (`/`,`\` → `_`), tilt marks
swapped left/right, caps removed, dots instead of spaces, bottom row dotted, rows reversed,
mirrored picture. Deliberate leniencies, all verified: trailing/leading newlines, blank rows
above the picture, right-stripped or padded rows, junk appended to the right of every row (each
row is normalised to width W).

### Engineering

`python tools/quickcheck.py challenges/lab/fennick.json --seeds 60` → **OK, no warnings**
(gen 0.98 ms, score 0.08 ms, solve 19.1 ms worst case). Over 3000 fresh seeds: generate avg
0.20 / max 1.15 ms, solve avg 4.1 / max 51 ms, score avg 0.044 / max 0.10 ms (0.02–0.13 ms on
junk); 3000/3000 distinct and deterministic, **0 generator fallbacks**, 800/800 solve outputs
score 1; **0 disagreements / 4800** (clue, answer) pairs against an independent *structural*
re-implementation (it validates column by column instead of re-rendering). Scorer **500/512**
chars, clue 51–56, solution 179–286.

Load-bearing invariant, written down because the scorer depends on it to fit in 512 chars:
`generate()` always anchors the shelf with ≥ 2 books at each end, so `i ± 2` is in range for
every book that has a gap on exactly one side, and the scorer omits the bounds test.

### The 12-year-old test, applied

*Half 1 — would a bright 12-year-old name the object from one demo?* v1: no (measured: two
Opus players said "bar chart" and "nested rows"; judge 3.4, "reads as a skyline"). v2: books
now have tops, stand on a shelf half as wide, and several of them are visibly tipped over into
the gaps with `/` and `\`. "Some of the books have fallen over against the tall ones" is the
first sentence a kid says. The clue's `U:1 E:2 R:2 W:1` then reads as *which* books fell.
*Half 2 — is the pinned pattern still unnameable?* Unchanged: "a gap on exactly one side, the
book two along that way, strictly taller" has no name, and the famous bookshelf operations
(sort by height, alphabetise, how many fit) are all excluded because the order is given.
A kid can also contribute the key construction fact for free: *make two books the same height
and they both stay up.*

### Predicted classification and the pre-registered response

Predicted **testing → calibrated**, mean final rate **0.4–0.7**, with a real risk of `too_easy`
(the demos now hand over the lean set). The class is deliberately **bimodal**: exact rule
≈ 100 %, near-miss 8–29 %, no rule 0 %; a 50 % mean means half the players get the law.

| observed | reading | change for iteration 3 |
|---|---|---|
| both ≥ 90 % | the drawn tilts gave the law away | harden by *hiding* the tilt marks again but keeping the book look: drop the `/` `\` caps to `_` and keep the one-column shift (the lean stays visible in the shape, not in a symbol); if that is not enough, stop shifting and go back to v1's rendering with v2's caps, width and tally format |
| one ≥ 90 %, one 10–90 % | **on target — stop** | — |
| both 10–90 % with `>=`- or "both sides"-shaped notes | designed near-miss tier | nothing structural |
| both < 10 % again | recognition still failing, which would be surprising | draw `|` walls at the two ends and a 6-slot law cameo under the shelf |
