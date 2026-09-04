# Brainstorm — sparse clue + forced completion (completion-agent)

Direction: clue is 2–6 chars; the clue itself fixes a **seed** (cells/pieces at positions the
512-char scorer can reconstruct from the clue alone), and the answer must be a *completion* of
that seed under an invented two-clause law (a local relation between neighbouring symbols + a
global count). No minimal witness may exist: the LegoZendo failure mode was "one 2x3N rectangle
answers every clue", so every candidate below is judged on **can a single clue-independent
template score 1?**

Nine candidates. `verify` = what the 512-char scorer must do.

1. **Degree labels ("each digit = its own neighbour count")** — grid of `.`/digits; every digit
   cell must have exactly *that many* orthogonal digit neighbours; the clue must appear as a
   horizontal run; global clause = total filled cells is a function of the clue digits.
   verify: neighbour count per cell + substring search + a sum. ~250 chars.
   Downside: the local law is a strong model prior ("label = degree" is guessed in one demo), and
   the labels are *determined* by the shape, so once guessed the puzzle collapses. Also the run
   makes many clues unsatisfiable (an interior `1` is impossible) so `generate` gets fiddly.
   REJECTED (too guessable), but it seeded #4.

2. **Anchored XOR sheet** — grid of `#`/`.`; every 2x2 window must contain an even number of `#`;
   row 0 is fixed to the clue's bits; global clause = exact `#` count.
   verify: 2x2 parity + count. ~200 chars. REJECTED: the law *is* rule-90/Sierpinski; a model
   recognises the picture, which violates "no named textbook object".

3. **Cycle-homomorphism grid (symmetric)** — the clue's k distinct letters define a cyclic order;
   orthogonally adjacent letters must be *cyclically consecutive*; global clause = every clue
   letter used equally.
   Nice property: the clue defines the **law**, not just a seed, so no clue-independent template
   exists. Downside: a two-letter checkerboard satisfies the local law, and the symmetric relation
   is the first hypothesis anyone tries → cracked from one demo. Kept as the *base* of #4.

4. **PICKED — chiral cycle law + staircase counts + seeded first line** (implemented as `OKRIN`)
   Clue = k distinct uppercase letters, k in 3..5 (3–5 chars). Cells are the clue's letters;
   every other character is inert filler. Three things must hold:
   (a) **seed**: line 1 begins with the clue (the fixed seed the scorer rebuilds from the clue);
   (b) **local, chiral**: for orthogonally adjacent letter cells, the right neighbour is the clue-
       cyclic *successor* and the cell below is the clue-cyclic *predecessor* (equivalently every
       component is `clue[(j-i) mod k]` for some offset — but only the local pairs are checked, so
       separate components may carry different offsets); no letter cell may be isolated;
   (c) **global count**: the t-th clue letter occurs exactly t+1 times (1,2,...,k; 6/10/15 cells).
   Why it fits the direction: the trivial witnesses die — the clue alone scores 0 (counts), a
   scatter of non-touching letters scores 0 (isolation), a checkerboard scores 0 (counts + seed),
   and no fixed picture works for two different clues (letters, k and the count profile all move).
   The chirality is the lateral catch: the natural hypothesis "neighbours are cyclically adjacent"
   is symmetric and scores 0 forever, so the player must notice direction.
   verify: dict of letter cells, four signed neighbour deltas, an isolation flag, k count checks.
   ~420 chars. Reference solve grows random shapes (multi-component, random offsets, random
   filler, decoy letters that are *not* in the clue) so demos never repeat a template.

5. **Brick completion (LegoZendo descendant)** — 2x3 letter blocks again, but the clue fixes the
   top-left block's letter and column offset and the answer must extend it. REJECTED: same object
   as an existing pool challenge; players who have seen LegoZendo transfer instantly.

6. **Seeded word-ladder column** — answer = a column of k-letter strings, each differing from the
   previous in exactly one position, starting from the clue, with a global "no letter used twice
   per column" clause. REJECTED: this is a Hamming/word-ladder prior, and it is a 1-D object —
   nothing to complete spatially.

7. **Ration tiles** — clue = k digits; answer = a strip of ASCII tiles where each tile's width is
   the digit and adjacent tiles must differ in height by exactly 1, plus total area fixed.
   verify: run-length parse + differences + sum. Fits, but the clue is *copied* into the answer as
   widths, so the answer is a rendering of the clue rather than a completion of it. REJECTED
   (fails "non-trivially dependent on the clue" in spirit: no search, just transcription).

