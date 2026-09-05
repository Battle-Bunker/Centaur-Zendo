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
| `generate` source | 7632 (3.3 KB of it is the dropped-word list) | 50 000 |
| `solve` source | 4267 (ditto) | 5 000 |
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

---

# Revision 2 — the lineup answer (2026-09-05)

`docs/RULE_FAMILIES.md` §"Revision 2" + §5b. v1 is kept byte-identical as
`challenges/lab/tavrik.v1.json`; the shipped file is `challenges/lab/tavrik.json`.

## 9. What the first arena showed

Both Opus teams took **no demo** on tavrik and scored **71 %** (dornic1a) and **66 %** (dornic1b)
without ever naming a rule. Their method (`players/dornic1b/strategy.py`, `zpools.py`): build a
pool of 273 word predicates, keep those true of *every* example, and emit a word satisfying **all**
of them at once. The true rule is somewhere in the pool, so the answer satisfies it by
construction; the eleven excluded traps cost nothing, because satisfying an *extra* rule is
harmless. The only thing that actually held them was the novelty clause — their own notes record
`tavrik – the answer must be >= 2 edits from every clue word. 0/4 -> 29/38` — i.e. a rule that is
not part of the hidden rule at all, and which players fairly called invisible.

**The fix.** The answer is now a *choice*: the clue is the same minimal identifying example set,
then a blank line, then **four candidate words**, and the answer is which one obeys the rule.
The intersection attack has nothing to intersect. The "≥ 2 edits" clause is **gone**, and with it
the whole notion of a well-formed answer: `score` no longer even calls `words.is_word`.

## 10. What changed, item by item

| | v1 | v2 |
|---|---|---|
| clue | 2–3 example words | 2–3 example words, blank line, **4 candidate words of one length** |
| answer | any dictionary word obeying R, ≥ 2 edits from every example | **one of the four**, verbatim (case/space-insensitive) or its index 1–4 |
| floor | 6.8 % (random common word) | **25 %** |
| freshness clause | "≥ 2 edits from every example" | **dropped** |
| U | 10 templates, 25 rules | **unchanged** (still an antichain) |
| eligible as the hidden rule | all 25 | **22** — template 0 is a competitor only (see below) |
| excluded traps | 11, worth 0.6–21.4 % | 14, worth **exactly 25.0 % each** |
| `score` | 821 chars, `words.is_word` + edit-distance test | **689 chars**, no dictionary at all |
| `solve` | rejection-samples a valid word, 22 ms | picks the obeying candidate, **0.13 ms** |

### Why "exactly *n* vowels" had to stop being the answer
§5b wants **matched trap profiles**: the truth and all three decoys must fire the *same* set of
example-consistent excluded rules. Two of the traps are "at least as many vowels as the least
vowelly example" and "at most as many as the most vowelly one" — both consistent with 100 % of
clues, both measured in v1. On a clue whose rule is "exactly *n* vowels", every example has *n*
vowels, so those two traps fitted to the clue are `≥ n` and `≤ n`, whose conjunction **is** the
rule. The truth fires both; a decoy, having ≠ *n* vowels, must fail one. Matching is impossible,
and the generator rejected 100 % of those clues. So template 0 keeps its place in U — the examples
must still kill "exactly 1 / 3 / 4 vowels" for the clue to be unique — but it is never drawn as
the hidden rule. This is the same COMPETITOR device `tresk` uses for its 15 loose rules and
`wisbek` for its minute-decades template. The other **9 templates / 22 rules** are drawn uniformly
by template first, then parameter (mix over 2000 clues: 201–247 per template, expected 222).

### How a decoy is built
Three matching conditions, in order:

1. **Trap profile** (§5b). `TRAPS()` fits the 14 excluded rules to the examples; `TBITS()` turns a
   word into a bit per fitted trap. Decoys are grouped by that bit-vector, true candidates are
   grouped the same way, and a lineup is only assembled from a bucket where both exist. Result:
   all four candidates fire exactly the same traps on **500/500** clues, and every decoy fires at
   least one (**500/500**).
2. **Shape.** The decoys use the *same number of different letters* as the truth wherever the rule
   allows (it cannot for "only three different letters", where 4 is the nearest legal value). This
   was added after measuring: without it "pick the odd one out by shared letters" scored **46 %**,
   and 73–74 % on the three-different-letters and letter-three-times clues, whose answers are
   naturally the letter-poorest word of the four.
