# Brainstorm — invented "physics" on ASCII pictures (physics-agent)

Direction: rules that *feel* like a physical world but are made up. The clue is a scene
fragment plus a parameter; the answer must **construct/complete a scene** that obeys the
invented physics. The insight is worldly ("what does *support* mean here?"), not
mathematical. `verify` = what the 512-char scorer must do.

1. **murn — settling under a two-shoulder gravity (PICKED).**
   Clue `FOOTPRINT|n`, e.g. `#.oo#.#|9`. Answer: an ASCII picture (rows newline-joined,
   `#` stone, `o` wood, `.` air) whose **bottom row is exactly the footprint**, all rows
   the same width, containing **exactly n `#` in total**. Invented gravity: a cell that is
   not on the ground is held only by what is *directly under its three-cell shadow* —
   **stone needs exactly two of {SW,S,SE} occupied, wood needs exactly one**. Zero or three
   supports = nothing may stand there (three is "over-braced", the counter-prior bit: solid
   pyramids are illegal, structures must be lacy).
   verify: split rows, bottom == footprint, all widths equal, alphabet ⊆ `#o.`, for every
   non-air cell above the bottom count non-air cells among the three below and compare to
   2/1, and total `#` == n. ~450 chars. Non-degenerate: the footprint alone always has
   fewer than n `#` (generator guarantees ≥3 stones must be added), a solid block breaks
   the "exactly" clause, and the empty answer fails the bottom-row test.
2. **water poured at a marked column, exactly k cells wet.** Clue = terrain + pour column
   + k; answer = the wet cells. Rejected: any *sane* flow rule is textbook "trapping rain
   water" (instantly recognised), and any insane one is arbitrary rather than worldly.
3. **shadows at 45°.** Unmarked light source; clue = the shadow stripe cast on the floor;
   answer = blocks whose shadows match. verify is cheap (`c + height`), but the trivial
   witness — one block one row above the floor per shadow cell — is exactly the answer, and
   closing it needs a second stability clause, i.e. idea 1 with extra machinery. Kept as a
   hardening option for murn (add "the picture must also cast shadow S").
4. **balance beam with invented letter weights.** Clue = fulcrum + total torque; answer =
   letters on a beam. Rejected: any non-obvious weight table (strokes, holes, ink) is a
   26-entry lookup that cannot be inferred from ≤6 demos; alphabet-position weights are the
   mathematical version we were told to avoid.
5. **crush / load capacity.** Every block carries at most 2 blocks above it. Rejected:
   verification needs load propagation (a small flow problem), no chance in 512 chars.
6. **buoyancy** — `o` floats on the `~` line, `#` sinks. Rejected: the rule is exactly the
   real-world prior, so it is read off the first demo.
7. **angle of repose** (no column more than 1 taller than its neighbour). Rejected: the
   answer collapses to a list of heights — a numeric rule, not a picture, and near-trivial.
8. **domino chain reaction.** 1-D, reduces to arithmetic on gaps. Rejected.
9. **magnet polarity lattice.** Reduces to a 2-colouring/parity puzzle — a maths insight
   wearing a physics hat. Rejected.
10. **erosion pre-image** (clue = shape after k rounds of erosion, answer = before).
    Rejected: it is `erewhon` (Life predecessor) with different neighbourhood rules.
11. **wind-blown drift** — support only from S/SW ("everything leans east"). A one-clause
    variant of 1; kept in reserve as an alternative flavour if 1 turns out too easy.
12. **rope mobile / hanging tension.** Nested brackets, i.e. a balanced-tree exercise.
    Rejected as textbook.

