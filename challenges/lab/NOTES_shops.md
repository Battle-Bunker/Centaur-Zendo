# NOTES — direction: shops, money and swapping (designer, 2026-09-05)

Brief: new format (7 classes, 4 rounds × 0.5 s, 3 demos per team per game). Copy what makes
fennick v3 and durnel work: **the clue is the drawn object plus a caption naming the verb and a
number**; **the rule is ONE physical/social clause a kid says in a breath**; **the answer is the
clue's picture edited**, unique; every demo carries its own near-misses; the "return the clue
unchanged" witness pays only on the caption's zero cases. Extra constraint from the direction:
**no arithmetic-as-rule** (sums, prices, change) — the players' predicate banks eat those.

## The 12-year-old test applied to 12 ideas

| # | idea | object a kid names? | rule in one breath? | *not* the model's first guess? | edit unique? | verdict |
|---|---|---|---|---|---|---|
| 1 | **Shelves and the things put back wrong**: 5 shelf rows of goods (letters); a shelf belongs to the kind most of its goods are; caption `2 swap`. Two goods swap iff they stand **in line (same slot)** and **each is on the other's shelf**. Edit: those cells become their shelf's letter. | yes — "shelves in a shop, someone's put things back wrong" | "those two are in line and each is on the other's shelf — swap them" | the famous operation is *tidy everything up* (scores 0 here); "all the mutual pairs" is the canonical blind guess and it scores **0**; the alignment clause is the arbitrary-but-natural half | yes, exactly 2n cells | **CHOSEN** |
| 2 | **Sticker swaps**: kids' rows of stickers; you swap a double for one the other hasn't got. | yes | yes | **no** — "swap doubles for missing" is the first thing any model writes, and the tidy-up is canonical | the rewritten rows are not canonical (where does the swapped sticker go?) | reject |
| 3 | **What fits in the bag**: boxes on the counter, a bag of depth D; a box gets laid on its side iff it is too tall to stand but not too wide. | yes | yes ("turn it sideways") | half — it is one comparison, and "does it fit" is a model's first hypothesis; also it is bin-packing-adjacent (Wikipedia) | the rotated footprint reflows the row unless slots are pre-sized | reject (arithmetic-shaped, and durnel already owns "under a height limit") |
| 4 | **Which shelf empties**: customers take goods off shelves in some order. | yes | no — **stateful**, the scorer must simulate a queue | — | yes | reject (not one clause) |
| 5 | **Tills and queues**: several checkouts, a queue of heads under each; who hops to another queue. | yes | "you go to the shortest queue" | **no** — famous and obvious; the arbitrary versions ("everyone shuffles left") are not natural | yes | reject |
| 6 | **Coins on the counter**: which coins the shopkeeper sweeps into the till. | yes | only if the rule is about value | — | yes | reject (money ⇒ arithmetic, banned) |
| 7 | **Odd shoe on the shoe-shop shelf**: a shoe goes back in its box iff its partner is missing. | yes | yes | **no** — "find the unmatched one" is a textbook predicate | yes | reject |
| 8 | **Price labels on the shelf edge**: which item is standing over the wrong label. | yes | yes | no — the mismatch is directly readable off the picture, one probe | yes | reject (too easy) |
| 9 | **Jars that get topped up**: a jar is refilled iff it holds less than both its neighbours. | yes | yes | **no** — "local minimum" is a model's second guess | yes | reject |
| 10 | **The market aisle**: two facing shelf rows; a good is taken iff the same kind faces it across the aisle. | yes | yes | half — "directly opposite" is the first probe anyone runs on two rows | yes | weak version of #1; folded into it as the *alignment* clause |
| 11 | **Trolley bay / nested trolleys**: which trolley can be pulled out. | yes | yes | **no** — "only the front one" | trivial | reject |
| 12 | **Everyone goes home round the ring**: same picture as #1 but every ring (2-way *and* 3-way) resolves. | yes | yes | **no** — the permutation-cycle decomposition is exactly what a model reaches for | yes | reject, and **kept as the decoy**: every clue contains a three-way ring that does *not* resolve |

## Why #1 wins

* **The object is instant and the scene is the archetypal shop job.** Rows of goods with shelf
  edges under them; a few things standing on the wrong shelf; a caption naming the verb (`swap`)
  and the count. A kid names the object and the *problem* from one glance.
* **The measurement has no name.** "A vertical pair that is the wrong way round" is not a thing
  anybody has a word for. It is the LegoZendo/virel shape (a coincidence between two items that
  needs *two* independent coincidences at once), transplanted into a shop.
* **It is not the object's famous operation.** The famous operation is "put everything back where
  it belongs" — measured at **0.0 %** here, because every clue contains strays that stay put.
* **The blind-canonical deduction fails.** A player with no demo who reasons "a swap needs two
  things to trade places, so it must be the pairs that are on each other's shelves" scores
  **0.0 %**. That single fact is what puts the class on the edge of needing a demo, and it is why
  the alignment clause was added after the first build (see below).
