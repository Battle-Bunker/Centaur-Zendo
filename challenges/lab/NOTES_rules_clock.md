# NOTES — rule-family class, world = a clock time `h:mm` (class `wisbek`)

Paradigm: `docs/RULE_FAMILIES.md`. A finite universe **U** of parametrised rules; the clue is a
minimal set of positive example times that pins exactly one rule inside U; the answer is one more
time obeying it. The player does **not** know U, so their larger hypothesis space contains obvious
rules the class never uses. Learning **what this class never says about a clock** is the game.

Shipped file: `challenges/lab/wisbek.json` (name checked unique against `challenges/` and
`challenges/lab/`). Not committed; no arena run (out of scope for this job).

> **Superseded on 2026-09-05, twice — read the two dated records at the end of this file first.**
> Everything below describes v1 (`challenges/lab/wisbek.v1.json`), whose answer was a freshly
> constructed time at an hour not in the clue. **v2** (`challenges/lab/wisbek.v2.json`) kept the
> universe U, the example sets and the exclusions unchanged and replaced the answer with a choice
> among four candidates. **v3** (the shipped `challenges/lab/wisbek.json`, §§9–17) throws the
> universe away: every rule of v1/v2's U turned out to be a cheap predicate in the players' own
> feature banks (Jaccard 1.00, all 66 of them), so U is now a set of RELATIONS between the two hands
> or between two places of the written time, the lineup is five candidates, and the clue is always a
> pair of examples.

---

## 1. The world

One time per line, 12-hour clock, written `h:mm` — `7:45`, `10:05`, `12:00`. Hours 1–12 with no
leading zero, minutes always two digits. **720 possible times**, small enough to brute-force every
rule's satisfying set exactly and to check the antichain condition by hand.

There is **no am/pm**, so "all in the morning" is not even expressible — a first-time player's most
reflexive time hypothesis is off the board before it starts. (Recorded as a finding, not a trap: it
never fires because it cannot be written.)

**The examples in a clue always have different hours, and the answer must use an hour that is not in
the clue.** That is the one well-formedness convention and the most important design decision in the
class (§5). It is *visible in the clue* — two or three lines, never two with the same hour — and a
demo confirms it in one look.

### Readouts the class measures (exactly what the scorer computes)
```
h                       the hour, 1..12
m                       the minutes, 0..59
m//10 + m%10            the minute digit sum
(h if h<10 else h-9)    the hour digit sum   (10, 11, 12 -> 1, 2, 3)
(m - 5*h) % 60          how far past the hour NUMBER the minute hand points, in minutes
                        (divide by 5 to get "how many clock numbers past")
```

---

## 2. The universe U — 10 templates, 66 concrete rules

"density" = probability that a uniformly random one of the 720 times satisfies the rule — i.e. what
a player who answers at random scores when that rule is the truth. **R?** = may be the hidden rule;
a rule is eligible only if its density is ≤ 0.11. The rest stay in U as **competitors** the
generator has to kill.

| # | template (the kid sentence) | parameter grid | density | R? |
|---|---|---|---|---|
| 0 | "the minute digits add up to *n*" | n = 3…12 | .067 → .100 → .050 | all (mean .085) |
| 1 | "the minutes are in the *n* times table" | n = 7, 8, 11, 12 | .150 / .133 / .100 / .083 | **11, 12 only** |
| 2 | "the minute hand points at an **even** / an **odd** number" | 2 rules | .100 each | both |
| 3 | "the minute hand points ***n* numbers past** the hour number" | n = 0,1,2,4,5,6,7,8,10,11 | .0167 each | all |
| 4 | "the hands make a **square corner**" (`(m-5h)%30==15`, i.e. n = 3 or 9 in one rule) | — | .033 | yes |
| 5 | "the minutes are ***n* times** the hour" | n = 1,2,3,4 | .0167 each | all |
| 6 | "the hour and the minutes **add up to *n***" | n = 15,20,…,60 | .0167 each | all |
| 7 | "**all the digits** add up to *n*" | n = 7…16 | .061 → .089 → .050 | all (mean .074) |
| 8 | "the minutes are ***n* more** than the hour" | n = 5,10,…,45 | .0167 each | all |
| 9 | "the minutes are in the ***n*-tens**" (`m//10 == n`) | n = 0…5 | .167 each | — competitor |

|U| = 66, of which **58 are eligible**. Mean density of the hidden rule, measured over 500 clues:
**0.048** — the floor a thoughtless player gets, and the number the eligibility ceiling controls.

Two rules of template 3 have famous names: **n = 0 is "the two hands point at the same number"**
(1:05, 5:25, 12:00) and **n = 6 is "the hands point at opposite numbers"** (1:35, 5:55, 12:30).

`generate()` draws the **template uniformly first** and only then a parameter, so no template is
rare merely because it owns fewer rules. Measured mix over 500 clues: 5:69, 3:64, 0:64, 1:63, 6:63,
4:48, 7:46, 8:45, 2:38 (template 2 is under-represented because it owns only two rules and often
fails the minimality search).

### Why 8 loose rules stay in U as competitors
The six minute-decade rules ("the minutes are in the twenties") at density .167, and the two loose
times-table rules (7 and 8) at .150 / .133, are too generous to be an answer. Leaving them **in U**
means the generator must kill them, which forces the clue to do layout work for free: the decade
rules can only die if the examples' minutes are spread across the decades, and the loose times-table
rules can only die if the examples are not all multiples of 7 or 8. Same trick as dornic's "exactly
*n* cards" and tresk's length rules.

### Why U is an antichain (why uniqueness is possible at all)
Positive examples can never separate a rule from a **weaker** rule containing it: if A ⊆ B and A is
the truth, B survives too, forever. Brute-forced over all 720 times: **no rule of the final U
contains another** (0 violations). Casualties of that check — and they are the interesting ones,
because they are exactly the templates the brief suggested:

* **"it is *n* minutes past the hour" / "it is quarter past" / "half past" / "quarter to" /
  "the minute hand points straight up / down / left / right".** An exact minute value is the most
  specific statement there is, so it sits *inside* the minute digit-sum rule, inside a times-table
  rule whenever the value divides, and always inside a decade rule. Every one of them is
  structurally unpinnable in an antichain that contains any looser minute property. **They became
  exclusions instead** — and "o'clock / quarter past / half past / quarter to" is now the single
  most obvious wrong hypothesis a player can hold about a clock class.
* **"the hands are exactly on top of each other" / "exactly opposite" / "exactly a right angle".**
  On a whole-minute clock the hour hand sits at 30h + m/2 degrees, so the gap is |30h − 5.5m|, and
  5.5m is a multiple of 0.5 — the equations 30h − 5.5m ≡ 0, 180, ±90 (mod 360) have integer-minute
  solutions only at **12:00** and **6:00**. A rule with one or two instances cannot support a
  2–3-example clue plus a fresh answer. Replaced by the *clock-face* versions (templates 3 and 4),
  which say where the minute hand points **relative to the hour number** — exact, integer, 12 or 24
  instances each, and a kid can read them straight off a drawn face.
* **"the minutes are the same as the hour"** (`m == h`, template 5 n = 1) forced out
  **"the hour digits add up to the same as the minute digits"**: the second contains the first
  (1:01, 10:10, 11:11, 12:12 all have equal digit sums), so one of them had to go. Kept the kid
  sentence, dropped the clever one.
* **"the minute hand points at twice the hour number"** (`m = 5·(2h mod 12)`) ⊂ "the minute hand
  points at an **even** number" — twice anything is even. Cut.
* **"the minutes are a multiple of 9"** ⊃ "the minute digits add up to 9" (the non-zero multiples of
  9 under 60 are exactly the two-digit-sum-9 minutes), and **"multiple of 11" ≡ "the two minute
  digits are the same"** — the same set under two names. Kept 11 in the times-table template and
  describe it to the organiser as "the minute digits match"; dropped 9 in favour of the digit sum.
* **"the minutes are less than 30" / "more than 30"**, and every other half-of-the-hour split,
  contains `m = h` and `m = 2h` outright (their minutes never reach 30). Loose comparisons are
  exclusions here, not competitors.
* **"the minutes end in *n*"** (`m%10 == n`) as a competitor family would have contained both of
  template 2's rules (the even-number positions all end in 0, the odd ones all end in 5). Dropped;
  the decade competitor does the same layout job without the collision.

### Templates considered and thrown out for being too generous (density in brackets)
"the hour is odd / even" [.50] · "the minutes are odd / even" [.50] · "the minutes are bigger than
the hour" [.88] · "it is between *h1* and *h2* o'clock" [.17–.75] · "the minutes end in 0 or 5"
[.20] · "the hour goes exactly into the minutes" [.26] · "both hands are in the same half of the
face" [.50] · "all the digits are different" [.62] · "the hour's digit shows up in the minutes"
[.20, and wildly h-dependent]. Every one of these comes back below as an **exclusion** — being dense
is exactly what makes a good trap.

Also cut for not being one breath: "the time reads the same backwards" (only 10:01, 11:11, 12:21 —
three instances, and only two-digit hours can ever qualify), "the hours and minutes use the same
digits", "the minutes are the hour written twice".

---

## 3. The exclusions (never in U; frequently consistent with the examples)

