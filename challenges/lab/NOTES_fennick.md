
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

---

## v3, 2026-09-04 (demo-economy pass for the 7-class / 4-round / 3-demo format)

**What changed.** The heights moved *into the clue*. v2's clue was `LAYOUT/TALLY` and the answer was a
picture the player had to build from scratch, choosing a height for every book so that four per-letter
tallies came out right — a search that cost the losing player two whole rounds and ~40 candidate height
laws, and that the winner only escaped with a third demo ("there is no height rule; heights are free").
That detour is gone. v3's clue **is the finished shelf with every book standing upright**, and the answer
is **that same picture with the right books tipped over**. Concretely:

* clue = picture rows (right-stripped) + a `====` shelf row + a line `4 fall` (how many books fall).
  181–342 chars, 34–42 slots, 2–7 picture rows.
* answer = the clue with each falling book redrawn: its foot letter stays in its slot on the bottom row,
  its other `h-1` letters and its cap move one column into the empty slot it falls into, and the cap
  becomes `/` (leaning right) or `\` (leaning left). Standing books, shelf row and the `n fall` line are
  copied unchanged. The `n fall` line may be kept or dropped; both score 1. The answer is **unique**.
* the four-letter tally is gone (with heights given it constrained nothing), which also retires the
  theorist's fairness complaint about unlisted letters being assumed zero.
* rule unchanged since v1, and now sayable in one breath: **a book falls over if there is a gap on one
  side and a taller book just across it** (books with books on both sides are held up; books with gaps on
  both sides have nothing pushing them over; across a two-slot gap there is nothing within reach; equal
  heights and both stay up).
* `solve()` no longer searches: 4.1 ms → 0.03 ms.

**Every demo now teaches the whole rule.** `generate()` plants, in every instance: ≥4 tipped books
(mean 4.3); ≥1 pair of *equal-height* books facing each other across a one-slot gap, both standing
(100 % of clues, which is what kills the `>=` near-miss); ≥1 book with gaps on both sides, at least two
high, standing (98.5 %); ≥2 books beside a two-slot gap, standing (100 %); and ~4.6 books that stand
beside a gap because the book across it is shorter (100 %). One demo therefore shows the positive case
and all three near-misses side by side.

One demo as it renders (seed 7 of the shipped generator; rows padded here for alignment):

```
CLUE                                    ANSWER
 _         _ __    _  _    _  _  _       _         _ __    _  _    _  _  _
 F    _    F RR    S  R_   R_ R_ F       F    _    F RR    S  R_   R /R /F
 F   _R _ _F RR  _ S  RK_  RK RC F__     F   _R _ _F RR   /S  RK_  R KR CF__
_F_  KR R FF RR _R S  RKC  RK RC FKC    _F_  KR R FF RR\  RS  RKC  R KR CFKC
FFC..KR.R.FF.RR.CR.S..RKC..RK.RC.FKC    FFC..KR.R.FF.RR.CR.S..RKC..RK.RC.FKC
====================================    ====================================
4 fall                                  4 fall
```

Four books have tipped and nothing else moved (slots numbered from 0; heights
`141..23.2.24.44.12.4..432..43.43.422`). The one-high `C` at 16 falls left over the gap at 15 onto the
four-high `R` at 14 (`\`); the two-high `R` at 17 falls right over the gap at 18 onto the four-high `S`
at 19 (`/`); `K` at 28 and `C` at 31 (both three high) fall right onto the four-high `R` at 30 and `F`
at 33. Standing beside them, in the same picture: the `S` at 19 has gaps on **both** sides and stays up;
`F` at 11 and `R` at 13 are **equal** at four high across the gap at 12 and both stay up; and the `C` at 2
has a gap on its right, but that gap is **two** slots wide (3 and 4), so there is nothing within reach and
it stays up too. Those are exactly the three near-misses, drawn next to the positive case.

**Witness table** (2000 fresh clues, shipped scorer; every wrong-rule template is drawn with the *true*
convention, i.e. it models a player who has seen a demo and holds the wrong rule):

| template | rate |
|---|---|
| clue picture returned unchanged | **13.0 %** ← foothold |
| all books upright, `n fall` line dropped | **13.0 %** ← same thing, lenient form |
| every book tipped into a gap | 0.0 % |
| tip toward any taller neighbour (no gap) | 0.0 % |
| tip toward its one gap, height ignored | 0.0 % |
| tip toward any gap, height ignored | 0.0 % |
| near-miss `>=` instead of `>` | 0.0 % |
| near-miss "gaps on both sides count too" | 19.2 % |
| near-miss "nearest book beyond any gap" | 14.2 % |
| random tilts | 0.0 % |
| demo replay (another clue's answer) | 0.0 % |
| constant string | 0.0 % |
| junk / empty / clue fragments | 0.0 % |
| TRUE RULE (`solve`) | 100.0 % |

The foothold is the first two rows: 12.7 % of clues (8000 seeds) say `0 fall`, and on those the correct
answer *is* the clue's picture unchanged. So a demo-less player who echoes the clue scores ~13 %, and one
who reads the count line scores exactly that deliberately. Nothing else exceeds ~19 %, well under the
~50 % ceiling; the two surviving near-misses are the intended gradient (wrong-but-close ≈ foothold,
exact ⇒ 100 %) and both are contradicted by every demo. Cost of the foothold: ~13 % of demo requests land
on a shelf where nothing falls; the zero-tip branch is tuned (p = 0.075) to keep that risk low while
holding the foothold above 10 %.

**What a demo-less player can infer.** The clue is already a drawn bookshelf, a shelf line and "4 fall",
so the answer's shape is fully visible: it is this picture, same width, same rows, with four books
somehow knocked over — a well-formed attempt is "send the picture back, maybe with something tipped",
and on `0 fall` instances that literal echo is correct. What the demo buys is the *how* (a falling book's
body slides one column into the gap and its cap becomes `/` or `\`) and the *which* (gap on one side,
taller book across).

**Engineering** (8000 seeds; 1000 solved/scored): generate avg 0.12 ms / p99 0.52 ms / max 1.1 ms, 0
fallback uses; solve avg 0.03 ms max 0.07 ms; score avg 0.030 ms max 0.094 ms, ≤0.09 ms on junk; scorer
496/512 chars, solve 1045/5000, clue 181–342/1024, solution 184–342/1024; 3000/3000 clues distinct and
deterministic; 1000/1000 `solve()` outputs score 1; 20 hand-built well-formedness attacks all 0 (no shelf
row, two shelf rows, dashes for `=`, short shelf, leading blank row, rows reversed, mirrored, caps
removed, tilts straightened, `/`↔`\` swapped, dots for spaces, wrong count line, count forced to 0,
answer + junk line, 4000 chars of junk, empty). Declared leniencies: trailing whitespace/newlines, rows
right-padded or right-stripped, junk beyond column W, and the count line present or absent.
`python tools/quickcheck.py challenges/lab/fennick.json --seeds 200` → OK (the one warning, "score
accepts the clue itself as a solution", is the foothold by construction).

v2 kept byte-identical as `challenges/lab/fennick.v2.json` (verified against commit 07dc2e3).
Not committed; arena not opened (orchestrator's job).
