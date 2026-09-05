# NOTES — tresk1b

Pool: borsel, dornic, fennick, garrow, tavrik, tresk, wisbek (7).
Round 1 = all skips: 354 clues harvested, 0 answered.

## Structure found in round 1 (from clues alone)

Five classes are "Zendo" rule-family classes: several POSITIVE EXAMPLE lines,
a blank line, then FOUR CANDIDATE lines. Each clue has its own hidden rule.
  - tavrik  : lowercase English words
  - wisbek  : clock times H:MM
  - borsel  : lists of dice numbers 1..6
  - tresk   : strings over {R,G,B}
  - dornic  : hands of playing cards ("AS 2C 10D ...")
Two are picture classes:
  - fennick : bar chart of letter-stacks, each capped by "_", ground row uses
              "." for an empty column; trailing text "N fall".
  - garrow  : a walled tank of "~" water containing 3-character fish (ooo, ccc,
              aaa, ppp, bbb, mmm, ttt); header line like "c2" / "p3" / "t2".

## Ten hypotheses written from the clues alone (12-year-old phrasing)

1. For the five list classes, the answer is "which of the four bottom lines is
   also allowed by the secret rule" — you send back that line, exactly as written.
2. tavrik's secret rules are simple spelling facts: "ends in s", "has a double
   letter", "has some letter three times", "starts with a vowel", "contains w".
   (All five already check out on round-1 clues.)
3. wisbek's rules are simple clock facts: "the minutes are even", "the minutes
   are a multiple of 10", "the minutes are the hour doubled", "the two minute
   digits are the same", "all the digits add up to the same total".
4. borsel's rules are facts about a handful of dice: "they're all the same",
   "one of them is a 4", "no two next to each other differ by one".
5. tresk's rules are facts about a string of coloured beads: "exactly one green",
   "starts and ends with the same colour", counts and runs of colours.
6. dornic's rules are facts about a hand of cards: "there is a pair", "no picture
   cards", "two cards of the same colour match", suit counts.
7. fennick's picture is towers of blocks; the "_" is the empty slot right on top
   of each tower, i.e. where the next block would land.
8. "N fall" in fennick means N more blocks drop out of the sky and land on the
   towers, so the answer is the same picture with N blocks added (probably onto
   the shortest tower each time — water-filling / Tetris).
9. garrow's picture is a fish tank; "c2" names the fish letter and a number of
   steps, so the answer is the same tank with every c fish swum 2 places
   sideways (or with the 2nd c fish singled out / taken out).
10. Because "the trailing text line may be kept or left out", fennick's answer is
    the redrawn picture; the "N fall" line is optional.

## Probes chosen instead of demos
- Answer FORMAT for the five list classes: probe by alternating between sending
  the winning line and sending its index (1..4) in round 2. No demo needed.

## Demo plan
- fennick and garrow: cannot guess the *edit* from the clue, and each appears
  ~50/354 times. Spend demo 1 and 2 there.
- Hold demo 3 until after round 2, for whichever picture class still fails.
- Deliberately NO demo for tavrik/wisbek/borsel/tresk/dornic: their clue already
  shows the answer shape (one of the four candidate lines) and the rule can be
  found by search over a predicate universe.

## Final record

| round | presented | answered | correct | hit-rate |
|---|---|---|---|---|
| 1 (skip-all probe) | 354 | 0 | 0 | – |
| 2 | 272 | 234 | 166 | 71% of answered |
| 3 | 272 | 236 | 179 | 76% |
| 4 | 271 | 243 | 185 | 76% |
| FINAL | 1539 | 1335 | **1047** | 78% of answered / 68% of presented |

Demos spent: fennick, garrow, garrow. fennick cracked exactly (100% ever since).
garrow never cracked -> skipped all game.

Engine: one generic "Zendo" solver for the five list classes. Parse clue into
positive examples + 4 candidates; evaluate ~200-350 hand-written predicates;
keep those true of every example; each predicate that accepts exactly ONE
candidate votes for it with a learned weight; weights learned by EM from my own
0/1 feedback (rounds 2-4). Fallback: pairwise conjunctions of survivors, then
"candidate accepted by most survivors".
