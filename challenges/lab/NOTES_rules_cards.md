# NOTES — rule-family class, world = a hand of 4–6 playing cards (`dornic`)

Paradigm: `docs/RULE_FAMILIES.md`. A finite universe **U** of parametrised rules; the clue is a
minimal set of positive example hands that pins one rule inside U; the answer is one more hand
satisfying it. The player does **not** know U, so their larger hypothesis space contains obvious
rules the class never uses. Learning *what the class never asks* is the game.

Shipped file: `challenges/lab/dornic.json`. Name chosen neutral/random (checked unique against
`challenges/` and `challenges/lab/`).

---

## 1. The world

A hand is one line: 4–6 distinct cards separated by spaces, e.g. `3H 5D 5S 9C JH`.
Rank tokens `A 2 3 4 5 6 7 8 9 10 J Q K`, suit tokens `H D C S`.
**Values are never stated**: A=1 … 10=10, J=11, Q=12, K=13. Inferring that convention is a
deliberate second layer — half of U (all the counting rules) works without it.

Every clue line is written **sorted by value**. That is a legibility choice (levers 9: salience —
the counted relation must be the loudest thing in the picture) and it doubles as the strongest
exclusion: order is *always* consistent and *never* the rule.

**Fresh-cards clause.** All clue hands are pairwise card-disjoint and the answer must share no
card with any of them — every hand is dealt from one deck. This is a well-formedness rule, not a
hidden clause, and it is the single most important design decision here (see §5).

---

## 2. The universe U — 17 templates, 91 rules

The scorer computes a 16-number readout of a hand and every rule is one predicate on one number.
"rate" = fraction of uniformly random well-formed hands satisfying that parameter.
"R?" = may be the hidden rule (rules outside a 2 %–32 % random-hand rate stay in U as **competitors**
but are never the answer to find).

| # | template (kid sentence) | params | rate per param | R? | weight |
|---|---|---|---|---|---|
| 1 | "there are exactly *n* hearts / diamonds / clubs / spades" | n = 0,1,2,3 (×4 suits) | .23 / .41 / .27 / .08 | 0,2,3 | 2.4 |
| 2 | "there are exactly *n* red cards" | 1–4 | .16 / .33 / .30 / .15 | 1,3,4 | 1.0 |
| 3 | "there are exactly *n* even cards" | 1–4 | .20 / .33 / .28 / .11 | 1,3,4 | 1.0 |
| 4 | "there are exactly *n* picture cards" | 1–3 | .42 / .25 / .07 | 2,3 | 1.4 |
| 5 | "there are exactly *n* different suits" | 2–3 | .17 / .56 | 2 | 0.6 |
| 6 | "there are exactly *n* cards" | 4–6 | .33 each | — (competitor only) | 0.8 |
| 7 | "the highest card is *n*" | 8–13 | .04 → .34 | 8–12 | 1.4 |
| 8 | "the lowest card is *n*" | 1–5 | .34 → .07 | 2–5 | 1.4 |
| 9 | "the highest minus the lowest is *n*" | 5–12 | .05 → .16 | all | 1.6 |
| 10 | "there is exactly one pair" | — | .40 | — (competitor only) | 0.6 |
| 11 | "the cards add up to exactly *n*" | 20–40 | .013 → .041 | 23–40 | 1.8 |
| 12 | "the cards add up to a prime number" | — | .25 | yes | 0.7 |
| 13 | "the cards add up to a multiple of *y*" | y = 3–7 | .33 → .14 | 4–7 | 1.2 |
| 14 | "the red cards add up to a prime number" | — | .31 | yes | 0.5 |
| 15 | "the red cards add up to a multiple of *y*" | y = 3–7 | .35 → .16 | 4–7 | 0.9 |
| 16 | "the black cards add up to a prime number" | — | .31 | yes | 0.5 |
| 17 | "the black cards add up to a multiple of *y*" | y = 3–7 | .35 → .16 | 4–7 | 0.9 |

|U| = 91. 15 of the 17 templates can be the hidden rule. Within a template a parameter is drawn
with weight ∝ 1/√rate, so tight rules dominate and the mean hit-rate of the hidden rule on a random
hand is **0.18** (it was 0.245 with flat weights; the floor a thoughtless player gets is the thing
that number controls).

**Why keep two templates that can never be the answer.** "there are exactly *n* cards" and
"there is exactly one pair" are loose (rate .33 / .40) so they would hand a demo-less player a
free 33 %. But leaving them *in U* means the generator must kill them off, which forces every clue
to contain **hands of at least two different sizes** and usually a mix of paired/unpaired hands.
The competitor set is doing layout work for free.

**Structural exclusions that fell out of U's shape.** `total = n` is only ever pinnable for n whose
value is not also prime and not a multiple of 3–7, because those rules would survive too. Likewise
`highest − lowest = 12` can never be unique (it entails `lowest = 1` and `highest = 13`). The
generator does not special-case these; they simply never achieve uniqueness and are re-drawn.

---

## 3. Excluded templates (the traps)

Never in U. The generator prefers example sets that *are* consistent with them (it scores up to 10
candidate sets by how many traps survive), so they are the hypotheses a first-time player will
reach for. Trap rate = the template fits **every** example of a clue (measured over 500 clues).

| excluded template | kid sentence | trap rate | why excluded |
|---|---|---|---|
| order | "the cards are in increasing order" | **100 %** | every clue line is sorted; nothing about order or position is ever the rule |
| ranks | "no two cards share a number" | **39 %** | the single most obvious card-hand rule; `exactly one pair` sits in U instead |
| high card | "the highest card is red" | **40 %** | "colour of a particular card" is never a rule; only counts and sums are |
| balance | "more red cards than black" | 17 % | U only ever asks for an exact count, never a comparison |
| pictures | "there are no picture cards" | 11 % | `picture cards = 0` is deliberately cut from template 4's grid |
| runs | "no two cards next to each other in value" | 4 % | adjacency/sequence is never measured |
| floor | "nothing below a 5" | 4 % | U has `lowest = n`, never `lowest ≥ n` |
| colour | "all one colour" | 1 % | `red cards = 0` and `= 5,6` are cut from template 2's grid |
| suit | "all one suit" | 0 % | `different suits = 1` is cut from template 5's grid |

The last three are near-unreachable and that is a finding worth recording: an *"every card shares
property P"* clue pins some U-feature to a constant (all-red hands force `clubs = 0`, `spades = 0`,
`black total = 0`), which destroys uniqueness. **Strong "all the cards are…" traps are largely
self-excluding in this paradigm.** So the load-bearing traps are the three at 39–100 %, and the
useful lesson for the player is narrower and sharper than "there are no all-X rules": it is
*"this class only ever counts or adds; it never compares, never orders, never looks at where a
card sits."*

---

## 4. Three demos

