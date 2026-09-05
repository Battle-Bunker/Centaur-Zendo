# NOTES — tovel1b

## House convention (learned from demo #1, norvel)
* Answer = the ENTIRE clue, picture edited, **trailing "N word" line kept verbatim**.
* The number N in the trailing line is a **count of events**, not a parameter.
  -> I can verify any hypothesised rule offline by checking count == N on all 45+ logged clues.
* Edits are drawn in-place with a marker char (norvel uses `-` for the vacated/passed cells).

## For the 12-year-old
Demo picture: three rows of drum boxes — "hat", "snare", "kick" — each row chopped into
little boxes of four beats with `|` walls. In the answer only the snare row changed, and the
change was two `x` sliding to the right leaving little dashes behind, like a snail trail.
Three things a kid notices first: (1) only the MIDDLE row changed; (2) the x's slid RIGHT,
never left; (3) the dashes show where it came from. All three turned out to be exactly right.

## norvel — SOLVED (demo #1)
Rule: a snare `x` standing on a step where BOTH hat and kick are silent is "slipping".
It slides right to the next step where hat or kick sounds; cells from its old position up to
(not including) the landing cell become `-`, landing cell becomes `x`. N = number of slippers.
Verified on the demo (2 slips, all 8 bars consistent). Confidence: high.

## The single most useful discovery
The trailing "N word" line is a COUNT of events in the picture, not a parameter.
Two consequences:
1. When N == 0 the picture is unchanged, so **echoing the clue verbatim scores 1**
   for EVERY class.  Confirmed 100% on all seven classes over rounds 2-4.
2. N is a free checksum: any hypothesised rule can be validated offline against
   every logged clue by checking count == N.  That is how norvel was nailed.

## norvel — SOLVED, 100% (93/93 in rounds 3+4)
A snare `x` on a step where BOTH hat and kick are silent slips right to the next
step where the **hat** sounds (not hat-or-kick -- that variant scored 59%);
cells from its old position up to but excluding the landing cell become `-`.
Slips cross bar lines freely.  N = number of slippers.

## kelmar — rule half-solved, answered only when certain
Ground line: `*` = flower, `Y` = sapling, `_` = bare.  A flower standing
IMMEDIATELY beside a tree of the picture's MAXIMUM trunk height leans toward it:
tree on the left -> `\`, tree on the right -> `/`.  Exception-free over 404
labelled flowers.  BUT that count only equals N in ~45% of clues; the other
clues have extra leaners I could not identify (never fewer -- the rule never
over-counts).  Measured: base==N -> 72/72 correct, base!=N -> 0/88.  So the
solver answers only when base==N and skips otherwise (free precision).

## basten / molvic / tovel / durnel / garrow — NOT cracked
Only the N==0 clues are answered (identity).  Searched hundreds of candidate
count-rules against the logged clues for each; nothing matched.
* basten  fish `><>`/`<><` and seaweed `|`; best pair-adjacency rule 23/49.
* molvic  shop shelves with misplaced stock; best 12/43.
* tovel   calendar of lettered days; best 18/47.
* garrow  pizza, header "<topping letter> N slices"; best 24/33.
* durnel  vehicles/buildings on a road; not attempted analytically.

## Demos spent
1. norvel  -- simplest, most structured picture; bought the house convention
   (answer = whole clue edited, caption kept) AND a full class.  Best demo.
2. kelmar  -- most frequent class (55/323) and the picture I understood least.
   Bought the rendering and most of the rule.
3. tovel   -- unlucky: the server returned a "0 bump" clue, whose answer is the
   identity I already knew.  Zero information.  A demo can be wasted this way.
