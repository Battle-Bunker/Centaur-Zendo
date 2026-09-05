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
