# NOTES — rule-family class, world = a string of 6–10 coloured beads (`tresk`)

Paradigm: `docs/RULE_FAMILIES.md`. A finite universe **U** of parametrised rules; the clue is a
minimal set of positive example strings that pins exactly one rule inside U; the answer is one more
string obeying it. The player does **not** know U, so their larger hypothesis space contains obvious
rules the class never uses. Learning **what this class never says** is the game.

Shipped file: `challenges/lab/tresk.json` (name checked unique against `challenges/` and
`challenges/lab/`). Not committed; no arena run (out of scope for this job).

> **2026-09-05 — sections 1–8 below describe v1**, which is now archived byte-identical as
> `challenges/lab/tresk.v1.json`. The shipped `tresk.json` is the **lineup** build of
> RULE_FAMILIES.md revision 2: the clue carries four candidates and the answer is *which one*.
> U, the antichain argument and the exclusion list are unchanged; the answer format, the
> witness table and the fresh-length clause are not. Start at **section 9**.

---

## 1. The world

One bead string per line, letters from **R G B**, **6–10 beads**: `RRGBGRBB`.
Three colours, not four: with four colours every "no two X touch" style rule becomes *more* likely
(a rare colour rarely doubles), and the whole space of lengths 6–10 is 88 209 strings, small enough
to brute-force the antichain check exactly.

**The examples in a clue always have different lengths, and the answer must use a length that is
not in the clue.** This is the one well-formedness convention, and it is the most important design
decision in the class (§5). It is *visible in the clue* — three lines of three different lengths —
so it is inferable, and a demo confirms it in one look.

---

## 2. The universe U — 8 templates, 38 concrete rules

Readout of a string `w` (this is exactly what the scorer computes):

```
f = (#R, #G, #B, longest block, number of blocks, length, palindrome?, #colours, all blocks same size?)
```

"density" = probability that a **random string of a random length 6–10** satisfies the rule — i.e.
what a player who answers at random scores when that rule is the truth. "R?" = may be the hidden
rule (the loose ones stay in U as **competitors** the generator must kill, but are never the answer).

| # | template (kid sentence) | grid | density per parameter | R? |
|---|---|---|---|---|
| a | "there are exactly *n* red / green / blue beads" | n = 2,3,4,5 (×3 colours) | .268 / .256 / .163 / .072 | 4, 5 |
| b | "the longest block of one colour is *n* beads long" | n = 2,3,4,5 | .496 / .301 / .097 / .027 | 4, 5 |
| c | "there are exactly *n* blocks" | n = 3,4,5,6,7 | .062 / .156 / .238 / .236 / .168 | 3, 4, 7 |
| d | "the string is *n* beads long" | n = 6…10 | .200 each | — (competitor) |
| e | "it reads the same backwards" | — | .021 | yes |
| f | "only two colours are used" | — | .135 | yes |
| g | "all the blocks are the same size" | — | .076 | yes |
| h | "there are as many red as green beads" (R/G, R/B, B/G) | 3 pairs | .171 | yes |
| i | "all the red beads come before all the green beads" (both must appear) | 6 ordered pairs | .120 | yes |

|U| = 38, of which **23 are eligible** to be the hidden rule (density ≤ 0.20). Mean density of the
hidden rule, measured over 500 clues: **0.105** — that is the floor a thoughtless player gets, and
the number the eligibility ceiling controls.

`generate()` draws the **template uniformly first** and only then a parameter, so no template is
rare merely because it owns fewer rules. Measured mix over 500 clues: before 80, equal 68, count 66,
palindrome 65, longest-block 63, two-colours 56, blocks 54, equal-blocks 48.

### Why 15 loose rules stay in U as competitors
"exactly 2 / 3 reds", "longest block 2 / 3", "5 / 6 blocks" and all five length rules are too
generous (.20–.50) to be an answer, but leaving them **in U** means the generator has to kill them,
which forces the clue to do layout work for free: the length rules can only die if the examples
have different lengths, and the loose count/block rules can only die if the examples disagree about
those numbers. Same trick as dornic's "exactly *n* cards" competitor.

