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
