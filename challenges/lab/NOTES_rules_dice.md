# NOTES — rule-family class, world = a roll of 3–5 dice  (class `borsel`)

Paradigm: `docs/RULE_FAMILIES.md`. The clue is a set of positive example rolls that pins one
rule inside a private universe U; the answer is one more roll obeying that rule. The player does
not know U, so their (larger) hypothesis space contains obvious rules the class **never** uses.
Learning what the class never says is the game.

## World / format decisions

| decision | choice | why |
|---|---|---|
| instance | a roll of **k dice**, pips 1–6, written `4 2 6 1` | the most kid-evocable random object there is; one line each |
| k | drawn per clue from {3,4,4,5,5}; **fixed inside a clue** | the clue's line width tells the player the answer's width — the demo economy is satisfied by the clue alone |
| dice order | **shuffled** in every example, and in `solve()`'s answer | keeps every rule order-independent and makes "the dice are in order" an occasional (8%) accidental trap rather than a permanent one |
| answer | one more roll of k dice | `not` a re-ordering of an example: the scorer compares **sorted multisets**, so `copy an example` and `copy an example shuffled` both score 0 |
| pips vs ASCII faces | pips (digits) | 5 dice as ASCII faces is 5 lines per roll; digits keep 3 examples inside 29 characters and stay legible |

## The universe U — 11 templates, 26 concrete rules (k=3) / 27 (k=4, k=5)

`d` = the roll sorted ascending, `S` = total, `M` = biggest, `m` = smallest.
"density" = probability that a uniformly random roll of k dice satisfies the rule = **the score of
a player who answers at random when this rule is the truth**. Every parameter value was chosen to
keep that between 0.02 and 0.17 (mean 0.10); the dense members of every family were cut.

| # | kid sentence | parameter grid | density k=3 / 4 / 5 | IN? |
|---|---|---|---|---|
| 0 | "the dice add up to **n**" | n ∈ {3k−2, 3k, 3k+2, 3k+4} | .069–.125 / .062–.113 / .054–.100 | IN |
| 1 | "the dice add up to **more than n**" | n = 4k+2 (one threshold only) | .093 / .097 / .098 | IN |
| 2 | "the dice add up to **less than n**" | n = 3k−2 (one threshold only) | .093 / .097 / .098 | IN |
| 3 | "the **biggest** die is a **m**" | m ∈ {3,4} | .088,.171 / .050,.135 / .027,.100 | IN |
| 4 | "the **smallest** die is a **m**" | m ∈ {3,4} | .171,.088 / .135,.050 / .100,.027 | IN |
| 5 | "**exactly two** of the dice are **v**s" | v ∈ 1..6 | .069 / .116 / .161 | IN |
| 6 | "there are exactly **i** different numbers" (i=1 → "all the dice are the same") | i ∈ 1..min(k−2,2) | .028 / .005,.162 / .001,.058 | IN |
| 7 | "the **two biggest** add up to **s**" | s ∈ {k+3, k+4} | .088,.125 / .083,.132 / .100,.154 | IN |
| 8 | "the **two smallest** add up to **s**" | s ∈ {10−k, 11−k} | .125,.088 / .132,.083 / .154,.100 | IN |
| 9 | "the biggest die is **double** the smallest" | — | .167 / .134 / .100 | IN |
| 10 | "the **biggest and the smallest** add up to **n**" | n ∈ {4,5,9,10} | .060–.111 / .039–.096 / .023–.077 | IN |

`generate()` draws the **template** uniformly first and only then a parameter, so no template is
rare because it happens to have fewer parameters (before this fix, "exactly two v's" was 26 % of
all clues and a player who knew only that one template scored 43 %).

### Why U is an antichain (why uniqueness is possible at all)
Positive examples can never separate a rule from a **weaker** rule that contains it: if A ⊆ B and A
is the truth, B survives too. So no rule of U may imply another. This killed several first drafts:
* "the total is a multiple of y" (y ∈ 3,4,5) — swallows every `sum == n` with y | n; also too dense
  (.20–.33). Dropped, along with `multiple of 7` (.14) and `multiple of 8` (.125, swallows sum=16).
