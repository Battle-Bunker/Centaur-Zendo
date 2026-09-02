# Lateral direction: an invented notation / mini-language

Design constraints recap: clue is a short string in a made-up notation; the answer must be
a string in the *same* notation standing in a hidden relation to it; `score` <= 512 chars
and must verify the relation from the clue alone; empty string, the clue itself and any
constant answer must score 0; the answer must genuinely depend on the clue.

Players (measured): ~450 graded probes per 0.5 s round, 6 rounds, 6 demos. Named textbook
objects are recognised instantly; a human-invented rule (LegoZendo) cost 3-4 demos. So the
notation must (a) not resemble a known formalism, (b) reward decoding semantics rather than
computation, (c) not admit a surface heuristic that scores 1 most of the time.

## Brainstorm

1. **Stroke script with a cyclic closing relation ("quaich")** — CHOSEN.
   Alphabet is three strokes `/ - |`. There are no visual openers/closers: every symbol can
   open and every symbol can close, and the closing relation is a 3-cycle
   (`/` is closed by `-`, `-` by `|`, `|` by `/`). A word is *well formed* if the eager
   left-to-right reading (push, unless the current stroke closes the stroke on top of the
   stack, in which case pop) empties the stack, and *whole* if the stack is empty only at
   the very end (no proper prefix is balanced, i.e. the word is a single nested unit).
   The clue is a scrambling of a well-formed whole word that is itself NOT well formed.
   The answer must be a rearrangement of exactly the same strokes that IS well formed and
   whole. Discovery ladder: (i) the answer is an anagram of the clue; (ii) the last stroke
   is always the cyclic successor of the first; (iii) it is a bracket language with an
   invented, non-involutive pairing; (iv) top-level concatenation is forbidden.
   Cheap to check (one stack pass + `sorted(s)==sorted(c)`), ~250 chars.
   Trivial witnesses closed: `""` (multiset), the clue (generator guarantees it is not well
   formed), any constant (multiset), sorted order (`///---` style fails unless counts
   coincide), palindromes (the cyclic pairing kills mirror answers), pair-concatenation
   `/-|/` (killed by the wholeness clause). Random shuffling scores ~0.4-1 % (measured),
   which is a legitimate but very weak evidence channel, not a crack.

2. **Two invented scripts, translate between them.** Clue in script A, answer in script B.
   Rejected: this is a substitution cipher with a small alphabet; LLM players solve
   substitution ciphers from two demos, and there is nothing lateral left afterwards.

3. **Made-up poem form, produce the next line.** Clue is a line of symbols; the answer must
   match a hidden metre (count of one symbol class), rhyme (shared suffix) and differ from
   the clue. Rejected: every clause is a surface statistic that ~450 probes per round
   discover by ablation; no single "aha".

4. **Rewrite system: reduce to a normal form.** Clue is a word, answer must be its normal
   form under invented rules. Rejected: a canonical answer means the demos are a lookup
   table and the map is inferred in 1-2 demos; and a non-canonical version needs the scorer
   to search, which does not fit 512 chars / 50 ms.

5. **Invented grammar, "reply to the sentence".** Clue is a question sentence with markers
   for topic/polarity; the answer must agree in class, echo the topic morpheme and flip the
   polarity. Rejected: too close to natural-language morphology, which is exactly the prior
   an LLM has; and the scorer needs many small clauses, eating the 512 chars.

6. **Bracket completion with holes.** Clue is a partial word `/?-?|?` and the answer fills
   the holes. Kept as a *hardening variant* of idea 1 (forces position information into the
   clue) rather than as the v1 rule: the "fill the `?`" convention is spotted immediately,
   so it adds bookkeeping rather than insight, while the underlying grammar still has to be
   the alien part.

7. **Same-normal-form words.** Answer must be any word reducing to the same normal form as
   the clue. Rejected: `clue + xx` (a cancelling pair appended) is a trivial witness, and
   patching it with a length constraint makes the rule arbitrary rather than discoverable.

8. **Invented numerals with sign/scale marks; answer is the successor.** Rejected: LLMs
   decode positional numeral systems from two examples; the notation is a thin disguise.

9. **Depth-parity twist**: the closing relation reverses at odd nesting depth. Held in
   reserve as hardening lever for idea 1 if both players crack v1.

10. **Second clause held in reserve**: require a specific stroke to occur at maximum depth,
    or require the number of top-level children of the root to be encoded by the clue.

## Chosen: `quaich` (idea 1)

Name is a neutral short word with no relation to strokes, nesting, anagrams or cycles.
