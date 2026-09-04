# Direction: everyday time and place (time-agent)

The demo must be a picture a kid names in one second - a clock face, a calendar page, a bus
timetable, a seat map. The clue is tiny and pins an **arbitrary-but-natural measurement** of
that picture. Not the object's famous operation ("angle between the hands", "days between two
dates", "how long does the journey take"), and the measurement must have no name.

Constraints I applied to every candidate before scoring it:

* **Parse budget.** The scorer is 512 chars. Any picture whose *well-formedness* cannot be
  verified in ~350 chars is dead on arrival, no matter how lovely. This kills every attempt to
  draw a circular clock face in ASCII (12 hand positions + two hands + a ring = a table plus a
  geometry check; LegoZendo spends its whole budget on a much simpler tiling).
* **Completion, not free construction** (DESIGN_LOOP lever 1). If the player may choose the
  whole picture, a fixed template answer scores whenever the clue's count happens to match
  (~10-15 % free). If the clue *pins the picture's shape* and only the contents are free, a
  constant answer scores 0 on every clue and the degenerate witness is gone for free.
* **The rule must be reachable** (NOTES_game conclusion). orlan died because "the leap length
  is the mover's own neighbour count" was never generated as a hypothesis by six Opus runs. A
  0/1 channel only tests hypotheses the player already proposes. So the measurement must live
  in the family a player *does* enumerate over a picture (counts of local relations between
  marked cells) - and difficulty must come from *which* relation, not from being off the map.
* **No negative-only clauses** (NOTES_everyday lesson 2). Demos only ever show satisfying
  examples, so anything a demo cannot exhibit is invisible. Restrictions of that kind go in
  `generate()`, not `score()`.
* **Recognition necessary but not sufficient** (NOTES_everyday diagnosis). If naming the object
  hands you the rule, it is a three-word puzzle (`quilm`: "move one matchstick") and it dies in
  one demo.

## Brainstorm

1. **Analogue clock face, hands drawn on a ring.** Clue `n`; answer: a clock whose hands sit so
   that *n* hour marks lie strictly between them the short way round.
   *Kid test:* 10/10 - it is a clock. *Nameable?* Half-nameable: "the angle between the hands"
   is the single most famous clock computation and a model names the minor arc instantly; the
   marks-between count is that number divided by 30. *Parse:* fatal - a circular face needs a
   12-entry position table plus a hand-legality check, ~400 chars before any counting.
   **Rejected: parse budget + the famous operation.**

2. **Wall of city clocks (a station concourse).** Clue `k`; answer: 6 clock faces where exactly
   *k* pairs of clocks have their hour hands on the same number.
   *Kid test:* good. *Nameable?* No. *Parse:* same fatal circle problem, x6.
   **Rejected: parse budget.**

3. **Bus timetable** (rows = stops, columns = journeys, cells = HH:MM or `-`). Clue `k`; answer:
   a timetable whose times increase down every column and across every row, with exactly *k*
   legs on which the clock ticks over into the next hour.
   *Kid test:* 9/10, and "look, it goes 7:58 then 8:03" is exactly a kid's observation.
   *Nameable?* "crosses the hour" is three words but there are many rival readings (down a
   column vs across a row; do `-` cells break the chain?), so recognition is not sufficient.
   *Parse:* ~450 chars (HH:MM validity + two monotonicity directions + dashes) - possible but
   it eats the whole budget, leaving nothing to pin the *shape*, so a constant timetable would
   score ~1/8 of clues for free. **Runner-up; rejected on the free-witness rate.**

4. **Departure board.** A list of times and destinations; count pairs of departures less than
   5 minutes apart. *Kid test:* fine. *Nameable?* Yes - "trains that clash" is one hypothesis
   and the answer space is a bag of numbers, not a picture. **Rejected: it is arithmetic on a
   list, not a reading of a picture.**

5. **Street with house numbers** (odds one side, evens the other, `.` = empty lot). Clue `k`;
   answer: a street where exactly *k* houses face an empty lot.
   *Kid test:* 8/10 - the odd/even sides are a real thing kids know. *Nameable?* The
   measurement has no name. *Weakness:* the picture is a 2 x N bit pattern, and the whole
   hypothesis family is "local window predicates over a 2 x 3 window" - a model fits that
   family exhaustively from two demos. The house numbers are decoration, since they are
   determined by position. **Rejected: the feature space is too small to need triangulation.**

6. **Plane/cinema seat map with an aisle.** Clue `k`; answer: a seat map with exactly *k* empty
   seats that have a taken seat on both sides, where across the aisle does not count.
   *Kid test:* 9/10, and "nobody wants the middle seat" is kid-native. *Nameable?* "the middle
   seat" - dangerously close to a name, and again a local window predicate on a bitmap.
   **Rejected: same fitting weakness as 5, plus the rule is almost nameable.**

7. **Lift panel / floors.** Clue `k`; answer: a journey (a list of floors) that passes exactly
   *k* floors where someone is waiting without stopping. *Kid test:* 7/10. *Nameable?* fair.
   *Weakness:* the answer is a sequence of numbers, so it degenerates to arithmetic and the
   "picture" is a button grid that carries no structure. **Rejected.**

8. **A week's weather chart** (icons + temperatures). Clue `k`; answer: a chart with exactly
   *k* days that are warmer than the day before *and* cloudier than the day before.
   *Kid test:* 9/10. *Nameable?* No, and the two-way conjunction is nice. *Weakness:* seven
   columns is a tiny picture, so the count lives in 0..6 and a constant chart scores ~20 % of
   clues; scaling to a 4-week chart fixes that but the object stops being "the forecast" and
   becomes a grid of numbers. **Rejected on the free-witness rate; kept as a fallback.**

9. **Calendar month page, every day carrying a letter** (a busy family calendar: B = bins,
   S = swimming...). Clue `L/S/x/k`: the month has L days and starts in column S, and the
   letter x must satisfy a count k. *Kid test:* 10/10 - the calendar page is the most
   instantly recognised picture in the whole direction, and a kid can read letters off days.
   *Nameable?* Depends on the measurement chosen (below). *Parse:* cheap - tokens are
   `date+letter`, and the *shape* check (first row 7-S wide, middle rows 7, dates 1..L in
   order) is ~150 chars and pins the page completely, so a constant answer scores 0 always.
   **Picked.** Measurement candidates considered:
   * (a) marks in the last, ragged week row - equivalent to `d > L-7`, one hypothesis, dead.
   * (b) marks in a weekday column that occurs five times this month - "five Fridays" is
     folklore and nearly a name.
   * (c) pairs of x side by side on the page (consecutive dates that do not straddle a week
     break) - good twist, but the *only* twist, and "adjacent same-letter pairs" is the first
     thing anyone enumerates.
   * (d) **pairs of x two days apart, both on school days, in the same week** - i.e. Mon+Wed,
     Tue+Thu, Wed+Fri. **Chosen.** The distance is a free parameter (1,2,3,7 all plausible),
     the weekend exclusion is a second, independent qualifier, and both are visible in every
     demo as decoys. A kid can state it in one sentence and count it by eye; no name exists
     for it; it is not the calendar's famous operation.

10. **Advent-calendar / school timetable variants of 9.** Same page, marks are lesson names.
    Rejected only because the family calendar with one letter per day is the cheapest to
    parse and the easiest to recognise.

11. **Two-clue composition (calendar + timetable).** Rejected: two objects means two format
    gates, and orlan showed that a gate the player cannot pass produces all-zero rounds and no
    learning at all.

## Picked: idea 9(d), named `tovel` (neutral, no pun, no abbreviation)

