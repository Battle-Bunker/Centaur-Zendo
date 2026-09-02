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
