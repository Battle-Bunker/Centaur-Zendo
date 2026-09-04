# NOTES — team sarn2b — class `sarn` (the only class in the pool)

## The one demo (window 0)
clue: `d2473`   solution: `dull derrick drunken down`   score 1

Facts I can read straight off it, no maths:
* 4 words, lowercase, single spaces, no punctuation.
* Every word starts with **d** — the same letter that starts the clue.
* Word lengths 4, 7, 7, 4. The digits are 2, 4, 7, 3. **They do not match**, so
  the digits are NOT the word lengths.
* Lengths 4,7,7,4 are a mirror (short long long short) — could be chance.
* The clue is one lowercase letter followed by four digits.
* All four words are ordinary English (`dull`, `derrick`, `drunken`, `down`) —
  a derrick is a crane. The phrase is not a sentence; it is an alliteration.

## Ten hypotheses, as I'd say them to a 12-year-old
1. **Alliteration.** "The letter at the front tells you the letter every word
   must start with. Write four words that all start with it."
2. **Digit count = word count.** "Count the numbers — there are four of them, so
   write four words. All start with the letter."
3. **Number is just a name tag.** "The number is a serial number so the server
   can tell one puzzle from another. Any words starting with the letter work."
4. **Digits are word lengths.** (Already dead: 2473 vs 4,7,7,4.)
5. **Digits add up to something.** 2+4+7+3 = 16; the answer has 22 letters and
   25 characters. Dead unless something else is counted.
6. **Mirror lengths.** "The words have to get long and then short again, like a
   see-saw: 4, 7, 7, 4."
7. **Secret word hidden at those positions.** "Take the 2nd, 4th, 7th and 3rd
   letters of your answer and they spell something." (u, l, r, l — nonsense.)
8. **The number picks the words out of a dictionary** — the 2473rd d-word, etc.
   (Checked against a frequency list: 453/899/712/3. Nothing lines up.)
9. **It must sound good / be a real phrase** — a tongue-twister a person would
   say out loud, not just any four words.
10. **The number sets the difficulty**: bigger number = more words, or rarer
    words. 2473 is a 4-digit number and there are 4 words.

Best three: **1/2/3** are nearly the same rule and are the everyday, physical
reading — it's a tongue-twister. The only real open question is **how many
words**, and whether the digits control it.

## What I will probe (round 1)
One question only, answered in one round: **word count**. Cycle the answer
through 1,2,3,...,12 words (all starting with the clue's letter, ordinary words,
lowercase, single spaces) plus two shaped variants. Whichever counts score 1
settles hypotheses 1/2/3 and kills the rest.

## Outcome
Final: presented 3622, answered 1770, **correct 11**. Rank 1 (only team finished).
n=3 answers 8/830 (0.96%); n=4 (+2 offset) 3/940 (0.32%) — the 12.5% seen in
training was noise, so the n=4 hedge cost throughput and gained little.

## What I know for certain about `sarn`
* Answer = a space-separated list of lowercase words, **one word per digit**,
  every word starting with the clue's letter. All 7 reference solutions obey it.
* The digits matter *beyond* their count: replaying a known-correct answer on a
  different clue with the same letter and same word count scored 0, 122 times.
* The digit is **not** any letter-weighted count (length, vowels, consonants,
  holes, …): the exact linear system over 26 letter weights is inconsistent.
* It is also not distinct letters, vowel/consonant groups, first/last vowel
  position, syllables, alphabetical rank, or any constant length offset.
* Reference answers show len(word) − digit ranging from −3 to +4.
