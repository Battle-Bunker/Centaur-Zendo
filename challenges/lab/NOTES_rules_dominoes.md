# mestrel — a rule-family class in the world of a LINE OF DOMINOES

Designed 2026-09-05 to the **Revision 3** recipe in `docs/RULE_FAMILIES.md` ("beat the free-label
attack") — the first rule-family class built to that recipe from scratch rather than hardened into
it. Sibling write-ups: `NOTES_rules_beads.md` §§15–23 (tresk v3) and `NOTES_rules_pixels.md`
§§17–25 (ospren v3). Shipped file: `challenges/lab/mestrel.json`. Not committed.

---

## 1. The world

An instance is a **row of 4–7 dominoes**, each half 0–6, drawn exactly as a kid would lay them out:

```
[3|5][5|1][1|6][6|6]
```

**The halves do not have to match.** That single decision is what makes the world work: the famous
domino operation — *the proper chain* — becomes a **property a line may or may not have** instead of
a constraint on how lines are built, so it can be (and is) an **excluded rule that the decoys
satisfy**. `sim/DESIGN_LOOP.md`'s 12-year-old test is explicit that the object's famous operation
must never be the rule ("if the rule is the object's famous operation the model recognises the genre
and the game is over"); here it is the loudest trap in the class.

**Clue** = 2 example lines (3 on 0.2 % of clues), a blank line, then **five candidate lines with the
same number of dominoes**, exactly one of which obeys the hidden rule.
**Answer** = that candidate written back (whitespace-insensitive; the scorer reads the digits, so
`[0|3][5|3]`, `0 3 5 3` and `0-3 5-3` all work) **or its 1-based index 1–5**. Floor = 20 %.

Internally a line is the list of its 2n halves; domino *i* is `(h[2i], h[2i+1])`.

---

## 2. The universe U — 14 templates, 27 rules

`density` = share of the 18 000-line generator pool that obeys the rule. `minsup` = the smallest
number of satisfiers at any one length (4, 5, 6 or 7 dominoes) — the lineup needs them there.
**`bank J`** = the best Jaccard against any of the **821** realised (key, value) predicates of the
attacker's bank (§5), measured **within a length**, because every candidate of a clue shares one:
that is the number which decides whether the attacker can *express* the rule at all.

| t/q | kid sentence (read it aloud) | density | minsup | bank J | best bank predicate |
|---|---|---|---|---|---|
| 0/0 | "the number at the **left end** of the line is on **every domino**" | .079 | 294 | **.39** | `nshare == 3` |
| 0/1 | "the number at the **right end** is on every domino" | .081 | 278 | **.39** | `nshare == 3` |
| 1/0 | "the number at the **left end** is **nowhere else** in the line" | .215 | 636 | **.39** | `dbl0 == False` |
| 1/1 | "the number at the **right end** is nowhere else" | .207 | 601 | **.38** | `dbl_last == False` |
| 2/0 | "the dominoes **take turns**: bigger number on the right, then on the left, then on the right…" | .041 | 152 | **.19** | `nasc == 3` |
| 2/1 | "…the other way round (bigger on the left first)" | .044 | 154 | **.19** | `ndesc == 4` |
| 3/0 | "**the doubles are all next to each other** (there are two or more)" | .110 | 408 | **.34** | `ndbl == 2` |
| 4/0 | "**all the doubles are the same number** (there are two or more)" | .063 | 229 | **.42** | `modecnt == 7` |
| 5/0 | "**every double is at one of the two ends** of the line" | .153 | 484 | **.45** | `ndbl == 1` |
| 6/1–6/6 | "**all the 4s are on the same domino**" (v = 1…6) | .037–.040 | 119 | **.20–.39** | `cnt4 == 2` |
| 7/0 | "**the biggest number and the smallest number are on the same domino**" | .391 | 1713 | **.40** | `noninc == False` |
| 8/0 | "**the two numbers at the ends of the line are together on one domino**" | .323 | 1275 | **.45** | `fl_eq == False` |
| 9/0 | "the **left-hand numbers** never go down as you go along" | .080 | 203 | **.30** | `nondec == True` |
| 9/1 | "the **right-hand numbers** never go down" | .079 | 189 | **.32** | `nondec == True` |
| 10/0 | "**the double's number is nowhere else** in the line" | .084 | 197 | **.35** | `modecnt == 2` |
| 11/0 | "the two numbers at **the ends of the line are the same**" | .200 | 873 | 1.00 | `fl_eq == True` **CHEAP ×2** |
| 12/1–3 | "exactly *k* of the dominoes are **doubles**" (k = 1, 2, 3) | .092–.318 | 312 | 1.00 | `ndbl == k` **CHEAP** |
| 13/0–2 | "exactly *k* of the halves are **blank**" (k = 0, 1, 2) | .232–.285 | 844 | 1.00 | `cnt0 == k` **CHEAP** |

**|U| = 27 rules over 14 templates, eleven of them relational** (bank J .19–.45) and three cheap
(J 1.00, on purpose — the learnable slope, §6). **Antichain** verified by brute force over the
18 000-line pool **and** 300 000 uniform-random lines: **0 nesting violations**, minimum support
663 lines in the pool and 1 928 in the random sample. `MASKOF` (the one-pass table builder) was
verified identical to the readable predicate `P` on all 18 000 pool lines and 60 000 random lines.

Template mix over 2 000 clues: every one of the 27 rules is drawn; the three cheap templates are
**28.2 %** of clues (template 11 alone at double weight, 16 %).

### The relations, in one place

*the number at an end is on every domino · that number is nowhere else · the dominoes take turns
which way up · the doubles are all together · the doubles are all the same number · every double is
at an end · all the 4s are on one domino · the biggest and the smallest number share a domino · the
two end numbers share a domino · the left-hand numbers never go down · the double's number is
nowhere else.*

Every one is a **two-thing comparison a kid makes by eye** — an end against the whole line, a
domino against its neighbour, a half against the half above it, a number against where it turns up
again. Nothing here is arithmetic: the class **never** says anything about how much a domino adds
up to (the tavrik lesson, `RULE_FAMILIES.md` §9 — counted relations dropped that class's kid score
from 4.7 to 3.83, while tresk's and ospren's visual relations held 4.5).

---

## 3. Templates measured and thrown out (all measured on the shipped pool and bank)

| template | density | bank J | why not |
|---|---|---|---|
| **every domino touches the next one with the same number** (a proper chain) | .032 | **1.00** | `nmatch == n−1`; and it is the object's famous operation — **kept as the loudest trap** |
| exactly one join does not match | .081 | **1.00** | `nmatch == n−2` |
| every domino shares a number with the next one | .217 | **1.00** | `nshare == n−1` |
| no domino shares a number with the one next to it | .070 | **1.00** | `nshare == 0` |
| the line reads the same backwards | .016 | **1.00** | `palin` |
| every domino has its bigger number on the right / left | .019 | **1.00** | `allasc` / `alldesc` |
| the numbers never go down along the whole line | .014 | **1.00** | `nondec` (only the *half-by-half* version, template 9, is outside the bank) |
| **every domino has a 3 on it** (a fixed number) | .020 | **1.00** | `ntile3 == n` — the parameterised version is a gift; the **anchored** version ("the number at the *end* is on every domino", template 0) is not |
| one number is on every domino | .138 | .69 | `nshare` again |
| the first and last dominoes are the same domino | .108 | **1.00** | `t0eqtl` |
| the first domino is the last one **turned round** | .068 | .67 | inside `t0eqtl` |
| the biggest number is only there once | .371 | **1.00** | `cntmax == 1` (the players' `maxtwice`) |
| all the left-hand numbers are different | .115 | **1.00** | `nleft == n` |
| the biggest number is on the first domino | .373 | **1.00** | `maxtile0` |
| the same domino turns up twice the same way up | .376 | .90 | `ndisttileo` |
| the biggest number in the line is on a double | .219 | .73 | `maxsum` |
| there is a double at one end of the line | .368 | .68 | `hasdbl`; also too dense |
| the left numbers and the right numbers are the same numbers | .087 | .66 | `nsingle` |
| every domino shares a number with the first one | .188 | .65 | `nshare` |
| the number at the left end is on the last domino too | .346 | .59 | `fl_eq`; and it **contains** template 11 (antichain) |
| the same domino turns up again turned round | .280 | .56 | `alldisttile` |
| the biggest number in the line is on every domino | .036 | .55 | `ntile6` |
| the first domino and the last share a number | .528 | .55 | density > .5 — four decoys all *lacking* it is itself a signature |
| the first and last dominoes have no number in common | .472 | .60 | same, from the other side |
| all the dominoes with a 3 on them are next to each other | .171 | .51 | `ge2_3` |
| every domino has one of the two end numbers on it | .210 | .49 | `nshare` |
| **the line starts with a double AND ends with a double** | .078 | **.38** | passed the Jaccard test and was **still dropped**: it is exactly the conjunction of two trap families ("the first domino is a double" ∧ "the last domino is a double"), so **no matched-profile decoy can exist** — measured 0 usable clues in 2 000 |
| every double has another double next to it | .118 | .34 | **contains** template 3 (antichain) |
| the number at the left end is on the second domino | .328 | .35 | **contains** template 0 (antichain) |
| the dominoes read the same from either end (tile mirror) | .003 | .21 | far too rare; at 4 dominoes it is `ndisttileo ≤ 2` in disguise |
| no number is on two different dominoes | .007 | .19 | too rare, and impossible at 7 dominoes — a length-conditioned rule leaks through a lineup |
| the left-hand numbers go **up every time** (strict) | .010 | .27 | too rare; the non-strict version is template 9 |

**Two lessons worth carrying to the next world.** (1) *Anchor, don't parameterise.* "every domino
has a 3 on it" is `ntile3 == n` (J 1.00); the same sentence anchored to something the line itself
supplies — "the number at the **end** is on every domino" — is J .39. Every relational template here
is anchored to an end, to the extremes, to the doubles, or to a value's own occurrences.
(2) *A rule that is the conjunction of two traps is unusable*, however good its Jaccard: the matched
trap profile (§6) then forces every decoy to obey the rule.

---

## 4. The exclusions (never in U; the decoys satisfy them)

**23 trap families**, fitted to each clue from the examples (17 of them fire at least once in 500 clues): the chain and every count of matching
joins · no join matches · every domino shares a number with the next · the line reads the same
backwards · **all the pip arithmetic** (every domino adds up to the same, the totals never go down,
the whole line adds up to *n*, all the halves even, all odd) · at least *k* of the number *v* · at
least *k* doubles · no number bigger / smaller than *v* · exactly these numbers are used · no two
dominoes are the same · the first / last domino is a double · the biggest number turns up only once
· all the left-hand (right-hand) numbers are different · every domino has its bigger number on the
right / on the left.

Measured over 500 clues: **6.35 fitted traps per clue, 3 174 in all, and every single one of them is
satisfied by ALL FIVE candidates or by NONE (3 174 / 3 174 = 100 %)** — §5b of Revision 2 in its
strong form. So no trap, no count of traps and no combination of traps separates the lineup, and a
player whose universe is U *plus* all 22 trap families is worth exactly a player who knows U.

| excluded rule (fitted to the clue) | fits | picking by it scores |
|---|---|---|
| at least *k* of the number *v* (7 values) | 342 % (3.4 per clue) | 20 % |
| at least *k* of the dominoes are doubles | 54 % | 18 % |
| no number smaller than *v* | 53 % | 18 % |
| no number bigger than *v* | 51 % | 21 % |
| **at least *k* joins match (k = n−1: a proper chain)** | 40 % | 28 % |
| no two dominoes are the same | 19 % | 21 % |
| the biggest number turns up only once | 14 % | 19 % |
| no join matches at all | 14 % | 24 % |
| every domino shares a number with the next one | 12 % | 23 % |
| the last / first domino is a double | 11 % / 11 % | 29 % / 27 % |
| the whole line adds up to *n* · exactly these numbers are used | 4 % / 4 % | never selects / 0 % |
| all the left-hand / right-hand numbers are different | 2 % / 2 % | never selects / 0 % |
| the totals never go down · all the halves even | 1 % / 0 % | never selects |

The 18–29 % column is **pure tie-breaking** (all five candidates satisfy the trap, so the pick is
random), against a 20 % floor.

---

## 5. The attacker's bank, rebuilt inside `generate` (recipe step 1)

Union of the generic banks the revision-2 players actually brought — `tresk1b`'s `build_seq()` +
`extra_seq()` (a list of numbers: sums, sums mod *m*, max/min/range, sorted/strict/palindrome,
adjacent equalities, counts and parities of each value, positions, runs, peaks and valleys, mode
counts…) and `build_dornic()` + `extra_dornic()` (a hand: pairs, trips, "two of a kind", the highest
card, ranks present, consecutive values, per-suit counts), plus `ospren1a`'s `f_borsel_a` /
`f_borsel_b` — **transposed to a line of dominoes and extended with everything a second round would
add for this world**: the per-domino totals (`sums`, `maxsum`, `sumsalleq`, `sumsnondec`), the
doubles (`ndbl`, `dbl0`, `dbl_last`, `dblvals`), the blanks, the **joins that match** (`nmatch`,
`chain`, `nomatch`), the **neighbours that share a number** (`nshare`, `loosechain`), the **tiles
containing each value** (`ntile0…ntile6`), the left and right halves (`lefts`, `rights`, `nleft`,
`nright`), the first and last domino and their equality (`t0`, `tl`, `t0eqtl`), `alldisttile`,
`ntouchsame`, `cntmax`, `cntmin`, `posmax`, `maxtile0`…

**150 feature keys, 42 913 realised (key, value) pairs over the 18 000-line pool; the 821 with base
rate ≥ 1 % are carried inside `generate` as a bit mask for the aiming** (the players floor their own
frequency estimates at 5 %, so nothing rarer is usable to them anyway). The bank is deliberately
*stronger* than the banks the players brought: it already knows dominoes are pairs. That is why the
retirement list in §3 is so long — and why the eleven surviving templates are worth having.

---

## 6. How the lineup is built

1. **The instance distribution is a mixture of real-looking lines, not seven-sided dice**: scatter
   (20 %), a chain with 0–3 joins broken (12 %), one number on nearly every domino (14 %), a small
   set of numbers (8 %), doubles planted in a block / at the ends / scattered (12 %), every domino
   turned the same way or turning by turns (12 %), the halves in order (8 %), a number shut inside
   one domino (8 %), mirrors and repeats (6 %). Under uniform pips a chain has probability .003 and
   two doubles together .01 — the mixture is what gives both the rules and the kid something to look
   at, and every example and every candidate is drawn from exactly it.
2. **Minimal example set, a pair first** (lever 2): the two examples leave exactly one rule of U
   alive and neither alone does. 499 of 500 clues are two-example clues.
3. **Five candidates** (lever 1), one length, five distinct lines, none equal to an example.
4. **Matched trap profiles** (§5b, strong form) *and* the same number of different pip values, so
   "the odd one out by variety" is worth nothing.
5. **The truth's rank is aimed at four orders** (lever 5): the **rarity** order (the rarest bank
   predicate that selects exactly one candidate — what both revision-2 players actually ran), the
   **count** order, the **look-alike** order (halves shared with the other four), and the
   **family-resemblance** order (halves shared with the nearest example). Measured over 500 clues:
   a decoy strictly **out-counts** the truth on **69.6 %** of clues (Revision 2 rule 2 asks ≥ 40 %)
   and carries a unique explanation **at least as rare** on **74.8 %**.
6. **Three cheap templates at 28 % of clues** (lever 4 of the recipe's step 4) are the learnable
   slope. Measured dial, same engine, 500 clues, attack at 0 / 30 / 60 / 120 / 240 labels:

   | cheap draw weight | share of clues | attack |
   |---|---|---|
   | single | 21.4 % | 22.4 / 37.6 / 36.8 / 39.0 / 38.8 |
   | **template 11 doubled (shipped)** | **28.2 %** | **26.2 / 43.4 / 43.2 / 44.0 / 44.6** |
   | all three doubled | 34.0 % | 27.8 / 50.4 / 52.8 / 51.8 / 52.0 |

   The middle row is the one that sits in the middle of the recipe's 35–55 % band.

---

## 7. The attacker table (recipe step 8)

Full engine: skip-harvest 300 clues for base rates → answer a **random candidate** on a disjoint set
of clues, keeping the ~1/5 that come back correct as gold labels **and the wrong picks as
negatives** → per-predicate unique-explanation weights → rarity-weighted pick. 500 fresh test clues
(seeds 1e6 …), live bank (every realised (key, value) pair, base rate floored at 5 %).

| gold labels (clues answered) | **mestrel with the generic bank** | the same engine with a bank that also holds all of U | U-coverage |
|---|---|---|---|
| 0 (0) | **26.2 %** | 64.8 % | 0 % |
| 30 (143) | **43.4 %** | 98.0 % | 11 % |
| 60 (292) | **43.2 %** | 99.0 % | 49 % |
| 120 (647) | **44.0 %** | 100.0 % | 70 % |
| 240 (1 185) | **44.6 %** | 100.0 % | 92 % |
| 360 (1 785) | — | 100.0 % | 97 % |

**The shape is the point.** The free labels are worth 17 points and then **nothing**: 43 → 45 % from
30 to 240 labels. They buy exactly the three cheap templates (28 % of clues, scored **98.6 %** once
the attacker has 60 labels) and nothing else; the eleven relational templates together sit at
**21.4 %** — the 20 % floor — because the vocabulary cannot express them. Per-template accuracy of the
60-label attacker on the shipped build (500 clues): the six cheap rules **92–100 %** (99 % together);
the relational ones 11 % (every double at an end), 11 % (biggest and smallest), 16 % (the two end
numbers together), 19 % (the doubles together), 22 % (the double's number), 25 % (the doubles all
alike), 0–29 % (an end number nowhere else), 16–29 % (an end number on every domino), 12–38 % (the
halves never go down), 31–45 % (take turns), 0–80 % (all the *v*s on one domino, 3–9 clues each).

**The honest ceiling.** The **in-U intersection is 100.0 %** — a player who has reconstructed U
answers every clue correctly. An attacker whose bank also contains all of U reaches 98 % at 30
labels and learns U to **90 % coverage in ≈ 230 labels** (coverage = the share of fresh clues whose
true rule the learner has confidently identified: *m* ≥ 4 firings and *n*/*m* ≥ 0.7). With the
generic bank alone, coverage can never pass the three cheap templates. **The gap 43 % → 100 % is the
class**, and it is paid for by inventing the vocabulary: looking at
`[2|2][5|0][6|5][6|5]` / `[0|0][0|5][5|0][0|4][4|3][1|4][4|4]` and thinking *"where are the
doubles?"* rather than *"how many?"*.

---

## 8. Lever ablation (identical conditions, 400 test clues)

| build | k | floor | attack at 0 / 30 / 60 labels |
|---|---|---|---|
| **as shipped** | 5 | 20 % | 24.0 / 40.8 / **41.0 %** |
| **minus lever 3** — the same engine, the same bank, the same traps, but a universe of 22 rules every one of which IS a single bank predicate (exactly *k* doubles / blanks, the ends match, a chain, no join matches, a palindrome, all dominoes one way up, the biggest number is *v*, the number *v* is on exactly two halves, the totals never go down, no two dominoes the same) | 5 | 20 % | 48.5 / 91.5 / **93.5 %** |
| minus lever 5 — decoys not aimed at all | 5 | 20 % | 32.0 / 38.0 / **47.0 %** |
| minus lever 1 — k = 4 | 4 | 25 % | 33.5 / 38.5 / **47.5 %** |
| lever 1 pushed — k = 6 | 6 | 16.7 % | 21.0 / 39.0 / **41.8 %** |
| minus lever 2 — three-example clues | 5 | 20 % | 36.5 / 44.0 / **44.2 %** |

Read off the differences: **the relational universe (lever 3) is worth ≈ 52 points** — the whole
game, exactly as on tavrik (41), tresk (49) and ospren (38). The rarity aiming (lever 5) is worth
≈ 6, the fifth candidate (lever 1) ≈ 6.5, the two-example clue (lever 2) ≈ 3. **k = 6 buys nothing**
(−0.8, inside noise) and costs a clue line and a kid's patience — five is the number, for the third
time in a row.

---

## 9. Three demos

```
seed 1000006      hidden rule: EVERY DOUBLE IS AT ONE OF THE TWO ENDS OF THE LINE

  examples     [2|2][5|0][6|5][6|5]
               [0|0][0|5][5|0][0|4][4|3][1|4][4|4]

  candidates 1 [0|0][2|2][3|4][4|4][5|5]
             2 [3|3][6|2][0|6][5|0][0|5]     <-- the answer
             3 [4|4][1|1][2|0][5|0][5|1]
             4 [1|1][0|0][1|4][6|4][5|5]
             5 [5|5][5|5][5|6][6|2][0|4]
```
The class in one picture. Every candidate has doubles (4, 1, 2, 3, 2 of them), no candidate's two
end numbers match, all five fire exactly the same excluded rules — "how many doubles?" and "do the
ends match?" are both worth nothing, and the only thing left to look at is **where** the doubles
sit. Only candidate 2 keeps its double off the middle.

```
seed 1000014      hidden rule: THE RIGHT-HAND NUMBERS NEVER GO DOWN AS YOU GO ALONG

  examples     [0|0][1|0][2|4][4|4]                 right halves 0 0 4 4
               [2|0][1|4][4|5][2|5][1|5]            right halves 0 4 5 5 5

  candidates 1 [0|2][1|4][4|3][3|2][6|1]            2 4 3 2 1
             2 [1|0][2|3][3|4][1|4][3|6]            0 3 4 4 6   <-- the answer
             3 [6|2][4|6][6|0][1|4][5|4]            2 6 0 4 4
             4 [5|5][1|2][2|0][6|6][4|4]            5 2 0 6 4
             5 [0|5][1|5][5|6][0|4][4|2]            5 5 6 4 2
```
The pure relation: a kid reads down one column of halves with a finger. A predicate bank has
`nondec` for the whole line of fourteen halves and nothing for *every other half*.

```
seed 1000008      hidden rule: THE TWO NUMBERS AT THE ENDS OF THE LINE ARE THE SAME  (a CHEAP one)

  examples     [4|1][3|6][5|1][1|3][6|4][2|3][6|4]
               [0|0][4|0][2|0][4|0]

  candidates 1 [5|2][2|6][3|6][4|3][0|0]
             2 [1|0][3|3][2|3][0|4][5|2]
             3 [3|6][2|1][2|5][4|3][6|3]     <-- the answer
             4 [1|3][1|4][0|2][3|5][2|2]
             5 [3|6][1|4][1|2][1|0][0|1]
```
The learnable slope: a kid checks the first and last number, and so does a predicate bank
(`fl_eq`). 28 % of clues are of this kind; they are what makes the free labels worth 17 points and
what stops the class reading as arbitrary.

---

## 10. Witness table — 500 fresh clues (seeds 1e6 … 1e6+499)

Five candidates, so the floor is 20 %.

| witness | score |
|---|---|
| **the in-U intersection — a player who knows U** | **100.0 %** |
| the true rule (`solve`), verbatim and by index | **100.0 % / 100.0 %** |
| a player who knows U minus **two whole templates** | 79.6 – 93.6 % (median 89.4) |
| **the full revision-3 attack, 30 labels** | **43.4 %** |
| … at 0 / 60 / 120 / 240 labels | 26.2 / 43.2 / 44.0 / 44.6 % |
| the candidate with the **fewest doubles** | **31.8 %** |
| the candidate whose **two end numbers are the same** | **31.4 %** |
| the candidate satisfying the MOST example-consistent bank predicates | 27.2 % |
| the candidate using the fewest different numbers | 22.6 % |
| the candidate with the most pips altogether | 22.6 % |
| pick candidate 1 | 22.8 % |
| the candidate whose neighbours share the most numbers | 22.2 % |
| **pick a random candidate (the floor)** | **20.4 %** |
| the candidate most like an example, place by place | 19.2 % |
| the candidate least like an example | 18.8 % |
| the candidate most like the other four (the medoid) | 18.8 % |
| the candidate with the biggest number on it | 18.4 % |
| the candidate with the most joins that match (the longest chain) | 17.6 % |
| the candidate least like the other four (the odd one out) | 17.4 % |
| the candidate with the most blanks | 16.6 % |
| the candidate with the most doubles | 16.2 % |
| the candidate satisfying the FEWEST example-consistent bank predicates | 13.6 % |
| **each of the 22 excluded rules, fitted to the clue** | **18 – 29 %** (pure tie-breaking) |

A scan of **every** bank feature used as a fixed one-feature heuristic ("always answer the candidate
with the largest / smallest *x*") found nothing above **38.9 %** (`fl_eq`, on the 329 clues where it
separates — 31.4 % unconditionally, and it is the cheap template doing its intended job), then
`min ndbl` 34.2 %, `t0eqtl` 30.1 %, `loosechain` 30.1 %, `modecnt` 29.2 %. Those two ~31 % rows are
the **foothold**: a demo-less player who plays either of them beats the floor by eleven points, as
tresk's "biggest clump" (33 %) does.

Other measured numbers (500 clues): uniqueness 500/500 · minimality 500/500 · exactly one candidate
obeys the rule 500/500 · all five candidates the same length 500/500 · five distinct candidates
500/500 · no candidate equal to an example 500/500 · **matched trap profiles 3 174/3 174** ·
examples per clue 2 → 499, 3 → 1 · candidate length 4/5/6/7 dominoes → 106/125/132/137 ·
true-candidate position 114/92/121/91/82 · over **3 000 seeds, 3 000 distinct clues**, and all 27
rules and 14 templates drawn in 500.

---

## 11. Validation

`python tools/quickcheck.py challenges/lab/mestrel.json --seeds 300 --cap max_score_code_chars=1024`
→ `OK mestrel  gen=14.38ms score=0.73ms solve=0.46ms`, **no warnings**.

| quantity | value | cap |
|---|---|---|
| `score` source | **1 023 chars** | 1024 (the rule-family raise, `RULE_FAMILIES.md` §4) |
| `generate` source | 25 639 | 50 000 |
| `solve` source | 2 541 | 5 000 |
| `generate` | **2.46 ms mean**, 2.02 median, 13.6 p99, 22.1 max over 5 000 seeds | 100 ms |
| `score` | 0.36 ms mean, 0.39 ms on a 4 000-character answer | 50 ms |
| `solve` | 0.46 ms max | 2 000 ms |
| clue | **147–263 chars** | 1024 |
| answer | ≤ 35 chars, or 1 | 1024 |

Module-level tables cost **3.6 s once per worker** (the 18 000-line pool, its 27-bit U mask, its
trap readouts and its 821-bit bank mask) — not charged to `max_generate_ms`, and well inside the
sandbox's 60 s budget for compiling a seven-class pool.

`score` was checked candidate-by-candidate against `solve` on 600 clues × 5 candidates × **7 answer
forms** (verbatim · index · index with spaces · a trailing newline · one space-separated line ·
digits only · brackets replaced by dashes) — **21 000 checks, 0 disagreements**. It returns 0
without raising for `""`, `"0"`, `"6"`, `"7"`, `"9"`, `"55"`, `"1 2"`, `"x"`, `"1"×100`, `"["×4000`,
a 4 000-character random domino string, `[9|9]×8`, the clue itself, the example block alone, the
candidate block alone, `"-1"`, `"1.0"`, `"None"`, `"[]"`, and the unicode digits `"١"` / `"²"`.
`generate` is deterministic across processes and hash seeds (md5 of the first 200 clues identical
under `PYTHONHASHSEED` 0 / 1 / 12345) and `MASKOF` agrees with the readable `P` everywhere.
The 27 rules are rebuilt in the scorer from a **54-character table** (`"0001101120213040…"`, two
characters per rule: a hex template id and a digit parameter) plus one fourteen-branch predicate
list — which is what bought room for eleven relational templates inside 1 024 characters.

---

## 12. Predicted classification

**Calibrated**, with the risk on the easy side and named.

* **Without a demo** the clue reads as multiple choice from round 1 (two lines of dominoes, a gap,
  five lines of the same length), so every probe is well formed and the floor is a free 20 %. The
  engine that took 79–96 % off the revision-2 lineup classes pays **26 % at zero labels, 43 % once
  the free labels arrive, and stops improving** (44.6 % at 240 labels). The best cheap heuristics —
  "answer the one with the fewest doubles", "answer the one whose two ends match" — are worth 32 %.
  Expect **25–45 %**.
* **With a demo** the demo teaches the format in one look and one worked rule. The way up is to
  notice that this class talks about **where the doubles are, which number is at an end, and one
  half against the next** — and to write those predicates down; a player who does scores 98–100 %,
  one who maps 12 of the 14 templates scores 80–94 % (median 89).

Mean across two Opus teams ≈ **0.35–0.55** → `calibrated`. If it comes back **too easy**, the levers
in order are: drop template 11 to single draw weight (measured: 21 % of clues, attack 22/38/37 %),
then retire template 7 (the densest relational one), then k = 6 (−0.8, cheap but real). If **too
hard**: put all three cheap templates on double weight (measured: 34 % of clues, attack
28/50/53 %), or k = 4 (+6.5).

**12-year-old test (target 4.3+).** The object is the most ordinary thing in the box: *a line of
dominoes*, drawn the way a kid lays them out. Nobody has to be told what a double or a blank is. The
task is the puzzle-book one — *which of these five fits?* — and every rule is a thing you **see**:
*the doubles are all next to each other · every double is at an end · all the doubles are the same
number · the number at the left end is on every domino · that number is nowhere else · all the 4s
are on one domino · the biggest and the smallest number are on the same domino · the two end numbers
sit together on one domino · the right-hand numbers never go down · the dominoes take turns which
way up.* Read them aloud: each is one breath, and each can be checked on a five-domino line with a
finger in about three seconds. Nothing in the class counts pips or adds anything up — the two
"counting" rules a kid ever meets are "exactly two doubles" and "exactly one blank", counted on one
hand — and the one thing every child *expects* a domino rule to be, the chain, is deliberately the
trap that the wrong answers satisfy.
