# Rule-family classes ("guess the rule from a few examples")

Added 2026-09-04 at the organiser's request. A second paradigm next to the picture classes.

## The idea
A class owns a **finite universe U of candidate rules** over some world of instances (card hands,
dice rolls, bead strings, words, clock times, small pictures, shopping lists, football scores…).
Each rule is a template with parameters, e.g. for a hand of cards:
* count of suit X is (<, >, =) n
* the count of every suit is prime
* the sum of the values of (all cards | suit X) is (= n | prime | a multiple of y)
* … a dozen or two templates, each with a small parameter grid.

`generate(seed)` draws one rule R from U (parameters included) and then draws **positive
examples** — instances that satisfy R — and keeps adding/replacing examples until the set of rules
in U consistent with all the examples is **exactly {R}**, and is **minimal**: removing any one
example leaves at least two consistent rules. The clue is those examples, one instance per line
(nothing else). The answer is **one more instance that satisfies R** (well-formed, not one of the
examples). `solve()` re-derives R from the clue exactly the way the scorer does and constructs
a fresh instance. `score()` parses the examples, enumerates U, filters by the examples, expects a
single survivor R, and returns 1 iff the answer is a well-formed instance, not among the
examples, satisfying R.

## Why it is hard in the right way
* The clue's shape tells the player the answer's shape at once (another line like the examples),
  so a demo-less player always sends well-formed attempts — the demo economy is satisfied for free.
* The examples are **just enough** to pin R inside U — but a player does not know U. Their own,
  larger hypothesis space contains rules the designer never uses (deliberately excluded obvious
  ones: "all the same suit", "all red", "sorted", "no repeats"…) that also fit the examples. A
  player who answers with an instance of such a rule scores 0. Over many clues and 0/1 feedback
  they must learn **which rule types the class never uses**, and which it does. Even a player who
  has mapped most of U will sometimes be wrong when an unmapped template survives.
* Difficulty dials: the size and shape of U, which obvious templates are excluded, how many
  examples (fewer = more ambiguity for the player; the filter keeps it unique within U), and how
  "distant" the excluded rules are from the used ones.

## Design rules
1. Choose U so that every rule is a one-breath kid sentence about the world ("three hearts",
   "every suit an odd number of times", "the spades add up to twenty").
2. Exclude at least three obvious templates that a first-time player will try, and record them
   in the private description. Make sure they are frequently consistent with the examples (that is
   the trap) — the generator does not need to avoid them; only rules IN U are filtered.
3. Minimality: 2–5 examples; the generator must verify uniqueness within U and minimality;
   report the distribution of example counts.
4. Answers must be verifiable by the scorer from the clue alone (SPEC §2: no hidden channel).
   The scorer re-derives R; if U cannot be enumerated within the scorer cap, encode U as a tiny
   table of (template id, parameter) pairs and one shared predicate function. Target ≤ 512 chars;
   this paradigm may use up to 1024 (declared judgement call: `max_score_code_chars` may be
   raised to 1024 for the pool if a family needs it — report the length).
5. Well-formedness must be strict but the world simple (fixed instance size, small alphabet) so a
   demo-less first probe — "copy an example with one change" — is well formed and sometimes right
   (the foothold: report its rate).
6. The witness table must include: copy an example verbatim (must score 0), copy with one random
   change, an instance of each excluded obvious rule fitted to the examples, an instance of the
   most common U-template regardless of examples, random instances, and the true rule.
7. `solve()` must not leak: vary the constructed instance (random among valid ones), never the
   minimal or canonical one.

## Worlds to try (one class each; keep them small and legible)
cards (hands of 4–6), dice (rolls of 3–5 dice), beads on a string (6–10 colours from 3–4),
words (4–7 letter English words: letter/vowel/position rules), clock times (`hh:mm`), tiny
pictures (5×5 of two symbols), shopping receipts (item, price), football scores (`3-1`),
dominoes (sets of 4), coins in a purse, playing-card layouts, weather-week strips.

## Revision 2 (2026-09-05): the lineup answer

**What the first run showed.** Two Opus players took no demos on the five rule-family classes and
scored 23–97 % on them (tresk 97 %, wisbek 95 %, dornic 77 %, tavrik 66 %, borsel 58 % for the
better player) with one method: build a pool of 200–350 candidate predicates, keep those true of
every example, and emit an instance satisfying **all** of them at once. The true rule is somewhere
in the pool, so the answer satisfies it by construction. Nobody named a rule; the excluded traps
cost nothing because satisfying an extra rule is harmless. The "fresh instance" clauses (no clue
card reused, unused length…) were the only thing that held them for a round, and players called
those invisible and unfair — rightly, since they are not part of the rule.