### The rule (private)
Clue `L/S/x/k` with L in 28..31, S in 0..6, x a capital letter, k in 2..6.
The answer is the month page: week rows of seven, the first row starting in column S
(0 = Monday), the dates 1..L in order, **every** date carrying a capital letter.
Score 1 iff the page is exactly right and
`#{ d : d and d+2 both carry x, and d falls on Mon, Tue or Wed } == k`
i.e. the number of times x appears twice in the same school week with exactly one day in
between (Mon+Wed, Tue+Thu, Wed+Fri). Everything else - x next door to x, x a week apart,
x two apart across a weekend or across the week break, another letter two apart - is a decoy,
and `solve()` guarantees each of those decoys appears in every demo.

### Intended discovery path
1. One demo: "that's a calendar". The clue's `31/2/...` is the page shape (first row has
   7-2 = 5 dates). Kid-easy, and it is the gate: until the page is right, everything scores 0.
2. The letter x in the clue says *which* letter is being counted; the other letters are noise.
3. What is counted? Total x's, x's next to each other, x's a week apart, x's two apart... The
   demos falsify each of those (by construction), leaving "two apart".
4. The last step is the weekend: pairs that reach into Sat/Sun, or step over the week break,
   do not count. A player who misses this over-counts and lands in the 40-70 % partial band
   rather than at 0 - a graceful partial tier, which is what "mixed outcome" needs.

---------------------------------------------------------------------------
## Iteration 1 - `challenges/lab/tovel.json` (v1, shipped)

### Rule (private)
Clue `L/S/x/k`: `L` days in the month (28-31), the 1st falls in column `S` (0 = Monday),
`x` a capital letter, `k` in 2..6. The answer is that month's page - week rows of seven, the
first row holding `7-S` dates, the dates `1..L` in reading order, **every** date carrying a
capital letter written straight after it (`17B`). A weekday header line is allowed and ignored
(any line with no digit is skipped); tabs, extra spaces and blank lines are tolerated.
Score 1 iff the page is exactly right **and**

```
#{ d : d and d+2 both carry x, and d is a Monday, Tuesday or Wednesday } == k
```

"how many times x happens twice in the same school week with exactly one day in between"
(Mon+Wed, Tue+Thu, Wed+Fri). Everything else is a decoy: x next door to x, x directly below x
(a week apart), x two apart across the weekend, x two apart over the week break, another
letter two apart.

### Validation
`python tools/quickcheck.py challenges/lab/tovel.json --seeds 200` -> **OK**, no warnings.
`score` 389 chars (cap 512), `solve` 4635 (cap 5000), `generate` 219; clue 8 chars, solution
<= 175; gen 0.04 ms, score 0.04 ms, solve 46 ms worst / 3.2 ms average (cap 2000).
solve() scores 1 on **3000/3000** fresh seeds and re-parses its own output with a byte-copy of
the scorer before returning it.

### Self-tests (scratchpad/time/{selftest,hyp}.py, 800 fresh clues unless noted)

| attack | witness | score |
|---|---|---|
| blind | empty / spaces / newlines / `0` / `1` / `x` / `1`*100 / 4000-char junk | 0.00 % |
| blind | the clue itself | 0.00 % |
| format | date grid with no letters | 0.00 % |
| format | every day = x | 0.00 % |
| format | every day = one other letter | 0.00 % |
| blind | random 6-letter page (x20 per clue, 16 000 answers) | 2.34 % |
| minimal | one qualifying pair, rest inert | 0.00 % (k >= 2 closes it) |
| replay | another clue's demo | 0.00 % |
| constant | best single fixed answer over 200 clues | 1.50 % |
| rule | k pairs of x **next door** | 0.41 % |
| rule | k pairs of x **a week apart** | 1.03 % |
| rule | k pairs of x **three apart** | 0.00 % |
| rule | exactly k x's | 0.00 % |
| rule | k x-**cells** in qualifying pairs, not k pairs | 0.00 % |
| rule | k pairs two apart, **anywhere** | 7.91 % |
| rule | k pairs two apart **inside a week row** (weekend kept) | 17.03 % |
| rule | k pairs two apart, **avoiding the week break only** | 18.00 % |
| rule | the true rule | 100.00 % |
| shape | correct count, page laid out from column 0 (S ignored) | 13.00 % = exactly the S=0 clues |
| shape | one row / one token per line / zero-padded dates | 0.00 % |
| shape | an extra day / a dropped day / a widened last row | 0.00 % |
| shape | lower case / `17 B` instead of `17B` / numeric header line | 0.00 % |
| shape | header, no header, tabs, blank lines | 100.00 % (robust about form) |

Scorer sanity: 20 000 random junk strings -> **0 raises, 0 non-binary returns**, worst
0.102 ms; a 1200-char answer costs 0.011 ms. Independent re-implementation of the stated rule
vs the shipped scorer on 32 000 well-formed answers: **0 disagreements**.

### Fairness floor - hypothesis-elimination surrogate (`hyp.py`)
768 hand-built "count a relation between marked days" expressions (distance 1-7 x 10 window
predicates x pairs/cells x this-letter/any-letter x three gap conditions, plus 7 non-pair
counts such as total x, rows containing x, columns containing x, runs, lonely x), collapsed by
behaviour into **538 distinct functions**. Feeding real demos:

| demos | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| survivors (6 trials) | 20-92 | 6-11 | 1-5 | 1-2 | 1-2 | 1 |

3-6 demos isolate the rule - inside the 6-demo budget, and the same profile as LegoZendo.
The three surviving expressions are *aliases* of one function ("both days are weekdays" ==
"the pair starts Mon/Tue/Wed" == "same row and both weekdays"), i.e. genuinely one rule.

### Witness leaks closed by the design (not by the scorer)
* **The clue pins the picture.** L and S vary per clue, so a constant answer is wrong on
  ~96 % of clues before the count is even looked at; there is no fixed template to hill-climb.
* **k >= 2** kills the letterless page, the all-one-letter page and the single-pair witness.
* **Every date must carry a letter**, so "sprinkle a few marks" pages are rejected and the
  player has to place decoy letters deliberately.
* **solve() never emits a demo whose rival counts equal k** (10 rival counts checked), and
  every demo contains at least one x-pair reaching into the weekend, one stepping over the
  week break, one x next door to x, one x a week apart and one same-letter non-x pair - so the
  exclusions are shown positively rather than being invisible (NOTES_everyday lesson 2).
* Cosmetics randomised per clue: header style (3), alphabet size (4-5) and letters, chain
  structure of the counted pairs, decoy placement.

### Arena (DESIGN_LOOP step 3) - players NOT run (no Agent tool here)
```
pool   $SCRATCH/pool-tovel-1/tovel.json
setup  python sim/arena.py setup --run lab-tovel-1 --teams tovela,tovelb \
         --challenge-dir $SCRATCH/pool-tovel-1 --arena-root $SCRATCH/lab-tovel-1
port   45685   pid 4094   phase training   pool_size 1
team tovela  $SCRATCH/lab-tovel-1/players/tovela
team tovelb  $SCRATCH/lab-tovel-1/players/tovelb
teardown     python sim/arena.py teardown --run lab-tovel-1 && python sim/arena.py report --run lab-tovel-1
```
Expected reading of the result: **cracked** = they found "two apart, same school week";
**partial ~17-18 %** = they found "two apart in a week" but not the weekend exclusion;
**partial ~8 %** = "two apart anywhere"; **< 2 %** = the page format only.
If both crack: harden by moving the counted relation off the horizontal (count x's directly
below x two rows apart, i.e. a fortnight) or by requiring two letters (`x` then `y` the next
school day), both of which keep the object and the kid-statable sentence.
If neither gets past ~2 %: the format gate is the suspect, and the fix is to put the row
structure in the clue in words (e.g. `31/2` -> `31 days from Wed`), not to simplify the rule.

---------------------------------------------------------------------------
## Iteration 2 - 2026-09-04 - `challenges/lab/tovel.json` (v2; v1 kept as `tovel.v1.json`)

