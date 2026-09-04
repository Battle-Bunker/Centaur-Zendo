# Rule-family classes ("guess the rule from a few examples")

Added 2026-09-04 at the organiser's request. A second paradigm next to the picture classes.

## The idea
A class owns a **finite universe U of candidate rules** over some world of instances (card hands,
dice rolls, bead strings, words, clock times, small pictures, shopping lists, football scores…).
Each rule is a template with parameters, e.g. for a hand of cards:
* count of suit X is (<, >, =) n
* the count of every suit is prime
* the sum of the values of (all cards | suit X) is (= n | prime | a multiple of y)
* … a dozen or two templates, each with a small parameter grid.

`generate(seed)` draws one rule R from U (parameters included) and then draws **positive
examples** — instances that satisfy R — and keeps adding/replacing examples until the set of rules
in U consistent with all the examples is **exactly {R}**, and is **minimal**: removing any one
example leaves at least two consistent rules. The clue is those examples, one instance per line
(nothing else). The answer is **one more instance that satisfies R** (well-formed, not one of the
examples). `solve()` re-derives R from the clue exactly the way the scorer does and constructs
a fresh instance. `score()` parses the examples, enumerates U, filters by the examples, expects a
single survivor R, and returns 1 iff the answer is a well-formed instance, not among the
examples, satisfying R.

## Why it is hard in the right way
* The clue's shape tells the player the answer's shape at once (another line like the examples),
  so a demo-less player always sends well-formed attempts — the demo economy is satisfied for free.
* The examples are **just enough** to pin R inside U — but a player does not know U. Their own,
  larger hypothesis space contains rules the designer never uses (deliberately excluded obvious
  ones: "all the same suit", "all red", "sorted", "no repeats"…) that also fit the examples. A
  player who answers with an instance of such a rule scores 0. Over many clues and 0/1 feedback
  they must learn **which rule types the class never uses**, and which it does. Even a player who
  has mapped most of U will sometimes be wrong when an unmapped template survives.
* Difficulty dials: the size and shape of U, which obvious templates are excluded, how many
  examples (fewer = more ambiguity for the player; the filter keeps it unique within U), and how
  "distant" the excluded rules are from the used ones.

## Design rules
1. Choose U so that every rule is a one-breath kid sentence about the world ("three hearts",
   "every suit an odd number of times", "the spades add up to twenty").
2. Exclude at least three obvious templates that a first-time player will try, and record them
   in the private description. Make sure they are frequently consistent with the examples (that is
   the trap) — the generator does not need to avoid them; only rules IN U are filtered.
3. Minimality: 2–5 examples; the generator must verify uniqueness within U and minimality;
   report the distribution of example counts.
4. Answers must be verifiable by the scorer from the clue alone (SPEC §2: no hidden channel).
   The scorer re-derives R; if U cannot be enumerated within the scorer cap, encode U as a tiny
   table of (template id, parameter) pairs and one shared predicate function. Target ≤ 512 chars;
   this paradigm may use up to 1024 (declared judgement call: `max_score_code_chars` may be
   raised to 1024 for the pool if a family needs it — report the length).
5. Well-formedness must be strict but the world simple (fixed instance size, small alphabet) so a
   demo-less first probe — "copy an example with one change" — is well formed and sometimes right
   (the foothold: report its rate).
6. The witness table must include: copy an example verbatim (must score 0), copy with one random
   change, an instance of each excluded obvious rule fitted to the examples, an instance of the
   most common U-template regardless of examples, random instances, and the true rule.
7. `solve()` must not leak: vary the constructed instance (random among valid ones), never the
   minimal or canonical one.

## Worlds to try (one class each; keep them small and legible)
cards (hands of 4–6), dice (rolls of 3–5 dice), beads on a string (6–10 colours from 3–4),
words (4–7 letter English words: letter/vowel/position rules), clock times (`hh:mm`), tiny
pictures (5×5 of two symbols), shopping receipts (item, price), football scores (`3-1`),
dominoes (sets of 4), coins in a purse, playing-card layouts, weather-week strips.