* "biggest − smallest = 1" ⊂ "exactly 2 different numbers" (a range of 1 always means two values).
* "two dice add up to 11" ⊂ "the biggest die is a 6"; "exactly 4 different numbers" (k=5) ⊂ "two
  dice add up to seven" (4 values out of 3 complementary pairs must contain a whole pair).
* "exactly c dice show m or more" — every member with 0 < c < k except a few extreme corners is
  either dense (.22–.44) or a restatement of "all ≥ m" / "all ≤ m", which are excluded (below).
  Replaced by template 5, "exactly two dice show v", which is the same idea at density .07–.16.
* Sum thresholds are monotone, so U may contain **one** "more than" and **one** "less than" only.
Checked by brute force over all multisets for k=3,4,5: no rule of the final U is contained in
another, and every rule has ≥ 5 satisfying rolls (needed so a 2–3-example clue still leaves the
player at least two possible answers).

### Templates considered and thrown out for being too generous (density in brackets)
"exactly c of the dice are odd" [.25–.375] · "two of the dice add up to seven" [.42/.64/.80] ·
"no two dice are next to each other" [.42/.22/.12] · "three of them are in a row" [.11/.28/.45] ·
"exactly one die is a v" [.35/.39/.40] · "biggest − smallest = g" [.14–.34] · "the middle die is m"
[.19–.29] · "the two biggest are the same" [.24/.31/.37] · "the biggest is three times the
smallest" [.17/.19/.19] · "all the dice are within one of each other" [.17/.06/.02, and wildly
k-dependent]. Several of these come back as **excluded** rules — they are exactly what a first-time
player reaches for, and being dense they fit the examples often.

## The exclusions (never the rule; frequently consistent with the examples)

Measured over 500 fresh clues: **fits** = the excluded rule is consistent with every example in the
clue (the trap fires); **score** = what a player who always answers with an instance of that rule
scores overall.

| excluded rule | why a player tries it | fits | score |
|---|---|---|---|
| X2 "every die is at least m" (m = smallest pip in the clue) | the loose cousin of "the smallest die is m" | **100 %** | 22.6 % |
| X3 "no die is bigger than m" (m = biggest pip seen) | the loose cousin of "the biggest die is m" | **100 %** | 20.4 % |
| X5 "the total is odd / even" | implied by every `sum == n` clue | 43 % | 12.4 % |
| X7 "exactly c of the dice are odd" | the classic first dice hypothesis | 20 % | 10.4 % |
| X8 "two of the dice add up to seven" | *the* famous dice fact | 18 % | 8.0 % |
| X6 "there is a six" | "what do the examples have in common?" | 12 % | 7.2 % |
| X10 "the dice are in increasing order" | the examples are printed unsorted, but sometimes look sorted | 8 % | 9.8 % |
| X4 "all odd / all even" | ditto | 6 % | 1.4 % |
| X9 "three of them are in a row" | run-spotting | 3 % | 13.0 % |
| X1 "all the dice are different" | the most obvious Zendo rule of all | 1 % | 3.8 % |

The class's real secret is a **convention**, not a single rule: it only ever makes **tight**
statements (*exactly* n, *exactly* two v's, the biggest *is* 4) and never loose ones (at least,
at most, all odd, contains a six). X2 and X3 are consistent with 100 % of clues by construction —
a player who answers "anything within the range I have seen" is never contradicted by the clue and
still scores only ~21 %. X1's trap rate is low for an interesting reason: an all-different roll is
a weak discriminator, so the minimal example sets the generator finds almost always contain a
repeat.

## Generator

1. draw k ∈ {3,4,4,5,5}; build (cached) the 56/126/252 multisets and, for each, the bitmask of
   the rules of U it satisfies;
2. draw a template uniformly, then a parameter uniformly, then its satisfying set A (|A| ≥ 5);
3. search 40 random triples of A for a **minimal identifying set of 3**: the three together leave
   exactly one rule of U alive, and no two of them do; if none is found, search 40 random pairs
   for a minimal pair;
4. require |A| ≥ #examples + 2 so the answer is never forced;
5. print each example with its dice shuffled, one per line.

Measured: 43 % of clues carry 3 examples, 57 % carry 2 (k=3 is almost always 2 — with 56 possible
rolls two examples nearly always pin the rule; k=4/5 are about half and half). Mean 0.066 ms.

