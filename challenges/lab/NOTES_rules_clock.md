# NOTES — rule-family class, world = a clock time `h:mm` (class `wisbek`)

Paradigm: `docs/RULE_FAMILIES.md`. A finite universe **U** of parametrised rules; the clue is a
minimal set of positive example times that pins exactly one rule inside U; the answer is one more
time obeying it. The player does **not** know U, so their larger hypothesis space contains obvious
rules the class never uses. Learning **what this class never says about a clock** is the game.

Shipped file: `challenges/lab/wisbek.json` (name checked unique against `challenges/` and
`challenges/lab/`). Not committed; no arena run (out of scope for this job).

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
