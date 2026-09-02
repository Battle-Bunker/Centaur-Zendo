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
