# kelmar1b — notes

Pool: LegoZendo2, basten, kelmar, murn, orlan, tovel, velk. 4 training rounds, 3 demos.

## Rounds
| round | presented | answered | correct | what it was for |
|---|---|---|---|---|
| 1 | 450 | 450 | 0 | harvest all 7 clue formats (cheap cycling answers) |
| 2 | 437 | 437 | 4 | 20 hypotheses per class, one per item, logged by id |
| 3 | 444 | 444 | 4 | picture-format hypotheses + lego/tovel solvers |
| 4 | 422 | 422 | 3 | staggered lego walls, tovel rota rules, sims |
| final | 3622 | 403 | **46** | adaptive client (bandit over 119 hypotheses) |

## Method
Every training round ran a *hypothesis-cycling* strategy: for each class a list of
candidate answer functions, one per presented item, with `(index, class, hypothesis)`
logged to memory so the round log could be joined back and each hypothesis scored
separately. A right hypothesis is deterministic, so a single hit identifies it.

For the final I wrote my own client (`zclient.py`, protocol is public in the guide)
that reads the per-item `result` message and runs a bandit: try each hypothesis up
to 3 times, lock onto anything that scores, skip a class once every hypothesis is
dead. Skips are instant, so writing off five classes raised the number of items
presented from ~450/0.5s to 3622/3s.

## Per class
* **LegoZendo2** `GB6` -> picture of a Lego wall of 2x3 bricks drawn with colour
  letters. Demo taken. Every n=0 clue is satisfied by *any* structurally valid wall
  (single brick works); no design ever scored for n>0. Evidence: two same-colour
  bricks side by side (a 3x4 or 3x12 one-colour region) scores 0 even at n=0, while
  a single brick, two different-colour bricks, and 6 alternating bricks all score 1
  — so multi-brick regions of one colour break the checker's brick parse, and my
  earlier stacked/staggered walls were invalid rather than mis-counted. Fourteen
  clean designs for n (a-on-b contacts, brick count, colours used, lying bricks,
  tower height, floating bricks, same-colour pairs...) were all refuted in the final.
* **tovel** `29/2/A/5/13` -> a month rota calendar: `a` days, first day in column
  `b` (0=Mo), header ` Mo  Tu ...`, cells `%2d%s`, rows rstripped. Format nailed
  from two demos; the rule linking C/d/e never was. Both demos have person C
  working on day `e` (13) and holding the plurality of shifts, max run 4 <= d.
  Sixteen assignment rules refuted.
* **velk** `FRSZKX|5` — letters + k. Refuted: Caesar +-k, sorting, rotations, k-th
  letter/permutation, NATO, Morse, phone keypad, bubble-sort passes/traces, grids.
* **murn** `.#..##o#o|4` — track + n. Refuted: marbles moving/bouncing/spreading n
  steps, traces, gravity, counts, RLE, wrapping.
* **kelmar** `___Y__*__/*3Y1` — marks with weights. Refuted: weighted sums, bar
  pictures, stretches, queue/race simulations, gap lists.
* **basten** `...3...2..../4` — marks with heights + n. Refuted: skylines, sums,
  bin/bus packing, jump simulations, gap lists.
* **orlan** 5-6 row grid of `. # o x`. Refuted: all 8 rotations/reflections,
  gravity, Voronoi/territory fill, minesweeper counts, BFS paths and path length.

## Demos
1. **LegoZendo2** — clue `GB6` gave the least away of all seven (two letters and a
   number); spent before round 2. Paid: told me the answer is a picture.
2. **tovel** — most frequent class, clue looked like a date but the answer shape was
   unguessable; the demo gave the calendar layout exactly.
3. **tovel again** — one example could not separate "C works a-e days",
   "C works e days" and "day e"; the second example killed the first two.
Deliberately left without a demo: velk, murn, kelmar, basten, orlan — their clue
shape (string + number, grid) looked probeable. In hindsight that was the wrong
call: probing 30+ hypotheses each found nothing, and a demo would have given the
answer *format* for one of them.
