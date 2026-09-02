# Direction: wordplay as kids know it (wordplay-agent)

Brief: the demo is a short list of real words a kid can read; the tiny clue pins an
arbitrary-but-natural **measurement** across those words. Not a named puzzle. Wordz already
owns vowel/consonant counts, so those are off the table. Scorer must require dictionary
words (`words.is_word`), a fixed word count, and the clue-derived constraint; constant
answers must fail.

Design constraints inherited from the earlier lab runs (read before judging the ideas):

* `quilm`: **recognising the object must be necessary but not sufficient.** If the object
  admits exactly one natural relation, "which object" and "which rule" are the same
  question and the model recognises rather than infers.
* `quilm`: **no negative-only clauses** in the scorer — demos only show positives, so a
  clause no demo can exhibit is invisible. Put exclusions in `generate()`.
* `orlan`: **a 0/1 channel only tests hypotheses the player already generates.** If the
  hidden quantity is never displayed, a lateral rule is unreachable. Corollary for this
  direction: the measurement must be *shown* — the clue digits ARE the quantity, and every
  demo hands over 3-6 (word -> number) pairs. That is the strongest channel available short
  of naming it.
* `murn`: a near-miss hypothesis that scores a few percent is worth keeping — it is the
  only gradient in an all-or-nothing conjunction.

## The attack I am designing against

The players are Opus agents with ~450 graded probes per 0.5 s round and 6 demos. For a
"list of words + digits" class their attack is:

1. Enumerate per-word integer features (length, vowels, consonants, syllables, distinct
   letters, scrabble score, alphabet positions...) and match them against the demo digits.
2. If none fits, **fit a hidden letter subset**: `digit_i = |{letters of word i} ∩ S|` is a
   linear system over 26 binary unknowns; ~25 (word, digit) pairs from 6 demos are enough to
   pin S by ILP/greedy search — *without ever naming the concept*. Any "count the letters
   that <have a property>" rule dies to this, however exotic the property.
3. Learn a (letter -> digit) lookup table empirically from binary feedback.

So: (2) says the measurement must be **non-linear in letter counts**, and (3) must be
priced out by making the table of facts too big to learn blind.

## Brainstorm (12 ideas, each against the 12-year-old test)

Test part 1 = a kid can evoke and *verify* the measurement with no equipment beyond a
pencil, a keyboard or their voice. Test part 2 = once you know it is "words + a number",
the measurement is still not nameable, so recognition does not end the game.

| # | idea | kid can do it? | nameable? | survives the subset-fit attack? | verdict |
|---|---|---|---|---|---|
| 1 | **Rhyme ladder**: digit *i* = length of the longest shared ending of word *i* and word *i+1* ("cat/hat = 2") | yes, rhyming is the first wordplay a kid learns | half — "longest common suffix" is a standard string op and the first pairwise feature anyone codes | n/a (pairwise) but it is feature #1 in every library | reject: cracked from one demo |
| 2 | **Shared letters with the next word**: digit *i* = number of distinct letters words *i* and *i+1* have in common | yes, "which letters are in both?" | not named, but set-intersection is a standard pairwise feature | yes (non-linear) | keep as fallback; risk of a fast crack |
| 3 | **Syllable claps**: digit = number of vowel groups ("clap it out") | yes, universal | it is *the* approximation for syllable counting; in every prior | yes | reject: too close to Wordz and too in-prior |
| 4 | **Alphabet-song steps**: digit *i* = distance in the alphabet from word *i*'s initial to word *i+1*'s initial | yes | "alphabet index difference" — instantly guessed | n/a | reject: one demo |
| 5 | **Pokey letters (handwriting)**: digit = number of letters that leave the middle band — tall ones `bdfhklt` or tailed ones `gjpqy` | yes, and it is delightful (a kid counts them on the page) | not nameable as a *measurement* — "ascender" is typography, not a puzzle move | **no — it is exactly `|word ∩ S|`**, so an ILP over 6 demos finds S without the insight | reject as the main rule; excellent kid hook, keep as a decoy family |
| 6 | **Holes in the letters** (`a b d e g o p q` = 1 hole) | yes, classic playground counting | no | no — same subset fit | reject, same reason as 5 |
| 7 | **Pen lifts**: how many times you lift the pencil (`i j t x f` need a second stroke) | yes | no | no — subset fit again | reject, same reason |
| 8 | **Beheadings/deletions**: digit = how many single-letter deletions of the word are still words ("how many letters can you cross out?") | yes, and kids love it | no, genuinely unnameable | yes — needs a dictionary, not a subset | **reject on fairness**: the value depends on the engine's exact 235k web2 list; a player with a different word list computes different numbers and can never converge. Dictionary membership must stay in the *easy* direction (are these real words?) only |
| 9 | **Words hidden inside words**: digit = length of the longest real word strictly inside word *i* | yes ("I spy a little word") | no | yes | same dictionary-mismatch fairness problem as 8; also expensive in the scorer |
| 10 | **I-spy letter counts**: clue letter L, digit *i* = how many times L appears in word *i* | yes | trivially guessed in round 1 | n/a | reject: too easy |
| 11 | **Keyboard row jumps**: digit = how many times the typing finger changes row (`qwertyuiop` / `asdfghjkl` / `zxcvbnm`) | yes — keyboards are the object a kid uses most, and they can literally type the word and count | not a named puzzle; "typewriter word" (one row) is the only famous keyboard fact and this is not it | **yes** — a transition count is not a linear function of letter counts, so the subset fit returns *no consistent S* and the whole "count the letters that..." family gets discarded | strong |
| 12 | **Keyboard row travel**: digit = total number of row lines the finger crosses, counting a top-row-to-bottom-row hop as **2** | yes, same act, one extra sentence | no | yes | **chosen** |

