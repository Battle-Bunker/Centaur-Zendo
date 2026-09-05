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
