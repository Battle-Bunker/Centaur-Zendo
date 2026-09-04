# sarn2a — notes

## Challenge class: `sarn`  (the only class in the pool)
Clue format: one letter + 3..6 digits, e.g. `h64582`, `d953`.
Answer: space-separated words, one per digit, ALL starting with the clue letter.
Clue letters seen: only {a,b,c,d,e,f,g,h,l,m,p,r,s,t,w}. Digits 1..9 (mode 2-4).

## The per-word rule (confidence: high on the shape, never fully solved)
Each word w must satisfy  f(w) == its digit, where
    f(w) = len(w) - 1 - penalty(w),   penalty in {0,1}
Verified on 150+ (word,digit) pairs: f is ALWAYS len-1 or len-2, never anything else.

Best closed-form guess (rule "B", ~80% accurate on hit-derived labels):
    penalty = 1  iff  (after collapsing doubled letters) the word ends in a
                      consonant AND contains no run of 2+ different consonants.
    e.g. hat/set/hell/heed/hood/team/meet/feel/for/facet/holiday/however -> len-2
         help/heath/point/hole/have/from/hanging/homestead/degenerate    -> len-1
Known counter-examples: draft, during, house, first, health, history, hospital,
met vs set, tell vs hell. So penalty is not exactly this; likely phonetic
(sounds/graphemes) rather than pure spelling.

## What actually won: an empirical lookup table
1. Every scored-1 answer confirms (word -> digit) for every word in it.
2. Every scored-0 answer whose other words are all confirmed disconfirms the
   remaining word (negative mining).
3. penalty(w) transfers when only the FIRST LETTER changes:
   hell/dell/fell all = 2, dor/gor/for all = 1, dave/gave/have all = 3.
   => one confirmed word populates a whole row of (letter,digit) cells.
4. Fallback for uncovered cells: rule B.

## Round log
r1 random-ish multi-hypothesis  1/454
r2 rule variants                5/500
r3 rule x rarity probe          7/476
r4 tail-transfer table v1      40/402
r5 table v2 (+neg-derived)     52/384
r6 table v3 (hits only) + B    152/515
final                        1441/3841  (37.5%)