## Chosen: 12 (+ a tongue-twister clause), named `sarn`

Clue = one lowercase letter + 3-6 digits, e.g. `s3142`. The answer is exactly that many
real words, **all starting with the clue letter** (the kid-visible tongue-twister layer,
readable off any demo), where word *i*'s **row travel** equals digit *i*.

Row travel: give each letter its keyboard row (top `qwertyuiop` = 0, home `asdfghjkl` = 1,
bottom `zxcvbnm` = 2) and add up `|row(a) - row(b)|` over neighbouring letters.
`salt` = s(1) a(1) l(1) t(0) -> 0+0+1 = **1**. `shout` = s(1) h(1) o(0) u(0) t(0) -> 0+1+0+0
= **1**. `scrape` = s(1) c(2) r(0) a(1) p(0) e(0) -> 1+2+1+1+0 = **5**.

Why 12 beats 11 (the same object, one notch harder): "how many times does the row change"
is the *first* thing anyone tries once the keyboard is in play, and it is wrong exactly when
a word hops top<->bottom. Measured on the common-word pool, the two agree on **34.9 %** of
words, i.e. on **1.5-4 %** of whole answers — a real, visible gradient above the ~0 % floor
that says "keyboard, but not quite", and it costs the player exactly one probe cycle to
resolve. That is the murn 17-20 % band, scaled down for a conjunction of 3-6 items.

### Why the tongue-twister clause carries its weight (this is a witness closure, not decoration)

Without it, the class would be crackable with **no insight at all**: the player would only
need one word per digit value 1..9 — nine facts, and each demo hands over 3-6 of them. Two
demos and a fixed nine-word vocabulary would answer every clue forever. Forcing every word
to start with the clue letter turns those nine facts into ~200 `(letter, value)` cells,
while the demos still supply only ~25 of them; a player who has learned the table and not
the rule can then answer `(25/200)^4 ≈ 0.02 %` of clues. The empirical-table route is
dead, and the only way through is the measurement itself.

It also makes the demo evocative in one glance — `swim shut scrape sand` is a tongue
twister, which is what a 12-year-old sees before they see anything else — and it is
discoverable from the clue shape alone in round 1, so it is *visible* structure rather than
a hidden second clause (recognition necessary, not sufficient).

### Degenerate witnesses and how each is closed

| witness | closed by |
|---|---|
| empty string / junk / the clue echoed back | word count + `words.is_word` |
| a constant answer reused for every clue | the letter and all 3-6 digits must match; measured best constant = 0.0 % over 3000 clues |
| one-letter words (`a`, `i`) padding a list | `generate` never emits a 0 digit, and a 1-letter word has travel 0, so every answer word has >= 2 letters — closed without a negative clause |
| the same word repeated | `generate` requires >= 2 distinct digit values in every clue |
| any "count the letters that X" hypothesis | the measurement is a transition count, not a subset count: no S fits |
| learning a word -> number table from demos | the alliteration clause makes the table ~200 cells; demos supply ~25 |
| non-words that look plausible | `words.is_word` against the engine's 235k list |

