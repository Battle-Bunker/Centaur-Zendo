# Brainstorm: number theory & arithmetic challenges (numbers-agent)

Scratch notes. Format: NAME — clue — scores 1 — why fun/tractable — how guessable.

1. **SUNZI** (Sun Zi / CRT) — clue `1%3 4%7 2%5` — x with x%m==r for all pairs and 0<x<prod(m) — classic CRT, unique answer, brute force also works — clue's `%` is a huge hint; demo nails it. **PICKED (easy)**
2. **HAIL** (hailstone) — clue `37` — n whose Collatz total stopping time is exactly 37 — famous sequence, memoised search is instant — demo shows small k -> bigger n; AI recognises 3n+1. **PICKED (easy)**
3. **SPQ** (p·q) — clue `104729003` — any nontrivial divisor — verify in 3 lines, find needs trial division/Pollard; mixed factor sizes give a real gradient — demo: clue is a big number, answer divides it. **PICKED (medium)**
4. **AHMES** (Rhind papyrus) — clue `5/13` — ≥2 *distinct* unit-fraction denominators summing exactly to p/q — Egyptian fractions, greedy works, cute — demo reveals `3 30 65`-style answers; sum check is the aha. **PICKED (medium)**
5. **CHAKRA** (chakravala) — clue `61` — `x y` with x²−D·y²=1, y>0 — Pell; tiny scorer, brute force works for small D but explodes at 61/109/151 → gradient — demo on D=61 shows two giant numbers. **PICKED (hard)**
6. **IDX** (index = discrete log) — clue `5 1234 100003` — x with g^x ≡ h (mod p) — one `pow` verifies, BSGS needed to find; naive loop wins some — demo makes the pow relation checkable. **PICKED (hard)**
7. **ZECK** (Zeckendorf) — clue `n` — non-consecutive distinct Fibonacci numbers summing to n — nice, but scorer must rebuild the Fibonacci set *and* check non-adjacency; ~300 chars. **REJECTED: scorer cap.**
8. **TOT** (Euler φ) — clue `m` — n with φ(n)=m — φ in 256 chars means an O(n) gcd loop (too slow) or a factorisation (too long). **REJECTED: scorer cap/time.**
9. **DIVK** — clue `k m` — n>m with exactly k divisors — scorer is a sqrt divisor count, fits; fun but similar flavour to SPQ. Backup.
10. **VAMP** (vampire numbers) — clue `d` — n=a·b, digits of a‖b a permutation of n's — scorer needs sorted-digit compare + length rules, ~230 chars, but overlaps the string/word direction. **REJECTED: overlap.**
11. **BIPAL** — clue `b1 b2 m` — n>m palindromic in both bases — scorer needs two base conversions (~230 chars, tight) but overlaps PP's palindrome idea. **REJECTED: overlap with PP.**
12. **PERS** (multiplicative persistence) — clue `k` — smallest n needing k digit-product steps to reach one digit — "smallest" is unverifiable in the scorer, and without it the answer is trivial for small k. **REJECTED: not verifiable from clue alone.**
13. **ABC** (abc-triples, rad(abc)<c) — needs a factorisation-based radical inside the scorer. **REJECTED: scorer cap.**
14. **AMIC** (amicable pairs) — σ(a)=b, σ(b)=a — two O(n) divisor-sum loops; borderline on the 50 ms score cap and ~200 chars. Backup.
15. **SOS3** — sum of three squares (n ≢ 4^a(8b+7)) — scorer trivial, but so is the search; too easy and close to CHAKRA in feel. Backup easy.

## Chosen six (2 easy / 2 medium / 2 hard)
SUNZI, HAIL (easy) · SPQ, AHMES (medium) · CHAKRA, IDX (hard)

Design rules I kept to:
* clue carries everything the scorer needs (no hidden channel);
* scorer never raises on junk — every one guards `len`/`isdigit` before `int`;
* the clue itself never scores 1 (checked; HAIL resamples the Collatz fixed point k=5);
* every challenge has a "naive bot gets a subset" gradient (small D in CHAKRA, small p in
  IDX, small factors in SPQ, brute-force range in SUNZI, memoised scan in HAIL,
  two-term fractions in AHMES).
