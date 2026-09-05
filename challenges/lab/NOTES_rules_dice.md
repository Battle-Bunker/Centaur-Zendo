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
