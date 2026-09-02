# Centaur Zendo — team ada — solved rule book

All 31 classes solved. Rounds 9-12 scored 100% (690/690, 824/825, 771/771, 797/797).
Answer-format variants are pinned in `strategy.py:FORCE`; solvers in `solvers.py`.

| name | clue | rule | answer format | conf |
|---|---|---|---|---|
| AHMES | `7/32` | greedy Egyptian fraction | denominators, space sep: `5 54 4320` | certain |
| ALLWIN | `ab 5` | lex-least de Bruijn B(k,n) | cyclic string, length k^n | certain |
| ANAPAL | `L\|R` | palindromic anagram of L containing R (prefix when possible, then rest sorted) | the palindrome | certain |
| BASILISK | `100340:5>7` | base conversion | digits, lowercase | certain |
| CHAKRA | `91` | Pell x²−Dy²=1 (chakravala) | `x y` | certain |
| CRIBROT | `vwudsvkhhseodph\|strap` | Caesar shift found via the crib | plaintext | certain |
| DUOMASK | two regexes | shortest string matching BOTH | the string | certain |
| GRAYLING | `a b k` | self-avoiding hypercube path a→b of length k | states space sep | certain |
| HAIL | `47` | smallest n whose Collatz stopping time == clue | that n (`246`) | certain |
| HANSOM | pts`\|`budget | Manhattan TSP tour within budget | point indices space sep | certain |
| IDX | `g h p` | discrete log (index) g^x≡h mod p | x | certain |
| MARIENBAD | `15 13 1 13` | Nim winning move | resulting position, space sep | certain |
| PP | `645` | smallest palindromic PRIME containing the clue | `9645469` | certain |
| RUNIC | `ccaaa...` | run-length encode | `2c9a3c...` (count first) | certain |
| SPQ | `40079396887` | semiprime factorisation | the SMALLER prime factor only | certain |
| SUNZI | `38%79 27%43` | CRT (Sunzi) | least non-negative x | certain |
| TARE | nums`\|`target | subset sum | 0/1 bitmask, one char per item | certain |
| TOPPLE | `6652=58` | build the target from all digits, ops + - * (NO division) | reverse Polish, no spaces: `566+*2-` | certain |
| TWINE | `a\|b\|k` | longest common subsequence (k = its length) | the LCS string | certain |
| carre | `231./.../...` | 4x4 Latin square (not sudoku boxes) | rows joined by `/` | certain |
| erewhon | 6x6 grid | **reverse Conway's Life**: lex-least predecessor state ("nowhere" backwards) | grid, rows joined by `\n` | certain |
| hanjie | row clues `\n` col clues | nonogram | grid rows joined by `\n` | certain |
| ikos | `n` + edges | Hamiltonian PATH (not cycle) | vertices space sep | certain |
| krom | 3-literal clauses | SAT | bit string per variable, e.g. `0000100000` | certain |
| regina | grid, X = blocked | n-queens avoiding X | **row index per COLUMN**, concatenated, lex-least | certain |
| skerry | grid | count `#` components, 4-connectivity | the count | certain |
| trico | `n` + edges | 3-colouring | digits `1..3` concatenated | certain |
| volute | letter grid | read in clockwise spiral from top-left | the string | certain |
| warren | maze with S,E | shortest path | `UDLR` uppercase | certain |
| wolf | `state>next` pairs | infer the elementary CA rule (cyclic boundary) | rule as 8-bit binary MSB-first | certain |
| zebu | `B#3 A<B B\|E` | 5 letters A-E get distinct 1..5; `#`=equals, `<`=less, `\|`=adjacent | letters in ascending value order, e.g. `DABEC` | certain |

## Demos spent (8)
PP, TOPPLE, TARE, HAIL, ANAPAL, erewhon, regina, regina(2nd).
Each was spent on a class where the *rule* (not just the format) was unknown; format
ambiguity was resolved for free by the variant-rotation machinery below.

## Method
`strategy.py` picks an answer-format variant per class deterministically from a hash of
the clue, so scores can be attributed to variants in `on_round_end`; a variant that ever
scores 1 is locked. That resolved 24 of 31 classes in a single round without a demo.
