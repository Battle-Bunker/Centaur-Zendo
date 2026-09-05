# NOTES — rule-family class, world = 4–7 letter common English words (`tavrik`)

Paradigm: `docs/RULE_FAMILIES.md`. A finite universe **U** of parametrised rules; the clue is a
minimal set of positive example words that pins exactly one rule of U; the answer is one more real
word obeying it. The player does **not** know U, so their (much larger) hypothesis space is full of
obvious word rules the class never uses. Learning **what this class never asks about** is the game.

Shipped file: `challenges/lab/tavrik.json` (name checked unique against `challenges/` and
`challenges/lab/`). Lessons copied from `dornic` (cards) and `borsel` (dice): U must be an
**antichain**, the **template is drawn uniformly before the parameter**, a **"not a one-change
copy"** clause kills the cheapest witness, the best traps are the **loose cousins** of the
templates that are used, and `score` stays ≤ 1024 chars.

---

## 1. The world

An instance is **one lowercase English word of 4–7 letters**, one per line.

* **Clue** = 2 or 3 example words (one per line, nothing else).
* **Answer** = one more word of 4–7 letters that `words.is_word` accepts, obeying the hidden rule,
  and **not within one letter of any example** (see §5). Case and surrounding spaces are forgiven.
* Example pool = the first 5000 4–7-letter entries of `words.COMMON` (frequency-ordered), minus
  499 dropped words → **4501 words**. The drop list is in the source: 473 proper nouns (john,
  april, texas, michael…) that `wordfreq`'s list is full of and that the sandbox cannot detect on
  its own (`words.WORDS` is lower-cased, so "april" and "apron" look alike), plus 26 words no
  school wants in a clue. Clue words are therefore words a 12-year-old knows.
* The **answer** may be any dictionary word (`words.WORDS`, 56 176 of length 4–7), not just a
  common one — the scorer is generous about vocabulary and strict about the rule.

Everything the scorer needs is in the clue: it re-derives the rule by enumerating U and filtering
on the examples (SPEC §2, no hidden channel).

---

## 2. The universe U — 10 templates, 25 rules

"density" = fraction of the 4501-word pool satisfying the rule = **what a player who answers with
a random word scores when this rule is the truth**. Mean density of the hidden rule: **0.080**.

| # | template (kid sentence, one breath) | parameter grid | density | in U? |
|---|---|---|---|---|
| 0 | "the word has exactly *n* vowels" | n = 1, 3, 4 | .220 / .220 / .020 | **IN** |
| 1 | "it has a double letter" (two of the same letter side by side) | — | .158 | **IN** |
| 2 | "it starts and ends with the same letter" | — | .046 | **IN** |
| 3 | "it starts with a vowel" | — | .132 | **IN** |
| 4 | "its letters are in alphabetical order" | — | .016 | **IN** |
| 5 | "it has a *c* in it" | c ∈ b f k m p v w | .107 .088 .077 .141 .149 .070 .078 | **IN** |
| 6 | "it ends with *c*" | c ∈ d g l n r s t y | .091 .061 .063 .068 .092 .046 .114 .101 | **IN** |
| 7 | "it has a j, q, x or z in it" | — | .048 | **IN** |
| 8 | "it only uses three different letters" | — | .047 | **IN** |
| 9 | "some letter turns up three times" | — | .023 | **IN** |

|U| = 25 over 10 templates. `generate` draws the **template uniformly** and only then the
parameter, so the seven single-rule templates are each ~10 % of clues and the two big letter
families are ~10 % between all their letters (measured template mix over 500 clues:
.074 .120 .122 .108 .108 .102 .080 .104 .086 .096).

### Why U is an antichain
Positive examples can never separate a rule from a **weaker** rule containing it. Checked by brute
force: over the 4501-word example pool **and** over all 56 176 dictionary words of length 4–7, no
rule of U is a subset of another, and every rule has ≥ 419 dictionary instances. This is what
forced several of the choices above:

* the **contains-*c*** grid and the **ends-with-*c*** grid are letter-disjoint — "ends with y" ⊂
  "contains a y" would have been a nested pair;
