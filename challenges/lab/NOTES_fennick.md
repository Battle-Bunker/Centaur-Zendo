
## v2 ladder run `lad-fennick-v2-1` (6×0.5 s, 2 players)

| team | profile | final | cracked round | demos |
|---|---|---|---|---|
| fennick1a | opus-lowdemo (max 2 demos) | 0% | – | 2 |
| fennick1b | opus-theorist | 100% | 4 | 3 |

Mean final 50% — the first genuinely split result on this class. v1 was 1%/1% (object unrecognised);
v2's drawn tilts (`/` and `\` caps, bars standing in the gap) fixed recognition: both players got
"it's a rendered bar chart" from demo 1 and reproduced demos byte-for-byte given the true heights.

What separated them was the **bar-height rule**. The lowdemo player spent rounds 3–4 running 40
candidate height rules as index-cycled arms (all 0) and searched every local feature
(same-letter counts in windows, distances to dots, position-in-token…) — best fit 21/47 — and never
found the global multi-pass reading. The theorist, with a third demo, got it in round 4.

The lowdemo player's own post-mortem is the kid-test in one line: *"a kid looking at the demo would
more likely see it as one shape — a skyline — and ask what is going up and down here, left to right"*
rather than hunting an arithmetic formula per bar. It also read `/` and `\` as bookkeeping
("displaced left/right") instead of as slopes. Same pattern as LegoZendo/virel/tovel: the picture
reading is the rule, the table reading is the detour.

Player feedback worth keeping: a one-class pool is high-variance (skip-all final scored 0 with no
fallback); the 4-of-6-letter spec reads as noise and once silently omitted a real displacement,
which cost trust in a correct reading. Consider making the spec complete (a proper checksum) — it
does not give the height rule away and would remove a source of false doubt.

Status: testing, 2 finals, 1 crack. Needs 2 more finals on other profiles before calibration.

Correction after reading the theorist's report: there is no height rule to find. Heights are free
(any physically consistent drawing with the right lean counts scores 1); the rule is the tipping
physics — a book tips iff one side is an empty slot, the other side is a touching book, and the book
across the gap is strictly taller. The theorist saw from demo 3 that heights "float", stopped
searching for a formula, and built its own witness (every book 2 high, leaners cut to 1). The
lowdemo player never had that third demo and spent the whole game on the red herring. So the
split is exactly the intended one: "the tall ones are just tall — stop trying to work out why" is the
kid insight, and it was reached by one Opus player in four rounds and by the other never.

Theorist's fairness note: the four-letter tally is partial (the reference had leaners of unlisted
letters). Fine as designed, but a future version could say so in the clue shape, e.g. always list
the same four letters, so nobody wins by the lucky assumption "unlisted = zero".
