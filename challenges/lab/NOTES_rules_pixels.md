# NOTES — rule-family class, world = a 5×5 picture of black and white squares (`ospren`)

Paradigm: `docs/RULE_FAMILIES.md`. A finite universe **U** of parametrised rules; the clue is a
minimal set of positive example pictures that pins exactly one rule of U; the answer is one more
picture obeying it. The player does **not** know U, so their (much larger) hypothesis space is full
of obvious picture rules the class never uses. Learning **what this class never says** is the game.

Shipped file: `challenges/lab/ospren.json` (name checked unique against `challenges/` and
`challenges/lab/`). Not committed; no arena run (out of scope for this job).

Lessons copied from `dornic` (cards), `borsel` (dice), `tresk` (beads) and `tavrik` (words):
U must be an **antichain**; the **template is drawn uniformly before the parameter**; **loose
competitor rules stay in U** so the generator is forced to kill them (they do the clue's layout
work for free); a **"fresh" clause** on the answer kills every copy-edit witness at once; the best
traps are the **loose cousins** of the templates that *are* used; the class only ever makes
**tight** statements; `score` ≤ 1024 chars.

---

## 1. The world

An instance is one **5×5 picture**, five lines of five characters from `#` (black) and `.` (white):

```
..#..
.###.
#####
.###.
..#..
```

* **Clue** = 2 or 3 example pictures, separated by a blank line, nothing else (≤ 91 chars).
* **Answer** = one more 5×5 picture that
  1. has between **2 and 15** black squares,
  2. uses a **number of black squares that no example uses**, and
  3. differs from every example in **at least two squares**.
* The examples of a clue always have **different numbers of black squares** and are pairwise ≥ 3
  squares apart, so clause 2 is visible in the clue itself and clause 3 is never suggested by it.

Clauses 2 and 3 are the "fresh" clause of §5 and they cost the scorer almost nothing: clause 2
replaces the "the answer is not one of the examples" test the scorer had to do anyway.

---

## 2. The universe U — 10 templates, 29 rules

The scorer reduces a picture to a **15-number readout** and every rule of U is one readout number
equal to one constant. "density" = the probability that a *naive random picture* (a uniformly
random count 2–15, then that many random squares) satisfies the rule — i.e. **what a player who
answers at random scores when this rule is the truth**. A rule may be the hidden one only if its
density is ≤ 0.20; the rest stay in U as **competitors** the generator has to kill.

| # | template (kid sentence, one breath) | parameter grid | density per parameter | may be the answer? |
|---|---|---|---|---|
| COUNT | "there are exactly *n* black squares" | n = 5, 6, 7 | .069 / .071 / .073 | **never** (competitor; see below) |
| SYM | "the picture looks the same **in a mirror** / **flipped top-to-bottom** / **turned upside down**" | 3 params | .0087 / .0088 / .0035 | all 3 |
| CORNERS | "exactly *n* of the four corners are black" | n = 1, 2, 3, 4 | .341 / .272 / .128 / .024 | 3, 4 |
| SPREAD | "the black squares sit in exactly *n* rows / *n* columns" | n = 1, 2 × rows/cols | .014 / .107 / .014 / .106 | all 4 |
| BLOBS | "there are exactly *n* blobs" (squares joined side by side; *n* = 1 is "they are all joined up in one blob") | n = 1, 2, 3, 4 | .035 / .192 / .280 / .255 | 1, 2 |
| FULLLINE | "exactly one row is completely black" / "exactly one column is" | 2 params | .051 / .052 | both |
| MIDDLE | "the middle square is black" | — | .339 | **never** (competitor) |
| EQLINE | "every row has the same number of blacks" / "every column does" | 2 params | .0080 / .0087 | both |
| MAXBLOB | "the biggest blob is *n* squares" | n = 2, 3, 4 | .173 / .136 / .108 | all 3 |
| LONELY | "exactly *n* black squares stand completely alone" (no black neighbour) | n = 3, 4, 5 | .190 / .095 / .040 | all 3 |

|U| = **29**, of which **21 are eligible** to be the hidden rule, over **8 eligible templates**.
`generate()` draws the **template uniformly first** and only then a parameter, so no idea of the
class is rare merely because it owns fewer rules (measured mix over 500 clues: eqline 73, blobs 69,
corners 64, spread 62, maxblob 62, lonely 59, sym 58, fullline 53). Mean density of the hidden rule:
**0.070** — that is the floor a thoughtless player gets, and the number the eligibility ceiling
controls.

### Why the loose rules stay in U as competitors
`exactly n black squares` (n = 5, 6, 7), `exactly 1 / 2 black corners`, `exactly 3 / 4 blobs` and
`the middle square is black` are far too generous (.13–.34) to be an answer, but leaving them **in
U** means the generator has to kill them, which forces the clue to do layout work for free:

* the three COUNT rules can only die if the examples **disagree about the number of blacks** — which
  is exactly the convention the answer's fresh-count clause needs, so the format and the competitor
  enforce each other (same trick as `tresk`'s length rules and `dornic`'s "exactly n cards");
* MIDDLE can only die if some example has a **white** middle square and some other one a black one;
* the loose CORNERS and BLOBS parameters force the examples to disagree about corners and blob
  counts. A clue is therefore never three pictures that look alike.

### Structural consequence of the fresh-count clause
A rule that **fixes** the number of black squares can never be pinned, because the examples must
disagree about that number. So `"every row has exactly one black square"` (a lovely kid sentence,
and one the brief suggested) is impossible here — it forces n = 5 — and the same goes for every
"exactly n blacks" rule and for "every column has exactly one". The class pays for its cheapest
anti-copy clause with those rules; `every row has the **same** number of blacks` (n ∈ {5, 10, 15})
is the survivor of that family and is in U.

### Why U is an antichain
Positive examples can never separate a rule from a **weaker** rule that contains it: if A ⊆ B and A
is the truth, B survives too, and A can never be pinned. Brute-forced over the generator's 11 000
picture pool: **no rule of the final U contains another** (0 violations). Casualties of that check:

* **"as many blacks above the middle row as below"** ⊇ *top-bottom symmetry* **and** ⊇ *every row the
  same number* — it is implied by two different templates of U, so it cannot be a rule. It became one
  of the best traps instead (fires on 26 % of clues, and on essentially every symmetry clue).
* **"as many blacks left of the middle column as right"** — ditto for left-right symmetry.
* **"the top row is the same as the bottom row"** ⊇ top-bottom symmetry; **"the first column is the
  same as the last"** ⊇ left-right symmetry. Both are traps, not rules.
* **"the four corners are all the same colour"** ⊇ `0 black corners` ∪ `4 black corners`. Trap.
* **"the black squares make a straight line"** ⊇ "all the blacks are in one row"; the disjunction had
  to go and the two tight halves stayed.
* **"the biggest blob is 1"** (= *no two black squares touch*) is contained in nothing but is *dense*
  (a rule that a third of all sparse pictures satisfy is not a rule) — so the MAXBLOB grid starts at
  2 and "no two blacks touch", the most obvious Zendo rule of all, became an exclusion.
* `exactly 0 blobs` / `0 corners` / `all-white` are excluded by the well-formedness floor of 2 blacks.

### Why the number of blacks is capped at 15
Without a ceiling the **all-black picture** satisfies left-right, top-bottom and half-turn symmetry,
`4 black corners`, `1 blob`, `every row the same number` and `every column the same number` — seven
eligible rules at once, and its count is never in a clue. A single constant answer would have scored
~30 % with no insight at all. The cap (2–15 blacks) removes that degenerate witness and every
near-copy of it; the surviving "hedge" (a fully symmetric single blob) is measured at 19 %, which is
a legitimate partial insight rather than a free ride.

### Templates measured and thrown out
| template | why not |
|---|---|
| "every row has exactly one black square" | fixes the count at 5 → unpinnable under the fresh-count clause (above) |
| "the black squares make a straight line" | contains "all in one row"; the tight halves are in U instead |
| "no two black squares touch" | dense (.2–.45 depending on the count) → **exclusion**, where being dense is what makes it a good trap |
| "there is a row that is all black" | a *there-is* statement; the tight version ("exactly one row is") is in U |
| "the top row is all white", "the middle square is white" | the class never says anything is **white** → exclusions |
| "at least / at most *n* blacks" | the class never makes a loose statement → the two 100 %-consistent traps |
| "the picture looks the same flipped along the diagonal" | a fourth symmetry; a kid sees mirror/flip/turn much faster than a transpose, and three is enough |
| "exactly *n* black squares touch the edge" | fiddly to check by eye for no new idea |
| "the blacks make a solid rectangle" | ⊂ "one blob", and far too rare to build clues from |

