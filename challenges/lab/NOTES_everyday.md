# Brainstorm — everyday-object semantics, laterally encoded (everyday-agent)

Direction: the clue is tiny; the rule depends on reading it through a **real-world object a
kid knows** (clock face, keypad, dice, dominoes, seven-segment display, calendar grid,
tally marks, calculator). The scorer embeds the tiny table the object implies. Difficulty
must come from the lateral *reading*, never from search or arithmetic.

Design constraints I applied to every candidate:
* **Construction, not lookup.** A rule that is a bijective symbol map (`2 -> ABC`,
  calculator letters) is cracked forever by one demo and is then rote. The answer has to be
  something the player *builds*, whose validity depends on the object's geometry.
* **Probe-resistant.** Players get ~450 graded probes per 0.5 s round (~2,700 over 6
  rounds). Any rule whose table can be reconstructed by probing one symbol at a time
  (single-digit answers, single-cell answers) is a lookup in disguise. Minimal witnesses
  must score 0 so the format itself has to be discovered before probing can start.
* **Ambiguous demos.** `solve()` must never emit the minimal or canonical witness, and must
  randomise which instances of the object it uses, so that one demo admits many hypotheses
  and it takes 3-4 to triangulate (the LegoZendo profile).

## Candidates

1. **Seven-segment growth pairs** (PICKED, implemented as `quilm`).
   Everyday object: the digits on a microwave / alarm clock / calculator, and "how many
   matchsticks do I add to turn this digit into that one". Clue `"N K"`. Answer: two
   K-digit strings `X Y`; every digit of Y must be the corresponding digit of X *with more
   segments lit* (mask superset, strictly), and exactly N segments are added in all.
   Table: ten masks, 32 chars in the scorer. Construction: the player has to distribute N
   over K digits using the per-digit growth options (gains 1..5 exist, but only from
   specific digits), so it is a real build, not a lookup. Minimal witnesses closed: K >= 3,
   strict growth per digit kills `X == Y` and padding with equal digits, and N >= K+2 kills
   the degenerate "all 1s -> all 7s" family that needs only one fact about the display.
   Fingerprints that make it fair: 8 never appears in X, 1 and 2 never appear in Y.

2. **Phone-keypad walk.** Clue `"d N"`; answer: a digit path starting at d whose consecutive
   digits are physically adjacent on the 3x3+0 pad, all distinct, digit sum N.
   Rejected: "adjacent on a phone keypad" is a top-three hypothesis for any digit-adjacency
   puzzle (knight-dialer is folklore), so the lateral step is barely a step. Kept as the
   fallback if the segment idea proves too hard.

3. **Die-tipping sequence.** Everyday: opposite faces of a die sum to 7, so when a die is
   tipped the new top face is neither the old top nor its opposite. Answer: a face sequence
   with `a != b` and `a + b != 7` for neighbours, total N. Rejected: a random sequence
   satisfies the local constraint most of the time, so blind probing yields 1s and the rule
   leaks without the die reading; and the "table" is a single arithmetic fact.

4. **Calendar month grid.** Clue `"L f"` (month length, weekday of the 1st); answer: a set of
   dates forming an edge-connected blob in the month grid (adjacency = +/-1 in the same week
   row, or +/-7). The lateral bit is that the grid is *ragged*: the 7th and 8th are not
   neighbours if the 7th ends a week row. Rejected for this pass: the interesting part is
   exactly LegoZendo's connected-blob shape (duplicate mechanic), and the uninteresting part
   degenerates to plain mod-7 arithmetic, which a model reaches without any calendar reading.

5. **Calculator upside-down words (beghilos).** Clue: a word over `{B,E,G,H,I,L,O,S,Z}`;
   answer: the number that spells it when the calculator is turned over. Rejected: a
   bijection, therefore one demo and done; and the clue's restricted alphabet is a loud
   tell. Reconsidered as "a *prime* that flips to the clue word" — but the flip is still a
   bijection, so the number is determined and the primality is decoration.

6. **Upside-down digital clock.** On a seven-segment display 0,1,2,5,8 read as themselves
   rotated 180 deg and 6/9 swap (2 -> 2 is true on a display and false in print — a lovely
   discriminator). Answer: a time that is still a valid time when the clock is read from the
   other side of the bed, N minutes from the clue time. Rejected as *composed of two*
   lateral leaps (rotation table + time arithmetic with a 24 h wrap) — likely "too hard",
   and it shares the segment table with candidate 1, which is the cleaner build.

