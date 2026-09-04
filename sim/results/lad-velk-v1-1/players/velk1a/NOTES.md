# velk — solved

Clue format: `WORD|k`  (WORD 4-6 uppercase letters, k = 2..6 in training).

Answer: a crossing / braid ladder diagram.
* Row 0 = the word, letters joined by single spaces (width 2n-1).
* Separator lines: n bars `| | | ...`; one adjacent pair replaced by a mark
  (`\` or `/`) at column 2i+1 with spaces at 2i and 2i+2; trailing space stripped.
  That mark means the two letters at positions i, i+1 swap in the next row.
* THE RULE: exactly 2k-1 crossings, strictly ALTERNATING —
  the strand that starts in position 0 (the "hunt") is in crossings 1,3,5,...
  (k of them); crossings 2,4,6,... involve any other pair.
* Free choices (all verified to score 1): which non-hunt pair crosses, the
  mark on non-hunt crossings, and which way the hunt moves.
  Convention kept from the demo: `\` = hunt moves right, `/` = hunt moves left.

Evidence: round 1 cycled 12 answer shapes over 511 items, 3 correct — all three
had (2k-1 crossings AND alternating). 28 items had 2k-1 crossings and k hunt
crossings but were NOT alternating: all scored 0. Rounds 2-6: 2477/2477.

Not required (demo 2 proved the class is more permissive than this family):
DWKOA|5 was answered by the reference solver with 15 crossings and no
alternation, so some looser invariant also passes. Irrelevant — the family
above is always accepted.

Speed: per-(n,k) `%`-format template + operator.itemgetter built in
on_round_start; a solve is one dict lookup + one interpolation, ~1.9 us.
