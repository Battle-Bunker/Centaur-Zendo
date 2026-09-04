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

## Iteration 1 outcome (lab-quaich-1) — MIXED, on target, no v2

| player | rounds (correct/answered) | final | verdict |
|---|---|---|---|
| quaicha | 1/590, 35/476, 248/469, 375/461, 448/457, 571/571 | 3539/3539 (100 %) | **cracked**, round 5-6, 3 demos |
| quaichb | 1/572, 13/500, 73/513, 47/310, 64/322, 78/403 | 728/3149 (23 %) | **partial**, never found the rule |

quaichb got the anagram property from demo 1 and then only correlates (start `/` / end `-`
enriched, bigram `|/` enriched, `--`/`||`/`|-` depleted), trained a 9-weight bigram model
and sampled best-of-16; it plateaued at ~23 % and reported that the plateau "feels like
convergence" — the intended failure mode for a statistical proxy.

quaicha never found the nesting or the eager reading, but did recover the **pair-count
decomposition** (p, q, r above) and emitted a fixed three-block layout
`/^r |^r -^p |^p /^q -^q` with case splits. Verified: 600/600.

Decision: **leave the rule unchanged.** Measured, the family is not cheaply closable:

| candidate extra clause | family still valid on | accepted set removed |
|---|---|---|
| no run of >= 3 identical strokes | 20 % of clues | 54 % |
| no run of >= 4 identical strokes | 51 % of clues | 14 % |
| some node has >= 2 children | 83 % of clues | 1 % (no separation) |

None separates "understood the nesting" from "fitted a layout to the counts", because once
the pair multiset is known *some* canonical layout always exists; and quaicha's solver
already contains block-splitting logic, so a run cap would simply be re-fitted with ~450
probes per round. Shrinking the accepted set would also push quaichb from partial to
failed, i.e. off target, with no player run left to verify it. The proper close is lever 1
(positional information in the clue — the hole-completion variant, idea 6), which is a
different challenge, not a tweak.

## Iteration 2 (2026-09-04) — RE-SKIN for the kid rubric: strokes -> nesting cups

Trigger: AI balance was fine (mean final 64 % over 2 finals: one crack, one 23 % partial)
but the 12-year-old judge scored v1 **1.6/5** — "no recognisable object, abstract stroke
grammar, nameable as *custom bracket matching*". Judge's advice: re-skin the cyclic pairing
onto a concrete touchable object (paper-chain links, nesting cups/boxes) so that the pairing
and the "one single nested chain, not several end to end" clause become **visible in the
demo**.

v1 is preserved as `challenges/lab/quaich.v1.json`; the new version is
`challenges/lab/quaich.json`.

### What changed (skin only)

| | v1 | v2 |
|---|---|---|
| alphabet | strokes slash, dash, bar | cup colours `R G B` |
| closing relation | slash→dash→bar→slash | R→G, G→B, B→R (**same 3-cycle**) |
| wholeness clause | unchanged | unchanged |
| clue | scrambled word, 12–18 chars | scrambled pile of cups, 12–18 chars (**still tiny**) |
| answer space | anagram + stackable + whole | **identical** (letters only are read) |
| `solve()` output | the bare word | an **ASCII drawing of nested boxes** |
| `score()` | 238 chars | 275 chars (adds "ignore any character that is not R/G/B") |

Nothing about the rule moved. Verified mechanically:
* `generate(seed)` in v2 is *exactly* the relabelling (`/`→R, `-`→G, `|`→B) of v1's
  `generate(seed)` — 0 mismatches over 500 seeds;
* v2 `score` agrees with v1 `score` on the relabelled string for **10 000** random probes
  (0 mismatches). The accepted set is isomorphic, so v1's balance evidence carries over.

The scorer now reads only the R/G/B letters of the submission, in order, and ignores every
other character. So the answer may be sent as a bare word *or* as the picture; `solve()`
always sends the picture, because the demo is the only channel that reaches a kid.

### The picture (this is the whole point)

```
clue:  BGRRGBRRRGRBRB          <- 14 loose cups in a heap

+R----------------+
| +B----+         |
| +----R+         |
| +B----+         |
| +----R+         |
| +R------------+ |
| | +R--------+ | |
| | | +B----+ | | |
| | | +----R+ | | |
| | | +B----+ | | |
| | | +----R+ | | |
| | +--------G+ | |
| +------------G+ |
+----------------G+
```

One box per pair: opening colour on the top edge, closing colour on the bottom edge,
children stacked inside their parent (children grow the drawing downwards only, so width is
4·depth + 7 and the whole picture stays ≤ 647 chars over 3000 seeds, well under the 1024
solution cap). Reading the letters top-to-bottom reproduces the word exactly.

### 12-year-old test, applied explicitly

*What a kid sees in one demo*: a heap of red/green/blue cups, and a drawing of boxes inside
boxes inside boxes. Count the letters in the drawing — same cups as the heap, so "it is the
same cups, restacked". Every box has two different colours: R on top always ends G, G always
ends B, B always ends R — **the invented pairing is now readable straight off the picture**,
which is exactly what the judge asked for. And there is exactly **one** outer box: the
"single tower, not two towers side by side" clause is a thing you can point at.

*What is still not nameable*: which restackings actually count. The hidden layer is the eager
reading — you go along the row and a cup snaps shut the instant the matching colour arrives,
so a G may never be put straight inside an R (it would snap the R shut early); equivalently a
box may only hold boxes of its own colour or of the previous colour in the cycle. That is an
arbitrary-but-natural measurement of the object, not the object's famous operation, and it is
invisible in the picture — v1's `quaicha` cracked the class *without ever finding it*.

Kid score predicted: **4/5** (object recognisable from one demo, two of the three clauses
pointable, one clause left to experiment on). Not 5 because the drawing is boxes-in-boxes
rather than a coloured photograph, and the clue is still a letter string.

### Witness table (500 fresh clues, v2 scorer)

| witness family | v1 | v2 |
|---|---|---|
| empty string | 0 % | **0/500** |
| the clue itself | 0 % | **0/500** |
| constant answer (`RG`, `R^6G^6`) | 0 % | **0/500** |
| sorted order, all 3 rotations | 0–1 % | **0/500** |
| descending sort | 0 % | **0/500** |
| reversed clue | 0 % | **0/500** |
| palindrome (half + mirror) | 0 % | **0/500** |
| greedy pair-concatenation `RG*a GB*b BR*c` | 0 % | **0/500** |
| uniform random shuffle | 0.4–1 % | **5/500 (1.0 %)** |
| all openers then all closers (`R^4G^4B^4`) | 0 | **0** (wholeness) |
| naive nesting that ignores the eager read (`RGBG…`) | 0 | **0** |
| two valid towers end to end | 0 | **0** (wholeness) |
| quaicha's block layout (the v1 crack) | 600/600 | **500/500** (deliberately left open) |
| reference `solve()` picture / letters only / picture + junk text | — | **500/500 each** |

### Known risk

The picture hands AI players clause (2) (the pairing) and clause (3) (single tower) in demo 1,
which v1 hid behind a flat string; only the eager-reading layer stays hidden. Expect the mean
final rate to rise above v1's 64 %. If the next run classifies `too_easy`, the compensating
lever is idea 9 — the **depth-parity twist**: the closing relation runs the other way round
the cycle at odd depth, so a box's bottom colour depends on how deep it sits. That stays fully
kid-visible in the same drawing (a kid can see that the deeper boxes close the other way) and
does not add jargon, while breaking every count-only layout family including quaicha's.
