# Direction: an invented board game (lateral)

Clue = a tiny ASCII position (<= 6x6) in a game nobody has heard of, 2-3 piece types.
Answer = a move `r,c>r,c` that is legal under hidden rules AND achieves a hidden goal.
Scorer (<=512 chars) must verify legality + goal from the clue alone.

Design constraints from DESIGN_LOOP.md:
* the *rule space* must be large, not the move space (blind probing gets ~2,700 binary
  probes over 6 rounds, but every clue is a fresh position, so probing can only teach
  statistics about the rule, never memorise an answer);
* most legal moves must NOT achieve the goal (else "enumerate + guess" wins);
* no trivial/constant move may work;
* the goal must not be achievable without the movement law.

## Brainstorm (6+)

1. **MIRRORJUMP** - a piece moves by jumping over an orthogonally adjacent piece of the
   *other* type and landing on the mirror square. Goal: reach the far edge.
   *Reject*: this is exactly a checkers jump; chess/checkers priors nail it in one demo.

2. **PUSHLINE** - moving a piece pushes the whole contiguous line of pieces ahead of it
   one square; goal: push an enemy off the edge.
   *Reject*: Abalone/Sokoban prior, and "shove the guy nearest the rim" is a heuristic
   that scores without the rule.

3. **COUNTLEAP + FREEZE**  <-- chosen
   Step length k of a piece = number of *orthogonally adjacent occupied* squares (of any
   kind). It leaps exactly k squares orthogonally (jumping over whatever is in between)
   onto an empty square. k=0 => the piece is stuck. You move one `o`.
   Goal: after your move **no `x` has any legal move** (same law).
   * Movement depends on neighbour count => "how far" is not a property of the piece, it
     is a property of the *position*; chess/checkers priors give nothing.
   * Isolated pieces being immobile is the exact inverse of every game they know.
   * Goal reuses the movement law => one insight is not enough, you must have the law
     *exactly* right, and the same law twice.
   * The winning move is usually "land on the one square the enemy needed" or "step away
     so the enemy's count changes and its landing squares vanish" - both are real
     insights, neither is visible as a picture in a demo.

4. **PARITYSWAP** - a piece may swap with the piece at the point-reflection of the board
   centre; goal: make the position symmetric.
   *Reject*: goal is visible in the demo picture; one demo cracks it.

5. **SHAPEGOAL** - novel movement + goal "the three `o` end up collinear and evenly
   spaced". *Reject as goal*: the demo shows the finished shape, so the goal leaks for
   free; keeps only the movement half hidden. (Kept as a fallback softener.)

6. **DEGREEHOP** - move distance = number of *enemy* pieces in the 8-neighbourhood,
   direction diagonal. Same family as 3 but the mismatch (diagonal move, count all 8)
   is arbitrary rather than elegant - harder to *justify* once found, so less fair.

7. **SURROUND** - move so that some `x` ends up with 4 occupied orthogonal neighbours
   (custodial capture). *Reject*: Go/Othello prior, and it is visible in the demo.

8. **INERT THIRD TYPE** - add `#` blocks that never move but do count as neighbours and
   do block landings. Adopted as a *modifier* of 3: it adds a genuine, probe-testable
   question ("do walls count?") without costing scorer characters, and it makes the
   positions denser without adding mobile pieces.

## Chosen: idea 3 + modifier 8, named `orlan` (neutral, random-looking)

Rule space a player must search (each axis independently plausible):
  * what counts for k: all pieces / only enemies / only friends / walls or not
  * neighbourhood for k: 4-orth / 8 / 4-diag
  * move geometry: orthogonal / diagonal / any; leap vs. clear path; exactly k vs. up to k
  * who moves: `o` / any / `x`
  * goal: freeze enemy / capture / shape / escape / reach a square
That is a few thousand hypotheses; each probe returns one bit. Demos give
(position, winning move) pairs which pin the geometry down fastest - the intended path.