## Why 1 wins
It is a *world* with two materials and one weird law; the clue is ~20 characters; the
answer must be built, not copied; the natural human prior (solid pyramid, "resting on the
block below", "at least one support") is wrong in an interesting way; the scorer is a pure
verifier that fits the cap; and there are three independent things to discover (the output
format + bottom-row anchoring, the two support laws, and what `n` counts).

---

## murn v1 — implementation, validation and self-test (iteration 1)

`challenges/lab/murn.json`. `python tools/quickcheck.py challenges/lab/murn.json --seeds 200`
→ `OK murn  gen=0.16ms score=0.08ms solve=0.26ms`, **no warnings**. Sizes: score 477/512,
solve 2127/5000, generate 988/50000; clue ≤ 19 chars; answers 2–11 rows.

Generator guarantees, measured over 2000 clues: every clue needs **≥3 stones added above the
ground** (distribution of "stones to add": 3–24, median 6), and **65% of clues cannot be
finished with a single extra row** — wood scaffolding must be built to lift the quota into
reach. `n ≤ 30`, footprint 9–16 wide.

Adversarial self-test (400 clues, `$SCRATCH/murn/adv.py`) — hypotheses a player might hold,
and how often each scores 1:

| answer built from                                             | scores 1 |
|---------------------------------------------------------------|---------|
| "at least 2 under a stone, at least 1 under wood", greedy fill | 1.8 %   |
| "rests on the cell directly below"                             | 4.8 %   |
| solid pyramid on the footprint                                 | 0 %     |
| right rule, count off by one                                   | 0 %     |
| a correct answer printed upside down                           | 0 %     |
| footprint + one row of stones wherever legal (count ignored)   | 11.5 %  |
| wood-only tower                                                | 0 %     |
| a correct answer with every `o` turned into `#`                | 0.5 %   |
| a correct answer with every `#` turned into `o`                | 0 %     |
| footprint alone / empty / the clue itself / junk / 1024-char junk | 0 %  |
| the footprint repeated k times (k ≤ 8)                         | 0.4 %   |

The only non-trivial partial witness (11.5 %) already requires the support law; it fails on
the quota, which is the second clause. Junk and oversized inputs: worst single `score` call
0.08 ms.

Cosmetic tolerance (all 200/200 accepted): trailing/leading blank lines, CRLF, spaces used
as air, ragged right edges (rows are right-padded with air before checking).

A player who has the rule right but writes the simplest possible solver (walk up, lay stones
on every exactly-2 position until the quota is met, scatter wood on every exactly-1 position)
scores **100.0 %** over 3000 clues in ~0.15 ms per answer — so the class is all-or-nothing
once cracked, which makes cracked/failed easy to read off the final.

**What demos alone can prove.** Demos are positive examples only, so within the natural
hypothesis family "glyph g may stand where the number of occupied cells below is in S_g",
positive examples can only ever establish that 2 ∈ S_# and 1 ∈ S_o. `{2}` vs `{2,3}` vs
`{1,2,3}` are indistinguishable from any number of demos: the "exactly" clause can only be
found by *probing* (build an over-braced cell, see it score 0). That is the intended
insight — cheap to test (≈450 graded probes per round) but it has to be thought of, and the
first three natural priors ("sits on the block below", "at least one support", "at least two
supports") all produce over-braced cells and score ~0–5 %.

**Hardening dials held in reserve** (if players crack it in ≤2 demos): make `n` count only
the stones *above* the ground; require the picture to have exactly one topmost cell; add a
third material with a 3-support law; or (idea 3) also require the scene to cast a given
45° shadow. **Softening dial** (if nobody gets traction): put the number of rows in the clue,
or widen the footprint's stone quota so a single extra row always suffices.

## Iteration-1 arena status

Arena `lab-murn-1` is set up and the server is **running** (see the report). The Agent tool
for spawning player agents is not available in this designer session, so per the
`sim/DESIGN_LOOP.md` fallback the loop stops after step 3; the filled-in briefs for both
teams are in `sim/results/lab-murn-1/BRIEF_murna.md` and `BRIEF_murnb.md`.
An end-to-end smoke run (separate throwaway arena, torn down; logs in
`sim/results/lab-murn-smoke/`) confirmed a 0.5 s round presents **445 murn challenges**, the
default random strategy scores **0/445**, and `player.py demo murn` returns a scoring example.

---

## Iteration 1 result and the v2 hardening

Both players cracked v1, but late: murnb in round 5 (4 demos), murna in round 6 (6 demos);
finals 3416/3416 and 2669/2669. Neither found a degenerate witness — both needed the real
rule, which is the important part. Both converged on the *same abstraction*: **count the
occupied cells in the 3-cell window below, untyped**, plus "total `#` == n". murnb's notes
record the exploit that made the quota free: *"an adjacent pair of filled cells is
self-sustaining (2 `#` per level forever), so an unlimited number of `#` can always be
stacked"* — so the second clause cost them nothing once the first was found.

**v2 = one notch, two coupled changes** (v1 kept as `murn.v1.json`):

1. **The support law becomes material-typed** — *nothing may rest directly on its own kind*
   (staggered joints, masonry running bond). A stone still needs exactly two of the three
   cells below occupied and wood exactly one, but a stone may not sit directly on a stone,
   nor wood directly on wood. This is the change aimed at both winning methods: murna's
   constraint propagation ran over **occupancy** windows (8 contexts x 2 glyphs = 16
   classes); legality now depends on *which material* is directly underneath (27 contexts
   x 2 glyphs = 54 classes), so their labelled data does not merely become sparse, their
   abstraction becomes *contradictory* — the same occupancy context is legal or illegal
   depending on a variable they were not modelling. murnb's factorial over five placement
   policies is defeated the same way: every policy in that family is now wrong. It also
   kills the self-sustaining `##` column outright (a stone may no longer stand on a stone),
   so quotas must be built by bridging gaps and the pictures visibly zig-zag.
2. **`n` counts only the stones ABOVE the ground row.** Cheap, but it costs a demo/probe
   cycle: the natural "total stones" reading (which murna took until demo 4 to settle) now
   fails, and it keeps the ground-row-alone witness closed for free.

Rejected hardening dials, with reasons:
* *third material with its own support count* (coordinator's suggestion B): it multiplies
  the context table by less than the material-typed windows do (24 classes vs 54) **and it
  adds slack** — 3-support positions become usable, which makes construction easier and
  removes the "over-braced is illegal" counter-prior for one glyph. Strictly worse.
* *exactly one topmost cell* (coordinator's suggestion A, strict reading "nothing directly
  above"): provably unsatisfiable. If every occupied cell except one must have an occupied
  cell directly above it, each non-empty column's occupied cells run contiguously to the top
  of that column and each non-empty column therefore contributes exactly one topmost cell —
  so "exactly one" forces exactly one non-empty column, contradicting a ground row with
  occupied cells in several columns.
* *exactly one summit* (the 3-cells-above reading): satisfiable, but it couples every row to
  every other (each row must cover the row below and the whole picture must narrow to one
  cell), which turns the post-insight task into backtracking search. The final is 3 s for
  ~2700 items, so a cracked player must answer in ~1 ms; this would make "cracked" score
  badly and would move the difficulty from insight to search, against the loop's rule.

### v2 validation and self-test
`quickcheck --seeds 200` → `OK murn gen=0.22ms score=0.08ms solve=2.15ms`, no warnings.
Score 465/512 chars. Over 5000 seeds: no solve failures, no generator fallbacks, clue ≤ 19
chars, worst solve 11.8 ms, answers ≤ 12 rows. Quotas now 3–25 stones above the ground
(median ~7).

Hypothesis hit rates over 1500 clues (`$SCRATCH/murn2/adv2.py`):

| what the player believes | scores 1 |
|---|---|
| the exact v2 law, one-pass greedy — **fairness floor** | **100.00 %** |
| v1's winning solver verbatim | 0.13 % |
| v1 law + v2 quota (only the quota change found) | 2.00 % |
| v2 law + v1 quota (only the support change found) | 1.60 % |
| staggering found, but "at least two / at least one" | 19.67 % |
| "no stone on stone" only (wood unrestricted) | 17.40 % |
| "no wood on wood" only (stone unrestricted) | 5.73 % |
| "it rests on the cell directly below" | 0.07 % |
| ground row alone / solid pyramid / wood-only tower / recolourings / upside down / off-by-one / ground row repeated / empty / clue / 1024-char junk | 0.00 % |

The 17–20 % band is deliberate: it gives a player who has most of the law a visible gradient
to climb, while nothing short of the exact law gets near 90 %. Cosmetic tolerance unchanged
(trailing/leading blank lines, CRLF, spaces as air, trailing spaces, ragged right edges: all
300/300). Worst single `score` call on junk: 0.071 ms.

Arena `lab-murn-2` is set up and running; see `sim/results/lab-murn-2/HANDOFF.md`.
