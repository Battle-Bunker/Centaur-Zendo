# NOTES — direction: music, rhythm and dance

Designer session 2026-09-04. Target: a class Opus centaurs crack ~half the time in 6×0.5 s
rounds with 6 demos, that a 12-year-old recognises instantly and can hypothesise about.
Read first: LADDER.md, REPORT.md, DESIGN_LOOP.md (12-year-old test ×2, levers 7/8/9),
SPEC §2–4, LegoZendo/Wordz, CHALLENGE_AUTHORING §3b, STARS.md, NOTES_game "conclusion",
and the last run sections of NOTES_fennick / _nature / _kitchen / _time.

## The three constraints I designed against

1. **Salience (lever 9).** Players rebuild the picture grammar perfectly and then hunt
   statistics. Whatever is counted must be the loudest thing in the drawing, not a
   quantity you have to segment the picture to see.
2. **Statistic-space size.** A picture with 3 binary rows and no horizontal structure has a
   *tiny* space of cell-level statistics: the 8-entry column-type histogram plus a handful
   of adjacency counts. Any cell/column-level rule on such a picture is found by a sweep in
   one round (this killed ideas 1–3 below). Difficulty in this direction has to live in the
   **horizontal** dimension — runs, holes, distances — which is also where music lives.
3. **Anchoring (transfer).** If the counted relation does not involve the clue-pinned part
   of the picture, one answer per value of N serves every clue and six demos are worth
   100 %. Every survivor below has the count anchored to the pinned row.

## Brainstorm (12 ideas, each with the 12-year-old test)

| # | object (kid sees…) | the measurement | verdict |
|---|---|---|---|
| 1 | step sequencer, 3 rows `x`/`.` | beats where the kick is followed by a snare | **no** — cell-level; the model sweeps all 16 ordered symbol pairs × 3 counts in one round |
| 2 | body-percussion **round**: 3 voices playing the same bar-long pattern, each starting a bar later (prettiest picture of the lot) | beats where exactly two of the three clap | **no** — the picture is one string repeated, so the whole statistic space is "count columns with exactly k of symbol s" (≈24 numbers). Kept as a fallback *object*; the format is genuinely lovely and instantly reads as a round |
| 3 | dance-mat footprint chart, `L`/`R` on a floor of dots | poses where the feet are crossed | **no** — first- or second-guess relation between the only two tokens in a row; the state/event ambiguity is a trap, not a gradient |
| 4 | piano-roll melody (GarageBand) | notes repeated exactly one bar later at the same pitch and length | **no** — the bar lines advertise the lag, and pitch drags in the model's strongest music prior (scales, intervals, transposition) |
| 5 | handbell/boomwhacker class chart, one kid per note | times one kid must play twice in a row | **no** — weak picture (a table), shallow rule (per-row adjacency) |
| 6 | setlist with song lengths drawn as bars | songs shorter than both neighbours | **no** — numbers anti-pattern; "local minimum" is nameable |
| 7 | skipping-rope rhyme: words + jumps | words whose length equals the jumps after them | **no** — arithmetic-on-words, an RLVR shape; the picture is a line of text |
| 8 | xylophone bars + a mallet path | bars struck twice | **no** — weak picture, shallow rule |
| 9 | sticking chart `R L R R L` with accents | accents played by the weak hand | **no** — named (paradiddle, accent), shallow |
| 10 | marching/dance formation grid of `^ v < >` | dancers facing a partner | **no** — cell-level pair relation, and barely music |
| 11 | **drum-machine grid; the clue pins the kick row** | **the kick's rests that the second drum fills EXACTLY — same first beat, same last beat, no more, no less** | **YES — built as `norvel`** |
| 12 | same grid | snare runs whose length equals a kick run's length (unison echo) | **no** — a straight transposition of virel's twin stacks |

## Why 11 passes the 12-year-old test

* **Object from one demo.** Three labelled rows of `x` and `.` chopped into bars of four,
  labelled `kick / snare / hat` (or `boom / bang / tss`, `bass / clap / shaker`, …). Every
  kid who has opened GarageBand, a drum-machine toy or a music app says "that's a beat".
  The picture is 3–4 lines and 20–43 characters wide.
* **The pattern is not nameable.** The object's famous operations are "four on the floor",
  "the backbeat on 2 and 4", "how many hits per bar". The rule is none of them: it is a
  relation between a *hole* in one row and a *run* in another, and the whole difficulty is
  the word **exactly**. Drummers have a word for playing in the gaps ("a fill"), which is
  the shallow hypothesis the demos falsify — no one has a word for "a fill that starts on
  the first empty beat and ends on the last one".
* **The kid sentence.** *"The snare fills up two of the kick's holes exactly — look, it
  starts the beat the kick stops and stops the beat the kick comes back."* A 12-year-old
  can say that from one demo, and can point at the near-misses that don't count.