**The fix: make the answer a choice, not a construction.** The clue is the minimal identifying
example set **plus a lineup of k = 4 candidate instances**, and the answer is *which one* of the
candidates fits the hidden rule (write the candidate back verbatim, or its number). Exactly one
candidate satisfies R. Each decoy is built to satisfy R's **rivals**: the excluded obvious rules
that are consistent with the examples, and, where possible, as many out-of-U predicates as the
true candidate does, so that "the candidate satisfying the most of my predicates" is a decoy at
least as often as not. Choosing correctly requires knowing which rule the class means — the
intersection trick has nothing to intersect. The floor is 1/k = 25 % (the foothold), a player who
has mapped U scores 100 %, and a player with a bigger universe is fooled exactly when a decoy
satisfies one of their surviving rules — which is the behaviour the organiser asked for.

Rules for the lineup:
1. Exactly one candidate satisfies R. Verify in generate().
2. Every decoy fails R but satisfies at least one **excluded** rule that is consistent with the
   examples (the trap), and at least one decoy should satisfy *more* of a reasonable outside
   predicate pool than the true candidate does (report the rate at which "most predicates wins"
   picks a decoy: target ≥ 40 %).
3. Decoys must not be trivially distinguishable (same length/size as the true candidate where the
   world has a size; no repeats of examples; drawn from the same instance distribution).
4. The clue format: examples, a blank line, then the candidates one per line. The scorer accepts
   the chosen candidate verbatim (whitespace-insensitive) or its 1-based index.
5. Drop the "fresh instance" clauses — they are no longer needed and were never legible.
5b. Refinement measured on tresk v2: give every candidate the SAME trap profile (the true one and the
   decoys fire exactly the same set of example-consistent excluded rules), otherwise "pick the
   candidate that satisfies the fewest excluded rules" is a free crack. With matched profiles every
   trap heuristic scores exactly chance and the only way up is reconstructing U.
5c. Measured on dornic v2: the *rarity-weighted* intersection (score each surviving outside
   predicate by −log of its base rate and pick the candidate with the highest total) is the
   smarter sibling of the count attack and is harder to blunt — 47 % on dornic after tuning,
   because the hidden rule is by construction the rarest thing the examples share. Test it in
   every lineup class; templates with two-step readouts (sums of a colour, primes) resist it best.
6. Witness table for revision 2: pick candidate 1 / a random candidate; pick the candidate that
   satisfies the most predicates from a broad outside pool; pick the candidate satisfying every
   rule in U that the examples allow (the in-U intersection — must be 100 %); pick by each excluded
   rule; a player who knows U minus its two rarest templates; the true rule.

## Revision 3 (2026-09-05): beat the free-label attack

**What runs 1 and 2 of the lineup pool showed.** Four Opus centaurs met the six lineup classes in
`lad-tresk-v2-1` and `lad-ospren-v2-1`. They spent **no demo** on the good ones and scored tavrik
85/96/89/89 %, tresk 79–86, wisbek 77–88, ospren 80–87; only dornic (59–66) and borsel (58–65) sat
on target, and only because their families are wide and cheap — several natural rules survive two
positives, which the players fairly called unfair. Both revision-2 defences were anticipated and
both lost.

**The attack to beat**, in the players' own words (`ospren1a`, `ospren1b`, `tresk1b` NOTES):

1. **Round 1: skip everything** — ~300 clues per class harvested free; that is the base-rate corpus.
2. **Round 2: answer a RANDOM candidate on every item.** With k candidates, 1/k come back correct:
   **~30 gold-labelled clues per class, for nothing** — "30× what a demo gives". A demo is one
   worked example; a round of random guessing is thirty. *This is the number that broke revision 2:
   the lineup that made the answer a choice also made every wrong guess a labelled datum.*
3. **Per clue**: enumerate 60–350 cheap predicates over the instance; keep those true of every
   example and of **exactly one candidate**; weight by rarity (`freq^-2.5 / satisfiers^6`, or
   −log base rate); answer the candidate the **rarest** survivor points at.
4. **Learn U from the labels**: measure which predicate was the *unique explanation* of each
   known-correct answer. ospren1a's learned list for tavrik was our U almost rule for rule, with
   the complement written out: "does not use word length, vowel count, palindromes, suffixes,
   semantics." Once U is learned the in-U intersection is 100 % and the lineup is a lookup.

**The diagnosis.** Matched trap profiles (§5b) and rarity-aware decoys (§5c) both failed for one
reason: **every rule of a revision-2 U was itself a cheap predicate in the attacker's bank.**
Measured for tavrik against a 627-predicate reconstruction of the three player banks, every rule of
v2's U had best Jaccard **0.97–1.00**. When the truth is in the bank *and* is by construction the
rarest thing the examples share, no amount of decoy matching helps: the truth is the answer to a
question the attacker already knows how to ask.

