# tovel4a — Centaur Zendo notes (final score 783)

## Universal discovery (round 1, identity probe on every 3rd item)
Picture classes end with a text line `[letter] N verb`. **N = number of edits.**
Echoing the clue unchanged scores 1 whenever N==0. This alone gave the round-1 hits
and is the safety net for every picture class.

## Per class
- **garrow** `L N sprinkle` — grid of 3 rows split into boxes by `|`, `#` frame.
  Rule: every box containing **>=2** tokens `LL` has all its `:` replaced by `*`.
  N is exactly the number of such boxes (verified 39/39 then 100% in 3 rounds + final).
  Answer omits the trailing text line. DEMO TAKEN.
- **tovel** `N bump` — month calendar, letters on days. Runs of consecutive occupied
  days: in every run of length k>=3 the **middle** members (all but first and last)
  are bumped; each becomes `>` and its letter moves to the next free day.
  N == sum over runs of max(0,k-2) (verified 41/41, then 100%). DEMO TAKEN.
- **molvic** `N home` — 4 shelves labelled by item. Types that are misplaced *and*
  whose home row has a `___` move home; destination = **first** empty of the home row;
  source = the rightmost misplaced instance (tie -> lowest row). Reproduces the demo
  exactly but only ~35% live: the true instance-choice rule (and the exact count) is
  still unknown; skip when my move count != N. DEMO TAKEN.
- **felsim** `N tip` — isometric stack of `\__/` cups. NO DEMO SPENT (least frequent
  class). Never cracked: N matches no support/overhang/gap/isolation count I tried.
  Strategy: answer only the N==0 cases, skip the rest (keeps precision, costs nothing).
- **borsel / kaldrin / mestrel** — rule-family classes: 2-3 positive examples, blank
  line, 4-5 candidates, exactly one fits a hidden rule that changes per clue.
  Solver: ~90 features per class; any feature with a common value across all examples
  that matches exactly one candidate votes for it; weights learned from round 2-4
  score feedback (features that ever uniquely picked a known-wrong candidate are
  zeroed). Both answer formats are accepted (verbatim line and 1-based index).
  Round 2 cycled candidates to harvest labels: ~20% (random). Rounds 3/4 + final: 39-63%.

## Demos
molvic, tovel, garrow — chosen because their clue told me the answer *shape* but
nothing about the *edit*, and they are three of the four most frequent classes.
felsim deliberately left without one (rarest class, and its N==0 cases are free).