```
CLUE                                   ANSWER              hidden rule (private)
4S 5D 6S 10S JS KS
AS 3C 7H 10D            ->  6C 7S 10C QH          the cards add up to a multiple of 7
3S 5H 7C 9H QD KD

2S 6S 7C 8C
AD 3S 4H 4S 5H 7D       ->  3D 5C 10D JH QS KS    there are exactly 2 spades
AC AS 2H 10S

2H 3H 4C 5S 8D
AD 5D 6S 7S 10H 10D     ->  AS 5C 6D 8S QS        there are exactly 3 even cards
```
(the third demo also shows the value convention biting: Q counts as an even card, 12.)

---

## 5. The design decision that made the class: fresh cards

First build, before the disjointness clause:

| witness | score |
|---|---|
| copy an example, one card changed | **52.6 %** |
| random hand | 28.2 % |

A demo-less player's most natural probe — echo a clue line with one card swapped — was cracking the
class outright, because count/extremum rules are robust to a one-card edit (~55 %). Insight was
optional (DESIGN_LOOP lever 8). Two fixes were applied together:

1. **The answer may not reuse any card from the clue** (and the clue's own hands are pairwise
   disjoint, so the story is honest: one deck, deal another hand). Cost in the scorer: **zero
   characters** — the same set-intersection test replaces the "answer is not one of the examples"
   test it had to do anyway. Copy-with-one-change now scores 0 %.
2. **Rules re-weighted toward tight parameters** and rules looser than 32 % barred from being the
   answer. Mean hidden-rule hit-rate 0.245 → 0.18.

Result: the cheap probes now land in the 10–27 % foothold band the loop asks for, while a player who
actually maps U scores 100 %.

---

## 6. Witness table — 500 fresh clues

| witness | score | well-formed |
|---|---|---|
| copy an example verbatim | 0.0 % | 100 % |
| copy an example, one card changed | 0.0 % | 100 % |
| EXCLUDED: no two cards share a number | 14.2 % | 100 % |
| EXCLUDED: written in increasing order | 16.4 % | 100 % |
| EXCLUDED: the highest card is red | 12.8 % | 100 % |
| EXCLUDED: more red cards than black | 17.4 % | 100 % |
| EXCLUDED: no picture cards | 15.0 % | 100 % |
| EXCLUDED: no two cards next to each other in value | 12.4 % | 100 % |
| EXCLUDED: nothing below a 5 | 15.4 % | 100 % |
| EXCLUDED: all one colour | **26.8 %** | 100 % |
| EXCLUDED: all one suit | 9.8 % | 51.6 % (a 5–6 card flush from the free cards is often unbuildable) |
| most common U-rule, ignoring the examples | 19.6 % | 100 % |
| random well-formed hand (fresh cards) | 11.0 % | 100 % |
| random well-formed hand (any cards) | 3.0 % | 100 % |
| player who has mapped U perfectly | **100.0 %** | 100 % |
| player who has mapped U minus its 2 rarest templates | 95.4 % | 100 % |
| player who knows U but picks a wrong survivor | 15.4 % | 100 % |
| the true rule (`solve`) | 100.0 % | 100 % |

Notes on the two "partial knowledge" rows:

* **U minus the 2 rarest templates** (`red total is prime` 3.4 %, `total = n` 1.8 %): removing
  templates can only *shrink* the survivor set, so this player never faces ambiguity — on 94.8 % of
  clues they still get exactly one survivor and score 1, and on the other 5.2 % they get **zero**
  survivors and are left guessing. 95.4 %.
* **Wrong survivor** is therefore defined the other way round, which is how it actually happens: a
  player whose universe is *larger* than U (U plus the excluded templates). Whenever an excluded
  template also fits every example — 100 % of clues for "increasing order", 39–40 % for the two
  strong ones — they have several survivors, and picking a wrong one scores **15.4 %**. A player who
  knows U but drops one example from the filter and takes a wrong near-survivor scores 15.2 %.

Other measured numbers:

* **Example-count distribution**: 2 → 14.4 %, 3 → 81.6 %, 4 → 4.0 %, 5 → 0 %.
* **Uniqueness** (exactly one U-rule consistent with all examples): 500 / 500.
* **Minimality** (dropping any one example leaves ≥ 2 consistent rules): 500 / 500.
* **Examples pairwise card-disjoint**: 500 / 500.
* Mean hit-rate of the hidden rule on a random hand: **0.179**.
* Hidden-rule template mix: suit count 16.4 %, spread 13.4 %, red count 10.8 %, highest 7.8 %,
  different suits 7.0 %, even count 6.8 %, black-total multiple 6.0 %, total multiple 5.2 %,
  lowest 5.0 %, red-total multiple 4.8 %, black-total prime 4.4 %, pictures 3.8 %, total prime
  3.4 %, red-total prime 3.4 %, total = n 1.8 %.

---

## 7. Validation

`python tools/quickcheck.py challenges/lab/dornic.json --seeds 300 --cap max_score_code_chars=1024`
→ `OK dornic  gen=1.01ms score=0.69ms solve=22.39ms`, no warnings.

| quantity | value | cap |
|---|---|---|
| `score` source | **1016 chars** | 512 default; **1024** requested (permitted for this paradigm, RULE_FAMILIES §4) |
| `generate` source | 5058 | 50 000 |
| `solve` source | 1685 | 5 000 |
| `generate` | 0.20 ms mean, 1.01 ms max | 100 ms |
| `score` | 0.69 ms max (incl. junk) | 50 ms |
| `solve` | 22.4 ms max | 2 000 ms |
| clue | ≤ 100 chars | 1024 |
| answer | ≤ 20 chars | 1024 |

`generate` is fast because the 9000-hand sample pool and each hand's 91-bit "which rules do I
satisfy" mask are built **at module level** (≈ 220 ms, once per worker, not charged to
`max_generate_ms`); a call is then a handful of integer ANDs.

---

## 8. Predicted classification

**On target / testing, leaning slightly easy.** Prediction for two Opus players in a 7-class pool:

* Without a demo: the clue's shape is self-evident (send another line of cards), so attempts are
  well formed from round 1. Sensible-but-wrong hypotheses and random fresh hands score **11–27 %**.
  Expect 15–25 %.
* With a demo: one solved example shows a fresh-card hand and confirms "another hand of the same
  sort", but not the rule; the player still has to find which of ~91 measurements the examples pin.
  With ~60 probes per round for 4 rounds they can test a handful of hypotheses per clue but cannot
  brute-force per-clue rule discovery, so I expect **40–60 %**, not 100 % — the ceiling is only
  reachable by a player who reconstructs U itself and filters, which is the intended crack.

Mean across the two ≈ **0.3–0.45**, i.e. `calibrated`, with the risk being the *easy* side: the
foothold floor (11 %) plus the "all one colour" probe (27 %) is a lot of free score. If it comes
back too easy, the first lever is to cut the `= 0` parameter from the suit-count template (which is
what makes a monochrome hand pay) and to lower the eligibility ceiling from 32 % to 25 %. If it
comes back too hard, raise the ceiling and add a fourth example more often.

