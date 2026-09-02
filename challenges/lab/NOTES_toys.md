# Direction: toys and building things kids play with (toys-and-building agent)

The demo must be a little ASCII picture a kid recognises instantly; the clue is a few
characters and pins an arbitrary-but-natural **measurement** of that picture; the rule must
not be the toy's famous operation and must not have a name.

Two constraints I took from the earlier lab work and applied to every candidate:

* **NOTES_game.md conclusion.** A 0/1 channel only tests hypotheses the player already
  generates. The hidden quantity must therefore be *visible in the demo picture* and
  countable by eye — the clue shows the number, the demo shows the picture, and the only
  question is "what does this number count?". That is exactly the LegoZendo shape (3–4
  demos, cracked last of 32), and it is the shape I aimed at.
* **No character-frequency shortcut.** If the measurement equals "how many `X` are in the
  picture", an LLM finds it with zero insight about the toy. The measurement has to be
  *relational* (something about two pieces at once) or *positional*, never a glyph count.

## Brainstorm (14 candidates, each against the 12-year-old test)

Test 1 = "a kid names the object from one demo". Test 2 = "the pinned pattern has no name,
and is not the object's famous operation".

1. **Domino chain** `[3|5][5|2][2|2]`, count the joints where the pips match.
   T1 10/10. T2 **fail** — matching ends *is* the game. Also 1-D digit strings pull every
   hypothesis towards arithmetic (sums to 7, doubles), which is the RLVR-prior anti-pattern.
   *Reject.*

2. **Dominoes scattered on a table (2-D)**, count the pairs lying end-to-end with equal
   pips. T1 10/10, T2 marginal — it is the famous operation moved into a picture, and pips
   still invite "sum to seven". *Reject as primary, keep as a fallback softener.*

3. **Tetris well** with the heap drawn as letters `I O T S Z J L` in a `|....|` well.
   T1 10/10 — nothing is more instantly recognisable. T2 **fail**: the *measurement* list
   for a Tetris heap is folklore (holes, bumpiness, aggregate height, wells, line clears),
   so every "arbitrary" measurement I invented was either on that list or looked like it.
   The genre would be recognised and the measurement guessed from a public list. *Reject.*
   (Sub-variant "pieces touching a piece of the same shape" needs shape-normalisation in a
   512-char scorer, and same-letter pieces merge under any connected-component parse.)

4. **Jigsaw grid, count the pieces whose top edge is a tab.** T2 excellent — unnameable,
   and the famous operation (tabs fit blanks) becomes a *validity* constraint instead of the
   rule. But if up-tabs are drawn `n` and down-tabs `u`, the count is literally
   `picture.count("n")` — a fatal character-frequency leak. The positional fix (draw the
   bump inside the piece it intrudes into) survives, but the ASCII then reads as a table of
   arrows, so T1 drops to ~6/10. *Reject on T1 + leak risk; the best of the rejects.*

5. **Beads threaded on a string**, count the beads sitting between two beads of the same
   colour. T1 8/10, T2 good. *Reject as primary*: 1-D, and "count i with s[i-1]==s[i+1]" is
   an ordinary string statistic that an LLM enumerates early. Kept as the softener if the
   chosen class turns out too hard.

6. **Marble run**, count the ramps the marble touches. T2 **fail** — tracing the ball is the
   toy's famous operation and a stock puzzle genre. *Reject.*

7. **Wooden train track loop**, count the pieces whose peg end faces north. T2 good (kids
   know the peg/socket asymmetry intimately). T1 fails in ASCII: curves and a closed loop are
   expensive to draw and the famous fact (equal numbers of left and right curves) dominates
   any layout the scorer can check. *Reject.*

8. **Stacking cups / nesting dolls**, count the cups smaller than the one below. T2 fail —
   that is "sorted", a named property, and the state space is tiny. *Reject.*

9. **Jenga tower**, count the layers missing their middle block. T1 7/10 (a plan view reads
   as a table), T2 ok but thin. *Reject.*