`solve()` re-derives the survivor exactly as the scorer does, enumerates every roll satisfying it,
drops the examples and returns a **uniformly random** one in random dice order (26 % of its answers
happen to come out sorted — it never emits a canonical or minimal witness).

`score()` (653 chars, needs `max_score_code_chars = 1024`, the raise `RULE_FAMILIES.md` §4 allows
for this paradigm) parses the example lines, rebuilds U from k alone, filters, insists on a single
survivor, and checks the answer is a fresh well-formed roll obeying it. No hidden channel.

---

## 2026-09-05 — revision 2: the LINEUP answer (`borsel` v2; v1 kept as `borsel.v1.json`)

`docs/RULE_FAMILIES.md` "Revision 2". v1 was cracked without a rule ever being named: dornic1b kept
every predicate of a 226-strong dice pool that was true of all the examples and emitted a roll
satisfying all of them at once (58 %), and the only thing that ever held them was the invisible
"not a re-ordering of an example" clause (0/10 → 25/40 the moment they guessed it). So the answer
stops being a construction and becomes a **choice**.

### What changed

| | v1 | v2 |
|---|---|---|
| clue | 2–3 example rolls | the same examples, a blank line, then **4 candidate rolls** of the same k |
| answer | any fresh roll obeying the rule | the **one candidate** that obeys it, verbatim (any dice order) or its index 1–4 |
| freshness clause | "not a re-ordering of an example" | **gone** (rev. 2 §5) |
| floor | ~10 % (a random roll) | 25 % |
| example search | minimal identifying triple, else pair | **unchanged**, plus up to 4 example sets per rule |
| U | 11 templates, 26–27 rules | **unchanged** (still the same antichain) |
| score | 653 chars | 763 chars (still under the 1024 the paradigm may use) |

### The demotion (the tavrik lesson)

The trap set now contains the two **total brackets** — "the total is at least the smallest total in
the clue" and "at most the biggest one". When the hidden rule is template 0, *the dice add up to
exactly n*, every example has total n, so those two loose cousins bracket the rule **exactly**:
their conjunction IS the rule, and a decoy firing the same traps as the truth would have to satisfy
the rule. Template 0 is therefore **demoted to competitor-only** — it stays in U, the examples must
still kill it, but it is never the hidden rule. Ten of the eleven templates remain eligible, coming
up 37–67 times per 500 clues (template 5 is unusable at k = 3: only 5 rolls of three dice show
exactly two v's).

Every other template survives the check because the remaining brackets are **one-sided on their own
readout**: "every die is at least a" bounds the minimum from below only, "no die is bigger than b"
the maximum from above only, so *the smallest die is 4* and *the biggest die is 3* are not
reconstructible from the traps. Templates 1 and 2 (the two sum thresholds) survive but are fussy:
the truth has to sit outside the examples' total range, which is why they need the four-example-sets
retry to stay as common as the rest.

### Matched trap profiles (rev. 2 §5b)

All four candidates fire **exactly the same** set of example-consistent excluded rules — asserted
over 500 clues; every trap is satisfied by all four or by none. Thirteen excluded rules are tested:

| excluded rule | fires | pick-by-it score |
|---|---|---|
| every die is at least a | 100 % | 26.6 % |
| no die is bigger than b | 100 % | 24.8 % |
| the total is at least s | 100 % | 26.2 % |
| the total is at most s | 100 % | 24.6 % |
| two dice show the same number | 89 % | 27.3 % |
| the total is even / odd | 42 % | 21.5 % |
| exactly c of the dice are odd | 16 % | 28.0 % |
| two of them add up to seven | 16 % | 17.3 % |
| there is a six | 12 % | 22.4 % |
| all odd | 3 % | 33.3 % |
| all even | 2 % | 0.0 % |
| three of them are in a row | 1 % | 14.3 % |
| all the dice are different | 0.4 % | 0.0 % |

(The small-sample rows are 3–15 clues each.) The order-dependent v1 trap "the dice are in increasing
order" is dropped: every roll, example or candidate, is printed in a random order, so it is noise for
all four alike.

### Beating the count attack (rev. 2 §2 and §5c)

The generator carries dornic1b's own pool, rebuilt from their `zpools.py` — the 173 **order-free**
predicates of it (totals, divisors, per-pip has/none/max/min/count, distinct counts, ranges,
parities, runs, products); their order-sensitive predicates are noise here because the dice are
shuffled on every line. Each predicate is weighted by −log2 of its base rate under a uniform roll,
bucketed 1–7, so a candidate's rarity-weighted score is seven big-int ANDs.

The surprise: with matched trap profiles, in **~42 %** of clues *no* decoy can reach the true
candidate's score at all (the hidden rule's own predicates are in the surviving set and only the
truth satisfies them). Aiming the truth's rank uniformly at 0–3, as tresk does, therefore leaves
"pick the biggest score" at 38 %. Aiming at **1–3** instead — take the best reachable when 1 is
already out of reach — flattens both ends: 29 % for the argmax and 24 % for the argmin. Within that
split the truth is also placed at a randomly aimed rank on the plain count and on "closest total to
the examples' totals". A decoy beats the truth on the attacker's count in **62 %** of clues.