Over 500 fresh clues: **fits** = the excluded rule is consistent with *every* example (the trap
fires); **score** = what a player who always answers with an instance of it scores, built at a legal
(fresh) hour — i.e. the ceiling of that hypothesis for a player who has already found the hour
convention.

| excluded rule | why a player tries it | fits | score |
|---|---|---|---|
| "the minutes stay between the smallest and the largest minute in the clue" | the **loose cousin** of every minute rule | **100 %** | 8.0 % |
| "the hour stays between the smallest and the largest hour in the clue" | the loose cousin of "the hour is *n*"; "it's a morning/afternoon class" | **100 %** | 4.8 % |
| "the minutes are bigger than the hour" | the first comparison anyone makes between the two numbers | 69.8 % | 3.6 % |
| "it is in the same half of the hour as the examples" (`m<30` / `m≥30`) | before / after half past is how a kid reads a clock | 50.6 % | 5.2 % |
| "the minutes are all even / all odd" | the classic parity hypothesis | 42.2 % | 5.4 % |
| "the minutes end in 0 or 5" (the minute hand points straight at a number) | *the* most obvious clock hypothesis | 30.8 % | 10.0 % |
| "all the digits in the time are different" | the most obvious Zendo rule of all | 26.6 % | 4.0 % |
| "the hour is odd / even" | ditto, on the other number | 26.2 % | 4.2 % |
| "the hour divides exactly into the minutes" | the loose cousin of "the minutes are *n* times the hour" | 23.4 % | 8.0 % |
| "both hands are in the same half of the face" | the geometric hypothesis | 15.0 % | 5.0 % |
| "it is o'clock, quarter past, half past or quarter to" | the four times every kid can name | **0.4 %** | 10.4 % |

The class's secret is a **convention**, not a single rule: it only ever makes **tight** statements
(the digits add up to exactly *n*, the minute hand is exactly *n* numbers past the hour number, the
minutes are exactly three times the hour) and never loose ones (bigger than, at least, odd, even,
morning, between two o'clocks, on a five). The two 100 %-consistent traps are the loose cousins of
its own readouts — a player who answers "anything inside the range I have seen" is never
contradicted by the clue and still scores only 5–8 %.

**On average 4.9 excluded rules also fit every example of a clue.** So a player whose universe is U
*plus* the obvious extras faces ~5.9 survivors: picking one uniformly scores **25.6 %** (that
includes the ~1-in-6 chance of picking the truth), and picking a **wrong** one scores **8.2 %**.
That is the intended failure mode, and the only way out is to notice which *kinds* of statement this
class never makes.

Two honest findings about weak traps:
* **"o'clock / quarter past / half past / quarter to" fires on only 0.4 % of clues** — a minimal
  identifying example set almost never consists entirely of quarter times, because a strong "every
  example is…" property is a weak discriminator (it leaves the decade and times-table competitors
  alive). Same self-excluding effect dornic found for "all one suit" and tresk for "it alternates".
  Its *score* (10.4 %) is nevertheless one of the highest, because quarter times satisfy several
  eligible rules at once (template 2, template 3, template 4).
* **"the same hour as an example" is not merely never the rule — the well-formedness clause makes it
  actively wrong** (score 0). It is the cheapest lesson in the class and the first one a player
  learns from 0/1 feedback.

---

## 4. Three demos

```
CLUE                  ANSWER          hidden rule (private)
2:35
7:00       ->         1:30            the minute hand points 5 numbers past the hour number
8:05

3:38
7:42       ->         2:37            the minutes are 35 more than the hour

1:37
4:55       ->         11:37           the minute digits add up to 10
```
(seeds 4, 17, 31, answers straight from `solve`. Note every clue shows different hours and every
answer a fresh one — and that the third answer happily **reuses** an example's minutes, which is
legal and is exactly the 35 % foothold in action.)

---

## 5. The design decision that made the class: a fresh hour

Every readout in U except the hour itself is a smooth function of the minutes, so the demo-less
probe "echo a clue line with a tweak" would crack the class outright (DESIGN_LOOP lever 8) if the
answer only had to be well formed and different from the examples. Three candidate clauses were
measured over the same 500 clues:

| witness | no clause | **fresh hour** (shipped) | fresh hour **and** fresh minutes |
|---|---|---|---|
| copy an example verbatim | — (0 by "not an example") | **0.0 %** | 0.0 % |
| copy an example, one digit changed | ~50 % | **9.6 %** (only 33 % well formed) | 0.0 % |
| the same hour as an example, different minutes | ~35 % | **0.0 %** | 0.0 % |
| the same minutes as an example, a fresh hour | ~35 % | **34.8 %** | 0.0 % |
| a random well-formed time | 4.8 % | **5.0 %** | 2.2 % |
| commonest single U-rule (square corner), blind | 16 % | **16.6 %** | 14.8 % |

**Fresh hour** was chosen. It costs *fewer* scorer characters than the clause it replaces
(`any(h==e[0] for e in E)` does the "not one of the examples" job too), it is honest and visible
(the clue never repeats an hour), and it splits the copy-edit family cleanly in two: the two thirds
of one-digit edits that keep the hour are **not even well formed**, while "keep the minutes, move to
a new hour" survives at **34.8 %** — the foothold, and it pays exactly when the hidden rule is one
of the three minute-only templates (0, 1, 2), which is 3 of the 9 eligible templates.

**Fresh hour + fresh minutes** was rejected even though it zeroes every copy-edit witness: it flattens
the class to a 2 % floor with no graded probe between "random" and "knows the rule", which is the
failure mode DESIGN_LOOP lever 7 warns about — Opus players conclude the grader is exact-match and
farm demos instead. The shipped clause leaves a clean ladder: **0 % → 5 % → 35 % → 100 %**.

---

## 6. Witness table — 500 fresh clues (seeds 1 000 000–1 000 499)

| witness | score | well-formed |
|---|---|---|
| copy an example verbatim | 0.0 % | 0 % (the hour is reused) |
| copy an example with one digit changed | 9.6 % | 32.8 % |
| the same hour as an example, different minutes | 0.0 % | 0 % |
| **the same minutes as an example, at a fresh hour** | **34.8 %** | 100 % |
| an example's minutes ±1, at a fresh hour | 2.6 % | 100 % |
| a random well-formed time (fresh hour) | 5.0 % | 100 % |
| a random time at any hour | 3.6 % | 81.2 % |
| an instance of the commonest single U-rule (square corner), ignoring the clue | 16.6 % | 100 % |
| an instance of a commonest-template rule (minute digits add to 7), ignoring the clue | 1.2 % | 100 % |
| EXCLUDED: minutes inside the clue's minute range | 8.0 % | 100 % |
| EXCLUDED: hour inside the clue's hour range | 4.8 % | 87.6 % |
| EXCLUDED: the minutes end in 0 or 5 | 10.0 % | 100 % |
| EXCLUDED: o'clock / quarter past / half past / quarter to | 10.4 % | 100 % |
| EXCLUDED: the hour divides exactly into the minutes | 8.0 % | 100 % |
| EXCLUDED: the minutes are all even / all odd | 5.4 % | 100 % |
| EXCLUDED: same half of the hour as the examples | 5.2 % | 100 % |
| EXCLUDED: both hands in the same half of the face | 5.0 % | 100 % |
| EXCLUDED: the hour is odd / even | 4.2 % | 100 % |
| EXCLUDED: all the digits are different | 4.0 % | 100 % |
| EXCLUDED: the minutes are bigger than the hour | 3.6 % | 100 % |
| **player who has mapped U perfectly** | **100.0 %** | 100 % |
| player who has mapped U minus its 2 rarest templates (2 and 8) | 84.2 % | 100 % |
| player whose universe is U + the excluded rules, picking a survivor uniformly | 25.6 % | 100 % |
| … the same player, conditioned on picking a **wrong** (excluded) survivor | 8.2 % | 100 % |
| player who knows U but filters on all-but-one example and picks a random survivor | 61.6 % | 100 % |
| the true rule (`solve`) | 100.0 % | 100 % |

Notes on the partial-knowledge rows:
* **U minus two templates**: removing rules can only shrink the survivor set, so this player never
  faces ambiguity — on the 83.4 % of clues whose truth is elsewhere they still get exactly one
  survivor and score 1; on the other 16.6 % they get **zero** survivors and are left guessing (~5 %).
* **Filters on all but one example**: minimality guarantees ≥ 2 survivors when an example is dropped,
  but usually exactly 2, so a coin flip lands on the truth about half the time — 61.6 %. This is the
  one genuinely soft edge of the class, and it only pays a player who has already reconstructed U.

Other measured numbers (500 clues unless stated):
* **Example-count distribution** (2000 seeds): 2 → 47.1 %, 3 → 52.9 % (4 → 0 %; the generator tries
  a minimal 3-set first and falls back to a minimal pair — for the tight templates two examples
  almost always already pin the rule, which is why a *minimal* triple is impossible there).
* **Uniqueness** (exactly one U-rule consistent with all examples): 500 / 500.
* **Minimality** (dropping any one example leaves ≥ 2 consistent rules): 500 / 500.
* **All example hours distinct**: 500 / 500.
* At least 3 satisfying times remain at unused hours on every clue (the answer is never forced).
* Mean density of the hidden rule: **0.048**.

---

## 7. Validation

`python tools/quickcheck.py challenges/lab/wisbek.json --seeds 300`
→ `OK wisbek  gen=0.88ms score=0.19ms solve=0.25ms`, **no warnings**.

