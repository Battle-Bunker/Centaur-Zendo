# Centaur Zendo — team grace — solved rule book

All 31 classes solved (round 12: 772/772 presented/correct, 0 skips).
Answer formats below are the ones the server accepts (verified by scoring).

| class | rule | answer format |
|---|---|---|
| AHMES | Egyptian fraction (greedy) of n/d | denominators, space-sep: `2 3 8` |
| ALLWIN | de Bruijn sequence B(k,n) over alphabet | the cyclic sequence, k^n chars |
| ANAPAL | rearrange s into a palindrome containing t as substring | the palindrome |
| BASILISK | `digits:from>to` base conversion | digits in target base |
| CHAKRA | Pell equation x^2 - N y^2 = 1 (chakravala) | `x y` |
| CRIBROT | Caesar cipher, crib = known plaintext | the decrypted plaintext |
| DUOMASK | string matching BOTH regexes | shortest such string over {a,b} |
| GRAYLING | simple path in hypercube a->b of exactly n bit flips | states space-sep incl. endpoints |
| HAIL | clue = Collatz total stopping time | smallest n with that step count |
| HANSOM | Manhattan TSP cycle within budget | point indices, space-sep |
| IDX | discrete log ("index"): g^x = h mod p | x |
| MARIENBAD | Nim, make the xor zero | the resulting pile sizes |
| PP | smallest palindromic PRIME containing the clue digits | that prime |
| RUNIC | run-length encode | `6c2f9d` (count then char) |
| SPQ | semiprime-ish factoring | smallest prime factor |
| SUNZI | CRT: `a%m a%m ...` | smallest non-negative x |
| TARE | subset summing to target | binary mask, one char per item |
| TOPPLE | make target from the 4 digits | **RPN/postfix** string, e.g. `954*9-*`; avoid `/` (rejected) |
| TWINE | longest common subsequence (length given) | the LCS string |
| carre | 4x4 LATIN square (no 2x2 boxes!) | rows joined by `/` |
| erewhon | Game-of-Life PREDECESSOR (non-wrapping) | grid, rows joined by `\n` |
| hanjie | nonogram (rows `\n` cols, groups `/`) | grid rows joined by `\n` |
| ikos | Hamiltonian cycle (path fallback) | node list, space-sep |
| krom | SAT, clauses `l,l,l` space-sep | bit string per variable, `0011...` |
| regina | N-queens on a board with X = blocked cells | digit string: out[col] = row |
| skerry | count 4-connected `#` islands | the count |
| trico | proper 3-colouring | digit string of colours, no separator |
| volute | read grid in clockwise spiral from top-left | the letters |
| warren | maze S->E shortest path | direction string `UDLR` |
| wolf | deduce Wolfram elementary CA rule (wrap-around) | rule as **8-bit binary** |
| zebu | A-E ordering; `<` before, `|` adjacent, `#` at position | letters in position order |

## Demos used (7 of 12)
IDX, erewhon, PP, trico, TARE, TOPPLE, regina, ANAPAL, CHAKRA — each on a class no
amount of self-play was going to disambiguate (unknown rule, not just format).
Format-only ambiguities were resolved for free by cycling 2-6 answer formats within
a single round (variant = i-th occurrence of that class % k) and reading per-variant
hit-rates out of the round log.
