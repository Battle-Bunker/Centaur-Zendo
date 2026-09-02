# quilm — SOLVED (final: 3030/3030)

Clue: "a b".  Answer: two b-digit zero-padded digit strings "x y" such that, on a
seven-segment display, for EVERY position i:
  * segments(x[i]) is a subset of segments(y[i])
  * x[i] != y[i]  (the subset must be strict — at least one segment added)
and the total number of segments switched on over all b positions == a.

Segment masks (a=1,b=2,c=4,d=8,e=16,f=32,g=64):
  0:63 1:6 2:91 3:79 4:102 5:109 6:125 7:7 8:127 9:111

Construction used: per-position "add v segments" pairs
  v=1 (0,8)  v=2 (5,8)  v=3 (7,9)  v=4 (1,9)  v=5 (1,8)
Greedy: give each of the b positions 1, then pour the surplus a-b in chunks of <=4.
Whole table for b=1..12 precomputed at import; solve() is one dict lookup (~0.09us).

Clue ranges observed: b in 3..6, a in [b+2, 4b].
Evidence: 1430 logged rows + 4 demos, zero mismatches against this rule.
