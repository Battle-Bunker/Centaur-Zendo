# sarn1a — notes

Pool has exactly one class: `sarn`.  Clue = `<letter><digits>`, 3–6 digits,
digits 1..9 only, and only 15 first letters ever appear: a b c d e f g h l m p r s t w.

## Final rule (confidence: high)
Answer = one word per digit, in clue order.  Every word starts with the clue
letter; word i has exactly `digit_i + 1` letters; every word must be a member of
a secret server word list holding roughly 27% of ordinary English words.
Repeating the same word for a repeated digit is legal.

## How it was established
| step | evidence |
|---|---|
| letter + one word per digit | demo `p664 -> pendant patient pivot` |
| length = digit+1 | round 1 split even/odd on `len=d` vs `len=d+1`; all 4 hits were `d+1` |
| length/order really matter | round 2 variant that ignored digits ("have he his", all confirmed member words) scored 0/6 |
| word identity matters | `h324 -> have his house` = 0 while `h328 -> have his happening` = 1, both correct shape |
| membership is ~27% | 1.3% hit rate on 3–4 word answers of top-frequency words |
| duplicates allowed | round 6 A/B: reuse 75/207 (36%) vs distinct 50/214 (23%) |

## Method
`analyze.py` re-reads every round log: a scoring answer proves all its words are
members; a failing answer proves at least one is not.  Mean-field belief
propagation over those constraints gives a posterior per word; `strategy.py`
uses confirmed members first and rotates fresh candidates through the unsolved
(letter,length) slots.  Coverage compounds: each confirmed slot raises the odds
that a whole answer is all-members, which confirms more slots.

confirmed slots: 19 (r3) -> 42 (r4) -> 53 (r5) -> 59 (r6, of 135).
Letters e, g, p, r, w never bootstrapped.

## Demos are not trustworthy
3 demos taken.  Only the first (`p664`) has a solution whose word lengths fit the
clue shown.  `s826 -> shining sack suspend` (lengths 7/4/7, needed 9/3/7) and
`h3452 -> heroic health human hail` (lengths 6/6/5/4, needed 4/5/6/3) do not fit,
and `human` is provably rejected in a real round (`h342 -> have human his` = 0).
Demo clue and demo solution look like they come from two different draws.
They were demoted to hints (prior 0.5) rather than facts.
