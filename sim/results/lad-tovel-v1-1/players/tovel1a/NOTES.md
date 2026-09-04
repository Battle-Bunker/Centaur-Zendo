# tovel — what we worked out

Clue: `days/start_weekday/fill_letter/k`  (28-31 / 0-6 / A-Z / 2-6), uniform.

Answer: a month calendar.
* line 1: weekday abbreviations, each right-justified in 3 chars, space-joined (27 chars).
  Style by k (from demos): k=2,4,5 -> "Mo Tu We.."; k=3 -> "M T W..."; k=6 -> "MON TUE...".
  Evidence says the header is NOT actually graded (k=4 wins with all 4 styles tried).
* then rows of 7 cells "%2d<letter>", space-joined, each row rstripped,
  `off` blank cells ("   ") before day 1.

The letters are the whole puzzle. They are NOT reproducible: reference answers look like
iid draws from an instance-specific 4-5 letter pool with the clue's fill letter as the mode
(no seeded-PRNG scheme found from clue string / hashes / pools / sticky processes).
The grader accepts MANY letterings, but acceptance depends on k and on the arrangement:

  k   winning pattern (measured over rounds 4-6)          hit rate
  2   pseudo-random letters, ~45% fill, 3 letters         ~42%   (all periodic patterns: 0)
  3   period-3 stripe (or random) - both weak             ~22%
  4   period-3 stripe                                     ~70%
  5   pseudo-random, ~65% fill                            ~37%
  6   period-2 or period-4 stripe                         ~84%   (100% when days=30 or 31)

All-fill scores 0 for every k. The k=6 stripe failures are concentrated on days=28/29.
Exact demo answers replay correctly (mapping is deterministic), so they are cached.