8. **Anchored self-avoiding tour with turn law** — clue fixes the first two cells of a path drawn
   with `-|+`; the law is "no two consecutive turns in the same direction" + total length fixed.
   verify: path walk from the clue-derived start, turn-history check. ~450 chars but the walk
   parser (three glyphs, direction inference) blew the budget in a draft, and path-drawing is a
   maze prior (`warren` already covers it). REJECTED on cap + overlap.

9. **Balanced colouring with a forbidden pair table derived from the clue** — the clue's characters
   list the *forbidden* adjacent pairs and the answer is any grid avoiding them with fixed colour
   counts. REJECTED: "avoid these pairs" is legible from the clue almost immediately (the clue
   reads as a table), so there is no rule to infer — the clue leaks the law instead of seeding it.

## Adversarial witnesses that #4 must reject (self-test list)
* `clue` itself, `clue` on one line with padding — counts wrong.
* seed line + the remaining letters scattered with no contacts — isolation clause.
* seed line + a full rectangle of shifted rows — counts wrong.
* the correct shape with the vertical relation flipped (successor downwards) — chirality.
* the correct shape rotated/mirrored, or with the seed not at line 1 col 0 — seed clause.
* the correct shape with one extra copy of the last letter — counts.
* a valid answer for a *different* clue — letters not in the clue become filler ⇒ counts wrong.

## Implementation: OKRIN (v1)
`challenges/lab/OKRIN.json` — validated: `python tools/quickcheck.py challenges/lab/OKRIN.json --seeds 200`
⇒ `OK  gen=0.04ms score=0.1ms solve=6.34ms`, no warnings. score source 466/512 chars.

Adversarial self-test (60 random clues × 12 attack families, scratchpad harness): every family scores 0 —
empty, clue alone, clue padded, `"1"*1000`, 1000 random letters, seed row + isolated scatter, counts taken in
clue order, the down=successor stripe grid, the shift rectangle, another clue's valid answer, an answer
indented by one column, an answer pushed down one line. Single-cell mutations of a valid answer survive
<35% of the time. Worst scorer time on adversarial input 0.04 ms.
The only inputs that score 1 under a *wrong* hypothesis are clues whose letters are already in alphabetical
order (≈5% of instances), where clue-order and alphabet-order counts coincide — kept deliberately as a
partial-credit gradient.

### Fairness/ceiling probe (`sim/results/lab-OKRIN-selftest`, 3 scripted teams, 1 round each)
| scripted team | hypothesis | presented | correct | hit | ms/answer |
|---|---|---|---|---|---|
| full | complete rule | 270 | 270 | **100.0%** | 0.85 |
| nearmiss | counts keyed to clue order, everything else right | 406 | 24 | 5.9% | 0.35 |
| symmetric | down = successor (chirality dropped), everything else right | 74 | 0 | 0.0% | 8.0 |
So a team that has the rule can answer at full round speed (ceiling 100%), a team that misses only the
alphabet-order clause sees a small non-zero signal, and a team that misses the chirality sees nothing.

### Arena handoff (iteration 1) — set up here, players run by the coordinator
No Agent/Task tool is available in this session (only `mcp__Claude_Code_Remote__create_session`, which puts a
sibling in a *different container* with no route to the arena's localhost port and with the repo visible —
unusable for a confidential player run), so per DESIGN_LOOP step 4 the loop stops after step 3.
The arena is already set up and live:
* run `lab-OKRIN-1`, pool = OKRIN only (server log: "1 accepted: OKRIN"), phase `training`
* 6 rounds × 0.5 s, cooldown 5 s, 1 demo/window, 3 s final; training window open ~6 h from 10:40 UTC,
  final window +1 h
* team dirs (give each agent `sim/PLAYER_AGENT_BRIEF.md` with `{TEAM_DIR}` = its dir, `{ROUNDS}`=6,
  `{COOLDOWN}`=5, `{ROUND_SECONDS}`=0.5, and nothing else):
  `…/scratchpad/lab-OKRIN-1/players/OKRINa` and `…/scratchpad/lab-OKRIN-1/players/OKRINb`
* afterwards: `python sim/arena.py teardown --run lab-OKRIN-1 && python sim/arena.py report --run lab-OKRIN-1`

### Hardening levers held in reserve for iteration 2 (if both players crack it)
1. Rotate the count profile by a clue-derived offset (e.g. start the counts at 2 + (ord(clue[0])%k)) so the
   alphabet-rank aha is not the last step.
