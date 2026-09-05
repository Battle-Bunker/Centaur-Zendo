# NOTES — tovel4b

Playing with a curious 12-year-old. Every demo gets narrated in plain words first.

## Round 1 (harvest): 232 presented, 116 answered (clue verbatim on even indices), 8 correct.
KEY FIND: all 8 correct answers were clues whose trailing line began with **0**
("0 bump", "0 home", "0 tip", "p 0 sprinkle"). So four classes are picture classes
where the trailing number = how many edits, and 0 means "leave the picture alone".

## Class notes

### tovel — calendar, "N bump"   [DEMO 1]
Kid's-eye view of the demo: "It's a month wall-calendar. Some days have a letter,
some have a dot. In the answer, three letters in the middle of a busy week turned
into arrows, and the same letters popped up again a few days later."
Three things a kid notices first: (1) arrows `>` appear where letters used to be,
(2) the letters reappear later in the month, (3) days at the ENDS of a busy patch
did not move.
RULE: find maximal runs of consecutive days that all have events. Every event in
the *interior* of a run of length >=3 gets bumped (run of L gives L-2 bumps). It
moves to the next still-empty day after it; its old cell becomes `>`.
Verified: run-interior count == N on 35/35 round-1 clues; solver reproduces the
demo answer byte-for-byte. CONFIDENCE: very high.

### felsim — honeycomb pile, "N tip"   [no demo — cracked by arithmetic]
Hex grid: row r (0 = bottom) has cells at x = 2r + 4k. A cell rests on (r-1,k)
and (r-1,k+1). Every cell in every clue has >=1 support, so the pile is legal.
RULE: a cell "tips" if it has exactly ONE support AND nothing sitting on it.
Count of those == N on 29/29 clues. Answer = picture with those cells erased
(blanked to spaces, lines rstripped). CONFIDENCE: high on the trigger,
medium on "erase" being the edit — round 2 will tell.

### molvic — THE CORNER SHOP, "N home"   [DEMO 2]
Kid's-eye view: "Four shelves, each labelled with what belongs on it: ALE, RYE,
KEG, EGG. Mostly right, but a few things sit on the wrong shelf and there are
gaps. In the answer three strays vanished and three new correct items appeared in
the gaps." Three things a kid notices: (1) an item disappeared and left a gap,
(2) the new items always appear in the FIRST gap on their own shelf, (3) one
stray (rye on the ALE shelf) stayed put — the RYE shelf had no gaps at all.
RULE: a stray only goes home if it is half of a *straight swap in the same
column* (shelf Y holds X and shelf X holds Y at the same column), AND its home
shelf has at least one gap. It moves to the leftmost gap of its home shelf; its
old cell becomes `___`.
Verified: that count == N on 32/32 clues; solver reproduces the demo byte-for-byte.
CONFIDENCE: very high.

### garrow — rooms of a house, "<letter> N sprinkle"   [DEMO 3]
Kid's-eye view: "A row of rooms with dotted floors and little pairs of letters
lying about. In the answer two whole rooms had their dotted floor turned into
stars, and the letters stayed where they were." Three things a kid notices:
(1) NOTHING was added — the `:` just became `*`, (2) only some rooms changed,
(3) the changed rooms were the ones with the most `aa` in them.
RULE: for the named letter, any room containing 2 or more of it gets its whole
floor (`:`) replaced by `*`. N = number of such rooms (27/27 clues).
The trailing text line is dropped in the reference answer.
CONFIDENCE: very high. "sprinkle" is a lovely red herring — it adds nothing.

### borsel / mestrel / kaldrin — examples + candidates  [no demos, on purpose]
All three are the guide's §5b shape: a block of positive examples, blank line, a
block of candidates, exactly one of which fits the hidden rule. The rule changes
every clue, so a demo buys one rule, not the class — bad value. Instead: a
generic engine.
  borsel : rows of digits            atoms = digit
  mestrel: rows of dominoes [a|b]    atoms = (a,b,sum,diff,hi,lo,double,tile)
  kaldrin: trains [E]=[cargo^]=...   atoms = (cargo, flag, cargo+flag)
ENGINE: compute ~200 cheap features per row; keep every feature on which ALL the
examples agree; a feature matched by exactly one candidate is worth 3, otherwise
1/(number matched). Highest total wins. Self-checked by hand: it finds
"contains a repeated tile" on mestrel #0 and "some value appears >=4 times" on
borsel #1, which is what I derived by hand.
OPEN QUESTION: is the answer the candidate line verbatim, or its 1-based number?
Round 2 probes both (verbatim on even index, number on odd) — no demo spent.

## Demo budget: 3/3 used — tovel, molvic, garrow.
Deliberately no demo for: felsim (cracked by counting), borsel/mestrel/kaldrin
(a demo only reveals one instance's rule, not the family).

## Round-by-round
| round | presented | answered | correct | notes |
|---|---|---|---|---|
| 1 | 232 | 116 | 8 | harvest; clue-verbatim on even indices — the 8 hits were all "0" clues |
| 2 | 227 | 227 | 146 | tovel/molvic/garrow 100%; felsim erase FAILED; format probe: verbatim AND number both accepted |
| 3 | 197 | 197 | 124 | felsim probe: move / cascade-move / prop — all 0 |
| 4 | 181 | 181 | 107 | felsim probe: 5 glyph markers + 2 lean glyphs + erase-keep-length + cascade-erase — all 0 |

felsim trigger re-verified 115/115 across all four rounds; the top row never empties,
so no rendering artefact is hiding a correct edit. The edit itself stays unsolved.

Engine config shipped: unique-selecting features only, weighted by smoothed
per-class family reliability fitted on rounds 2-4 (258 items). Leave-one-round-out
on the 104 items whose true answer I know: unique-only 96.2%, +family weights 97.1%,
mixed (unique + partial) 88.5% — so unique-only + weights.
