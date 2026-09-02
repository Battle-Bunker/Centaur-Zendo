# Brainstorm — optimisation, search, games & encodings (optim-agent)

Design rule for this whole batch: the clue carries a **threshold or target**, so `score`
is a cheap *check* (sum it, walk it, xor it) and never an optimiser. Verify-easy / find-hard.

## 12 ideas (name — clue → what scores 1 — why fun — how guessable)

1. **TARE** — `"17 4 23 9 12 5 8|41"` → solution is a 0/1 **bitmask** over the numbers whose
   selected sum equals the target. Fun: classic subset-sum, tiny (n≤9 ⇒ 512 masks). Guessable:
   one demo shows a mask the same length as the number list; feedback confirms "sum == RHS".
2. **BASILISK** — `"1f4:16>7"` → the same value written in base 7, no leading zeros. Fun: pure
   encoding warm-up. Guessable: the clue almost reads itself; one demo nails it. (BAS-ilisk = base.)
3. **HANSOM** — `"3,1 0,4 5,5 2,2 6,0|28"` → a permutation of the point indices whose **closed
   taxicab tour** is ≤ the bound. Fun: real TSP, but only 5–7 points so brute force is 1 ms.
   Guessable: demo shows a permutation; gradient = bound has slack on some seeds (greedy passes),
   is tight on others (need optimal). Hansom = a *cab* ⇒ taxicab metric.
4. **MARIENBAD** — `"5 7 9 3"` (heaps, xor≠0) → the **position after one legal move** that is a
   Nim P-position (xor 0). Fun: the classic film's game; verification is one xor. Guessable:
   demo shows a near-copy of the clue with one heap smaller; the "xor to zero" rule is the aha.
5. **TOPPLE** (was LUKAS; renamed to avoid a clash with logic-agent's `lukas`) — `"3728=24"` → an **RPN** expression over `+ - *` using each digit exactly once
   that evaluates to the target. Fun: 24-game with a twist; no eval() needed, the scorer runs a
   7-token stack machine. Guessable: demo reveals postfix notation; hard part is the search.
6. **GRAYLING** — `"0110 1011 6"` → a path of exactly 6 one-bit flips from start to end visiting
   **distinct** bitstrings. Fun: self-avoiding walk on a hypercube (Gray-code flavour).
   Guessable: demo shows the flip-one-bit chain; exact length + distinctness learned from 0s.
7. **CRATE** (bin packing) — `"8 3 5 7 2 6|10|3"` → a digit per item naming its bin, every bin
   ≤ cap. Cheap scorer (~200 chars). Dropped only for slot count; strong reserve.
8. **HOARD** (knapsack) — `"w,v pairs|cap|minvalue"` → bitmask with weight ≤ cap and value ≥ bound.
   Scorer needs two sums + two comparisons, ~230 chars: feasible but close to TARE in feel.
9. **TENDER** (coin change, exactly k coins) — `"1 3 7 11|29|5"` → five denominations summing to 29.
   Very short scorer; rejected as too close to TARE.
10. **BLANKET** (set cover ≤ k) — universe + sets as bitstrings + k → indices whose OR is full.
    Scorer ~230 chars. Nice, but the clue gets long and it duplicates TARE's "pick a subset" verb.
11. **OXO** (tic-tac-toe winning cell) — `"XOX..O..X"` → the index X plays to make three in a row.
    Scorer must carry the 8 lines as `'012345678036147258048246'` (~230 chars). Cut: overlaps the
    grids direction, and a 9-way guess gives ~11% free credit (bad gradient).
12. **LUHNACY** (checksum completion) — 15 digits → a 16-digit Luhn-valid extension. Scorer fits
    (~190) but the whole puzzle is one hidden check digit: 1-in-10 blind luck, no partial gradient.
    Cut for discoverability.

## Chosen 6 (2 easy / 2 medium / 2 hard)
TARE (easy), BASILISK (easy), HANSOM (medium), MARIENBAD (medium), TOPPLE (hard), GRAYLING (hard).

| name      | meaning                                            | diff   | solve ms (mean/max) | score chars |
|-----------|----------------------------------------------------|--------|---------------------|-------------|
| TARE      | subset-sum to target, answer = 0/1 bitmask          | easy   | 0.08 / 0.50         | 154 |
| BASILISK  | re-encode a number from base A to base B            | easy   | 0.00 / 0.01         | 158 |
| HANSOM    | taxicab TSP tour <= bound, answer = permutation     | medium | 0.10 / 1.06         | 238 |
| MARIENBAD | Nim: the position after the winning move (xor 0)    | medium | 0.00 / 0.04         | 249 |
| TOPPLE    | RPN expression over + - * hitting a target          | hard   | 0.52 / 2.89         | 255 |
| GRAYLING  | exact-length self-avoiding one-bit-flip path        | hard   | 0.18 / 15.2 (p99 2) | 238 |

All six: `quickcheck --seeds 200` => OK, zero errors, zero warnings; scorers never raise on
4 KB junk (worst scorer time 1.5 ms on an adversarial `9*2048 + '*'*2047` RPN bomb).

## Rejected *because of the 256-char scorer cap*
* **Euclidean** TSP (needed `((dx*dx+dy*dy)**.5)` plus a tolerance ⇒ ~40 chars more than taxicab).
* Max-flow-lite / min-cut: verifying conservation at every node + capacity + value ≥ bound is
  ~400 chars however it is written. Would need ~400 to be viable.
* Full 24-game with **division** (fractions.Fraction + zero-division guard): ~320 chars.
* Job-shop / interval scheduling ≥ k with *weights*: parse + sort + overlap + weight sum ≈ 300.
* Multi-constraint knapsack (2 resources) ≈ 300.