### Why U is an antichain (why uniqueness is possible at all)
Positive examples can never separate a rule from a **weaker** rule containing it: if A ⊆ B and A is
the truth, B survives too. Brute-forced over all 88 209 strings of length 6–10: **no rule of the
final U contains another** (0 violations). Casualties of that check:

* "exactly **2 blocks**" ⊂ "only two colours are used" (two blocks = two colours). Grid starts at 3.
* "the longest block is **1**" (= *it alternates*) ⊂ "no two red beads touch" and both its siblings,
  and ⊂ "all the blocks are the same size". Cut from the grid — and it becomes an exclusion instead.
* "exactly **0** / **1** red beads" ⊂ "no two red beads touch". Every count grid starts at 2.
* "**no two red beads touch**" itself: dropped from U because it is *dense* (.42–.61 with three
  colours — a rule that half of all strings satisfy is not a rule) — it moved to the exclusions,
  where being dense is exactly what makes it a good trap.
* "**all the red beads are in one clump**" — dense (.44) because a single red bead counts as a
  clump; the tightened version needs an "at least two" clause, which is not one breath. Dropped.
* "**the middle bead is red**", "**it starts with red**" — position rules are excluded on purpose
  (below), and a middle bead only exists at odd lengths, which fights the varying-length format.
* "the total number of beads is even", "**more reds than greens**" — loose comparisons; the class
  only ever makes tight statements, so these are exclusions, not rules.

---

## 3. The exclusions (never in U; frequently consistent with the examples)

Over 500 fresh clues: **fits** = the excluded rule is consistent with *every* example (the trap
fires); **score** = what a player who always answers with an instance of it scores, built at a legal
(unused) length — i.e. the ceiling of that hypothesis for a player who has already found the length
convention. A player who has not found it scores ~0.4× these numbers.