### What is *not* closed, deliberately

A player who reaches "keyboard rows" gets the class in one more probe cycle. That is the
intended fairness floor: the insight is the whole difficulty, and once a human says
"count the times your hand jumps rows" the AI half finishes it in a round.

---------------------------------------------------------------------------
## Iteration 1 — `challenges/lab/sarn.json` (v1, shipped)

### Rule (private)

Clue: one lowercase letter `L` + 3-6 digits, each `1-9` (e.g. `t3634`, 4-7 chars).
Answer: exactly that many whitespace-separated English words (`words.is_word`), **every word
starting with `L`**, where word *i*'s **row travel** equals digit *i*.

Row travel: `qwertyuiop` = row 0, `asdfghjkl` = row 1, `zxcvbnm` = row 2; add `|row(a)-row(b)|`
over neighbouring letters. A top<->bottom hop costs **2**.
`salt` 1, `thread` 3, `scrape` 5, `crazy` 6. Case and whitespace are free.

`generate` draws real everyday words (proper nouns filtered by an inflection test:
a common noun or verb nearly always has `-s/-es/-ed/-ing/-er/-ly/-y` in the dictionary, a
name nearly never does) from dense `(letter, value)` cells (>= 5 words each) over the 15
letters `a b c d e f g h l m p r s t w`, and emits their travels; it re-draws until the clue
has >= 2 distinct digits. `solve` re-picks *different* words for the same digits, preferring
words of <= 7 letters so a human can check a demo by hand.

### Intended discovery path

1. Round 1, free: the clue is `letter + digits`, `#words == #digits`, and every demo word
   starts with the letter. The tongue-twister clause costs nothing — as designed, so that
   recognising the object is necessary but not sufficient.
2. The digits are a per-word integer that is **not** length, vowels, consonants, syllables,
   distinct letters, scrabble score or any letter-category count (all measured below at
   0.0-0.6 %).
3. The leap: *type the word and count the row lines your finger crosses.* This is the kid's
   half of the centaur — a 12-year-old with a keyboard can check `thread` = t(top) h(home)
   r(top) e(top) a(home) d(home) = 1+1+0+1+0 = 3 in ten seconds.
4. The near miss: counting row **changes** instead of the distance. It agrees on 34.9 % of
   words, i.e. **2.2 %** of whole answers against a 0.03-0.07 % floor — a visible
   "keyboard, but not quite" signal that costs one probe cycle to resolve.

### Validation

`python tools/quickcheck.py challenges/lab/sarn.json --seeds 200` -> `OK sarn gen=0.09ms
score=0.08ms solve=1.16ms`, no warnings. Sources: score **290**/512 chars, solve 1279/5000,
generate 1152/50000. Over 3000 fresh seeds: generate mean 0.023 ms / worst 0.153 ms, no
generator fallbacks, clue <= 7 chars; solve mean 0.021 ms, never empty, **3000/3000 score 1**,
deterministic, always distinct words, answers <= 51 chars; worst `score` call on any junk
0.031 ms and it never raises. 15 clue letters, digit histogram 1..9 =
13/22/24/23/18/15/10/7/4 %, word counts 3-6 near-uniform.

### Self-tests (scratchpad `wp/*.py`)

* **Cross-check against an independent re-implementation**: 14 000 answers (real solutions,
  random word lists of the right and wrong length, one-word-substituted, reversed, extended,
  capitalised) — **0 disagreements**.
* **Cosmetic tolerance** (300 clues each, all 300/300): upper case, Title Case, doubled and
  leading/trailing spaces, newline-separated, tab-separated, trailing newline.

### Anti-witness measurements (3000 shipped clues)

| answer family | scores 1 |
|---|---|
| the exact rule — **fairness ceiling** | **100.00 %** |
| row CHANGES instead of travel (the near miss) | 2.23 % |
| consonant count = digit | 0.57 % |
| distinct-letter count = digit | 0.27 % |
| letters with holes = digit | 0.17 % |
| word length = digit | 0.13 % |
| ascender+descender ("pokey letters") count = digit | 0.10 % |
| vowel count / alphabet-step sum / scrabble score / vowel groups | 0.00-0.07 % |
| random words with the right initial and word count | 0.03 % |
| best constant answer (best of 300 candidates over 1000 clues) | 0.20 % |
| empty string, junk, `"1"*100`, the clue echoed back | 0.00 % |