7. **Tally marks (five-bar gate).** Clue N; answer: the ASCII tally. Rejected: the drawing
   is essentially determined by N, so it is a rendering exercise, and an ASCII scorer eats
   the 512-char budget for a one-bit insight.

8. **Piano keyboard.** White keys with no black key between them (E-F, B-C); answer: a
   sequence of key letters obeying the pattern. Rejected: reads as music theory (a named
   body of knowledge) rather than as an everyday object, and the table is two facts.

9. **Shifted number row (`1 -> !`, `2 -> @`).** Rejected: the clue would contain the
   symbols, which announces the object instantly; and it is another bijection.

10. **Braille cells.** a-j, then k-t = a-j plus dot 3, u-z = plus dots 3 and 6. Genuinely
    lateral and a real construction (build a word whose cells differ by given dots), but the
    table is 26 entries, the "kid recognises it" test is weak, and the scorer will not hold
    the table plus the checks in 512 chars.

11. **Elevator panel that skips 13.** Cute, one fact, no construction. Rejected.

12. **Domino chain from a double-six set.** Rejected by the loop's own rule: dominoes are a
    named puzzle object with a textbook (Eulerian) solution.

## Picked: 1, named `quilm`

Intended discovery path: demos show two same-length numbers, the second always "fatter"
(8 and 9 common on the right, 1 and 2 absent on the right, 8 absent on the left). The player
must ask *what makes 1 -> 7, 3 -> 9, 5 -> 6, 0 -> 8 the same kind of move* and land on the
digital display; the second clue number then reads as the count of added segments, and K as
the digit count. Without the display reading there is nothing to build; with it, a greedy
composition of N into K parts solves every instance in microseconds.

---

## Iteration 1 — build + self-test (done), arena live, players NOT run

`challenges/lab/quilm.json`: score 327 chars (cap 512), solve 1288, generate 154;
gen 0.02 ms, score 0.05 ms, solve 0.08 ms; `quickcheck --seeds 200` = OK, no warnings.
Clue space = 50 distinct clues (K in {3,4,5,6}, N in [K+2, 4K]); every one is solvable and
`solve()` scores 1 on all 50. A player who has the insight answers with a greedy
composition in 0.006 ms, 50/50 — so the class is fully winnable at final speed.

Adversarial witness audit (50/50 clues, all score 0 unless noted):
empty, whitespace, the clue, the clue reversed, "0", "1"*100, "1 8", "111 111",
all-1s->all-7s (both lengths), all-1s->all-8s, all-0s->all-8s, constant "111 888" /
"1111 8888", the clue's own digits, X padded with unchanged digits, K+1 digits, the
demo answer with the two halves swapped, comma-separated, space-removed, extra token.
Blind random same-shape guessing hits 0.015 % (3/20000). Only genuine acceptances:
whitespace-tolerant separators (newline instead of space — deliberate kindness) and
digit-permutations of a demo answer for the *same* clue (harmless; useless for other clues).

Known shortcut, deliberately left in for iteration 1: a player who knows only the growth
options of the digit **1** (1->7 +1, 1->4 +2, 1->3 +3, 1->9 +4, 1->8 +5) solves 50/50 with
X = "1"*K. That shortcut *is* the seven-segment insight applied to one glyph, so it is not
a way around the lateral reading — but it is also the target of a grind attack: once a demo
reveals the "K digits, space, K digits" shape, ~450 probes/round could enumerate "111 ???"
and recover the gains empirically. Ready hardening for v2 if both players crack it:
**require the digits of X to be pairwise distinct** (kills the all-1s family, forces growth
options for >=3 glyphs; generate then needs a feasibility check because gains per glyph are
0:{1} 1:{1..5} 2:{2} 3:{1,2} 4:{2,3} 5:{1,2} 6:{2} 7:{2,3,4} 9:{1}).
Ready softening if neither player gets anywhere: restrict K to {3,4} and make `solve()`
always include one 1->8 and one 0->8 in the same answer, so the "add strokes to the glyph"
pattern is loud in a single demo.

Arena for iteration 1 is set up and running (ws://127.0.0.1:35521/ws, pool = quilm only,
6 rounds / 0.5 s / 5 s cooldown). **No Agent/Task tool is available in this session**, so
per sim/DESIGN_LOOP.md I stopped at step 3; see sim/results/lab-quilm-1/HANDOFF.md.

---

## Iteration 1 — RESULT: both players cracked (too easy)

| player | rounds (correct/answered) | final | demos | cracked |
|---|---|---|---|---|
| quilma | 2/516, 3/486, 15/405, 493/493, 493/493, 486/486 | 3030/3030 (100 %) | 4 | round 4 |
| quilmb | 0/0, 0/494, 1/502, 14/418, 100/590, 468/468 | 2579/2579 (100 %) | 6 | round 6 |