* **Anchored.** The holes belong to the clue row, so no answer transfers between clues.

## The rule as shipped (private)

Clue `K/n`: `K` is a 16/20/24/28-step kick row over `x`/`.` that starts and ends with `x`
and has G = 4–8 maximal holes (each 1–5 beats, at most one of length 1, at least one ≥3, at
least two distinct lengths); `n` is 2–5 with G = n + 1..4, and is never the number of holes,
the number of kick runs, the number of kick hits or the longest hole. (Both bounds were set
by measurement, not taste — see the witness table below.)

The answer is any picture that contains **exactly three** rows of `x`/`.` once every other
character is deleted (labels, bar lines, beat numbers, spaces are all free), all as long as
`K`, the **first one equal to `K`**, and in which **exactly `n` of the maximal runs of `x`
in the second row have exactly the same span as a maximal run of `.` in `K`**. The third
row is free and is where the "any drum will do" hypothesis goes to die.

Discovery path: (a) it's a drum grid and the top line is the clue — round 1; (b) the second
row is what matters, not the third — the demos separate them; (c) something about the
snare and the kick's holes — the demo headline; (d) **exactly**, not "inside" — the
near-misses in every demo. (d) is the step that decides the run.

## Levers held in reserve

* Too easy → count only holes of length ≥2; or require the hat to be silent for the whole
  of a counted hole; or make the counted row the one the clue *names*.
* Too hard → put the number of holes in the clue as a second field; or guarantee three
  exact fills of length ≥3 per demo; or drop the third row.

---------------------------------------------------------------------------

# `norvel` — shipped v1 (`challenges/lab/norvel.json`)

## What a player sees

Clue `x..x..x..x..xx...x..x..x/4`, and a demo like

```
      1    2    3    4    5    6
boom |x..x|..x.|.x..|xx..|.x..|x..x|
bang |.xx.|.x.x|x.xx|..xx|x..x|.xxx|
 tss |xxx.|xx.x|xx.x|xx.x|x..x|....|
```

Three drum rows chopped into bars of four; the top row is the clue, verbatim. Instrument names,
bar lines and the beat header are randomised per demo (`kick/snare/hat`, `bd/sn/hh`, `boom/bang/tss`,
`1/2/3`, `foot/hand/voice`, …) and the grader ignores everything that is not `x` or `.`.

## The rule (private)

The kick row has G = 4–8 **holes** (maximal runs of `.`, 1–5 steps). Score 1 iff the picture has
exactly three x/. rows of the clue's length, the first equal to the clue, and **exactly `n` of the
maximal runs of `x` in the SECOND row have exactly the same span as a hole** — same first beat,
same last beat. `n` is 2–5 and G = n + 1..4, so `n` is never the number of holes, of kick runs,
of kick hits, or the longest hole. The third row is free.

Kid sentence: *"the snare fills up four of the kick's holes exactly — it starts the beat the kick
stops and stops the beat the kick comes back."*

## Intended discovery path

1. **Round 1, one demo:** it's a drum grid; the top line is the clue. (The grammar is trivial —
   that is deliberate; every measured player rebuilds picture grammars perfectly.)
2. The second row is the counted one, not the third: every demo has row 3 exactly filling a
   *different* number of holes.
3. The relationship is between the snare's runs and the kick's holes — the headline of the drawing.
4. **EXACTLY**, not "inside" and not "over". Every demo carries a run that is too short (inside a
   hole, 66 %), a run that is too long (covers a hole and spills over a kick hit, 100 %) and a run
   as long as a hole but in the wrong place (89 %). This step is what decides the run.

## Witness table (800 fresh clues, same harness for every row)

| strategy | score |
|---|---|
| the true rule (`solve`) | **100.00 %** |
| empty / `"1"*100` / clue echoed / 4000 chars of x and dots | 0.00 % |
| copy the clue row three times | 0.00 % |
| clue row + two empty rows / two full rows | 0.00 % |
| a well-formed random picture (density 0.2 → 0.8) | 0.04 – 0.62 % |
| **COMPLEMENT** — fill every hole exactly | **0.00 %** (closed by n < G) |
| complement, one hole dropped | 34.62 % |
| complement, two holes dropped | 27.62 % |
| "always fill exactly k holes", k = 1 / 2 / 3 / 4 | 0.0 / 30.1 / 29.6 / 28.9 % |
| graft: an old answer's rows 2–3 under the new clue row | 1.88 % |
| …grafted from a demo with the same n | 1.12 % |
| previous clue's answer (demo replay) | 0.00 % |
| one fixed real answer for every clue | 0.12 % |
| **n holes get a random run INSIDE (the loose reading)** | **7.50 %** |
| n holes: run flush to the hole's left edge | 8.58 % |
| n holes get ONE snare hit | 0.00 % |
| n holes COVERED with a spill either side | 0.00 % |
| n unison hits on the kick | 0.00 % |
| exactly n snare runs, anywhere | 0.17 % |
| right rule but applied to row 3 | 0.56 % |
| right rule, rows 2 and 3 swapped | 0.00 % |
| right rule but n−1 / n+1 holes | 0.00 % / 0.00 % |
| fill n random holes exactly (= the rule, built blind) | 100.00 % |