2. Make the vertical relation +2 rather than −1 for odd k (kills "down is just the inverse of right").
3. Move the seed off line 1: require the clue to appear as a *vertical* run in column 1, so the demo no
   longer displays the clue as a readable word.
4. Soften instead (if neither cracks it): drop the isolation clause, or make `solve` emit one component only.

## Iteration 1 — RESULTS (`sim/results/lab-OKRIN-1`, 2 Opus centaur players)
6 training rounds × 0.5 s, 5 s cooldown, 1 demo/window, 3 s final; pool = OKRIN alone (so both players
could spend all six demos on this one class — a harder test than a 32-class pool).

| team | r1 | r2 | r3 | r4 | r5 | r6 | final | outcome |
|---|---|---|---|---|---|---|---|---|
| OKRINa | 0/610 | 0/457 | 10/597 | 447/449 | 444/445 | 444/449 | **2685/2685 = 100%** | **cracked**, round 4, 3 demos |
| OKRINb | 0/0 | 0/462 | 0/474 | 0/454 | 0/442 | 149/379 | **2767/3804 = 73%** | **partial** |

**What OKRINa believed** (from its `strategy.py` docstring): exactly the intended rule — right neighbour =
successor, below = predecessor, "the clue letter of alphabetical rank k (1-based) occurs exactly k+1 times",
no isolated letter — plus two extra beliefs that cost it nothing: "the clue appears as a contiguous
horizontal run" (implied by the seed clause) and "no fully enclosed blank cell" (superstition; the scorer
never checks it). It shipped one precomputed grid template per rank-permutation. It reported the seed clause
as the last one isolated, only in rounds 5–6 from residual near-misses: *"invisible until you're already
at 99%."*

**What OKRINb believed**: the alphabetical-rank counts and the Toeplitz law `g[r][c] = clue[(c-r) % n]` —
i.e. both halves of the local law — but never the seed clause as a rule. Instead it learned, from 226
labelled round-6 answers, a GOOD/BAD lookup table of *which grid width mod n is accepted* per
rank-permutation (that width is exactly what decides whether row 0 starts at `clue[0]`). Final accuracy
tracked table coverage: n=3 100%, n=4 79%, n=5 53%. It also flagged the decoy non-clue capitals in demos as
a suspected bug — they are intended noise (lever 4), they did prevent a template leak, and they cost it
analysis time; worth an organiser FAQ line rather than a change.