Both believed the exact rule. The two attacks that did it:
* **Identification scan (quilma).** v1's accept condition was `property(answer) == clue number`,
  an *absolute* readout. Submitting a FIXED answer against every clue is therefore an oracle
  for that property: whichever clue accepts it announces `F(answer)`. Near-identical fixed
  answers (`0011 8888` -> 12 vs `0111 8888` -> 16) then differenced out the per-position
  weights, which matched seven-segment popcounts.
* **Cross-clue equations (quilmb).** 50 distinct clues made demo answers reusable and let
  single-digit edits of a known-good answer be read as simultaneous equations (weights 2,4,6).
  They also used the `X = "1"*K` shortcut I had flagged and left in.

Diagnosis: the leak was **structural, not cosmetic**. Any rule of the form "some absolute
number computed from the answer equals the clue" is scan-solvable, whatever the object is.
Closing the `"1"*K` witness alone would not have helped.

## Iteration 2 (`quilm` v2, live) — same object, relational rule

Kept: the seven-segment display, i.e. the everyday reading is still "these digits are glyphs
made of little bars". Changed: **the clue is now a partial object the answer must be built
against, not a target number.**

Clue `X/N` (X = 3..6 digits, N = 1..4). Answer: a number Y of the same length reached by
switching exactly N segments OFF and exactly N ON across the whole display — *move exactly N
matchsticks and read the new number* — and Y must not be a rearrangement of X's digits.

Why this answers each attack:
* **Scan is dead.** Validity is relative to the clue, so a fixed answer is accepted only for
  the rare clue it happens to fit and yields no readout. Measured on 3000 clues: all-8s
  0.0 %, all-1s 0.0 %, constant string 0.0 %, all-0s 1.2 %, random same-length string 0.8 %.
* **Memorisation and cross-clue equations are dead.** Clue space ~10^k x 4 (2899 distinct in
  3000 draws) instead of 50; a demo answer is worth exactly one challenge.
* **Every v1 shortcut is dead.** The on/off counts must be *equal*, so anything that only
  adds segments (all-8s, X = "1"*K, "grow every digit") scores 0. A lone `1->7` now has to be
  paid for by a removal elsewhere in the number, which is the balance clause in miniature.
* **The one blind family the audit found is closed.** Permuting X preserves its segment total
  for free, so `X` reversed / sorted / randomly permuted scored ~11 % with no insight and
  handed out labelled equations; the non-rearrangement clause takes all of those to 0.0 %.

Residual signal, left in deliberately as the fairness floor: a random single-digit edit of the
clue is accepted 2.6 % of the time, so a player who probes that way collects ~12 labelled
positives a round and can start fitting "which digit swaps cost 1, which cost 2". That path
tops out at **40.5 %** (the ceiling for answers that change only one digit); getting past it
needs the balance rule, i.e. two compensating edits, which reaches **98.4 %**. A player with
the full insight scores 100 % at 0.053 ms per answer. That gradient should separate "learned
the swap table" from "read the object" in the final score.

Difficulty gradient by clue: N=1 (13.6 % of clues) often falls to a single same-count swap
(0<->9, 2<->3, ...); N=3,4 needs the budget spread over two or three digits.

Validation: score 337 chars (cap 512), solve 2006, generate 1870; `quickcheck --seeds 200` OK,
no warnings; worst case over 3000 seeds gen 0.24 ms / solve 0.26 ms / score 0.04 ms (0.0004 ms
on 4 KB junk); `solve()` scores 1 on all 3000 and generate is deterministic. Demo answers
change 1..5 digits (mode 2), so no canonical shape leaks.

Arena for iteration 2: run `lab-quilm-2`, `ws://127.0.0.1:36625/ws`, teams quilm2a / quilm2b,
6 rounds / 0.5 s / 5 s cooldown / 3 s final. Briefs: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/BRIEF_quilm2a.md`, `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/BRIEF_quilm2b.md`.
v1 is kept as `challenges/lab/quilm.v1.json` for the record.

If iteration 2 comes back "both cracked" again, the next lever is **composition**: keep the
move rule and add a second everyday clause the demos cannot show negatively — e.g. Y must
also read as a valid clock time, or the moved sticks must all come from one digit. If it comes
back "neither cracked", soften by fixing N=1 for a third of clues and letting `solve()` prefer
single-digit moves, which makes the 0<->9 / 2<->3 tell louder in a single demo.
