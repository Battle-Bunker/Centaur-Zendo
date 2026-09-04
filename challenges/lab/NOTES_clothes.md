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

## crandel v2 ladder run `lad-crandel-v2-1` (2026-09-04, 6×0.5 s, 2 Opus players) — server died before the final

| team | profile | rounds 1–4 | cracked | demos |
|---|---|---|---|---|
| crandel1a | opus-default | 0, 4/455, 447/447, 534/534 | round 3 | 3 |
| crandel1b | opus-kidproxy | 0, 9/406, 459/459, 615/615 | round 3 | 2 |

No finals (the server was killed at 20:50 by crandel1b's own `pkill -f "python -"`; arena
launcher and player brief now hardened). Evidence is nonetheless clear: **both Opus players
cracked v2 in round 3**, faster than any class today. Both read the object at once ("shelves, the
stuff is hanging down", "wardrobe rail with clothes"); both imagined kids said the rule in the
first minute ("some of them nearly touch the one below"). The legibility work succeeded — and made
the class too easy for Opus.

Why it fell so fast: (1) the clue is a fingerprint with one group per shelf, so the mapping
group→shelf is free; (2) `h` and `longs` are directly countable, leaving `drips` as a one-bit
question; (3) the generator law `drips ∈ {longs−2, longs−1}` means drips is nearly determined;
(4) the missing last group says "it is about the shelf below". Levers for v3 (keep the picture
and the clue shape — they are what the kid judge rewarded): (a) let drips range 0..longs freely
so it carries information; (b) make the counted relation less nameable than "overlaps something
below": e.g. count long garments whose hem is directly above a *gap* between two garments below
(dripping onto the floor between them) — or garments that drip onto a garment of the SAME letter
(same colour bleeds) — pick by witness table and kid-legibility; (c) make `longs` not directly
visible (e.g. count garments that reach the rail below *and* something else). Do not drop the
group-per-line clue shape or the drawn drips.

---------------------------------------------------------------------------

# crandel v3 — hardening pass (refiner, 2026-09-04)

v2 was **too easy**: in `lad-crandel-v2-1` both Opus players reached 100 % in round 3 (see the
run table above). The kid judge's complaint had been fixed and must stay fixed, so the picture,
the clue shape and every legibility decision of v2 are **unchanged**; only the counted relation
and the `drips` law moved.

## What the players actually did (read from their code, not their prose)

Both `crandel1a` and `crandel1b` finished with the *same* construction, invented independently:
a **slot grid**. Items 1–2 columns wide on a fixed pitch (2 or 3), every item on a slot, every
one of a line's `a` items drawn **full height**; line *i*'s slot interval is shifted by
`a_i − b_i` so exactly `b_i` slots are shared with the line below. 1b: `IW=1, SLOT=2`; 1a:
`pitch 2` / `pitch 3` alternating by `memory["_index"]`. Both wrote down the same three
assumptions: *"letters, item widths, gap widths and the picture width are all free"*, *"the last
block has nothing below it, so only its height is specified; its contents are free"*, and
`b ∈ {a−2, a−1}` (1b verified that law over 2192 groups and used it to prune hypotheses).
Round 2 was a wrong model that still scored 4/455 and 9/406 — and **those accidental hits were
the crack**: 1b's notes say the pattern of which layouts scored *"only made sense as a relation
between neighbouring blocks"*. Two demos each; round 3 onwards 100 %.

The fatal property of v2 is not that "overlaps something below" is guessable — it is that inside
a slot grid of full-height items **every refinement of it collapses to the same number**. A
witness that never draws a short garment underneath, never draws an overhang and never leaves
daylight cannot tell the rule from its neighbours, so no insight beyond "shared slot" is needed.

## What changed in v3

1. **`drips` ranges freely over `0..longs`** (lever: reduce clue determinism). v2's generator law
   `drips ∈ {longs−2, longs−1}` left the third digit almost fixed once `longs` was read, and 1b
   used it as a pruning law. The only clause left in `generate()` is a rejection: not *every*
   line may have `drips == longs`, because such a picture cannot be drawn with the v2 reading
   falsified (if every long garment counts, "overlaps something below" agrees on every line).
   Distinct clue classes: **~6 500 → ~12 000**.
2. **The counted relation is now "hangs over a GAP"**, not "overlaps something". A garment counts
   if it hangs all the way down to the line below **and** part of it is over the **daylight
   between two garments of that line** — *it is dripping through onto the floor between two
   things instead of onto the washing.* Kid sentence, one line: *"that towel's so long it
   reaches the next line, and it's dripping straight down the gap between the shirt and the
   socks."* Three-word test: there is no name for it; it is not "overlap", not "cover", not
   "aligned".
   * It is **not dodgeable by the crack**: on a slot grid nothing ever overhangs a gap, so the
     shipped round-4 code of both players scores **0.4 % / 0.0 %** on v3 (it scored 100 % on v2).
   * The two candidates the run notes also proposed were measured and rejected. *"drips onto a
     garment that is itself long"* (the cascade): pretty, but the players' own witness still
     scores **90.5 %**, because in a grid of full-height items "onto a long one" **is** "onto
     anything" — it hardens nothing anybody actually builds. *"drips onto a garment of the same
     letter"*: kills the crack (0 %) but flattens every rival to ≈0 (random-among-the-longs
     **0.5 %**), i.e. a wall of zeros, which DESIGN_LOOP lever 7 says turns players into demo
     farmers. The gap rule keeps a foothold at **8.8 %**.