| quantity | value | cap |
|---|---|---|
| `score` source | **895 chars** | 1024 (the SPEC default since 2026-09-05; picture classes still aim ≤ 512) |
| `generate` source | 4785 | 50 000 |
| `solve` source | 1278 | 5 000 |
| `generate` | **0.354 ms mean**, 1.36 ms max over 2000 seeds | 100 ms |
| `score` | 0.054 ms max on junk (`""`, `"x"`, `"1"*100`, `"9"*4000`, the clue itself, `"12:60"`, `"13:05"`, unicode digits) | 50 ms |
| `solve` | 0.25 ms max | 2000 ms |
| clue | ≤ 17 chars | 1024 |
| answer | ≤ 5 chars | 1024 |

`generate` is fast because the 720-time table, each time's 66-bit "which rules do I satisfy" mask,
and each rule's hour→times index are built **at module level** (~60 ms, once per worker, not charged
to `max_generate_ms`); a call is then a handful of integer ANDs. `score` was checked to agree with
the reference predicate on **all 720 times × 200 clues** (0 disagreements) and rejects `0:30`,
`13:05`, `12:60`, `7:5`, multi-line input and unicode digits; it forgives surrounding whitespace and
a leading zero on the hour.

`solve` re-derives the survivor exactly as the scorer does and returns a **uniformly random** valid
time at a random unused hour — never the canonical or minimal witness.

---

## 8. Predicted classification

**Testing / low calibrated, leaning slightly easy of tresk.** Prediction for two Opus players in a
7-class pool (4 rounds, ~60 probes per class per round, 3 demos for 7 classes):

* **Without a demo**: the clue's shape is self-evident — three short times, so send another time.
  Attempts are well formed from round 1. Copying a clue line scores 0 every time; within ~20 probes
  the 0/1 channel says "the hour must be new", and from there "keep the minutes, change the hour"
  pays **34.8 %**. Expect **15–35 %**, mostly from that one probe.
* **With a demo**: the demo shows a fresh hour immediately (and often reused minutes, which teaches
  the convention precisely: *hour* fresh, *minutes* free). Cracking it outright needs the player to
  reconstruct enough of U to filter — 10 templates, 66 rules, three of them clock-face geometry
  nobody enumerates by default — from ~120 probes and two or three example times. Expect
  **45–70 %**.

Mean across the two ≈ **0.35–0.5**, i.e. `calibrated`, with the risk on the *easy* side because the
34.8 % foothold is cheap and self-teaching. Levers if it comes back too easy, in order:
(i) tighten the eligibility ceiling from 0.11 to 0.09, which drops the three minute-only templates'
loosest members and pulls the foothold below 30 %;
(ii) add a second competitor family that forces the examples to disagree about the minute digit sum,
which makes template 0 harder to pin;
(iii) switch to fresh-hour **and** fresh-minutes, which zeroes the foothold entirely (measured in
§5) — but that is a cliff, not a step, and should be a last resort.
If it comes back too hard: always emit three examples instead of 53 % (more information, same
minimality), and raise the ceiling to 0.13 so the loose times-table rules become answerable.

**12-year-old test**: the object is a clock — a kid names it from one look at `7:45`, no demo needed,
and every rule is one breath said over a drawn face: *"the two hands point at the same number"*,
*"the hands make a square corner"*, *"the minutes are three times the hour"*, *"the minute digits add
up to ten"*, *"the hour and the minutes add up to forty-five"*. A kid can test any of them by hand on
two short times, and is *better* placed than an adult to notice the lesson — this class never says
"before", "after", "odd", "even", "morning" or "on a five"; it only ever says *exactly*. The
nameable-pattern risk is real (these are all nameable rules) but the difficulty lives in the size of
U, the loose-cousin traps and the thin 0/1 channel, not in any single rule being obscure.

---

# 2026-09-05 — v2: the lineup answer

`challenges/lab/wisbek.json` is now the lineup version; v1 is kept byte-identical as
`challenges/lab/wisbek.v1.json`. Written for `docs/RULE_FAMILIES.md` **"Revision 2: the lineup
answer"**. No arena run from this job.

## 1. Why v1 had to change

Both Opus teams in `lad-dornic-v1-1` took **no demo** on wisbek and still scored **95 %**
(dornic1b: 222/234). Their method (`sim/results/lad-dornic-v1-1/players/dornic1b/strategy.py`,
pool in `zpools.py::wisbek_preds`, 307 predicates over `(h, m)`):

1. keep every predicate of the pool that is true of **all** the example times;
2. walk the 720 times and emit the first one that satisfies **all** of them, subject to one
   learned novelty filter (`_nov_wisbek`: the hour must not appear in the clue).

The hidden rule is *in* their pool (the pool contains `hmsum=k`, `diff=k`, `mdig=k`, `alldig=k`,
`m=kh`, `m5off_k`, `hmdiff12=k` — i.e. templates 0, 3, 5, 6, 7, 8 almost verbatim), so the answer
satisfies it by construction. **They never named a rule.** The excluded traps cost them nothing:
satisfying an extra rule is free when you are constructing. The only thing that ever hurt them was
the fresh-hour clause (0/4 → 40/41 once they found it), which players called invisible and unfair.

## 2. What v2 changes

* **Clue** = the same minimal identifying example set (2 or 3 times, all hours different), a blank
  line, then **4 candidate times**, one per line.
* **Answer** = the one candidate that obeys the hidden rule, written back verbatim (whitespace- and
  leading-zero-tolerant) or as its **1-based index** `1`–`4`.
* **U is unchanged** — the same 10 templates / 66 rules / antichain / density ceiling 0.11. The
  example-set logic (unique inside U, minimal, one example per hour) is unchanged.
* **The fresh-hour clause is gone.** It is no longer a rule about the answer; it is now a property
  of the whole lineup (below), so it cannot single the true candidate out.

## 3. How the decoys are built (revision-2 rules 1–5)

1. **Exactly one candidate obeys the rule** — verified in `generate` on every clue (500/500).
2. Every decoy **fails** the rule and is an instance of at least one **excluded** rule that is
   consistent with the examples (500/500 clues; on average 3.2 of the eleven excluded rules are
   consistent on top of the two always-consistent range traps).
3. **No shape tell.** Every candidate — true and decoy — sits at an hour **not in the clue** and at
   a minute **not in the clue**, and the four candidates use four different hours. So v1's 34.8 %
   "keep the minutes, move the hour" foothold has nothing to point at, and neither has "the one at a
   new hour".
4. **The count defence.** `generate` carries the winner's own pool (`wisbek_preds()`, 307
   predicates, verbatim) and scores every candidate by *how many pool predicates that survive the
   examples it satisfies* — that is what their attack degenerates to when the answer is a choice.
   It then aims the **rank** of the true candidate by that count:
   * on the **66 %** of clues where some minimal example set allows it (up to 12 sets are tried),
     the rank is drawn uniformly from **1..3** — at least one decoy beats the truth on the
     attacker's own measure;
   * on the other 34 % no time outside the rule can match the truth's count at all, because the
     truth owns pool predicates (`m5off_k`, `hmdiff12=k`) that a non-instance cannot have. These
     are almost entirely template 3 (clock-face offsets: 0/10 of its rules ever admit a full-range
     example set) and template 7.

   Measured: **"most surviving predicates" picks the truth 39.4 %** of the time (floor 25 %), i.e.
   it picks a **decoy 60.6 %** — revision 2 asks for ≥ 40 %. "Fewest predicates" scores 17.8 %, so
   the count is not usefully reversible either.
   **Honest leak:** on the 31 % of clues whose example minutes are *all* multiples of 5, "most
   predicates" rises to **54.5 %** (elsewhere 32.6 %). A player who discovers that conditional gains
   roughly five points. It is the price of keeping the clock-face templates, which are the most
   kid-legible rules in the class.

## 4. Three demos

```
CLUE                     ANSWER                 hidden rule (private)

2:35                     12:25   (index 1)      the minute hand points 5 numbers
7:00                                            past the hour number
9:10

12:25
3:29
5:33
8:45
--------------------------------------------------------------------------
9:46                     5:37    (index 4)      the minute digits add up to 10
12:19

1:14
6:58
8:41
5:37
--------------------------------------------------------------------------
4:35                     8:25    (index 3)      the hands make a square corner
7:50
10:05

1:09
6:48
8:25
2:30
```
(seeds 4, 31, 5; answers straight from `solve`. Note the third lineup: `2:30` is the o'clock/half
past trap, `6:48` keeps the clue's "minutes bigger than the hour" and `1:09` has all its digits
different — three different excluded rules, and every candidate is at a new hour with new minutes.)

## 5. Witness table — 500 fresh clues (seeds 1 000 000 – 1 000 499)

Every answer is a choice among four, so the floor is **25 %** and there is no well-formedness column
any more.

