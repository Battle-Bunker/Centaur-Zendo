# Wordz — notes

## Rule (confirmed, 100% on 4 rounds + final)
Clue = string of digits d1..dk (observed k in 3..6, digits 1..9).
Answer = k dictionary words, one per digit.
  * word at an ODD position  (1st, 3rd, 5th) must have exactly d vowels    (a e i o u, counted with repeats)
  * word at an EVEN position (2nd, 4th, 6th) must have exactly d consonants (with repeats)
  * every word must be in the server's English dictionary (matches the `english_words` web2 list)
Word choice is otherwise free; repeats of the same word are allowed.

## Evidence trail
- demo 1: 34222 -> "squire wilson align tab stricken"   v3 / c4 / v2 / c2 / v2
- demo 2: 443633 -> "situated healing assumed smallpox investor wheat"  v4/c4/v3/c6/v3/c3
- demo 3: 3322 -> "sneaking hall norman ante"           v3 / c3 / v2 / c2
- Round 1 lone hit 12141 -> "to the to which to" (v1/c2/v1/c4/v1) while 2424 ->
  "the which the which" missed: that pair killed every position-independent rule.
- Round 2 (demo words keyed by digit) gave 28/130: 216 "align to smallpox" missed
  but 261 "align smallpox to" hit -> order matters -> alternating property.
- 13 answers satisfied the alternating rule yet scored 0; every one of them
  contained a word absent from web2 (ears, coins, murdered, programmes, qb, ...).

## Solver
on_round_start builds, from wordfreq top-200k filtered to web2, one word per
(vowel count) and per (consonant count). solve() is a table lookup + join,
~1 us, with a clue->answer cache.