---

## 3. The exclusions — what the class never says (the traps)

Never in U, deliberately. **fits** = the trap, fitted to the clue, is consistent with *every*
example, so a player who forms it is never contradicted; **score** = a player who always answers
with a well-formed instance of it (fresh count, ≥ 2 squares different) over all 500 clues;
**when played** = its score on the clues where it fits.

| excluded rule (fitted to the clue) | why a player reaches for it | fits | score | when played |
|---|---|---|---|---|
| "every square that is black in **all** the examples is black" | *the* first thing anyone tries: what do these pictures have in common? | **100 %** | **19.4 %** | 19 % |
| "**at least** *n* black squares" (*n* = the clue's smallest) | the loose cousin of the COUNT competitors | **100 %** | 10.2 % | 10 % |
| "**at most** *n* black squares" (*n* = the clue's biggest) | the other loose cousin | **100 %** | 10.2 % | 10 % |
| "the same number of black squares as an example" | the laziest hypothesis there is | **100 %** | **0.0 %** | 0 % |
| "there is a black square in the middle column" | position-hunting; it looks true | 58 % | 9.8 % | 11 % |
| "the middle square is white" | the negation of a real competitor | 36 % | 10.0 % | 9 % |
| "every row has at least one black square" | the loose cousin of SPREAD | 27 % | 10.0 % | 14 % |
| "as many blacks **above** the middle row as below" | the loose cousin of top-bottom symmetry **and** of EQLINE | 26 % | 12.4 % | **22 %** |
| "as many blacks **left** of the middle column as right" | ditto, left-right | 23 % | 11.4 % | 17 % |
| "the four corners are all the same colour" | the loose cousin of CORNERS | 18 % | 10.2 % | 17 % |
| "the top row is the same as the bottom row" | the loose cousin of the top-bottom flip | 11 % | 13.6 % | **30 %** |
| "the first column is the same as the last column" | ditto, left-right | 10 % | 13.0 % | 25 % |
| "the top row is all white" | white-square hunting | 4 % | 11.8 % | 9 % |
| "**no two black squares touch**" | the most obvious Zendo rule of all | **1 %** | 9.4 % | 0 % |

The class's secret is a **convention**, not a single rule. It only ever makes **tight** statements
about **black** squares — *exactly* three corners, the biggest blob **is** four, *every* row the
**same** number, the picture **is** its own mirror — and never a loose one (at least, at most, no
two touching, there is a…, the top row is white). Its two strongest traps are the loose cousins of
its own templates, and they are consistent with **100 %** of clues by construction.

Three honest findings:

* **"No two black squares touch" fires on only 1 % of clues.** A strong *every-square* property is a
  weak discriminator, so a minimal identifying example set is almost never made of such pictures —
  the same self-excluding effect `dornic` found for "all one suit" and `tresk` for "it alternates".
  The load-bearing traps are the four that fit 100 % of the time, not the famous one.
* **"The same number of blacks as an example" is not merely never the rule — it is actively wrong**
  (score 0 by well-formedness). It is the cheapest lesson in the class and the first thing 0/1
  feedback teaches.
* **Two rare traps are nearly always right when they fire**: if the examples share their top and
  bottom row the rule is usually the top-bottom flip (30 %), and if their first and last columns
  match it is usually the mirror (25 %). That is honest structure, not a leak: on those clues the
  trap and a U-rule agree.

**On average 6.2 of the 14 exclusions are consistent with every example** (never fewer than 4). So a
player whose universe is U *plus* the obvious extras always faces several survivors; picking a
**wrong** one scores **11 %**, picking a random one **25 %**, and picking the true one 100 %. That
gap is the whole difficulty of the class.

---

## 4. Three demos

```
CLUE                              ANSWER      hidden rule (private)

##.#.   #.###   #####             .....
#####   .#.##   #.#..             #####
.....   #####   .....       ->    .....       exactly one row is completely black
....#   ###..   #....             .....
..#..   .....   .#...             .....

#...#   #..##                     ##.##
...#.   .##.#                     .#..#
#....   .#.##               ->    ..##.       exactly 3 of the four corners are black
.....   #.#..                     #.#.#
#.#..   ####.                     #.##.

.....   #....   ###..             .....
.....   ##...   ####.             ....#
..##.   .....   ..#..       ->    #####       the black squares are all joined up in one blob
.....   .....   .....             ..#..
.....   .....   .....             .....
```
(seeds 3, 42, 19. Note that every clue shows a different number of black squares in each picture,
and every answer a fourth number: 9/15/6 → 5, 6/13 → 12, 2/3/8 → 7.)

---

## 5. The design decision that made the class: a fresh count of black squares

First build — the answer only had to be a well-formed 5×5 picture that was not one of the examples:

| witness (bare scorer, no fresh clause) | score |
|---|---|
| **mirror / flip / turn / transpose an example** | ~100 % (every symmetry-blind rule survives) |
| copy an example with one square flipped | **35.2 %** |
| add one black square to an example | 34.0 % |
| rub one black square out of an example | 32.6 % |

Almost every measurement of a picture in U is invariant under the eight symmetries of the square and
robust under a one-square edit, so the demo-less probe "echo a clue picture with a tweak" was
cracking the class outright — insight optional (DESIGN_LOOP lever 8). The fix, in the spirit of
`dornic`'s fresh-cards and `tresk`'s fresh-length clauses:

> **the answer must use a number of black squares that is not in the clue, and must differ from
> every example in at least two squares.**

* The first half kills **copy, mirror, top-bottom flip, half turn and transpose in one clause** —
  all five preserve the count — and costs the scorer *nothing*, because it replaces the "the answer
  is not one of the examples" test it needed anyway. It is honest and visible: the clue's own
  pictures never share a count.
* The second half (≈ 75 chars, copied from `tavrik`) kills the three one-square edits. It only ever
  bites when the count differs by exactly one, since the Hamming distance is at least the difference
  in counts.
* What is left is a real foothold that **requires the first insight**: "copy an example and change
  two squares" scores **12.8 %** (well-formed 43 % of the time), a symmetric single blob at a fresh
  count **19.2 %**, "everything the examples have in common" **19.4 %**, and a random picture at a
  fresh count 7.8 %. No cheap probe is above 20 % and none is zero — the 5–30 % band the loop asks
  for.

---

## 6. Witness table — 500 fresh clues (measured against the shipped JSON)

| witness | score | well-formed |
|---|---|---|
| copy an example verbatim | **0.0 %** | 0 % |
| flip one cell of an example | **0.0 %** | 0 % |
| add one black square to an example | **0.0 %** | 0 % |
| rub one black square out of an example | **0.0 %** | 0 % |
| mirror an example left-right | **0.0 %** | 0 % |
| flip an example top-bottom | **0.0 %** | 0 % |
| turn an example upside down | **0.0 %** | 0 % |
| transpose an example (flip on the diagonal) | **0.0 %** | 0 % |
| flip two cells of an example (the cheapest legal probe) | 12.8 % | 43 % |
| EXCLUDED: every square black in all the examples is black | **19.4 %** | 99 % |
| EXCLUDED: at least *n* black squares | 10.2 % | 99 % |
| EXCLUDED: at most *n* black squares | 10.2 % | 99 % |
| EXCLUDED: the same number of blacks as an example | 0.0 % | 0 % |
| EXCLUDED: the top row is the same as the bottom row | 13.6 % | 100 % |
| EXCLUDED: the first column is the same as the last column | 13.0 % | 100 % |
| EXCLUDED: as many blacks above the middle row as below | 12.4 % | 100 % |
| EXCLUDED: as many blacks left of the middle column as right | 11.4 % | 100 % |
| EXCLUDED: the four corners are all the same colour | 10.2 % | 100 % |
| EXCLUDED: the middle square is white | 10.0 % | 100 % |
| EXCLUDED: every row has at least one black square | 10.0 % | 100 % |
| EXCLUDED: there is a black square in the middle column | 9.8 % | 100 % |
| EXCLUDED: the top row is all white | 11.8 % | 100 % |
| EXCLUDED: no two black squares touch | 9.4 % | 100 % |
| a symmetric one-blob picture at a fresh count (the hedge) | 19.2 % | 100 % |
| always an instance of the densest U-rule (exactly 2 blobs), ignoring the examples | 12.6 % | 100 % |
| always a 3-blob picture (the commonest picture there is), ignoring the examples | 5.0 % | 100 % |
| a random picture from the class's own sampler, fresh count | 10.4 % | 100 % |
| a random well-formed picture, fresh count | 7.8 % | 100 % |
| a random well-formed picture, any count | 6.4 % | 81 % |
| **player who has mapped U perfectly** | **100.0 %** | 100 % |
| player who has mapped U minus its 2 rarest templates (lonely, eqline) | 74.4 % | 100 % |
| player who has mapped U minus 2 templates (sym, corners) | 77.6 % | 100 % |
| player whose universe is U + the 14 exclusions, random survivor | 25.0 % | 86 % |
| player whose universe is U + the 14 exclusions, a **wrong** survivor | **11.0 %** | 81 % |
| player who knows U but drops one example and takes a wrong near-survivor | 13.8 % | 100 % |
| the true rule (`solve`) | **100.0 %** | 100 % |

Notes on the partial-knowledge rows:
* A player whose universe is a **subset** of U gets **zero** survivors on the clues whose rule they
  have not mapped (positive examples kill everything else), so they know they are lost and guess:
  ~75 % + a guess. Each of the 8 templates is worth roughly 12 points.
* A player whose universe is **larger** than U faces 6.2 extra survivors per clue on average and
  scores 25 % by choosing at random, 11 % if they systematically choose wrong. **100 % vs 11 %** is
  the whole game, and the only way across is to notice which *kinds* of statement this class never
  makes.
* The two rows with well-formedness below 100 % are an artefact of the measuring harness (it
  rejection-samples an instance of the chosen rule and sometimes fails within its budget), not of
  the class.

Other measured numbers (500 clues):
* **Example counts**: 2 examples 52.4 %, 3 examples 47.6 % (the generator tries 3 first on 65 % of
  draws, 2 first otherwise; it can fall back to 4, which never happened in 500 clues).
* **Uniqueness** (exactly one U-rule consistent with all examples): 500 / 500.
* **Minimality** (dropping any one example leaves ≥ 2 consistent rules): 500 / 500.
* **All example black-counts distinct**: 500 / 500. Examples pairwise ≥ 3 squares apart: 500 / 500.
* Mean density of the hidden rule for a naive random picture: **0.070**.
* `generate` is deterministic across processes (the pool is built from a fixed seed): checked.
* Hidden-rule mix (500 clues): one full column 40, one full row 37, 3 corners 32, half turn 32, all
  4 corners 31, equal columns 28, 3 lonely 28, 5 lonely 28, equal rows 26, one blob 25, 2 columns 24,
  biggest blob 2 → 22, biggest blob 3 → 22, mirror 20, biggest blob 4 → 19, 2 blobs 19, top-bottom
  flip 17, 4 lonely 15, one column 13, one row 13, 2 rows 9.

---

## 7. Validation

`python tools/quickcheck.py challenges/lab/ospren.json --seeds 300 -v`
→ `OK ospren  gen=2.03ms score=0.22ms solve=26.91ms`, **no warnings** (worst case over 300 seeds; a
second run gave gen=1.38 ms, solve=16.5 ms).

| quantity | value | cap |
|---|---|---|
| `score` source | **1004 chars** | 1024 (the raise `RULE_FAMILIES.md` §4 allows for this paradigm) |
| `generate` source | 9502 | 50 000 |
| `solve` source | 4087 | 5 000 |
| `generate` | 0.30 ms mean, 2.11 ms max over 5000 seeds | 100 ms |
| `score` | 0.060 ms on a real answer, ≤ 0.004 ms on junk | 50 ms |
| `solve` | 27 ms max | 2000 ms |
| clue | ≤ **91** chars | 1024 |
| answer | **29** chars | 1024 |

Junk (`""`, `"0"`, `"x"`, `"1"*100`, the clue itself, `"#"*4000`) all score 0 without raising. The
scorer parses with `s.split()`, so an answer is accepted with any line ending, with trailing spaces,
or written as one space-separated line — strict about the rule, forgiving about form.

`generate` is fast because the 11 000-picture pool, each picture's 29-bit "which rules of U do I
satisfy" mask and the index `rule → {number of blacks: [pictures]}` are built **at module level**
(460 ms once per worker, not charged to `max_generate_ms`); a call is then a handful of integer
ANDs. `solve` re-derives the survivor exactly as the scorer does and rejection-samples a **random**
valid picture from a nine-way mixture of picture shapes at a random unused count — never the
canonical or minimal witness (it does sometimes land on a small one, which is fine: it is drawn at
random from the legal answers, not chosen).

---

## 8. Predicted classification

**Testing / on target.** Prediction for two Opus players in a 7-class pool (4 rounds, ~60 probes per
class per round, 3 demos for 7 classes):

* **Without a demo**: the clue's shape is self-evident — two or three little 5×5 pictures, so send
  another one — and attempts are well formed from round 1. But the two freshness clauses cost them:
  copying, mirroring or one-square-editing a clue picture scores **0**, so the first hundred probes
  can look like a wall. What pays is a picture that is genuinely different: 7.8 % for a random one,
  12.8 % for a two-square edit, ~19 % for "everything the examples have in common" or a symmetric
  blob. Expect **5–20 %**.
* **With a demo**: one solved example shows a picture with a fourth black-count that is nothing like
  a copy — that teaches both freshness clauses in one look, which is worth ~10 points immediately.
  Cracking it outright needs the player to reconstruct enough of U to filter — 8 eligible templates,
  21 rules — from ~120 further probes and two or three example pictures per clue. Every template
  mapped is worth ~12 points. Expect **35–60 %**.

Mean across the two ≈ **0.25–0.4**, i.e. `testing` / low `calibrated`, with the risk on the **hard**
side (the same place `tresk` sat). Levers if it comes back too hard: (i) always emit 3 examples
instead of 65 % — more information, same minimality; (ii) drop the ≥ 2-squares-different clause,
which restores the 33–35 % one-square-edit foothold at the cost of making insight partly optional;
(iii) raise the eligibility ceiling from 0.20 to 0.28, which puts `3 blobs`, `4 blobs` and `2 black
corners` in play and lifts the random floor from 0.070 to ~0.11. If it comes back too easy: cut the
MAXBLOB and LONELY templates (the two whose parameters are densest) and lower the ceiling to 0.15.

**12-year-old test**: the object is a little pixel picture — cross-stitch, Minecraft, a Game Boy
sprite — and a kid names it from the clue alone, no demo needed. Every rule is one breath and every
one of them is something a kid can check with a finger on the page: "count the black ones… no, look,
three corners are black in both of them", "it's the same in a mirror", "the black bits are all
joined up", "the biggest lump is three squares". A kid contributes hypotheses immediately, and the
*lesson* of the class — "they never say *at least*, they never talk about the white squares, they
always say *exactly*" — is the kind of thing a kid notices before an adult does. The
nameable-pattern risk is real (these *are* nameable rules), but the difficulty lives in the size of
U, the loose-cousin traps and the thin 0/1 channel, not in any single rule being obscure.

---

# Revision 2 — the lineup answer (2026-09-05)

`challenges/lab/ospren.json` is now the **lineup** version; the version described in §§1–8 above is
kept byte-identical as `challenges/lab/ospren.v1.json`. Not committed; no arena run.

## 9. Why v1 had to change

Nobody has played `ospren` yet, so unlike `dornic`/`tresk`/`tavrik` there is no arena log to point
at. But the attack that took **77–97 %** off those three v1 classes is world-independent
(`docs/RULE_FAMILIES.md` "Revision 2"): build a pool of 250–350 generic predicates about the
object, keep every predicate true of **every** example, then emit an object satisfying all of them
at once. The hidden rule is somewhere in the pool, so the answer obeys it *by construction*; the
excluded traps cost nothing, because satisfying an extra rule is harmless. A 5×5 picture is if
anything an easier target than a bead string — the pool below writes itself. And v1's own witness
table already named the thing that was actually holding players: the **fresh-count** clause, which
is not part of the rule and which players fairly called invisible.

**The fix (revision 2): the answer is a choice, not a construction.** Both freshness clauses are
gone; the answer is which of four candidate pictures obeys the hidden rule.

## 10. The v2 format

Blocks separated by one blank line. The first 2–3 blocks are the **examples** (five lines of five
characters each); the last four are the **candidates**, each a block of six lines whose first line
is just the candidate's number:

```
....#              <- example 1
#....
...#.
#....
....#

.###.              <- example 2
#..##
#.#.#
##..#
.###.

1                  <- candidate 1
#...#
#...#
##...
#...#
#...#

2
.#...
...
```

A five-line block is an example, a six-line block starting with a digit is a candidate, and the
candidates are always the last four blocks — three independent ways to parse the same layout, which
is why the digit lines are there at all (a blank line alone cannot separate the two halves when the
objects are themselves multi-line). The answer is the candidate that obeys the rule, written back
**verbatim** (whitespace-insensitive, with or without its number line) **or as its index 1–4**.

* **U is unchanged** — 10 templates, 29 rules, 21 eligible, 8 competitors, still an antichain — so
  §2's table, the density figures and the antichain argument all still hold.
* **The fresh-count and ≥ 2-squares clauses are gone** (revision 2 §5). The examples still have
  distinct black-counts, but that is now purely a generator invariant forced by the COUNT
  competitors, **not** a scorer clause.
* **The floor is 1/4 = 25 %** (was ~7 %), and the ceiling for a player who has mapped U is 100 %.

## 11. How the lineup is built (revision-2 rules 1–5, 5b, 5c)

1. **Exactly one candidate obeys the rule** — verified in `generate` on every clue (500/500).
2. **Same size.** All four candidates have the **same number of black squares** (500/500). This is
   the picture world's version of `tresk`'s equal lengths, and it is worth more here than there: it
   makes every count-shaped statement — and three of the fourteen traps, and the ~70 count-shaped
   predicates of the outside pool — matched for free.
3. **Matched trap profiles (§5b).** The generator buckets sampled pictures by *which* of the
   example-consistent excluded rules they fire and assembles the lineup inside one bucket, so all
   four candidates fire exactly the same traps (500/500). Every trap heuristic, and any count of
   traps, is therefore worth **exactly 25.0 %** — see the table in §14.
4. **The count defence, both readings.** `generate` carries a **300-predicate** outside pool
   (§12) plus a base rate for each, measured on its own 16 000-picture pool. It scores every
   candidate by the plain count of surviving predicates it satisfies **and** by their
   rarity-weighted total (−log base rate), and aims the true candidate's **rank on both** at a
   place drawn uniformly from the sixteen (count rank, rarity rank) squares, falling back through
   the rest in order of distance. Decoys are drawn at random, **targeted** at the tight surviving
   predicates through a per-predicate index, and finally taken from the near or far end of their
   distance order from the truth so that "the odd one out" is aimed too.
5. Uniqueness and minimality inside U are unchanged and still verified on every clue; no candidate
   is an example and all four are distinct (500/500 each).

### The outside pool (300 predicates)

No player has played `ospren`, so the pool is the one a strong player *would* enumerate, written in
the style of the round-1 winner's `zpools.py`: `n=k` for every k and every `n>=k` / `n<=k` bound;
the count in each of the five rows and each of the five columns; rows/columns used, full and
equal; max/min row and column; corners (each one, the count, "all the same colour"); blobs, biggest
blob, smallest blob, "has a blob of size k", lonely squares, touching pairs; the five symmetries
(mirror, top-bottom, half turn, both diagonals) plus 4-way and 8-way; top row = bottom row, first
column = last column; the two halves above/below and left/right; the border count and the middle
3×3 count; 2×2 blocks, runs of 3 and 4 across and down, repeated rows, a solid rectangle, a
straight line; and the parities. It expresses **most of U** — which is exactly what makes the
rarity attack hard to beat (§12).

## 12. The findings

**The count attack is beaten.** "Pick the candidate satisfying the most surviving pool predicates"
— the direct port of the round-1 method — scores **31.6 %** (floor 25 %), with at least one decoy
strictly out-counting the truth on **68.4 %** of clues (revision 2 asks ≥ 40 %). "Fewest" scores
23.4 %, so it is not reversible either.

**The rarity-weighted attack is only blunted: 46.8 %** (42.5 % over a 2000-seed re-run). This is
the same wall `dornic` hit at 47.2 %, and for the same reason: on the clues where the hidden rule
is itself in the attacker's pool it is the rarest thing all the examples share, and no picture that
fails it can look as specially chosen. Two levers moved it:

| lever | effect on the rarity attack |
|---|---|
| matched trap profiles + equal black-counts + rank aiming (the base build) | ~58 % |
| **prefer example sets that leave the most rare outside predicates alive** | 58 % → ~47 % |
| **re-weight the templates toward the derived readouts** (blobs, lonely, maxblob) | 47 % → **43 %** |

Per-template rarity attack, measured over 600 clues before the re-weighting: **spread 70 %,
corners 60 %, eqline 51 %, fullline 47 %, sym 43 %, maxblob 40 %, lonely 33 %, blobs 30 %**. The
ordering is exactly RULE_FAMILIES §5c's prediction: a rule over a **derived** quantity — how many
separate blobs there are, how many squares stand alone, how big the biggest lump is — takes two
steps to read off a picture, so a decoy can be built to imitate it; a rule you can see in one
glance (how many corners are black, how many rows the blacks use) cannot. The weights now lean
the other way (blobs 1.4, lonely 1.4, maxblob 1.25, sym 1.05, fullline 1.0, eqline 0.9,
corners 0.7, spread 0.55); the template is still drawn **before** its parameter.

**Two examples beat three.** The generator builds up to four minimal example sets of each size and
prefers the one that leaves the most **rare** outside predicates alive, because those are the
coincidences a decoy can be built to carry. Two-example sets win that criterion almost always:
**2 examples 90.5 %, 3 examples 9.4 %** over 2000 seeds (v1 was 52/48). The measurement behind the
choice is blunt — with the set drawn without that preference, a decoy could out-score the truth on
only **19 %** of three-example clues against **62 %** of two-example ones (mean rare surviving
predicates 3.8 vs 5.8). *A third example removes exactly the coincidences the decoys need.* This is
the constructive version of `dornic`'s discarded "anchor" idea: rather than forcing the examples to
share a second tight non-U property (which broke uniqueness there), simply prefer, among example
sets that are already unique and minimal, the ones that happen to share more.

**No template had to be demoted** (the brief asked for the check). `tavrik` had to demote "exactly
*n* vowels" because two of its traps were "at least as many vowels as…" and "at most as many
as…", whose conjunction on such a clue **is** the rule, so no decoy could share the truth's trap
profile. `ospren` has exactly one at-least/at-most pair among its fourteen exclusions — "at least
*n* black squares" / "at most *n* black squares", fitted to the clue's smallest and biggest — and
their conjunction is a **range**, never a single count, because the examples always disagree about
the number of blacks; and COUNT is a competitor-only template anyway. Empirically a matched-profile
lineup was found on **500/500** clues and all 21 eligible rules are drawn over 2000 seeds.

**The residue that is left: "pick the odd one out" scores 32.2 %** (and its inverse, the medoid,
13.6 %). A picture that obeys a structural rule is genuinely a little unlike three that do not —
mean truth-to-decoy Hamming distance 10.3 against 9.8 decoy-to-decoy — and aiming the truth's
place in the look-alike order (each decoy taken from the near or the far end of its group's
distance order, all eight patterns tried plus random draws) only halves the tell. It is named
here rather than hidden: it is the second-best cheap heuristic in the class after the
rarity-weighted count.

## 13. Three demos

```
seed 25   hidden rule: exactly one row is completely black          (2 examples)

  EXAMPLES               CANDIDATES 1      2      3      4
   ...#.  .....        ..##.  ..#.#  .....  #####
   #####  #####        ##..#  ..##.  #####  ##..#
   ....#  ##.#.        ...#.  .#.#.  .....  .....
   ...#.  ####.        ..#.#  #...#  .....  ..##.
   .#...  .....        ##...  .#.#.  #####  .....
  ANSWER: 4   (##### ##..# ..... ..##. .....)

seed 15   hidden rule: the picture looks the same in a mirror       (2 examples)

  EXAMPLES               CANDIDATES 1      2      3      4
   #.#.#  #...#        .###.  ..#..  .##..  .###.
   ..#..  #...#        #..##  ##.##  #..##  ##..#
   .###.  .....        .#...  #.#.#  #.###  #.#.#
   ..#..  .....        #.###  ##.##  #####  #..##
   #.#.#  .#.#.        ###.#  #.#.#  .#...  .###.
  ANSWER: 2   (..#.. ##.## #.#.# ##.## #.#.#)

seed 21   hidden rule: there are exactly 2 blobs                    (3 examples)

  EXAMPLES                      CANDIDATES 1      2      3      4
   ....#  #....  .#...        .....  .....  .....  .....
   .....  .....  .....        .....  ....#  ##...  ..#..
   .....  .....  .....        ...#.  #....  .....  .#.#.
   #....  .....  .....        ...#.  .....  ##...  ..#..
   #....  ..###  ....#        ...##  #...#  .....  .....
  ANSWER: 3   (..... ##... ..... ##... .....)
```

Note demo 1: all four candidates have **ten** black squares, candidate 3 has *two* full rows (so it
fails "exactly one"), and candidate 2 has two blacks in every row — a U rule (`every row the same
number`) that the examples have already killed. Demo 2: all four have fifteen blacks and all four
have `first column = last column`, the mirror's loose cousin and one of the fourteen traps; only
candidate 2 is actually its own mirror. Demo 3: four blacks each, and candidate 1's four squares
are joined into one blob while candidate 4's four stand apart in three.

## 14. Witness table — 500 fresh clues (seeds 1 000 000 – 1 000 499)

The answer is a choice among four, so the floor is **25 %** and there is no well-formedness column.

| witness | score |
|---|---|
| **the true rule (`solve`)** | **100.0 %** |
| **the in-U intersection** (the candidate satisfying every rule of U the examples allow) | **100.0 %** |
| a player who knows U minus its **two rarest templates** (spread, corners) | 89.4 % |
| a player who knows U minus sym + eqline | 81.8 % |
| a player who knows U minus blobs + lonely | 74.6 % |
| **MOST surviving pool predicates, weighted by rarity (−log base rate)** | **46.8 %** |
| a player whose universe is U + the 14 exclusions, random survivor | 35.0 % |
| the candidate **least like the other three** (outlier) | 32.2 % |
| **MOST surviving pool predicates (the round-1 attack, 300 preds)** | **31.6 %** |
| the candidate least like any example | 29.0 % |
| **pick candidate 1** | 27.8 % |
| the candidate firing the MOST fitted traps | 26.8 % |
| EXCLUDED: **each of the fourteen, when it fits** | **exactly 25.0 %** |
| a player whose universe is U + the 14 exclusions, a **wrong** survivor | 24.4 % |
| the candidate most like an example | 23.8 % |
| the candidate satisfying the FEWEST surviving pool predicates | 23.4 % |
| the candidate firing the FEWEST fitted traps | 23.4 % |
| **pick a random candidate (the floor)** | 22.4 % |
| the candidate closest to the other three (medoid) | 13.6 % |

The fourteen excluded rules, with how often the trap fitted to the clue is consistent with *every*
example:

| excluded rule (fitted to the clue) | fits | scores |
|---|---|---|
| every square black in all the examples is black | 100 % | **25.0 %** |
| at least *n* black squares (the clue's smallest) | 100 % | **25.0 %** |
| at most *n* black squares (the clue's biggest) | 100 % | **25.0 %** |
| the same number of blacks as an example | 100 % | **25.0 %** |
| there is a black square in the middle column | 56.4 % | **25.0 %** |
| the middle square is white | 49.0 % | **25.0 %** |
| every row has at least one black | 33.8 % | **25.0 %** |
| as many blacks above the middle row as below | 30.8 % | **25.0 %** |
| as many blacks left of the middle column as right | 24.2 % | **25.0 %** |
| the four corners are all the same colour | 19.6 % | **25.0 %** |
| the top row is the same as the bottom row | 14.2 % | **25.0 %** |
| the first column is the same as the last | 10.6 % | **25.0 %** |
| the top row is all white | 5.8 % | **25.0 %** |
| no two black squares touch | 2.8 % | **25.0 %** |

In v1 these paid 9.4–19.4 %; matched profiles make them exactly neutral. Mean **6.5** of them are
consistent with any one clue (min 4, max 10). The v1 lesson — "this class never says *at least*" —
no longer pays on its own; the game is now purely **which** rules the class uses.

Other measured numbers (500 clues unless stated):

* uniqueness 500/500, minimality 500/500, all example black-counts distinct 500/500, examples
  pairwise ≥ 3 squares apart 2000/2000;
* exactly one candidate obeys the rule 500/500; all four the same number of blacks 500/500; four
  distinct candidates 500/500; no candidate equal to an example 500/500;
* matched trap profiles 500/500; every decoy fires ≥ 1 consistent trap 500/500;
* true-candidate position 139/124/127/110; example counts 2 → 90.5 %, 3 → 9.4 % (2000 seeds);
* rank of the truth by plain predicate count 158/100/125/117 (a decoy beats it on **68.4 %**), by
  rarity-weighted total 234/108/106/52 (**53.2 %**);
* mean 33.1 outside predicates survive the examples, of which ~5 are rare (base rate ≤ 0.25);
* hidden-rule mix over 2000 seeds: 2 blobs 202, 1 blob 170, 3 lonely 127, one full row 126,
  5 lonely 121, one full column 121, equal rows 114, 4 lonely 108, biggest blob 2 → 103, equal
  columns 97, 3 corners 89, biggest blob 3 → 89, biggest blob 4 → 89, 4 corners 87, top-bottom
  flip 85, mirror 82, half turn 72, 1 row 32, 2 columns 30, 2 rows 29, 1 column 27.

## 15. Validation

`python tools/quickcheck.py challenges/lab/ospren.json --seeds 300` →
`OK ospren  gen=12.74ms score=0.18ms solve=0.21ms`, **no warnings** (the 1024 scorer cap is the
quickcheck default).

| quantity | value | cap |
|---|---|---|
| `score` source | **899 chars** (v1: 1004) | 1024 (the rule-family raise) |
| `generate` source | 29 821 | 50 000 |
| `solve` source | 1 841 | 5 000 |
| `generate` | **2.39 ms mean**, 1.11 ms median, 12.5 ms p99, 17.9 ms max over 5000 seeds | 100 ms |
| `score` | 0.07 ms mean, 0.18 ms max | 50 ms |
| `solve` | 0.11 ms mean, 0.28 ms max (v1: 27 ms — nothing to rejection-sample any more) | 2000 ms |
| clue | 192–223 chars (v1: ≤ 91) | 1024 |
| answer | 29 chars, or 1 | 1024 |

Module-level tables cost **≈ 4.3 s** once per worker (v1: 0.46 s): the 16 000-picture pool, its
29-bit U mask, 10-bit trap mask, 25-bit square mask and 300-bit outside-pool mask, plus the
per-predicate rarity index. Not charged to `max_generate_ms`; a call is then integer ANDs,
`bit_count`s and a handful of small sorts. `generate` is deterministic across processes and hash
seeds (md5 of the first 200 clues checked in three interpreters).

`score` was checked on 500 clues × every candidate and × every index (exactly one scores 1 each
time) and rejects `''`, `x`, `0`, `5`, `9`, `1 2`, `1`×100, `#`×4000, the clue itself, the example
block alone, a Unicode digit, a well-formed picture that is not in the lineup, and the true
candidate with one square rubbed out. It forgives surrounding and internal whitespace, accepts the
answer written as one space-separated line, and accepts the candidate's number line if the player
copies it. `solve` re-derives the survivor exactly as the scorer does and returns the true
candidate verbatim — it constructs nothing, so there is nothing to leak.

## 16. Predicted classification

**Calibrated, and much flatter than v1.**

* **Without a demo**: the shape reads as a multiple choice (two little pictures, a gap, four
  numbered ones), so a player who works that out is on the **25 %** floor from probe one; a player
  who answers with a constructed picture scores 0 until the 0/1 feedback teaches them. The
  round-1 method degrades to counting surviving predicates: **32 %**. A team that weights its
  predicates by rarity — and the round-1 winner already computed base rates — reaches **47 %**.
  Expect **25–45 %**.
* **With a demo**: a demo now teaches only the format, because there is no invisible convention
  left to learn. The way up is to reconstruct U, and the moment a player filters U correctly they
  score **100 %**, because the in-U intersection is exact. Eight templates and 21 rules from two
  example pictures per clue is a real climb, but a much shorter one than `dornic`'s 91 rules, and
  every rule is nameable at a glance. Expect **45–70 %**.

Mean across two Opus teams ≈ **0.4–0.55** → `calibrated`, with the risk on the **easy** side and
named: the rarity-weighted count is a free ~47 %, and "the odd one out" a free ~32 %. Levers if it
comes back too easy: (i) push the template weights further toward blobs/lonely/maxblob (spread and
corners are the leaky ones); (ii) go to k = 5 candidates (floor 20 %); (iii) add templates whose
readout no natural pool carries — "the blacks make a shape that is the same width as it is tall"
was rejected in v1 for density, but "exactly *n* squares touch the edge" is available and is
outside the pool. Too hard: (iv) k = 3 (floor 33 %); (v) let one decoy obey a rule of U that all
but one example allows, so a partly-mapped player is rewarded rather than punished.

**12-year-old test**: better than v1, for the same reason `tresk` v2 was. The object is still a
little pixel picture — cross-stitch, Minecraft, a Game Boy sprite — and the question is now the
one every kid knows from a puzzle book: *which of these four fits?* A kid can check four 5×5
pictures against a hypothesis with a finger in seconds, all four have the same number of black
squares so the cheap "count them" answer is visibly useless, and the 0/1 signal is now about the
rule rather than about an invisible novelty convention. The one loss is the v1 lesson ("they never
say *at least*"), which no longer pays on its own because the traps have been made exactly
neutral.

---

# Iteration 3 — 2026-09-05, **v3: a universe of RELATIONS** (`docs/RULE_FAMILIES.md` "Revision 3")

v2 is kept as `challenges/lab/ospren.v2.json`; the shipped file is `challenges/lab/ospren.json`.

## 17. What the arena showed, and the attack to beat

`lad-ospren-v2-1`: two Opus centaurs, **neither spent a demo on ospren**, and they scored
**87 % and 80 %** (target ≈ 50 %). Their notes describe one engine, used on all six lineup
classes:

1. **Round 1: skip everything** — ~300 clues harvested free, the base-rate corpus.
2. **Round 2: answer a RANDOM candidate.** With k = 4 a quarter come back correct: **~30 gold
   labels for nothing** — `ospren1b`'s "30× what a demo gives".
3. **Per clue**: enumerate the 5×5 predicate bank, keep what is true of every example and of
   **exactly one candidate**, weight by rarity (`freq^-2.5 / satisfiers^6`), answer the
   candidate the rarest survivor points at.
4. **Learn U from the labels**: which predicate uniquely explained each known-correct answer.

Revision 2's defences (matched trap profiles, rarity-aware decoys) were both in v2 and both
lost, for one reason: **every rule of v2's U was itself a predicate in the attacker's bank.**

### The attacker's bank, rebuilt (recipe step 1)

Union of the two 5×5 banks the players actually brought — `ospren1a/strategy.py::f_ospren`
(44 keys: `k`, `k%2`, `hmir/vmir/rot180/tr/atr/rot90`, `nrows`, `ncols`, `nfullrow`, `ncorner`,
`border`, `rowc`, `colc`, `rowc_sorted`, `ncomp`, `maxcomp`, `isolated`, `noadj`, `nsq`,
`top/bot/left/right`, `topbot`, `leftright`, `maindiag`, `antidiag`…) and
`ospren1b/features.py::f_ospren` (80 keys: `tot%m`, `rmin/rmax/cmin/cmax`, `rowsame`, `symd`,
`syma`, `diag`, `anti`, `inner`, `n2x2`, `maxrunrow/col`, `niso`, `rowparity`, `npalrow`,
`quad`, `qsorted`, `adjpairs`, `ndistrow`, `parA/parB`, `ncomp0`, `nholes`, `deg`, `totge k`,
`halffull`…) — **plus the obvious extensions a second round adds**: the count in each
individual row and column, the bounding box (`bw`, `bh`, `barea`, `btop`, `bleft`), which sides
of the frame are touched (`ttop/tbot/tleft/tright`, `nsides`), `tb_same`, `lr_same`,
`neqrowpairs`, `neqcolpairs`, 8-connected blobs, `mincomp`, `compsizes`, `diagpairs`,
`emptyrows`, `nsinglerow`. **153 feature keys, 3 442 realised (key, value) predicates** over the
20 000-picture pool; the 808 with base rate ≥ 1.5 % are the ones `generate` carries as a bit
mask for aiming (the players floor their own frequency estimates at 5 %, so nothing below that
is usable to them anyway).

### The retirement test (recipe step 2) — **all 29 of v2's rules are gifts**

| v2 rule | the bank predicate that says the same thing | J |
|---|---|---|
| exactly *n* marks (5, 6, 7) | `k == n` | **1.00** |
| its own mirror / flip / half turn | `hmir` / `vmir` / `rot180` | **1.00** |
| exactly *n* corners (1–4) | `corners == n` | **1.00** |
| the marks sit in exactly *n* rows / columns | `nrows == n` / `ncols == n` | **1.00** |
| exactly *n* blobs (1–4) | `ncomp == n` | **1.00** |
| exactly one row / column completely full | `nfullrow == 1` / `nfullcol == 1` | **1.00** |
| the middle square is marked | `centre == 1` | **1.00** |
| every row / column the same number | `rowsame` / `colsame` | **1.00** |
| the biggest blob is *n* (2–4) | `maxcomp == n` | **1.00** |
| exactly *n* marks stand alone (3–5) | `niso == n` | **1.00** |

**29 of 29 at J = 1.00.** Every one is retired to the trap list. (`tavrik` measured 0.97–1.00
and `tresk` 1.00 on their own v2 universes — the same result three times.)

## 18. The universe U — 12 templates, 33 rules

"density" = the share of the 20 000-picture generator pool that obeys the rule (the uniform-noise
figure is in brackets where it differs sharply). **"bank J"** = best Jaccard against any of the
3 442 realised bank predicates — the number that decides whether the attacker can *express* the
rule at all. Parameter convention, shared with the scorer: **A = the rows if q < 2 else the
columns**.

| t | kid sentence (read it aloud) | params | density | bank J | in U? |
|---|---|---|---|---|---|
| 0 | "every row of marks reaches the **left / right wall**" · "every column of marks reaches the **top / the floor**" | q = 0,1,2,3 | .108–.112 (.027) | **.23–.24** | **IN** |
| 1 | "every mark has a mark **right beside it**, left or right" · "…**right above it or right below it**" | q = 0,2 | .060–.062 (.006) | **.23** | **IN** |
| 3 | "the **first two rows** come back again as the **last two rows**" · same for columns | q = 0,2 | .021 (.004) | **.17** | **IN** |
| 4 | "the **top row and the middle row** are exactly the same" · "the **middle row and the bottom row**…" · same for columns | q = 0,1,2,3 | .116–.121 | **.19** | **IN** |
| 5 | "**two rows next to each other** are exactly the same" · same for columns | q = 0,2 | .277 | **.34–.39** | **IN** |
| 6 | "the **top row and the first column** have their marks in the same places" · 2nd · middle · 4th · bottom/last | q = 0..4 | .112–.128 | **.21–.26** | **IN** |
| 7 | "in **every row** the marks are all **in one piece**" · same for columns | q = 0,2 | .307 | **.40** | **IN** |
| 8 | "every **row of marks starts in the same column**" · "every column of marks starts in the same row" | q = 0,2 | .153–.155 | **.28** | **IN** |
| 9 | "every mark in the **top row** has a mark **right under it**" · bottom · first column · last column | q = 0..3 | .198–.202 | **.31** | **IN** |
| 10 | "the picture looks the same **in a mirror**" · "**flipped top to bottom**" | q = 0,1 | .057 / .062 | 1.00 | **IN** (cheap, ×2 weight) |
| 11 | "**exactly one row** is completely full" · "exactly one column is" | q = 0,2 | .041 | 1.00 | **IN** (cheap, ×2) |
| 12 | "**exactly three corners** are marked" · "**all four corners** are marked" | q = 3,4 | .057 / .031 | 1.00 | **IN** (cheap, ×2) |
| — | exactly *n* marks · *n* corners · *n* blobs · biggest blob *n* · *n* lonely marks · marks in *n* rows/columns · the middle square · every row the same number · half turn | | .004–.36 | **1.00** | EXCLUDED (all of v2's U) |
| — | at least / at most *n* marks · every square marked in all the examples · a mark in the middle column · every row has a mark · as many above as below · as many left as right · the corners all alike · top row = bottom row · first column = last column · the top row is empty · no two marks touch · touches the frame on *n* sides · has a hole · longest run *n* | | | 1.00 | EXCLUDED (v2's trap list + the bank's own extensions) |

|U| = **33 rules over 12 templates**, **27 of them relational** (bank J .17–.40) and 6 cheap
(J 1.00, on purpose). Antichain verified by brute force over the 20 000-picture pool **and**
150 000 uniform-random pictures: **0 nesting violations**, minimum support 420 pictures.

### Templates measured and thrown out this round

| template | density | bank J | why not |
|---|---|---|---|
| "every mark touches another mark **corner to corner**" | .086 | .31 | passed every test — **dropped for scorer room only** (128 of the 1024 chars for one rule) |
| "the marks all **rest on the floor** or on another mark" (gravity, 4 walls) | .036 | .34–.39 | ⊂ template 0 ("every column of marks reaches the floor"), which is denser and reads better |
| "**two lumps are exactly the same shape**" | .538 | .73 | density > .5: four decoys all *lacking* it is itself a signature |
| "**all the lumps are the same shape**" | .091 | .84 | it is `maxcomp == 1` in disguise |
| "the drawing is **as wide as it is tall**" | .465 | .81 | `barea == 25`, and too dense |
| "the picture touches the frame on exactly *n* **sides**" | .053–.38 | **1.00** | `nsides == n` — a gift; kept as a trap |
| "the **top row is the same as the bottom row**" / first = last column | .16 | **1.00** | `tb_same` / `lr_same` — gifts (they were v2 traps and stay traps) |
| "**no two marks share a row or a column**" | .014 | .38 | forces ≤ 5 marks, so the clue leaks the count; and ⊂ "no two marks touch" |
| "every **lump is a straight line**" | .317 | .55 | half a bank predicate (`maxruncol == 1`) |
| "the **biggest lump is wider than it is tall**" | .277 | .30 | needs blob-finding in the scorer; 1024 chars would not hold it |
| "the **first mark and the last mark** (reading like a book) are in the same column" | .154 | .20 | reading order is a puzzle-book device, not something a kid *sees* |
| "**all the lumps are different sizes**" · "the two biggest lumps are the same size" | .27 / .24 | .64 / .35 | counted relations — the tavrik lesson (§ kid constraint) |

**The kid constraint drove the final cut, not only the Jaccard.** `tavrik` v3's judge score fell
4.7 → 3.83 on rules that read as puzzle-book tricks; `tresk` v3 held 4.5 by keeping only
relations a kid **spots by eye**. Every rule of ospren v3 is one of those: a row against a
column, a mark against its neighbour, a line of marks against a wall, two rows against each
other. Nothing here counts anything except "three corners" and "one full row", which a kid
counts on one hand. The two counted candidates on the recipe's own list — "the left half holds
as many marks as the right" and "the marks touch the frame on exactly two sides" — were **not
used** (the first is a v2 trap already, the second is `nsides` in the bank).

**One extra legibility rule**, new here: for templates 3, 4 and 6 the examples and the true
candidate are always drawn from pictures that satisfy the rule **visibly** — "the top row and
the middle row are exactly the same" is technically true of two *empty* rows, and a kid reading
such an example learns nothing.

## 19. What changed, item by item

| | v2 | v3 |
|---|---|---|
| candidates | 4 (floor 25 %) | **5** (floor 20 %) |
| examples | 2 in 90 %, 3 in 10 % | 2 in **95.6 %**, 3 in 4.4 % |
| U | 10 templates / 29 rules, **all bank J 1.00** | **12 templates / 33 rules**, 27 relational, bank J **.17–.40** |
| competitor-only rules | 8 (counts, 1–2 corners, 3–4 blobs, middle square) | **none** — every rule of U may be the hidden one |
| what forces the clue's layout | the COUNT competitors (examples must differ in mark count) | nothing: no rule reads the total, so example counts are free |
| traps | 14 families, mean 6.5 fit | **31 families**, mean 7.15 fit, 29 of them v2's own rules |
| decoys aimed at | the count and rarity ranks | **rarity, then count, then look-alike, then family resemblance** (4 orders) |
| bank carried inside `generate` | 300 predicates | **808** (of 3 442 realised) |
| instance distribution | uniform noise (a count 2–15, then random squares) | a **mixture of little pictures** (scatter, lumps, repeated lines, mirrored halves, stacks) |
| `score` | 899 chars | **1 017 chars** |
| simulated attack, 30 labels | **87.3 %** | **46.4 %** |

## 20. Levers, measured (identical conditions, 400 test clues, 60 labels)

| build | k | floor | simulated attack |
|---|---|---|---|
| **v3 as shipped** | 5 | 20 % | **47.2 %** |
| minus lever 3 — **v2 as shipped** (same engine, same bank) | 4 | 25 % | **85.3 %** |
| minus lever 5 (decoys not aimed at all) | 5 | 20 % | 54.2 % |
| minus lever 1 (k = 4) | 4 | 25 % | 51.0 % |
| lever 1 pushed (k = 6) | 6 | 16.7 % | 44.5 % |
| minus lever 2 (three-example clues) | 5 | 20 % | 44.8 % |

Read off the differences: **the relational universe (lever 3) is worth ≈ 38 points**, the
aiming (lever 5) **≈ 7**, the fifth candidate (lever 1) **≈ 4**. Two honest departures from the
recipe's expectations: **k = 6 does buy 2.7 points here** (tavrik: nothing; tresk: −3.4) and
**three-example clues buy 2.4** rather than costing 3 — but a sixth candidate is a sixth block
of five lines in an already 7-block clue and a third example is a third picture to hold in the
head, so both were declined on the 12-year-old test rather than on the attack number. They are
the first two levers to reach for if the class comes back too easy.

## 21. The attacker table, v2 vs v3

Full engine: skip-harvest 300 clues for base rates → answer a random candidate on a disjoint
1 600 clues, keeping the ~1/k that come back correct as gold labels **and the wrong picks as
negatives** → per-predicate unique-explanation weights → rarity-weighted pick. 500 fresh test
clues (seeds 1e6 …), live unfiltered feature bank (every realised (key, value) pair, base rate
floored at 5 % as the players do).

| labels | v2 as shipped (k = 4, floor 25 %) | **v3 (k = 5, floor 20 %)** | v3 with a bank that also holds all of U |
|---|---|---|---|
| 0 | 76.8 % | **44.2 %** | 82.8 % |
| 30 | 87.3 % | **46.4 %** | 87.2 % |
| 60 | 85.3 % | **47.0 %** | 88.6 % |
| 120 | 87.8 % | **48.0 %** | 90.0 % |
| 240 | 88.0 % | **47.4 %** | 91.4 % |

The shape is the point: v2 is a lookup from the first free labels, v3 is **flat**. The simulator
scored 85–88 % on v2 where the real players scored 80–87 %, so it is a fair-to-slightly-strong
model of an Opus centaur and its v3 figure is not an optimistic one.

**The honest ceiling.** The **in-U intersection is 100.0 %**. An attacker whose bank also
contains all of U reaches 88.6 % at 60 labels and learns U to **90 % coverage in ≈ 360 labels**
(coverage = the share of fresh clues whose true rule the learner has confidently identified,
*m* ≥ 4 firings and *n*/*m* ≥ 0.7: 0 % at 30 labels, 17 % at 60, 60 % at 120, 89 % at 240,
91 % at 360). With the generic bank alone, coverage can never pass the three cheap templates
(36.6 % of clues). The gap **47 % → 90 %** *is* the class.

## 22. Three demos

```
seed 1000035   hidden rule: every column of marks reaches the floor

  EXAMPLES             CANDIDATES 1      2      3      4      5
   .....  .....       #####  .####  .##.#  ###..  #####
   ..##.  .....       #####  #...#  .###.  ##..#  #.#..
   ..#..  ..#..       .#..#  #...#  .#.#.  .#..#  .....
   ..##.  ..##.       #...#  .#..#  .###.  ##..#  #.#..
   ..##.  #.###       .....  .####  .##.#  ###..  #####
  ANSWER: 5

seed 1000023   hidden rule: the middle row and the bottom row are exactly the same

  EXAMPLES             CANDIDATES 1      2      3      4      5
   .#...  ###..       .....  .....  .....  #.#..  .....
   #.#..  ##.##       #....  .##..  .....  ..#..  #.#.#
   #....  ..#.#       #....  #..#.  .....  .....  .....
   #....  .....       ###..  ....#  .#.#.  .#..#  .....
   #....  ..#.#       #....  .#...  #.###  ..#..  #.#.#
  ANSWER: 1

seed 1000011   hidden rule: exactly one column is completely full   (a CHEAP template)

  EXAMPLES             CANDIDATES 1      2      3      4      5
   #.#..  .#.#.       .##.#  #...#  ...#.  ..#.#  #....
   #.##.  #..##       .##..  #####  ..#..  #....  ...##
   ##...  .#.#.       .##..  ..#..  #####  ..##.  #####
   #.##.  ...#.       ..#..  ...#.  ###..  #####  ....#
   #.#..  ..###       ..###  ..##.  ..#..  ..#..  .#.#.
  ANSWER: 1
```
(In the real clue the five candidates are five six-line blocks, each headed by its number.)
Demo 1 is the class in one picture: every candidate has fourteen marks, every one fires exactly
the same excluded rules, and the only one whose every marked column reaches the bottom row is
number 5. Demo 2 is the pure relation — two rows compared by eye, nothing counted. Demo 3 is
the learnable slope: a kid looks for the full column and so does a predicate bank.

## 23. Witness table — 500 fresh clues (seeds 1e6 … 1e6+499)

Five candidates, so the floor is 20 %.

| witness | score |
|---|---|
| **the in-U intersection — a player who knows U** | **100.0 %** |
| the true rule (`solve`), verbatim and by index | **100.0 % / 100.0 %** |
| a player who knows U minus **two templates** | 80.6 – 93.2 % (median 86.8) |
| **the full revision-3 attack, 30 labels** | **46.4 %** |
| … at 0 / 60 / 120 / 240 labels | 44.2 / 47.0 / 48.0 / 47.4 % |
| the **rarest unique surviving bank predicate** (the players' own rule) | 44.8 % |
| the candidate with the most **touching pairs** | **30.8 %** |
| the candidate with the fewest **lonely marks** | 30.6 % |
| the candidate with the longest **straight run** | 30.4 % |
| the candidate with the most **marked corners** | 30.4 % |
| the candidate **least like the other four** (the odd one out) | 28.6 % |
| the candidate with the fewest **lumps** | 27.6 % |
| the candidate **least like an example** | 25.0 % |
| **MOST surviving bank predicates** (the round-1 count attack) | **24.2 %** |
| pick candidate 1 | 21.8 % |
| the candidate **most like an example** | 20.2 % |
| **pick a random candidate (the floor)** | **19.0 %** |
| the candidate with the most lumps / most lonely marks / fewest touching pairs | 17.4 / 16.0 / 14.6 % |
| the candidate closest to the other four (the medoid) | 15.2 % |
| **each of the 21 trap families that ever fit** | **0 – 33 %** (pure tie-breaking) |

A decoy strictly **out-counts** the truth on **74.0 %** of clues (revision 2 rule 2 asks for
≥ 40 %) and carries a **rarer** unique explanation on 52.0 %.

The excluded rules are *structurally* dead, not merely weak: over 500 clues **all 3 574 fitted
traps are satisfied by all five candidates or by none (3 574/3 574)**, so no trap, no count of
traps and no combination of traps separates the lineup, and a player whose universe is U *plus*
the 31 trap families is worth exactly a player who knows U. The 0–33 % spread in the table is
the random tie-break on samples of 1–362 fits. Fit rates over the 500 clues: at least *n*
marks 72 % · at most *n* marks 66 % · a mark in the middle column 56 % · the middle square is
empty 40 % · the touched sides of the frame 20 % · every square marked in all the examples
16 % · the longest straight run 15 % · the columns used 13 % · as many marks left of the middle
as right 12 % · as many above as below 11 % · the rows used 9 % · every row has a mark 8 % ·
the top row is the same as the bottom row 7 % · the first column is the same as the last 6 % ·
the count-agreement traps (exactly *n* marks, *n* blobs, *n* lonely marks, one full line) 0–5 %.

Other measured numbers (500 clues unless stated): uniqueness 500/500 · minimality 500/500 ·
exactly one candidate obeys the rule 500/500 · all five candidates the same number of marks
500/500 · five distinct candidates 500/500 · no candidate equal to an example 500/500 ·
examples per clue 2 → 478, 3 → 22 · true-candidate position 109/96/94/107/94 · candidate mark
counts 3–14, every count drawn · template mix 19–65 per template, all **33 rules drawn** ·
cheap templates 36.6 % of clues · over **20 000 seeds, 20 000 distinct clues and 0 fallback
clues**.

## 24. Validation

`python tools/quickcheck.py challenges/lab/ospren.json --seeds 300 --cap max_score_code_chars=1024`
→ `OK ospren  gen=14.75ms score=0.21ms solve=0.21ms`, **no warnings**.

| quantity | value | cap |
|---|---|---|
| `score` source | **1 017 chars** (v1 1004, v2 899) | 1024 (the rule-family raise, RULE_FAMILIES §4) |
| `generate` source | 26 504 | 50 000 |
| `solve` source | 1 661 | 5 000 |
| `generate` | **2.45 ms mean**, 1.76 ms median, 11.3 ms p99, 24.9 ms max over 5000 seeds | 100 ms |
| `score` | 0.083 ms mean, 0.21 ms max (junk included) | 50 ms |
| `solve` | 0.088 ms mean, 0.21 ms max | 2 000 ms |
| clue | 225–256 chars | 1024 |
| answer | 29 chars, or 1 | 1024 |

Module-level tables cost **≈ 6 s once per worker** (v2: 4.3 s): the 20 000-picture pool, its
33-bit U mask, its trap readouts and its 808-bit bank mask. Not charged to `max_generate_ms`,
but it is the reason the pool is 20 000 and not 30 000 — the sandbox gives a **60 s budget to
compile the whole seven-class pool**, and a bigger pool bought only 1.5 points of attack
(measured: 30 000 → 45.6 %, 20 000 → 46.4 %, 16 000 → 49.4 % at 30 labels).

`score` was checked candidate-by-candidate against `solve` on 600 clues × 5 candidates × 7
answer forms (verbatim · index · index with spaces · the candidate with its number line · one
space-separated line · a trailing newline · surrounding spaces) — **21 000 checks, 0
disagreements** — and returns 0 without raising for `""`, `"x"`, `"0"`, `"6"`, `"9"`, `"55"`,
`"1 2"`, `"1"×100`, `"#"×4000`, `"-1"`, `"1.0"`, the unicode digits `"١"` / `"²"`, a
well-formed picture that is not in the lineup, the clue itself, the example block alone and a
single example. The 33 rules are rebuilt in the scorer from a **33-character table** — one
character per rule, `chr(48 + 5*template + parameter)` — plus one thirteen-branch predicate
function, which is what bought room for nine relational templates inside 1024 chars.
`generate` is deterministic across processes and hash seeds (md5 of the first 200 clues
identical under `PYTHONHASHSEED` 0 / 1 / 12345). `solve` re-derives the survivor exactly as the
scorer does and returns the true candidate verbatim — it constructs nothing, so there is
nothing to leak.

## 25. Predicted classification

**Calibrated**, with the risk on the **easy** side and named.

* **Without a demo** the clue still reads as multiple choice from round 1 (two little pictures,
  a gap, five numbered ones of the same size), so every probe is well formed and the floor is a
  free 20 %. The engine that scored 80–87 % on v2 now pays **44 % at zero labels, 46–48 % once
  the free labels arrive, and stops improving.** The best cheap heuristic — "answer the
  candidate whose marks touch each other most" — is worth 31 %. Expect **30–50 %**.
* **With a demo** the demo teaches the format in one look and one worked rule. The way up is to
  notice that this class talks about **two rows, two columns, a mark and its neighbour, a line
  and a wall**, and to write those predicates down; a player who does scores 87–91 %, one who
  maps 10 of the 12 templates scores 81–93 %. Expect **45–70 %**.

Mean across two Opus teams ≈ **0.4–0.55** → `calibrated`. If it comes back **too easy**, the
levers in order are: drop the three cheap templates to single draw weight (measured: 30.8 % of
clues, attack 43.5 / 45.0 / 45.3 % at 0/30/60 labels), then k = 6 (−2.7), then three-example
clues (−2.4). If **too hard**: k = 4 (+3.8) or cheap templates at triple weight.

**12-year-old test (target: keep 4.3+).** The object is unchanged — a little pixel picture,
cross-stitch or Minecraft or a Game Boy sprite — and the task is still the puzzle-book one,
*which of these five fits?* What changed is **what the rules talk about**, and every one of
them is something a kid sees rather than counts. Read them aloud (RULE_FAMILIES §9): *every
column of marks reaches the floor · every mark has a mark right beside it · the top row and the
middle row are exactly the same · two rows next to each other are exactly the same · the top
row and the first column have their marks in the same places · in every row the marks are all
in one piece · every row of marks starts in the same column · every mark in the top row has a
mark right under it · the first two rows come back again as the last two.* Each is one breath
and each can be checked on a 5×5 picture with a finger in about three seconds — which is
exactly what a predicate bank is bad at and a kid is good at. The three cheap rules (its own
mirror, one full row, three corners) keep the v1/v2 flavour and give a kid an entry point on a
third of the clues. All five candidates have the same number of marks, so "count them" is
visibly useless, and the examples now *show* their relation rather than satisfying it vacuously.
