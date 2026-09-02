# quilm — SOLVED (confidence: certain, 2579/2579 in the final)

Clue `A B` -> answer `x y`, two B-digit decimal numbers.

RULE: on a seven-segment display, y is x with matchsticks ADDED.
  * for every position i, segments(x_i) must be a STRICT subset of segments(y_i)
    (so every digit must change — a position that gains 0 segments is illegal)
  * total segments added over all B positions == A

Segment counts: 0:6 1:2 2:5 3:5 4:4 5:5 6:6 7:3 8:7 9:6

Growth moves from '1' (2 segments): 1->7 (+1), 1->4 (+2), 1->3 (+3),
1->9 (+4), 1->0 (+4), 1->8 (+5).  Max gain per position is 5.

SOLVER: x = "111...1"; greedily give each position gain g = clamp(A-remaining,1,5)
and map g -> {1:'7',2:'4',3:'3',4:'9',5:'8'}.  O(B), table-cached: 0.1 us/answer.

Clue space is exactly 50: B in 3..6, A in [B+2, 4B] (drawn uniformly).

## How it was found
r1 skip-all -> 806 clues, established clue grammar.
Demos 1-2 both happened to satisfy popcount(x)+popcount(y)==A; demo 3 killed it
(r2 scored 0/494 on that hypothesis).  r3 random probing: 1 hit in 502 (0.2%).
r4 perturbed the 5 known-good answers -> some digit permutations kept scoring 1,
others didn't; x+-1 always failed.  r5 sent single-digit edits of known-good
answers against *other* clues: hits revealed w(1)=2, w(4)=4, w(0)=w(6)=w(9)=6
with opposite signs for x and y -> seven-segment counts, A = seg(y) - seg(x).
The "every digit must change" clause came from 11 items that fit the arithmetic
but scored 0 — all had a position where x_i == y_i.