**The fix, in one line: put U outside the bank.** Make the rules **relations between two elements
or two positions** of the instance instead of properties of one element — and aim the decoys at the
attacker's *rarity* order rather than his count.

### Levers, measured on tavrik v3 (identical conditions, 400 clues, 60 free labels)

| build | k | floor | simulated attack |
|---|---|---|---|
| **v3 as shipped** | 5 | 20 % | **40.8 %** |
| minus lever 3: v2's own universe | 4 | 25 % | **98.0 %** |
| minus lever 5: decoys not aimed | 5 | 20 % | 54.2 % |
| minus lever 1: k = 4 | 4 | 25 % | 47.8 % |
| minus lever 2: three-example clues | 5 | 20 % | 44.2 % |
| lever 1 pushed: k = 6 | 6 | 16.7 % | 40.0 % |

**Worked.**
* **Lever 3 — a universe of RELATIONS (≈ 41 points, the whole game).** 15 of tavrik v3's 18
  templates relate two letters or two places: *the first and last letters are exactly n apart in
  the alphabet · a letter comes back after exactly one other letter · the 2nd letter and the
  2nd-from-last letter are the same · the first letter is the earliest in the alphabet of all its
  letters · the back half has more vowels than the front half · the first vowel is an e · the
  vowels go up the alphabet*. Best Jaccard against the 627-predicate bank: **0.08–0.75** (v2:
  0.97–1.00). They are still one-breath kid sentences — a kid is *good* at looking at two letters
  at once, and a predicate bank is bad at it.
* **Lever 5 — aim the RARITY order, not the count (≈ 13 points).** Revision 2 aimed the true
  candidate's rank on the *number* of surviving outside predicates. No player used that statistic.
  Both used **the rarest predicate that selects exactly one candidate**. So: carry the attacker's
  bank inside `generate`, intersect it over the examples, compute for every candidate the surprise
  of the rarest bank predicate that picks it *alone*, and aim the true candidate's rank in **that**
  order at a uniformly random place (then the count order, then the mutual-similarity order, as
  secondary aims). This works only once lever 3 is in place: when the truth's rule is not
  expressible in the bank, the truth's cheapest explanation is an accident of exactly the same kind
  as a decoy's, and a decoy carrying one at least as rare can always be found.
* **Lever 1 — five candidates (≈ 7 points).** Floor 20 %, one more decoy that must carry a rare
  example-consistent explanation, and a predicate is less likely to select uniquely. **k = 6 buys
  nothing** (−0.8, inside noise) and costs a clue line and a kid's patience. Five is the number.
* **Lever 2 — always the minimal example set, a PAIR wherever one exists (≈ 3 points).** tavrik v3
  is 99.8 % two-word clues. Every extra example is free information for the attacker's
  intersection and buys the designer nothing once U is an antichain.
* **Keep §5b.** Matched trap profiles now hold in the strong form: over 500 clues **all 3001 fitted
  traps are satisfied by all five candidates or by none**, so a player whose universe is U *plus*
  the excluded rules is worth exactly a player who knows U.

**Did not work / not used.**
* **Lever 4 (skew the draw toward the rare part of U) — dropped.** Once the rarity *order* is
  aimed, the truth's own base rate carries no signal, so skewing the draw only distorts the mix a
  kid feels. Measured: the truth's rank in the rarity order is uniform by construction; nothing
  left to buy.