12-year-old test: the object is a hand of cards (instantly evocable); every rule is one breath
("there are exactly two spades", "the cards add up to a multiple of seven"); the demo shows a hand
that obeys the rule; and a kid can contribute hypotheses ("count the hearts — nope, try the
picture cards"). The nameable-pattern risk is real (these *are* nameable rules), but the difficulty
lives in the size of U and the excluded set, not in any single rule being obscure.

---

# 2026-09-05 — revision 2: the LINEUP answer (`dornic` v2)

v1 is kept byte-identical as `challenges/lab/dornic.v1.json`; the shipped file is
`challenges/lab/dornic.json`. Paradigm change per `docs/RULE_FAMILIES.md` §"Revision 2".

## 9. What changed

| | v1 | v2 |
|---|---|---|
| clue | 2–5 example hands | 2–4 example hands, a blank line, **4 candidate hands** |
| answer | *construct* another hand obeying the rule | **choose** the candidate that obeys it (verbatim or index 1–4) |
| well-formedness | 4–6 distinct cards, **no card from the clue** | none — the answer is a choice; the fresh-cards clause is **gone** |
| floor | ~11 % (a random fresh hand) | 25 % (one of four) |
| U | 17 templates, 91 rules | **unchanged** |
| template weights | prime / colour-sum family 19 % of clues | **42 %** (the one defence that worked; see §11) |
| `score` | 1016 chars | **905** |

**Why.** The round-1 winner (team `dornic1b`, leaderboard rank 1) took no demo and scored **77 %**
on v1 without ever naming a rule: keep every predicate of a 359-strong pool that is true of all
the examples, then emit a hand satisfying all of them at once — the hidden rule is in the pool,
so the answer obeys it by construction. Their own notes are blunt that the *fresh-cards clause*,
not the rule, was the difficulty (`dornic — the answer must use cards not in the clue: 0/10 → 27/33`).
A choice among four kills the construction: the intersection has nothing to intersect.

**Dropping the fresh-cards clause (the brief asked for a decision).** Dropped entirely — candidates
may reuse clue cards or not. The v1 clause existed to close "copy an example, change one card",
which a lineup closes for free (no candidate is an example, checked 500/500). The "copy the
minutes"-style leak the brief warns about is the risk that the *true* candidate is distinguishable
by its relationship to the clue's cards; it is not present, because the truth and the decoys are
drawn from the same 6000-hand pool with the same filters. Measured over 500 clues: the true
candidate shares **no** clue card on 19.4 % of clues, decoys on 18.6 %; the witness "pick the
candidate sharing the most clue cards" scores **26.8 %** and "sharing none" **25.0 %** — both at the
floor. Constraining the overlap would have been a *new* invisible convention, exactly what
revision 2 removes.

## 10. How the lineup is built (revision-2 rules 1–5)

1. **Exactly one candidate obeys the rule** — verified in `generate` on every clue (500/500).
2. Every decoy **fails** the rule and is an instance of at least one **excluded** rule consistent
   with the examples, or else lies inside the clue's total range (the trap that always fits)
   — 500/500.
3. **No shape tell.** All four candidates have the **same number of cards**, are four distinct
   hands, and none is one of the examples (500/500 each). The true candidate's position is
   uniform (127 / 127 / 125 / 121 over 500).
4. **The count defence.** `generate` carries the winner's own pool (`dornic_preds()`, 359
   predicates, verbatim) plus a base rate per predicate measured on its own hand pool. It scores
   every candidate by a **rarity-weighted** count of the pool predicates that survive the examples
   (raw count breaks ties) and aims the **rank** of the true candidate by that score: over up to
   five different minimal example sets and two hand sizes it prefers a lineup where at least one
   decoy out-scores the truth, and takes rank 0 only when the clue cannot support better.
   Decoys are drawn both at random and **targeted** at the tight surviving predicates through a
   per-predicate hand index, so a decoy can carry a rare property that every example shares.
5. Minimality and uniqueness inside U are unchanged from v1 and still verified 500/500. Example
   sets are still ranked by how many **excluded** templates they leave alive.

## 11. The finding: a lineup beats the *count*, only blunts the *rarity-weighted count*

The direct port of the round-1 attack — "pick the candidate satisfying the most surviving
predicates" — is beaten: **31.2 %** (floor 25 %), with at least one decoy strictly out-counting the
truth on **66.2 %** of clues (revision 2 asks ≥ 40 %). "Fewest" scores 23.4 %, so the count is not
reversible either.

But the *smarter* version of the same attack is not beaten. Weight each surviving predicate by
−log(its base rate) — the natural Bayesian reading of "the hidden rule is one of my survivors",
and correct here because the hidden rule is by construction a tight predicate — and the attack
scores **47.2 %**. It started at **74 %** on the first build of v2.

**Why it cannot be pushed to the floor.** On the clues where the hidden rule is itself expressible
in the attacker's pool, it is the rarest thing all the examples share, and *no* hand that fails it
can look as specially chosen. Exhaustive search over the whole 6000-hand pool, over 40 different
minimal example sets per rule and all three hand sizes, says how beatable each template is:

| template | some decoy can out-score the truth on rarity |
|---|---|
| total is prime, red/black total is prime, red/black total is a multiple of *y* | **100 %** (the pool has no colour-sum and no primality predicate) |
| exactly *n* hearts/…/spades, *n* red, *n* even | 25–50 % |
| *n* pictures, *n* different suits, highest = *n*, lowest = *n*, highest−lowest = *n*, total = *n*, total a multiple of *y* | 0–15 % |

Three things were tried:

* **Targeted decoys** (a per-predicate index so a decoy can carry a rare surviving property):
  kept, worth ~1 point on its own.
* **An "anchor"** — force every example to share a *second* tight property drawn from the
  attacker's pool but absent from U, so the clue carries two coincidences and a decoy can carry
  the wrong one. **Measured and discarded**: anchored example sets almost never pin a unique rule
  of U any more (**10 usable sets out of 310 attempts**), because the pool's tight predicates are
  U's own readouts (`maxr=k`, `cntS=k`, `span=k`…), so anchoring one keeps another U rule alive.
* **Re-weighting the templates toward the two-step readouts** (filter by colour, add up, test for
  prime or for a multiple): prime/colour-sum rules go from 19 % to 42 % of clues, and the
  rarity attack falls **61 % → 47.2 %**. Kept. This is the one lever that worked, and it is a
  genuine difficulty dial rather than an over-fit to one player's pool: a rule over a *derived*
  quantity is harder for any predicate pool to enumerate than a rule over a directly visible
  count. The cost is legibility — half the clues are now "the black cards add up to a multiple of
  five" rather than "there are exactly two spades". Halving the shift costs about 8 points.

**This is expected to apply to `wisbek` and `tresk` too** — both were tuned against the *unweighted*
count only, and neither measured the rarity-weighted witness. Worth re-measuring there before the
next arena; if it reproduces, the general lesson for revision 2 is that a lineup is only as strong
as the gap between U and the attacker's *prior*, not the gap between U and their *hypothesis space*.

## 12. Three demos