* the ends-with grid holds **no vowels**, because "ends with e" ⊂ "ends with a vowel" (so
  "ends with a vowel" is out of U altogether, and is a trap instead);
* "all the vowels are the same letter" (.303) contains "exactly one vowel" — dropped;
* "no letter is repeated" (.560) contains "the letters are in alphabetical order" whenever the
  word has no double — dropped (and it is the single most obvious word rule, so it became a trap);
* "some letter turns up three times" and "only three different letters" are *not* nested
  (checked): `session` has three s's and five different letters; `level` has three different
  letters and no letter three times.

### Templates measured and thrown out
| template | density | why not |
|---|---|---|
| "it has *n* letters" (n = 4..7) | .197–.287 | **the** obvious hypothesis; kept out so it can be a trap (§3) |
| "no letter is repeated" | .560 | too loose, nests with #4, and it is the classic Zendo word rule → trap |
| "the second letter is a vowel" | .641 | too loose → trap |
| "more consonants than vowels" | .768 | a *comparison*; this class only ever makes tight statements → trap |
| "two vowels side by side" | .244 | loose, and half the clues fit it by accident → trap |
| "it ends with a vowel" | .236 | loose and nests with the ends-with grid → trap |
| "exactly 2 vowels" | .536 | far too loose (cut from template 0's grid) |
| "exactly 4/5/6 different letters" | .261/.330/.271 | too loose; only "three different letters" survives |
| "it has an e / a / s / t / r / n / i / o / c / l in it" | .20–.55 | too loose; **only b f k m p v w are ever used** — "they all have an e" is never the answer |
| "the letters are in *reverse* alphabetical order" | .010 | only ~45 pool words: the generator needs ≥ 12 instances to build a minimal set, and it duplicates #4's idea |
| "the same vowel twice or more and no other vowel" | .106 | good density, but it takes two breaths to say |
| "exactly *n* consonants" | .125–.381 | a second counting family adds no new idea |
| "it rhymes with…", "it is a plural", "it is an animal" | — | meaning and sound are not decidable from letters; the class is purely about spelling |

---

## 3. The exclusions — what the class never asks (the traps)

Never in U, deliberately. **fits** = the trap, fitted to the clue, is consistent with *every*
example (so a player who forms it is never contradicted); **score** = a player who always answers
with an instance of it scores this over all 500 clues; **when played** = its score on the clues
where it fits.

| excluded rule (fitted to the clue) | why a player reaches for it | fits | score | when played |
|---|---|---|---|---|
| "the answer contains every letter the examples share" | *the* first thing anyone tries: what do these words have in common? | **68 %** | **21.4 %** | 31.5 % |
| "at least as many vowels as the least vowelly example" | the loose cousin of "exactly *n* vowels" | **100 %** | 10.8 % | 10.8 % |
| "at most as many vowels as the most vowelly example" | the other loose cousin | **100 %** | 10.2 % | 10.2 % |
| "more consonants than vowels" | the standard word statistic | 45 % | 3.6 % | 7.9 % |
| "it starts with a consonant" | ditto, and it looks true | 44 % | 3.4 % | 7.7 % |
| "the second letter is a vowel" | the classic spelling-shape rule | 29 % | 2.0 % | 6.9 % |
| **"the same number of letters as the examples"** | the most obvious rule of all | 28 % | 3.8 % | 13.4 % |
| "no letter is repeated" | the classic Zendo word rule | 10 % | 0.8 % | 8.2 % |
| **"same first letter as the examples"** | "they all start with e!" | 7 % | 5.6 % | **80 %** |
| "two vowels side by side" | vowel-pattern hunting | 6 % | 0.6 % | 10.3 % |
| **"it rhymes — same last two letters"** | the kid's first idea | 2 % | 2.0 % | **91 %** |

Two findings worth keeping:

* **The loose cousins are consistent with 100 % of clues by construction** and still pay only
  ~10 %. As in `borsel`, the class's real secret is a *convention*: it only ever makes **tight**
  statements — *exactly* three vowels, the word *ends with* t, there *is* a k — never "at least",
  "at most", "more than", "no…".
* **Two traps are rare but nearly always right when they fire.** If all the examples start with
  the same letter the rule is usually "starts with a vowel" (80 %); if they share their last two
  letters it is usually "ends with *c*" (91 %). That is honest structure, not a leak: those clues
  are the ones where the trap and a U-rule agree, and they are only 2–7 % of clues.
* The headline lesson a player must extract is narrow and sharp: **this class only ever talks
  about letters — which letters are in the word, where the first and last one sit, how the letters
  repeat, and how many vowels. It never talks about length, position in the middle, sound,
  meaning, or "more/less than".**

---

## 4. Three demos

```
CLUE                          ANSWER      hidden rule (private)
exhaust
account       ->  cartoon     the word has exactly three vowels
sixteen

peek
kept          ->  ankle       there is a k in the word
skinny

session       ->  exceed      some letter turns up three times
receive
```
The first demo is also the clearest illustration of the traps: all three examples have seven
letters (so "same length" fits, and is wrong), all three share the letter *e* ("they all have an
e" fits, and is wrong), and all three have their second letter a consonant.

---

## 5. The design decision that made the class: no one-letter copies

The cheapest probe in any word class is *"echo an example with one letter changed"* — a real word
one edit away. Most of U survives a one-letter edit (a word with three vowels usually still has
three vowels after swapping a consonant), so that probe was measured at **~45 %** in the first
build: insight optional (DESIGN_LOOP lever 8). The fix, copied in spirit from `dornic`'s
fresh-cards clause:

> **the answer may not be any example, nor one letter away from one** (one substitution, insertion
> or deletion) — and the generator also keeps the examples themselves ≥ 2 edits apart, so the clue
> never suggests the move.

Cost: 4 lines in the scorer (~200 chars of the 821). Result: copy-verbatim **0 %** and
copy-with-one-letter-changed **0 %**, while the honest footholds (a random word 7 %, "everything
they have in common" 21 %, "always answer a double letter" 19 %) stay in the 5–30 % band the loop
asks for.

---

## 6. Witness table — 500 fresh clues

| witness | score |
|---|---|
| copy an example verbatim | **0.0 %** |
| a real word one letter different from an example | **0.0 %** |
| EXCLUDED: contains every letter the examples share | 21.4 % |
| EXCLUDED: at least as many vowels as the least vowelly example | 10.8 % |
| EXCLUDED: at most as many vowels as the most vowelly example | 10.2 % |
| EXCLUDED: same number of letters as the examples | 3.8 % |
| EXCLUDED: same first letter as the examples | 5.6 % |
| EXCLUDED: rhymes (same last two letters) | 2.0 % |
| EXCLUDED: no letter is repeated | 0.8 % |
| EXCLUDED: the second letter is a vowel | 2.0 % |
| EXCLUDED: more consonants than vowels | 3.6 % |
| EXCLUDED: two vowels side by side | 0.6 % |
| EXCLUDED: it starts with a consonant | 3.4 % |
| always answer a word with a double letter (commonest single U-rule) | 19.4 % |
| always answer a word with exactly two vowels (commonest word shape) | 5.8 % |
| random common word | 6.8 % |
| random dictionary word (4–7 letters) | 8.8 % |
| player who has mapped U perfectly | **100.0 %** |
| player who has mapped U minus 2 templates (starts-with-vowel, three-different-letters) | 81.6 % |
| player who has mapped U minus 2 templates (vowel counts, letter-three-times) | 83.0 % |
| player who has mapped U minus 2 templates (contains-*c*, ends-with-*c*) | 82.4 % |
| player with U **plus** the 11 traps, picking a random survivor | **32.6 %** |
| player who picks a **wrong** survivor (never the true rule) | 13.6 % |
| the true rule (`solve`) | **100.0 %** |

Every answer above is well-formed (100 %): the clue's shape *is* the answer's shape, so the demo
economy is satisfied for free. The one exception is the one-letter-change row, where 20 % of the
time no real word exists one edit from the chosen example.

Notes on the partial-knowledge rows: a player whose universe is a **subset** of U gets **zero**
survivors on the clues whose rule they have not mapped (positive examples kill everything else),
so they know they are lost and guess: ~80 % + a guess. A player whose universe is **larger** than
U (U + the traps) sees several survivors on most clues and scores 32.6 % by picking at random —
that gap, 100 % vs 33 %, is the whole difficulty of the class.

Other measured numbers, 500 clues:

* **Example counts**: 2 examples 56.8 %, 3 examples 43.2 % (never more: three is always enough).
* **Uniqueness** (exactly one U-rule consistent with all examples): 500/500.
* **Minimality** (dropping any one example leaves ≥ 2 consistent rules): 500/500.
* Hidden-rule density mean **0.080**; hidden-rule mix: start=end 12.2 %, double letter 12.0 %,
  starts with a vowel 10.8 %, alphabetical 10.8 %, j/q/x/z 10.4 %, contains-*c* 10.2 %, letter
  three times 9.6 %, three different letters 8.6 %, ends-with-*c* 8.0 %, vowel count 7.4 %.
* Clue ≤ 23 chars, answer ≤ 7 chars.

---

## 7. Validation

`python tools/quickcheck.py challenges/lab/tavrik.json --seeds 300` →
`OK tavrik gen=0.24ms score=0.19ms solve=22.3ms`, no warnings.

| quantity | value | cap |
|---|---|---|
| `score` source | **821 chars** | 1024 (the raise `RULE_FAMILIES.md` §4 allows for this paradigm) |
| `generate` source | 7634 (3.3 KB of it is the dropped-word list) | 50 000 |
| `solve` source | 4269 (ditto) | 5 000 |
| `generate` | 0.088 ms mean, 0.24 ms max | 100 |
| `score` | 0.13 ms mean, 0.04 ms on junk | 50 |
| `solve` | 18 ms mean, 24 ms max | 2 000 |
| clue | ≤ 23 chars | 1024 |
| answer | ≤ 7 chars | 1024 |

Junk (`""`, `"0"`, `"x"`, `"1"*100`, the clue itself, `"hel lo"`, `"élan"`, `"CAT"`) all score 0
without raising; `"TONIGHT"` and `" tonight "` score 1 when `tonight` is right. `generate` is fast
because the 4501-word pool and each word's 25-bit "which rules of U do I satisfy" mask are built
**at module level** (≈ 420 ms once per worker, not charged to `max_generate_ms`); a call is then a
handful of `bit_count()`s.

---

## 8. Predicted classification

**On target / testing.** Two Opus players in a 7-class pool:

* **Without a demo** the clue is transparently shaped (2–3 lowercase words, so send a word), and
  the natural probe — "a word with everything these share" — pays **21 %**; a random word pays
  7 %. Expect **10–25 %**, no zeroes, no demo-farming.
* **With a demo** the player learns the paradigm in one look (clue = examples of a rule, answer =
  another word obeying it) but not U. From there they must discover, from 0/1 feedback across
  ~120 fresh clues, that this class talks only about letters and only in tight statements. Every
  template they map is worth ~10 points; a player who maps 8 of 10 scores 82 %, one who maps 4–5
  scores ~50 %. I expect **40–65 %**.

Mean across the two ≈ **0.3–0.45**, i.e. `calibrated`, with the risk on the **easy** side: the
templates are individually guessable ("double letter", "starts with a vowel") and an Opus player
who realises the rule set is small may map most of it in four rounds. If it comes back too easy
the first levers are (a) drop the two loosest rules, "exactly one vowel" and "exactly three
vowels" (.22 each), (b) widen the contains/ends grids to more letters, which makes each *rule*
rarer without adding a new *idea* to find, (c) allow 2-example clues only, which doubles the
ambiguity outside U. If it comes back too hard, put "it has *n* letters" into U — that is the
hypothesis everybody starts with.

**12-year-old test**: the object is a word (nothing is more evocable); every rule is one breath
and every one of them is a game a kid has played ("find a word with a double letter"); one demo
shows a word obeying a rule; and a kid contributes hypotheses immediately ("they all start and end
the same!"). The nameable-pattern risk is real — these *are* nameable rules — but the difficulty
lives in the size of U and in the excluded set, not in any single rule being obscure.
