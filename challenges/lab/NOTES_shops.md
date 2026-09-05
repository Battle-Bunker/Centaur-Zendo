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

---------------------------------------------------------------------------

## Refinement record — `molvic` v2 (2026-09-05, refiner)

### What the players did to v1 (`sim/results/lad-durnel-v2-1/`)

Both Opus players finished **100 % / 100 % on molvic without spending a demo** (56/56 and 52/52
verified in training, then 100 % of the final; cracked in round 2 by both). Player a's NOTES:
*"5 rows, each with a majority letter. Event = two cells in the SAME COLUMN, rows i,j, with
cell(i)=maj(j) and cell(j)=maj(i). N = number of such mutual pairs (verified 56/56). Answer =
grid with those swaps applied."* Player b spent its three demos on virel, kelmar and garrow and
wrote *"deliberately no demo on molvic (I had already reasoned the swap rule)"*.

This is durnel v1's failure, exactly as DESIGN_LOOP's "checksum caption" section predicts: the
`n swap` caption is a checksum, so a rule can be falsified offline against ~55 harvested clues at
zero cost — and v1's rule reproduced `n` on 100 % of them at the second guess, while the edit
(swap the two letters) was guessable from the picture, so knowing the rule was the whole game.
The judge added the other half of the problem (kid 3.67): *"the demo picture is dense (7-14 strays
across 5 shelves) so the in-line+mutual signal is buried"*.

### The v2 change (levers (a) + (b) + (c) of the brief, in one physical story)

A shop assistant does not swap two tins over the aisle — **he puts each one back on its own
shelf, in the first free space, and if that shelf is chock-a-block he leaves it where it is.**

> those two are in line and each one's on the other's shelf, so they go home — into the first gap
> on their own shelf; and if a shelf is full there's nowhere to put it, so it stays.

* **(a) the edit needs the demo.** The mover is erased from where it stood (its slot becomes a
  gap) and redrawn in the FIRST GAP of its own shelf — a slot nothing in the clue points at, and
  usually far from the column it stood in (82 % of movers land to the *left* of their old column).
  Every clue is built so that at least one mover's landing gap is neither the nearest gap to its
  column nor the nearest gap on its left, so "the first gap" is forced by one demo but cannot be
  guessed. Measured: v1's rule rendered v1's way (swap in place) now scores **0.0 %**.
* **(b) the natural blind rule is now wrong.** Because a good needs somewhere to land, a **full
  shelf refuses it**. Every clue plants an in-line mutual good whose own shelf has no gap at all
  (100 %, audited over 4000 clues), so the players' rule — "n = the mutual pairs in the same
  column" — reproduces the caption on **0.0 %** of clues instead of 100 %. The offline checksum
  now falsifies the first sensible reading instead of confirming it; with a demo it is a 100 %
  verifier again, which is what it is for.
* **(c) the judge.** 4 shelves (was 5), 5–8 strays (was 7–14), 9–12 slots. The only thing that
  ever happens is in a column where two strays stand one above the other, and the shelf that
  refuses is visibly packed solid. No count-based crack was opened: every count/position template
  in the table below sits at or under the 12 % foothold.

Kept from v1: the object (a drawn shelf unit, goods as letters, gaps as holes), the checksum
caption (`n home` — the verb changed because the goods no longer swap), the one-clause rule, the
unique answer, the ~12 % `0 home` foothold, and the whole family of near-miss plants.

### An exhaustive check of what the caption alone can tell a player

A search over conjunctions of nine natural per-stray predicates (in line with a mutual partner /
mutual anywhere / in line with any stray / room at home / standing on a full shelf / a gap in line
at home / home above or below / left half / a gap next door) finds exactly **two** rules that
reproduce the caption on all 1200 clues: the true one, and its **twin** *"in line, mutual, and the
shelf it is STANDING on is not full"* — which counts the same in every pair but picks the *other*
good, and cannot be drawn at all (it would send a good to a full shelf). Nothing simpler survives:
"in-line mutual pairs" reproduces the caption on 30.8 % of clues, "pairs with room for both" on
11.8 %, v1's rule and every alignment- or mutuality-free reading on 0.0 %.

### Witness table, before → after (1500 fresh clues each, shipped scorers)