Anti-leak checklist for the generator:
  * >= 6 legal `o` moves, exactly 1 winning => "know the movement law, guess" pays ~1/6.
  * at least 2 mobile `x` before the move (so "the x were already frozen" is false, and a
    null/constant answer cannot work).
  * at least one `o` with k = 0 (immobile) in every position, so the "every piece can
    always move somewhere" prior is contradicted in every single clue.
  * winning move distances vary over 1..3 across seeds; source/target squares uniform-ish.
  * the winning move must not be recoverable by any of the cheap heuristics I test
    offline (see SURROGATE tests below).

---------------------------------------------------------------------------
## Iteration 1 - `challenges/lab/orlan.json` (v1, shipped)

### Rule (private)
Clue: a 5x5..6x6 position, `.` empty, `o` yours, `x` enemy, `#` immovable block.
Answer: one move `r,c>r,c`, 0-indexed (scorer reads any four integers in order).
* **Step length** of a piece = how many of its four orthogonal neighbours are not empty.
  `#` counts. **The board rim counts** (off-board reads as a wall). Step 0 => stuck.
* **Move**: leap exactly that many squares orthogonally, over anything in between, onto an
  on-board empty square. You move an `o`.
* **Goal**: after the move, **no `x` has a legal move** under the very same rule.

### Validation
`python tools/quickcheck.py challenges/lab/orlan.json -v` -> `OK`, **no warnings**,
`gen=2.99ms score=0.10ms solve=0.07ms`; `--seeds 200` -> `OK` (`gen=6.02ms`).
Sizes: generate 3391, solve 881, **score 508 / 512**.

### Self-tests (scratchpad/game/*.py, 1000-1200 fresh seeds unless noted)
| test | result |
|---|---|
| `solve` scores 1 on every seed | 1200/1200 |
| brute force *all* `a,b>d,e` over the whole board (400 clues) | **exactly 1** winner per clue, always |
| best constant answer over 400 clues | 1.5 % |
| independent re-implementation vs the 508-char scorer, 41 347 (clue, move) pairs | **0 disagreements** |
| junk: `""`, `"0"`, `"x"`, `"1"*100`, `"0,0>0,0"`, `"9,9>9,9"`, `"999999,0>0,0"`, `"a,b>c,d"`, 1024 `0`s, unicode, 400 numbers | never raises, never returns non-0/1, **never scores 1** |
| worst score time (1024-char junk) | 0.040 ms (cap 50) |
| generate determinism (200 seeds) | identical |
| end-to-end on the real engine | pool loaded 1 accepted / 0 rejected; 261 clues in a 0.5 s round; default random strategy 0/261 |

### Anti-witness measurements (1000 shipped clues)
Legal `o` moves per clue: mean **8.86** (min 8, max 13); exactly one wins.
* know the movement law, guess uniformly: **11.5 %**
* best of 14 cheap non-rule heuristics: **17.1 %** ("land nearest an enemy")
  (first/last legal 9-11 %, longest 10.8 %, shortest 10.1 %, mover-touches-most-x 14.0 %,
  landing-touches-most-x 15.9 %, landing-farthest-from-x 1.6 %)
* plausible **wrong movement laws**, each solving its own version of the puzzle:
  rim doesn't count **14.2 %**, ignore blocks 6.4 %, 8-neighbourhood 4.4 %, count only
  enemies 3.8 % - all at or below the guessing baseline, and only 16-68 % of their answers
  are even legal, so a near-miss law gets a clean 0 rather than misleading partial credit.
* right law + wrong goal: "maximise own mobility" 9.2 %, "make the landing crowded" 14.8 %,
  "minimise own mobility" 16.2 %, "stalemate *both* sides" 52.2 % (the only near-synonym).

Winning mechanism mix (so no single visual pattern is the answer): enemy's step length
changes and its new landing squares are all blocked 53 %, the move plugs the exact square
the enemy would have leapt to 52 %, the enemy is stranded at step 0 by the mover leaving
11 % (they overlap when several enemies are mobile).

