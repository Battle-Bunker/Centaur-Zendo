# Star challenges — what they are and why they work

Appended whenever a class reaches (or convincingly approaches) the calibrated band. Each entry:
the rule in plain words, what a kid sees, what the players did, and the design lesson.

## OKRIN — "finish the letter pattern" (forced completion, three clauses)
**Rule.** Clue: 3–5 distinct capital letters, e.g. `KSA`. Answer: a grid in which the first line
starts with the clue itself, every letter's right-hand neighbour is the next clue letter (cyclic)
and the letter below it is the previous one, no letter stands alone, and each clue letter appears
exactly (2 + its alphabetical rank among the clue letters) times. Anything that is not a clue
letter is filler.
**What a kid sees.** Diagonal stripes of the clue letters running down-left, like a knitted
pattern, with the clue written in the top-left corner.
**What players did.** One cracked it in round 4 with 3 demos, isolating the "starts at the
corner" seed clause last from residual near-misses. The other found the count rule and the
stripe geometry but never the chirality/seed clause as a rule and learned a lookup table
instead: 73 % in the final.
**Why it works.** Three independent clauses, each worth nothing alone, so partial understanding
scores 0 and the demos (positive examples only) cannot finish the job: the last clause has to be
found by spending a round on falsification. The clue letters are visible in the picture, so a kid
can *see* the seed; the alphabetical-rank count is the kind of arbitrary-but-natural measurement
a kid will hypothesise ("the letter that comes first in the alphabet appears least").

## quaich — "an invented way of pairing up strokes" (notation)
**Rule.** Clue: a scrambled word over three strokes `/ - |`. Answer: any rearrangement of the
same strokes that "closes properly" when read left to right, where `/` is closed by `-`, `-` by
`|`, `|` by `/` (a 3-cycle), using a stack, and the whole word is one nested unit rather than
several side by side.
**What a kid sees.** Three kinds of tally strokes that must be shuffled into an order the
server likes; every demo is an anagram of its clue and always ends with the stroke that
"follows" its first stroke.
**What players did.** One cracked it by round 5–6 with 3 demos, but via an empirical block-form
family (`/^r |^r -^p |^p /^q -^q` with case splits) fitted to the demos, never the grammar.
The other found only correlates (starts `/`, ends `-`, bigram frequencies), trained a model and
plateaued at 23 %, which "felt like convergence".
**Why it works.** The pairing relation is invented (no textbook bracket language has three
mutually-closing symbols), so recognition yields nothing; but the surface statistics are rich
enough that a statistical proxy scores 15–30 %, which is the partial band. A kid's contribution
is the "each stroke closes a *different* stroke" idea, a playground-rules style hypothesis that
the models did not propose.

## murn (v2) — "what can stand on what" (invented support physics)
**Rule.** Clue: a ground row of stone `#`, wood `o` and air `.`, plus a stone quota `n`. Answer:
a picture whose last row is the ground row and which stands exactly `n` stones above it, where
a stone needs exactly two of the three cells beneath it occupied, wood exactly one, nothing may
stand on its own kind, and nothing floats or is over-braced.
**What a kid sees.** A wall being built up from a foundation, zig-zagging because stones can't
sit on stones; a very physical "will it stand up?" question.
**What players did.** v1 (no staggering clause): both cracked, but late (rounds 5 and 6, 4–6
demos) by constraint propagation over ~1900 labelled answers. v2 (staggering added): one
cracked in round 5 with 4 demos, the decisive evidence being a *sparse* demo; the other found
four of five layers (shape, quota, local support counts) and never the "not on its own kind"
clause: 3 % in the final.
**Why it works.** The law is a conjunction of local rules with a physical feel, so hypotheses
come naturally to anyone who has stacked blocks, yet the exact quantities (exactly two, exactly
one, own kind forbidden) are arbitrary enough that priors do not settle them. Demos only show
things that *do* stand, so "exactly" (not "at least") is invisible until a probe falls over.
The staggering clause is the lesson: a rule about *which material* is underneath punishes any
player modelling only *how many* cells are underneath.

## Cross-cutting reflections
* Every star has a **visible seed** (the clue appears inside the answer) and a **count**; the
  count is the kid-friendly half, the seed closes the degenerate witness.
* The failed player in each pair converged on a **statistical proxy** worth 3–73 %. That is what
  "sometimes" looks like in practice: not random luck, but whether the player generated the right
  hypothesis before the rounds ran out.
* Classes that were cracked by all players (quilm, the 31 textbook classes, LegoZendo v1 via its
  witness) shared one property: **the rule could be named** or the witness could be built
  without the rule.