```
CLUE                          LINEUP                   ANSWER          hidden rule (private)

4S 7H 8C 9D JH QC             AC 8C 9S QH
5D 7C QH KC                   2H 3H JD QH          ->  2H 3H JD QH     there are exactly
4D 10S JD KD                  6D JS QC KS              (index 2)       2 picture cards
                              AD 6S 9C JD
------------------------------------------------------------------------------------------
5H 6S 7C KH                   5H 10C JH JD QD
AH AD AS 3D 9H                7D 9D 10S JD KD      ->  2H 9H 9C 10H    the highest minus
4S 9S 10H JC QD               2H 9H 9C 10H 10C         10C (index 3)   the lowest is 8
                              2H 6H JD QS KD
------------------------------------------------------------------------------------------
AS 6S 9H 10D 10C              AD 7S 9H 10S
AC 3H 9C JC                   AD 6S 9C JD          ->  7H 7S 8C JS     the red cards add up
4H 6H 8H KD                   7H 7S 8C JS              (index 3)       to a prime number
                              2D 6S 8H 10C
```
(seeds 4, 11, 26; answers straight from `solve`. Note the second lineup: every candidate has five
cards, three of them keep the clue's "the highest card is red", and `5H 10C JH JD QD` carries the
pair trap — only the span of 8 separates the true one. Note the third: the value convention bites,
`7H` alone is a prime red total of 7, while `AD 7S 9H 10S` has red total 1+9 = 10.)

## 13. Witness table — 500 fresh clues (seeds 1 000 000 – 1 000 499)

The answer is a choice among four, so the floor is **25 %** and there is no well-formedness column.

| witness | score |
|---|---|
| **the true rule (`solve`)** | **100.0 %** |
| **the in-U intersection** (the candidate satisfying every rule of U the examples allow) | **100.0 %** |
| a player who knows U minus its 2 rarest templates (`total = n`, `n different suits`) | 97.2 % |
| universe = U + the excluded templates, pick one surviving hypothesis uniformly | 67.4 % |
| **MOST surviving pool predicates, weighted by rarity (−log base rate)** | **47.2 %** |
| … the same, scored by the generator's own weighting (diagnostic) | 47.0 % |
| **MOST surviving pool predicates (the round-1 attack, 359 preds)** | **31.2 %** |
| the candidate satisfying the FEWEST example-consistent excluded traps | 30.8 % |
| EXCLUDED: all one colour (fits 0.0 % of clues) | 30.4 % |
| the candidate with the biggest total | 28.6 % |
| EXCLUDED: no picture cards (fits 8.8 %) | 27.8 % |
| the candidate sharing the MOST cards with the clue | 26.8 % |
| **pick a random candidate (the floor)** | **26.4 %** |
| EXCLUDED: more red cards than black (fits 11.4 %) | 25.8 % |
| **pick candidate 1** | **25.4 %** |
| EXCLUDED: nothing below a 5 (fits 4.2 %) | 25.2 % |
| the candidate sharing NO card with the clue | 25.0 % |
| EXCLUDED: all one suit (fits 0.0 %) | 25.0 % |
| the most common U-rule ignoring the examples (`1 heart`) | 24.2 % |
| the candidate whose total is nearest an example total | 23.4 % |
| the candidate satisfying the FEWEST surviving pool predicates | 23.4 % |
| the candidate satisfying the MOST example-consistent excluded traps | 23.2 % |
| EXCLUDED: the highest card is red (fits 39.6 %) | 22.6 % |
| EXCLUDED: no two cards next to each other in value (fits 5.0 %) | 22.6 % |
| EXCLUDED: no two cards share a number (fits 31.0 %) | 22.2 % |

True-candidate rank by pool-predicate count over the 500 clues: **169 / 119 / 103 / 109**
(rank 0 = the truth is the sole top scorer; it is the residue of clues where the rule is
unbeatable on rarity, and it is where the counting attack is still worth something).

Other measured numbers:

* uniqueness 500/500, minimality 500/500, exactly one candidate obeys the rule 500/500;
* same hand size 500/500; no candidate equal to an example 500/500; four distinct candidates
  500/500; examples pairwise card-disjoint 500/500;
* every decoy an instance of a consistent excluded rule or inside the clue's total range 500/500;
* example counts (2000 seeds): 2 → 13.5 %, 3 → 81.9 %, 4 → 4.6 % (v1: 14 / 82 / 4);
* mean hit-rate of the hidden rule on a random hand **0.199** (v1: 0.179);
* hidden-rule template mix over 500: suit count 57, black-total multiple 47, red-total multiple 44,
  total prime 43, black-total prime 43, span 43, lowest 41, red-total prime 35, highest 32,
  total multiple 28, red count 25, even count 25, pictures 16, different suits 13, total = n 8.

## 14. Validation

`python tools/quickcheck.py challenges/lab/dornic.json --seeds 300` →
`OK dornic  gen=2.07ms score=0.16ms solve=0.19ms`, **no warnings** (the 1024 scorer cap is now
the quickcheck default, so no `--cap` override is needed).

| quantity | value | cap |
|---|---|---|
| `score` source | **905 chars** (v1: 1016) | 1024 (the rule-family raise) |
| `generate` source | 17 611 | 50 000 |
| `solve` source | 1 256 | 5 000 |
| `generate` | **0.65 ms mean**, 3.2 ms max over 2000 seeds | 100 ms |
| `score` | 0.18 ms | 50 ms |
| `solve` | 0.09 ms mean, 0.17 ms max | 2 000 ms |
| clue | ≤ 138 chars | 1024 |
| answer | ≤ 19 chars | 1024 |

The 6000-hand pool with its 91-bit U mask, 8-bit trap mask and 359-bit attacker-pool mask costs
**≈ 2.5 s once per worker** at module level and is not charged to `max_generate_ms`; that is 10×
v1's 220 ms and is the price of scoring every hand against the attacker's 359 predicates. A call
is then a handful of integer ANDs, `bit_count`s and two `bisect`s.

`score` was checked on 500 clues × every candidate (exactly one scores 1 each time, 500/500) and
rejects `''`, `x`, `0`, `5`, `9`, `1 2`, `1`×100, the clue, the example block alone, a unicode
digit, a malformed hand, a well-formed hand not in the lineup, and a candidate with a card added
or removed. It forgives surrounding and internal whitespace and accepts a 1-based index.
`solve` re-derives the survivor exactly as the scorer does and returns the true candidate verbatim.

## 15. Predicted classification

**Calibrated, and materially harder than v1** (which was measured at 77 % — too easy).
Two Opus players, 7-class pool, 4 rounds:

* **Without a demo**: the shape is self-evident (hands, a gap, four hands, pick one), so every
  probe is well formed from round 1 and the floor is a free **25 %**. The round-1 method degrades
  to counting surviving predicates: **31 %**. A team that thinks to weight its predicates by
  rarity — and this team already computed base rates in round 1 — reaches **47 %**. Expect
  **30–50 %**.