10. **Lite-Brite / pegboard grid**, count pegs with two same-colour neighbours. T1 6/10 (a
    coloured grid is not a toy, it is a grid), and the LLM prior over grid statistics is
    enormous. *Reject.*

11. **Standing dominoes on a grid, count how many topple.** Simulation = famous operation.
    *Reject.*

12. **Wall of toy building blocks**, count the **joints that line up** between courses.
    T1 10/10, T2 good — but "aligned joints" is a mid-list hypothesis for any LLM shown a
    stack of rows, and the kid's version ("the cracks line up, you're not supposed to do
    that") is the same thought. Likely cracked in 1–2 demos. *Reject as the rule — adopted
    instead as the decoy the generator falsifies in every demo.*

13. **Wall of toy building blocks**, count the blocks that bridge exactly one crack below.
    T1 10/10, T2 good. Runner-up; slightly less visual than 14 and the count is large.

14. **Wall of toy building blocks, count the blocks that sit exactly on top of a block of
    the same size** ("a block resting on its twin") — **CHOSEN**.
    * T1 10/10: `[--][-][----][--]` stacked in courses is unmistakably a wall of blocks.
    * T2: nobody has a name for "a brick whose left *and* right edge line up with the brick
      underneath". It is not the famous fact about walls (that one is *stagger the joints*),
      it is a measurement of it. A kid spots it in seconds — "look, that one's sitting right
      on its twin" — and it is a conjunction of two alignments, so it sits below "the joints
      line up" in an LLM's candidate list without being exotic.
    * Not a character count: it is a relation between two courses.
    * Simplification-resistant: a player can only score by *producing* exactly N of them, so
      any rule that keeps paying is the rule (measured: the whole aligned-joint family caps
      at 18–23 %).

## Chosen: `virel` (neutral name, no pun, no abbreviation of the concept)

### Rule (private)

