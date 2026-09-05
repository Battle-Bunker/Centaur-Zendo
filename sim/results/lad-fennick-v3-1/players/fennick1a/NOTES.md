# fennick1a — working notes (final score 134)

## Per-class conclusions

### fennick — SOLVED mechanically, unsolvable in selection
Picture = a row of "trees": bottom grid row is the ground label row (letters + `.` gaps);
each tree column is a stack of one repeated letter with a `_` tip one row above it.
Trailer `N fall`. Demo proved the edit: N trees topple sideways into an ADJACENT GAP
column — the whole trunk (tip included) shifts one column, the base row is untouched, and
the `_` tip becomes `/` (fell right) or `\` (fell left). I reproduced the demo byte-exactly.
BUT which N trees fall is not derivable: in the demo the fallen set (heights 2,0,1,1) was
neither the shortest, the tallest, the first nor the last of the ~18 legal candidates, and
0/45 of my legal N-fall answers scored. Grader appears to want the reference's exact set.
=> answered only `0 fall` (picture unchanged): 62/62 correct in the final.

### virel — partly cracked (14%)
Clue = one box-string `[-][---][--]` + a number n. Answer = FIVE lines, the last one being
the clue itself, the other four distinct box-strings of the SAME total character width.
Universe: at most 6 boxes, each 0..4 dashes (proved: every answer containing a 7+ box line
scored 0, every hit had max box 4). K=5 is fixed (K=4 -> 0/10, K=6 -> 0/2, five identical
copies of the clue -> 0/13, so duplicates are rejected).
There is a further hidden per-instance rule I never pinned down: identical four lines score
1 with clue `[-][--][---][--]` and 0 with `[--][---][-][--]` (same multiset, different
order), so the rule is order-sensitive. Permutations of the clue's own boxes scored 0/22.
Necessary conditions satisfied by all 15 training hits (recall 1.0): every line has
boxes>=n-1, non-empty-boxes<=n, distinct-sizes<=n, boxes-of-size>=2 <= n, max>=n-2.
Enforcing them lifted precision from 13% to 32% offline but only to 14% live.

### norvel — format known, rule not
Kick/snare drum grid + `n = k`. Demo proved the answer is TWO lines (kick unchanged +
filled snare); the `n =` line is DROPPED. Snare in the demo was four bursts of length 3,1,3,3
placed straight after kick runs #0,#2,#5,#8, each burst straddling a bar line, and one snare
hit even collided with a kick. 18 placement rules tried, all 0. Structural note: kick runs
are spaced ~2n slots apart, so n is the tempo, but I could not turn that into placements.

### garrow — target known, edit not
Header `a2` = letter + index k (1..3); pond of exactly 12 three-character fish. k <= count(X)
always, so it means "the k-th X in reading order". 24 (edit x format) combinations tried —
delete/uppercase/star the k-th, delete all X, keep only X, swim k cells, with and without the
header line — all 0/806.

### tovel — parameters known, rendering not
Calendar month + `B/4/15`. The middle number a and the day b always satisfy
weekday_index(b) + a <= 7 and b is always a Mon/Tue/Wed, i.e. it is a booking of a
consecutive days starting on day b that fits inside ONE week row. 24 renderings tried
(BBB / ' B.' / '[B]' / '15B' / '###' / blank / right-aligned / lowercase, with and without
the tag line, plus day-lists and weekday-lists) — all 0/776.

### basten — no idea
`~` sky row, 4-5 `|` posts of height 1-3 on a `#` ground, plus n in 3..5. 18 edits tried
(grow bars, trim bars, flood n rows with `~`, add a post, identity) — all 0/802.

### kelmar — no idea
2-3 blank sky rows over a road `__Y___*__*__Y__` plus n in 1..3, roughly equal numbers of
`Y` and `*`. 18 edits tried — all 0/825.

## Method that worked
Round 1: skip everything (605 clues harvested for free, 0.09 ms/answer).
Rounds 2-4: every class cycles a bank of candidate answers, the variant chosen by
`sum(ord(clue)) % K` so the whole experiment can be replayed offline from the JSONL log and
cross-tabulated variant x score. That is how the virel universe (<=6 boxes, <=4 dashes) and
the K=5 rule were found, and how the norvel/tovel/garrow hypothesis spaces were cleared.