3. **The attacker's own count.** `generate` carries `dornic1b`'s `tavrik_preds()` — all **273**
   predicates, rebuilt bit for bit inside the challenge, including the six duplicate dict keys
   (`stv`, `stc`, `env`, `enc`, `dblv`, `dblc`) that silently shadow the per-letter versions in
   their own code. It intersects that pool over the examples (`C`) and then *aims* the true
   candidate's rank on `popcount(PMS & C)`. Realised rank 237 / 86 / 98 / 79 over 500 clues, i.e.
   at least one decoy out-counts the truth on **52.6 %** of clues (§2 asks for ≥ 40 %).
   Finally `BUILD` picks, among the triples that respect that split, one that also puts the truth
   at a randomly aimed place in the mutual letter-overlap order, which is what pulls "odd one out"
   and "medoid" back to chance.

## 11. The excluded rules (fitted to the clue)

`fits` = the rule, fitted to the examples, is consistent with every one of them, so a player who
forms it is never contradicted. `scores` = a player who always picks a candidate satisfying it.

| excluded rule | fits | scores |
|---|---|---|
| at least as many vowels as the least vowelly example | 100 % | **25.0 %** |
| at most as many vowels as the most vowelly example | 100 % | **25.0 %** |
| it ends with a consonant | 67.8 % | **25.0 %** |
| it contains every letter the examples share | 62.8 % | **25.0 %** |
| it starts with a consonant | 49.0 % | **25.0 %** |
| more consonants than vowels | 48.6 % | **25.0 %** |
| the second letter is a vowel | 29.4 % | **25.0 %** |
| the same number of letters as the examples | 24.2 % | **25.0 %** |
| the second letter is a consonant | 17.2 % | **25.0 %** |
| no letter is repeated | 9.0 % | **25.0 %** |
| two vowels side by side | 4.4 % | **25.0 %** |
| it rhymes (same last two letters) | 4.2 % | **25.0 %** |
| the same first letter as the examples | 2.2 % | **25.0 %** |
| it ends with a vowel | 1.0 % | **25.0 %** |

