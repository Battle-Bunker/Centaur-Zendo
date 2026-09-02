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