| witness | score |
|---|---|
| **the true rule (`solve`)** | **100.0 %** |
| **the in-U intersection** (the candidate satisfying every rule of U the examples allow) | **100.0 %** |
| a player who knows U minus its two rarest templates (2 and 8) | 87.5 % |
| **the candidate satisfying the MOST surviving predicates of the round-1 pool** | **39.4 %** |
| … the same attack, restricted to clues whose example minutes are all multiples of 5 (31 %) | 54.5 % |
| … the same attack, on all other clues | 32.6 % |
| universe = U + the excluded rules, pick one surviving hypothesis uniformly | 38.3 % |
| EXCLUDED: the minutes end in 0 or 5 (fits 31.2 % of clues) | 37.9 % |
| the candidate whose minutes are a multiple of 5 | 36.0 % |
| EXCLUDED: minutes inside the clue's minute range (fits 100 %) | 30.6 % |
| EXCLUDED: the hour goes exactly into the minutes (fits 25.8 %) | 30.4 % |
| the candidate whose minutes are nearest an example's | 27.7 % |
| EXCLUDED: hour inside the clue's hour range (fits 100 %) | 27.3 % |
| the candidate with the smallest hour | 26.0 % |
| the candidate in a minute-decade the clue uses | 25.8 % |
| EXCLUDED: all the digits are different (fits 27.0 %) | 25.7 % |
| EXCLUDED: both hands in the same half of the face (fits 18.0 %) | 25.4 % |
| EXCLUDED: the minutes are bigger than the hour (fits 71.4 %) | 25.3 % |
| **pick candidate 1** | **25.2 %** |
| **pick a random candidate (the floor)** | **25.0 %** |
| the candidate with the smallest minutes | 25.0 % |
| EXCLUDED: o'clock / quarter past / half past / quarter to (fits 1.0 %) | 24.9 % |
| EXCLUDED: the same half of the hour as the examples (fits 51.2 %) | 24.5 % |
| EXCLUDED: the minutes are all even / all odd (fits 52.6 %) | 23.4 % |
| EXCLUDED: the hour is odd / even (fits 40.6 %) | 17.1 % |
| the candidate satisfying the FEWEST surviving pool predicates | 17.8 % |

True-candidate rank by pool-predicate count over the 500 clues: 197 / 103 / 111 / 89 (rank 0 = the
sole top scorer).

Other measured numbers (500 clues unless stated):

* uniqueness 500/500, minimality 500/500, exactly one candidate obeys the rule 500/500;
* all example hours distinct 500/500; every candidate at a fresh hour **and** a fresh minute 500/500;
* every decoy an instance of a consistent excluded rule 500/500;
* example counts (2000 seeds): 2 → 48.2 %, 3 → 51.8 %;
* template mix 38–69 of 500 each (unchanged from v1); mean density of the hidden rule 0.048.

## 6. Validation

`python tools/quickcheck.py challenges/lab/wisbek.json --seeds 300` →
`OK wisbek  gen=2.83ms score=0.12ms solve=0.12ms`, **no warnings**.

| quantity | value | cap |
|---|---|---|
| `score` source | **812 chars** (v1: 895) | 1024 (the rule-family raise) |
| `generate` source | 11 418 | 50 000 |
| `solve` source | 1 212 | 5 000 |
| `generate` | **1.13 ms mean**, 2.9 ms max over 2000 seeds | 100 ms |
| `score` | 0.08 ms max on junk | 50 ms |
| `solve` | 0.05 ms mean, 0.10 ms max | 2000 ms |
| clue | ≤ 38 chars | 1024 |
| answer | ≤ 5 chars | 1024 |

**`generate` is over the 1 ms target and this is deliberate**: scoring the decoy pool against the
307 attacker predicates costs ~0.2 ms per example set, and up to 12 minimal example sets are tried
to find one that lets a decoy out-count the truth. The module-level tables (the 66-bit U mask, the
12-bit excluded-rule mask and the 307-bit pool mask for each of the 720 times) cost ~60 ms once per
worker and are not charged to `max_generate_ms`. Dropping to 5 example sets would give 1.08 ms and
cost nothing measurable; dropping the search altogether gives 0.6 ms and pushes "most predicates" up
to 54 %.

`score` was checked against the reference predicate on **all 720 times × 300 clues** (0
disagreements) and rejects `''`, `x`, `0`, `5` (an out-of-range index), the clue itself, unicode
digits and any well-formed time that is not one of the four candidates. It forgives surrounding
whitespace and a leading zero on the hour. `solve` re-derives the survivor exactly as the scorer
does and returns the true candidate verbatim.

## 7. Predicted classification

**Calibrated, and materially harder than v1.** Two Opus players, 7-class pool, 4 rounds:

* **Without a demo**: the shape is self-evident (examples, gap, four times, pick one), so every
  probe is well formed from round 1 and the floor is a free **25 %**. The round-1 method degrades
  to counting surviving predicates: **~39 %**. Add the cheap conditional (trust the count when the
  example minutes are all multiples of 5, guess otherwise) and a very good team reaches ~45 %.
  Expect **25–45 %**.
* **With a demo**: a demo now teaches almost nothing about a *convention* (there is none left to
  learn) — it only confirms the format. The way up is to reconstruct U, and the moment a player
  filters U correctly they score **100 %**, because the in-U intersection is exact. That is a cliff,
  not a slope: 10 templates and 66 rules from ~120 probes and 2–3 example times, with three
  clock-face templates nobody enumerates by default. Expect **35–65 %**, with the upper half
  requiring a player who explicitly hypothesises and tests rule *families*.

Mean across the two ≈ **0.35–0.5** → `calibrated`, now with the risk on the **hard** side rather
than the easy one (v1's graded 0 → 5 → 35 → 100 ladder is gone; v2's ladder is 25 → 39 → 100).
Levers if it comes back too hard: (i) go to k = 3 candidates (floor 33 %); (ii) let one decoy be an
instance of a *U* rule the examples nearly allow, so a partly-mapped player is rewarded rather than
punished. Too easy: (iii) spend the example-set search on the template-3/7 clues too, by allowing
decoys that reuse a clue minute when the truth does as well — that would pull "most predicates"
towards the 25 % floor.

**12-year-old test**: unchanged and slightly better. The object is still a clock, every rule is still
one breath said over a drawn face, and "which one of these four fits?" is an easier question to *ask*
a child than "make me another one" — the four candidates are themselves a hint about what kind of
thing the rule can be. What a kid loses is the freedom to answer with the first time they think of;
what they gain is that a wrong guess is now informative (one of four, not one of 720).

---

# 2026-09-05 — v3: the relational universe (Revision 3)

`docs/RULE_FAMILIES.md` §"Revision 3 (2026-09-05)" and its nine-step recipe. v1 and v2 are kept
byte-identical as `challenges/lab/wisbek.v1.json` and `challenges/lab/wisbek.v2.json`; the shipped
file is `challenges/lab/wisbek.json`. No arena run from this job.

## 9. What the two lineup arenas showed

Four Opus players met wisbek v2 in `lad-tresk-v2-1` and `lad-ospren-v2-1`. **None of them spent a
demo on it** and they scored **77 / 82 / 85 / 88 %** (target ≈ 50). Their engine, in their own
words: round 1 skip everything (~300 clues harvested free = the base rates); round 2 answer a
**random candidate** on every item, so a quarter come back correct — ~30 gold-labelled clues for
nothing ("30× what a demo gives"); then per clue keep the cheap predicates true of every example
and of **exactly one candidate**, weight by `freq^-2.5 / satisfiers^6`, and answer the candidate the
**rarest** survivor points at.

**The diagnosis, measured.** I rebuilt the attackers' bank for clock times from their own code —
`tresk1a/engine.py::f_time`, `tresk1b/strategy.py::build_wisbek+extra_wisbek` (286 booleans),
`ospren1a/strategy.py::f_wisbek`, `ospren1b/features.py::f_wisbek` — realised every (key, value)
pair over the 720 times, added the obvious extensions (more moduli, more thresholds, min/max digit,
counts of odd/even digits, `(m//5±h)%12`, `(m−5h)%60`, exact hand offsets) and de-duplicated by
satisfying set: **1332 predicates over 138 keys**. Scored against it, **every one of v2's 66 rules
has best Jaccard 1.00** — the whole universe was already in the bank. When the truth is in the bank
*and* is by construction the rarest thing the examples share, the lineup is a lookup.

**Two honest judgement calls about the bank.** I included `(m//5 + h) % 12 == k` (the *sum* of the
two hand numbers — the mirror of a predicate `dornic1b` really wrote) but not the minute-precision
`5h + m == k` / `(m + 5h) % 60 == k`, which nobody wrote and which would be handing over the new
mirror family verbatim. With the sum family in the bank the mirror rules still measure J = 0.20,
because a mirror also demands `m % 5 == 0` and no single bank predicate says both. I also kept
"how many digits are odd/even" in the bank, which is why "every digit is odd / every digit is even"
is **not** in U (J = 1.00) and "the digits are all one kind" (their union) is, at J = 0.60.

## 10. The universe U — 13 templates, 32 rules

Antichain verified by brute force over **all 720 times: 0 violations**. Mean density 0.087; mean
density of the hidden rule as actually drawn 0.101. "J" = best Jaccard against the 1332-predicate
bank. "attack" = the players' engine at 60 free labels on that template's clues.

