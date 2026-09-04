# tovel — notes

## Clue format
`days / first_weekday(0=Mon) / LETTER L / k / m`   e.g. `31/1/G/4/15`
Invariants over 2880 observed clues: days in 28..31; first_weekday 0..6;
L uniform A-Z; k in 1..5; **m+2k <= days always**; **weekday of day m is
always Mon, Tue or Wed**.

## Answer format (from demo 1, byte-exact)
```
 Mo  Tu  We  Th  Fr  Sa  Su
     1I  2G  3G  4G  5Y  6Q
 7Q  8Q  9P 10P 11Y 12Y 13G
...
```
header + one row per week; cell = `"%2d%s" % (day, letter)`; cells joined by a
single space; `first_weekday` blank `"   "` cells first; each row rstripped;
no trailing newline.  Renderer reproduced both demos exactly.

## The rule (confidence: high for k<=2, unsolved for k>=3)
Letter **L must sit on day m and then every other day, k+1 times**
(days m, m+2, ..., m+2k).  Everything else about the letters is free —
any filler letter works, L may appear elsewhere, the number of distinct
letters is unconstrained.
* k=1: confirmed, 100% over ~300 attempts, every weekday of m.
* k=2: confirmed **only when day m is a Monday** (100%); with m on Tue/Wed
  every construction tried scored 0 (0/45).
* k>=3: never scored (0 / ~600 attempts) with any of ~25 constructions,
  including the plain chain, weekend-skipping chains, maximal chains,
  chains embedded in rich random calendars, and the demo-like profiles.

## Killed hypotheses
* m = count of L (demo has 13 G's with m=15) — dead.
* k+1 = number of distinct letters (a scoring answer used 3 letters at k=1).
* L must be the most frequent letter (winning answers use L twice).
* seeded-PRNG / exact-match reconstruction (predicate checker, many answers pass).
* chain of length k (0/38), chain running left from m (0/37), endpoints only
  at k=2 (0/7): the full forward chain is required.

## Open question
What extra condition k>=3 (and k=2 off a Monday) needs.  It is present in
both demo calendars, absent from every minimal construction.