### Witness table, 500 fresh clues (attacker pool = the real 226 borsel predicates)

| witness | score |
|---|---|
| pick candidate 1 | 24.8 % |
| pick a random candidate | 26.4 % |
| the candidate satisfying the **most** attacker predicates | **29.2 %** (target ≤ 60 %) |
| the candidate satisfying the **fewest** | 23.6 % |
| rarity-weighted intersection (§5c) | 39.0 % |
| closest total to the examples' totals | 39.2 % (v1's best cheap heuristic scored 35 %) |
| the in-U intersection | **100 %** |
| pick by each excluded rule | 17–28 %, mean 25 % |
| knows U minus its two rarest templates | 88.0 % |
| the true rule | **100 %** |

The two cheap heuristics still above chance — the rarity-weighted intersection and "closest total" —
are the same pair dornic v2 reports (47 % there). They are the price of a world whose readouts are
all arithmetic on the same five numbers; a two-step readout would blunt them further, but there is no
two-step readout of a dice roll that stays a one-breath kid sentence.

### Measurements

3000 clues: mean generate **0.31 ms** (p50 0.26, p95 0.65, max 1.4), no fallback ever used; 57 % two
examples / 43 % three (unchanged from v1); k = 3/4/5 in 16/40/44 % of clues; clue ≤ 70 chars; answer
≤ 9 chars; the correct candidate is uniform over positions 1–4 (751/745/732/772). `solve` returns the
obeying candidate line verbatim — with a lineup there is nothing to vary and nothing to leak.
`score` is 763 chars, accepts the candidate in any dice order or its 1-based index, insists on a
single surviving rule of U, and returns 1 iff the chosen candidate obeys it.
`python tools/quickcheck.py challenges/lab/borsel.json --seeds 300` → OK.

### Three demos (the clue exactly as the player sees it, then the answer)

```
3 2 3 2                 1 4 2 5 2               6 5 4 6 5
2 2 3 2                 5 4 4 1 4               5 4 5 5 4
1 2 3 3                                         5 4 4 4 5
                        4 3 3 6 2
1 1 1 1                 5 2 1 6 2               5 6 6 5 5
1 1 2 1                 1 2 3 6 2               6 6 6 6 6
1 3 3 1                 4 6 1 1 4               5 5 6 6 6
2 2 2 2                                         4 6 6 6 6
```
| answer | candidate | the hidden rule |
|---|---|---|
| `1 3 3 1` | 3 | the biggest die is a 3 |
| `1 2 3 6 2` | 3 | the two biggest add up to 9 |
| `4 6 6 6 6` | 4 | the smallest die is a 4 |

(Each column above is one whole clue: the examples, a blank line, the four candidates. In the first
one all four candidates fire exactly the same traps — every die at least 1, no die bigger than 3,
total at most 10, two dice the same — and none of them fires "the total is at least 9".)

### Predicted classification

**Hard but crackable — the intended band.** The floor is 25 % and every cheap statistic sits between
24 % and 39 %; a player who reconstructs U scores 100 % and one who is two templates short scores
88 %. An Opus centaur team with 3 demo requests and a few hundred clues of 0/1 feedback should land
around **45–60 %**: the rarity-weighted intersection alone gives ~39 %, and each template they name
adds roughly its 4–13 % share of the clues. That is the "cracked about half the time" target.
