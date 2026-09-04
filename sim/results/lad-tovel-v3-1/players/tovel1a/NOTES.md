# NOTES — challenge "tovel" (the only class in this pool)

## Clue format (confirmed)
`{days_in_month}/{start_weekday}/{LETTER}/{k}/{query_day}`

- `days_in_month`: 28, 29, 30 or 31.
- `start_weekday`: 0-6, weekday of day 1 of the month, Monday=0 .. Sunday=6.
  Confirmed by reconstructing the printed grid's column alignment in every
  demo (day 1 always lands under the column this field names).
- `LETTER`: a single uppercase letter A-Z.
- `k`: small int, 2-6 in our samples. Best guess: palette size for this
  month's letters is `k+2` (fits demo3 k=2→4 letters seen, demo4/5 k=3→5
  letters seen exactly twice in a row; demo1/2 k=4→ predicts 6 but only 4
  distinct letters were seen in ~30 draws, plausibly because 2 of 6 rare
  palette letters just never got drawn). Not confirmed with confidence, and
  never turned out to matter for scoring since we never solved the letter
  rule for individual days.
- `query_day`: a specific day-of-month.

## What we're confident about
`LETTER` is the correct letter for `query_day`, i.e. clue.LETTER ==
grid[query_day]. This held in **5 out of 5** demos (days 11/13/21/18/18
across 5 different months/start-weekdays/k values), which given a
4-5-letter palette is far too consistent to be chance (~1/500-1/3000 if
random).

## What sank us
The server's reference "solution" is the **entire multi-line calendar
grid** (header + all day/letter cells, exact whitespace), not a short
answer. We tested, across two full training rounds (~950 real, non-demo
"tovel" challenges) with format cycling by `memory['_index']`:
  - bare `LETTER` (upper and lower case)
  - `f"{query_day}{LETTER}"`, `f"{LETTER}{query_day}"`, padded variants
  - the clue echoed back verbatim
  - `f"{query_day}: {LETTER}"` and a JSON `{"day":.., "letter":..}` blob
  - bare `query_day`, bare `k`, sum of all 4 numeric fields
  - the weekday index / weekday name (Mon/Tue/...) of `query_day`
All of these scored **0/0** — not even a single hit across ~1935 answered
challenges plus skips. Content (the letter) is right; format is wrong.
Conclusion: exact string match against the full grid is required.

## Why we couldn't build the full grid
Per-day letter assignment does **not** fit any of:
  - `n mod k` for k=2..9 (checked per grid, exact match required)
  - linear/modular combos `(a*n + b*row + c*col + d) mod m` for
    a,b,c ∈ [-3,3], d ∈ [0,m), m ∈ [2,7] — brute forced against 3 full
    demo grids, zero fits
  - divisor count, prime/composite, digit sum, Roman-numeral length,
    Collatz length, popcount, palindrome — none separate the letters
    cleanly
  - a fixed 5x7 "shape" mask (row,col) independent of the specific clue —
    compared demo2 vs demo4 masks, they're different shapes

Distribution: the clue's LETTER is always the **most frequent** letter in
the grid (roughly 33-54% of days across our 4 full-grid demos), with the
remaining days scattered across 3-4 other letters with no discernible
period or simple filter. This looks like a **weighted random draw per
day** (heavily favoring the seed letter) rather than a closed-form rule —
i.e. probably reproducible only with the server's own RNG/seed, which we
don't have access to and are not allowed to look for.

Also: the header itself alternates between a single-letter style
("M T W T F S S") and a two-letter style ("Mo Tu We Th Fr Sa Su") between
demos with no field we could find that predicts which one a given clue
will use — so even a correct letter-grid would need a lucky/complete guess
of header style too.

## Decision
Given 5 demos + 4 experimental rounds (~1935 answered + thousands of
skips) produced zero hits and no tractable formula, we stopped chasing the
cipher, used the last 2 training rounds as pure skips (protects the
fewer-answers tiebreak, costs nothing since we can't score), and ran the
final skipping every "tovel" challenge. Final score: 0/0 (rank 1 on
tiebreak vs. sibling team tovel1b, who also scored 0 but answered 2935).