Read it as a gradient: **0 %** (no idea) → **0.5 %** (the format only) → **7–9 %** (snare runs in
the kick's holes — the foothold DESIGN_LOOP lever 7 asks for) → **28–35 %** (the *exact* match
found, the meaning of `n` missed) → **100 %** (the rule). The two levers that mattered:

* `n < G` kills the complement outright, and **G − n is spread over 1,2,3,4 on purpose** so that no
  constant guess ("fill all but two holes", "always fill three") pays more than ~35 %. An earlier
  build had G = n+2 in two thirds of clues and "complement minus two holes" scored **84 %** — the
  tovel-stripe failure mode exactly, found only because the table tests templates, not just laws.
* At most one hole of length 1. With many 1-holes, any run placed inside a hole *is* an exact fill
  and the loose reading scored 26 % instead of 7.5 %.

## Fairness (hypothesis-elimination surrogate)

141 hand-built "count a relation in this picture" counters (runs/hits/rests of row 2, row 3 or
both; runs equal to / inside / covering / overlapping / as long as / starting where / ending where
a hole or a kick run; holes touched, holes with exactly one hit, holes covered, holes silent;
column histograms; per-pair column agreements; identical bars; clue-only readings).

Mean survivors after 1…6 demos: **12.2 → 4.4 → 1.9 → 1.5 → 1.1 → 1.0**, and the last survivor is
the true rule in **12/12** trials. So the class is fair — the rule is uniquely pinned by three or
four demos — and all of its difficulty sits in *generating* the hypothesis, which is exactly where
the ladder wants it (orlan's lesson: a rule the players never propose is unreachable; this one is
one refinement below a hypothesis they all propose).

## Validation

`python tools/quickcheck.py challenges/lab/norvel.json --seeds 200` → **OK, no warnings**
(`gen=0.14 ms score=0.08 ms solve=50.8 ms`). Sizes: **score 281/512**, solve 4871/5000,
generate 1127; clue ≤ 30 chars, solution ≤ ~180.

* `solve()` scores 1 on **3500/3500** fresh clues (1500 + 2000 runs), mean 12 ms, p99 42 ms, max 52 ms.
* `generate` deterministic on 3000 seeds, 0.03 ms mean / 0.14 ms worst; n uniform over 2–5;
  2757 distinct clues per 3000 seeds.
* Scorer on **63 000 junk strings** (empty, unicode, 1024 zeros, 4000-char noise, the clue itself,
  40-line blocks): 0 raises, 0 non-binary, worst 0.49 ms.
* Scorer vs an **independent re-implementation** (no regex, written from the description) on
  **10 400 mutated answers**: 0 disagreements.
* Leniency (all 100 %): bare rows, bar lines, labels + header, blank lines between rows, leading and
  trailing spaces, tabs, CRLF. Strictness (all 0 %): rows reversed, rows 2/3 swapped, 2 rows, 4 rows,
  one wrong character in the clue row, row 2 shifted by one, row 2 emptied, all rows on one line.
  (Row 2 reversed scores 2.5 % — palindromic coincidences, not a strategy.)

## Predicted classification