### The attack this class is built against (measured, not assumed)

`digit = |word ∩ S|` for a hidden letter set `S` is the generic no-insight crack for any
"count the letters that ..." rule, and six demos supply enough pairs to fit it. Here it has
no solution, because row travel is a **transition** count:

| attack | per-word exactness | end-to-end score |
|---|---|---|
| best greedy 0/1 subset `S`, fitted on 2000 (word, digit) pairs | 26 % held-out | 0.70 % |
| least-squares letter-weight + length model, fitted on **25** pairs (= 6 demos) | 96 % train / **12 % held-out** | 0.25 % |
| same model fitted on 100 pairs | 34 % | 1.30 % |
| same model fitted on 2000 pairs (unobtainable: ~400 demos) | 39 % | 2.75 % |

The 25-pair row is the trap worth naming: the fit **explains the demos perfectly and
generalises at 12 %**, so a player who trusts it ships a solver that scores a quarter of a
percent. And travel is unchanged by shuffling a word's letters only 30 % of the time, so no
bag-of-letters feature can express it at all.

### Fairness floor — hypothesis elimination

30 plausible per-word integer features (length, vowels, consonants, distinct letters, vowel
groups, syllable-with-silent-e, double letters, scrabble, alphabet rank/gaps, alphabetical
adjacent pairs, ascenders, descenders, ascenders+descenders, holes, straight-line letters,
symmetric letters, top/home/bottom-row counts, left-hand letters, phone-keypad digit changes
and sums, row changes, row travel ±1, max row jump, distinct rows used, ...) were tested
against demo evidence:

* **after ONE demo (6 word/number pairs) exactly one feature survives: row travel.**

So elimination is free and the entire difficulty is *generation*: the class is hard iff
"count the row lines your finger crosses" is not in the player's hypothesis library, and it
is trivially confirmable the moment a human says it out loud. That is the orlan lesson
applied in reverse — the hidden quantity is printed in the clue of every single item.

### Witness leaks closed

| witness | closed by |
|---|---|
| empty / junk / clue echo | word count + `words.is_word` |
| a constant answer | letter + all 3-6 digits must match (best constant 0.20 %) |
| one-letter words (`a`, `i`) as filler | generate never emits a 0 digit and a 1-letter word travels 0 — closed without a negative clause |
| the same word repeated n times | every clue carries >= 2 distinct digits |
| "count the letters that X" for any X | transition count: no subset fits (0.70 %) |
| learning a (word -> number) table from demos instead of the rule | the alliteration clause turns 9 learnable facts into ~125 `(letter, value)` cells; 6 demos supply ~25, so a table-only player can answer `(25/125)^4 ≈ 0.2 %` of clues |
| a fitted linear letter-weight model | 0.25 % at the data volume six demos provide |

### Arena (DESIGN_LOOP step 3) — set up, players NOT run (no Agent tool here)

```
run          lab-sarn-1        pool = sarn only (1 challenge, so both teams can spend all 6 demos on it)
config       6 rounds x 0.5 s, 5 s cooldown, 1 demo/window, 3 s final
port         60703 (server pid 3496)
team sarna   /tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-sarn-1/players/sarna
team sarnb   /tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-sarn-1/players/sarnb
teardown     python sim/arena.py teardown --run lab-sarn-1 && python sim/arena.py report --run lab-sarn-1
```

### How to read iteration 1

* **both cracked** -> harden: swap row travel for phone-keypad travel (same object family,
  weaker prior), or require the words in alphabet-song order by their second letter
  (a second, kid-visible but constructive clause).
* **one cracked, one not** -> on target, freeze.
* **neither cracked, both ~0 %** -> soften one notch: switch the measurement to row
  **changes** (the simpler sibling, no double-count), which keeps the object and drops the
  one arbitrary detail. If a player reports "keyboard" anywhere in NOTES.md, the class is
  fair and only that detail was missing.
* Watch for: anyone scoring 1-3 % is holding the near-miss hypothesis; anyone scoring
  0.2-0.6 % has fitted a letter-weight model and believes it.
