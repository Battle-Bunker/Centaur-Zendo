# quilm — notes

Only ONE class in the pool: `quilm`.

Clue format: `<digit string>/<K>` where digit string has length 3..6 (leading
zeros allowed, ~11% of clues) and K in {1,2,3,4} (freq 2:223, 3:174, 4:81, 1:72).

Known (clue -> correct) pairs:
| N | K | X (correct) | source |
|---|---|---|---|
| 7830 | 4 | 5220 | demo 1 |
| 2931 | 3 | 4991 | demo 2 |
| 7708 | 4 | 5138 | round1 hit (formula N*K//6) |
| 3000 | 4 | 2996 | round1 hit (formula N-K) |
| 548  | 2 | 550  | round1 hit (formula N+K) |

Round 1: 550 presented, 498 answered, 3 correct (0.6%).

Observations:
- X always has the same number of digits as N in these samples.
- X has the same PARITY as N in all 5 samples.
- Three mutually inconsistent formulas each scored 1 => the accepting
  predicate is probably LOOSE (many valid answers), density ~2.4% for
  arbitrary numeric formulas.
- 7830*2/3 = 5220 exactly and 7708*2/3 = 5138.67 -> 5138 both hit (K=4),
  but 3000 (K=4) accepted 2996, so 2/3 is not THE rule.

Round 2 plan: measurement round. Split challenges between density probes
(uniform random same-length; N+/-small delta) and ~12 structural formulas,
then read per-family hit rates from the log.

## After round 2 + demo 3

Ground truth so far (N, K, X):
7830 4 5220 | 2931 3 4991 | 3339 2 8739 | 7708 4 5138 | 3000 4 2996
548 2 550 | 9384 2 9393 | 3748 2 3756 | 1239 2 1248 | 325 3 332 | 19129 2 19130

Round 2 families: uniform-random same length 0/124, N+-delta(1..9) 5/120,
every structural formula (identity, reverse, N*K, N//K, sorted, kaprekar,
complements, digitwise*K) 0/30 each.

KEY STRUCTURE: in every known pair, X has the SAME LENGTH as N and X differs
from N only inside a CONTIGUOUS WINDOW OF K DIGITS. Verified on all 11:
  3339/2 window[0:2] 33->87 ; 9384/2 [2:4] 84->93 ; 3748/2 [2:4] 48->56
  1239/2 [2:4] 39->48 ; 19129/2 [3:5] 29->30 ; 548/2 [1:3] 48->50
  2931/3 [0:3] 293->499 ; 325/3 [0:3] 325->332
  7830/4 [0:4] ; 7708/4 [0:4]... 7708->5138 [0:3] ; 3000/4 [0:4]
So K = size of the editable window. That explains uniform-random 0/124.
But window-containment alone is NOT sufficient (most N+-delta answers are
inside a 2-window yet only 4% scored) -> there is an extra property P.

Round 3 plan: mostly random K-window replacements (should hit ~P's density,
harvesting many true pairs), plus probes for window size K+1 / 1.

## SOLVED — the rule

quilm, clue `<digit string>/<K>`:
Render the digit string on seven-segment (calculator) displays and MOVE
EXACTLY K MATCHSTICKS. The answer is the same-length digit string X with
    sum_i |seg(n_i) \ seg(x_i)| == sum_i |seg(x_i) \ seg(n_i)| == K
(matches removed == matches added == K; total lit segments conserved).
Leading zeros in the answer are accepted. An answer that is a pure ANAGRAM
of the clue's digits is REJECTED (that is the only extra constraint).
Some strings are unsolvable for a given K (e.g. "888/4" — 8 can only lose
segments), so return None there.

Round 5 (rule, no anagram guard): 490/495. Round 6 (with guard): 465/465.
FINAL: 2698 presented / 2698 answered / 2698 correct.
