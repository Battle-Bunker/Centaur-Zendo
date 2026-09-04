# NOTES — team sarn1b — pool = ONE class, `sarn`

## The class
Clue: `<letter><3..6 digits>`, digits 1-9 (distribution peaks at 3, mean 4.0).
Answer: **one word per digit, every word starting with the clue letter**, in
digit order. Each digit is a **fixed per-word property p(word)** — verified: 59
labelled words, zero conflicts across many different clues.

What p is NOT (all ruled out against 59 labels): word length, distinct letters,
vowels, consonants, syllables, Scrabble score, alphabet sums, letters before /
after the clue letter, count of the clue letter, gap between repeats,
frequency/rank, any linear combination of ~60 such features, any additive
per-letter weighting (exact rational solve -> contradictory), any binary
op over feature pairs. Killer evidence: `prudent`/`proving`/`picture` are all
7 letters, 7 distinct, p-initial, yet p = 6 / 7 / 4. `like`=3 `life`=3 `live`=5
`lick`=4 `last`=1 — four-letter `li_e` words with four different values.
Best single predictor found: len - count(first letter), 44% per word.

## What worked instead
Learn the mapping by example. Harvest (word -> digit) from every answer the
server ever scored 1 (rounds + demos), build a `(letter,digit) -> [words]`
table, answer only clues the table covers **completely**, skip everything else.
Training check: fully-covered clues 30/30 correct; one-word-short clues 0/59.

## Round log
| round | strategy | presented | correct |
|---|---|---|---|
| 1 | random-ish + shape probes | 482 | 1 |
| 2 | 12 rival digit-rules | 497 | 1 |
| 3 | 12 more rival digit-rules | 539 | 2 |
| 4 | A/B/C digit->word-length tables | 465 | 3 |
| 5 | A/B universal vs per-letter offset | 485 | 4 |
| 6 | learned lookup table + fallback | 444 | 30 |
| final | table only, skip the rest | 4543 | **275** (275 answered, 0 wrong) |