Clue `<digits>/<N>`: the digits (3–6 of them, each 2–6) are the brick widths of the
**bottom course**, left to right; W = their sum, 12..26; N ∈ 1..min(10, max(3, W//2−2)).

A solution is a wall, one line per course, **top course first**:

* every course is a gapless tiling of the same width W by bricks `[`+`-`*(w−2)+`]`, w ∈ 2..6
  (`[]`, `[-]`, `[--]`, `[---]`, `[----]`);
* at least **5** courses;
* the **last line** is exactly the clue's brick widths;
* exactly **N twin stacks**, where a twin stack is a brick whose span (left *and* right
  edge) equals the span of a brick in the course directly below, summed over all adjacent
  course pairs.

```
clue 4553/5                     the five twin stacks
[--][--][][-][--]               [  ][  ][][ ][  ]
[-][][--][-][-][]               [ ][][  ][ ][ ][]
[][-][-][-][--][]               [][ ][^][ ][  ][]
[---][-][][--][-]               [   ][v][][  ][ ]
[--][--][---][--]               [^^][  ][   ][  ]
[--][-][--][-][-]               [^^][ ][  ][ ][^]
[--][---][---][-]               [vv][   ][   ][v]     <- bottom = 4,5,5,3 = the clue
```

### Intended discovery path

1. Demo 1: the picture is a block wall; `4553` vs the last line is immediate (one demo).
   The format clauses — same width every course, bricks 2..6 wide, ≥5 courses, bottom
   course last — are all "what makes it a real wall", i.e. a kid reads them off one picture.
2. All remaining difficulty is *what N counts*. Round-1 skip-harvest gives clues only; the
   count cannot be inferred from clues (N is independent of the digits).
3. Rivals fall to the demos, because `solve()` rejects any wall in which a rival equals N:
   courses, junctions, total bricks, aligned joints, same-width-above pairs, near-twins,
   width-2 bricks. Every shipped wall also carries ≥2 *stray* aligned joints (aligned joints
   not belonging to a twin) and ≥2 near-twins (same width, different span), so "the joints
   line up" and "same size above" are visibly wrong rather than untested.
4. Probing is honest but slow: one shot per clue, so a player cannot binary-search N on a
   single picture; they must fix a hypothesis and let ~450 items/round grade it.

### Degenerate witnesses closed (measured; 300–400 fresh clues each)

| attack | scores |
|---|---|
| empty string / `"0"` / `"x"` / `"1"*100` / the clue itself | 0 % |
| one course (the clue row alone) | 0 % |
| the clue course repeated 2, 3, 4, 5, 6 or 9 times | 0 % (N ≤ 10 makes k·(H−1) unreachable) |
| honest **minimal** witness: 4 courses, N twins at the bottom junction | 0 % (≥5 courses) |
| a valid wall built to have **zero** twins | 0 % |
| a valid random wall, 6 courses, no twin control | **10.5 %** |
| a valid random wall, 9 courses, no twin control | **12.5 %** |
| rival family: build a wall with aligned-joint count N | 20.2 % |
| rival family: aligned-joint count 2N | 20.7 % |
| rival family: aligned-joint count 2N or 2N+1 (best rival found) | **22.7 %** |
| rival: bricks in the top course = N | 7.8 % |
| rival: total bricks = N / courses = N / same-width-above = N | 0.0 / 0.5 / 0.0 % |
| one fixed wall submitted for every clue | 0.2 % |
| the wall printed upside down | 0.2 % |

So: format-only ⇒ ~11 %, best wrong-but-workable law ⇒ ~23 %, the rule ⇒ 100 %. N regularly
exceeds the number of bricks in the bottom course, so the twins cannot all be parked at one
junction — the player has to control several junctions at once.

### Rival statistics on the shipped demos (600 demos)

How often each rival *equals* N in a demo (a player fitting hypotheses to demos):
twins 100 %; aligned joints 0 %; courses 0 %; junctions 0 %; total bricks 0 %;
same-width-above 0 %; near-twins 0 %; width-2 bricks 0 %; aligned//2 29 %;
3-row aligned columns 17 %; bricks in top course 16 %; distinct widths 14 %;
max bricks in a course 12 %; twins at the bottom junction 3 %.
The three survivors are the intended 2–3-demo work: each dies on the second or third demo,
and none of them is constructible to a score above 23 %.

### Validation

`python tools/quickcheck.py challenges/lab/virel.json --seeds 200` → `OK   virel
gen=0.06ms score=0.12ms solve=2.1ms`, no warnings. Sources: generate 290, solve 2794,
score **353**/512 chars. 1000 fresh clues: 0 solve failures, solve mean 0.32 ms / max 1.8 ms,
score 0.03 ms on real answers, 0.07 ms on junk, 0.15 ms on a 40×24 wall, solution ≤ 242
chars, 5–9 courses. Determinism checked on 50 seeds.

**Cross-check**: an independent, un-golfed re-implementation of the rule agreed with the
shipped 353-char scorer on **4200/4200** pairs (correct answers, 14 mutation families —
dropped/added/reversed courses, wrong bottom course, ragged course, width-7 brick,
whitespace noise, random garbage — and random valid walls).

### Arena (DESIGN_LOOP step 3) — players not run by me

Iteration 1 pool: `$SCRATCH/pool-virel-1/virel.json` (single-class pool).
Run/team directories are reported to the orchestrator; the two player agents are spawned by
the orchestrator with `sim/PLAYER_AGENT_BRIEF.md`, `{ROUNDS}`=6, `{COOLDOWN}`=5,
`{ROUND_SECONDS}`=0.5.

### What I will do with the result

* both cracked ⇒ harden by moving the count off the most-guessable rung: keep the wall, but
  count twins **only where the twin pair is not itself adjacent to another twin**, or pin
  the bottom course only by its *width* and add a second clause (top course must contain no
  brick of the clue's widest size). Also raise N's range to flatten the 11 % floor.
* neither cracked but partials near 20 % ⇒ they are on the aligned-joint rung; soften by
  making twins denser and rarer-in-rivals (bias N upward, force ≥1 twin in the bottom
  junction so the first demo shows the relation next to the clue row).
* one crack + one partial ⇒ on target, stop.
