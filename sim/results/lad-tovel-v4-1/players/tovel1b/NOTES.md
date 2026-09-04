# tovel — notes (team tovel1b)

Only one challenge class in the pool: `tovel`.

## Clue format (confirmed on 2418 clues)
`<days>/<first weekday>/<letter X>/<a>/<b>`
* days ∈ {28,29,30,31}; first weekday 0=Mon..6=Sun (column of day 1)
* X = any A–Z; a ∈ 1..5; b ∈ 2..days-2
* **b is always a Monday, Tuesday or Wednesday** (never Thu–Sun)
* min(days − b) rises with a: 2, 4, 9, 11, 16 for a = 1..5

## Answer format (exact, from demo 1)
Header `" Mo  Tu  We  Th  Fr  Sa  Su"`, then week rows. Each cell is 3 chars
`"%2d%s"` (day number + one letter), cells joined by a single space, leading
blank cells before day 1, every row right-stripped, no trailing newline.

## The rule (confirmed 100% on the final for the cases it covers)
Mark day **b** with X, then every other day: b, b+2, b+4, … — **a+1 marks in
all** — with a non-X day in each gap, and this must be the **unique longest**
such every-other-day run of X in the month. Everything else is free.
* a=1, any column → 894/894 correct in the final.
* a=2 with b on a **Monday** (marks Mon/Wed/Fri) → 296/296 correct.
* a=2 with b on Tue (Tue/Thu/**Sat**) or Wed (Wed/Fri/**Sun**) → 0.
  ⇒ the run must avoid the weekend; from Tue/Wed it evidently jumps into the
  next week instead (min-b data points at b+8 / b+7, i.e. the next Wednesday).
* a≥3 → not cracked. Every offset family tried scored ~0.

## Round log
| round | answered | correct | what I ran |
|---|---|---|---|
| 1 | 658 | 0 | calendar filled entirely with the clue letter (clue harvest) |
| 2 | 538 | 0 | 12 structural variants (counts/placements of X) |
| 3 | 440 | 3 | 20 variants incl. weighted-random 4-letter calendars |
| 4 | 0 | 0 | **wasted** — `random.Random((clue,i))` raised TypeError → all skipped |
| 5 | 438 | 54 | forced X at b and b+2, non-X at b+1; 8 groups testing extras |
| 6 | 492 | 69 | offset families for a≥3 |
| final | 4124 | **1190** | rule above, hedged candidates for a≥3 |
