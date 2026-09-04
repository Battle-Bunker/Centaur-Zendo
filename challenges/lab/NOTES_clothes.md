# NOTES — direction: clothes, dressing and packing

Designer run 2026-09-04. Target: a class Opus centaur players crack ~half the time in
6x0.5 s rounds with 6 demos; a 12-year-old recognises the object from one demo and can
contribute hypotheses. Small drawing (a judge penalised 30-line demos). The counted
relationship must be the **headline** of every demo.

Constraints I took from the measured runs before drawing anything:
* Players rebuild the picture grammar perfectly from 1-2 demos, then hunt **statistics**.
  So the difficulty must live in *which* statistic, and every neighbouring statistic must
  be visibly false in every demo (virel, basten, garrow all do this).
* A rule outside the players' natural hypothesis space is unreachable at this cadence
  (NOTES_game conclusion: nobody ever proposed "the leap length is the mover's neighbour
  count" in six runs). So the quantity must be *pointable in the picture*, and the
  difficulty must be the last refinement step, not the whole idea.
* Named operations are read instantly (three-word test). For clothes the famous operations
  are: pairing socks, buttoning in order, folding, "does it fit in the case" (knapsack),
  "what goes on before what" (topological sort). All of those are banned.
* Counting rules protect themselves *if* hitting the exact count needs the rule, but the
  noise floor (a player who copies the format and draws at random) must be measured.

## The eight-plus ideas

| # | object (what the kid sees) | the measurement | 12-year-old test | verdict |
|---|---|---|---|---|
| 1 | **washing line with pegs** — one line, garments hung side by side | pegs that hold two garments at once | object 5/5. But "a peg does double duty" is exactly "two garments touch", the most obvious adjacency statistic on a 1-D row | **reject: too easy**, reduces to touching neighbours |
| 2 | **towel rail** — garments draped over one rail, part above, part below | garments hanging equally far above and below the rail | object 5/5, rule pointable ("that one's even, that one's lopsided"). But `above==below` is a top-3 comparison for any model given two numbers per item | **reject: too easy** (per-item equality, no relation) |
| 3 | **suitcase** — bordered box, clothes as letter rectangles packed inside | items completely hidden under exactly one other item | object 4/5, rule nice ("how many things do you have to lift?"). But the picture is a letter-rectangle grid = LegoZendo/murn/virel again | **reject: duplicates the collection's dominant object** |
| 4 | **folded stack in a drawer** | items that overhang the one below | virel's measurement with a new skin | **reject: duplicate rule** |
| 5 | **shirt front** — buttons `o` on one side, holes on the other | buttons that end up one hole out | object 5/5 but the rule IS the famous mistake; three-word test fails ("done up wrong") | **reject: nameable** |
| 6 | **packing list / outfit table** — days x garments | days that repeat yesterday's trousers | tables are the *detour* reading (fennick: "the picture reading is the rule, the table reading is the detour"); models regress tables instantly | **reject** |
| 7 | **socks on a line** — a row of letters | pairs of matching socks with exactly one thing between them | object 5/5, but "same letter at distance 2" is the first string statistic any model tries | **reject: too easy** |
| 8 | **shoe with laces** — eyelets and crossings | crossings that pass over rather than under | not drawable small; semi-famous (lacing patterns) | **reject** |
| 9 | **cloakroom pegs** — coats spilling onto the neighbouring peg | coats that cover a peg that already has a coat | object 5/5 and very social ("your coat's on my peg"), but overlapping blocks cannot be drawn in ASCII without collision | **reject: undrawable** |
| 10 | **drying rack / lines one above the other** — several lines, clothes hanging under each | garments long enough to **reach the line below** that have something hanging **directly underneath** them = "how many things are dripping on something" | object 5/5 (washing on lines, one lot above another). The rule is a conjunction of two facts a kid can point at, has no name, is not the famous operation, and sits one step past two obvious rivals ("count the long ones", "count the ones with something below") | **PICK** |
| 11 | **wardrobe rail with hangers** | garments wider than the gap to the next hanger | needs invisible geometry (hanger pitch), not pointable | reject |
| 12 | **laundry basket / ironing pile** | items ironed since last worn | invisible state, no picture | reject |
| 13 | **knitted jumper stripes** | colour changes | nameable (run-length) | reject |
| 14 | **paper doll layers** (vest, shirt, jumper, coat) | which layer is on top | topological sort, textbook | reject |

## Why #10 wins the 12-year-old test

*Object.* Three or four washing lines strung one above the other, each with clothes pegged
under it, drawn small (≤ 14 lines, ≤ 30 columns). Every kid has seen this. The pegs are
drawn on the lines (`==v===vv==`), the clothes are blocks of a letter (T-shirts, socks,
pants, jeans, dresses) of different widths and different lengths.

*Rule.* A **drip** is a garment that hangs all the way down to the line below it **and**
has a garment hanging directly under it (their columns overlap). The clue names how many
drips the picture must have. "Which ones are dripping on the washing underneath?" is a
sentence a 12-year-old says out loud; it has no name in any textbook; it is not what
washing lines are famous for.

*Why it is not free for a model.* The two obvious neighbours — "count the long ones" and
"count the ones with something under them" — are both forced to be false in **every**
shipped demo, along with ~14 other statistics of the same picture (see the witness table).
The last step, "it has to be BOTH", is what has to be paid for with a round of falsifying
probes, because demos only ever show satisfying pictures.

*Kid contribution.* The child's sentence — "that towel's so long it's touching the next
line, and it's dripping on the shirt" — is the rule. The model's sentence — "the number of
garments whose depth equals the inter-rail spacing" — is half of it.

---------------------------------------------------------------------------

# crandel v1 — the shipped class

`challenges/lab/crandel.json` (neutral invented name, unique in `challenges/` and
`challenges/lab/`). Everything below is measured, not asserted; the harnesses are in
`$SCRATCH/clothes/` (`attack.py` witness table, `hyp.py` hypothesis elimination,
`test.py` junk + independent scorer + template leak + caching).

## The rule, in one paragraph (private)

The clue is `gaps/longs/drips`, e.g. **`524/43/11`**. `gaps` gives one digit per LINE
(3 or 4 lines, each 2–6 rows, total 6–11): how many rows of air hang under that line.
`longs` and `drips` give one digit each per line **except the last**. The answer is an
ASCII drying rack, every row the same width (the drawer picks 26–32): a row made only of
`=` and `v` is a line (the `v`s are pegs, cosmetic and unchecked), every other row is air;
a **garment** is a horizontal run of one capital letter that hangs from the line above —
it must appear in the top row of its block and the identical run must repeat down to its
hem, so garments are rectangles and each row's runs are a subset of the row above.
Everything else — filler character, letters, widths, hems, pegs, how many garments — is
free. Two numbers are pinned per line (except the last): **`longs[i]`** = how many
garments on line *i* hang all the way down to the line below, and **`drips[i]`** = how
many of *those* have at least one garment hanging directly underneath them from the next
line (their columns overlap) — *"of the ones that reach, how many are dripping on the
washing below."* `drips[i] < longs[i]` always, so every line always shows at least one
long garment hanging over a bare stretch.

## Intended discovery path

1. **One demo → the object.** Lines with clothes pegged under them, one lot above another.
2. **1–2 demos → the grammar.** Measured player behaviour is that they rebuild picture
   grammars perfectly; nothing here resists that, and nothing should.
3. **Field 2 is the foothold** (DESIGN_LOOP lever 7): "how many hang right down to the
   line below" is the obvious statistic and is readable off one demo. Getting it alone
   scores **12.6 %** — a real, improving signal, not a wall of zeros.
4. **Field 3 is the lateral step.** It is a *subset* of the long garments, and the two
   neighbouring readings are dead on arrival: "all the long ones" *is* field 2, so it is
   visibly not field 3; "the ones with something underneath" is falsified on every line of
   every demo (every line always carries a short garment that does have something below).
   What is left is the conjunction, which is what a kid says out loud: *that one's so long
   it's touching the next line, and it's dripping on the shirt underneath.*

## The witness table (500 fresh clues)

Every attacker knows the picture grammar **and** field 2 perfectly and builds a legal rack;
they differ only in the law they use to choose which of their long garments should count.

| law used for field 3 | built | scores |
|---|---|---|
| **has a garment underneath — THE RULE** | 500 | **100.0 %** |
| fully covers a garment below (a refinement) | 491 | 25.5 % |
| is not at either end of the line | 352 | 16.8 % |
| hangs over two garments | 37 | 16.2 % |
| is wide (≥ 3 columns) | 500 | 15.2 % |
| is in the left half of the line | 500 | 13.6 % |
| **random choice among the long ones (= field 2 only)** | 500 | **12.6 %** |
| is narrow (≤ 2 columns) | 491 | 9.4 % |
| **template: identical garment columns on every line** | 500 | **0.0 %** |
| template: two garments a line | 500 | 0.0 % |
| previous clue's answer replayed | 500 | 0.0 % |
| one fixed answer for every clue (best of 15) | 500 | 0.6 % |
| `solve()` | 500 | 100.0 % |
| empty / `"0"` / `"x"` / `"1"*100` / `"T"*4000` / `"="*30` / the clue itself / a blank rack | — | 0.0 % |

**The template row is the whole reason the clue has three fields.** An earlier version
pinned only the drip count per line. Against that version the *aligned-columns* template —
put the garments at the same columns on every line, so every long garment automatically has
something under it — scored **87.4 %**, because under alignment every rival reading
(long / dripping / pairs / wet / covering) collapses to the same number and the wrong,
much simpler law "the digit counts the long ones" wins without insight. Naming `longs`
in the clue makes the spare long garments **mandatory and non-dripping**, which kills that
template outright (87.4 % → 0.0 %) and — unlike a hidden "there must be a spare long one"
clause — never taxes a player who *has* the rule but draws a tight witness. (basten's
lesson: a positive-only clause costs the player who is right and buys nothing.)

## Hypothesis elimination (fairness floor)

A family of 150 per-line readouts (any/long/short × below / nothing-below / two-below /
covers / covered-by × wide/narrow × inner-only, plus pair counts and lower-line counts),
evaluated on shipped demos: **6.2 survive one demo, 1.5 survive two, and the true rule is
the only survivor from demo 3 onwards in 30/30 trials.** The demos are informative; the
difficulty is generating the hypothesis, not eliminating it — which is exactly the split
NOTES_game's conclusion says a class must respect.

## Leak checks on `solve()` itself (600 demos)

* the counted garment is the leftmost on its line 26 % of the time, the rightmost 13 %;
  it sits at index 0–6 with a smooth spread — no positional template.
* by width: 388 / 412 / 878 of the counted ones are 1 / 2 / ≥3 wide against 1603 / 965 /
  1314 of all long garments, i.e. wide garments overlap more often (intrinsic geometry).
  "The widest of the long ones" is the counted one 69 % of the time, but as a *law* it
  pays only 15.2 % because the count still has to come out exactly right on every line.
* filler is one of `. , :` at random, letters are a random 3–5 of `TSPJDCHV` with no
  repeat next door, width 26–32, height 10–15, 41 distinct (height, width) shapes.
* `solve()` re-parses its own picture with a byte-identical copy of the scorer before
  returning it, and never emits the minimal witness.

## Validation

`python tools/quickcheck.py challenges/lab/crandel.json --seeds 200` → **OK, no warnings**
(`gen=0.07 ms score=0.13 ms solve=71.97 ms`). Sizes: **score 506/512**, solve 4737/5000,
generate 545, clue ≤ 12 chars, solution ≤ 494. `generate` mean **0.017 ms** (cap 100 ms,
brief asked < 1 ms), deterministic. `solve()` scores 1 on **5000/5000** fresh seeds, mean
12.9 ms, worst 84 ms. `score` on **20 000 junk strings**: 0 raises, 0 non-binary, 0 false
positives, worst 0.24 ms. Scorer cross-checked against an **independent grid-based
re-implementation** (no regex, written from the spec) on 15 200 mutated / shuffled /
re-cased / truncated answers: **0 disagreements**. ~9 800 distinct clue classes, so
brute-force-and-cache over 6×450 probes is worth ~12 % of the final *on top of* the 12.6 %
blind rate — i.e. the no-insight ceiling is ≈ 22 %, and there is no smaller clue space to
farm.

## Typical demo (clue `524/43/11`: lines of 5, 2 and 4 rows; 4 and 3 long; 1 and 1 dripping)

```
v==v=========v=========vv=v
J..S.........P.........TT.J
J..S.........P.........TT.J
...S.........P.........TT.J
...S.........P.........TT.J
...S.........P.........TT.J
v=v=v=v==v=v=v=vv==vv======
SSS.P.T..S.TTT.SS..JJ......
...........TTT.SS..JJ......
vv==v=v==v=v=v========v=v==
JJ..T.J..TTT.P........JJJ..
JJ..T.J..TTT.P........JJJ..
JJ..T.J..TTT.P........JJJ..
JJ..T.J..TTT.P........JJJ..
```
Four things on the top line hang right down to the second line (`S`, `P`, `TT`, `J`) and
exactly one of them, the `P`, has something under it (`TTT`). On the second line three hang
right down (`TTT`, `SS`, `JJ`) and only `TTT` is over something (`P`). 13 lines, 27 columns.

## Predicted classification

**On target (testing → calibrated), mean final 40–60 %.** Expect one crack around round
3–5 (the demos are informative enough that a player who thinks about the picture rather
than the token stream gets there) and one player stuck in the 12–25 % band with field 2 and
a wrong subset law. Predicted kid score **4.2–4.6/5**: the object is a 5/5 (washing on
lines), the rule is a sentence a 12-year-old says before a model does, the picture is
10–15 lines, and the two clue digits per line are two instances of the same sentence rather
than two separate rules.

**Levers if it comes out too easy** (in order): drop field 2 back out of the clue and
instead require, in the scorer, that at least one long garment per line has nothing below
(kills the aligned template a different way, but taxes tight witnesses); or count only
drippers whose lower garment is *not* fully covered. **If it comes out too hard**: make
the third field a single total instead of one digit per line, or guarantee in every demo
that one counted garment is narrow and one uncounted long garment is the widest on its
line, so the width correlation stops being a distraction.

---------------------------------------------------------------------------

# crandel v2 — kid-legibility pass (refiner, 2026-09-04)

v1 was never played; the kid judge scored it **2.6/5** (object 3, rule_statable 3,
kid_contributes 2, no_prereqs 3, fun 2) with two pieces of advice: *"make the drip
relationship visually loud instead of requiring precise column alignment across a 30-wide
grid"*, and *"cue that there are three separate counted fields before the kid must
reverse-engineer that from unlabeled digit strings"*; the judge also read the letters as
solid blocks/bricks rather than clothes. The rule is unchanged. What changed is the clue's
**shape**, the rack's **scale**, and what the drawer is allowed to draw.

## What changed and why

1. **The clue is now one group per line** (DESIGN_LOOP lever 3: the clue's shape should
   match the picture, since labels are not allowed). `524/43/11` became `321/531/2`:
   group *i* is `<rows><longs><drips>`, and the last group is a single digit because the
   bottom line has nothing below it. Three groups, three washing lines. The **first digit
   of every group is directly countable off the picture** (rows of air under that line),
   so it is the key that tells a solver — or a kid — that a group belongs to a line;
   the other two digits then have an obvious owner. `gaps` was kept rather than dropped
   (lever 4) precisely because it is the group's anchor, and because dropping it collapses
   the clue space to a few hundred classes, which hands players a cheap cache attack.
2. **The picture reads as washing at a glance** (lever 1). Racks are 20-28 wide instead of
   26-32; 3-6 garments a line instead of 4-6 crammed; every garment is **2-6 columns wide**
   (v1 allowed 1-wide sticks) with **at least one column of air beside it** (v1 allowed
   garments touching, which is what read as brickwork), and the line carries a **peg `v`
   over each end of each garment** instead of pegs scattered at random.
3. **The drip is a picture, not a computation** (lever 2 + lever 9, salience). solve() now
   builds each line on purpose, from the bottom up: a garment that counts overlaps the
   washing below by **>= 2 columns**, and a long garment that does *not* count clears
   everything below by **>= 2 columns** on both sides. So a drip is an unbroken column of
   washing running through the line (hem, line, more washing), and a non-drip is a long
   garment hanging over a visibly bare stretch. No marker, nothing the scorer requires —
   the scorer still accepts a 1-column overlap; only the demos are drawn loudly.
4. `longs` is **kept** — it is load-bearing: it is what makes the spare long garments
   mandatory and non-dripping, which is what kills the aligned-columns template (87% -> 0%).

Cosmetic knock-ons: filler is `.` 75% of the time (`,` `:` otherwise), bottom-line hems
vary over the full depth, and garment widths are now drawn width-first so that "the wide
ones are the ones that drip" is much weaker than in v1 (the counted garment is the widest
of the long ones 53% of the time, was 69%).

