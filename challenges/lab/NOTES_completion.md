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