## virel — "bricks resting on their twin" (toys and building; candidate star)
**Rule.** Clue: the bottom course of a wall as brick widths, e.g. `33655`, and a number `N`. Answer:
an ASCII wall (`[--][---][]…`), every course the same width, at least five courses, the bottom
course exactly the clue, with exactly N bricks sitting precisely on top of a brick of the same
span (same left and right edge) in the course below.
**What a kid sees.** A brick wall. The kid-proxy players reported their imagined child said
"it's a wall and every line is the same length", read the bottom row as the clue digits by
counting dashes, and asked "what's the little number after the slash for?" three times.
**What players did.** Experimentalist: cracked exactly in round 3 with 3 demos (after detours
through base conversion and Project Euler's crack-free walls). Kid-proxy: found four of five
clauses (width, clue row, no fault line, ≥5 courses) and never what N counts; 14 % in the final.
Kid judge: 3.8/5.
**Why it works.** The object is instantly nameable but the measurement is not: "a brick resting on
its twin" is below "the joints line up" in a model's candidate list and near the top of a kid's.
The generator rejection-filters every wall so that all rival statistics differ from N and forces
decoys (aligned joints, near-twins) into every demo, so the famous fact about walls (stagger the
joints) is visibly false. Partial understanding pays 10–20 %, a real gradient without a cliff.
**Lever if it drifts easy.** Count only twins that are not adjacent to another twin; pin the bottom
course by width alone plus a second clause.

## fennick v3 — the bookshelf (calibrated 2026-09-05, new format)

**Rule.** The clue is a shelf drawn from the side: books as columns of one letter with a `_` cap,
arbitrary heights, gaps between them, a `====` shelf line, and a caption `4 fall`. The answer is
the same picture with exactly the right books tipped over: a book falls iff one side of it is a
single empty slot, the other side is a touching book, and the book across the gap is strictly
taller (it has something to lean on); a fallen book keeps its foot in its slot and its body and
cap slide one column into the gap, the cap becoming `/` or `\`. Nothing else may change.

**Record (4 Opus finals, 4 profiles): 11 %, 100 %, 11 %, 100 % — mean 55 %; with a demo 70 %
(3 players), without 11 % (1).** The 11 % scores are the `0 fall` clues, where the correct answer
is the clue unchanged: a player who has understood only the *format* banks them. The two 100 %
players were the kid-proxy ("the shorter one falls into the gap next door", round 3) and the
theorist ("that one's fallen over onto the tall one", round 2). The two who failed with the demo
in hand tried arithmetic — "the four shortest", "heights summing to 4" — and never asked the
physical question.

**What a kid sees.** A bookshelf, some books knocked over, and a caption saying how many. The
question "why did *those* fall?" has an everyday answer: a book falls into a gap when there is a
taller book on the far side to lean on and a neighbour behind it to push from. Every demo shows
the positive case beside its three near-misses (equal heights across a gap stand; a book with
gaps on both sides stands; a two-slot gap is out of reach), so one demo can teach the whole rule.

**Why it works under the demo economy.** The clue carries the object (the upright shelf) and the
verb (`fall`), so a demo-less player sends well-formed attempts and even scores the identity
cases; the *rule* still needs the example — every player who cracked it spent a demo here, and
no one cracked it blind. The red herring of v1/v2 (a height formula) is gone because heights are
given in the clue; the only work left is the tipping physics, which is one clause. It is the
first class whose split is by *reading* rather than by *probing*: the same demo produced 11 % and
100 % depending on whether the player looked at the picture as a shelf.

**Levers.** Too easy: require the caption to be dropped (removes the identity foothold) or draw
some books already leaning in the clue so the answer is "which further ones fall". Too hard:
put a single fallen book into the clue as a worked instance.

## kelmar v3 — rain over a garden (calibrated 2026-09-05)

**Rule.** The clue is a finished weather picture: a cloud row `(~~)`, three rows of falling drops
`''''` under each cloud (some showers stop in mid-air), a garden row of flowers `*` and trees `Y`
on the ground, and a caption `2 lean`. The answer is the same picture with exactly the right
plants redrawn leaning (`/` or `\`): a plant leans over for a drink iff the shower right next to
it comes all the way down to the ground. A shower that hangs in the air is no use to anyone.
Nothing else may change; the caption may be kept or dropped.

**Record (4 Opus finals): 100 %, 13 %, 13 %, 100 % — mean 57 %; with a demo 71 % (3 players),
without 13 % (1).** The 13 % scores are the `0 lean` clues (the echoed clue). The two 100 %
players both bought the demo and both cracked it in round 2 *offline*: one verified "every plant
touching a full-height tree leans" on 67/67 harvested clues before answering a single one; the
other wrote "a mushroom whose stem reaches full height pushes over the plant beside it". Neither
saw rain — they saw trees or mushrooms — and it did not matter, because the relation they read
(the column reaches the ground) is the rule. The one demo-holder who failed had an imagined kid
say "clouds with rain under them" and ignored it, parking on the foothold.

**What a kid sees.** Clouds, rain, a garden, and a caption saying how many plants lean. The
question "why did *those* lean?" has an everyday answer once the kid notices that some showers
stop short: the plants next to rain that actually lands lean towards it. Every clue plants the
near-misses in one picture: a flower standing in the rain (does not lean), one directly under a
hanging shower, one beside a hanging shower, and a tree two columns clear.

**Why it works.** This is the fennick recipe applied to a class that had scored 0–9 % across
twelve finals: the object that had been the *answer* (the rain) moved into the clue, the answer
became the smallest edit of the picture, and the caption became a checksum. v2 had asked players
to invent the rain, so the picture read as arbitrary blocks and the plants read as decoration; v3
asks only "which plants?", and the caption lets the answer be tested against 80 clues for free.
The reading is what splits players: read it as weather (or trees, or mushrooms — anything
physical) and it is one clause; read it as bookkeeping and the numeric thresholds never fit.

**Reflection.** Three versions of kelmar carried the same relation (plant beside landing rain) and
scored 0, 5 and 57 %. The rule was never the problem; what changed was *which half of the picture
the player had to produce*. When the answer is the complicated half (rain), the class is opaque;
when the answer is the small edit (a lean), it is fair. That is now the house rule for every
picture class: finished object in the clue, verb and count in the caption, the demo shows how the
edit is drawn.

**Levers.** Too easy: make the reach depend on the plant (trees drink from two columns away,
flowers from one) so "nearest landing rain" stops being enough. Too hard: draw one plant already
leaning in the clue as a worked instance.

## virel v3 — the next course of bricks (calibrated 2026-09-05)

**Rule.** The clue is a finished wall, three or four courses of bricks `[--][---][]…`, every
course the same width, plus a number N in 0..3. The answer is the same wall with ONE more course
laid on top, a gapless row of bricks 2–6 wide, such that exactly N of the new bricks sit
precisely on top of a brick of the same span (same left and right edge) in the course below. Any
course that does it scores; the reference builds one at random.

**Record (4 Opus finals): 100 %, 100 %, 0 %, 20 % — mean 55 %; with a demo 73 % (3 players),
without 0 % (1).** The two 100 % players both bought the demo and both reported that their
imagined 12-year-old got there first: "it's a brick wall, you put the next row on top, and look —
no brick is sitting right on top of another brick"; "a child would have counted: one brick in my
new row sits exactly on a brick below". Both AIs first measured joints (the famous fact about
walls: stagger the joints) and lost most of an hour before trying the kid's sentence. The
theorist who scored 20 % with the demo never fixed the brick mix and treated it as number
theory; the low-demo player never learned the format at all (0 %).

**What a kid sees.** A wall, and the job of laying the next row. The number is how many bricks are
allowed to sit *exactly* on a brick the same size. Virel is the one class in the pool whose
answer's shape is NOT readable from the clue — the clue is a wall and a number, and nothing says
"add a row" — so every player who scored bought the demo, and the demo teaches the format and the
rule in one look.

**Why it works.** v2 asked for a whole wall of five courses carrying exactly N twin stacks — a
search that players never finished, so identical answers scored 1 on one clue and 0 on another
and looked unfair. v3 collapses the construction to one course, which makes the answer a
sentence ("add one row so that exactly N bricks sit right on top of a brick the same size") and
keeps the measurement unnameable: "resting on its twin" sits below "the joints line up" in a
model's list and near the top of a kid's. The generator makes the width budget force decoys
(near-twins, aligned joints) into every clue.

**Reflection.** Virel is calibrated for a different reason from fennick and kelmar: it is
demo-gated by *format*, not by rendering. That is fine as one class in seven — the players
said so themselves — but it means the class's rate is decided almost entirely by whether a
player chooses to spend a demo on the opaque clue. A pool should carry at most one such class.

**Levers.** Too easy: count only twins that are not adjacent to another twin. Too hard: draw the
new course's first brick already in place.

## basten v4 — the fish tank (calibrated 2026-09-05)

**Rule.** The clue is a finished fish tank: a `~` water surface, a `#` gravel floor, weeds drawn as
columns of `|` of different heights, and fish `><>` / `<><` facing left or right, plus a caption
`2 nibble`. Each fish looks straight along its row at the first weed in front of it; if that
weed's top is in the fish's row or one row above, the fish swims over until its nose touches the
weed and nibbles the top segment off. Fish whose weed is out of reach (its top too high or too
low) stay where they are. The answer is the same tank with exactly those fish moved and those
weeds one shorter.

**Record (4 Opus finals): 13 %, 13 %, 13 %, 100 % — mean 35 %; with a demo 100 % (1 player),
without 13 % (3).** Basten had been at 0 % across sixteen finals of three earlier versions: v1–v3
showed an empty tank and asked the player to draw N fish, so the number was a free parameter and
nobody could test anything offline; nobody bought the demo because the tank was already drawn,
and nobody cracked it blind. v4 put the fish in the clue, made the answer the smallest edit, and
made the caption count the edits. The one player who then bought the demo verified the rule on
44/44 harvested clues before answering and scored 100 %; his sentence was the kid's: "the fish
swam over and bit the top off the weed it could reach".

**What a kid sees.** A fish tank, which every player and every judge has named instantly (kid
score 4.5, the highest object score in the collection). The question "why did *those* fish
move?" has a physical answer that a kid asks about before an AI does — "can it reach?" — and the
rule's only clause is vertical reach, which a diff of two pictures does not reveal but a glance
at the scene does. Every clue plants the near-misses: a fish staring at a weed whose top is far
above it (stays), a fish whose weed is exactly one row up (nibbles), a fish level with a taller
weed (stays).

**Why it works.** Same recipe as fennick and kelmar, with one extra lesson: the refiner's first
draft used *blocking* (a fish queued behind another cannot get through) as the near-miss, and
that leaked — blocked fish were systematically further from their weed, so "the n fish closest
to their weed" scored 89 % for any demo-holder. Replacing it with vertical reach, which is
orthogonal to horizontal distance, dropped every wrong rule below 32 %. The generator also
decorrelates the obvious rankings on purpose (an out-of-reach fish is nearer its weed than a
nibbler in 80 % of clues, and further in 79 %).

**Reflection.** Basten is the clearest demonstration in the ladder that a class's difficulty is
almost entirely a property of which half of the picture the player has to produce, and that
the with-demo / without-demo split is the shape the format wants: 100 % for the one player who
spent a demo, the format foothold for everyone else. Whether a class like this is "worth a
demo" is now the whole strategic question, and the players say they cannot tell from the clue —
which is the point.

**Levers.** Too easy: let reach depend on the fish (a big fish reaches two rows). Too hard: draw
one fish already at its weed with the top nibbled as a worked instance.

## norvel v4 — the drum grid (calibrated on rate 2026-09-05; kid 3.7, below the bar)

**Rule.** The clue is a finished three-row drum grid, hat / snare / kick in bars of four steps,
and a caption `3 slip`. A snare hit with no hat above it and no kick under it — a hit left
playing on its own — skids late: it leaves `-` where it stood and on across the hat's gap, and
lands `x` on the first step where the hat ticks again. The answer is the grid with exactly those
hits moved. **Record (6 Opus finals): 100 %, 100 %, 100 % with a demo; 15, 14, 14 % without.**
Three versions before it (an empty snare row to fill, n a free parameter) never passed 12 %.

**Why it is not yet a star.** The judge scores it 3.67: the grid is more visual bookkeeping than a
picture, and the clue does not say which row changes. Both are salience fixes (fewer bars, caption
"n snare slip") and the player evidence is unambiguous that the rule itself is one breath — one
player needed a second demo only because the first happened to fit "slip the first n pairs", a
non-discriminating example, which the engine now avoids for the n = 0 case but not in general.
A demo-drawing rule (prefer an example that refutes the commonest wrong reading) is the next
engine-side lever for every picture class.

## molvic v3 — the corner shop (calibrated on rate 2026-09-05; kid 3.3, below the bar)

**Rule.** Four labelled shelves of goods; a few strays stand on the wrong shelf. Two strays in
the same slot, one above the other, each on the other's shelf, both go home to the first empty
slot on their own shelf — unless that shelf is full, in which case that one stays. Caption
`n home`. **Record (4 Opus finals): 100 % with a demo; 20, 16, 15 % without.** v1 was cracked
blind at 100 % by both players (a letter swap is guessable and the checksum pinned it offline);
v2 made the rendering need the demo (goods move to a gap elsewhere) and planted the full-shelf
refusal so the blind reading scores 0; v3 re-skinned it as a shop with written labels.

**Why it is not yet a star.** Two conjuncts plus an asymmetric split (one of a pair moves, the
other is refused) is more than one breath, and the judge's advice is to cut the room-at-home
clause and buy the difficulty back with a single visual quirk. The evidence says the class plays
exactly to the fennick shape, so the fix is legibility, not difficulty.