* **Rules with density > .5** (e.g. "a letter and the very next letter of the alphabet are both in
  the word", .603) look attractive as anti-rarity rules but are unusable in a lineup: with five
  candidates, four decoys all *lacking* a common property is itself a signature.
* **Length-conditioned templates** ("the middle letter is a vowel", odd words only) leak through
  the lineup, because all candidates share a length.
* **Competitor-only templates** (§Revision 2, "exactly n vowels") turned out to be unnecessary once
  the loose vowel-count cousins are pure traps: dropping them shortened the clue to two words.
* **More labels stop paying.** The point of the design is the *shape* of the curve: tavrik v3 goes
  39.6 % (0 labels) → 42.2 (30) → 42.4 (60) → 44.2 (240), i.e. flat, where v2 went 91.2 → 97.6 →
  98.0 → 99.4. Free labels are only worth something if the vocabulary can express U.

**The ceiling stays where it belongs.** The in-U intersection is **100.0 %** on v3. An attacker
handed the bank *plus* all of U scores 79.8 / 88.0 / 95.6 / 99.2 % at 0 / 30 / 60 / 120 labels and
learns 90 % of U in ~360 labels. With the generic bank alone, U-coverage can never pass the cheap
templates (24.6 % of tavrik's clues). The gap 42 % → 96 % **is** the class: it is paid for by
inventing the right vocabulary, which is the insight the ladder wants to reward.

### Recipe for the other five lineup classes

tresk (beads), wisbek (clock), ospren (5×5 pictures), dornic (cards), borsel (dice) should each
run this, in order:

1. **Rebuild the attacker's bank for your world** from the players' own code — their feature banks
   are in `sim/results/lad-tresk-v2-1/players/*/strategy.py` and
   `sim/results/lad-ospren-v2-1/players/*/{strategy.py,features.py}` — and add the obvious
   extensions. 200–650 realised (key, value) predicates.
2. **Score every rule of your U against it by Jaccard** over your instance pool. **Any rule with
   J > 0.8 is a gift.** Retire it to the trap list.
3. **Replace it with a relation between two elements or two positions**, still one breath:
   * *tresk*: the two ends are different colours · the 2nd bead matches the 2nd-from-last · there
     are exactly n beads between the two greens · every red has a blue right after it · the back
     half has more reds than the front half · the longest run is the colour it starts with.
   * *wisbek*: the two minute digits differ by n · the hour is one of the minute digits · the
     minute digits add up to the hour · the second minute digit is bigger than the first.
   * *ospren*: every filled cell has a filled cell directly below it · the top row and the bottom
     row are the same · row n matches column n · the left half holds as many marks as the right.
   * *dornic*: the highest card is a heart · two cards are next to each other in value · there are
     as many hearts as spades · the first and last card share a colour.
   * *borsel*: two dice differ by exactly n · the biggest die is the last one · the first two add
     up to the last · no two dice are next to each other in value.
4. **Keep two or three CHEAP templates on purpose, at double draw weight** (~25 % of clues) as the
   learnable slope and as continuity with your v2. Without them the attack sits at the floor and
   the class reads as arbitrary; with them it sits at ~40 % and rewards labels.
5. **k = 5 candidates**, one length/size, minimal example set, **pair first**.
6. **Verify the antichain** over the example pool *and* the full instance universe.
7. **Aim three orders** in `generate` (rarity first, then count, then mutual similarity) and keep
   §5b's matched trap profiles; check the strong form (every fitted trap all-or-none).
8. **Simulate the attack before shipping.** The witness table for revision 3 must add:
   the full engine (skip-harvest base rates → random-candidate labels → per-predicate
   unique-explanation weights → rarity-weighted pick) at **0 / 30 / 60 / 120 / 240 labels**; the
   same engine with a bank that also contains all of U (the honest ceiling); the **in-U
   intersection, which must be 100 %**; the number of labels to learn U to 90 % coverage; and the
   lever ablation (k, aiming on/off, example count).
   **Target: 35–55 % at 30–60 labels**, and a curve that is flat in the number of labels. The
   simulator is a *lower* bound on a real Opus centaur — on tavrik v2 it scored 91–98 % where they
   scored 85–96 % — so aim at the middle of the band, not the bottom.
9. **Re-read the rules aloud.** If a 12-year-old cannot check a candidate against the rule by hand
   in a few seconds, the relation is too clever. "The second letter and the second-from-last letter
   are the same" passes; "the letters' alphabet positions sum to a multiple of the length" does not.

### Addenda from tresk v3 and wisbek v3 (2026-09-05)

* **Retire by J × rarity, not J alone.** A bank predicate helps the attacker only when it selects
  exactly one candidate, so a *dense* predicate is worthless even at J = 1.00 (wisbek: "twins",
  density .10, pays 47 %; "the hour turns up again", .20, pays 19 %; the one-per-hour families,
  .017, pay 98–100 %). Cheap templates kept as the learnable slope should be the dense ones.
* **Lever 0 — choose the example set that hides the rule from the bank.** Among minimal example
  pairs, prefer one for which no surviving bank predicate implies the rule (wisbek: opposite sides
  of the face for "n apart"; one all-odd and one all-even time for "all one kind"). Worth ~5 points;
  took wisbek's "n apart" family from 47 % to 6 %.
* **Small universes cannot hold §5b in the strong form** (wisbek: 720 times; forcing agreement on
  ~9 fitted traps empties the pool). Make trap matching a preference inside the aimed rank and
  measure "most/fewest excluded rules" against the floor instead (wisbek: 26 % / 17 % vs 20 %).
* **Kid score follows the kind of relation.** tavrik v3 (counted relations: alphabet distance,
  "comes back after n letters") fell 4.7 → 3.83; tresk v3 (visual relations only: ends match, a
  clump touches the end, every red followed by a blue) rose 4.0 → 4.5. Relations must be things a
  kid spots by eye.