3. **`longs` kept as it is** (the brief's optional lever (c) was considered and dropped). It is
   the foothold — the one statistic a player can read straight off a demo — and it still forces
   spare non-counted long garments into every picture. Making it conditional would have removed
   the only cheap probe that pays.
4. **Salience (lever 9), the reason the kid score should hold.** `solve()` draws each line on
   purpose from the bottom up: a **counted** garment either sits squarely *inside* the daylight
   between two garments below, or straddles the whole gap with an overhang on each side; a long
   garment that does **not** count is tucked **entirely over one garment below** (the water lands
   on the washing), and one per picture is hung **past the end of the line below** — over floor,
   but not between two things — so *"it has bare floor under it"*, the strongest rival at 39.5 %,
   is visibly false in every demo. 21 rival per-line readouts (including same-letter, onto-a-long-
   one, fully-covers, nothing-below, sits-entirely-over-one, over-two, pairs, wide/narrow/inner)
   must all differ from the drip vector before a picture is shipped.

## Witness table, v2 → v3 (500 fresh clues each, one identical harness)

Every attacker knows the picture grammar **and** the first two digits of every group, and differs
only in the law it uses for the third; each draws in its own naive style (random blocks, 20–28
wide), never in `solve()`'s style; long sets are chosen bottom-up so laws that look at the line
below can be imposed exactly. Both columns come from the same script, so they are comparable
with each other but not with the v2 table further up this file (that harness drew 1-wide sticks).

| law used for the third digit | v2 | v3 |
|---|---|---|
| **over a gap between two garments below — THE v3 RULE** | 4.2 % | **100.0 %** |
| **overlaps something below — THE v2 RULE** | **100.0 %** | 9.8 % |
| all the long ones | never buildable | never buildable |
| has bare floor under part of it | 4.5 % | **39.5 %** |
| is not at either end | 4.4 % | 16.8 % |
| drips onto a garment of the same letter | 1.2 % | 13.1 % |
| is wide (>= 3 columns) | 6.4 % | 12.4 % |
| hangs over two garments | 0.0 % | 11.7 % |
| fully covers something below | 0.6 % | 10.9 % |
| is in the left half of the line | 4.0 % | 9.9 % |
| has nothing at all under it | 5.7 % | 9.5 % |
| **random among the long ones (the foothold)** | **6.0 %** | **8.8 %** |
| drips onto a garment that is itself long | 6.4 % | 8.1 % |
| is narrow (<= 2 columns) | 6.0 % | 6.3 % |
| sits entirely over one garment below | 1.7 % | 4.4 % |
| template: identical garment columns on every line | 0.0 % | 0.0 % |
| template: the same, every garment full length | 0.0 % | 0.0 % |
| template: two garments a line | 0.0 % | 0.0 % |
| template: right rows, random hems | 0.2 % | 0.2 % |
| **template: crandel1a's round-4 code** | **100.0 %** | **0.4 %** |
| **template: crandel1b's round-4 code** | **100.0 %** | **0.0 %** |
| previous clue's answer replayed | 0.2 % | 0.0 % |
| one fixed answer for every clue (best of 15) | 0.8 % | 0.2 % |
| `solve()` | 100.0 % | 100.0 % |
| empty / junk / the clue itself | 0.0 % | 0.0 % |

The foothold is inside lever 7's 5–30 % band and went **up** (6.0 → 8.8 %); the ceiling of every
template is ≤ 0.4 %; the strongest wrong *rule* pays 39.5 %, which is the improving signal a
player is meant to climb — and the last step of that climb ("not just floor: floor **between two
things**") is the lateral one, drawn into every demo.

## Validation (shipped file)

`python tools/quickcheck.py challenges/lab/crandel.json --seeds 200` → **OK, no warnings**
(`gen=0.09 ms score=0.10 ms solve=395 ms`). Sizes: **score 509/512**, solve 4990/5000,
generate 663, clue ≤ 13 chars, solution ≤ 434/1024. `generate` mean **0.022 ms** (brief: < 1 ms),
deterministic. `solve()` scores 1 on **2000/2000** fresh clues, mean 29 ms, p95 124 ms, worst
775 ms. `score` on **20 000 junk strings**: 0 raises, 0 non-binary, 0 false positives, worst
0.13 ms. Cross-checked against an **independent grid-based re-implementation** (no regex, written
from the spec) on 15 200 mutated / shuffled / re-cased / truncated answers: **0 disagreements**.
Hypothesis elimination over a **320-readout** family (v2's 150 plus the "what is it landing on"
dimension — onto-long, onto-short, onto-wide, onto-same-letter, bare-floor, over-gap — and
letters): **6.9 survive one demo, 1.2 survive two, and the true rule is the only survivor from
demo 3 in 30/30 trials**. Pictures are 11–15 rows × 22–28 columns, 35 distinct shapes; the
counted garment is leftmost 14 % / rightmost 15 % of the time and is the widest of the long ones
49 % (v2: 53 %) — wide garments do overhang gaps more often (2-wide 50 %, 6-wide 96 %), which is
intrinsic geometry and is why "wide" is a decoy worth 12.4 % rather than a law. ~12 000 distinct
clue classes, so cache-and-replay over 6×450 probes is worth ~5–9 % of the final on top of the
~9 % blind rate: the **no-insight ceiling is ~15–18 %** (v2 ~26 %).

## Three demos as they now render

clue `331/231/3`

```
======vv==vv===vv=vv==vv
......CC..SS...TT.SS..TT
......CC.......TT.....TT
......CC.......TT.....TT
==vv==vv==v==v===v=v=v=v
..CC..SS..CCCC...TTT.CCC
......SS.........TTT.CCC
==v=v======v=v===v==v===
..CCC......SSS...TTTT...
..CCC......SSS...TTTT...
..CCC......SSS...TTTT...
```

line 1: 5 garments, 3 hang right down (`CC`, `TT`, `TT`); only the middle `TT` is over a gap —
it hangs in the daylight between `CCCC` and `TTT`. The left `CC` sits exactly on top of `SS`
and the right `TT` is tucked inside `CCC`, so both land on washing.
line 2: 5 garments, 3 hang right down (`SS`, `TTT`, `CCC`); only `SS` is over a gap (the wide
bare stretch between `CCC` and `SSS`). `TTT` is tucked over `TTTT`; `CCC` hangs past the END of
the bottom line — floor, but not between two things, so it does **not** count.

clue `342/321/2`

```
=vv==vv===v===v=vv=vv=vv
.SS..CC...SSSSS.JJ.CC.JJ
.....CC...SSSSS.JJ.CC.JJ
.....CC...SSSSS....CC.JJ
=vv======vv==v==v=v=v===
.DD......CC..JJJJ.SSS...
.DD......CC..JJJJ.SSS...
.DD..........JJJJ.......
===v==v===vv======v=v===
...CCCC...SS......DDD...
...CCCC...SS......DDD...
```

line 1: 6 garments, 4 hang right down (`CC`, `SSSSS`, `CC`, `JJ`); two are over gaps — `CC`
straddles the daylight between `DD` and `CC` below, `SSSSS` straddles the daylight between `CC`
and `JJJJ`. The other `CC` sits over `SSS`; `JJ` hangs past the end.
line 2: 4 garments, 2 hang right down (`DD`, `JJJJ`); only `JJJJ` is over a gap (between `CCCC`
and `SS`); `DD` is at the far left with nothing under it at all — floor, no gap, no count.

clue `232/331/230/4` (four lines; `drips` can now be 0, which v2 could not express)

```
=vv==v=v===v===v===vv=====
,DD,,CCC,,,TTTTT,,,CC,,,,,
,,,,,CCC,,,TTTTT,,,CC,,,,,
=vv======v=v==v=v==vv==vv=
,PP,,,,,,DDD,,CCC,,PP,,DD,
,PP,,,,,,DDD,,CCC,,,,,,DD,
,PP,,,,,,DDD,,,,,,,,,,,DD,
v===v=v=v===vv=v=v==v=v===
SSSSS,PPP,,,CC,TTT,,SSS,,,
SSSSS,,,,,,,CC,,,,,,SSS,,,
=====vv==vv=vv==vv=v====v=
,,,,,DD,,TT,DD,,CC,PPPPPP,
,,,,,DD,,,,,DD,,,,,PPPPPP,
,,,,,DD,,,,,DD,,,,,PPPPPP,
,,,,,DD,,,,,DD,,,,,PPPPPP,
```

line 1: 4 garments, 3 hang right down (`CCC`, `TTTTT`, `CC`); `CCC` and `TTTTT` are over gaps,
`CC` is tucked over `PP` — group `232`.
line 2: 5 garments, 3 hang right down (`PP`, `DDD`, `DD`); only `DDD` is over a gap — group `331`.
line 3: 5 garments, 3 hang right down (`SSSSS`, `CC`, `SSS`); every one of them lands squarely on
washing, so nothing drips through: group `230`.

## Predicted classification and kid score

**On target (testing), mean final 35–60 %.** Reasoning: the exact witness both Opus players built
now pays ≤ 0.4 %; the no-insight ceiling is ~15–18 %; the rule is one genuinely lateral step past
the reading everybody starts from, and that step is *drawn* in every demo rather than hidden, so
a player who thinks about the picture gets it in round 4–5 while a player who keeps refining
"overlap" statistics plateaus in the 10–40 % band. Expect one crack and one partial rather than
two cracks; if both crack again, the next lever is to stop naming `longs` and instead name
"how many hang right down **and** land on washing", which makes the foothold itself a conjunction.

**Kid score 4.0–4.5/5** (v2 scored 3.4 with the same picture): the object is unchanged and the
new sentence is *more* childlike than v2's — "it's dripping down the gap onto the floor" beats
"its columns overlap the washing below" — the counted thing is now a hole you can see rather
than an alignment you have to compute, and the first two digits of every group are still
countable straight off the picture, which is what the judge rewarded for kid_contributes.

**Levers if it comes out too easy**: make `longs` count only the long garments that land on
washing (so the foothold is itself the conjunction); or require the gap to be at least two
columns wide, which removes the "any sliver counts" edge and makes the count depend on a size
judgement. **If too hard**: make the last digit one total for the whole rack instead of one per
line, or guarantee that in every demo one counted garment sits wholly inside a wide gap.