* **With a demo**: a demo now teaches nothing about a *convention* (there is none left) — only the
  format. The way up is to reconstruct U, and the moment a player filters U correctly they score
  **100 %**, because the in-U intersection is exact. 91 rules over 17 templates from 2–4 example
  hands is a lot, and the prime / colour-sum half of the class is the part nobody enumerates by
  default. Expect **40–65 %**.

Mean across the two ≈ **0.35–0.55** → `calibrated`, with the risk on the **easy** side and named:
the rarity-weighted attack at 47 % is a free half-mark for a thoughtful team. Levers if it comes
back too easy: (i) push the two-step templates further (60 % of clues would put the rarity attack
near 40 %, at a real cost in kid-legibility); (ii) add colour-sum *parity* and "the picture cards
add up to…" templates to U — more of the class outside any natural pool. Too hard: (iii) go to
k = 3 candidates (floor 33 %); (iv) let one decoy instantiate a rule of U that all but one example
allows, so a partly-mapped player is rewarded rather than punished.

**12-year-old test**: the object is still a hand of cards; every rule is still one breath ("there
are exactly two picture cards", "the red cards add up to a prime number"); and "which of these four
fits?" is an easier question to ask a child than "make me another one" — the four candidates are
themselves a hint about what kind of thing the rule can be. The cost of the re-weighting is that
more clues now need mental arithmetic over a colour-filtered subset; that is the class's hardest
edge and it is where a kid needs the grown-up.

---

# 2026-09-05 — revision 3: a universe of RELATIONS (`dornic` v3)

v2 is kept byte-identical as `challenges/lab/dornic.v2.json`; the shipped file is
`challenges/lab/dornic.json`. Paradigm step per `docs/RULE_FAMILIES.md` §"Revision 3" — the nine
steps of the recipe, in order.

## 16. What the three lineup arenas and the judge showed

v2 met four Opus centaurs in three pools and finished **on target for the wrong reason**:

| run | players | dornic v2 | demo? |
|---|---|---|---|
| `lad-tresk-v2-1` | opus-lowdemo / opus-theorist | 66 % / 59 % | no |
| `lad-ospren-v2-1` | opus-default / opus-kidproxy | 66 % / 63 % | yes (1 each) |
| `lad-tavrik-v3-1` | opus-lowdemo / opus-theorist | 59 % / 45 % | no |

Mean 0.60 → `calibrated`. But both pool notes say the same thing: dornic and borsel are
"calibrated by luck — the families are **wide and cheap**, several natural rules survive two
positives", and a player called that unfair. And the judge scored v2 **3.33 / 5** (kid_contributes
2, no_prereqs 2, rule_statable 3, nameable = **yes**), with the instruction this iteration
implements:

> *"sum/prime/multiple-of-y templates are number theory and exactly the AI predicate bank's home
> turf; replace with relations between two cards or positions a kid checks by eye: 'the two reds are
> the same rank', 'the highest and lowest card share a suit', 'there are more hearts than any other
> suit'."*