* **One demo teaches the whole rule**, because the 2×2 is always complete in the picture:
  in line + mutual (swaps), in line + not mutual (stays), mutual + not in line (stays), and
  neither (stays), plus a stray in line with a *gap* and one in line with a *plain* good.
* **The foothold is fennick's/durnel's**: 12.1 % of clues say `0 swap`, where the correct answer
  is the clue returned unchanged — and those clues look exactly like the others (they still have
  mutual pairs, a ring, strays in line), so the foothold is not visible from the picture.

## Design decisions taken while implementing (the record; the JSON's `description` is canonical)

* **Slots, not free text.** Every shelf is a fixed grid of 10–12 slots drawn one character apart,
  so "in line" is unambiguous for a human and costs the scorer nothing (string index = slot).
* **No shelf labels.** DESIGN_LOOP: prefer drawing the object over adding legends. A shelf
  belongs to the letter most of its goods are; measured margin ≥ 2 on every row of every clue, so
  the majority read is never a coin-toss (this also keeps the scorer deterministic under Python's
  hash randomisation, which would otherwise break a tie differently in different processes).
* **At most one stray of a kind per shelf**, so a swap partner is never ambiguous and n is
  well-defined.
* **Gaps are placed after the strays and never on one**, so blanking can neither create nor
  destroy a swap; the final `len(sw) == 2n` check re-derives the truth from the drawn picture.
* **The zero-branch coin flip is drawn before the retry loop** (durnel's lesson) so `0 swap`
  clues are not over-represented by the rejection filter: measured 12.1 %.
* **n ∈ {2, 3}, never 1**, so a single lucky pair-guess is not enough.

### What was tuned during the build

1. **v0 had no alignment clause** — the rule was just "each on the other's shelf". Measured: the
   blind-canonical guess *is* the rule, so a player who never spends a demo could deduce it from
   the caption alone. Adding "in line" broke that (0.0 %) while keeping the sentence one breath
   long, and it turned the old rule into the top decoy.
2. **One non-aligned mutual pair was not enough.** With n aligned pairs and 1 spare, a player who
   found mutuality but missed alignment could guess which n of the n+1 pairs were meant and score
   **36.5 %**. Two spares (1/C(n+2,n)) cut that to **23.8 %**.
3. **"Tidy the whole column" paid 36.5 %** until every clue was made to carry a *third* stray
   standing in one of the swapping columns; now 15.9 % (12 of which is the foothold).
4. **A stray in line with a gap** is planted in every clue, so "it goes home if there's a space
   for it right there" is visibly false (0.0 %).
5. Scorer written as one comprehension over the clue's rows: **347/512 chars**, 0.03 ms.

## Implementation record — `molvic` v1 (2026-09-05)

Shipped as `challenges/lab/molvic.json` (private notes in its `description`). No arena run: the
brief stopped at self-testing.

* `python tools/quickcheck.py challenges/lab/molvic.json --seeds 200` → **OK**
  (`gen=0.35 ms score=0.06 ms solve=0.06 ms` worst call in the sandbox; one warning, "score
  accepts the clue itself" — that is the intended `0 swap` foothold, exactly as fennick/durnel).
* 3000–4000 fresh seeds: generate mean 0.15 ms / p99 0.36 / max 0.7, 0 fallback uses, all
  deterministic, 3000/3000 distinct clues; solve 0.026 ms; score 0.03 ms real / 0.026 ms junk
  (incl. 4000-char junk). Sizes: score **347**/512, solve 791/5000, generate 5.3 k/50000,
  clue and solution 226–266/1024.
* Plant audit (3000 clues): two mutual-but-not-in-line pairs 100 %, in-line-but-not-mutual pair
  100 %, three-way ring 100 %, swaps next door *and* across 100 %, shelf with a mover and a
  stayer 100 %, stray in line with a gap 100 %, stray in line with a plain good 99.1 %, third
  stray in a swapping column 99.4 %, movers ≠ the first strays read off 100 %.
* Cross-check: an independent re-implementation (slot-space parse, `Counter` majority, picture
  rendered from scratch) agreed with `solve`/`score` on **1500/1500** clues, 0 disagreements.
* Uniqueness: 16 611 single-character mutations of true answers, **0** still scored 1.
* Attack table (2000 fresh clues): top rival **23.8 %** ("mutuality found, alignment missed —
  guess n of the n+2 mutual pairs"), then 15.9 % ("tidy the swapping columns"), 12.6 %
  ("the leftmost columns holding two strays"), and the ~12 % family that is really the foothold.
  Everything that ignores either half of the rule is 0.0 %. True rule 100 %.

## Levers if it drifts

* **Too easy**: (a) require the caption dropped (removes the identity foothold and the offline
  checksum); (b) allow two strays of the same kind on one shelf so "in line" needs disambiguating;
  (c) add a good whose kind is no shelf's kind — it belongs in another shop and never moves.
* **Too hard**: (a) drop the alignment clause (measured: that is the blind-canonical guess, so it
  would make the class much easier); (b) draw one swap already done into the clue as a worked
  instance; (c) drop to three shelves.