| # | IN/EXCL | kid sentence (one breath) | params | density | bank J | attack |
|---|---|---|---|---|---|---|
| 0 | **IN** | the two hands are the same distance from the *n*, one on each side (fold the face along the *n*↔*n+6* line and they land on each other) | n = 12,1,2,3,4,5 | .017 | **.20** | 52 % |
| 1 | **IN** | the two hands are *n* numbers apart | n = 1…5 | .167 | **.50** | 6 % |
| 2 | **IN** | the big hand points at **half** the little hand's number | — | .042 | **.23** | 3 % |
| 3 | **IN** | the big hand points at **double** the little hand's number | — | .042 | **.50** | 10 % |
| 4 | **IN** | the hour is between the two minute digits | — | .189 | **.31** | 6 % |
| 5 | **IN** | the time starts with its smallest digit · ends with its smallest digit · its biggest digit is in the middle, not at either end | 3 | .142/.174/.119 | **.53/.69/.45** | 6 % |
| 6 | **IN** | the hour and the first (last) minute digit are next-door numbers | 2 | .139/.150 | **.28/.50** | 12 % |
| 7 | **IN** | the digits are all one kind — all odd, or all even | — | .208 | **.60** | 13 % |
| 8 | **IN** (cheap) | the two minute digits are twins (*n*=0) / are next-door numbers (*n*=1) | 2 | .100/.183 | 1.00 | 47 % |
| 9 | **IN** (cheap) | the two hands point at the same number (*n*=0) / at opposite numbers (*n*=6) | 2 | .017 | 1.00 | 98 % |
| 10 | **IN** (cheap) | the hour turns up again in the minutes | — | .200 | 1.00 | 19 % |
| 11 | **IN** (cheap) | the minutes are *n* more than the hour | n = 15,25,35,45 | .017 | 1.00 | 100 % |
| 12 | **IN** (cheap) | the minutes are *n* times the hour | n = 2,3,4 | .017 | 1.00 | 100 % |
| — | EXCL | every digit is odd / every digit is even | | .125/.083 | 1.00 | retired |
| — | EXCL | the time reads the same backwards | | .079 | 1.00 | retired (and ⊂ template 10) |
| — | EXCL | the minute hand is exactly *n* numbers past the hour number; the hands make a square corner (exactly) | | .017/.033 | 1.00 | retired (⊂ template 1) |
| — | EXCL | the minute digits add up to *n*; all the digits add up to *n*; the hour and the minutes add up to *n*; the minutes are in the *n* times table; the minutes are in the *n*-tens | | .05–.17 | 1.00 | retired: **all of v2's U** |
| — | EXCL | the minutes end in 0 or 5 · o'clock/quarter past/half past/quarter to · minutes even/odd · hour even/odd · first/second half of the hour · all the digits different · the hour goes exactly into the minutes · both hands in the same half of the face · the minutes bigger than the hour · the digits go up / go down · the time starts and ends with the same digit · the answer's minutes / hour inside the clue's range | | .10–1.0 | — | the kid traps |

**The finding this class adds to the recipe: J alone is not the retirement criterion — J × rarity
is.** In a lineup a bank predicate only helps the attacker if it selects exactly one candidate, so
a *dense* predicate is worthless to him even at J = 1.00. Measured: "the two minute digits are
twins" (.100) pays him 47 %, "the hour turns up again in the minutes" (.200) only 19 %, while the
one-instance-per-hour families (.017) pay 98–100 %. Step 2 of the recipe should read "retire rules
with J > 0.8 **and density below ~.1**"; the dense high-J rules are free kid-legible material.
Templates 8–12 are kept deliberately as the **learnable slope** (~38 % of clues drawn, but only the
three rare families actually hand over an answer, ≈ 23 % of clues).

## 11. How the lineup is built (levers 1, 2, 5 and one new one)

* **k = 5** candidates, floor 20 %; **always a minimal pair** (500/500 clues, 2000/2000 seeds);
  every candidate at an hour *and* a minute not in the clue, five different hours (500/500), so no
  copying heuristic can point at the truth.
* **Lever 0 (new here): choose the example set that hides the rule from the bank.** Up to 8 minimal
  pairs are built and the one preferred is the one for which **no surviving bank predicate implies
  the rule**. For "the hands are 3 apart" that means the two examples sit on *opposite* sides, so
  the bank's one-sided offset predicate is not example-consistent and cannot name the answer; the
  same trick kills "every digit is odd" as an explanation of "the digits are all one kind" (one
  example all-odd, one all-even). Worth **5 points** (49.3 → 44.3) and it took template 1 from
  47 % to 6 %. Where it is impossible — the five cheap families — that *is* the slope.
* **Lever 5: aim the rarity order.** `generate` carries the 1332-predicate bank and the players'
  own weight, and samples decoys of two kinds: ones that **delete** the truth's cheapest
  explanation by satisfying it too (its weight is then divided by 5^6), and ones carrying a
  **rarer accident of their own**. The lineups are bucketed by the rank they leave the truth in and
  that rank is drawn uniformly from 0…4. Within a rank it keeps the lineup whose excluded rules
  match best, where the truth is not the top of the count order and not the outlier or the medoid
  by shared digits (aims 2 and 3). Worth **6 points**.
* **§5b, weak form.** The 720-time universe is too small for tavrik's strong form: forcing all five
  candidates to agree about ~9 fitted traps at once empties the pool (measured: 0–4 usable decoys),
  and worse, forcing "the minutes end in 0 or 5" makes the mirror family's cheapest explanation
  unblunt-able. So trap matching is a **preference inside the chosen rank**, not a constraint:
  **53 % of fitted traps are all-or-none**, and the heuristics it exists to kill are measured
  dead anyway — "the candidate firing the most excluded rules" **26 %**, "the fewest" **17 %**
  against a 20 % floor.

## 12. The attacker table — v2 vs v3

Same simulator for both (`scratchpad/wis3/sim.py`): skip-harvest base rates from 250 clues →
random-candidate answers on a disjoint pool, of which 1/k come back correct = the gold labels →
per-key unique-explanation reliabilities → rarity-weighted pick. 400 test clues, seeds 1e6….

| free labels | **v2** (k = 4, floor 25 %) | **v3** (k = 5, floor 20 %) |
|---|---|---|
| 0 | **94.7 %** | **38.0 %** |
| 30 | **96.3 %** | **43.0 %** |
| 60 | **95.0 %** | **44.8 %** |
| 120 | 97.3 % | 46.2 % |
| 240 | 97.7 % | 49.0 % |