### Fairness floor - hypothesis-elimination surrogate (`hyp.py`)
A systematic centaur team is modelled as a fitter over **1944 hypotheses** = 216 movement
laws (4 choices of what counts x 3 neighbourhoods x rim counts or not x 3 move-direction
sets x exact/up-to-n/path-must-be-clear) x 9 goals. Feeding it demos:

| demos | consistent hypotheses | ... that also make the demo move the *unique* winner |
|---|---|---|
| 1 | 15-293 | 2-17 |
| 2 | 2-5 | 2-4 |
| 3 | **2** | **1-2** |

So **2-3 demos identify the rule** once the right hypothesis space is conceived - well
inside the "<= 6 demos" fairness floor. The difficulty is deliberately in *conceiving*
"distance = number of neighbours, and the goal is the enemy's stalemate", not in
confirming it. The only stubborn survivor is "minimise the enemy's mobility", which is a
synonym on these positions and answers identically - harmless.

### Witness leaks closed by the generator (verified by rejection filters)
1. exactly one winning move exists **anywhere on the board**, not just among legal moves;
2. >= 8 legal `o` moves, so "know the law and guess" pays ~11 %;
3. >= 1 enemy is mobile in the clue, so "the position is already won" is never true;
4. the winner is never the unique longest legal move, the unique move landing closest to
   an enemy, the only move landing beside an enemy, or the only move whose mover touches
   an enemy - the four heuristics that were worth 21-33 % before these filters.

### Arena (DESIGN_LOOP step 3) - players not run
No Agent/Task tool is available in this session, so per DESIGN_LOOP I stopped after step 3.
```
run          lab-orlan-1        (6 rounds, 0.5 s each, 5 s cooldown, 3 s final, pool = orlan only)
port         44499              training window open ~6 h from 2026-09-02 10:37Z
team orlana  $SCRATCH/lab-orlan-1/players/orlana
team orlanb  $SCRATCH/lab-orlan-1/players/orlanb
teardown     python sim/arena.py teardown --run lab-orlan-1 && python sim/arena.py report --run lab-orlan-1
```

---------------------------------------------------------------------------
## Iteration 1 RESULT (players run by the orchestrator) - both PARTIAL, neither cracked

| team | r1..r6 correct/answered | final | rule they believed |
|---|---|---|---|
| orlana | 4/168, 23/255, 36/267, 77/242, 63/214, 77/238 | 422/1304 = **32 %** | "an `o` hops along a line to the FIRST EMPTY cell, passing over anything" |
| orlanb | 1/201, 10/247, 11/246, 28/237, 45/207, 71/215 | 388/1357 = **29 %** | "put an `o` on any empty cell in its own row/column" |

Both spent all 6 demos, both shipped learned rankers (37 and 45 after-state features), and
**neither reached the step-length law**. orlana even tested "immobilise an `x`" as the goal
and rejected it - because they evaluated enemy mobility under the wrong movement law. The
goal was never reachable while the law was wrong, because the goal *reuses* the law.

### Root cause (measured after the fact)
**67.4 % of v1 winning moves land on the first empty cell along their ray.** Every winner
at distance 1 does so by definition, and distance 1 was 53 % of v1 winners. So the naive
"hop to the first empty cell" model was consistent with two thirds of every confirmed
answer and survived ~2,700 probes and 6 demos intact. My iteration-1 hypothesis-fitter had
the true law in its 216-law space and so never noticed that the *naive* law was almost as
good a fit as the true one.

---------------------------------------------------------------------------
## Iteration 2 - `challenges/lab/orlan.json` (v2; v1 preserved as `orlan.v1.json`)

