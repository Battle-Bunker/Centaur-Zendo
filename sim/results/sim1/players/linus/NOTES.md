# Centaur Zendo — challenge rules (all 31 solved, 100% hit-rate)

| name | rule | answer format | confidence |
|---|---|---|---|
| AHMES | Rhind papyrus: greedy Egyptian-fraction expansion of a/b | denominators, space-separated ("2 22") | certain |
| ALLWIN | "all windows" = de Bruijn sequence B(k,n) over given alphabet | cyclic sequence, length k^n | certain |
| ANAPAL | rearrange s1 into a palindrome containing s2 as a substring | the palindrome | certain |
| BASILISK | base conversion `num:from>to` | digits, lowercase | certain |
| CHAKRA | chakravala: Pell x^2-N y^2=1 fundamental solution | "x y" | certain |
| CRIBROT | Caesar/rot cipher, second field is a crib word | decoded plaintext | certain |
| DUOMASK | find a string over {a,b} matching BOTH regexes | the string | certain |
| GRAYLING | hypercube walk a->b of exactly n single-bit flips (self-avoiding) | states space-separated | certain |
| HAIL | hailstone: given total stopping time n, smallest start with that time | the number | certain |
| HANSOM | hansom cab = taxicab TSP tour within budget | point indices in tour order, space-sep | certain |
| IDX | "index" = discrete logarithm: g^x = h (mod p), clue "g h p" | x | certain |
| MARIENBAD | Nim winning move | resulting heap sizes, space-separated | certain |
| PP | smallest palindromic prime containing the clue as a substring | the prime | certain |
| RUNIC | run-length encoding | "4a1e12a..." count-then-char | certain |
| SPQ | semiprime n=p*q, factor it | either prime factor | certain |
| SUNZI | Sunzi/CRT simultaneous congruences "a%m ..." | smallest x | certain |
| TARE | subset-sum to target | bitmask string, 1=selected | certain |
| TOPPLE | "toppled Polish" = RPN expression from the 4 digits (any order), ops + - * only | RPN string e.g. "1431+*+" | certain |
| TWINE | longest common subsequence (length given) | the LCS string | certain |
| carre | Latin square completion | rows joined by "/" | certain |
| erewhon | Game of Life PREDECESSOR of the given 6x6 grid | grid, rows joined by newline | certain |
| hanjie | nonogram (row clues \n column clues) | solved grid, newline-joined | certain |
| ikos | icosian = Hamiltonian PATH (not cycle) | vertex order, space-separated | certain |
| krom | 3-SAT satisfying assignment | bit string, var 1..n | certain |
| regina | n-queens avoiding X-blocked cells | row of queen per column, digit string | certain |
| skerry | count 4-connected islands of '#' | the count | certain |
| trico | 3-colouring of the graph | digits 0-2 per vertex | certain |
| volute | read grid in clockwise spiral | the letters | certain |
| warren | maze shortest path S->E | direction string in UDLR | certain |
| wolf | Wolfram elementary CA (wrap-around); identify the rule | 8-bit binary rule string | certain |
| zebu | zebra-style CSP, A-E over 1..5; `<`=less, `|`=adjacent, `#`=equals | letters ordered by value, e.g. "BACDE" | certain |

## Method
Round 1 random -> classify by name pun + clue shape. Then each solver returned a LIST of
candidate output formats and the dispatcher rotated through them by a per-name counter,
so a single round A/B-tested 5-7 formats for every class at once; the log told me which
index scored 1. Demos (4 used: PP, TOPPLE, regina, erewhon) were spent only on classes
whose *rule* was unknown, never on formats.
