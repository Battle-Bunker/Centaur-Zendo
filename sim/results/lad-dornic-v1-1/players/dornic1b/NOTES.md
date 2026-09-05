# Centaur Zendo notes — team dornic1b

Pool: basten, borsel, dornic, kelmar, tavrik, tresk, wisbek

## Round 1 (skip-everything): 630 clues harvested, 0 answered.

## Shapes read off the clues alone
* basten - PICTURE. `~` water surface, `#` gravel, `|` seaweed, plus a number 3/4/5.
* kelmar - PICTURE. dot rows over a ground line `_` with `Y` and `*`, plus a number 1/2/3.
* borsel, dornic, tavrik, tresk, wisbek - RULE FAMILY: 2-3 example lines, answer = one more
  line of the same kind (dice rows / card hands / English words / B-G-R strings / clock times).

## Demos spent
1. basten  -> it is a FISH TANK. Answer = same picture with fish `><>` / `<><` added in the
   water, never overwriting `|`, `~`, `#`. Number line dropped. Demo N=3 but SIX fish drawn.
2. kelmar  -> answer = the dot rows replaced by blocks of `|` (identical on every row), ground
   line kept, number line dropped. Two demos, three blocks each; the block geometry is
   still unexplained.
3. (held back)

## Key idea for the rule-family classes
Every clue hides a different rule. Rather than *identify* the rule, compute the set of all
candidate predicates consistent with every clue line, then emit a NEW instance that satisfies
ALL of them. Whatever the true rule is, if it is in the pool the answer satisfies it.

## Result
FINAL: 968 correct / 1491 answered / 1720 presented (56.3%). Leaderboard rank 1.
tresk 97% · wisbek 95% · dornic 77% · tavrik 66% · borsel 58% · basten 1.5% · kelmar skipped.

## The three "novelty" constraints that were worth more than any rule
An answer that satisfies the hidden rule is still scored 0 unless it is a genuinely NEW
instance, and each class defines "new" differently:
  dornic - all lines of a clue are dealt from ONE deck (0 repeated cards in 104 clues);
           the answer must use cards not in the clue.        0/10 -> 27/33
  tresk  - the answer's length must differ from every clue line's length.   1/12 -> 10/12
  borsel - the answer's multiset must differ from every clue row's.         0/10 -> 25/40
  wisbek - the answer's HOUR must not appear in the clue.                   0/4  -> 40/41
  tavrik - the answer must be >= 2 edits from every clue word.              0/4  -> 29/38