**Design property to preserve (OKRINb's stated failure mode).** Three stacked clauses that each score 0
alone means there is *no partial-progress signal* until everything is right at once: OKRINb had the count
clause exactly right in round 5 and still scored 0/442. That is precisely what makes the class hard, and it
is why the ~5% alphabetical-clue coincidence (the only built-in gradient) matters — keep both.

**Decision: no iteration 2, rule frozen.** `generate`/`solve`/`score` are byte-identical to the version the
players faced (sha1 prefixes 1f36467340a7 / 44e54286b54f / f4d1a0b7044a); only the private `description`
gained the measured iteration-1 record. Re-validated after the edit:
`quickcheck --seeds 200` ⇒ `OK gen=0.04ms score=0.07ms solve=6.45ms`.
The reserve hardening levers above were deliberately NOT applied: one player cracking cleanly and one
stalling at 73% is the target band, and every lever would move an untested rule.

**Final classification: ON TARGET.** Evidence: cracked/partial split across two equally-briefed Opus
players; 3 demos and 4 rounds to crack (LegoZendo, the "hard" benchmark, took 3–4 demos in a 32-class pool
— OKRIN matched that while being the *only* class competing for demos); the ceiling is reachable at full
round speed (OKRINa answered 449 items in 0.5 s at 100%); and the two independent clauses each produced a
distinct, diagnosable failure mode rather than an opaque zero.

---

## Iteration 2 — RE-SKIN to a friendship bracelet (2026-09-04, refiner)

**Why.** Iteration 1 was *on target for AI players* (mean final rate 84 % over 2 finals: one crack in
round 4, one partial at 73 %) but the 12-year-old judge scored the class **1.8/5**: an abstract letter
grid with decoy letters, three stacked clauses, alphabetical-rank counts, and a shape that has a name
("Toeplitz diagonal grid"). Judge's advice: *"Recast the abstract letter-grid as a concrete kid object
(a friendship bracelet or knitting pattern, a marching-band formation, a seating chart) and give a kid
a foothold clause before the alphabetical-rank twist."*

This iteration is a **re-skin, not a re-balance**: every load-bearing mechanic that produced the
crack/partial split is kept structurally identical, and only the skin and the sorting key move.

### What did NOT change (the balance-carrying mechanics)
* **Seed clause** — the answer must *complete* a start the scorer rebuilds from the clue alone
  (row 0 begins with the clue). This was the clause both players found last ("invisible until you're
  already at 99 %") and the one OKRINb never found at all; it is why no clue-independent witness exists.
* **Local chiral neighbour law** — right = next colour, below = previous colour, no lonely bead, only
  touching pairs checked (so a second strand may carry its own offset).
* **Per-symbol count profile keyed to a *second* ordering of the same symbols** — still 2..k+1, still a
  permutation the clue does not display, so a demo's grid only transfers to clues with the same rank
  permutation (1/k!). Base 2 kept (base 1 makes ~19 % of profiles unweavable).
* Totals 9/14/20, k ∈ {3,4,4,5,5}, clue 3–5 chars, deterministic `random.Random(clue)` cosmetics.
* The three clauses still each score 0 alone — no partial-progress signal until all three are right,
  which is the property OKRINb's 0/442 in round 5 identified as the source of the difficulty.

### What changed
| | v1 (letters) | v2 (bracelet) |
|---|---|---|
| symbols | any 3–5 distinct capitals A–Z | the six **bead colours** `R O Y G B P` (red orange yellow green blue purple) |
| clue | random capitals, e.g. `BPAQE` | the **bracelet's colour order**, e.g. `BRYP` |
| count key | **alphabetical** rank | **rainbow** rank (`ROYGBP`) |
| decoy symbols | 55 % of demos sprinkled non-clue capitals | **dropped** (they read as clutter/bug; OKRINb filed them as a suspected bug) |
| `solve()` shape | components scattered over a large sheet, bead density ≈ 0.38 | one tight bracelet — dents filled first, growth hugs the top-left; density ≈ 0.64 (measured over 300 clues) |
| filler | `._-~:*` | thread-ish `. - _ ~` only |
| picture size | up to ~11 rows of sparse letters | 2–6 short rows |

Nothing else in `score` moved: the source is v1's with `sorted(c)` → `sorted(c,key=W.index)` and the
palette string added (**489 chars**, cap 512).

### Why the count clause was re-keyed rather than removed
The judge suggested replacing the rank counts with "a count a kid would naturally propose (e.g. the
number of beads of the clue's first colour)". Tried on paper and rejected: any count profile that
depends only on *k* makes one demo a **complete template for every clue of that k** (relabel the bead
classes), so a single round-1 demo would hand a player ~40 % of the final without any insight. The
count must stay keyed to a permutation the clue does not show. **Rainbow rank is that same measurement
in kid language** — "sort the colours like a rainbow" is a sentence a 12-year-old says unprompted,
where "alphabetical rank among the clue's letters" is not.

Bonus (measured over all 1200 possible clues, weighted by `generate`):
| ordering a player might try | agrees with rainbow rank on |
|---|---|
| clue order (the first hypothesis) | 5.3 % of clues — the deliberate partial-credit gradient, unchanged from v1 |
| **alphabetical (the LLM's default key)** | **0.00 % — never** |
| reverse alphabetical | 7.7 % |
| rainbow reversed | 0.00 % |
The palette's letters `B G O P R Y` have rainbow ranks `4 3 1 5 0 2`, whose longest increasing run is 2,
so no clue of three or more colours can ever agree with alphabetical order. The model's habitual key is
a wall; the kid's key is the door. That is the centaur asymmetry this class is now built around, and it
offsets the softening from dropping the decoys and shrinking the pictures.

### The three demos a player would see (real `solve()` output)
```
clue GRYPO          clue BRYP        clue RPY
GRYPOG              BRYPB            RPY
OGRYPOG             PBRYP            YRP
P~G~~P              YPB.             PY
YP~~~~~             ..P.             .P.
~YP~
```

### 12-year-old test, applied explicitly (first demo, clue `BRYP`)
*What a kid sees:* a little bracelet of coloured beads on a thread — blue, red, yellow, purple across
the top, the same four colours stepping **down and to the right** in diagonal stripes, and a ragged
bottom edge where the weaving stops.
*What a kid can say out loud from that one picture, in order (the foothold ladder the judge asked for):*
1. "The top row is exactly the pattern you were given." ← **foothold, clause 1, free from one demo**
2. "The stripes run diagonally, like a real friendship bracelet." ← clause 2, half of it
3. "Going right it's the next colour in the list; going down it's the one before." ← clause 2, the chiral half
4. "There are more purple beads than red ones — count them: 2, 3, 4, 5." ← clause 3, the *observation*
5. "Sort the colours like a rainbow and the counts go in order!" ← clause 3, the **twist**, and the one
   step an LLM's priors point away from.
No step needs a word a 12-year-old does not have; no maths beyond counting to five and "next/previous".

### Witness table (60 random clues each; v1 run through the same harness for comparison)
| witness family | v1 | v2 |
|---|---|---|
| reference `solve()` output (must be 1) | 60/60 | 60/60 |
| empty string | 0/60 | 0/60 |
| clue alone / clue + thread padding | 0/60 | 0/60 |
| `"1"*400`, 400 random bead letters | 0/60 | 0/60 |
| clue row + lonely beads scattered (isolation) | 0/60 | 0/60 |
| solid k×k stripe rectangle (equal counts) | 0/60 | 0/60 |
| stripes flipped (below = next colour) | 0/60 | 0/60 |
| full flipped stripe sheet | 0/60 | 0/60 |
| right shape, counts in **clue order** | 4/60 | 6/60 *(the intended ~5 % gradient)* |
| right shape, counts in **alphabetical order** | 60/60 *(= v1's rule)* | **0/60** |
| right shape, counts in reverse-alphabetical order | 0/60 | 2/60 |
| right shape, rainbow counts but stripes flipped | 0/60 | 0/60 |
| another clue's bracelet, verbatim | 0/60 | 0/60 |
| template transfer from another clue, same k | 1/60 | 2/60 |
| transfer from a clue with the **same rank permutation** | 28/34 | 30/30 *(by design; 1/k! of clue pairs)* |
| bracelet indented one column / pushed down a row | 0/60 | 0/60 |
| bracelet mirrored left-right / flipped top-to-bottom | 0/60 | 0/60 |
| one extra pair of beads appended | 0/60 | 0/60 |
| single-character mutation of a valid bracelet | 612/1091 (56 %) | **268/1096 (24 %)** |
Reading of the two rows that moved on purpose: alphabetical counts went from *being the rule* to being
impossible, and single-character noise now survives less than half as often (v1's inert decoy letters
made many mutations harmless). The same-rank-permutation transfer is the one intended leak: with 6
demos a player who never finds the rule can cover ≤ 6 of the 150 (k, permutation) pairs, ≈ 4 % of the
weighted clue space — the price of dropping the decoys, and small enough to pay for a legible picture.

### Validation
`python tools/quickcheck.py challenges/lab/OKRIN.json --seeds 200` ⇒
`OK  OKRIN  gen=0.04 ms  score=0.07 ms  solve=243 ms` (caps 100 ms / 50 ms / 2000 ms), no warnings.
`score` 489/512 chars, `solve` 4146/5000, `generate` 124/50000. 400/400 seeds: `solve()` non-empty and
scores 1; worst single solve 340 ms, mean 12.5 ms; scoring junk 0.001 ms/call.
v1 preserved verbatim at `challenges/lab/OKRIN.v1.json` (copy of the live `challenges/OKRIN.json`).

### Predictions
* **Kid score: 4/5** (from 1.8/5; range 3.5–4.5). Gains: a nameable everyday object, colours instead of
  arbitrary letters, a clue that *means* something ("the bracelet's colour order"), a picture that fits in
  four short lines, no decoys, and a foothold clause readable from one demo. Residual risks a judge may
  still charge: it is a letter grid *of colour initials*, not a drawn bracelet; the ragged bottom edge
  (forced by the unequal counts) makes the band look unfinished; and three stacked clauses are still
  three clauses.
* **AI balance: expect the class to stay in band (predicted mean final ≈ 60–85 %, one crack + one partial).**
  Softer than v1: cleaner, smaller demos and no decoys make the seed row and the stripe law more visible.
  Harder than v1: the count key is no longer the model's default sort, and a wrong-but-close alphabetical
  hypothesis now returns *exactly zero* instead of confirming. Net: unchanged to slightly harder on the
  count clause, slightly easier on the shape clause.
* If the next run comes back **too easy**, the reserve levers are unchanged from iteration 1 (rotate the
  count base by a clue-derived offset; make the vertical step +2 for odd k; move the seed to a vertical
  run in column 1) plus one new one: draw from **eight** bead colours (adding `W` white and `K` black,
  which have no rainbow position and would have to be pinned by experiment).

**Status: written and validated, arena NOT opened** (the orchestrator opens it). No commit, no push.