## Witness table, before and after

Every attacker knows the picture grammar **and** how many garments hang right down on each
line, and differs only in the law it uses for the last digit; each draws in its own naive
style (v1 attackers at 26-32 wide, v2 attackers at 20-28, matching each version's rack).
v1 = 200 fresh clues, v2 = 250 fresh clues.

| law used for the last digit | v1 | v2 |
|---|---|---|
| **has washing underneath — THE RULE** | **100.0 %** | **100.0 %** |
| fully covers a garment below | 27.6 % | 11.3 % |
| is not at either end of the line | 18.6 % | 12.0 % |
| is wide (>= 3 columns) | 13.5 % | 12.4 % |
| is in the left half of the line | 12.5 % | 12.4 % |
| is narrow | 11.1 % | 11.6 % |
| hangs over two garments | 10.0 % | 2.0 % |
| **random choice among the long ones (= the foothold)** | **10.0 %** | **10.8 %** |
| template: identical garment columns on every line | 0.0 % | 0.0 % |
| template: two garments a line | 0.0 % | 0.0 % |
| template: right rows, random hems (first digit only) | — | 0.0 % |
| previous clue's answer replayed | 0.0 % | 0.0 % |
| one fixed answer for every clue (best of 15) | 0.5 % | 0.8 % |
| `solve()` | 100.0 % | 100.0 % |
| empty / junk / the clue itself | 0.0 % | 0.0 % |

The foothold survives (10.8 %, inside the 5-30 % band of lever 7) and no template moved
above 1 %. The rivals are flatter than in v1 — the one that used to pay 27.6 % ("fully
covers") is now worth no more than a coin-flip guess, because a dripper overlapping by
>= 2 columns is usually *not* a full cover.

## Validation (shipped file)

`python tools/quickcheck.py challenges/lab/crandel.json --seeds 200` -> **OK, no warnings**
(`gen=0.10 ms score=0.13 ms solve=338 ms`). Sizes: **score 506/512**, solve 4984/5000,
generate 684, clue <= 13 chars, solution <= 434/1024. `generate` mean **0.023 ms**
(brief: < 1 ms), deterministic. `solve()` scores 1 on **2000/2000** fresh clues, mean
28 ms, worst 487 ms. `score` on **20 000 junk strings**: 0 raises, 0 non-binary, 0 false
positives, worst 0.13 ms. Cross-checked against an **independent grid-based
re-implementation** on 15 200 mutated / shuffled / re-cased / truncated answers:
**0 disagreements**. Hypothesis elimination over the 150-readout family: **6.5 survive one
demo, 1.7 survive two, and the true rule is the only survivor from demo 5 in 30/30 trials**
(v1: 6.2 / 1.5). ~6 500 distinct clue classes (v1 ~9 800): cache-and-replay is worth ~18 %
of the final on top of the ~11 % blind rate, so the no-insight ceiling is **~26 %**
(v1 ~22 %). Pictures are 11-15 rows x 20-28 columns, 44 distinct shapes.

## Three demos as they now render

clue `321/531/2`

```
===v====v======v=v======vv
...DDDDDD......JJJ......PP
...DDDDDD......JJJ........
...DDDDDD......JJJ........
=v==v=v=v==vv=======v=v=vv
.PPPP.CCC..PP.......CCC.JJ
.PPPP.CCC...........CCC.JJ
.PPPP.CCC...........CCC...
.PPPP.CCC...........CCC...
.PPPP.CCC...........CCC...
===========vv==vv=v===v=vv
...........DD..PP.JJJJJ.CC
...............PP.........
```

line 1: 3 garments, 2 hang right down to line 2; 1 of those (DDDDDD) is over washing
line 2: 5 garments, 3 hang right down to line 3; 1 of those (CCC) is over washing
line 3 is the bottom line, so its group is the single digit 2

clue `231/521/3`

```
=vv==v==v=v====v==v==v==vv
.TT..SSSS.TTTTTT..DDDD..TT
.....SSSS.........DDDD..TT
=v===v=vv====v=v==========
.TTTTT.SS....DDD..........
.TTTTT.......DDD..........
.TTTTT.......DDD..........
.TTTTT.......DDD..........
.TTTTT.......DDD..........
===========v==v===v==v=v=v
...........SSSS...HHHH.SSS
..................HHHH....
..........................
```

line 1: 5 garments, 3 hang right down (SSSS, DDDD, TT); only SSSS is over washing
        (TTTTT and SS are under it) - TTTTTT is wide but stops one row short
line 2: 3 garments, 2 hang right down; only DDD is over washing (SSSS below it)

clue `332/332/332/2`

```
==v===v==v=v=v==v==v===v=
..HHHHH..VVV.DDDD..VVVVV.
..HHHHH......DDDD..VVVVV.
..HHHHH......DDDD..VVVVV.
v==v=vv=v=v========vv=v=v
DDDD.HH.VVV........HH.SSS
DDDD.HH............HH....
DDDD.HH............HH....
vv=======vv=v==v==v=v==vv
DD.......VV.DDDD..PPP..DD
DD.......VV.......PPP....
DD.......VV.......PPP....
=====vv=v==v=v=v=v==v=vv=
.....DD.SSSS.PPP.SSSS.PP.
.....DD......PPP......PP.
```

four lines of 3 rows each; on every counted line 3 garments hang right down and
2 of them are over washing, so every group reads 332

## Predicted kid score and classification

**Kid score 4.0-4.5/5** (was 2.6): object 4-5 (pegs, air between garments, 2-6 wide
rectangles at 20-28 columns read as washing, not brickwork), rule_statable 4 ("how many of
the long ones are dripping on the washing underneath"), kid_contributes 4 (the group-per-
line clue with a countable first digit lets a child match a group to a line and check the
first two numbers by counting, which is exactly the contribution the judge found missing),
no_prereqs 4, fun 3-4. **Classification unchanged: on target (testing), mean final
40-60 %** — the rule and its witness table are the same, the no-insight ceiling is ~26 %,
and the foothold still pays ~11 %.

**Levers if it comes out too easy**: count only drippers whose lower garment is not fully
covered; or drop the second digit and require in the scorer that at least one long garment
per line has nothing below it. **If too hard**: make the last digit one total for the whole
rack instead of one per line.
