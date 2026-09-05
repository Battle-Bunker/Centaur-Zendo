# ospren1b — notes

## Shape of the pool
Seven classes; six share one shape and one is a picture class.

**Six "pick the candidate" classes** (borsel, dornic, ospren, tavrik, tresk, wisbek):
a clue is 2-4 positive examples, a blank line, then 4 candidates.  Exactly one
candidate obeys the hidden rule.  **Every clue has its own rule** — the class only
fixes the *universe* (dice / cards / 5x5 grids / words / bead strings / clock times).
Both answer formats score: the candidate's own text, or its 1-based index.
(ospren numbers its candidates because they are multi-line grids.)

**fennick** is a picture class: a bar chart drawn in ASCII, plus "N fall".

## fennick — solved exactly (demo 1)
Kid's-eye view of the demo: "it's a row of towers made of letters with lids on
top", "some towers moved one step sideways", "their lids turned into slashes".
Three things the kid noticed first, all of them right:
1. only *some* towers moved, and only by one step;
2. every tower that moved landed in an empty slot;
3. the moved ones were the *short* towers, not the tall ones.
Rule (0 mismatches on 35 clues, exact string match on the demo):
* height of a bar = characters above the ground line (letters + its `_` lid);
* for every **single-column gap** with a bar on both sides, the **shorter**
  neighbour topples into it.  Equal heights: nobody moves.  Two-column gaps: nobody.
* a **lone** bar (no bar beside it) never topples, even if it is the shorter one;
* a toppling bar keeps its letters, shifts one column, and its `_` lid becomes
  `/` (moved right) or `\` (moved left).  Ground row, rule line and `N fall` unchanged.
* "N fall" in the clue is exactly the number of bars that topple — a free checksum.

## The engine for the other six
For each clue: compute ~60-100 features of every positive and candidate; keep every
feature *value* shared by all positives; that is a candidate rule.  Weight it
`freq^-2.5 / (#candidates satisfying)^6` where `freq` is how common the value is in
the corpus of everything seen (rare rule + one satisfier = strong).  Sum the votes,
answer the winner.  Rules satisfied by 0 or all 4 candidates are ignored.

## Demo budget
1. **fennick** — the only class whose *format* was unreadable.  Paid for itself: 100%.
2. **dornic**, 3. **borsel** — the two weakest classes.  Cheap in value (one gold
   example each) but dornic's demo exposed the missing feature family:
   comparisons that survive different hand sizes ("more odd ranks than even").
   Deliberately no demo for wisbek/tavrik/tresk/ospren: their format was obvious
   and a demo would only have bought one more labelled example.

## Round plan
1. skip everything (harvest all 7 clue formats, free)
2. random candidate, alternating text/index (probe the answer format, harvest
   ~37 gold labels for free — 25% of random picks are right)
3. full engine
4. tuned engine
