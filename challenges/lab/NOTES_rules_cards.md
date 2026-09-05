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