### What changed (softened, per DESIGN_LOOP step 7)
1. **The naive law is now impossible.** Every winning move flies over **at least one empty
   square**: measured **0.0 %** of winners land on the first empty cell along their ray
   (v1: 67.4 %). Winner length is **2 (61 %) or 3 (39 %)**, never 1, so "it steps to a
   neighbour" is out as well. And **33.6 %** of winners also fly over an *occupied* square,
   which kills the next fallback, "the path must be clear".
2. **The rim clause is gone.** v1 counted off-board as an occupied neighbour; v2 counts
   only real pieces (`o`, `x`, `#`). The step length is now readable straight off the
   picture - count the pieces touching the mover - instead of needing a second insight.
3. The goal is unchanged: **after your move no `x` may have a legal move.** (The good part.)

Generation had to change to support this: the un-move now *pads the origin with blocks*
until its neighbour count is exactly the intended leap length, instead of waiting for a
random position to have one. A per-seed target length (2 or 3) and path mode (clear /
flies over a piece) keeps the demo set varied; a greedy augmentation step adds pieces so
that ~5 *other* legal moves also fly over empty ground, otherwise "the one that leaps over
a gap" would itself have been a free 37 % answer.

### Validation
`python tools/quickcheck.py challenges/lab/orlan.json -v` -> **OK, no warnings**
(`gen=11.2ms score=0.09ms solve=0.12ms`); `--seeds 200` -> OK (`gen=13.8ms`).
Over 3000 seeds: generate mean **4.2 ms**, p99 12.4 ms, max 38.5 ms (cap 100, warn at 50);
throughput on the live engine is therefore close to v1's (v1 delivered 261 clues per 0.5 s
round). Sizes: generate 7424, solve 883, **score 503 / 512**.

### Self-tests (fresh seeds, `$SCRATCH/game/adv2.py`, `xcheck2.py`, `shipheur2.py`, `hyp2.py`)
| test | v2 result |
|---|---|
| `solve` scores 1 on every seed | 1200/1200 |
| brute force *all* `a,b>d,e` over the whole board (400 clues) | **exactly 1** winner per clue |
| best constant answer (400 clues) | 2.25 % |
| independent re-implementation vs the 503-char scorer, 41 560 pairs | **0 disagreements** |
| junk (`""`, `"0"`, `"x"`, `"1"*100`, `"0,0>0,0"`, `"999999,0>0,0"`, 1024 zeros, unicode, 400 numbers) | never raises, never non-0/1, never scores 1 |
| worst score time | 0.033 ms |
| determinism (200 seeds) | identical |
| engine load | 1 accepted, 0 rejected |