Mean **5.2** of them are consistent with any one clue (min 2, max 9). In v1 the strongest of these,
"contains every letter the examples share", paid 21.4 % and was the intended foothold; it now pays
exactly chance, and so does its inverse and any count of traps. The v1 lesson ("this class never
says *at least*") no longer pays on its own — the game is now purely *which* rules the class uses.
Note one structural point: when the examples share exactly one letter and the rule is "it has a
*c* in it", that trap **is** the rule, and no matched profile exists; the generator simply tries
another minimal example set for the same rule (up to four), which is why `contains c` clues
overwhelmingly share two or more letters.

## 12. Three demos

```
CLUE                            ANSWER            hidden rule (private)

tissue
capped
                          ->    decree (2)        it has a double letter
reader
decree
madame
decade

kick
food
                          ->    level (4)         it uses only three different letters
rural
dummy
rebel
level

squeeze
execute
express
                          ->    major (4)         it has a j, q, x or z in it
yours
human
today
major
```
(seeds 19, 9, 24.) Note demo 2: all four candidates are five letters, all four fire the same
traps, and `rural` (4 different letters), `dummy` (4) and `rebel` (4) sit one letter away from
`level`'s 3 — the nearest a decoy can legally get.

## 13. Witness table — 500 fresh clues (seeds 1e6 … 1e6+499)

| witness | score |
|---|---|
| **the in-U intersection — a player who knows U** | **100.0 %** |
| the true rule (`solve`) | **100.0 %** |
| the true rule, answered by INDEX rather than verbatim | **100.0 %** |
| **the candidate satisfying the MOST example-consistent predicates of the 273-strong outside pool** | **34.0 %** |
| the candidate with the smallest edit distance to an example | 28.7 % |
| the candidate with the most vowels | 28.3 % |
| the candidate with the most letters in place with an example | 27.9 % |
| the alphabetically first candidate | 27.6 % |
| **pick candidate 1** | 27.0 % |
| the candidate satisfying the FEWEST such predicates (the inverse heuristic) | 26.9 % |
| **pick a random candidate (the floor)** | **25.0 %** |
| the outlier of the four by shared letters | 24.3 % |
| the candidate sharing the most letters with an example | 23.0 % |
| the candidate with the most different letters | 22.6 % |
| the medoid of the four | 21.0 % |
| **each of the 14 excluded rules** | **exactly 25.0 %** |
| a player whose universe is U + those 14, committing to a random survivor | 38.6 % |
| a player who knows U minus its two rarest templates (alphabetical order .016, a letter three times .023) | 83.7 % |
| … minus (starts-and-ends-the-same, three-different-letters) | 83.5 % |
| … minus (contains-*c*, ends-with-*c*) | 82.6 % |
| … minus (double letter, starts with a vowel) | 84.7 % |
| … minus (j/q/x/z, three-different-letters) | 83.5 % |

Other measured numbers (500 clues unless stated): uniqueness 500/500, minimality 500/500, exactly
one candidate obeys the rule 500/500, all four candidates the same length 500/500, four distinct
candidates 500/500, no candidate equal to an example 500/500, matched trap profiles 500/500, every
decoy fires ≥ 1 consistent trap 500/500. Examples per clue (20 000 seeds): 2 → 56.5 %, 3 → 43.5 %.
Candidate length 4/5/6/7 → 92/141/154/113. True-candidate position 135/113/122/130. Mean density
of the hidden rule 0.073. The seed-0..19999 sweep produced **0** fallback clues and **0** duplicate
clues.

## 14. Validation

`python tools/quickcheck.py challenges/lab/tavrik.json --seeds 300` →
`OK tavrik gen=9.2ms score=0.25ms solve=0.25ms`, **no warnings**.

| quantity | value | cap |
|---|---|---|
| `score` source | **689 chars** (v1: 821) | 1024 (the rule-family raise, `RULE_FAMILIES.md` §4) |
| `generate` source | 19 328 (3.3 KB of it is the dropped-word list) | 50 000 |
| `solve` source | 839 (v1: 4267) | 5 000 |
| `generate` | **1.21 ms mean**, 12.1 ms max over 2000 seeds | 100 ms |
| `score` | 0.12 ms mean, 0.51 ms max (junk included) | 50 ms |
| `solve` | 0.13 ms mean, 1.5 ms max (v1: 22 ms) | 2 000 ms |
| clue | ≤ 56 chars (v1: 23) | 1024 |
| answer | ≤ 7 chars | 1024 |

`generate` is ~14× slower than v1's 0.088 ms because a call now samples ~260 rule-breaking and
~100 rule-keeping words *per candidate length*, computes each one's trap bits and scores it
against the 273-predicate pool. Module-level tables (the 4501-word pool, its 25-bit U mask, its
10-field trap features and its 273-bit outside-pool mask) cost **≈ 690 ms** once per worker
(v1: 420 ms) and are not charged to `max_generate_ms`. `score` was checked candidate-by-candidate
against `solve` on 600 clues × 4 candidates × (verbatim + index) with 0 disagreements, and rejects
`""`, `"0"`, `"5"` (an out-of-range index), `"x"`, `"1"*100`, the clue itself, an example word, a
word one letter from the answer, `"hel lo"` and the unicode digits `"١"`/`"²"` without raising; it
forgives case and surrounding spaces (`" DECREE "` scores 1).

## 15. Predicted classification

**Calibrated, and materially harder than v1, with the risk now on the hard side.**

* **Without a demo**: the shape (2–3 words, a gap, 4 words) reads as multiple choice, so every
  probe is well formed from round 1 and the floor is a free 25 %. The round-1 method degrades from
  "emit the intersection" to "pick the candidate satisfying the most surviving predicates", worth
  **34 %**. Expect **25–40 %**.
* **With a demo**: a demo now teaches only the format (echo one of the four lines), because there
  is no convention left to learn. The way up is to reconstruct U, and the moment a player filters
  U correctly they score 100 %, because the in-U intersection is exact. That is a cliff, not a
  slope: 9 eligible templates from ~120 probes; a player who maps 7 of 9 scores **83 %**, one who
  maps all 9 scores **100 %**. Expect **40–70 %**.

Mean across the two ≈ **0.35–0.55** → `calibrated`. v1's ladder (6 % random → 21 % best trap →
100 %) is replaced by 25 % → 34 % → 100 %.

Levers if it comes back **too easy**: (i) k = 5 or 6 candidates (floor 20 % / 17 %); (ii) widen the
contains/ends grids to more letters, which makes each *rule* rarer without adding a new *idea*;
(iii) 2-example clues only. Too **hard**: (iv) k = 3 (floor 33 %); (v) let one decoy be an instance
of a *U* rule the examples nearly allow, so a partly-mapped player is rewarded rather than punished.

**12-year-old test**: better than v1. The object is still a word, every rule is still one breath
and a game a kid has played ("find a word with a double letter"), and the task is now the one every
kid knows from a puzzle book — *which of these four fits?* A kid can check four short words against
a hypothesis by hand in seconds, and a wrong guess is now informative (one of four, not one of
56 176). What is lost is the freedom to answer with the first word they think of. One residual
blemish inherited from v1: the 4501-word pool still contains a few proper nouns the drop list
missed (`jimmy`, `larry`, `lucy`, `warsaw`, `canada`), which can now surface as candidates as well
as examples.