Run `sim/results/lad-tovel-v1-1`: **in band by farming, not insight**. Mean final rate 66 %
over 2 players (tovel1a 48 %, tovel1b 83 %); neither player found the rule; the kid judge
scored v1 **4.4/5** (best in the ladder), so the calendar and its rendering are untouched.

### What the players actually did (their notes)

* tovel1b, verbatim: *"A letter pattern that scores 1 keeps scoring 1 when the identity of
  every letter is renamed, so only the **shape** counts. The accepted shape depends on
  (days, start, N) only - replaying a winning shape under a different clue LETTER scored
  **173/173** (round 5)."* It shipped `patterns.json`: **108 of the 140 (days,start,k)
  triples** mapped to one canonical winning page, replayed with the letters renamed. Its own
  summary: *"Rule NOT cracked. ~400 candidate statistics ... none covered even half the 303
  known winners."* -> 83 % with no theory.
* tovel1a did the cheap half of the same thing: *"pseudo-random letters, ~45 % fill"* /
  *"period-3 stripe"* tuned per k, i.e. it hill-climbed the **density** of the marked letter
  until `count == k` came out often enough. 48 %, and its notes never mention weekdays.
* Both leaks are one leak: **the accepted set depends only on (L, S, k) and is invariant
  under renaming letters**, so (i) one accepted page per triple is worth 100 % for that
  triple forever, and (ii) "count == k" alone is hit by a tuned random page about one time
  in six (measured on v1: 16.8 % at density 0.50; the players got more by tuning per clue).

### The fix (refiner brief idea (b), strongest form): the clue names the FIRST counted day

Clue `L/S/x/k` -> **`L/S/x/k/n`**, e.g. `31/6/R/5/17`. Score 1 iff the page is exactly right,
the counted days number k, **and the earliest counted day is n**:

```
C = { d : d and d+2 both carry x, and d is a Mon, Tue or Wed }     |C| == k  and  min C == n
```

Kid sentence, unchanged in kind: *"R doubles up in the same school week with one day in
between, five times, and the first time is the 17th."*

Why (b) and not (a) or (c):

* (a) *"make the clue letter's identity matter"* - a count of x is **invariant under exactly
  the rename tovel1b used** (it renames the other letters and keeps x as x), so a per-x count
  transfers unchanged; a second clue letter `y` with its own relation does bite, but the
  attacker can re-map `y` onto whichever of the 3-4 other letters fits, and it adds a whole
  second clause to a class that no player has yet solved *once* - a too_hard risk.
* (c) *"enlarge the clue space"* - comes free with (b): 140 (L,S,k) classes become **1229**
  (L,S,k,n) classes, mean 8.8 first-days per triple, which cannot be farmed in six 0.5 s
  rounds.
* (b) also **softens** the class in exactly the place it was failing. The clue now points at
  a day where the thing happens, so "day n carries x, and so does day n+2, in every demo" is
  readable straight off the demos - the distance-2 relation stops being a guess - and because
  every demo carries a two-apart x-pair *earlier than n* that does not count, the weekend /
  week-break exclusion is shown positively instead of having to be inferred from a count.

### Also done: the judge's advice

`solve()` now requires in every demo a **weekend-reaching** pair (Thu/Fri start) and a
**week-break-crossing** pair (Sat/Sun start) **within three days of a counted pair** - both
present and adjacent in **100 %** of demos - and a non-counting pair **before day n** in
**92 %** (it is dropped only when n sits at the very start of the month). The ten rival-count
guarantees of v1 are unchanged.

### Validation

`python tools/quickcheck.py challenges/lab/tovel.json --seeds 300` -> **OK**, no warnings.
`score` **419** chars (cap 512), `solve` 4719 (cap 5000), `generate` 388; clue 11 chars,
solution <= 175. gen 0.23 ms, score 0.26 ms, solve 151 ms worst under quickcheck.
solve() scores 1 on **6000/6000** fresh seeds (22 ms average, 220 ms worst) and re-parses its
own output with a byte-copy of the scorer before returning it. Scorer: **0 raises, 0
non-binary** on 20 000 junk strings (worst 0.05 ms); **0 disagreements** with an independent
re-implementation of the stated rule on 9 000 well-formed mutated answers.

### Witness table - v1 vs v2 (600 fresh clues each; scratchpad `time2/attack.py`)

| attack | v1 | v2 |
|---|---|---|
| **HARVEST: demo for clue A, letters renamed, submitted for clue B, same (days,start,k)** | **100.00 %** | **10.7-11.5 %** |
| same, matching (days,start,k,**n**) as well | - | 100 % *(but 1229 classes; blind probing lands on one 1.5 % of the time)* |
| tuned random lettering, density 0.20 / 0.35 / 0.50 / 0.65 / 0.80 | 2.71 / 11.17 / **16.79** / 14.38 / 4.29 % | 0.62 / 1.04 / **1.46** / 1.17 / 0.54 % |
| ... of which get the count right but not the first day | - | 4.3 / 10.6 / 17.2 / 12.1 / 4.6 % |
| best constant answer | 1.50 % | 1.00 % |
| empty / spaces / newlines / `0` / `1` / `x` / `1`*100 / 4000-char junk / the clue itself | 0.00 % | 0.00 % |
| no letters / every day = x / every day = one other letter | 0.00 % | 0.00 % |
| one row / one token per line / zero-padded dates / extra day / dropped day / lower case / `17 B` | 0.00 % | 0.00 % |
| page laid out from column 0 (S ignored) | 13 % *(= the S=0 clues)* | 11 % *(= the S=0 clues)* |
| header / no header / tabs / blank lines | 100 % | 100 % |

Wrong-relation constructors on a correct page (v2 column honours the clue's first day, which
is what a player who has read the fifth field will do):

| believed rule | v1 | v2, first day honoured | v2, first day ignored |
|---|---|---|---|
| x next door to x | 0.41 % | 0.00 % | 0.00 % |
| x three apart | 0.00 % | 1.35 % | 0.00 % |
| x a week apart (directly below) | 1.03 % | 5.22 % | 0.00 % |
| x two apart, anywhere | 7.91 % | 15.00 % | 0.33 % |
| x two apart, inside a week row (weekend kept) | 17.03 % | 27.67 % | 1.67 % |
| **the true rule** | 100 % | **100 %** | 6.33 % |

Two further tiers, measured because a good player will reach them:

* **weekly-repeat template** (mark x on n, n+2, then the same two days each following week):
  32 % overall - 77 % at k=2, 54 % at k=3, 25 % at k=4, 1 % at k=5, **0 % at k=6** (the month
  runs out). It needs the anchor and the distance but not the weekend rule; the large-k clues
  refuse it, which is where the weekday clause has to be understood.
* **week-shifted replay** (slide a harvested page up or down by whole weeks so its anchor
  lands on the new n): 61 % on the ~1/3 of clues where the shift is week-aligned. Deliberately
  left open: performing it means the player has read the calendar's week periodicity and the
  meaning of the fifth field, i.e. most of the rule. It is a near-crack tier, not a farm.

### Predicted classification

Farming ceiling ~12 % (was 83 %); blind ceiling ~1.5 % (was ~48 %); a player who reads the
fifth field and the distance gets 32 %, one who also gets "same week" 28 %, one who gets the
whole rule 100 %. Expect **testing / calibrated**, mean ~0.4-0.6 over two players, with the
mean now coming from insight rather than from a lookup table. If both players crack: harden
by moving the counted relation off the horizontal (x directly below x a fortnight apart) or
by adding a second clue letter with its own relation. If both land under 10 %: the fifth
field was not read as a date - soften by widening the clue to `31/6/R/5/first=17`.