**testing / on target, mean final 45–65 %.** The rule is one refinement below the hypothesis every
player generates ("the snare plays in the kick's gaps"), the demos falsify the loose reading in
every single instance, and no template pays more than ~35 % without the insight. The likeliest
split is one crack in rounds 3–5 and one player parked at 8–30 % on "runs inside the holes" or
"exact fills, wrong count". Predicted kid score **4.3–4.7/5**: the object is a drum machine (as
recognisable as LegoZendo's bricks), the drawing is three lines, and "it fills the hole exactly"
is a sentence a 12-year-old says before an optimiser does.

**Risk:** too_easy rather than too_hard — the picture's alphabet is small, and a player who
systematically sweeps run/hole relations will find the truth (141-counter test: unique after four
demos). If two players crack it, apply lever 1 (count only holes ≥ 2 long, which also removes the
free length-1 fills) or lever 2 (the third row must be silent for the whole of a counted hole).

Scratch harness used for all the numbers above (not committed):
`$SCRATCH/music/{harness,attack,demostats,selftest,hyp}.py`.

## norvel v1 ladder run `lad-norvel-v1-1` (2026-09-04, 6×0.5 s, 2 Opus players)

| team | profile | final | demos | reading |
|---|---|---|---|---|
| norvel1a | opus-default | 27% | 4 | fitted a sampler ("at a kick rest both voices play p=.78; at a kick hit one doubles p=.2") |
| norvel1b | opus-kidproxy | 36% | 3 | same: "never three stacked", "silence rare", tuned two knobs |

Mean 31%, no insight. Neither player looked at the snare row against the kick's holes; both
inferred "rules" (cover every beat, at most two voices per beat) that the scorer does not
check at all — they are artefacts of solve()'s style — and their 27–36% is the rate at which a
groove-shaped sampler happens to fill exactly n holes. Both called N "a trap" / "undiscoverable".
The kid-proxy's imagined child said "never three X's stacked" and "one box is empty" — both
about columns, not about the snare filling gaps. The near-miss runs in every demo were invisible
because the hat row and the snare row together read as one texture.

Diagnosis: the counted relationship (snare run == kick hole, exactly) is not the loudest thing in
the picture; the three-voice groove is. Softening levers for v2, in order: (a) make the hat row
sparse and regular (e.g. every 4th step) so it stops competing with the snare for attention —
or drop it to two rows; (b) make the snare row otherwise EMPTY apart from its runs, so every
snare run is either a hole-fill, a too-short, a too-long or a wrong-place — the four cases the
designer already plants; (c) keep the sampler leak in mind: a groove-shaped random row 2 must
not score ~30% — the witness table should include "random snare row with kick-rest bias".
Status: testing (2 finals, 0 cracks). Refine before the next pair.

## norvel v2 (2026-09-04) — refiner: soften by salience, rule untouched

**Kept:** the rule, character for character — *exactly n of the maximal runs of "x" in the snare row
have the same span as a hole of the kick row*. **Changed:** only what the picture looks like and how
the clues are shaped. `norvel.v1.json` is the byte-identical previous version.

### What the v1 players actually did (`lad-norvel-v1-1`)

Both Opus players rebuilt the picture grammar perfectly and then hunted the wrong statistics.
norvel1a's final `strategy.py` is a sampler: *at a kick-rest step both non-kick voices play with
p = 0.78, at a kick-hit step one of them doubles with p = 0.20, never three at once*; norvel1b's is
the same idea with two knobs (`acc`, `p2`). Neither NOTES.md contains a single sentence comparing a
snare run with a kick gap. Their "confirmed rules" — *every step has at least one voice*, *never
three voices at once*, *no completely silent step* — are not in the scorer at all; they are
artefacts of v1's `solve()` sprinkling filler on the hat and on kick hits. norvel1b's imagined
12-year-old said "there's never more than two x's stacked" and "one box is empty": both about
**columns**, never about a row against the kick's gaps.

Measured on v1's own generator (600 fresh clues, sweeping the sampler): **a groove-shaped snare row
with kick-rest bias tops out at 28.1 %** (p = 0.85, no doubling), and 37.8 % if the density is tuned
per clue. That is exactly the 27 % / 36 % the two players scored. The class was paying almost its
full no-insight ceiling to a strategy that never looks at the rule.

### The three changes (DESIGN_LOOP lever 9 — redraw the demo, don't touch the rule)

1. **The hat row is gone; the picture is two rows.** The three voices read as one texture, and the
   counted relation was the quietest thing in it. A fixed regular tick cannot fix this: for an
   arbitrary kick row an every-2nd or every-4th-step hat lands *inside* counted holes, which is
   precisely the competition brief (c) forbids. The witness table cannot choose between the two
   options (the scorer reads rows 1–2 either way, so every ceiling is identical), so the tiebreak is
   salience and legibility — and "kick against snare" is also the most kid-legible drum picture
   there is (`boom … bap`). Cost: the free third row that used to kill "right rule, wrong row" is
   gone; that witness is now unreachable anyway (a three-row answer scores 0).
2. **The snare row carries nothing but its runs.** v1's `solve()` added 5–20 % random filler on
   kick hits. v2 emits the n exact fills, **at most three planted near-misses, and silence.** Every
   run in a demo is now one of the four cases the designer always intended: an exact fill; a run too
   short inside a gap; a run that covers a gap and spills over a kick hit; a run as long as a gap in
   the wrong place. Measured over 1200 demos: too-short **100 %**, spill **100 %**, a non-fill run
   exactly as long as some gap **100 %** (1.7 per demo), a run sitting on kick hits away from every
   gap 38 %, a gap left completely silent 55 %.
3. **Bigger, more dispersed clues:** G = 7–10 holes (was 4–8), n = 2–8 (was 2–5), G − n = 2–6 (was
   1–4), two hole widths per clue from a base of 2–4 (was 1–5, at most one 1-hole). This is the part
   that actually moves the sampler ceiling: with 7–10 holes and n/G spread over 0.25–0.8 there is no
   single rest-density that lands on *exactly n* for most clues. Weights were tuned so that no
   constant guess is worth much: max P(n = k) = 21 %, max P(G − n = k) = 24 %.

### Three demos as they now render

```
clue  xx..x..xx...x...x..x..xx...x/5
bd xx..x..xx...x...x..x..xx...x
sn ..xx.xxx...x.xxx.xx.xx..xxx.
      runs: 2-3 EXACT · 5-7 too long (covers the gap 5-6 and spills onto the kick at 7)
            11 too short · 13-15 EXACT · 17-18 EXACT · 20-21 EXACT · 24-26 EXACT   → 5 fills = n
```
```
clue  x..x..x...x..x..x...x..xx...xx..x..x/8
K |x..x|..x.|..x.|.x..|x...|x..x|x...|xx..|x..x|
S |.xx.|.x.x|xx.x|x.xx|.xxx|.xxx|.xxx|..xx|.xx.|
      the zipper: 8 of the 10 gaps filled exactly, one gap gets a single hit (too short),
      one run (21-23) covers a gap and spills over a kick hit                     → 8 fills = n
```
```
clue  x....x...x...x...x....x...x...x....x/2
|x...|.x..|.x..|.x..|.x..|..x.|..x.|..x.|...x|
|....|....|....|.xxx|x.xx|xx.x|xx.x|x...|....|
      sparse end of the range: 13-16 too long, 18-21 EXACT, 23-25 EXACT, 27-28 too short
                                                                                  → 2 fills = n
```

### Witness table — v1 → v2 (800 / 1200 fresh clues, same harness)

| strategy | v1 | v2 |
|---|---|---|
| the true rule (`solve`) | 100.00 % | **100.00 %** |
| empty / junk / clue echoed / 4000 chars / clue row copied | 0.00 % | 0.00 % |
| clue row + an empty or a full row | 0.00 % | 0.00 % |
| the v1 three-row format | (was the format) | 0.00 % |
| a random snare row, density 0.2 → 0.8 | 0.04–0.62 % | 0.03–0.69 % |
| **groove sampler, kick-rest bias (the v1 players' strategy)** | **28.08 %** | **13.9–17.3 %** |
| groove sampler, density tuned per clue so E[fills] = n | 37.83 % | 29.03 % |
| COMPLEMENT — fill every hole exactly | 0.00 % | 0.00 % |
| complement minus one hole | 34.62 % | **0.00 %** (G − n ≥ 2 now) |
| complement minus two / three holes | 27.62 % / — | 24.50 % / 16.92 % |
| "always fill exactly k holes", k = 2…6 | 29–30 % | 12.0–22.4 % |
| fill the n longest / n shortest holes | — | 100 % (= the rule; *which* holes never matters) |
| graft an old answer's snare row under the new kick row | 1.88 % | 3.33 % |
| demo replay on the next clue / one fixed answer | 0.00 / 0.12 % | 0.00 / 0.08 % |
| n holes get a random run INSIDE (the loose reading) | 7.50 % | 3.08 % |
| n holes: run flush to the hole's left edge | 8.58 % | 2.94 % |
| n holes get ONE hit / n holes covered with a spill | 0.00 % | 0.00 % |
| n unison hits / exactly n snare runs anywhere | 0.00 / 0.17 % | 0.00 / 0.00 % |
| right rule but n±1 holes, or rows swapped | 0.00 % | 0.00 % |

**Foothold (lever 7).** v1's foothold was the loose reading at 7.5 %; v2's is bigger and more
natural: *"the snare plays through the kick's gaps"* at any density pays **14–17 %** from the first
probe after the first demo, and "fill k of the gaps exactly" pays 12–24 %. Nobody will conclude the
grader is exact-match. Crucially it is a **plateau, not a ladder** — no amount of density tuning
gets past ~18 % without actually counting, whereas in v1 the same sweep walked smoothly to 30 %+
and felt like progress.

**Fairness.** 62 "count a relation in this picture" counters: mean survivors 2.7 → 1.3 → 1.0 after
1–3 demos, and the last survivor is the true rule in 15/15 trials (v1: 12.2 → 4.4 → 1.9 → … → 1.0
over 141 counters). Two demos now pin the rule for anyone who enumerates snare-run/kick-gap
relations at all; every remaining bit of difficulty is in *looking there*, which is exactly what the
redrawn picture is for.

**Validation.** `python tools/quickcheck.py challenges/lab/norvel.json --seeds 200` → **OK, no
warnings** (`gen=0.11 ms score=0.14 ms solve=48.6 ms`). Sizes: score **269/512**, solve 4448/5000,
generate 1180; clue ≤ 50 chars, solution ≤ ~120. solve() scores 1 on 1500/1500 fresh clues (5.0 ms
mean, 248 ms worst); generate deterministic over 4000 seeds, 0.030 ms mean / 0.14 ms worst; scorer
0 raises / 0 non-binary / 0 false positives on 8800 junk strings (worst 0.19 ms) and 0 disagreements
with an independent re-implementation on 12 000 mutated answers; leniency 100 % (bare rows, bar
lines, labels, `|1234|` header, blank lines, tabs, CRLF, stray spaces), strictness 0 % (rows
swapped, snare only, three rows, one wrong character in the kick row, snare shifted, snare emptied,
all on one line; snare reversed 2.2 % = palindromic coincidence).

### Predicted classification

**calibrated / on target, mean final 45–65 %.** The insight-free ceiling has dropped from 28 % to
~17 %, and the picture now states the relation instead of hiding it: one demo shows a snare row
whose runs visibly interlock with the kick's gaps, with one run that stops short and one that plays
over the kick. The likeliest split is one crack (rounds 2–4) and one player parked at 17–25 % on
"play through the gaps" or "fill all but two". Predicted kid score **4.5–4.8/5** (v1 scored 4.2):
two rows labelled kick and snare are a drum machine at a glance, the sentence "the snare fills five
of the kick's gaps exactly" is one a 12-year-old says out loud, and the counting is 5-of-8, not a
statistic.

**Risk is now too_easy, not too_hard.** If both players crack it, harden with: count only holes ≥ 3
steps wide; require the counted fills to be non-adjacent; or push G − n to 2–3 so the answer is
nearly the complement and all the information sits in the near-misses. If it comes back under 15 %,
guarantee two silent gaps per demo or add the number of holes as a second clue field.

Scratch harness for every number above (not committed):
`$SCRATCH/music2/v2/{generate,solve,score,attack,sampler,demostats,hyp,selftest,build}.py`.

## norvel v2 ladder run `lad-norvel-v2-1` (2026-09-04, old cadence 6×0.5 s / demo per window, 2 Opus players)

| team | profile | final | demos | reading |
|---|---|---|---|---|
| norvel1a | opus-lowdemo | 44% | 2 | "complement of the thump in n whole measures" for dense clues (72%), sparse-fill sampler otherwise |
| norvel1b | opus-theorist | 49% | 4 | per-(n, silent-box count) lookup table; "0 or 1 silent boxes is always wrong" |

Mean 46% — but still zero insight: neither player wrote one sentence about the snare filling a
kick hole *exactly*. The two-row redraw removed the hat texture but the sampler leak survived:
tuning "how many boxes are silent" per n (1b) or complementing whole measures (1a) reaches
45–50% because the exact-fill count is highly correlated with silence counts when the clue's
holes are mostly measure-aligned. Both again reported the kid reading they missed ("a drummer
has to breathe", "the second row looks sloppy on purpose"). 1b: "every reference answer had
exactly 2 boxes where both drums hit" — an artefact of the planted near-misses, which read as
a rule.

Under the new format (4 rounds, 3 demos across 7 classes) this class will be re-measured; the
number that matters is the split between players who spend a demo on it and those who don't.
If the sampler leak persists, the lever is to make holes NOT measure-aligned (bar lines are a
red herring — a hole that straddles a bar line cannot be "complemented per measure") and to
make n small relative to the hole count so silence-count tuning has no gradient.

## norvel v3 (2026-09-05) — refiner: demo-economy pass (clue = the grid; both sampler leaks shut)

Brief: the new format (7 classes per pool, 4 rounds of ~60 probes per class, **3 demo requests
per team**) means a player may never see a demo of this class at all, and v2's two players had
reached 44 % / 49 % without ever comparing a snare run with a kick gap. `norvel.v2.json` is the
byte-identical previous version. **The rule is untouched for the third time**: *exactly n of the
maximal runs of `x` in the snare row have the same span as a gap of the kick row.*

### 1. The clue is now the drum grid (put the object in the clue)

v2's clue was the bare string `x..x.x../5`. v3's clue is three lines:

```
kick  |xx..|.x..|.xx.|.x..|.x..|.xx.|.x..|.xx.|.xx.|.xxx|
snare |....|....|....|....|....|....|....|....|....|....|
n = 2
```

The kick row is drawn in bars of four with a label; the snare row is **there and empty**, same
bars, all rests; then the number. "Fill in the snare row" is legible without a demo, and the
answer is literally this picture with row 2 coloured in. The scorer is unchanged in spirit —
delete everything that is not `x` or `.`, drop the lines that become empty, require exactly two
rows of the clue's length with the first equal to the kick row — so labels, bar lines, a
`|1234|` header, an echoed `n = 2` line, blank lines, tabs and CRLF are still all free (leniency
100 % on nine renderings, strictness 0 % on ten mutations). `solve()` now renders demos in the
**clue's own format**, so one look says "the answer is the clue, with the snare filled in".

### 2. The two sampler leaks

v2's players did not tune a rule, they tuned a *shape*: "complement the thump in n whole
measures" (44 %) and a per-(n, silent-box-count) lookup table (49 %). Both work for the same
reason: any process that sprays snare hits into the kick's rests fills some number of gaps
exactly, and if that number can be tuned to sit near n it lands on n about 20 % of the time
(P(count = n) for a Poisson-ish count is 0.20–0.27 — the arithmetic floor of this *whole family*
of rules). Two changes, and they work together:

* **No gap fits inside a measure.** Every gap now straddles at least one bar line — the wide
  family straddles two — so complementing a measure never produces a run that ends where a gap
  ends unless *every* measure the gap touches is complemented. The literal v2 strategy
  ("complement n whole measures") now scores **0.00 %**, and a contiguous block scores 7 %.
* **n is small and anti-correlated with gap width.** Three clue families, ~1/3 of clues each:
  9–10 gaps of 2–3 steps with **n = 2**; 9–10 gaps of 4–5 with **n = 3**; 7–8 gaps of 6–7 with
  **n = 4**. The blind density that would fill "about n" gaps by luck is then *different in every
  family* (p ≈ 0.45 / 0.65 / 0.85), so a single global density — per step or per measure —
  can only ever be right for one family. This is the change that matters: with n spread 2–4 over
  a *fixed* gap width, the same sampler scores 22 %; with the widths coupled to n it scores 11 %.

Measured on 2000 fresh clues, sweeping the knob the player would sweep:

| blind strategy | v2 (measured on v2's generator) | **v3** |
|---|---|---|
| kick-rest-biased random snare, density 0.5 / 0.6 / 0.7 / 0.8 | 13.9–17.3 % | **9.4 / 9.0 / 9.4 / 11.0 %** |
| …best over the whole density sweep 0.30–0.95 | 17.3 % (p = 0.90) | **12.7 % (p = 0.90)** |
| complement of n whole measures (the v2 player's actual rule) | 44 % in play | **0.00 %** |
| complement of a random contiguous block of measures | — | **7.0 %** |
| complement each measure w.p. 0.3 / 0.5 / 0.7 | — | 5.5 / **15.3** / 14.5 % |
| …best over the whole per-measure sweep | — | **15.3 % (s = 0.50)** |
| density tuned per clue so E[exact fills] = n (needs the insight) | 29.0 % | 26.8 % |

15.3 % is the residual: a per-measure coin is just a coarse sampler, and no design of this rule
can push a *tuned* random filler below ~P(count = n). It is a **plateau, not a ladder** — the
whole s ∈ [0.45, 0.70] band pays 13–15 % and nothing pays more — which is exactly the foothold
lever 7 asks for: a demo-less player who sprays snare hits into the gaps scores 9–15 % and never
concludes the grader is exact-match.

### 3. The demo says the rule and nothing else

`solve()` now emits **the n exact fills, ONE run that stops short inside a gap, ONE run that
covers a gap and spills over a kick hit, and silence.** Nothing else — no filler, no
right-length-wrong-place decoy (v2 had up to three near-misses plus a decoy, which is why "every
reference answer had exactly 2 boxes where both drums hit" read as a rule to the v2 player).
Measured over 1500 demos: **0 violations**, always exactly n + 2 runs, on average 3.7 gaps left
completely silent. Three demos as they render (clue, then answer):

```
kick  |xx..|.x..|.xx.|.x..|.x..|.xx.|.x..|.xx.|.xx.|.xxx|      n = 2
snare |....|....|...x|x...|.xxx|x..x|x...|....|...x|....|
        11-12 EXACT · 17-20 spills over the kick hit at 21 · 23-24 EXACT · 35 stops short
```
```
kick  |x...|..x.|...x|....|.x..|...x|....|.x..|..x.|...x|....|.x..|..x.|...x|   n = 3
snare |....|...x|xxx.|....|..xx|xx..|xxxx|x.xx|xxx.|....|....|....|...x|xxx.|
        7-10 EXACT · 18-21 one step short · 24-28 EXACT · 30-34 spills · 51-54 EXACT
```
```
kick  |xx..|....|.x..|....|.x..|....|..x.|....|..x.|....|..x.|....|..x.|....|..xx|  n = 4
snare |....|....|..xx|xxxx|x.xx|xxxx|x..x|xxxx|xx.x|xxxx|xx.x|xxxx|xx.x|xxxx|xxx.|
        10-16 EXACT · 18-24 one short · 27-33, 35-41, 43-49 EXACT · 51-58 spills
```

Fairness (47 "count a relation between the snare and the kick" counters): survivors
**6.2 → 4.1 → 3.1** after 1–3 demos; the true rule always survives, and its companions are its
own cousins ("the number of snare runs minus two" — an artefact of always planting exactly two
near-misses — and "gaps of width ≥ 3 filled exactly"), which a handful of probes separate.

### Witness table (500 fresh clues; the two sampler rows on 2000)

| strategy | v3 |
|---|---|
| the true rule (`solve`) · fill the n widest gaps · n fills + an extra spilling run | **100.00 %** |
| **clue returned unchanged (snare row silent)** | **0.00 %** |
| empty · junk · unicode · 4000 chars · kick row alone · kick row twice · full snare row | 0.00 % |
| **snare = complement of the kick (fill every gap)** | **0.00 %** |
| **complement n whole measures** / a contiguous block | **0.00 %** / 7.00 % |
| **complement each measure w.p. 0.5** (sweep peak) | **15.30 %** |
| **kick-rest-biased random snare, density 0.5–0.8** | **9.0–11.0 %** (sweep peak 12.7 %) |
| sampler tuned per clue so E[exact fills] = n | 26.80 % |
| **fill n gaps but each run one step short** | **0.00 %** |
| **fill n gaps but each run spills one step** | **0.00 %** |
| **a run strictly inside n gaps (the loose reading)** | **0.00 %** |
| one snare hit in each of n gaps · n runs anywhere · n unison hits | 0.00 % |
| right rule but n−1 / n+1 gaps · rows swapped | 0.00 % |
| always fill exactly 2 / 3 / 4 gaps exactly, ignoring n | 32.2 / 34.0 / 33.8 % |
| fill all but 3 / 4 / 6 / 8 gaps exactly | 7.6 / 26.2 / 14.4 / 17.0 % |
| fill every gap of the wider / narrower width exactly | 0.00 % |
| **demo replay** / one fixed answer / graft an old snare row onto a new kick | **0.00 %** / 0.20 % / 2.80 % |

Gradient: 0 % (well-formed, no idea) → 9–15 % (something in the gaps, any density — the
foothold, and a plateau) → 27–34 % (the *exact* match found, the meaning of n missed) → 100 %.
No template exceeds 34 % except the ones that already contain the rule.

**What a demo-less player can read off the clue:** that the answer is this two-row drum grid with
the snare row filled in, that it must be the same length as the kick row, and that some count of
2–4 is involved — enough for well-formed attempts worth 9–15 % by spraying snare hits into the
gaps, and not enough for the word *exactly*, which is what the demo's two near-misses teach.

### Validation

`python tools/quickcheck.py challenges/lab/norvel.json --seeds 200` → **OK, no warnings**
(`gen=0.27 ms score=0.10 ms solve=0.17 ms`). Sizes: score **322/512**, solve 1489/5000, generate
1655/50000; clue ≤ 191 chars, solution ≤ 191. `generate` deterministic, **0.069 ms** mean over
3000 seeds (n = 2/3/4 at 29/33/39 %); `solve()` scores 1 on **3000/3000** fresh clues, 0.063 ms
mean. Scorer: 0 raises, 0 non-binary, 0 false positives on 12 000 junk strings (worst 0.03 ms);
**0 disagreements** with an independent re-implementation on 12 000 mutated answers. Leniency
100 % (bare rows, bars, other labels, beat header, blank lines, CRLF, tabs, stray spaces, an
echoed `n =` line, prose wrapped around the picture); strictness 0 % (rows swapped, one row,
three rows, snare shifted / emptied / lengthened, all on one line, one wrong character in the
kick row). Snare reversed scores 7 % — palindrome coincidences in the wide family, not a
strategy.

### Predicted classification

**testing → calibrated, mean final 40–60 %; the risk is now `too_easy`, not `too_hard`.** The
clue prints `n = 3` right under a picture of gaps, so "fill n of the gaps" is a guessable blind
hypothesis; what still needs the demo is *exactly* — the four plausible implementations ("a run
inside the gap", "one hit per gap", "cover the gap", "fill it edge to edge") all score 0 except
the last. Expect the player who spends a demo to crack it in round 2–3 and the player who does
not to sit at 9–15 %. Hardening levers if both crack it: count only gaps ≥ 4 steps wide; require
the n fills to be non-adjacent; stop printing n and make it the number of gaps of the wider kind.
Softening levers if it comes back under 15 % with a demo: guarantee two silent gaps in every
demo, put a second worked example in the demo, or shrink the wide family so every clue fits in
11 bars.

Scratch harness for every number above (not committed):
`$SCRATCH/music3/{gen,v3,sweep,sweep2,sweep3,sweep4,try,try2,try3,attack3,selftest,hyp,build_json}.py`.