### Anti-witness measurements (1000 shipped v2 clues)
Legal `o` moves: mean **9.18** (min 6), exactly one wins.
* **iteration-1 player model ("hop to first empty cell"): 0.0 %** (was the basis of their 30 %)
* know the law, guess uniformly: **11.1 %**
* best of 16 cheap non-rule heuristics: **21.7 %** ("pick at random among the moves that fly
  over empty ground" - the deliberate foothold, capped by the augmentation step)
  next best: landing-next-to-an-enemy 17.0 %, landing-nearest-an-enemy 15.5 %,
  landing-touches-most-x 15.3 %, mover-touches-most-x 14.8 %, longest 12.9 %,
  flies-over-a-piece 7.1 %, shortest 4.4 %
* winner mechanism mix: enemy's step changes and its new landings are blocked 51 %, the
  move plugs the square the enemy would have leapt to 41 %, enemy stranded at step 0 31 %
  (they overlap when more than one enemy is mobile).

### Fairness floor - hypothesis-elimination surrogate, now including the players' own laws
Space = 1784 hypotheses: 216 counting laws **plus the 7 naive laws iteration 1 actually
believed** (hop-to-first-empty, slide, any-cell-in-line, move-exactly-k for k=1..4), times
8 goals. Feeding demos:

| demos | consistent hypotheses | of which naive laws | survivors that also make the demo the *unique* winner |
|---|---|---|---|
| 1 | 4-46 | 1-6 | 2-19 |
| 2 | 2-46 | 0-6 | 2-13 |
| 3 | **2** | **0** | 1-2 |

Every naive law is dead by demo 3, and the space collapses to the true rule plus its
synonym "minimise the enemy's mobility" (which answers identically here). v1's equivalent
table never contained the naive laws at all - that blind spot is what iteration 1 exposed.

### Arena for iteration 2 (players to be run by the orchestrator)
```
run          lab-orlan-2   (6 rounds, 0.5 s each, 5 s cooldown, 3 s final, pool = orlan only)
port         47869         training window open ~6 h from 2026-09-02 11:30Z
team orlan2a $SCRATCH/lab-orlan-2/players/orlan2a
team orlan2b $SCRATCH/lab-orlan-2/players/orlan2b
teardown     python sim/arena.py teardown --run lab-orlan-2 && python sim/arena.py report --run lab-orlan-2
```
Expected: if the softening works, the naive line-hop model scores 0 in round 1 instead of
30 %, which should push the players off it within one round; a team that then fits
"distance = pieces touching the mover" should crack the class outright. A team that stops
at the movement law and guesses among legal moves lands at ~11 %, and one that also spots
"the answer always flies over a gap" lands at ~22 % - so the three outcomes are cleanly
separated in the final score.

---------------------------------------------------------------------------
## Iteration 2 RESULT - both PARTIAL again (23 %, 25 %), law still not found

| team | r1..r6 | final | law they believed |
|---|---|---|---|
| orlan2a | 1/89, 5/85, 12/91, 12/87, 3/84, 17/90 | 127/551 = 23 % | "exactly two NON-WALL steps; `#` is transparent and not counted; the rest of the way must be empty" |
| orlan2b | 0/0, 5/72, 10/85, 4/79, 9/92, 15/89 | 127/517 = 25 % | "the destination is the SECOND empty cell along the ray; occupied cells are transparent" |

v2 killed "first empty cell" but the winners then always leapt **2 or 3**, so both teams
just moved one rung down the ladder to the next proxy - and every one of their confirmed
answers fitted it. orlan2a: "all 60 known-correct answers fit that set". A law that is
never contradicted is never abandoned. Two further v2 mistakes, both measured afterwards:
padding the origin with blocks made "walls are transparent" look true, and generate() at
4.2 ms/clue meant only ~90 items per 0.5 s round, i.e. ~12 positives per round - too few
to fit any selection rule even if the law had been right.

---------------------------------------------------------------------------
## Iteration 3 - `challenges/lab/orlan.json` (v3; v1/v2 kept as `orlan.v1.json`, `orlan.v2.json`)

Rule unchanged (leap = number of adjacent pieces, rim not counted; goal = every `x`
immobile). Everything that changed is about **making the law discoverable**.

### The metric I was missing until now
For a candidate law L, the question is not "how often does L predict the winner" but
**"how often is the winning move even LEGAL under L"** - if that is 100 %, positives never
falsify L and the players never leave it. That is precisely what happened twice. Measured
over 1500 fresh v3 clues:

| candidate movement law | contains the winner | uniform hit rate |
|---|---|---|
| **TRUE: leap = #occupied orthogonal neighbours** | **100 %** | **16.4 %** |
| slide with a clear path | 57 % | 3.9 % |
| first empty cell (iteration-1 teams) | 48 % | 4.2 % |
| second empty cell (orlan2b) | 45 % | 6.0 % |
| k non-wall steps, walls transparent (orlan2a) | <= 41 % | <= 6.5 % |
| fixed distance k | <= 32 % | <= 5.1 % |
| leap = #occupied of all 8 neighbours | 31 % | 5.9 % |
| leap = #adjacent pieces, blocks NOT counted | 21 % | 4.4 % |
| leap = #adjacent enemies | 8 % | 2.4 % |
| leap = pieces in that line (LOA) | 36 % | 5.9 % |
| leap = #EMPTY orth neighbours | 19 % | 3.4 % |
| any empty cell in the row/column | 100 % | 4.0 % (26 moves - useless) |

Two things are now true that were false in v2: every proxy is **contradicted by 2-3
confirmed answers**, and the true law is the **highest-scoring law by 2.5x**, so the score
gradient points at the truth instead of away from it (in v2 orlan2a's proxy scored 17.8 %
while the true law would have scored ~11 %).

### The three changes
1. **Leap length now spans 1-4** (measured 32 / 32 / 25 / 11 %), instead of v1's 53 % at
   length 1 or v2's "always 2 or 3". The generator picks the length per seed and *pads the
   mover's origin with pieces until its neighbour count is exactly that length*, so
   positions with a 1-neighbour mover leaping 1 and a 4-neighbour mover leaping 4 both
   occur. No fixed-distance or k-th-empty proxy can survive two demos.
   The flight path is also varied per seed (all empty / all occupied), which kills
   "the path must be clear" and "walls are transparent" separately.
2. **Legal `o` moves reduced to 4-8** (mean 6.3), so knowing the law alone is worth ~16 %
   and the goal is a 1-in-6 choice rather than 1-in-9.
3. **generate() is 3x faster**: mean **1.4 ms**, p99 5.9 ms, max 8.6 ms over 3000 seeds
   (v2: 4.2 ms). Measured on the live engine with the default random strategy:
   **234 items per 0.5 s round**, up from 90 - about 38 positives per round for a player
   who has the law, which puts the selection rule in statistical reach.

Also worth stating plainly (orlan2b asked for it): the scorer has **always** been
property-based - it accepts ANY legal `o` move that leaves every `x` immobile and never
compares against a reference answer. The generator merely arranges for exactly one such
move to exist, which brute force over every 4-tuple confirms on every clue.

### Validation and self-tests (shipped v3)
`quickcheck -v` -> **OK, no warnings** (`gen=3.4ms score=0.10ms solve=0.07ms`);
`--seeds 200` -> OK (`gen=6.15ms`). Sizes: generate 6327, solve 883, **score 503 / 512**
(scorer source unchanged from v2 - the rule did not change).

| test | v3 result |
|---|---|
| `solve` scores 1 | 1200/1200 seeds |
| brute force every `a,b>d,e` on the board (400 clues) | **exactly 1** winner each |
| best constant answer | 1.50 % |
| most common winning move over 1200 clues | 1.2 % |
| scorer vs independent re-implementation | 33 148 pairs, **0 disagreements** |
| junk (21 strings incl. `""`, unicode, 1024 zeros, 400 numbers, negative indices) | no raise, no non-0/1, mean 0.004 ms |
| determinism | 300/300 identical |
| best of 20 cheap selection heuristics | 23.8 % ("longest legal move" = "mover with most neighbours") - and every one of them already needs the law, so none is a shortcut past it |
| hypothesis elimination (976 = 122 laws x 8 goals, incl. every law iterations 1-2 believed) | all non-counting laws dead by **demo 4**; space collapses to the truth + its synonym "minimise enemy mobility" |

### Expected outcome / how to read iteration 3
* stuck on a proxy law -> **~4-6 %** (v2 paid them 23-25 % for the same mistake)
* law found, goal not -> **~16 %**, or ~24 % if they also rank by "longest legal move"
* law + goal -> **100 %**

### Arena for iteration 3
```
run          lab-orlan-3   (6 rounds, 0.5 s each, 5 s cooldown, 3 s final, pool = orlan only)
port         39663         training window open ~6 h from 2026-09-02 12:12Z
team orlan3a $SCRATCH/lab-orlan-3/players/orlan3a
team orlan3b $SCRATCH/lab-orlan-3/players/orlan3b
teardown     python sim/arena.py teardown --run lab-orlan-3 && python sim/arena.py report --run lab-orlan-3
```
