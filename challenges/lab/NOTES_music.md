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
  The picture is 3–4 lines and under 30 characters wide.
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

Clue `K/n`: `K` is a 16- or 20-character kick row over `x`/`.` that starts and ends with
`x` and has G = 4–6 maximal holes (each 1–5 beats, at least one ≥3, at least two distinct
lengths); `n` is 2..G−1 and is never any number readable off the clue (G, G+1, hits,
longest/shortest hole, distinct hole lengths, bars, holes ≥3, holes of length 1).

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
