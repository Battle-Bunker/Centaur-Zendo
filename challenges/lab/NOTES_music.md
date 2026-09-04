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
