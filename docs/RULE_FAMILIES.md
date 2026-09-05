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

## Revision 2 (2026-09-05): the lineup answer

**What the first run showed.** Two Opus players took no demos on the five rule-family classes and
scored 23–97 % on them (tresk 97 %, wisbek 95 %, dornic 77 %, tavrik 66 %, borsel 58 % for the
better player) with one method: build a pool of 200–350 candidate predicates, keep those true of
every example, and emit an instance satisfying **all** of them at once. The true rule is somewhere
in the pool, so the answer satisfies it by construction. Nobody named a rule; the excluded traps
cost nothing because satisfying an extra rule is harmless. The "fresh instance" clauses (no clue
card reused, unused length…) were the only thing that held them for a round, and players called
those invisible and unfair — rightly, since they are not part of the rule.

**The fix: make the answer a choice, not a construction.** The clue is the minimal identifying
example set **plus a lineup of k = 4 candidate instances**, and the answer is *which one* of the
candidates fits the hidden rule (write the candidate back verbatim, or its number). Exactly one
candidate satisfies R. Each decoy is built to satisfy R's **rivals**: the excluded obvious rules
that are consistent with the examples, and, where possible, as many out-of-U predicates as the
true candidate does, so that "the candidate satisfying the most of my predicates" is a decoy at
least as often as not. Choosing correctly requires knowing which rule the class means — the
intersection trick has nothing to intersect. The floor is 1/k = 25 % (the foothold), a player who
has mapped U scores 100 %, and a player with a bigger universe is fooled exactly when a decoy
satisfies one of their surviving rules — which is the behaviour the organiser asked for.

Rules for the lineup:
1. Exactly one candidate satisfies R. Verify in generate().
2. Every decoy fails R but satisfies at least one **excluded** rule that is consistent with the
   examples (the trap), and at least one decoy should satisfy *more* of a reasonable outside
   predicate pool than the true candidate does (report the rate at which "most predicates wins"
   picks a decoy: target ≥ 40 %).
3. Decoys must not be trivially distinguishable (same length/size as the true candidate where the
   world has a size; no repeats of examples; drawn from the same instance distribution).
4. The clue format: examples, a blank line, then the candidates one per line. The scorer accepts
   the chosen candidate verbatim (whitespace-insensitive) or its 1-based index.
5. Drop the "fresh instance" clauses — they are no longer needed and were never legible.
6. Witness table for revision 2: pick candidate 1 / a random candidate; pick the candidate that
   satisfies the most predicates from a broad outside pool; pick the candidate satisfying every
   rule in U that the examples allow (the in-U intersection — must be 100 %); pick by each excluded
   rule; a player who knows U minus its two rarest templates; the true rule.
