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