**The attack to beat** (both players' own words, pool 2 and pool 3): round 1 skip everything and
harvest ~300 clues for base rates; round 2 answer a **random candidate** on every item and keep the
1/k that come back correct — ~30 free gold labels, "30× what a demo gives"; per clue keep the
predicates true of every example and of **exactly one candidate**, weight by rarity, answer the
candidate the rarest survivor points at; then learn U from the labels by asking which predicate was
the *unique explanation* of each known-correct answer. The pool-3 players said in as many words
that "my engine wins on arithmetic families and loses on perceptual ones" — dornic v2 was the
arithmetic family.

## 17. Recipe step 1 — the attacker's bank, rebuilt for cards

Union of the card banks the players actually brought:

* `dornic1b`'s `dornic_preds()` — 359 predicates, carried verbatim inside v2's own `generate`;
* `tavrik1a/strategy.py::f_hand()` — `cntS:k`, `nsuits`, `red:k`, `redpar`, `hasr:r`/`nor:r`,
  `rsum`, `rsum%k`, `rmax`, `rmin`, `rrng`, `nrd`, `haspair`, `hastrip`, `consec2`, `maxrun`,
  `nev`, `nface`, `hasace`, `first:v`, `lastr:v`, `firsts:S`, `lasts:S`, **`sfl`**, `adjsuit`,
  `nlow`, `nhigh`;
* `tavrik1b/strategy.py::f_dornic()` — `sC/sD/sH/sS`, `maxsuit`, `ndistrank`, `maxrankcnt`,
  `npairs`, `span`, `minr`, `maxr`, `sum%2`, `nface`, `nred`, `nconsec`, `c3`, `ace`, `king`,
  `alldist`, `gapmax`, **`suitcons`**;
* `ospren1a/strategy.py::f_dornic()` — the same plus `sum%3`, `sum%5`, `gaps`, `longestrun`,
  **`high_suit`**, **`low_suit`**, `maxsuitcnt`, `spread_even`;
* `tresk1b/strategy.py::build_dornic()` — ~200 boolean predicates (`allsamesuit`, `allred`,
  `noface`, `alleven`, `sumeven`, `twopair`, `samecolourpair`, `pairdiffcolour`, `consec`,
  `run3`, `moreredthanblack`, `summod m`, `spadecount_eq_heart`, `cntsuit_Xk`, `max v`, `min v`…);

**plus the obvious extensions a second round adds**: every number feature under **both ace
conventions** (A = 1 and A = 14, because v3 prints the ace high and a player would try both), the
rank and suit at each end and in the middle (`firsts`, `lasts`, `mids`, `firstr`, `lastr`, `midr`),
`nadjsuit`, `suitset`, `colstr` (the hand's colour word, e.g. `BBRRR`), `nsuitpair`, `most X`,
`eq XY`, `gt XY`, `nfaceA`, `dig` (the total's last digit).

**127 feature keys, 4 225 realised (key, value) pairs, 511 of them with a base rate ≥ 1 %** over
the generator's 24 000-hand pool. Those 511 are what `generate` carries as a bit mask and what the
simulated attacker uses (the players floor their own frequency estimates, so rarer pairs are not
usable to them either).

## 18. Recipe step 2 — the retirement test: v2's universe **is** the bank

Jaccard of each v2 rule against the bank, over 30 000 random five-card hands:

| v2 template | the bank predicate that says the same thing | J |
|---|---|---|
| exactly *n* hearts / diamonds / clubs / spades | `cntH == n` … | **1.00** |
| exactly *n* red cards | `red == n` | **1.00** |
| exactly *n* even cards | `nevl == n` | **1.00** |
| exactly *n* picture cards | `nface == n` | **1.00** |
| exactly *n* different suits | `nsuits == n` | **1.00** |
| the highest card is *n* / the lowest is *n* / highest − lowest = *n* | `maxl` / `minl` / `rngl` | **1.00** |
| exactly one pair | `npairs == 1` | **1.00** |
| the cards add up to *n* / to a prime / to a multiple of *y* | `suml == n` / `sumpl` / `suml%y == 0` | **1.00** |
| the red / black cards add up to a prime or to a multiple of *y* | — (only in the extended bank) | .17–.35, **1.00** extended |

**44 of v2's 52 rules are bank predicates outright.** The eight colour-sum families are the only
ones the *shipped* bank cannot say — and they go too, because the judge's objection is not Jaccard
but arithmetic: **every sum / prime / multiple-of-*y* / rank-sum-mod-*k* template is retired to the
trap list regardless of J**. That is also what made v2 illegible: the ace's value was never stated
and half the clues needed mental arithmetic over a colour-filtered subset.

## 19. Recipe step 3–5 — the universe U: 9 templates, 33 rules

The world is now **a hand of exactly five cards**, printed **lowest card first**, ranks
`2 3 4 5 6 7 8 9 10 J Q K A` with the **ace HIGH**. The picture states the convention instead of a
sentence: every line reads upwards, so an ace sits at the right-hand end after the king (demo 4
below is a clue where `K A` are the two right-hand cards and the rule is "next-door numbers"). **No
rule ever adds card values up**, so `A = 1` arithmetic is impossible to need.

"density" = share of random five-card hands obeying the rule (40 000 hands). **"bank J"** = best
Jaccard against any of the 511 realised bank predicates — the number that decides whether the
attacker can *express* the rule at all.

| t | kid sentence (read it aloud) | params | density | bank J | in U? |
|---|---|---|---|---|---|
| 0 | "**every red card is higher than every black card**" · the other way round | R, B | .091 / .093 | **.23–.26** | **IN** |
| 1 | "**all the hearts are higher than every other card**" · lower · ×4 suits | 8 | .087–.093 | **.30–.42** | **IN** |
| 3 | "**the two cards at the left-hand end are the same number**" · the right-hand end | 2 | .147 | **.30** | **IN** |
| 4 | "**the card at the left-hand end is the only one of its suit**" · the right-hand end | 2 | .317 / .322 | **.42** | **IN** |
| 5 | "**the 1st and the 2nd card are the same suit**" · 4th and 5th · 1st and 3rd · 3rd and 5th | 4 | .212–.252 | **.25–.34** | **IN** |
| 8 | "**the two cards at the left-hand end are next-door numbers**" · the right-hand end | 2 | .298 / .301 | **.38** | **IN** |
| 2 | "there are more hearts than any other suit" (the judge's example) | 4 | .158–.160 | 1.00 | **IN** (cheap) |
| 5 | "the two end cards are the same suit" (the judge's other example) | 1 | .245 | 1.00 | **IN** (cheap) |
| 6 | "there are exactly two hearts / diamonds / clubs / spades" | 4 | .273–.278 | 1.00 | **IN** (cheap, ×2) |
| 7 | "the hand has an ace / a king / a queen / a jack" | 4 | .339–.344 | 1.00 | **IN** (cheap, ×2) |
| — | every count / extremum / span / pair / sum / prime / multiple rule of v1–v2 | 52 | .03–.59 | **1.00** | EXCLUDED (§18) |

|U| = **33 rules over 9 templates, 24 of them relational** (bank J .23–.42) and 9 cheap on purpose
(J 1.00, **32.0 % of clues**, template 6 and 7 at double draw weight). Mean density of the hidden
rule **0.231**. Antichain verified by brute force over **300 000 random hands** and over the
generator's own 24 000-hand pool: **0 nesting violations**, minimum support 8.8 % (26 481 hands).
Template mix over 500 clues: 5 → 89, 4 → 71, 8 → 66, 7 → 56, 6 → 49, 0 → 47, 1 → 44, 3 → 40,
2 → 38; all 33 rules used.

### Templates measured and thrown out this round

| template | density | bank J | why not |
|---|---|---|---|
| "the highest card is a heart" | .25 | **1.00** | it *is* `high_suit`; kept as a trap (it was a v1 trap too) |
| "two cards are next-door in rank" (anywhere) | .55 | **1.00** | `consh`; and > .5, so four decoys all lacking it is itself a signature |
| "no two cards next to each other in the row share a suit" | .60 | **1.00** | `adjsuit`; trap |
| "the two matching cards are the same colour" | .07 | **1.00** | `samecolpair`; trap |
| "there are as many hearts as spades" | .30 | **1.00** | `eqHS` — tresk1b's bank literally has `spadecount_eq_heart`; trap |
| "the hand has a pair" | .49 | **1.00** | `pair`, and too dense; trap (it was v2's competitor-only rule) |
| "two cards of one suit are next-door in rank" | .30 | ~.80 | `suitcons ≥ 1`; trap |
| "the first and the last card are the same **colour**" | .48 | .55 | density > .5 territory: four decoys all lacking it is a signature |
| "**the two red cards are the same rank**" (the judge's first example) | **.02** | .30 | too rare to support a lineup — needs exactly two reds *and* a pair inside them; the same idea survives as template 3 ("the two cards at an end are the same number"), which a kid checks the same way |
| "the picture cards are all the same suit" | .04 | .35 | too rare, and vacuous when there are none |
| "the middle card is a picture card" | .10 | .40 | a property of one card at one place, not a relation |
| "the cards go up in rank left to right" | **1.00** | — | true of every printed line, exactly as in v1/v2: order is always consistent and never the rule |

**The kid constraint did the final cutting, not the Jaccard.** tavrik v3's judge fell 4.7 → 3.83 on
counted relations ("*n* apart in the alphabet"); tresk v3 rose 4.0 → 4.5 on relations a kid **spots
by eye**. Everything in dornic v3's U is a *look*, not a sum: a colour block, a suit block, two
matching numbers at one end, a lone suit at one end, two places sharing a suit, two neighbouring
numbers at one end. The only counting left is "more hearts than any other suit" — four little piles
in a fanned hand, which is the judge's own example — and "exactly two hearts".

## 20. Recipe steps 6–7 — the lineup

* **k = 5** candidates, all five-card hands, five distinct hands, none equal to an example.
* **The clue is a minimal PAIR** (lever 2): the two examples leave exactly one rule of U alive,
  neither alone does, and they are **card-disjoint** (one deck, two hands dealt). 2 examples on
  500/500 clues.
* **Matched trap profiles in the strong form** (§5b): every candidate fires exactly the same
  example-consistent excluded rules as the true one. Over 500 clues **all 5 244 fitted traps are
  satisfied by all five candidates or by none** — so no trap, no count of traps and no combination
  of traps separates the lineup. 29 excluded families are fitted, mean 10.5 per clue.
* **Four aimed orders** (lever 5): `generate` carries the 511-predicate bank, intersects it over
  the two examples and aims the true candidate's rank uniformly at random in (a) the **rarity**
  order — the surprise of the rarest surviving predicate that selects exactly one candidate, the
  statistic the players actually used — then (b) the count order, (c) the look-alike order (cards
  shared with the other candidates) and (d) the **clue-overlap** order (cards shared with the
  examples). (d) was added after the first build measured "the candidate sharing the most clue
  cards" at 28.6 %: the cheap "the hand has a king" template leaks through card overlap because the
  decoys must *not* hold the king. With (d) it is 24.6 %, four points over the floor.

## 21. Recipe step 8 — the simulated attack, v2 vs v3

The full engine: skip-harvest 300 clues for base rates → answer a random candidate on a disjoint
stream, keeping the ~1/k that come back correct as gold labels → per-predicate unique-explanation
weights (`n/m`) → rarity-weighted pick. 500 fresh test clues (seeds 1e6 …), the same 511-predicate
bank both sides (for v2, extended with the colour-sum features its own U needs).

| labels | **v2 as shipped** (k = 4, floor 25 %) | **v3** (k = 5, floor 20 %) | v3, bank + all of U |
|---|---|---|---|
| 0 | 80.8 % | **32.2 %** | 67.6 % |
| 30 | 89.2 % | **35.4 %** | 81.6 % |
| 60 | 93.5 % | **39.6 %** | 87.4 % |
| 120 | 96.0 % | **42.2 %** | 93.8 % |
| 240 | 96.8 % | **44.0 %** | 95.4 % |
| 360 | — | **44.8 %** | 96.0 % |

The shape is the point: v2 is a lookup from the first free labels; v3 pays ~7 points for the first
120 labels (that is the cheap third of the clues) and then goes **flat**. **U-coverage** (the share
of fresh clues whose true rule the learner has confidently identified: a predicate with m ≥ 4
firings and n/m ≥ 0.7) saturates at **35 %** with the generic bank — it can never pass the cheap
templates — while the attacker who is *handed* U learns it to **90 % coverage in about 240 labels**
(14 % at 30, 38 % at 60, 69 % at 120, 91 % at 240). The **in-U intersection is 100.0 %**. The gap
**40 % → 90 %** is the class, and it is paid for by inventing the vocabulary: looking at two hands
and thinking "the two cards at the right-hand end", not "the sum of the ranks".

One honesty note that matters for reading these numbers: on **v2** this simulator scores 89–93 %
where the real Opus centaurs scored **45–66 %**, because the reconstructed bank contains the
colour-sum features their own pools did not. It is therefore a *strong* model of the attacker here,
not a weak one, and v3's 35–40 % at 30–60 labels should be read as the pessimistic end.

### Levers, measured (identical conditions, 400 test clues, 60 labels)

| build | k | floor | simulated attack |
|---|---|---|---|
| **v3 as shipped** | 5 | 20 % | **40.0 %** |
| minus lever 3 — **v2 as shipped** (same engine, same bank) | 4 | 25 % | **93.5 %** |
| minus lever 5 (decoys not aimed at all) | 5 | 20 % | 43.2 % |
| minus lever 1 (k = 4) | 4 | 25 % | 40.8 % |
| lever 1 pushed (k = 6) | 6 | 16.7 % | 35.5 % |
| minus lever 2 (three-example clues) | 5 | 20 % | 36.2 % |
| the four cheap templates at half draw weight | 5 | 20 % | 31.5 % |

**The relational universe (lever 3) is worth ≈ 53 points** — the whole game, for the third class in
a row (tavrik 57, tresk 49, ospren 38). Aiming is worth ≈ 3, the fifth candidate ≈ 1 over k = 4 at
60 labels (and 4 points at 0 labels: 32.0 vs 36.0). Two honest departures from the recipe's
expectations, both **declined on the 12-year-old test rather than on the attack number**: k = 6
would buy 4.5 points but adds a sixth line to a clue that already has seven, and three-example clues
would buy 3.8 points but ask a kid to hold a third hand in their head — and lever 2 says the
minimal pair is the shape. They are the first two levers to reach for if the class comes back too
easy. The cheap templates are the *slope*: halving their weight costs the attacker 8.5 points and
would leave the class reading as arbitrary.

## 22. Four demos

```
seed 1000002    hidden rule: EVERY RED CARD IS HIGHER THAN EVERY BLACK CARD

  examples      3C 4D 6D QH AH                  (black 3; red 4 6 Q A)
                6S 9C JC JS KD                  (black 6 9 J J; red K)
  candidates 1) 2C 4D 8S 9C 10H
             2) 2S 3C 5H 9S 10D
             3) 2S 3H 7D 10C AH
             4) 2C 2S 9H 10D QH   <-- ANSWER    (black 2 2; red 9 10 Q)
             5) 2S 3D 5C 5S 8H

seed 1000005    hidden rule: THE TWO CARDS AT THE LEFT-HAND END ARE THE SAME NUMBER

  examples      2H 2S 8C JH JS
                3H 3S 5S 6D 7S
  candidates 1) 2D 4S 5C 8H AD
             2) 4H 5H 7H JS AH
             3) 5H 5C 5S 6D AH   <-- ANSWER
             4) 2D 6C 8S 9H AD
             5) 3D 8D 10C QS AH
  (note the first example also has a matching pair at the RIGHT-hand end; the second example
   is what kills that rival, which is what "a minimal identifying pair" means)

seed 1000007    hidden rule: THERE ARE MORE CLUBS THAN ANY OTHER SUIT   (a CHEAP template)

  examples      4C 4S 6S 7C 10C
                2D 3C 7S 9H KC
  candidates 1) 2C 6C 8H 10C QS   <-- ANSWER
             2) 4C 8D 8S 10S KC
             3) 3S 5S 7D 10C KC
             4) 2H 5C 7C 9H QS
             5) 3S 8D 8C 8S JC

seed 1000003    hidden rule: THE TWO CARDS AT THE RIGHT-HAND END ARE NEXT-DOOR NUMBERS

  examples      7C 8S QC KC AD                  (K then A -- the ace is high, and the printed
                2H 4D 4S 5D 6S                   order says so without a word of explanation)
  candidates 1) 3C 4C 7H 8C QS
             2) 5H 5C 6C 6S 10C
             3) 6C 7S 9H 10H JC   <-- ANSWER    (10 then J)
             4) 4H 6H 7C 8C QS
             5) 5C 7H KS AH AS
```

Demo 1 is the class in one picture: five hands of five cards, all five firing exactly the same
excluded rules, and the answer is the only one that splits into a black block then a red block.
Demo 3 is the learnable slope — a kid counts four little piles and so does a predicate bank.

## 23. Witness table — 500 fresh clues (seeds 1 000 000 – 1 000 499)

The answer is a choice among five, so the floor is **20 %**.

| witness | score |
|---|---|
| **the true rule (`solve`), verbatim and by index** | **100.0 % / 100.0 %** |
| **the in-U intersection — a player who knows U** | **100.0 %** |
| a player who knows U minus its two least-used templates | 87.2 % |
| **the full revision-3 attack, 511-predicate bank, 30 labels** | **35.4 %** |
| … at 0 / 60 / 120 / 240 / 360 labels | 32.2 / 39.6 / 42.2 / 44.0 / 44.8 % |
| the candidate satisfying the MOST example-consistent bank predicates | 28.0 % |
| universe = U + the excluded rules, one surviving hypothesis picked uniformly | 27.8 % |
| the odd one out (fewest cards in common with the other four) | 26.0 % |
| the candidate sharing the most cards with the clue | 24.6 % |
| the candidate with the most hearts | 23.2 % |
| the candidate holding the highest card | 21.6 % |
| the candidate satisfying the MOST fitted excluded rules | 21.2 % |
| pick candidate 1 | 21.0 % |
| **pick a random candidate (the floor)** | **20.8 %** |
| the candidate satisfying the FEWEST fitted excluded rules | 20.8 % |
| the candidate whose two end cards share a suit | 20.4 % |
| the candidate with a pair | 19.6 % |
| pick candidate 5 | 17.4 % |
| the candidate sharing the fewest cards with the clue | 15.8 % |
| the medoid (most cards in common with the other four) | 15.6 % |
| the candidate satisfying the FEWEST bank predicates | 12.2 % |
| **each of the 27 fitted excluded-rule families** | **6.7 – 32.1 %** (tie-breaking; see below) |

The excluded rules are *structurally* dead rather than merely weak: all **5 244** fitted traps over
the 500 clues are satisfied by all five candidates or by none, so believing one only changes which
candidate a coin lands on. Fit rates: no card above the clue's highest 100 % · none below its
lowest 100 % · at least *n* of a suit 232 % (several suits per clue) · the highest card is red /
black 54 % · the lowest card is red / black 50 % · the total is a multiple of *y* 50 % · aces low, a
multiple of *y* 40 % · two cards next-door in rank 60 % · two neighbours share a suit 43 % · as many
X as Y 41 % · exactly *n* different suits 41 % · more red than black 37 % · the hand has a pair 29 %
· no two cards share a number 22 % · exactly *n* red cards 21 % · exactly *n* even cards 21 % ·
exactly *n* picture cards 19 % · highest − lowest = *n* 12 % · the pair is two colours 13 % · the
total is prime 6 % · the cards add up to *n* 4 %. The one row above 30 % (32.1 %, "two cards of one
suit are next-door in rank") is a 53-fit tie-break.

There is **no row 10+ points over the floor** — dornic v3 has no equivalent of tresk's "biggest
clump" foothold; the foothold here is the format itself (five hands, pick one) plus the ~32 % of
clues whose rule is cheap.

Other measured numbers (500 clues): uniqueness 500/500 · minimality 500/500 · exactly one candidate
obeys the rule 500/500 · five distinct candidates 500/500 · no candidate equal to an example 500/500
· examples card-disjoint 500/500 · matched trap profiles 5 244/5 244 · examples per clue 2 → 500 ·
true-candidate position 105/108/103/97/87 · over 2 000 seeds, **2 000 distinct clues and 0 fallback
clues**.

## 24. Validation

`python tools/quickcheck.py challenges/lab/dornic.json --seeds 300 --cap max_score_code_chars=1024`
→ `OK dornic  gen=9.9-13.3ms score=0.9ms solve=0.9ms` over repeated runs (quickcheck reports the
*max* over the 300 seeds; the mean is 2.83 ms), **no warnings**.

| quantity | value | cap |
|---|---|---|
| `score` source | **997 chars** (v1 1016, v2 905) | 1024 (the rule-family raise, RULE_FAMILIES §4) |
| `generate` source | 21 587 | 50 000 |
| `solve` source | 1 980 | 5 000 |
| `generate` | **2.83 ms mean** over 2 000 seeds, 6.5 ms max | 100 ms |
| `score` | 0.30 ms (0.9 ms max incl. junk) | 50 ms |
| `solve` | 0.27 ms | 2 000 ms |
| clue | ≤ 113 chars | 1 024 |
| answer | ≤ 16 chars | 1 024 |

The 33 rules are rebuilt in the scorer from a **131-character table**
(`"0R- 0B- 1H0 … 80- 81-"`, each entry a template digit plus a two-character parameter), which is
what bought the room for six relational templates inside 1 024 chars; the nine templates are one
list comprehension evaluated eagerly, so every parameter is padded to two characters and the one
index-taking rule reads its positions with `"01234".find(x)` (which returns −1, i.e. a legal index,
for the templates that do not use it).

`score` was checked candidate-by-candidate against `solve` on **500 clues × 5 candidates ×
(verbatim / 1-based index / lower case with doubled spaces) — 7 500 checks, 0 disagreements** — and
returns 0 without raising for `""`, `"x"`, `"0"`, `"6"`, `"9"`, `"-1"`, `"1.0"`, `"1 2"`,
`"1"×100`, the unicode digits `"١"` and `"²"`, the clue itself, the example block alone, a malformed
hand (`2Z 3Z …`), a well-formed five-card hand that is not in the lineup, a candidate with a card
removed and a candidate with a card added. Module-level tables cost **≈ 5 s once per worker** (the
24 000-hand pool, its 33-bit U mask, its excluded-rule features and its 511-bit bank mask); not
charged to `max_generate_ms`. `solve` re-derives the survivor exactly as the scorer does and returns
the true candidate verbatim.

## 25. Predicted classification

**Calibrated**, and for the right reason this time.

* **Without a demo** the clue reads as multiple choice from round 1 (two hands, a gap, five hands
  of the same size), so every probe is well formed and the floor is a free 20 %. The engine that
  scored 45–66 % on v2 now pays **32 % at zero labels, 35–40 % once the free labels arrive, and
  stops improving** (44.8 % at 360). Expect **25–45 %**.
* **With a demo** the demo teaches the format and one worked rule. The way up is to notice that
  this class talks about *ends of the fan, blocks of colour and pairs of places* and to write those
  predicates down; a player who does scores 87–96 %, one who maps 7 of the 9 templates scores 87 %.
  Expect **40–65 %**.

Mean across two Opus teams ≈ **0.35–0.55** → `calibrated`. If it comes back **too easy** the levers
are k = 6 (−4.5 points) and three-example clues (−3.8); if **too hard**, put the cheap templates
back up (double weight on all four takes the attacker to ~45 %) or drop to k = 4 (+1 to +4).

**12-year-old test (target: 4.3+, up from 3.33).** The object is unchanged and instantly evocable —
a hand of cards, fanned, printed in order. What changed is what the rules talk about. Read them
aloud: *every red card is higher than every black card · all the hearts are higher than every other
card · the two cards at the left-hand end are the same number · the card at the right-hand end is
the only one of its suit · the 4th and 5th cards are the same suit · the two cards at the right-hand
end are next-door numbers · there are more clubs than any other suit · the hand has a queen.* Each
is one breath and each can be checked on five cards in about two seconds, by looking rather than by
counting. The three things the judge objected to are gone: **no sums, no primes, no multiples**
(all retired to the trap list); **no unstated ace convention** (the printed order says A is high and
nothing ever adds A up); and the "nameable = yes" problem is answered the way tavrik/tresk/ospren
answered it — the rules are still one-breath sentences, but they are sentences about *relations
between two cards*, which is exactly what a predicate bank cannot say and a kid says first.
