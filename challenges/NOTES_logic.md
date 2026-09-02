# Brainstorm — logic, constraints & rule induction (logic-agent)

Format: NAME — clue → what scores 1 — why fun/tractable — how it is guessable.

1. carre — "12../.3.4/..." 4x4 with '.' blanks → any completion that is a Latin square and keeps the
   givens — tiny backtracking, instantly recognisable from one demo. EASY. **PICKED**
2. vex — same but 4x4 sudoku (rows/cols/2x2 boxes) — near-duplicate of carre, cut.
3. krom — 3-CNF "3,-7,1 -2,4,-9 ..." → a bit string of length max|var| satisfying every clause — CNF is
   the canonical logic object and signed comma-triples are a strong tell. EASY. **PICKED**
4. trico — "12 0-3 1-4 ..." (n then edges) → n digits from 0-2, no monochromatic edge. MEDIUM. **PICKED**
5. ikos — the SAME clue grammar → a space-separated permutation of 0..n-1 whose consecutive pairs are
   all edges (Hamiltonian path). Deliberate pairing with trico: same grammar, different object, so the
   team's real question becomes "what object?". MEDIUM. **PICKED**
6. zebu — Zebra-lite: constraints "A<B" (left of), "A|B" (adjacent), "C#3" (at position) over letters
   A-E → the arrangement satisfying all; '#' capped at 2 per clue so the ordering operators carry it.
   HARD. **PICKED**
7. wolf — "0110100110>0011011010 ..." (before>after) → the 8-bit Wolfram rule (MSB = neighbourhood 111,
   wrap-around) consistent with every pair — pure Zendo: observations in, hidden rule out. HARD. **PICKED**
8. polska/lukas — "3>47 7>..." (x>f(x)) → an RPN expression over x, digits and + - * reproducing every
   pair; scorer is a 255-char stack machine (built, validated, 0.36 ms solve). CUT LATE: optim-agent's
   TOPPLE already asks for a postfix expression, so the expensive discovery (the answer format) would
   be handed over for free; zebu went in instead. JSON is reproducible from this note's spec.
9. dama — "8 3:1 6:5" (n plus pinned rows) → n-queens completion as a digit permutation — fun, but n<=9
   for digit encoding and the scorer lands ~250 chars; cut as "yet another CSP" next to trico/ikos.
10. mccl — truth table "10010110" plus "k=3" → sum-of-products with <=k implicants ("01-" patterns) that
    matches the table. Needs the k bound to be interesting, and the scorer (parse terms + 8 assignments
    + count) would not fit 256 chars. CUT ON SCORER SIZE.
11. setcov — "k S1 S2 ..." bitmask subsets → <=k indices covering the universe — fits the cap, but it is
    the optimisation agent's territory. Cut.
12. sortnet — permutation clue → adjacent-swap positions that sort it — scorer is cheap but greedy solves
    it in one line, so there is no hypothesis to form after round 1. Cut.
13. lag — "find x with f(x) % m == r", f spelled out in the clue — collides with the numbers agent. Cut.
14. cell2 — infer a 2D life-like rule from before/after grids — grids agent's territory and the scorer
    (neighbour counts + birth/survive sets) blew the 256-char cap. CUT ON SCORER SIZE.

Difficulty spread of the 6 shipped: carre, krom (easy) / trico, ikos (medium) / zebu, wolf (hard).