| template (rendered with the true drawing convention unless marked BLIND) | v1 | v2 |
|---|---|---|
| **BLIND: v1's rule + v1's edit (the two swap over where they stand)** | **100.0 %** | **0.0 %** |
| BLIND: the same, only the pairs with room, swapped in place | — | 12.3 % |
| BLIND: in-line mutual goods rubbed out | — | 0.0 % |
| BLIND: tidy up — every stray put right where it stands | 0.0 % | 0.0 % |
| clue returned unchanged (the foothold) | 11.8 % | 12.3 % |
| clue unchanged, caption dropped | 11.8 % | 12.3 % |
| n mutual pairs picked at random (v1's top rival) | **23.8 %** | n/a |
| only the good on the LOWER shelf of each pair goes home | — | **20.7 %** |
| only the good on the UPPER shelf of each pair goes home | — | 19.9 % |
| n strays at random go home | 12.1 % | 16.1 % |
| every in-line mutual good goes home (fullness ignored) | — | 0.0 % |
| the whole pair goes home if either of the two has room | — | 12.3 % |
| TWIN rule (the good on a shelf that has room), moved / swapped | — | 12.3 / 12.3 % |
| true movers → the LAST gap / nearest gap / nearest gap on the left | — | 12.3 % each |
| true movers → the first gap on the shelf they were standing on | — | 12.3 % |
| true movers, old slot filled by the partner (swap AND move) | — | 12.3 % |
| true movers, old slot filled by the shelf's own letter | — | 12.3 % |
| true movers copied home, old slot left as it was | — | 12.3 % |
| true movers rubbed out, never arriving | — | 12.3 % |
| true movers, and the refused goods vanish too | — | 0.0 % |
| a good needs a gap IN LINE at home | 0.0 % | 12.3 % |
| any stray with a gap on its own shelf goes home | 0.0 % | 0.0 % |
| any stray in line with another stray goes home | 0.0 % | 0.0 % |
| any mutual stray (alignment ignored) goes home | 0.0 % | 0.0 % |
| any stray on a FULL shelf with room at home goes home | — | 0.0 % |
| the first n strays in reading order / on the fullest shelf | 11.8 % | 12.3 / 6.4 % |
| the swapping columns tidied completely | 15.9 % | n/a |
| one fixed real answer for every clue / demo replay | 0.1 / 0.0 % | 0.0 / 0.0 % |
| **TRUE RULE (solve), caption kept / dropped / rows padded** | 100 % | **100 %** |

Fourteen well-formedness attacks (gaps as dots, lowercased, shelf edges removed, slot spacing
squeezed out, rows reversed, caption count changed, the answer twice, a junk line appended, half
the picture, the caption alone, the empty string, 4000 chars of junk, one fixed answer, another
clue's answer) all score 0.0 %; trailing newlines, trailing whitespace per row and the caption
present-or-absent are the declared leniencies and score 100 %. 15 390 single-character mutations
of true answers: **0** still scored 1.

### One rendered demo (clue, then the answer solve() returns)

    |H H S J H     H  |            |H H S J H H   H  |
    +-----------------+            +-----------------+
    |S   S J S   C S  |            |S S S J S     S  |
    +-----------------+            +-----------------+
    |J J J H J S C J J|            |J J J   J S C J J|
    +-----------------+            +-----------------+
    |C   C C C C S   C|            |C C C C C C     C|
    +-----------------+            +-----------------+
    3 home                         3 home

The shelves are for H, S, J and C. The **J shelf is packed solid** — no gaps anywhere. In slot 3
an `H` stands on the J shelf and a `J` stands on the H shelf: in line, each on the other's shelf.
The `H` goes home into the first gap on the H shelf (slot 5, four slots away from where it was);
the `J` cannot go anywhere, because the J shelf is full, so it stays. In slot 6 a `C` stands on
the S shelf and an `S` stands on the C shelf: both shelves have gaps, so both go home, each into
the first gap on its own shelf (slot 1 both times). The `C` on the J shelf (slot 6) is in line
with that pair and has room at home, but nothing on the C shelf stands in line with it, so it
stays; the `S` on the J shelf (slot 5) has a *gap* in line on its own shelf and still stays; the
`S` on the H shelf (slot 2) is a lone stray. Six characters change, `3 home`.

### Engineering (4000 fresh seeds)

generate mean 0.34 ms, p99 1.26, max 4.1, **0 fallback uses**, 2000/2000 clues distinct and
deterministic (byte-identical under four PYTHONHASHSEEDs — the majority read is safe because the
shelf letter wins by ≥ 2 on every row); solve 0.012 ms; score 0.014 ms real / 0.015 ms junk;
**scorer 494/512 chars**, solve 1077, generate 8.0 k, clue and solution 166–198 chars, 1000/1000
answers distinct. `n` is 0 (12.1 %), 1 (15 %), 2 (22 %) or 3 (51 %); no two goods ever want the
same shelf (generation rejects it, so the first-gap rule stays unambiguous and the answer unique).
An independent re-implementation agreed with solve/score on 1200/1200 clues.
`python tools/quickcheck.py challenges/lab/molvic.json --seeds 200` → **OK**
(`gen=2.03 ms score=0.08 ms solve=0.04 ms` worst call in the sandbox; the single warning "score
accepts the clue itself" is the intended `0 home` foothold, exactly as fennick/durnel).

### Prediction

**too_easy → testing, on fennick's profile: ~12 % without a demo, ~95–100 % with one** (mean ≈ 50 %
over two players in a 7-class pool where one of them spends a demo here). The risk is now the
durnel v2 risk in both directions: the demo-holder must read three things off one picture pair
(which goods, where they land, and why one of them didn't move), and a theorist without a demo
might still find the count rule offline — it needs two conjuncts, one of which ("there is room at
home") only makes sense once you believe the good *moves* — and then buy the landing convention
with live probes. If a pair of demo-holders comes back at 0–10 %, soften with the JSON's "too
hard" levers: draw one good already put away in the clue as a worked instance, or give every
mover's shelf exactly one gap so that "the first gap" is just "the gap".

---------------------------------------------------------------------------

## Re-skin record — `molvic` v3 (2026-09-05, refiner)

v2 kept as `challenges/lab/molvic.v2.json` (byte-identical copy); v3 is `challenges/lab/molvic.json`.
**The rule, the counts, the plants, the foothold and the witness profile are untouched.** Only the
drawing changed. This is garrow v4's move (NOTES_kitchen.md §v4: the tray that read as a fish tank)
applied to the shop: DESIGN_LOOP lever 9, *salience beats rule changes*.

### Why: the judge did not see a shop

molvic v2 scored **kid 2.67** (object 2, fun 2, kid_contributes 2, rule_statable 3, clue_shape 4):

> "Rule engineering excellent but the rendering is an abstract letter table … a grid of capital
> letters between `|` and `+---+` is a data table, not a drawing of a shop shelf; a kid would say
> *'rows of letters where one letter repeats a lot'*, not *'oh, a shop!'*; comparing two dense
> letter grids character by character is a chore."

v1 had already been marked down for the same family of thing (kid 3.67, "dense, 7–14 strays, the
swap signal is buried"). v2 fixed the density (4 shelves, 5–8 strays) and the judge still called it
a table, so the remaining problem was not *how much* is drawn but *what the glyphs are*. Three
things in v2 were doing damage at once: (a) a shelf's identity had to be **tallied** — you found
the majority letter of a row before you could say what the shelf was for; (b) a stray was a single
capital among other single capitals, so finding one meant reading columns; (c) an empty slot was a
**blank**, i.e. nothing, so "the first empty slot on its own shelf" — half the rule — pointed at
something invisible.

### What v3 draws

```
     +=========== THE CORNER SHOP ===========+
COD  |cod cod cod cod cod cod rye wax cod cod|
     +---------------------------------------+
RYE  |rye rye rye cod log rye ___ rye ___ rye|
     +---------------------------------------+
LOG  |log log log log rye log log wax log log|
     +---------------------------------------+
WAX  |___ wax wax wax wax ___ wax cod wax ___|
     +---------------------------------------+
2 home
```

1. **The home shelf is written, not inferred.** `COD  |`, `RYE  |`, `LOG  |`, `WAX  |` at the left
   edge. "It goes home" is now a place you can point at. (The majority still wins by ≥ 2 on every
   row — verified on 1200 clues — so the written and the tallied reading never disagree; the scorer
   simply reads the label, which is *cheaper*: 496 chars against v2's 494 with a majority in it, and
   immune to a hash-order tie.)
2. **Goods are lowercase 3-letter words that match the label.** `cod cod cod … rye wax cod` instead
   of `C C C … R W C`. A stray is now a different **word** in a row of identical words; the eye
   lands on `rye wax` in the COD row without counting columns. Lowercase goods under a capital
   label also make the label unmistakably a label and not another good.
   The 21 kinds are three-letter shop goods, one per letter of the old alphabet, so the first
   letter still identifies the kind and nothing downstream changed: `ale bun cod dip egg fig gum ham
   jam keg log mop nut pie rye soy tea urn veg wax yam`.
3. **The gap is a thing you can point at**: `___`, not a blank. "The **first** empty slot on its own
   shelf" is the half of the rule that must be bought with a demo, and it now has a visible object
   with a position in the clue. Measured: **100 %** of movers land on a gap that is drawn `___` in
   the clue, so both ends of every edit are visible before the answer is drawn (new plant P9).
4. **Full is loud.** A full shelf is a solid run of one word — `log log log log rye log log wax log
   log` has no `___` anywhere — so "there's nowhere to put it" is a property of the picture, not a
   scan. Above, `wax` sits on the COD shelf and `cod` sits on the WAX shelf in slot 7: the `wax`
   goes home (WAX has gaps, first one is slot 0), the `cod` cannot, because the COD shelf is solid.
5. **Flavour that carries nothing.** The fixed sign `THE CORNER SHOP` is set into the top edge of
   the unit. It is identical in every clue apart from its width (which the shelf edges already
   show), so it can carry no information; it is there so that the first two seconds of looking end
   in "that's a shop". No price tags: they would widen the row without adding a reading.

Not changed: 4 shelves, 9–11 slots, 5–8 strays, ≤ 3 strays per shelf, one or two full shelves, 2–3
gaps on the others, the `<n> home` checksum caption, the ~12 % `0 home` foothold, plants P1–P8, and
the "no two movers want the same shelf" guard. `generate()` makes the same decisions in the same
order from the same RNG stream as v2 — only the last five lines, which render the picture, differ.

### Proof that nothing moved: v3 is a relabelling of v2

For 2000 consecutive seeds, v2's and v3's clues were reduced to the same abstract object (per row
and slot: *the shelf's own kind* / *a gap* / *the index of the shelf this good belongs to*) plus n.
**0 structural mismatches**, identical n on every seed, identical n distribution.

### Witness table, v2 → v3 (1500 fresh clues each, seeds 4 000 000–4 001 499, shipped scorers)

Same 34 templates as the v2 record, run against both builds in the same process.

| template (rendered with the true drawing convention unless marked BLIND) | v2 | v3 |
|---|---|---|
| BLIND: in-line mutual pairs swapped in place (v1's rule + v1's edit) | 0.0 % | **0.0 %** |
| BLIND: the same, only the pairs with room, swapped in place | 12.3 % | 12.3 % |
| BLIND: in-line mutual goods rubbed out | 0.0 % | 0.0 % |
| BLIND: tidy up — every stray put right where it stands | 0.0 % | 0.0 % |
| clue returned unchanged (the foothold) | 12.3 % | **12.3 %** |
| clue unchanged, caption dropped | 12.3 % | 12.3 % |
| only the good on the LOWER shelf of each pair goes home | 20.7 % | **20.7 %** ← top rival |
| only the good on the UPPER shelf of each pair goes home | 19.9 % | 19.9 % |
| n strays at random go home | 16.1 % | 16.5 % * |
| every in-line mutual good goes home (fullness ignored) | 0.0 % | 0.0 % |
| the whole pair goes home if either of the two has room | 12.3 % | 12.3 % |
| TWIN rule (the good on a shelf that has room), moved / swapped | 12.3 / 12.3 % | 12.3 / 12.3 % |
| true movers → the LAST gap / nearest gap / nearest gap on the left | 12.3 % each | 12.3 % each |
| true movers → the first gap on the shelf they stood on | 12.3 % | 12.3 % |
| true movers, old slot filled by the partner (swap AND move) | 12.3 % | 12.3 % |
| true movers, old slot filled by the shelf's own goods | 12.3 % | 12.3 % |
| true movers copied home, old slot left as it was | 12.3 % | 12.3 % |
| true movers rubbed out, never arriving | 12.3 % | 12.3 % |
| true movers, and the refused goods vanish too | 0.0 % | 0.0 % |
| a good needs a gap IN LINE at home | 12.3 % | 12.3 % |
| any stray with a gap on its own shelf goes home | 0.0 % | 0.0 % |
| any stray in line with another stray goes home | 0.0 % | 0.0 % |
| any mutual stray (alignment ignored) goes home | 0.0 % | 0.0 % |
| any stray on a FULL shelf with room at home goes home | 0.0 % | 0.0 % |
| the first n strays in reading order / on the fullest shelf | 12.3 / 6.4 % | 12.3 / 6.4 % |
| one fixed real answer for every clue / demo replay | 0.0 / 0.0 % | 0.0 / 0.0 % |
| **TRUE RULE (solve), caption kept / dropped / rows padded** | **100 %** | **100 %** |

\* the only row that moves: that template seeds `random.Random(clue)` on the clue *text*, which is a
different string in the new skin. Every other row is identical to the tenth of a percent. Top rival
still **20.7 %**, foothold still **12.3 %**, true rule still **100 %**.

**Well-formedness: 14 attacks × 1500 clues, all 0.0 %** — gaps drawn as dots, lowercased, shelf
edges removed, slot spacing squeezed out, rows reversed, caption count changed, the answer sent
twice, a junk line appended, half the picture, the caption alone, the empty string, 4000 chars of
junk, one fixed answer, another clue's answer. Six more aimed at the new skin, also **0.0 %**: the
shop-sign line removed, the shelf labels stripped, gaps drawn as three blanks, goods abbreviated
back to single capitals (the v2 skin), labels lower-cased with a correct picture, a blank line
inserted between shelves. Declared leniencies unchanged and still 100 %: trailing newlines,
trailing whitespace on any row, caption present or absent.
Uniqueness: **747 270** single-character mutations of true answers and **64 400** single-slot
mutations (every slot swapped for every other kind and for a gap) — **0** still scored 1.

### Plant audit and demo legibility (4000 fresh seeds)

P1 refused in-line mutual good 100 %; P2 mutual pair not in line 100 %; P3 third stray in a
going-home column 100 %; P4 stray on a full shelf with room at home 100 %; P5 stray with a gap in
line at home 100 %; P6 the first gap is neither the nearest gap nor the nearest gap on the left
100 %; P7 movers ≠ the first n strays 100 %; P8 climbers and descenders when n ≥ 2 100 % (2846/2846);
**P9 (new) every mover's landing gap is drawn `___` in the clue 100 %**.

**The moving pair is visually distinct in 100 % of demos**: in every clue with n > 0 (3499 of 4000),
every mover's source slot holds a word that differs from its shelf's label, and every mover's
landing slot is an explicit `___` in the clue — so both ends of each of the 2n changed slots are
visible objects before the answer is drawn, and no column-counting is needed to see the edit.
Movers land **82.3 %** of the time to the *left* of the column they stood in, mean shift 4.4 slots,
so the landing place still has to be learned from a demo — the point of the class is intact.

### One rendered demo (seed 245; clue on the left, `solve()`'s answer on the right)

```
     +=========== THE CORNER SHOP ===========+       +=========== THE CORNER SHOP ===========+
COD  |cod cod cod cod cod cod rye wax cod cod|  COD  |cod cod cod cod cod cod rye ___ cod cod|
     +---------------------------------------+       +---------------------------------------+
RYE  |rye rye rye cod log rye ___ rye ___ rye|  RYE  |rye rye rye cod log rye rye rye ___ rye|
     +---------------------------------------+       +---------------------------------------+
LOG  |log log log log rye log log wax log log|  LOG  |log log log log ___ log log wax log log|
     +---------------------------------------+       +---------------------------------------+
WAX  |___ wax wax wax wax ___ wax cod wax ___|  WAX  |wax wax wax wax wax ___ wax cod wax ___|
     +---------------------------------------+       +---------------------------------------+
2 home                                          2 home
```

Four shelves: cod, rye, logs, wax. **The COD and LOG shelves are solid** — not one `___` on either.
Slot 7: a `wax` on the COD shelf and a `cod` on the WAX shelf, in line, each on the other's shelf.
The `wax` goes home into the **first** `___` on the WAX shelf (slot 0, seven slots to its left, and
neither the nearest gap — slot 5 — nor the nearest on its left); the `cod` cannot go anywhere,
because the COD shelf has no gap at all, so it stays (P1). Slot 4: a `rye` on the LOG shelf and a
`log` on the RYE shelf; the `rye` goes home into the first `___` on the RYE shelf (slot 6), the
`log` is refused by the solid LOG shelf (P1 again). The near-misses are all on the picture: `wax`
also stands on the LOG shelf in slot 7 — the same column as a going-home pair, with room at home —
and stays (P3); `rye` stands on the packed COD shelf in slot 6, with room at home, and stays (P4) —
and there is a `___` in line right under it on its own RYE shelf, which does not help it (P5);
`cod`@3 on RYE and `rye`@6 on COD are on each other's shelves but not in line, so neither moves
(P2). Four slots change, `2 home`.

### Validation and engineering

`python tools/quickcheck.py challenges/lab/molvic.json --seeds 200` → **OK**, four times
(`gen=1.38 ms score=0.09 ms solve=0.04 ms` worst call on the quietest run; on a box under load
average 3.5 the same run reports up to 4–9 ms for *any* of the three, including `score`, whose real
cost is 0.015 ms — scheduler noise, not the class; caps are 100/50/2000 ms). The single warning
"score accepts the clue itself" is the intended `0 home` foothold, exactly as fennick/durnel/v2.

4000 fresh seeds: generate mean **0.45 ms**, median 0.27, p99 4.7, max 8.8 — v2 measured back to
back on the same (busy) box: 0.44 / 0.26 / 4.6 / 9.0, so the re-skin costs nothing; **0 fallback
uses**; 2000/2000 clues distinct and byte-identical under four PYTHONHASHSEEDs; solve 0.019 ms;
score 0.015 ms on real answers and on 4000-char junk; `score(clue, solve(clue)) == 1` on all 4000.
Sizes: **scorer 496/512**, solve 1266/5000, generate 8.5 k/50000, clue and solution **393–465**/1024
(v2: 166–198 — the picture is 2.3× wider in characters and much *less* dense in information).
n is 0 (12.5 %), 1 (16 %), 2 (22 %), 3 (49 %). Offline checksum test (1200 clues): true rule 100 %,
"in-line mutual pairs" 31.9 %, "pairs with room for both" 11.2 %, v1's rule and every
alignment- or mutuality-free reading 0.0 % — unchanged. An independent re-implementation (tokens by
regex, the shelf's kind taken by **majority** rather than from its label, picture rendered from
scratch) agreed with `solve`/`score` on 1200/1200 clues, and the label agreed with the majority on
every row of all of them.

### The kid reading we expect

*"That's a shop. Four shelves — jam, eggs, cod, wax — and someone's put a few things back on the
wrong shelf. Two of them have gone home into the empty spaces on their own shelf. But that shelf's
completely full, so that one had to stay."* Object, problem and verb in one breath, with no letter
grid to tally: the object is named from the labels, the strays are found because they are different
*words*, the empty slots are drawn, and the full shelf is a solid wall. What is still not free —
and is what the demo has to buy — is **which** empty slot (the first one on the shelf, 82 % of the
time to the left of where the good was standing) and **why one of the pair didn't move**.

### Prediction and levers

Unchanged from v2, because the rule is unchanged: **~12 % without a demo, ~95–100 % with one**
(mean ≈ 50 % over two Opus players in a 7-class pool where one spends a demo here). The bet of the
re-skin is only on the judge and on the demo-holder's first look: the counted relation (two goods in
line, each on the other's shelf) and the refusal (a solid shelf) are now the two loudest things in
the picture. If a re-judge still marks the object down, the remaining levers are cosmetic and cheap
— a price on each shelf edge, or the goods drawn as `[jam]` boxes — and the JSON's `LEVERS`
paragraph lists the difficulty knobs, which have not been touched.