| excluded rule | why a player tries it | fits | score |
|---|---|---|---|
| "no block is longer than the longest block in the clue" | the **loose cousin** of template b | **100 %** | 18.0 % |
| "there are at least *n* C beads" (*n* = the clue's minimum) | the **loose cousin** of template a | **100 %** | 19.8 % |
| "it uses exactly the same set of colours as the examples" | the classic "what do they have in common?" | 54 % | **21.0 %** |
| "no two C beads ever touch" (C = a colour never doubled in the clue) | the most obvious Zendo rule of all | 52 % | 11.6 % |
| "all three colours appear" | ditto | 52 % | 8.8 % |
| "there are more X beads than Y beads" | the loose cousin of template h | 48 % | 11.2 % |
| "it starts with the same colour as every example" | position is the first thing anyone looks at | 22 % | 10.8 % |
| "the two end beads are the same colour" | the loose cousin of the palindrome rule | 19 % | 8.6 % |
| "no two beads the same are next to each other" (it alternates) | the classic bead-string pattern | 8 % | 16.4 % |
| "the same length as the examples" | the laziest hypothesis there is | **0 %** | **0 %** |

The class's secret is a **convention**, not a single rule: it only ever makes **tight** statements
(*exactly n*, the longest block **is** 4, *as many* R as G, reads the same backwards) and never
loose ones (at least, at most, no two touching, contains, starts with). The two 100 %-consistent
traps are the loose cousins of its own templates — a player who answers "anything inside the range
I have seen" is never contradicted by the clue and still scores only ~19 %.

**At least one excluded rule also fits on 100 % of clues (mean 4.6 of them).** So a player whose
universe is U *plus* the obvious extras always faces several survivors; picking a wrong one scores
**16.2 %**. That is the intended failure mode, and the only way out of it is to notice which
*kinds* of statement this class never makes.

Two honest findings about weak traps:
* "the same length as the examples" is not merely never the rule — the well-formedness clause makes
  it **actively wrong** (score 0). It is the cheapest lesson in the class and the first one a player
  learns from feedback.
* "it alternates" fires on only 8 % of clues, because a minimal identifying example set almost
  never consists entirely of alternating strings — a strong "every bead is…" property is a weak
  discriminator, so the generator rarely picks such examples. Same self-excluding effect dornic
  found for "all one suit". Its *score* (16.4 %) is nevertheless one of the higher ones, because
  alternating strings satisfy several eligible rules at once (b:2, g, c-high).

---

## 4. Three demos

```
CLUE                    ANSWER          hidden rule (private)
BRRRGG
RRRRGBBG      ->        RBBRRGGBG       all the red beads come before all the green beads
BRRBGGG

GBBRRRRG
GRRBRBGRB     ->        GRRGGRR         there are exactly 4 red beads
RRBGRR

RGRBRGR
RRBBBBBBRR    ->        GBRBBRBG        it reads the same backwards
BBRRBB
```
(seeds 2, 18, 24. Note every clue shows three different lengths and every answer a fourth one.)

---

## 5. The design decision that made the class: a fresh length

First build — the answer only had to be well formed and differ from the examples:

| witness (bare scorer, no distance clause) | score |
|---|---|
| the **reversal** of an example | **67.4 %** |
| an example with one bead **taken out** | 62.4 % |
| a **rotation** of an example | 58.2 % |
| an example with one bead **added** | 55.8 % |
| a **shuffle** of an example's beads | 45.2 % |
| copy an example with one bead changed | 31.0 % |
| copy an example with two beads changed | 21.6 % |

Every measurement of a bead string in U is smooth under a small edit, so the demo-less probe "echo a
clue line with a tweak" was cracking the class outright — insight optional (DESIGN_LOOP lever 8).
An intermediate build with a Hamming-distance-≥2 + not-a-rotation + not-a-reversal clause cost
~100 scorer characters, zeroed those five witnesses — and still left "add a bead" 35.8 %, "drop a
bead" 30.0 % and "stretch to a new length" 45.6 %, because those change the length.

The fix that worked is the analogue of dornic's fresh-cards clause: **the examples all have
different lengths and the answer must use a length that is not in the clue.**

* It costs **fewer** characters than the clause it replaced (`any(len(a)==len(e) for e in E)`
  replaces the "not one of the examples" test the scorer had to do anyway).
* It kills copy, one-bead-change, two-bead-change, reversal, rotation and shuffle **in one line** —
  all six are length-preserving.
* It is honest and visible: the clue itself shows three different lengths, so the convention can be
  inferred from the clue, and a demo shows a fourth length.
* It leaves a real foothold that *requires the first insight*: "stretch an example to a length the
  clue does not use" scores 45 %, "add a bead" / "drop a bead" 33 %.
* The floor for a player who has not found the convention is 4.6 % (random string, random length)
  and 11.2 % once they have — a clean, quickly learnable 0/1 signal rather than a wall of zeroes.

---

## 6. Witness table — 500 fresh clues

| witness | score | well-formed |
|---|---|---|
| copy an example verbatim | 0.0 % | 100 % |
| copy an example with one bead changed | 0.0 % | 100 % |
| copy an example with two beads changed | 0.0 % | 100 % |
| the reversal of an example | 0.0 % | 100 % |
| a rotation of an example | 0.0 % | 100 % |
| a shuffle of an example's beads | 0.0 % | 100 % |
| an example with one bead added at the end | 32.6 % | 100 % |
| an example with one bead taken out | 32.6 % | 100 % |
| an example stretched/cut to an unused length | **45.0 %** | 100 % |
| EXCLUDED: no block longer than the clue's longest | 18.0 % | 100 % |
| EXCLUDED: at least *n* C beads | 19.8 % | 100 % |
| EXCLUDED: the same set of colours as the examples | **21.0 %** | 100 % |
| EXCLUDED: no two C beads ever touch | 11.6 % | 100 % |
| EXCLUDED: all three colours appear | 8.8 % | 100 % |
| EXCLUDED: more X beads than Y beads | 11.2 % | 100 % |
| EXCLUDED: starts with the same colour as every example | 10.8 % | 100 % |
| EXCLUDED: the two end beads are the same colour | 8.6 % | 100 % |
| EXCLUDED: it alternates | 16.4 % | 100 % |
| EXCLUDED: the same length as the examples | 0.0 % | 100 % |
| the densest U-rule, ignoring the examples ("as many red as green") | 12.0 % | 100 % |
| the most-drawn U-template, ignoring the examples ("all reds before all greens") | 11.2 % | 100 % |
| a random well-formed string of an unused length | 11.2 % | 100 % |
| a random well-formed string of any length | 4.6 % | 100 % |
| player who has mapped U perfectly | **100.0 %** | 100 % |
| player who has mapped U minus its 2 rarest templates (blocks, equal-blocks) | 81.8 % | 100 % |
| player whose universe is U + the excluded rules, picking a wrong survivor | 16.2 % | 100 % |
| the true rule (`solve`) | 100.0 % | 100 % |

Notes on the two partial-knowledge rows:
* **U minus two templates**: removing rules can only shrink the survivor set, so this player never
  faces ambiguity — on the ~79 % of clues whose truth is elsewhere they still get exactly one
  survivor and score 1; on the rest they get **zero** survivors and are left guessing (~0.10).
* **Wrong survivor** is the realistic failure: a player whose universe is *larger* than U. Every
  clue leaves them 4.6 extra survivors on average and picking one scores 16.2 %.

Other measured numbers (500 clues):
* **Example-count distribution**: 2 → 29.8 %, 3 → 70.2 % (4 → 0 %; the generator tries 3 first on
  70 % of draws, 2 first otherwise).
* **Uniqueness** (exactly one U-rule consistent with all examples): 500 / 500.
* **Minimality** (dropping any one example leaves ≥ 2 consistent rules): 500 / 500.
* **All example lengths distinct**: 500 / 500.
* Mean probability of the hidden rule for a random string: **0.105**.

---

## 7. Validation

`python tools/quickcheck.py challenges/lab/tresk.json --seeds 300`
→ `OK tresk  gen=0.31ms score=0.28ms solve=12.26ms`, no warnings.

| quantity | value | cap |
|---|---|---|
| `score` source | **761 chars** | 1024 (RULE_FAMILIES §4 raise; picture classes still aim ≤ 512) |
| `generate` source | 4864 | 50 000 |
| `solve` source | 1249 | 5 000 |
| `generate` | 0.046 ms mean, 0.59 ms max over 5000 seeds | 100 ms |
| `score` | 0.31 ms max (incl. junk: `""`, `"1"*100`, `"R"*4000`, the clue itself) | 50 ms |
| `solve` | 12.3 ms max | 2 000 ms |
| clue | ≤ 29 chars | 1024 |
| answer | ≤ 10 chars | 1024 |

`generate` is fast because the 14 916-string pool (all strings of length 6–7, 4000 sampled at each
of 8, 9, 10) and each string's 38-bit "which rules do I satisfy" mask are built **at module level**
(192 ms, once per worker, not charged to `max_generate_ms`); a call is then a handful of integer
ANDs. `solve` re-derives the survivor exactly as the scorer does and rejection-samples a **uniformly
random** valid string at a random unused length — never the canonical or minimal witness.

---

## 8. Predicted classification

**Testing, leaning slightly hard.** Prediction for two Opus players in a 7-class pool (4 rounds,
~60 probes per class per round, 3 demos for 7 classes):

* **Without a demo**: the clue's shape is self-evident (send another line of beads), so attempts are
  well formed from round 1, but the length convention costs them: a random legal-looking answer
  scores 4.6 %, rising to 11 % once they notice from feedback that repeating a clue length never
  scores. Expect **5–15 %**.
* **With a demo**: the demo answer is a fourth length, which teaches the convention in one look, and
  from there the cheap "stretch an example to a new length" probe pays 45 %. Cracking it outright
  needs the player to reconstruct enough of U to filter — 8 templates, 38 rules — from ~120 probes
  and two or three example strings. Expect **35–60 %**.

Mean across the two ≈ **0.25–0.4**, i.e. `testing` / low `calibrated`, with the risk on the *hard*
side. Levers if it comes back too hard: (i) always emit 3 examples instead of 70 % (more
information, same minimality), (ii) raise the eligibility ceiling from 0.20 to 0.25, which puts
"exactly 3 reds" and "5 blocks" back in play and lifts the random floor from 0.105 to ~0.14,
(iii) drop the fresh-length clause back to Hamming-≥2 + no-rotation, which restores the 30–55 %
copy-edit foothold at the cost of making insight optional. If it comes back too easy: cut the
`n = 4` parameters from the count and block templates (ceiling 0.20 → 0.15).

**12-year-old test**: the object is a bead necklace — a kid says "beads!" from one look at the clue,
no demo needed. Every rule is one breath ("there are exactly four red beads", "it reads the same
backwards", "all the red ones come before all the green ones", "the blocks are all the same size").
A kid can contribute hypotheses and test them by hand on three short strings, and the *lesson* of
the class — "they never say *at least*, they always say *exactly*" — is the kind of thing a kid
notices before an adult does. The nameable-pattern risk is real (these are all nameable rules), but
the difficulty lives in the size of U, the loose-cousin traps, and the thin 0/1 channel, not in any
single rule being obscure.

---

# v2 — 2026-09-05 — the LINEUP answer (RULE_FAMILIES.md revision 2)

`challenges/lab/tresk.json` is now the lineup build; the shipped v1 is kept byte-identical as
`challenges/lab/tresk.v1.json`. Not committed; no arena run (out of scope for this job).

## 9. Why v1 had to change

In `sim/results/lad-dornic-v1-1`, team **dornic1b** scored **97 %** on tresk and team dornic1a
**47 %**, both with **no demo** and without ever naming a rule. Their method (`strategy.py` +
`zpools.tresk_preds`): build a pool of **249 generic bead predicates** (counts per colour and
their parities/majorities/thirds, longest block overall and per colour, block counts, `noadj`,
`pal`, substring `XY` present/absent, all-X-before-Y, first/last bead, length, run-shape…), keep
every predicate true of **every** example, then emit a fresh string satisfying **all** of them at
once. The hidden rule is somewhere in the pool, so the answer satisfies it *by construction*. The
23 eligible rules of U and the 10 excluded traps were both irrelevant: satisfying an extra rule
costs nothing. The only thing that held them for a round was the fresh-length clause
(`1/12 → 10/12` once they found it) — and that clause is not part of the rule, which is exactly
what players called unfair.

**The fix (revision 2): the answer is a choice, not a construction.**

## 10. The v2 format

```
BRBBBRGB            <- 2 or 3 examples, one per line, all of DIFFERENT lengths
BRBRBBRBG
BRBBBGG
                    <- one blank line
GGBGGRGBG           <- 4 candidates, one per line, ALL OF THE SAME length
GGGRBBBGG
RBGGGBBGG
GGBGGRBGG
```

The answer is the one candidate that obeys the hidden rule — written back verbatim
(whitespace- and case-insensitive) **or as its 1-based index `1`–`4`**. A string that is not in
the lineup scores **0**, which is what kills the construction attack.

* **U is unchanged** (8 templates, 38 rules, 23 eligible, antichain, the 15 loose competitors
  still there) — so §2's table, the density figures and the antichain argument all still hold.
  The examples still have distinct lengths, because that is the only way the five length rules of
  U can die; but that is now purely a generator invariant, **not** a scorer clause.
* **The unused-length clause is gone** (revision 2 §5). Nothing about the answer has to be
  "fresh" any more: the lineup does that work.
* **The floor is 1/4 = 25 %** (was 4.6 %), the ceiling for a player who has mapped U is still
  100 %, and the whole 30-point spread that used to come from *guessing a legal string* is gone.

### How the decoys are built

Each decoy has the same length as the true candidate, is not an example, breaks the rule, and
fires at least one excluded rule that is consistent with the examples (revision 2 §2–3). Two
extra invariants do the real work:

1. **Same trap profile.** The generator groups sampled rule-breaking strings by *which* of the
   example-consistent excluded rules they satisfy, and then picks the true candidate from the
   rule's satisfiers **inside the same group**. All four lines therefore satisfy exactly the same
   excluded rules, so every trap — and any count of traps — is worth exactly 25 %.
   *Deviation from revision 2 §2, deliberately:* the doc suggests decoys that satisfy traps the
   true candidate fails. That makes "the candidate satisfying the fewest excluded rules" a free
   crack; matching the profile instead makes the traps exactly neutral, which is stronger.
2. **Balanced outside-predicate count.** `generate` rebuilds dornic1b's 249-predicate pool
   bit-for-bit (grouped by what each predicate reads off the string and memoised on that key, so
   a string costs five dict lookups and ~4 µs), intersects it over the examples (mean **35.8**
   surviving predicates), and then chooses the true candidate so that its **rank** among the four
   on that count is spread over all four places — realised rank distribution
   **213 / 110 / 86 / 91** over 500 clues. "Answer with the thing that satisfies most of my
   predicates" therefore scores **39 %**, not 97 %, and its inverse scores **20.8 %**.

## 11. Three demos

```
CLUE                         ANSWER              hidden rule (private)

BRBBBRGB
BRBRBBRBG
BRBBBGG
                       ->    RBGGGBBGG (3)       all the red beads come before all the green
GGBGGRGBG
GGGRBBBGG
RBGGGBBGG
GGBGGRBGG

RRBRGRG
BRRRGGBR
BRGGGRRRG
                       ->    GBGRBRRBR (3)       there are exactly 4 red beads
GRGBRRRBR
BRRGGRRGR
GBGRBRRBR
RGRRGBRRR

RGBBGR
BRRRBBRRRB
RBRBBRBR
                       ->    BRRGRRB (2)         it reads the same backwards
RBRRBBR
BRRGRRB
BRRBRGB
RRRGBBR
```
(seeds 2, 18, 24 — the same seeds as v1's demos.) Note in demo 3 that the three decoys are
*near*-palindromes: they share the examples' colour set, their block-length profile and their
trap profile, and two of them satisfy more of the 249-predicate pool than the answer does.

## 12. Witness table — 500 fresh clues

| witness | score |
|---|---|
| pick candidate 1 | 25.8 % |
| pick a random candidate | 25.0 % |
| **the candidate satisfying the most example-consistent predicates of the 249-strong outside pool** | **39.0 %** |
| the same, but requiring *all* of them (the exact v1 attack), falling back to the most | 39.0 % |
| the candidate satisfying the FEWEST such predicates (the inverse heuristic) | 20.8 % |
| the candidate closest to the other three by Hamming distance (medoid) | 25.2 % |
| the candidate furthest from the other three (outlier) | 25.1 % |
| **the in-U intersection — a player who knows U** | **100.0 %** |
| EXCLUDED: no block longer than the clue's longest (fits 100 %) | 25.0 % |
| EXCLUDED: at least *n* R / G / B beads, the clue's minimum (fits 100 %) | 25.0 % |
| EXCLUDED: exactly the clue's set of colours (fits 51 %) | 25.0 % |
| EXCLUDED: all three colours appear (fits 49 %) | 25.0 % |
| EXCLUDED: no two R / G / B beads ever touch (fits 24–27 %) | 25.0 % |
| EXCLUDED: more X beads than Y, 6 pairs (fits 9–14 %) | 25.0 % |
| EXCLUDED: starts with / ends with the clue's colour (fits 19 % / 22 %) | 25.0 % |
| EXCLUDED: the two end beads are the same colour (fits 16 %) | 25.0 % |
| EXCLUDED: it alternates (fits 9 %) | 25.0 % |
| a player whose universe is U + the excluded rules, committing to a random survivor | 34.8 % |
| a player who knows U minus its two rarest templates (blocks, equal-blocks) | 80.7 % |
| the true rule (`solve`) | 100.0 % |
| the true rule, answered by INDEX rather than verbatim | 100.0 % |

All nineteen excluded-rule rows are **exactly** 25.0 %: by construction the true candidate and its
three decoys satisfy the same excluded rules, so committing to a trap tells a player nothing at
all. That is the whole difference from v1, where those rows paid 8.6–21.0 %.

Other measured numbers (500 clues): uniqueness 500/500, minimality 500/500, all example lengths
distinct 500/500, all four candidates the same length 500/500, four distinct candidates 500/500,
no candidate equal to an example 500/500, exactly one candidate obeying the rule 500/500, every
decoy firing ≥1 consistent trap 500/500. Examples per clue 2 → 34 %, 3 → 66 %. Candidate length
6/7/8/9/10 → 86/88/100/112/114. True-candidate position 129/125/124/122. Template mix (500):
blocks 72, maxrun 69, twocol 66, before 64, equal 63, palin 60, eqblk 57, count 49. Mean 7.15
excluded rules are consistent with any one clue (min 4, max 12).

## 13. Validation

`python tools/quickcheck.py challenges/lab/tresk.json --seeds 300`
→ `OK tresk  gen=2.49ms score=0.29ms solve=0.28ms`, no warnings.

| quantity | value | cap |
|---|---|---|
| `score` source | **805 chars** (v1: 761) | 1024 (RULE_FAMILIES §4 raise) |
| `generate` source | 14 300 | 50 000 |
| `solve` source | 1 100 | 5 000 |
| `generate` | **0.645 ms mean**, 2.97 ms max over 5000 seeds | 100 ms |
| `score` | 0.29 ms max (incl. junk: `""`, `"0"`, `"9"`, `"1"*100`, `"R"*4000`, the clue itself) | 50 ms |
| `solve` | 0.28 ms max (v1: 12.3 ms — nothing to rejection-sample any more) | 2 000 ms |
| clue | ≤ 74 chars (v1: 29) | 1024 |
| answer | ≤ 10 chars | 1024 |

`generate` is ~14× slower than v1's 0.047 ms because a call now samples ~150 rule-breaking and
~60 rule-keeping strings and scores each against the outside pool; it is still 150× inside the
cap. Module-level tables cost **≈ 340 ms** per worker (v1: 192 ms): the 14 916-string pool, its
38-bit U mask, its 249-bit outside-pool mask and its trap features. Not charged to
`max_generate_ms`. `score` no longer needs the freshness test, and the 44 characters it saves pay
for splitting the clue on the blank line and resolving an index.

## 14. Predicted classification

**Calibrated, leaning easy-for-a-good-player, and much flatter than v1.**

* **Without a demo**: the clue shape (3 lines, a gap, 4 lines) reads as a multiple choice, but a
  player who has not worked that out will answer with a constructed string and score **0** until
  the feedback teaches them. Expect a round of near-zero, then **25 %**.
* **With a demo**: the demo shows one of the four lines echoed back, so the format costs one
  look. From there every cheap statistic is worth exactly 25 % — traps, predicate counts, medoid,
  position — and the only way up is to reconstruct U. A player who gets 6 of the 8 templates
  scores **81 %**; a player who has all 8 scores **100 %**. That is a steep, honest cliff: the
  expected score is 25 % + 75 % × P(the clue's template is one they have mapped).
* Mean across two Opus teams ≈ **0.35–0.6**, i.e. `calibrated`. The 97 % v1 result should drop to
  ≈ 39 % for the same unchanged strategy, and the 4.6 % floor rises to 25 %.

Levers if it comes back **too easy**: (i) k = 5 or 6 candidates (floor 20 % / 17 %); (ii) put two
rule-satisfying candidates in and ask for both — no, that breaks the one-line answer; better
(iii) grow U with a ninth template so "I have mapped U" costs more probes. Too **hard**: drop to
k = 3 (floor 33 %), or emit 3 examples always instead of 66 % of the time.

**12-year-old test**: unchanged and arguably better. The clue is still a bead necklace, and the
task is now the one every kid knows from a puzzle book — *which of these four fits?* A kid can
check four short strings against a hypothesis by hand in seconds, and the 0/1 signal is now about
the rule rather than about an invisible novelty convention. The one loss: the v1 lesson
("they never say *at least*") no longer pays on its own, because the traps have been made
exactly neutral; the game is now purely "which rules does this class use".