**Calibration.** The simulator scores 94.7 % on v2 where the four real Opus centaurs scored
77–88 %, so it runs **≈ 10 points hot** here (tavrik's ran 5 points hot). Read v3 as **≈ 33–40 %
for a real demo-less Opus player**, and the curve as flat: +6.8 points for the first 60 labels and
+4.2 for the next 180, where v2 was already finished at label zero.

**The ceiling stays where it belongs.** The in-U intersection is **100.0 %**. The same engine with a
bank that *also* contains all of U scores **69.0 / 77.2 / 83.8 / 94.0 / 95.8 %** at 0/30/60/120/240
labels and reaches **90 % U-coverage at ~110 labels** (100 % at 120). With the generic bank alone,
U-coverage stalls at **34 %** — only the five cheap templates are expressible in it at all. The gap
**45 % → 96 %** is the class, and it is paid for by inventing the vocabulary: *two hands, two
digits, two ends of the written time*.

## 13. Lever ablation (identical conditions, 300 clues, 60 labels)

| build | k | floor | simulated attack |
|---|---|---|---|
| **v3 as shipped** | 5 | 20 % | **44.3 %** |
| minus lever 1: k = 4 | 4 | 25 % | 47.0 % |
| lever 1 pushed: k = 6 | 6 | 16.7 % | 44.3 % |
| minus lever 5: decoys not aimed | 5 | 20 % | 50.0 % |
| minus lever 0: example set not chosen to hide the rule | 5 | 20 % | 49.3 % |
| minus lever 2: three-example clues | 5 | 20 % | 56.7 % |
| **minus lever 3: v2's own universe** | 4 | 25 % | **95.0 %** |

The relational universe is worth **≈ 51 points**; the two-example clue **12** (much more than
tavrik's 3 — with only two numbers per instance, a third example lets the bank intersect hard);
aiming **6**; hiding the rule from the bank in the example set **5**; the fifth candidate **3**.
**k = 6 buys exactly nothing** and costs a clue line and a kid's patience — five is the number.

## 14. Three demos

```
CLUE            LINEUP                          ANSWER          the rule, in a kid's words
2:20            10:25 3:36 6:22 7:22 11:16  ->  6:22  (3)       the two hands are 2 numbers apart
9:38                                                            (6 and 4 — count them)

1:05            4:13 6:47 8:13 9:27 3:11    ->  6:47  (2)       the hour is between the two
7:58                                                            minute digits (4 < 6 < 7)

3:15            6:50 11:22 5:25 7:47 1:08   ->  5:25  (3)       the two hands point at the same
12:00                                                           number
```
(seeds 1000000, 1000005, 1000013; in the real clue the five candidates are one per line, after a
blank line. Demo 3 is a *cheap* clue — the learnable slope — and demo 2 is the class in one
picture: five three-digit times, and only one of them has its hour squeezed between its two minute
digits.)

## 15. Witness table — 500 fresh clues (seeds 1 000 000 – 1 000 499)

Floor 20 % (one of five). All ties broken uniformly at random.

| witness | score |
|---|---|
| **the true rule (`solve`), verbatim and by index** | **100.0 %** |
| **the in-U intersection — a player who knows U** | **100.0 %** |
| a player who knows U minus its two rarest templates (half / double) | 90.2 % |
| a player who knows U minus the mirror and same-number templates | 86.1 % |
| **the full revision-3 attack, 1332-predicate bank, 30 labels** | **43.0 %** |
| … at 0 / 60 / 120 / 240 labels | 38.0 / 44.8 / 46.2 / 49.0 % |
| EXCLUDED: the minutes are *n* more than the hour †(a U template) | 91.4 % (fits 10 %) |
| the candidate satisfying the MOST example-consistent bank predicates | 37.1 % |
| EXCLUDED: all the digits are different (fits 51 %) | 26.6 % |
| the candidate firing the MOST example-consistent excluded rules | 26.4 % |
| the candidate whose minutes are a multiple of 5 | 26.2 % |
| EXCLUDED: the minutes end in 0 or 5 (fits 76 %) | 24.8 % |
| EXCLUDED: the hour turns up again in the minutes † (fits 65 %) | 24.8 % |
| the candidate with the smallest hour | 23.6 % |
| EXCLUDED: the minute digits are next-door numbers † (fits 69 %) | 23.2 % |
| EXCLUDED: the hour goes exactly into the minutes (fits 56 %) | 23.1 % |
| EXCLUDED: both hands in the same half of the face (fits 58 %) | 22.2 % |
| EXCLUDED: the minutes are in the same ten (fits 16 %) | 21.2 % |
| EXCLUDED: the digits go down / go up (fits 65 / 69 %) | 21.0 / 20.9 % |
| **pick candidate 1** | **20.4 %** |
| EXCLUDED: first / second half of the hour (fits 52 %) | 20.3 % |
| **pick a random candidate (the floor)** | **20.0 %** |
| the candidate sharing the most digits with an example | 20.0 % |
| EXCLUDED: the minute digits add up to the same total (fits 9 %) | 19.8 % |
| EXCLUDED: the minutes are bigger than the hour (fits 76 %) | 19.8 % |
| EXCLUDED: the hands make a square corner, exactly (fits 95 %) | 19.6 % |
| the candidate in a minute-decade the clue uses | 19.6 % |
| the candidate whose minutes are nearest an example's | 19.4 % |
| EXCLUDED: the hour is even / odd (fits 40 %) | 19.3 % |
| EXCLUDED: the time reads the same backwards (fits 84 %) | 18.7 % |
| EXCLUDED: o'clock / quarter past / half past / quarter to (fits 78 %) | 18.7 % |
| EXCLUDED: the time starts and ends with the same digit (fits 82 %) | 18.5 % |
| EXCLUDED: all the digits add up to the same total (fits 8 %) | 18.2 % |
| the candidate firing the FEWEST example-consistent excluded rules | 17.4 % |
| EXCLUDED: the minutes are even / odd (fits 44 %) | 16.7 % |
| EXCLUDED: the hour and the minutes add up to the same total (fits 2 %) | 16.4 % |
| the candidate with the smallest minutes | 15.8 % |
| the candidate satisfying the FEWEST example-consistent bank predicates | 9.3 % |

† Three of the trap features are also U templates (they are bank predicates that the class *does*
use). They are kept in the matched-profile list, which is why following one blindly is worth
23–25 %; the exception is the rarest of them — when "the minutes are 25 more than the hour" fits
both examples it is the rule 91 % of the time, and that is the slope working exactly as designed.

Other measured numbers (500 clues unless stated): uniqueness 500/500 · minimality 500/500 · exactly
one candidate obeys the rule 500/500 · five distinct candidates 500/500 · every candidate at a fresh
hour **and** a fresh minute 500/500 · five different candidate hours 500/500 · examples per clue
**2 → 2000/2000 seeds** · template mix 26–50 of 500 each · true-candidate rank in the rarity order
194/76/82/72/76 and in the count order 188/108/90/68/46 · fitted traps all-or-none 2873/5522 (53 %)
· **0 duplicate clues and 0 fallback clues over 3000 seeds**.

## 16. Validation

`python tools/quickcheck.py challenges/lab/wisbek.json --seeds 300 --cap max_score_code_chars=1024`
→ `OK wisbek  gen=4.49ms score=0.15ms solve=0.17ms` (those are the *maxima*), **no warnings**.

| quantity | value | cap |
|---|---|---|
| `score` source | **1009 chars** (v1 895, v2 812) | 1024 (the rule-family raise) |
| `generate` source | 26 701 (11 KB of it is the attackers' bank) | 50 000 |
| `solve` source | 1 481 | 5 000 |
| `generate` | **2.00 ms mean**, 1.97 median, 3.12 p99, 4.86 max over 2000 seeds | 100 |
| `score` | 0.06 ms mean, 0.46 ms max (junk included) | 50 |
| `solve` | 0.07 ms mean, 0.15 ms max | 2000 |
| clue | ≤ 38 chars | 1024 |
| answer | ≤ 5 chars | 1024 |

Module-level tables (the 32-bit U mask, the 21 trap features and the 1332-bit bank mask for each of
the 720 times) cost ≈ 0.2 s once per worker and are not charged to `max_generate_ms`.
`score` was checked against the reference predicate on **all 720 times × 200 clues** (0
disagreements) in four answer forms — verbatim, 1-based index, surrounding whitespace, leading zero
on the hour — and rejects `''`, `x`, `0`, `6`, `9`, `-1`, `1.0`, `'1'*100`, `'9'*4000`, the clue
itself, `12:60`, `13:05`, `7:5`, `hel lo`, the unicode digits `١` / `²` and a two-line answer,
without raising. `solve` re-derives the survivor exactly as the scorer does and returns the true
candidate verbatim.

## 17. Predicted classification

**Calibrated, with the risk on the hard side.** Two Opus players in a 7-class pool:

* **Without a demo** the clue reads as multiple choice from probe 1, so every attempt is well formed
  and the 20 % floor is free. The v2 engine — skip-harvest, random-candidate labels, rarest
  surviving predicate — now pays a simulated 43–45 % at 30–60 labels, i.e. **≈ 33–40 %** for a real
  player once the simulator's 10-point head start on v2 is removed, and it **stops improving**
  (+4 points for the next 180 labels). Expect **30–40 %**.
* **With a demo** the demo teaches the format in one look and one worked rule; the way up is to
  notice that this class only ever talks about *two hands, two digits or the two ends of the written
  time* and to write those predicates down. A player who does scores 90–100 %. Expect **45–65 %**.

Mean across the two ≈ **0.35–0.5** → `calibrated`, against v2's measured 0.83. The residual risk is
that an Opus player generalises from three or four labelled clues to "it is about the two hands",
which is exactly the insight the ladder wants to reward.

**12-year-old test (v2's score must hold at 4.0+).** The object is still a clock — a kid names it
from one look at `7:45` — and every rule is now something a kid **spots by eye** rather than
computes: *the two hands are two numbers apart · the two hands point at the same number · the hour
is squeezed between the two minute digits · the minute digits are twins · the minute digits are
next-door numbers · the hour turns up again in the minutes · the biggest digit is in the middle ·
the digits are all odd or all even · fold the clock and the hands land on each other*. Every
arithmetic readout of v1/v2 that read as a puzzle-book trick — the digit sums, the times tables,
`m mod k`, "all the digits add up to n" — has been **retired to the trap list**; the only counting
left is "the minutes are 25 more than the hour" and "the minutes are three times the hour", which a
kid does on two short numbers. The clue is now always **two** times plus five candidates, so a kid
reads the whole thing aloud in one breath, and checking a candidate by hand is one glance at a
drawn face.

# 2026-09-05 — v4: the look-only trim

`docs/RULE_FAMILIES.md` §"Revision 3" plus its addenda. v1/v2/v3 are kept byte-identical as
`challenges/lab/wisbek.v1.json`, `.v2.json`, `.v3.json`; the shipped file is
`challenges/lab/wisbek.json`. No arena run from this job. Working files:
`scratchpad/wis4/` (`uni4.py`, `gen4.py`, `sim.py`, `per.py`, `abl.py`, `wit.py`, `check.py`).

## 18. What v3's arena and its judge said

`lad-tavrik-v3-1` measured wisbek v3 **without demos at 32 % and 35 %** — the weakest class in the
lineup pool and just under the 35–55 % band. Two complaints, and they are the same complaint:

* the player, in `sim/results/lad-tavrik-v3-1/players/*/NOTES.md`: *"wisbek is the weakest class
  (34.7 %, against a 20 % floor). Its family mixes visual rules (a repeated digit, digits going up)
  with arithmetic ones (minutes divisible by 9, (m−5h) mod 10 = 0), and the last of those is not
  something a 12-year-old would phrase. Lean fully into the clock face: both hands point at a
  number, the hands are mirror images."*
* the judge (kid **4.33**, `nameable: no`): *"trim the arithmetic templates (minutes = hour+n,
  minutes = n × hour) and the fold-along-a-diameter one toward purely eye-checkable hand/digit-
  position relations."*

So v4 is a **trim, not a rebuild**: same world, same lineup machinery, same 1332-predicate attacker
bank, same levers 0–5. Every rule that needs a calculation is retired to the trap list, and the
class is softened back up the way the recipe says to soften — by **doubling the two cheap dense
templates** (addendum: retire by J × rarity; a dense bank predicate is worthless to a lineup
attacker, so dense cheap rules are free kid-legible material).

## 19. The universe — v3 (13 templates / 32 rules) → v4 (8 templates / 14 rules)

Antichain re-verified by brute force over **all 720 times: 0 violations**. Mean density 0.121
(0.137 as actually drawn). "J" = best Jaccard against the 1332-predicate bank; "atk" = the
simulated free-label attack on that template's clues at 60 labels (600 clues).

| w | # | IN/EXCL | kid sentence, read aloud | params | density | J | atk |
|---|---|---|---|---|---|---|---|
| 1 | 0 | **IN** | the two hands point at the same number · at next-door numbers · at opposite numbers | n = 0,1,6 | .017/.033/.017 | 1.00/.50/1.00 | 72 % |
| 1 | 1 | **IN** | the two hands are mirror images in the line from the 12 to the 6 (3:45 → 3 and 9) | — | .017 | **.20** | 55 % |
| 1 | 2 | **IN** | the hour is between the two minute digits | — | .189 | **.31** | 7 % |
| 1 | 3 | **IN** | the time starts with its smallest digit · ends with its smallest digit · its biggest digit is in the middle, not at either end | 3 | .142/.174/.119 | .53/.69/.45 | 15 % |
| 1 | 4 | **IN** | the hour and the first (last) minute digit are next-door numbers | 2 | .139/.150 | .28/.50 | 8 % |
| 1 | 5 | **IN** | the digits are all one kind — all odd, or all even | — | .208 | .60 | 18 % |
| 2 | 6 | **IN** (cheap) | the two minute digits are twins · are next-door numbers | 2 | .100/.183 | 1.00 | 89 % |
| 2 | 7 | **IN** (cheap) | the hour turns up again in the minutes | — | .200 | 1.00 | 68 % |
| — | — | **EXCLUDED in v4** | the minutes are *n* more than the hour (v3 T11) · the minutes are *n* times the hour (v3 T12) | | .017 | 1.00 | retired: arithmetic |
| — | — | **EXCLUDED in v4** | the two hands are *n* numbers apart, counted by sector (v3 T1) | | .167 | .50 | retired: a minute hand between two numbers has no honest count |
| — | — | **EXCLUDED in v4** | the big hand points at half / at double the little hand's number (v3 T2, T3) | | .042 | .23/.50 | retired: multiplication, and the same sector problem |
| — | — | **EXCLUDED in v4** | fold the face along the *n*↔*n+6* line, *n* = 1…5 (v3 T0) | | .017 | .20 | retired: only the 12–6 mirror has a name a kid says |
| — | — | EXCL (as v3) | minutes even/odd · first/second half of the hour · the minute hand points straight at a number · all the digits different · the hour even/odd · the hour goes exactly into the minutes · both hands in the same half of the face · o'clock/quarter past/half past/quarter to · the minutes bigger than the hour · the time reads the same backwards · the digits go up / go down · the time starts and ends with the same digit · the hands make a square corner · the minutes in the same ten · the minute digits / all the digits / the hour and the minutes add up to the same total · the two range traps · **all of v2's universe** (digit sums, *m* mod *k*, *m* = *k·h*) | | | | the kid traps |

**Read aloud, all fourteen:** *the two hands point at the same number · at next-door numbers · at
opposite numbers · the two hands are mirror images in the line from the 12 to the 6 · the hour is
between the two minute digits · the time starts with its smallest digit · the time ends with its
smallest digit · the biggest digit is in the middle · the hour and the first minute digit are
next-door numbers · the hour and the last minute digit are next-door numbers · the digits are all
one kind · the two minute digits are twins · the two minute digits are next-door numbers · the hour
turns up again in the minutes.* Not one of them contains a sum, a product, a remainder or a count.

**Three things the trim taught.**

1. **"The big hand points straight up or straight down" is unbuildable here, however lovely it
   reads.** Its satisfying set uses only the minutes `:00` and `:30`; the two examples sit at
   different hours but consume both minutes, and every candidate must be at a minute the clue does
   not use — so no candidate can obey the rule. Measured: template drawn 0 times in 300 clues.
   A rule whose satisfying set spans fewer minute values than (examples + 1) cannot live in a
   lineup class with a fresh-minute rule. It stays on the trap list inside "o'clock / quarter past
   / half past / quarter to".
2. **The mirror survives the fold family because it is the one axis with a name.** `(5h+m) % 60 = 0`
   means the two hand *numbers* add to 12 — 3 and 9, 2 and 10, 5 and 7 — and the minute hand is
   always exactly on a number, so a kid checks it by folding the drawn face down the middle. The
   other five diameters are the same arithmetic wearing a different hat.
3. **The complement half of a digit-position family is a trap, not a rule.** "The smallest digit is
   in the middle" (.476) and "the biggest digit is at the back" (.428) look like the natural mirror
   images of the three kept rules, but the minutes' tens digit only runs 0–5 and the units digit
   0–9, so those three are dense by construction and (RULE_FAMILIES) a lineup cannot carry a rule
   near density .5: four decoys all lacking a common property is itself a signature. Kept out.

## 20. The attacker table — v3 vs v4

Same simulator for both (`scratchpad/wis4/sim.py` = the players' own engine: skip-harvest base
rates from 300 clues → random-candidate answers on a disjoint pool, of which 1/k come back correct
= the gold labels → per-key unique-explanation reliabilities → rarity-weighted pick). 600 test
clues, seeds 1e6…, identical conditions for both rows.

| free labels | **v3** (13 templates, 32 rules) | **v4** (8 templates, 14 rules) |
|---|---|---|
| 0 | 39.0 % | **29.5 %** |
| 30 | 41.8 % | **41.0 %** |
| 60 | 43.2 % | **45.5 %** |
| 120 | 43.7 % | **50.8 %** |
| 240 | 49.5 % | **55.8 %** |
| bank + all of U (the honest ceiling) | — | 54.8 / 88.0 / 88.3 / 93.3 / 95.3 % |
| the in-U intersection (a player who has mapped U) | 100.0 % | **100.0 %** |
| U-coverage learned with the generic bank | 34 % | **37 %** (stalls; 100 % at 120 labels once U is in the bank) |

**How to read it.** v4 starts *lower* than v3 (29.5 vs 39.0: the two 100-%-at-zero-labels arithmetic
families are gone) and finishes *higher* (55.8 vs 49.5: the doubled cheap slope is learnable). The
shape is the point — this class now rewards labels on the part of U a predicate bank can express
and stalls on the rest, which is exactly what the recipe asks a "learnable slope" to do.

**Calibration, which is what the target has to be read through.** The simulator scored 94.7 % on v2
where four real Opus centaurs scored 77–88 %, and 43–49 % on v3 where two scored 32 and 35 %. It
runs **≈ 13 points hot** on this class. Both pool-3 players harvested **170–535 free labels**, so
the column to read is 120–240: v4 simulates **51–56 %** there → **≈ 38–43 % for a real demo-less
Opus player**, against v3's measured 33.5 %. That is the middle of the 35–55 % band.

## 21. Lever ablation (identical conditions, 300 clues, 60 labels)

| build | k | floor | simulated attack |
|---|---|---|---|
| **v4 as shipped** | 5 | 20 % | **46.7 %** |
| minus lever 1: k = 4 | 4 | 25 % | 48.0 % |
| lever 1 pushed: k = 6 | 6 | 16.7 % | 45.0 % |
| minus lever 0: example set not chosen to hide the rule | 5 | 20 % | 48.7 % |
| minus lever 5: decoys not aimed | 5 | 20 % | 51.7 % |
| minus lever 2: three-example clues | 5 | 20 % | 61.0 % |
| **minus step 4: the two cheap templates not doubled** | 5 | 20 % | **36.0 %** |
| minus lever 3: v2's own universe (measured on v3, unchanged) | 4 | 25 % | 95.0 % |

**The softening lever is step 4, and it is worth 10.7 points** — more than aiming (5.0), lever 0
(2.0) and the fifth candidate (1.3) put together. This is the addendum "retire by J × rarity"
paying off twice: the dense cheap templates are the only place a designer can add attack rate
without adding arithmetic. `k = 6` again buys nothing, and the two-example clue is still worth
14 points, so the pool-3 request for a third positive stays refused (it is free intersection
material for the attacker); the fairness answer is the *smaller, plainer* universe instead.

**One new sub-lever (v4).** When the rule is template 0 the decoys are now HARD-matched on the trap
"the minute hand points straight at a number": four of the fourteen rules force `m % 5 == 0` on the
true candidate, and without the match "pick the candidate whose minutes end in 0 or 5" was worth
**30.6 %** against a 20 % floor (now **26.5 %**). It is deliberately *not* applied to the mirror
template — there the rule *is* "on a number, and the two hand numbers add to 12", so forcing every
candidate onto a number hands the bank's hand-sum predicate the answer (measured 55 % → 88 %).
That is the concrete form of v3's note that this 720-time world cannot hold §5b in the strong form.

## 22. Three demos

```
CLUE            LINEUP                             ANSWER        the rule, in a kid's words
5:55            3:35 12:35 9:15 1:25 10:50    ->   9:15  (3)     the two hands point at opposite
8:10                                                             numbers (5 and 11; 8 and 2; 9 and 3)

2:30            9:57 5:14 8:03 11:26 4:16     ->   4:16  (5)     the hour is between the two minute
7:08                                                             digits (0<2<3, 0<7<8, 1<4<6)

2:33            6:04 11:57 4:00 7:46 12:39    ->   4:00  (3)     the two minute digits are twins
5:11
```
(seeds 1000002, 1000001, 1000004; in the real clue the five candidates are one per line, after a
blank line. Demo 3 is a *cheap* clue — the learnable slope. Demo 1 is the class in one picture:
draw the five candidate faces and only one has its hands pointing straight across the dial.)

## 23. Witness table — 500 fresh clues (seeds 1 000 000 – 1 000 499)

Floor 20 % (one of five). All ties broken uniformly at random.

| witness | score |
|---|---|
| **the true rule (`solve`), verbatim and by index** | **100.0 %** |
| **the in-U intersection — a player who knows U** | **100.0 %** |
| a player who knows U minus the two face templates | 81.6 % |
| a player who knows U minus the two cheap templates | 69.9 % |
| **the full revision-3 attack, 1332-predicate bank, 60 labels** | **45.5 %** |
| … at 0 / 30 / 120 / 240 labels | 29.5 / 41.0 / 50.8 / 55.8 % |
| EXCLUDED ††: fold the face along the *n*↔*n+6* line (fits 13 %) | 85.3 % |
| EXCLUDED ††: the two hands are *n* numbers apart, by sector (fits 16 %) | 63.3 % |
| EXCLUDED †: the hour turns up again in the minutes (fits 69 %) | 40.2 % |
| EXCLUDED: all the digits are different (fits 64 %) | 36.1 % |
| the candidate firing the MOST example-consistent excluded rules | 34.4 % |
| the candidate the rarest surviving bank predicate points at, no labels | 33.0 % |
| EXCLUDED †: the minute digits are next-door numbers (fits 72 %) | 32.2 % |
| the candidate satisfying the MOST example-consistent bank predicates | 28.3 % |
| the candidate whose minutes are a multiple of 5 | 26.5 % |
| EXCLUDED: all the digits add up to the same total (fits 5 %) | 25.4 % |
| EXCLUDED: the minutes end in 0 or 5 (fits 73 %) | 23.6 % |
| EXCLUDED: both hands in the same half of the face / the digits go up (fits 56 / 57 %) | 22.4 / 22.4 % |
| EXCLUDED: the digits go down (fits 58 %) | 21.6 % |
| the candidate with the smallest hour | 21.4 % |
| EXCLUDED: the hour goes exactly into the minutes (fits 53 %) | 21.3 % |
| EXCLUDED: the hands make a square corner, exactly (fits 96 %) | 20.3 % |
| **pick a random candidate (the floor)** | **20.0 %** |
| EXCLUDED: o'clock / quarter past / half past / quarter to (fits 76 %) | 19.1 % |
| EXCLUDED: the minutes are bigger than the hour (fits 77 %) | 19.0 % |
| the candidate with the smallest minutes | 18.7 % |
| EXCLUDED: the time starts and ends with the same digit (fits 77 %) | 17.8 % |
| the candidate sharing the most digits with an example | 17.8 % |
| EXCLUDED: the time reads the same backwards (fits 79 %) | 17.6 % |
| EXCLUDED: the minutes are in the same ten (fits 16 %) | 17.4 % |
| EXCLUDED: the hour is even / odd (fits 36 %) | 16.9 % |
| EXCLUDED: the minutes are *n* times the hour (fits 33 %) | 16.8 % |
| the candidate firing the FEWEST example-consistent excluded rules | 15.5 % |
| **pick candidate 1** | **15.4 %** |
| EXCLUDED: the minute digits add up to the same total / first-second half (fits 8 / 50 %) | 15.1 / 15.1 % |
| the candidate in a minute-decade the clue uses | 14.7 % |
| EXCLUDED: the minutes are even / odd (fits 38 %) | 14.2 % |
| EXCLUDED: the minutes are *n* more than the hour (fits 1 %) | 13.3 % |
| **INVERTED: the candidate the rarest unique bank predicate does NOT point at** | **12.5 %** |
| the candidate whose minutes are nearest an example's | 12.4 % |
| the candidate satisfying the FEWEST example-consistent bank predicates | 11.8 % |

† Two trap features are *also* U templates (they are bank predicates the class does use, and they
are the doubled slope), so following one blindly is worth 32–40 % — that is the slope, not a leak.
†† Two trap features are the **shadows of the face templates**: when both examples share a hand
offset, or fold onto the same diameter, it is nearly always *because* the rule is a face rule, and
no decoy can share the value without satisfying the rule. Following them is therefore worth 63 and
85 % on the 13–16 % of clues where they fit — i.e. a player who has invented the words "the two
hands" collects the face family, which is the insight the class exists to reward.
The honest cost of doubling the slope: "most excluded rules" is **34.4 %** against v3's 26.4 %, and
almost all of the rise comes from those two † templates. "Fewest" is 15.5 % and the **inverted**
rarity attack is 12.5 %, so there is no free heuristic pointing away from the truth either.

Other measured numbers (500 clues unless stated): uniqueness 500/500 · minimality 500/500 · exactly
one candidate obeys the rule 500/500 · five distinct candidates 500/500 · every candidate at a fresh
hour **and** a fresh minute 500/500 · five different candidate hours 500/500 · examples per clue
**2 → 2000/2000 seeds** · template mix 33–98 of 500 · true-candidate rank in the rarity order
163/109/97/68/63 and in the count order 142/122/105/73/58 · fitted traps all-or-none 2620/5626
(47 %) · **0 duplicate clues and 0 fallback clues over 2000 seeds**.

## 24. Validation

`python tools/quickcheck.py challenges/lab/wisbek.json --seeds 300 --cap max_score_code_chars=1024`
→ `OK wisbek  gen=3.74ms score=0.12ms solve=0.11ms` (maxima), **no warnings**.

| quantity | value | cap |
|---|---|---|
| `score` source | **816 chars** (v1 895, v2 812, v3 1009) | 1024 (the rule-family raise) |
| `generate` source | 27 554 (11 KB of it is the attackers' bank) | 50 000 |
| `solve` source | 1 186 | 5 000 |
| `generate` | **1.87 ms mean**, 1.83 median, 3.45 p99, 5.02 max over 2000 seeds | 100 |
| `score` | 0.11 ms max (junk included) | 50 |
| `solve` | 0.08 ms max; correct on 1000/1000 clues | 2000 |
| clue | ≤ 38 chars | 1024 |
| answer | ≤ 5 chars | 1024 |

Module-level tables (the 14-bit U mask, the 24 trap features and the 1332-bit bank mask for each of
the 720 times) cost ≈ 0.2 s once per worker and are not charged to `max_generate_ms`.
`score` was checked against the reference predicate on **400 clues × (the 5 candidates + all 720
times)** — 0 disagreements — in four answer forms (verbatim, 1-based index, surrounding whitespace,
leading zero on the hour): 1200/1200. It rejects `''`, `x`, `0`, `6`, `9`, `-1`, `1.0`, `'1'*100`,
`'9'*4000`, the clue itself, `12:60`, `13:05`, `7:5`, `hel lo`, `1:23:45`, `[1]`, `None`, a two-line
answer and the unicode digits `١` / `²` without raising. `solve` re-derives the survivor exactly as
the scorer does and returns the true candidate verbatim.

*(One inherited convention, unchanged from v3: for the two-digit hours 10, 11, 12 "the hour turns up
again in the minutes" reads the hour's **last** digit — 12:23 counts because of the 2. It is the
only place in U where a written time is not treated one digit at a time.)*

## 25. Predicted classification

**Calibrated, with the risk now on the easy side rather than the hard side.**

* **Without a demo** the clue reads as multiple choice from probe 1, so every attempt is well formed
  and the 20 % floor is free. The pool-2/3 engine — skip-harvest, random-candidate labels, rarest
  surviving predicate — simulates 45.5 % at 60 labels and **50.8 / 55.8 % at the 120–240 labels the
  real players actually harvested**, i.e. **≈ 38–43 %** once the simulator's measured 13-point head
  start is removed (v3: 33.5 % measured). Expect **35–45 %**.
* **With a demo** the demo teaches the format in one look and one worked rule, and the vocabulary is
  now small and concrete enough that a player who says "it is always about the two hands, or about
  where the smallest and biggest digits sit" can write U down. A player who does scores 100 %.
  Expect **50–70 %**.

Mean across the two ≈ **0.45–0.55** → `calibrated`, against v3's measured 0.335 and v2's 0.83. The
residual risk is the other way from v3's: U is now only 14 rules and an Opus player who spends a
demo may map it inside four rounds. If the next run comes back above 0.7, the lever to pull is step
4 in reverse (un-double the cheap templates: −10.7 points), not more arithmetic.

**12-year-old test (target 4.5+, v3 scored 4.33 with `nameable: no`).** The object is still a clock,
and every one of the fourteen rules is now something a kid **sees**: two hands pointing at the same
number, at next-door numbers, at opposite numbers, or mirrored down the middle of the face; the hour
squeezed between the two minute digits; the smallest digit at the front or the back; the biggest one
in the middle; the digits all odd or all even; twin minute digits; next-door minute digits; the hour
turning up again. The three families the judge named — `minutes = hour + n`, `minutes = n × hour`,
the fold along an unnamed diameter — are gone, and so are the sector-counted hand offsets and the
half/double pair that shared their flaw. There is no sum, product, remainder or count left anywhere
in U, and the clue is still two times plus five candidates, read aloud in one breath.
