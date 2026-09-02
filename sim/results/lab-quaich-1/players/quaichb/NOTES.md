# Centaur Zendo — lab-quaich-1 / team quaichb

Pool contains exactly ONE class: `quaich`.
Clue: random string over {-,|,/}, always EVEN length in {12,14,16,18}.

## What the answer is
Confirmed: the answer is always an ANAGRAM of the clue (same multiset).
The accepted set is broad (~0.3% of all anagrams; ~2.6% of anagrams that
start '/' and end '-'), so the checker is a PREDICATE, not a unique string.

Strong empirical structure of accepted answers (never fully cracked):
 * start '/' and end '-' hugely enriched (0/534 vs 1/38 in round 1)
 * bigram `|/` enriched ~2.4x; `-/`, `--`, `||`, `|-` depleted
   => answers like to walk the cycle - -> | -> / and avoid repeats/jumps
 * demo 5 (clue with only two '|') started '-' and ended '|', so the
   endpoint rule is a strong correlate, not a hard requirement.

## Final solver
Markov/bigram logistic model (9 weights) learned from 198 accepted +
2019 rejected answers; per clue, draw K=16 anagrams from a beta=0.12
softmax-biased sequential sampler (start '/', end '-', pos1 != '-',
pos n-2 != '|') and return the highest-scoring draw. ~0.2 ms/answer.
Over-optimising (hill-climbing to the model argmax, or K=48+) LOWERS the
hit rate — the accepted set is a band, not the extreme.
