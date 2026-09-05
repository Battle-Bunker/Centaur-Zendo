# tovel2a — careful-experimentalist log (1 demo allowed)

## Method
R1 skip-only harvest (567 clues, 0 answers) -> read every class's clue format.
R2/R3/R4 = mass hypothesis sweeps: each challenge in the round tested a different
candidate answer-generator (cycled per class), so ~20-30 rules were tested per
class per round and the round log said which rule scored.  All renderers were
first proved byte-exact by reconstructing the clue from my parse.

## Per class
- **garrow** `a3` + fish tank.  DEMO SPENT HERE (most opaque header, no idea what an
  answer even looked like).  Demo revealed: answer = the picture with vertical `|`
  cuts inserted.  Rule refined empirically: cut positions live in "columns that
  contain the header letter" space.  >=13 such columns -> cut after every 4th
  (8/8 in training); ==10 -> every 3rd; else -> after the 1st column of each
  3-char token of the header letter (~26%).  Final 36.6%.
- **fennick** bar chart of letter columns, caption "N fall".  Proved N=0 -> identity
  (many hits).  N is a free parameter in {4,5,6,7}; identity is NOT right when
  N>max height, so it is not "bars of height N fall".  ~30 fall/land/topple rules
  all scored 0.  Strategy: answer identity iff N=0, else skip.  Final 10.8%.
- **basten** seaweed `|` heights 1-3 (max always exactly 3), caption 3/4/5.  ~60 growth /
  add-object rules -> 0.
- **kelmar** ground `_` with `Y` and `*`, 2-3 empty sky rows, caption 1-3.  ~65 grow /
  lift / add rules -> 0.
- **norvel** kick/snare 16th-note grid, `n = 2..4`.  Found the kick pulses every 2n
  steps (n is the meter).  ~55 snare placements -> 0.
- **tovel** month calendar + `LETTER/a/b`.  b is always a Mon/Tue/Wed and a<=5, so
  days b..b+a-1 always lie inside one Mon-Sun row: almost certainly "mark a
  consecutive days from b with LETTER".  ~50 renderings of that mark -> 0, so the
  mark is drawn some way I never guessed.
- **virel** `[--][---][--][-]` + N, with N <= total dashes always (min slack 0), so N
  indexes the cells.  ~65 fill / add / repack rules -> 0.

## Final
3569 presented, 546 answered, 238 correct (43.6% precision on answers).
Skipping the five uncracked classes bought ~40% more challenges in the window.