### Arena (players NOT run; the orchestrator opens it)
```
pool   $SCRATCH/pool-tovel-2/tovel.json
setup  python sim/arena.py setup --run lad-tovel-v2-1 --teams tovel2a,tovel2b \
         --challenge-dir $SCRATCH/pool-tovel-2 --arena-root $SCRATCH/lad-tovel-v2-1
```

## tovel v2 ladder run `lad-tovel-v2-1` (2026-09-04, 6×0.5 s, 2 players)

| team | profile | final | demos | how |
|---|---|---|---|---|
| tovel1a | opus-lowdemo | 88% | 2 | solid run of the clue letter from day n, length looked up per k |
| tovel1b | opus-theorist | 34% of presented (62% of answered; skipped 45%) | 6 | same run witness, only for (k, weekday) cells it had measured |

Mean 61%. The (days,start,k) farming leak is closed as intended (1b: "my accepted grids look
nothing like the reference ones"; nobody replayed demos), but v2 has a new degenerate witness the
refiner's table did not contain: a **solid stripe** of the clue letter starting on day n. A stripe
manufactures a two-apart pair on every Mon/Tue/Wed inside it, so a run of the right length
(1a measured "working days to cover" = 4,7,8,9,12 for k=2..6) scores 1 with no idea of the rule.
Neither player stated the rule; 1a called the length table "not a rule a person could ever guess"
and 1b never decoded k at all.

Kid readings both players reported missing: "that's someone's holiday block" (1a), "just count the
clue letter's days" and "weekends are different" (1b), "the header changed between demos so the
grader isn't comparing text" (1b). Note the header inconsistency is a hint they both valued.

Fix for v3 (keeps the kid sentence): a pair counts only when the day in between is NOT the clue
letter — "R, something else, R" — which is what "with a day in between" means to a kid anyway. A
solid stripe then produces zero counted pairs. Keep the anchor n, the decoy pairs, and the picture.
Have the refiner's witness table include: solid stripe from n of every length 3..16, stripe plus
scattered extras, alternating R.R.R runs (which will still be a witness — accept that, it IS the
rule), and the old farming replay.

---------------------------------------------------------------------------
## Iteration 3 - 2026-09-04 - `challenges/lab/tovel.json` (v3; v2 kept as `tovel.v2.json`)

Run `lad-tovel-v2-1`: **still in band, still not by insight**. Mean final 61 % (tovel1a 88 %,
tovel1b 34 % of presented / 62 % of answered), kid judge 4.2/5, neither player stated the rule.

### What the players actually did

* **tovel1a (opus-lowdemo, 88 %, 2 demos)** found the *solid stripe*: "letter C runs from day E
  for as long as it takes to cover W(D) working days", `W = {2:4, 3:7, 4:8, 5:9, 6:12}`. Its own
  note: *"STILL UNSOLVED: D=2 and D=5 when day E falls on a Wednesday"* and the length table is
  *"not a rule a person could ever guess"*. Nothing in its notes mentions pairs, weekends or what
  `k` counts - it treated `k` as a run-length index.
* **tovel1b (opus-theorist, 34 %, 6 demos)** reached the same witness and then *restricted* it to
  the `(k, weekday-of-n)` cells it had measured, skipping 45 % of items: *"the grader is LENIENT
  ... it wants a horizontal run of L starting exactly on day q, and a count over the Mon-Fri part
  of that run equal to p+2"*. It never decoded `k` and never mentioned two-apart pairs.
* The v1 farming leak stayed shut - 1b: *"my accepted grids look nothing like the reference
  ones"*, and nobody replayed a demo. The anchor `n` did its job; the **stripe** was the new hole.
* Kid readings both players reported wanting: "that's someone's holiday block" (1a), "just count
  the clue letter's days" / "weekends are different" (1b), and 1b used the varying header as
  evidence that *"the grader isn't comparing text"*.

**Why the stripe works against v2:** v2 counted `d` whenever `d` and `d+2` both carried `x` and
`d` was Mon/Tue/Wed, *whatever sat on `d+1`*. A solid block of `x` therefore manufactures a
counted pair on every Mon/Tue/Wed it covers, so the count is a function of the block's length
alone. Measured on 600 fresh v2 clues: a stripe from day `n` with a per-`k` best-length table
scores **87.50 %** - i.e. it reproduces 1a's 88 % exactly.

### The fix: the day in between must NOT be the clue letter

```
C = { d : d and d+2 carry x, d+1 does NOT carry x, d is a Mon/Tue/Wed }    |C| = k,  min C = n
```

Kid sentence, unchanged in kind and arguably *more* natural: *"R, something else, R - twice in
the same school week with a day in between - five times, and the first time is the 17th."* That
is what "with a day in between" already means to a 12-year-old; v2 was the loose reading.
A solid stripe now has `x` in the middle of every pair and counts **nothing**.

Everything else is untouched as briefed: the anchor `n`, the Mon/Tue/Wed clause, the decoy
guarantees, the calendar picture, the token format, the header handling.

### Second change (generate only): the clue's first day `n` now sits late

The witness that survives the fix is the **alternating run** `x . x . x . x` from day `n` with
its length tuned per `(k, weekday of n)` - and that is fair game, because building it means the
player has found the anchor, the distance 2 *and* the empty day in between; only the Mon/Tue/Wed
clause is missing, and a length table absorbs it. It cannot be closed without breaking the rule,
but it can be **starved**: an every-other-day run needs about `14k/3` days of room (it collects 3
counted pairs per fortnight), while the rule itself needs only about `7k/2` (counted starts may
be packed Mon+Wed inside one week). So `generate()` now picks `n` as the max of three uniform
draws over the days that still leave room for `k` non-adjacent counted starts.

| | uniform `n` | late `n` (shipped) |
|---|---|---|
| alternating run, `(k, weekday)` length table | 72.2 % | **57.3 %** |
| distinct `(L,S,k,n)` clue classes | 927 | 765 |
| demo replay, letters renamed, same `(L,S,k)` | 11.5 % | 24.7 % |
| blocked `x x x` shown *before* day `n` in a demo | 73.6 % | 88.9 % |

The replay figure rises because a late `n` is less spread out, but it is harmless: a player holds
at most six demos, i.e. six of the ~140 `(L,S,k)` triples, and blind pages hit ~1 %.

### Header: kept varying, deliberately

Three header styles, chosen per demo; the scorer skips any line with no digit. tovel1b read the
variation as *"the grader isn't comparing text"* - which is **true**, costs the rule nothing (the
header carries no information about it), and is exactly the affordance we want: it steers players
away from exact-replay theories (the v1 leak) and toward hypotheses about content. Making it
uniform would only make replay look more promising than it is. Recorded as a deliberate hint.

### Validation

`python tools/quickcheck.py challenges/lab/tovel.json --seeds 200` -> **OK**, no warnings.
`score` **431** chars (cap 512), `solve` 4945 (cap 5000), `generate` 675; clue 11 chars, solution
<= 175. gen 0.06 ms, score 0.05 ms, solve 196 ms worst under quickcheck.
solve() scores 1 on **3000/3000** fresh seeds (92 ms average, 226 ms worst) and re-parses its own
output before returning it. Scorer: **0 raises, 0 non-binary** on 20 000 junk strings (worst
0.05 ms); **0 disagreements** with an independent re-implementation on 9 000 mutated answers.

Demo guarantees (3000 demos): a blocked `x x x` run starting Mon/Tue/Wed **99.5 %**, one of them
*before* day `n` **89.6 %**, a Thursday-start pair (reaches the weekend) plus a Sat/Sun-start pair
(steps over the week break) **95.5 %**, some non-counting pair before day `n` **93.8 %**, and all
eleven rival counts differ from `k` in **100 %**.

### Witness table - v2 vs v3 (600 fresh clues each; scratchpad `time3/attack.py`)

| attack | v2 | v3 |
|---|---|---|
| **SOLID STRIPE from day n, length 3..16** (best length per k) | **87.50 %** | **0.00 %** |
| ... best length per k: v2 `k=2->4, 3->9, 4->10, 5->11, 6->16` | 72.7-100 % per k | 0.00 % at *every* length |
| stripe + 1 / 2 / 3 / 5 scattered extra x's (best of 3 lengths) | 85.3 / 83.8 / 79.8 / 66.2 % | 0.00 / 0.00 / 0.00 / 0.00 % |
| **ALTERNATING `x . x . x` run from n**, per-k best-length table | 51.8 % | **45.3 %** |
| ... with a `(k, weekday of n)` table (the strongest tuning) | 58.0 % | **57.3 %** |
| ... that table per k (v3): k=2 97.7 %, k=3 74.1 %, k=4 64.0 %, k=5 40.0 %, **k=6 9.5 %** | | |
| demo replay, letters renamed, same `(L,S,k)` (the v1 leak; v1 = 100 %) | 11.5 % | 24.7 % |
| ... same `(L,S,k,n)` | 100 % *(1229 classes)* | 100 % *(765 classes)* |
| tuned random lettering, density 0.20 / 0.35 / 0.50 / 0.65 / 0.80 (v1: 3.5-16.4 %) | 0.4 / 0.9 / 1.3 / 1.2 / 0.3 % | 0.1 / 0.7 / 0.5 / 1.0 / 0.4 % |
| best constant answer (best of 20 over 200 clues) | 1.00 % | 1.00 % |
| empty / spaces / newlines / `0` / `1` / `x` / `1`*100 / 4000-char junk / the clue itself | 0.00 % | 0.00 % |
| no letters / every day = x / every day = one other letter | 0.00 % | 0.00 % |
| one row / one token per line / zero-padded / extra day / dropped day / lower case / `17 B` | 0.00 % | 0.00 % |
| page laid out from column 0 (S ignored) | 11 % *(= the S=0 clues)* | 11 % *(= the S=0 clues)* |
| header / no header / tabs / blank lines | 100 % | 100 % |

Wrong-relation constructors on a correct page (v3 scorer, 300 clues):

| believed rule | first day honoured | first day ignored |
|---|---|---|
| x next door to x | 0.00 % | 0.00 % |
| x three apart | 0.00 % | 0.00 % |
| x a week apart (directly below) | 3.82 % | 0.00 % |
| x two apart, anywhere | 12.33 % | 0.00 % |
| x two apart, inside a week row | 17.67 % | 2.00 % |
| **x two apart, Mon-Wed = THE v2 RULE (gap free)** | **33.33 %** | 4.00 % |
| x . x anywhere (gap kept, no weekday clause) | 15.00 % | 0.67 % |
| x . x inside a week row (gap kept) | 20.67 % | 1.00 % |
| **the true rule** | **100.00 %** | 7.00 % |

### Fairness floor - hypothesis-elimination surrogate (`time3/hyp.py`)

840 hand-built "count a relation between marked days" expressions (distance 1-7 x 10 weekday
windows x 3 gap conditions x this-letter/any-letter x pairs/cells), 752 distinct behaviours.
Survivors after 1 / 2 / 3+ demos: **3-21 / 1 / 1** in all six trials (v1 needed 3-6 demos). The
anchor plus the blocked `x x x` runs make each demo far more informative, so v3 is *fairer* as
well as harder: the rule is reachable from two demos by a player who thinks about the picture.

### Predicted classification

Blind ceiling ~1 %; constant answers ~1 %; the stripe that carried v2's 88 % is dead (0.00 %);
farming a `(L,S,k,n)` table is out of reach in six 0.5 s rounds. The live tiers are
**33 %** (the v2 rule - two apart, Mon-Wed, gap free), **21 %** (gap kept, week row), **15 %**
(gap kept, anywhere), **57 %** (the tuned every-other-day run - anchor + distance + gap, no
weekday clause), **100 %** (the rule). Expect **testing / calibrated**, mean ~0.4-0.6 over two
players.

Honest risk: the top mechanical tier is 57 %, so *one crack plus one templater* lands at ~0.79,
i.e. `too_easy` on the mean even though the crack was earned. If that happens the next lever is
**not** another exclusion clause but the one that kills length-tuning outright: name the *last*
counted day as well as the first (`L/S/x/k/n-m`), which forces both ends of the counted set and
makes a one-parameter run infeasible without the weekday clause. If instead both players land
under 10 %, soften by spelling the fifth field (`31/6/R/5/first=17`) rather than touching the
rule. Kid score: expect **4.2-4.5/5** - the sentence got shorter and more natural ("R, something
else, R"), the picture is unchanged, and every demo now shows a three-in-a-row that does not
count, which is the kind of thing a 12-year-old spots before an optimiser does.

### Arena (players NOT run; the orchestrator opens it)
```
pool   $SCRATCH/pool-tovel-3/tovel.json
setup  python sim/arena.py setup --run lad-tovel-v3-1 --teams tovel3a,tovel3b \
         --challenge-dir $SCRATCH/pool-tovel-3 --arena-root $SCRATCH/lad-tovel-v3-1
```

## tovel v3 ladder run `lad-tovel-v3-1` (2026-09-04, 6×0.5 s, 2 Sonnet players)

| team | profile | final | demos |
|---|---|---|---|
| tovel1a | sonnet-default | 0% (skipped final) | 5 |
| tovel1b | sonnet-kidproxy | 0% | 6 |

Not evidence about v3. Neither Sonnet player discovered that the grader is a predicate (both
assumed exact byte match and hunted a per-day letter formula for the decoys); both Opus players on
v2 found the leniency by round 3. Both again called the varying header "noise", where the Opus
theorist called it the most important hint in the game. Ladder now schedules Sonnet profiles only
after every Opus profile has played a class twice. v3 needs an Opus pair — queued.

## tovel v3 ladder run 2 `lad-tovel-v3-2` (2026-09-04, 6×0.5 s, 2 Opus players)

| team | profile | final | demos | how |
|---|---|---|---|---|
| tovel2a | opus-default | 1.8% (104/104 answered) | 7 | demo cache × 26 letter renames per (days,start,k,n) family |
| tovel2b | opus-kidproxy | 0.05% | 7 | demo cache only |

v3 is too_hard (4 finals: 0, 0, 1.8, 0.05). Cause is not the rule but the loss of the foothold:
in v2 the first cheap probes (a stripe of the clue letter) scored sometimes, which told players
the grader is a predicate and that the letter placement is what matters. In v3 every cheap probe
scores 0 (stripe 0%, random lettering ~1%), so both Opus players concluded exact-match grading,
declared the decoy letters "arbitrary data", and farmed demos. 2b's imagined kid actually saw
the rule's shape — "K and O just take turns, K O K O K O", "the middle of the month is all L" —
and 2b never tested it because it believed letters were graded exactly. Three of four Opus players
on v3 called the varying header a trap; only the v2 theorist read it as the leniency hint.

v4 brief: keep the v3 rule (pair = x, not-x, x; start Mon/Tue/Wed; count k; first at n) and
restore a foothold: let k range 1..5 so that the minimal natural probe "x on day n and n+2, nothing
else x" scores 1 on the k=1 clues (~20–25% of items) — that reveals the predicate, the pair shape
and the anchor at once, and k≥2 still needs the weekday and blocked-middle clauses. Make the header
uniform (the hint job now belongs to the foothold). Re-run the template table: alternating
x.x.x from n must stay ≤ ~60%, stripes 0%, the k=1 foothold exactly the k=1 share.

---------------------------------------------------------------------------
## Iteration 4 - 2026-09-04 - `challenges/lab/tovel.json` (v4; v3 kept as `tovel.v3.json`)

Runs `lad-tovel-v3-1` (2 Sonnet) and `lad-tovel-v3-2` (2 Opus): **too_hard**, four finals
0 %, 0 %, 1.8 %, 0.05 %, kid judge 3.8/5. v2 was 88 %/34 % by a stripe template; the target is
~50 % *earned by insight*.

### What the players actually did on v3

* **tovel2a (opus-default, 1.8 %, 7 demos)** rebuilt the page grammar perfectly, established that
  the header is not graded, and then wrote: *"No rule found linking the offsets to p, q ... Treated
  as instance-specific data that only a demo can reveal."* Its final play was a cache of the 7
  demos x 26 base-letter renames - 208 precomputed strings, a dict lookup in `solve`, skip
  everything else. 104/104 answered correct, 1.8 % of presented.
* **tovel2b (opus-kidproxy, 0.05 %, 7 demos)** ran the two decisive negative experiments:
  round 3, 461 answers over 8 layout/header variants -> **0 correct**; round 6, 443 property-style
  answers (exactly n distinct letters, clue letter m times, clue letter on day m) -> **0 correct**.
  Conclusion in its notes: *"no lenient property check; the answer must equal the reference
  output"*. Final: demo cache, 3 items answered, 3 correct out of 5471 presented.
* 2b had **already seen the rule's shape** and discarded it: *"Day m always carries the clue letter
  (7/7 demos), ~0.8 % by chance, so real"* and *"long alternating stretches (20K 21O 22K 23O 24K
  25O 26K 27O) - far too regular for i.i.d. sampling, so there is structure"*. It never tested a
  pair hypothesis because it believed the letters were compared byte for byte.
* Three of the four Opus players who have seen v3 called the varying header a **trap**. Only the
  v2 theorist ever read it as "the grader isn't comparing text".

### Diagnosis: v3 removed the foothold, not just the leak

v2's stripe was a *bad* witness (it scored 88 % with no idea of the rule) but it was also the
**foothold**: the first cheap probe scored *sometimes*, which is what told v2's players that the
grader is a predicate over the letters. v3 closed the stripe and every other cheap probe with it -
solid stripe 0.00 %, random lettering ~1 %, the minimal pair probe 0.00 %, all wrong-relation
constructors <= 33 % but only reachable after the anchor was found. With a 0 % floor, the rational
read of ~900 zero-scoring probes *is* "exact match", and the rational play is demo farming. Both
Opus players made exactly that call, independently, in the same round.

This is now design principle #7 in `sim/DESIGN_LOOP.md`: **leave a foothold**.

### The fix - three changes, all in `generate()`; the rule and the scorer are byte-identical

1. **`k` now ranges 1..5, with `k = 1` on 22 % of clues.** On a k=1 clue the smallest natural probe
   - *"x on day n and on day n+2, x nowhere else"* - scores 1. It is the minimal witness of the
   rule and it hands back the four facts v3 hid: the grader is a predicate, the clue letter is what
   is graded, `n` is where it starts, `k` counts these little pairs. `k >= 2` still needs the
   Mon/Tue/Wed clause and the blocked-middle clause, so it is a first rung, not the answer.
   The mix is `1 if r.random() < 0.22 else r.choice([2,2,3,3,4,4,4,5,5,5])` = 0.22/0.16/0.16/0.23/
   0.23, skewed a little to the large `k` because the every-other-day template is near-perfect at
   k=2 (there it *coincides* with the rule and cannot be closed) and nearly hopeless at k=5.
2. **Uniform header** (` Mo  Tu  We  Th  Fr  Sa  Su` on every demo). v3 rotated three styles as a
   deliberate free hint; the measurement is in - 1 of 6 Opus players read it as the leniency hint,
   3 of 6 read it as a trap. The foothold does that job honestly now, so the cosmetic noise goes.
3. **`n` sits later for `k >= 2`**: the max of *six* uniform draws over the days that still leave
   room for `k` non-adjacent counted starts (v3: max of three, for every `k`). The every-other-day
   run needs ~`14k/3` days of room, the rule only ~`7k/2`, so a late `n` starves the template
   without touching the rule. For `k = 1` it is the max of *two* draws only: at k=1 the template
   *is* the rule, so lateness buys nothing, and a mid-month `n` leaves room before `n` for the
   decoys that make a k=1 demo readable.

### Witness table - v3 vs v4 (600 fresh clues each; scratchpad `time4/attack.py`)

Template rows fit the best run length per cell on the same clues, i.e. an optimistic ceiling.

| attack | v3 | v4 |
|---|---|---|
| **minimal probe: x on n and n+2, nothing else x** | **0.00 %** | **22.00 %** |
| ... per k in v4: k=1 132/132, k=2 0/96, k=3 0/96, k=4 0/137, k=5 0/139 | | |
| ... same probe with random other letters on the free days | 0.00 % | 22.00 % |
| **solid stripe from n**, every length 3..16, best per k | 0.00 % | **0.00 %** |
| **alternating `x . x . x` from n**, per-`k` length table | 46.00 % | 50.83 % |
| ... with a `(k, weekday of n)` table (the strongest tuning) | 56.17 % | **57.67 %** |
| ... that table per k (v4): k=1 100 %, k=2 91.7 %, k=3 61.5 %, k=4 37.2 %, **k=5 11.5 %** | | |
| **weekly pair** (n, n+7, n+14 ...): "the same day every week" | - | 31.67 % |
| ... per k: k=1 100 %, k=2 50.0 %, k=3 8.3 %, k=4 1.5 %, k=5 0.0 % | | |
| **tightest Mon/Tue/Wed packing per (k, weekday)** = the rule as an offset table | 100 % | **100 %** |
| tuned random lettering, density 0.20/0.35/0.50/0.65/0.80 | 0.0/0.3/0.7/0.2/0.2 % | 0.7/1.0/1.0/0.7/0.7 % |
| best constant answer (best of 20 over 200 clues) | 0.50 % | 1.00 % |
| demo replay, letters renamed, same `(L,S,k)` | 2.2 % | 5.8 % |
| ... same `(L,S,k,n)` (tovel2a's actual final play) | 64.2 % | 70.7 % |
| **the true rule** | 100.00 % | **100.00 %** |

Wrong-relation constructors on a correct page honouring the clue's first day (600 clues):

| believed rule | v3 | v4 |
|---|---|---|
| x next door / three apart / a week apart | 0.00 % | 0.00 % |
| x two apart, anywhere | 0.00 % | 22.00 % |
| x two apart, Mon-Wed = THE v2 RULE | 7.50 % | 26.50 % |
| x . x anywhere (gap kept, no weekday clause) | 9.33 % | 30.17 % |
| **the true rule** | **100.00 %** | **100.00 %** |
| all of the above with the clue's first day ignored | 0.00 % | 0.00 % |

Every wrong relation now *floors* at the 22 % of k=1 clues where it coincides with the rule, and
none of them reaches 31 %: the foothold pays out immediately and then stops paying.

Two notes on the template rows. The **weekly pair** ("do the same thing every week") is the one
template that satisfies the Mon/Tue/Wed clause *without knowing it* - and it is dominated by the
alternating run at every `k`, because 7(k-1)+2 days of room is far more than the rule ever needs.
The **tightest packing** row is the other end: because `generate()` only ever picks an `n` that
still leaves room for `k` non-adjacent counted starts, the greedy Mon/Tue/Wed packing always fits,
so a player who *has* the rule can play it as a 15-cell (k, weekday) offset table with no per-clue
search - the crack, once earned, is worth a clean 100 %. The gap between 57.67 % and 100 % is
exactly the Mon/Tue/Wed clause, and the experiment that closes it ("how close may the second pair
sit to the first?", swept per weekday) costs about 30 probes - a fifth of one round.

Clue space: 924 distinct `(L,S,k,n)` classes (v3: 915), 337 *effective* classes
(`1/sum p^2`; v3: 460), so a player holding 6 demos covers ~2 % of items - which is exactly the
1.8 % tovel2a scored by that route.

### Fairness floor and demo guarantees (3000 demos, `time4/hyp.py`, `time4/solvecheck.py`)

840 hand-built "count a relation between marked days" expressions: survivors after 1 demo 2-17,
after 2 demos **1**, in all six trials - unchanged from v3. Demo guarantees: a blocked `x x x` run
starting Mon/Tue/Wed in 100.0 % of demos, one of them *before* day `n` in 100.0N %, a Thursday-start
pair (reaches the weekend) 97.6 %, a Sat/Sun-start pair (steps over the week break) 99.3 %, some
non-counting pair before day `n` 98.3 %, and all eleven rival counts differ from `k` in 100 %.

### Validation

`python tools/quickcheck.py challenges/lab/tovel.json --seeds 200` -> **OK**, no warnings.
`score` **431** chars (unchanged, cap 512), `solve` **4879** (cap 5000), `generate` 721; clue 11
chars, solution <= 175. gen 0.09 ms, score 0.06 ms, solve 163 ms worst under quickcheck.
solve() scores 1 on **3000/3000** fresh seeds across all five `k` (95.5 ms average, 197 ms
worst). Scorer: 0 raises, 0 non-binary on 20 000 junk strings (worst 0.066 ms); **0 disagreements** with an
independent re-implementation of the stated rule on 9 000 mutated answers; 0 on empty / spaces /
newlines / `0` / `1` / `x` / `1`*100 / a 4000-char junk string / the clue itself.

### Predicted classification

The tiers are now blind ~1 %, demo cache with renames ~2 %, **the natural first probe 22 %**, the
tuned every-other-day run **51-58 %**, the rule **100 %**. The 22 % floor alone puts any player who
runs one honest experiment above `too_hard` (< 15 %). Expect **testing / calibrated**, mean
**0.45-0.65** over two Opus players. Honest risk in the other direction: a crack (100 %) plus a
templater (58 %) means 0.79, just inside `too_easy` (> 0.8); if that happens the next lever is the
one held back from v3 - name the *last* counted day as well as the first (`L/S/x/k/n-m`), which
forces both ends of the counted set and makes a one-parameter run infeasible. Kid score: expect
**4.2-4.5/5** (v3 scored 3.8). The rule sentence is unchanged, the header no longer varies between
demos, and the k=1 pages are the clearest picture the class has ever had: one `x . x` on a
Monday-to-Wednesday, and everything else deliberately not counting.

### Arena (players NOT run; the orchestrator opens it)
```
pool   $SCRATCH/pool-tovel-4/tovel.json
setup  python sim/arena.py setup --run lad-tovel-v4-1 --teams tovel4a,tovel4b \
         --challenge-dir $SCRATCH/pool-tovel-4 --arena-root $SCRATCH/lad-tovel-v4-1
```

## tovel v4 ladder run `lad-tovel-v4-1` (2026-09-04, 6×0.5 s, 2 Opus players)

| team | profile | final | demos | reading |
|---|---|---|---|---|
| tovel1a | opus-lowdemo | 29% (1505/1505 answered) | 2 | "L on day m then every other day, k+1 times"; k=1 100%, k=2 Monday 100%, skipped the rest |
| tovel1b | opus-theorist | 29% (1190/4124) | 6 | same chain; saw from the 0% cells that the run "skips the weekend and resumes next week" but ran out of rounds |

Mean 29% — the foothold works exactly as designed (k=1 pays 100%, first hits in round 3), both
players reached "every other day from m" by insight, and both stalled at the same wall: the
chain must restart after the weekend (the Mon/Tue/Wed-start clause). 1b's kid line is the rule:
"swimming's on Mondays, Wednesdays and Fridays … and picks up again next week". 1a's: "a child
reads the grid; I read the string".

Status: testing (2 finals on v4, both partial, no crack). The class now has a clean gradient
(0 → 1% → 22% foothold → 29% chain → 57% tuned run → 100%). Two more Opus finals decide; if
both again stall at ~30%, the softening lever is a demo guarantee: every demo must contain a
counted pair in the SAME week row as a non-counting pair that straddles the weekend, adjacent to
each other, so the week boundary is the loudest contrast in the picture. Do not touch the rule.

## New format note (2026-09-04, 4 rounds / 3 demos / 7 classes)
First 7-class run: the kid-proxy player spent 2 of its 3 demos on tovel v4 (most frequent class,
"the clue looked like a date") and still scored 0/51 on it; a demo-less player cannot even tell
the answer is a calendar page from `31/6/R/5/17`. v5 brief: put the object in the clue — the clue
IS the blank month page (header + day numbers, no letters) plus `R/5/17`; the answer is the same
page with a letter on every day. Shape then reads off the clue with no demo; the rule still needs
one. Scorer must ignore the clue's own layout (regenerate from days/start) or compare cells.

## Iteration 5 - 2026-09-04 - `challenges/lab/tovel.json` (v5; v4 kept as `tovel.v4.json`)

### Why: the class fails the new format's *first* half, not its second

`lad-tovel-v4-1` (old format) ended 29 % / 29 % - the foothold worked, both Opus players reached
"every other day from m" and stalled at the week boundary. Then the format changed to **7 classes,
4 rounds, 3 demo requests per team**, and the first 7-class run said something different: the
kid-proxy spent **2 of its 3 demos** on tovel v4 - the most-seen class, "the clue looked like a
date" - and still finished **0/51**. A player without a demo cannot tell from `31/6/R/5/17` that
the answer is a *calendar page*: not the type, not the size, not the convention. That is
DESIGN_LOOP's demo-economy test failed at step one ("the clue alone must reveal the shape of an
answer"), and it is expensive twice over: the team burns demos to learn the *format* rather than
the rule, and a team that spends its demos elsewhere scores a flat 0 instead of a foothold.

### The change: the clue IS the blank month page

The rule is untouched. `score()` grades the letters exactly as v4 did. What changed is the
picture: the clue now carries the object, and the answer is that picture edited (DESIGN_LOOP,
"the most reliable way to reveal the answer's shape").

```
 Mo  Tu  We  Th  Fr  Sa  Su          <- the same header the answer may use
                 1.  2.  3.
 4.  5.  6.  7.  8.  9. 10.          <- every day printed "%2d." - a dot where a letter goes
11. 12. 13. 14. 15. 16. 17.
18. 19. 20. 21. 22. 23. 24.
25. 26. 27. 28.
H/1/26                               <- the letter, how many, the first one
```

* the whole page is 145-182 chars (cap 1024); the cells are 3 wide and the answer's cells
  (`"%2d%s"`, e.g. `26H`) land in exactly the same columns, so "send this back with a letter on
  every day instead of the dot" is legible without any demo;
* `days` and `start` are no longer in the code line: the scorer derives them from the page
  (line 0 = header, lines 1..-2 = the week rows, last line = `x/k/n`), `L` = number of dated
  cells, `S` = 7 - (cells in the first week row). It never trusts the *answer's* header - the
  answer's row structure must still be `7-S`, then rows of 7, then 1..7, exactly as in v4 -
  so the clue's layout is regenerated from days/start rather than copied out of the answer;
* returning the clue's page unchanged scores **0** for free: a cell must end above `"9"` and
  `"."` does not.

`score` grew 431 -> **496 chars** (cap 512) for the page parsing; `solve` 4879 -> **4935**
(cap 5000) for the same reason (three comments shortened to fit); `generate` 721 -> 1055.
`k`, the `k=1` share, the placement of `n`, every decoy guarantee and all of `solve()`'s demo
variety are **byte-for-byte the v4 logic**.

### Witness table - v4 vs v5, 600 fresh clues, both re-measured today (`scratchpad/time5/attack.py`)

Template rows fit the best run length per cell on the same clues, i.e. an optimistic ceiling.
The two new rows are what a **demo-less** player can do with the clue in front of them.

| attack | v4 | v5 |
|---|---|---|
| **NEW: clue page returned unchanged** (cells still end in `.`) | - | **0.00 %** |
| **NEW: clue page with the clue letter on every day** (the stripe) | - | **0.00 %** |
| **NEW: well-formed page from the clue alone, random letters A-Z** | - | **0.00 %** |
| ... same, random over a 4-letter alphabet containing `x` | - | 0.67 % |
| **minimal probe: x on n and n+2, nothing else x** | 22.00 % | **22.00 %** |
| ... per k: k=1 132/132, k=2 0/96, k=3 0/96, k=4 0/137, k=5 0/139 | | |
| ... same probe with random other letters on the free days | 22.00 % | 22.00 % |
| **solid stripe from n**, every length 3..16, best per k | 0.00 % | **0.00 %** |
| **alternating `x . x . x` from n**, per-`k` length table | 50.83 % | 50.83 % |
| ... with a `(k, weekday of n)` table (the strongest tuning) | 57.67 % | **57.67 %** |
| ... per k: k=1 100 %, k=2 91.7 %, k=3 61.5 %, k=4 37.2 %, **k=5 11.5 %** | | |
| **tightest Mon/Tue/Wed packing per (k, weekday)** = the rule as an offset table | 100 % | **100 %** |
| tuned random lettering, density 0.20/0.35/0.50/0.65/0.80 | 0.7/1.0/1.0/0.7/0.7 % | 0.7/0.5/0.3/0.3/0.7 % |
| best constant answer | 1.00 % | 0.50 % |
| demo replay, letters renamed, same `(L,S,k)` | 34.83 % | 34.83 % |
| ... same `(L,S,k,n)` | 70.67 % | 70.67 % |
| **the true rule** | 100.00 % | **100.00 %** |

Wrong-relation constructors on a correct page honouring the clue's first day (600 clues) are
identical in the two versions, as they must be - the rule did not move: x next door / three
apart / a week apart **0.00 %**, x two apart anywhere **22.00 %**, x two apart Mon-Wed (the v2
rule) **26.50 %**, `x . x` anywhere with the gap kept **30.17 %**, the true rule **100.00 %**;
with the clue's first day ignored, all of them 0.00 %.

*Correction to the v4 entry above:* re-running the same script on `tovel.v4.json` today gives
**34.83 %** and **70.67 %** for the two demo-replay rows, not the 5.8 % / 70.7 % recorded in the
v4 notes; the 5.8 % was a harness artefact. The honest figure for both versions is that a team
which caches one solved page per `(month shape, k)` and renames its letters wins ~35 % of the
clues that share that key - but the clue space is **867** distinct `(L,S,k,n)` classes (**334**
effective), so with 3 demos for 7 classes that route is worth ~1 % of items overall.

### One demo as it renders (seed 900004, k=1)

```
CLUE                                 ANSWER
 Mo  Tu  We  Th  Fr  Sa  Su           Mo  Tu  We  Th  Fr  Sa  Su
                 1.  2.  3.                           1Y  2A  3Y
 4.  5.  6.  7.  8.  9. 10.           4A  5S  6H  7S  8A  9A 10Y
11. 12. 13. 14. 15. 16. 17.          11S 12H 13H 14H 15Y 16Y 17Y
18. 19. 20. 21. 22. 23. 24.          18S 19Y 20A 21H 22S 23H 24S
25. 26. 27. 28.                      25H 26H 27A 28H
H/1/26
```

The month starts on a Friday (`S=4`). `H`-pairs two apart: **12-14** (Tue start, but the middle
day is `H` too - blocked), **21-23** (Thu start - it reaches the weekend), **23-25** (Sat start -
it steps over the week break) and **26-28** (Tue start, middle day `A`) - so exactly one counts
and it is day 26, which is what `H/1/26` says. All three kinds of negative evidence are in this
one picture, two of them before day `n`.

### Fairness floor, demo guarantees, validation

`scratchpad/time5/hyp.py`, 840 hand-built "count a relation between marked days" expressions
(distance 1-7 x 10 weekday windows x 3 gap conditions x this-letter/any-letter x pairs/cells):
survivors after 1 demo **2-11**, after 2 demos **1-2**, after 3 demos **1**, in all six trials.

Demo guarantees over 3000 demos (`time5/solvecheck.py`), all within noise of v4: a blocked
`x x x` run starting Mon/Tue/Wed in **100.0 %** of demos, one of them *before* day `n` in
**94.6 %**, a Thursday-start pair (reaches the weekend) **96.9 %**, a Sat/Sun-start pair (steps
over the week break) **98.7 %**, some non-counting pair before day `n` **98.4 %**, four or more
distinct letters **100 %**.

`python tools/quickcheck.py challenges/lab/tovel.json --seeds 200` -> **OK**, no warnings.
`score` **496** chars (cap 512), `solve` **4935** (cap 5000), `generate` 1055; clue 145-182
chars (cap 1024), solution <= 175. gen 0.07 ms, score 0.05 ms, solve 159 ms worst under
quickcheck. solve() scores 1 on **3000/3000** fresh seeds - 669/669, 457/457, 481/481, 746/746, 647/647
at k=1..5, exactly the v4 counts (the parameter draws are untouched) - 94 ms average, 192 ms
worst.
The scorer never raises and never returns a non-binary value on 20 000 random junk strings
(worst 0.092 ms), scores 0 on empty / spaces / newlines / `0` / `1` / `x` / `1`*100 / a
4000-char junk string / **the clue itself**, and agrees with an independent re-implementation of
the stated rule on 9000 mutated well-formed answers with **0 disagreements**. Shape attacks on a
page with the correct count: header or no header **100 %**, tabs + blank lines **100 %**; one
row, one token per line, zero-padded dates, lower case, `"17 B"` spacing, a dropped day **0 %**;
a page laid out from column 0 scores **0.12** = the `S=0` clues.

### What a demo-less player can infer, and what still costs a demo

From the clue alone: the answer is *this* month page with one capital letter on every day, and
the letter named on the last line is obviously the marker - so a demo-less team produces
well-formed answers immediately (worth ~0-1 % by luck), and the first honest experiment,
"put `x` on day `n` and on day `n+2`", pays **22 %** (all the `k=1` clues). What it cannot get
from the clue: that a pair whose middle day also carries `x` does not count, and that a pair only
counts if it starts on a Monday, Tuesday or Wednesday. That is what the demo teaches, and it is
worth 22 % -> 58 % -> 100 %.

### Predicted classification

Tiers: blind but well-formed ~1 %, the natural first probe **22 %**, the tuned every-other-day
run **51-58 %**, the rule **100 %**. Under 4 rounds x ~60 probes per class, a team with a demo
should reach the pair hypothesis in round 2 and the week-boundary clause by round 4 about half
the time; a team without one should sit at the 22 % foothold instead of 0. Expect
**testing / calibrated**, mean **0.3-0.6**. Kid score should rise from v4's expected 4.2-4.5:
the object is now visible before any demo at all. Risk in the other direction: if a player
cracks it (100 %) while the other runs the tuned template (58 %) the mean is 0.79, just inside
`too_easy`; the lever held back is still the same one - name the *last* counted day as well as
the first (`x/k/n-m`), which forces both ends of the counted set.

### Arena (players NOT run; the orchestrator opens it)
```
pool   $SCRATCH/pool-tovel-5/tovel.json
setup  python sim/arena.py setup --run lad-tovel-v5-1 --teams tovel5a,tovel5b \
         --challenge-dir $SCRATCH/pool-tovel-5 --arena-root $SCRATCH/lad-tovel-v5-1
```
