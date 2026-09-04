# Wordz — solved

## The rule
Clue = a string of digits. Answer = one dictionary word per digit, space separated.
Word in slot `i` (0-based):
* `i` EVEN  -> the word has exactly `d` VOWELS (aeiou)
* `i` ODD   -> the word has exactly `d` CONSONANTS (everything else)
* the word must be a real dictionary word (Webster's 2nd / `english_words` `web2`);
  names, British spellings and most inflected forms are rejected.

Confidence: certain. 100% precision AND recall over 1332 logged answers, and
1668/1668 correct across live rounds 4-6.

## How it was found
1. r1 random-ish probes: 2 hits. r2 A/B of 12 per-word features: best was
   "vowels==d" at 17% -> necessary-ish, not sufficient.
2. Demos showed words with identical vowel/consonant profiles getting different
   digits (`recipient`4 vs `reputable`5, `sigma`2 vs `apron`3) -> no per-word
   count function can work.
3. r3 single-variable experiment: confirmed-good baseline word in every slot but
   one. Control (all baseline) = 94.9%; the 4 control failures ALL had a `6` at
   an even index, where the d=6 baseline `something` has 6 consonants but only 3
   vowels. That was the tell: **position parity switches vowels<->consonants**.
4. Re-checked all three demos -> perfect fit; web2 membership explained every
   remaining false positive.

## Clue statistics (from 2119 logged clues)
* even slots carry digits 1-6 only; odd slots carry 1-9 (7:217, 8:52, 9:12).
* so the vowel table only needs 1-6; the consonant table needs 1-9.

## Table used (each entry confirmed accepted live)
even: 1 to, 2 your, 3 before, 4 american, 5 population, 6 autonomous
odd : 1 to, 2 your, 3 before, 4 american, 5 population, 6 something,
      7 government, 8 construction, 9 understanding
