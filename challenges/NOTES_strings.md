# Brainstorm: strings, words & text (strings-agent)

12 candidates. Format: NAME — clue → what scores 1 — why fun/tractable — discovery path.

1. **RUNIC** — clue `aaabbbbc` → canonical run-length encoding `3a4b1c` — verify = re-expand +
   "adjacent group letters differ" (unique answer); a 6-line solver. Discovery: one demo shows
   digits+letters that expand to the clue. EASY. *(chosen)*
2. **CRIBROT** — clue `ct|crib` → any Caesar rotation of `ct` that contains `crib` (generator
   guarantees exactly one) — verify = "all (ord diffs mod 26) equal" + crib substring, ~145 chars;
   solve = 26 rotations. Demo shows readable English → instant aha. EASY. *(chosen)*
3. **ANAPAL** — clue `letters|w` → a palindrome that is an anagram of `letters` and contains `w`
   — verify = 4 terms, ~110 chars; solve = place w at each offset, mirror, fill leftovers.
   Two constraints interact, so partial hypotheses ("palindrome", "same letters") give a gradient.
   MEDIUM. *(chosen)*
4. **TWINE** — clue `A|B|L` → a common subsequence of A and B of length exactly L (= LCS length)
   — verify = iterator-consumption subsequence trick, ~135 chars; solve = DP + traceback.
   Greedy gets some instances right → nice gradient. MEDIUM. *(chosen)*
5. **DUOMASK** — clue `re1 re2` → any string ≤16 chars matching BOTH regexes (fullmatch) — verify
   = two `re.fullmatch`, ~110 chars; solve = BFS over {a,b}* up to |w|. The trap is fullmatch vs
   search, and realising both must hold. MEDIUM-HARD. *(chosen)*
6. **ALLWIN** — clue `ab 4` → a cyclic de Bruijn sequence B(k,n): length k**n, every n-window once
   — verify = set of rotated windows, ~155 chars; solve = FKM/Lyndon, <1 ms. Big aha, all-or-
   nothing per item. HARD. *(chosen)*
7. **NOFIX** — clue = a word → an anagram with no letter left in its original position (a
   derangement). Scorer `sorted(s)==sorted(c) and all(a!=b for ...)` ~100 chars. Cute but very
   close to ANAPAL in flavour; kept in reserve.
8. **NONCE** — clue `sha1|3f2|SALT` → any s with `sha1(SALT+s)` starting with the prefix. Scorer
   ~120 chars; solve = brute force 4096 tries (~4 ms). Fun "mining" feel, but it is guess-the-hash
   -function rather than a string idea, and rewards nothing partial. Reserve.
9. **VIGCRIB** — Vigenère with stated key length: verify = "ord-diff sequence is periodic with
   period L" + crib present (~180 chars). Harder version of CRIBROT; dropped only to keep one
   cipher in the set.
10. **PALSUB** — clue `text|L` → a palindromic substring of `text` of length L. Scorer ~90 chars,
    but too close to trivial and overlaps ANAPAL.
11. **XBRACE** — clue = bracket string with `X` wildcards → fill the X's so the whole string is
    balanced over `()[]{}`. Scorer needs a repeated-`replace` reduction loop (~200 chars, O(n²)
    but n≤120 so still <50 ms). Good puzzle; lost to DUOMASK on diversity (both are
    constraint-satisfaction searches).
12. **ISOMORF** — clue = a word-pattern → a same-length string with the identical repetition
    pattern sharing no letters with the clue. Scorer `[c.index(x)for x in c]==[s.index(x)for x in s]`
    is delightful and short, but the solve is a one-liner: too easy even for the easy tier.

## Rejected because of the 256-char scorer cap
* **String rewriting / MIU / Post systems** (clue = start, target and 2–3 rewrite rules; solution =
  the derivation). Replaying a derivation needs a parse of the rule list plus an apply-at-position
  loop: ~450 chars minimum. Would be a superb hard challenge at a 512-char cap.
* **Edit distance to a target k** — the Levenshtein DP alone is ~200 chars, leaving no room for the
  second constraint that stops the answer being "append k letters", so the puzzle degenerates.
* **Word search in a letter grid** (clue = grid + word; solution = coordinates+direction): grid
  parse + 8-direction walk + bounds ≈ 300 chars. Also overlaps the grids direction.
* **Dictionary-backed anything** (real-word anagrams, crosswords, hangman): the scorer cannot see a
  word list and a 1024-char clue cannot carry one, so "is it a real word" is unverifiable. Only
  works if the clue itself ships the candidate list, which gives the answer away.
* **Vigenère without a stated key length / unknown-alphabet substitution ciphers**: verifying
  "decrypts to English" needs a language model or dictionary; verifying "some key exists" needs the
  key search inside the scorer.
