# kelmar1a — Centaur Zendo notebook

Pool: LegoZendo2, basten, kelmar, murn, orlan, tovel, velk.  Rounds 0.5 s, 5 s cooldown.

## Round log
| round | strategy | presented | answered | correct |
|---|---|---|---|---|
| 1 | skip-everything harvest | 591 | 0 | 0 |
| 2 | gen-1 probes, 16 variants/class | 393 | 365 | 3 (LegoZendo2, all N=0) |
| 3 | gen-2 probes, 20 variants/class | 423 | 383 | 0 |
| 4 | gen-3 probes + confirmed N=0 wall | 402 | 346 | 5 (LegoZendo2 N=0) |
| final | LegoZendo2 N=0 only + N>0 hedge | 3562 | 214 | 45 |

## Demos spent (3)
1. **LegoZendo2** — clue `PM10`, answer = 18x48 ASCII Lego wall of 2x3/3x2 bricks
   (letters = colours, `:` = empty).  Chosen because `XX<n>` gave no shape at all.
2. **tovel** — clue `30/5/S/2/24`, answer = month calendar, `days/firstWeekday(Mon=0)/
   letter/a/b`, cells `%2d%s` joined by a space under header ` Mo  Tu  We  Th  Fr  Sa  Su`.
3. **orlan** — clue = grid of `.#xo`, answer = `1,1>1,5`, i.e. a **move**, `r,c>r,c`.
No demo on basten, kelmar, murn, velk: each has a probe-able answer shape (a number,
an index pair, a transformed string) so probing looked cheaper than an example.

## Per class
* **LegoZendo2** — CRACKED (partly).  Any fully solid rectangle of one letter scores 1
  **iff the clue number is 0** (8/8 in training, 45/45 in the final).  N counts something
  about the wall we never found: disproved = empty cells, enclosed holes, connected
  pieces, floating pieces, brick count, bricks of colour a/b, a-on-b stacks, colours,
  wall height/width, N*3 rows, N*2 cols.  Demo (N=10) has 72 bricks, 7 colours, exactly
  half the cells filled, 11 filled components, 14 empty regions, 10 distinct column heights.
* **tovel** — frame SOLVED (byte-identical to the demo apart from the letters), rule on the
  letters unsolved.  ~40 letter schemes tried (all L / blank / L on day b / L on a days /
  L down day-b's weekday column / L every a days / cycling / with and without trailing
  spaces).  Demo letters S,I,B,P look random; S=11 B=8 P=6 I=5 days; a=2 equals the number
  of S in day-24's Monday column, which was the best but unconfirmed lead.
* **orlan** — shape known (`r,c>r,c`, 1-indexed: the demo answer is exactly
  "first `.` in reading order" > "first `x` in reading order").  40 move hypotheses
  (o->x rook slides, adjacent moves, longest empty run, corner->x, both index bases,
  row/col order swapped) all scored 0.
* **velk** `LETTERS|n` — letters always distinct, len 4-6, n 2-5 and n may exceed len.
  36 hypotheses failed: Caesar +/-n, sort, reverse, rotate, rail fence (encode/decode),
  columnar transposition, Josephus, n-th letter present/absent, inversions, take/drop n.
* **kelmar** `track/*aYb` — track has 5-7 `*` and 4-5 `Y`, spec always asks for fewer, so
  both "a-th star / b-th Y" and "shortest window" readings are well-defined.  36 answers
  (window substring, window bounds, gap length, index pairs 0/1-indexed, `i>j`) all 0.
* **murn** `cells|n` — `.o#`, len 9-16, n 3-23 with no linear relation to the cell counts
  (exhaustive integer-coefficient search).  36 hypotheses failed (rotation of the necklace,
  Josephus, marbles sliding/gravity, counts, indexes).
* **basten** `track/n` — track 28-36 long, 4-6 digits from {1,2,3} with gaps 4-11, n 2-8 and
  independent of everything measurable.  36 hypotheses failed (sums, walks with stride n,
  digit-chain walks, positions, marked tracks).

## Endgame reasoning
A skip costs ~0.85 ms, an answer ~1.25 ms, so answering everything would have cut the final
from ~3500 challenges to ~2400 and cost ~13 of the guaranteed LegoZendo2 points.  With no
hypothesis above a few percent, the lean strategy (answer only what is proven, plus a
1-in-3 hedge on LegoZendo2 N>0) maximised both score and the fewer-answers tiebreak.
