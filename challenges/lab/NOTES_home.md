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
