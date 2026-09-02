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
