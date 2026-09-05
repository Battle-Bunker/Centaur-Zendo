# kaldrin — a rule-family class in the world of a GOODS TRAIN

Designed 2026-09-05 to the **Revision 3** recipe in `docs/RULE_FAMILIES.md` ("beat the free-label
attack"), built to that recipe from scratch. Sibling write-ups: `NOTES_rules_dominoes.md` (mestrel,
the newest, kid 4.17), `NOTES_rules_beads.md` §§15–23 (tresk v3, kid 4.5) and
`NOTES_rules_pixels.md` §§17–25 (ospren v3, kid 4.5). Shipped file: `challenges/lab/kaldrin.json`.
Not committed.

---

## 1. The world

An instance is **an engine and 4–7 wagons**, drawn left to right exactly as a kid would lay them
out with wooden track:

```
[E]=[coal^]=[logs]=[milk]=[pigs^]=[coal]
```

Six loads — **coal, logs, milk, pigs, sand, wool** — and one visible attribute per wagon: a wagon
is either **heaped up** (drawn with a `^`, the load piled above the sides) or **flat**. The engine
`[E]` carries nothing and only says which end is the front; it is the same in every train.

That second dimension is the whole design. A rule can talk about the loads (a string over six
letters — the tresk/beads world), about the heaps (a string over two), or, best of all, **about one
against the other**: *the heaped wagons all carry the same load · every heaped wagon is coupled to a
wagon carrying the same load · all the pigs wagons are heaped*. A generic (feature == value)
predicate bank holds each dimension separately and cannot express the join — which is exactly what
Revision 3's lever 3 asks for.

**Clue** = 2 example trains (3 on ~1 % of clues), one per line, a blank line, then **five candidate
trains all with the same number of wagons**, exactly one of which obeys the hidden rule.
**Answer** = that candidate written back (whitespace-, bracket- and case-insensitive: the scorer
reads the load words and the `^`s, so `[E]=[coal^]=[logs]`, `coal^ logs` and `COAL^ LOGS` all work)
**or its 1-based index 1–5**. Floor = 20 %.

Internally a wagon is one number, `load * 2 + heaped`.

---

## 2. The universe U — 13 templates, 30 rules

`density` = share of the 18 000-train generator pool that obeys the rule. `minsup` = the smallest
number of satisfiers at any one length (4, 5, 6 or 7 wagons) — the lineup needs them there.
**`bank J`** = the best Jaccard against any of the **650** realised (key, value) predicates of the
attacker's bank (§5), measured **within a length**, because every candidate of a clue shares one.

| t/q | kid sentence (read it aloud) | density | minsup | bank J | best bank predicate |
|---|---|---|---|---|---|
| 0/0 | "the load right behind the engine is carried by **no other wagon**" | .324 | 1182 | .63 | `fl_eq == False` |
| 0/1 | "the load on the **last wagon** is carried by no other wagon" | .329 | 1171 | .61 | `fl_eq == False` |
| 1/0 | "**each load is all in one place** — nothing comes back later down the train" | .299 | 838 | .74 | `hasadjeq == True` |
| 2/0 | "wherever **two wagons of a kind are coupled together** they are at an end" | .366 | 1349 | .75 | `hasadjeq == True` |
| 3/0 | "the load behind the engine and the load at the back are **coupled together somewhere**" | .320 | 1249 | .53 | `adjeq == 2` |
| 4/0 | "the **heaped wagons are all coupled together**" (two or more) | .281 | 960 | .59 | `s1 == 1` |
| 5/0 | "**every heaped wagon is at one of the two ends**" | .111 | 271 | .65 | `nhh == 2` |
| 6/0 | "**no two heaped wagons carry the same load**" (two or more) | .286 | 1113 | .62 | `alldistw == True` |
| 6/1 | "**no two flat wagons carry the same load**" (two or more) | .281 | 1079 | .64 | `alldistw == True` |
| 7/0 | "every wagon carrying **the same load as the one behind the engine** is heaped" | .140 | 474 | **.34** | `nfullfront == 2` |
| 7/1 | "every wagon carrying **the same load as the last one** is heaped" | .142 | 501 | **.34** | `nfullback == 2` |
| 7/2–7/7 | "**all the pigs wagons are heaped up**" (one rule per load, two or more) | .055–.059 | 138 | .63–.67 | `cf<v> == 2` |
| 8/0 | "**every load that travels heaped also travels flat** somewhere on the train" | .257 | 791 | .50 | `nfullkinds == 1` |
| 8/1 | "**every load that travels flat also travels heaped**" | .238 | 755 | .41 | `nsingle == 0` |
| 9/0 | "**every heaped wagon is coupled to a wagon carrying the same load**" | .192 | 727 | **.43** | `nfullkinds == 1` |
| 9/1 | "**every flat wagon is coupled to a wagon carrying the same load**" | .184 | 723 | **.39** | `adjeq == 2` |
| 10/0 | "the wagon behind the engine and the last wagon **carry the same load**" | .308 | 1020 | 1.00 | `fl_eq == True` **CHEAP ×2** |
| 11/0–11/4 | "**exactly k wagons are heaped up**" (k = 0…4) | .054–.253 | 132 | 1.00 | `nfull == k` **CHEAP** |
| 12/0–12/2 | "the train carries **exactly k different loads**" (k = 2, 3, 4) | .234–.326 | 684 | 1.00 | `nd == k` **CHEAP ×2** |

**|U| = 30 rules over 13 templates, ten of them relational** (bank J .34–.75) and three cheap
(J 1.00, on purpose — the learnable slope, §6). **Antichain** verified by brute force over the
18 000-train pool **and** 300 000 uniform-random trains: **0 nesting violations**, minimum support
975 trains in the pool and 8 765 in the random sample. `MASKOF` (the one-pass table builder) was
verified identical to the readable predicate `P`, and the **shipped scorer's** compressed predicate
lifted verbatim out of the JSON was verified identical to both, on **58 000 trains × 30 rules
(0 mismatches)**: the whole 18 000-train pool plus 40 000 uniform-random trains.

Template mix over 500 clues: all 30 rules are drawn; the three cheap templates are **35 %** of clues
(templates 10 and 12 at double weight).

### The relations, in one place

*an end load carried by no other wagon · each load all in one place · the couples only at the ends ·
the two end loads coupled together somewhere · the heaped wagons all coupled together · every heaped
wagon at an end · no two heaped (flat) wagons carrying the same load · everything like the front
(back) load heaped · all the pigs wagons heaped · every heaped load travelling flat as well (and the
other way round) · every heaped (flat) wagon coupled to its own load.*

Every one is **a two-thing comparison a kid makes by eye** — a wagon against its neighbour, a wagon
against the end of the train, a wagon's load against its heap. Nothing here is arithmetic: the class
**never** adds anything up, and the one comparison of two counts a player will reach for ("more
heaped than flat") is deliberately an excluded **trap** (§4). That is the tavrik lesson —
`RULE_FAMILIES.md` §9: counted relations dropped tavrik's kid score from 4.7 to 3.83, while tresk's
and ospren's visual relations held 4.5.

### Counting and arithmetic: the decision, recorded

Excluded from U on purpose: totals of any kind, parities, "more X than Y", "as many X as Y",
positions counted in from an end, distances between wagons. **Borderline, and decided:** *"more
heaped wagons than flat ones"* is **excluded** (it is a trap instead) — it is a comparison of two
counts, and tavrik shows that a kid stops seeing and starts counting. The only counting that
survives is in the two cheap templates, "exactly k wagons are heaped" (k ≤ 4) and "exactly k
different loads" (k ≤ 4) — counted on one hand, at a glance, and kept because they are the class's
learnable slope (§6).

---

## 3. Templates measured and thrown out

All measured on the shipped pool and bank. The rule of thumb from the recipe is J > 0.8 = a gift;
the addendum's "retire by J × rarity" and one new lesson (the **trap-conjunction leak**, below) did
the rest.

| template | density | bank J | why not |
|---|---|---|---|
| **no two of a kind are coupled together** | .299 | **1.00** | `adjeq == 0` — kept as a trap |
| exactly one place where two of a kind are coupled | — | **1.00** | `adjeq == 1` |
| the train reads the same backwards | .087 | **1.00** | `palin` — kept as a trap |
| **the load behind the engine is coal** (a fixed load) | .167 | **1.00** | `first<v>`; the anchored version (template 0, "*that* load is nowhere else") is J .63 — kept as a trap, and it is the first thing anyone tries |
| the two wagons behind the engine carry the same load | .300 | **1.00** | `eq01` |
| the last two wagons carry the same load | .288 | **1.00** | `eqll` |
| the heaped wagons all come first (or all last) | .223/.215 | **1.00** | `snoninc` / `snondec` |
| the wagons take turns, heaped and flat | .044 | **1.00** | `spat` is in the bank as a whole tuple |
| the first and last wagons are exactly the same wagon | .178 | **1.00** | `w_fl_eq` |
| every load is on at least two wagons | .188 | **1.00** | `nsingle == 0` |
| wagons carrying the same load always match (both heaped or both flat) | .320 | **1.00** | `nmixed == 0` — a lovely sentence, a single bank predicate; the best trap in the class |
| the wagons like the one behind the engine are all coupled together | .189 | .84 | collapses to `eq01` (if the front load is blocked, wagons 1 and 2 match) |
| every flat wagon has a heaped one coupled to it | .425 | .71 | too dense, and `nhh == 0` |
| every heaped wagon has a flat one coupled to it | .460 | .88 | `sfmaxrun == 1` |
| the load behind the engine is carried by another wagon too | .676 | .76 | density > .5 — four decoys all *lacking* it is itself a signature |
| exactly k wagons carry the load behind the engine | .182–.348 | .61–.73 | counting, and inside template 0 |
| **all the coal wagons are coupled together** (one rule per load) | .100 | .56 | **the trap-conjunction leak** — see below; measured **65 %** for the label-spending attacker while it was in U |
| **the heaped wagons all carry the same load** | .118 | .52 | same leak — measured **68 %** |
| the flat wagons are all coupled together | .309 | — | **breaks the antichain**: "every heaped wagon is at an end" implies it at n ≥ 4 (the middle is then one block of flat wagons) |
| every flat wagon is at one of the two ends | .084 | — | same, the other way round (it implies "the heaped wagons are all coupled together") |
| the middle wagon is the odd one out | — | — | length-conditioned; Revision 3 says those leak through a lineup, because all five candidates share a length |

### The new lesson: the trap-conjunction leak

mestrel's §3 records that *a rule which is the conjunction of two traps is unusable, because the
matched trap profile then forces every decoy to obey the rule*. This world produced the **mirror
image** of that failure, and it is worth writing down:

> **If a rule is (a trap) ∧ (one bank predicate), the matched trap profile hands the attacker the
> bank predicate as a clean unique explanation of the true candidate.**

"All the coal wagons are coupled together (two or more)" = *at least two coal wagons* (a fitted
trap, so **every decoy has two coal wagons too**) ∧ `blk_coal == 1`. Since no decoy obeys the rule
and all of them carry two-or-more coal, `blk_coal == 1` selects the true candidate alone on every
such clue — the learner needs one label to find that out. Measured: 65 % for that family, 68 % for
"the heaped wagons all carry the same load" (= *at least two heaped* ∧ `nfullkinds == 1`).
Freeing the implied traps from the matched profile only moved the leak (the freed trap then became
the unique explanation: 59 % and 52 % on other templates). Both families were retired to the trap
list, and every surviving template was checked to have **no single bank predicate as its residue**
after its implied traps: *the heaped ones all coupled* leaves `sfmaxrun == nfull` (a join of two
keys), *no two heaped alike* leaves `nfullkinds == nfull`, *all the pigs heaped* leaves
`cf_pigs == cnt_pigs`, and so on — none of them is a (key, value) pair.

---

## 4. The exclusions (never in U; the decoys satisfy them)

**24 trap families**, fitted to each clue from the examples. They are what a first-time player
tries: the train read backwards (loads only, and loads-with-heaps) · no two of a kind coupled · at
least *k* couples · at least *k* `<load>` wagons · exactly these loads · at least *k* different
loads · no load on more than *k* wagons · at least *k* heaped wagons · the heaped ones all first /
all last · the wagons taking turns heaped and flat · no two heaped wagons coupled · the wagon behind
the engine (or the last one) heaped · the first and last wagons identical · every load on two or
more wagons · all the wagons carrying different loads · **wagons with the same load always match,
both heaped or both flat** · **more heaped wagons than flat ones** (the one arithmetic comparison,
excluded on purpose) · the load behind the engine is `<v>` · the load at the back is `<v>` · the two
wagons behind the engine carrying the same load · the last two carrying the same load.

Two of them, "the heaped ones all come first" and "…all come last", are fitted **only when they say
something**: on an all-flat or all-heaped example both are vacuously true, and fitting both at once
forces every decoy to be all-heaped — which made "none of the wagons are heaped" undrawable
(0 clues in 2 000). With the guard, all 30 rules of U are drawn.

Measured over 500 clues: **6.3 fitted traps per clue, 3 133 in all, and every one of them is
satisfied by ALL FIVE candidates or by NONE (3 133 / 3 133 = 100 %)** — §5b of Revision 2 in its
strong form. No trap, no count of traps and no combination of traps separates the lineup, and a
player whose universe is U *plus* all 24 trap families is worth exactly a player who knows U.

| excluded rule, fitted to the clue | fits | picking by it scores |
|---|---|---|
| at least *k* different loads | 94 % | 21 % |
| at least *k* `<load>` wagons | 91 % | 18 % |
| at least *k* wagons are heaped | 89 % | 19 % |
| no load is on more than *k* wagons | 62 % | 18 % |
| at least *k* wagons of a kind are coupled together | 50 % | 17 % |
| the last wagon is heaped | 26 % | 17 % |
| no two heaped wagons are coupled together | 24 % | 16 % |
| the wagon behind the engine is heaped | 24 % | 17 % |
| **the load behind the engine is `<v>`** ("the cows are right behind the engine") | 18 % | 29 % |
| the load at the back is `<v>` | 17 % | 0 % |
| **there are more heaped wagons than flat ones** (the excluded comparison) | 16 % | 23 % |
| wagons with the same load always match, both heaped or both flat | 13 % | 15 % |
| no two of a kind are coupled together | 7 % | 29 % |
| the two wagons behind the engine carry the same load | 6 % | 33 % |
| the first and last wagons are exactly the same | 5 % | never selects |
| the last two wagons carry the same load | 5 % | 14 % |
| every load is on two or more wagons | 4 % | 50 % (20 clues) |
| the heaped wagons all come after / before the flat ones | 1 % / 0 % | never selects |
| exactly these loads are carried · the train reads the same backwards · the wagons take turns | 1 % / 1 % / 0 % | never selects |

The "picking by it scores" column is **pure tie-breaking** — all five candidates satisfy the trap,
so the pick is random — against a 20 % floor; the two 29–50 % rows are the small-sample families
(20–35 clues each).

---

## 5. The attacker's bank, rebuilt inside `generate` (recipe step 1)

Union of the generic banks the revision-2 players actually brought — `ospren1a`'s `f_borsel_a` /
`f_borsel_b` (a list of numbers: sums and sums mod *m*, max/min/range, sorted/strict/palindrome,
adjacent equalities, runs, peaks and valleys, per-value counts, positions, mode counts) and
`tresk1b`'s `build_seq()` / `build_dornic()` — **transposed to a train and extended with everything
a second round would add for THIS world**:

* the loads as numbers (`sum`, `sum%k`, `max`, `min`, `nondec`, `posmax`… — nonsense features that a
  real attacker computes anyway, and dense ones that blunt his rarity order);
* the load string (`first`, `last`, `fl_eq`, `p1`, `q1`, `eq01`, `eqll`, `nd`, `alldist`, `setvals`,
  `multiset`, `modecnt`, `nsingle`, `adjeq`, `nruns`, `maxrun`, `palin`, and per load `cnt`, `has`,
  `ge2`, `first`, `last`, **`blk`** (how many separate blocks), `pos`);
* the heap string (`nfull`, `nhalf`, `allfull`, `allhalf`, **`spat`** (the whole pattern), `s0`,
  `sl`, `s1`, `s_fl_eq`, `snondec`, `snoninc`, `salt`, `spalin`, `sadjeq`, `nff`, `nhh`, `sruns`,
  `smaxrun`, `sfmaxrun`, `posf`, `fullpos`, `nfullfront`, `nfullback`, `morefullfront`);
* **the join** — the two dimensions together, which is where the class lives and where a generic
  bank would normally stop: the wagons as twelve symbols (`w0`, `wl`, `w_fl_eq`, `ndw`, `alldistw`,
  `wadjeq`, `wmodecnt`, `wsorted`, `wpalin`), **`cf<v>`** (how many `<v>` wagons are heaped),
  **`nfullkinds`**, **`nmixed`**, `nrep`.

**126 feature keys, 650 realised (key, value) predicates with base rate ≥ 1 %**, carried inside
`generate` as a bit mask for the aiming. The bank is deliberately *stronger* than the banks the
players brought — it already knows that a wagon has a load and a heap, and it counts blocks per
load — which is why the retirement list in §3 is long and why the ten surviving templates are worth
having.

---

## 6. How the lineup is built

1. **The instance distribution is a mixture of real-looking trains, not twelve-sided dice**: scatter
   (16 %), blocks of a few loads (12 %), one load dominating (12 %), one load confined to one place
   (10 %), a structured heap pattern — heaped ones sorted to one end, alternating, one block, at the
   two ends, exactly one or two, all or none (12 %), the load deciding the heap (10 %), the ends
   rhyming (8 %), only two or three loads (8 %), mirrors and repeats (6 %), uniform over the twelve
   wagons (6 %). Every example and every candidate is drawn from exactly this mixture, so nothing
   about a train's provenance separates the truth from a decoy.
2. **Minimal example set, a pair first** (lever 2): the two examples leave exactly one rule of U
   alive and neither alone does. 495 of 500 clues are two-example clues.
3. **Five candidates** (lever 1), one length, five distinct trains, none equal to an example.
4. **Matched trap profiles** (§5b, strong form) *and* the same number of different wagons, so "the
   odd one out for variety" is worth nothing.
5. **The truth's rank is aimed at four orders** (lever 5): the **rarity** order (the rarest bank
   predicate that selects exactly one candidate — what both revision-2 players actually ran), the
   **count** order, the **look-alike** order (wagons shared with the other four) and the
   **family-resemblance** order (wagons shared with the nearest example). 50 candidate line-ups are
   scored per clue against a 500-train decoy sample; the aiming effort is itself a dial worth ~10
   points of relational accuracy (36 tries / 340 samples left the relational templates at 33.9 %,
   50 / 500 brings them to 23.9 % for 0.4 ms of `generate`).
6. **Three cheap templates at 35 % of clues** are the learnable slope. Measured dial, same engine,
   400 clues, attack at 0 / 30 / 60 / 120 / 240 labels:

   | cheap draw weight | share of clues | attack |
   |---|---|---|
   | single | 23 % | 27.0 / 33.0 / 31.2 / 35.8 / 37.2 |
   | template 10 doubled | 28 % | 29.4 / 33.8 / 39.2 / 41.2 / 45.6 |
   | **templates 10 and 12 doubled (shipped)** | **35 %** | **29.2 / 37.2 / 40.2 / 45.0 / 48.5** |
   | all three doubled | 38 % | 34.2 / 36.2 / 43.5 / 48.8 / 51.8 |

   (One engine, 400 clues, measured before the last change to the trap list — see §4's note on
   vacuous traps; the shipped build re-measured on 500 fresh clues gives 31.4 / 35.4 / 45.2 / 48.0 /
   51.0.) The shipped row sits in the middle of the recipe's 35–55 % band at 30–60 labels.

---

## 7. The attacker table (recipe step 8)

Full engine: skip-harvest 300 clues for base rates → answer a **random candidate** on a disjoint set
of clues, keeping the ~1/5 that come back correct as gold labels **and the wrong picks as
negatives** → per-predicate unique-explanation weights → rarity-weighted pick. 500 fresh test clues
(seeds 1e6 …), live 650-predicate bank, base rate floored at 5 % exactly as the players floor theirs.

| gold labels (clues answered) | **kaldrin with the generic bank** | the same engine with a bank that also holds all of U | U-coverage |
|---|---|---|---|
| 0 (0) | **31.4 %** | 57.8 % | 0 % |
| 30 (145) | **35.4 %** | 70.0 % | 76 % |
| 60 (241) | **45.2 %** | 80.6 % | 86 % |
| 120 (668) | **48.0 %** | 89.0 % | 94 % |
| 240 (1 219) | **51.0 %** | 95.0 % | 98 % |
| 360 (1 810) | — | 96.6 % | 100 % |

**The shape is the point.** The free labels are worth ~14 points and then stop: 45 % at 60 labels,
51 % at 240, and every one of those points is the three cheap templates. Per-template accuracy of
the 60-label attacker (400 clues): the cheap ones **69.6 / 79.0 / 86.2 %** (the ends matching, the number of
different loads, the number of heaped wagons; 77.4 % together, 34 % of the 400 clues); the ten relational templates together **25.1 %**, five points over the 20 % floor —
14.8 % (an end load nowhere else), 15.2 % (heaped only at the ends), 15.8 % (couples at the ends),
14.3 % (the two end loads together), 18.5 % (heaped loads travel flat too), 21.2 % (each heaped
wagon coupled to its own load), 34.8 % (the heaped ones all together), 35.7 % (each load in one
place), 37.0 % (no two heaped alike), 44.0 % (everything like the front load heaped).

**The honest ceiling.** The **in-U intersection is 100.0 %** — a player who has reconstructed U
answers every clue correctly. An attacker whose bank also contains all of U reaches 80 % at 60
labels, 95 % at 240, and learns U to **90 % coverage in about 100 labels** (coverage = the share of
fresh clues whose true rule the learner has confidently identified: ≥ 4 firings and n/m ≥ 0.7).
With the generic bank alone, coverage never passes the cheap templates (33–38 %). **The gap
45 % → 100 % is the class**, and it is paid for by inventing the vocabulary: looking at
`[E]=[wool]=[wool^]=[logs]=[logs^]=[wool]` and thinking *"what is next to the heaped one?"* rather
than *"how many are heaped?"*.

---

## 8. Lever ablation (identical conditions, 400 test clues)

| build | k | floor | attack at 0 / 30 / 60 labels |
|---|---|---|---|
| **as shipped** | 5 | 20 % | 30.5 / 38.0 / **42.2 %** |
| **minus lever 3** — the same engine, bank and traps, but a universe of 30 rules every one of which IS a single bank predicate (exactly *k* heaped, exactly *k* loads, the ends match, a palindrome, no two of a kind coupled, exactly one couple, the front load is *v*, the back load is *v*, the heaped ones sorted to one end, taking turns, same load same look, all loads different, the first and last wagon identical) | 5 | 20 % | 60.0 / 71.5 / **79.2 %** |
| minus lever 5 — decoys not aimed at all | 5 | 20 % | 41.2 / 45.5 / **49.0 %** |
| minus lever 1 — k = 4 | 4 | 25 % | 35.2 / 38.0 / **44.0 %** |
| lever 1 pushed — k = 6 | 6 | 16.7 % | 29.0 / 33.5 / **39.5 %** |
| minus lever 2 — three-example clues | 5 | 20 % | 41.2 / 41.2 / **45.2 %** |

Read off the differences at 60 labels: **the relational universe (lever 3) is worth ≈ 37 points** —
the whole game, as on tavrik (41), tresk (49), ospren (38) and mestrel (52). The rarity aiming
(lever 5) is worth ≈ 7, the two-example clue (lever 2) ≈ 3, the fifth candidate (lever 1) ≈ 2, and
**k = 6 buys nothing** (−2.7, and it costs a clue line and a kid's patience). Five is the number,
for the fourth class in a row.

A lever the earlier write-ups did not measure: **how hard `generate` tries to aim**. Raising the
search from 36 line-ups against a 340-train decoy sample to 50 against 500 took the ten relational
templates from 33.9 % to 23.9 % against the 60-label attacker, for 0.4 ms of `generate` — the aiming
is not a formality, it is the second-biggest dial in the build.

---

## 9. Three demos

```
seed 1000006      hidden rule: EVERY HEAPED WAGON IS AT ONE OF THE TWO ENDS OF THE TRAIN

  examples     [E]=[logs^]=[sand]=[sand]=[wool]=[wool]=[logs^]
               [E]=[logs]=[pigs]=[milk]=[coal^]

  candidates 1 [E]=[pigs]=[milk]=[sand]=[milk]=[logs^]=[pigs]
             2 [E]=[milk^]=[logs]=[pigs]=[pigs]=[logs]=[sand]     <-- the answer
             3 [E]=[coal]=[sand]=[logs^]=[sand]=[coal]=[pigs]
             4 [E]=[wool]=[coal]=[coal]=[milk^]=[logs]=[logs]
             5 [E]=[wool]=[coal]=[sand^]=[wool]=[logs^]=[coal]
```
The class in one picture. Every candidate has one or two heaped wagons, all five fire exactly the
same excluded rules, and the loads are a different mixture on each — "how many are heaped?" and
"which load is it?" are both worth nothing, and the only thing left to look at is **where** the
heaps are. Only candidate 2 has its heap at an end (right behind the engine). (The first example shows the honest form:
a heap at each end.)

```
seed 1000013      hidden rule: EVERY HEAPED WAGON IS COUPLED TO A WAGON CARRYING THE SAME LOAD

  examples     [E]=[wool]=[wool^]=[logs]=[logs^]=[wool]
               [E]=[logs]=[coal]=[pigs^]=[pigs^]=[pigs^]

  candidates 1 [E]=[wool^]=[pigs^]=[pigs^]=[coal^]=[coal^]
             2 [E]=[wool]=[wool]=[milk^]=[milk]=[milk^]           <-- the answer
             3 [E]=[pigs^]=[milk^]=[milk^]=[pigs]=[pigs]
             4 [E]=[sand^]=[wool^]=[coal]=[coal]=[coal]
             5 [E]=[milk^]=[milk]=[coal^]=[coal^]=[milk^]
```
The join between the two dimensions, and the reason for the world. A kid puts a finger on each
heaped wagon and asks "is the one next door carrying the same thing?"; candidates 1, 3, 4 and 5 all
have a heaped wagon standing on its own (the `wool^` at the front of 1, the `pigs^` at the front of
3, both heaps of 4, the `milk^` at the back of 5). A predicate bank has "how many are heaped", "how
many blocks of wool", "is wagon 1 heaped" — and nothing for *this wagon's load against its
neighbour's, but only for the heaped ones*.

```
seed 1000000      hidden rule: THE TRAIN CARRIES EXACTLY 2 DIFFERENT LOADS  (a CHEAP one)

  examples     [E]=[logs]=[pigs^]=[logs]=[pigs^]=[logs^]
               [E]=[wool]=[wool]=[wool]=[wool]=[milk]=[milk^]=[milk]

  candidates 1 [E]=[sand^]=[logs]=[sand^]=[coal]=[coal]=[logs]
             2 [E]=[wool]=[coal]=[milk^]=[milk^]=[coal]=[wool]
             3 [E]=[wool]=[wool]=[wool]=[pigs]=[pigs^]=[pigs^]    <-- the answer
             4 [E]=[pigs]=[sand^]=[pigs]=[logs]=[logs]=[sand^]
             5 [E]=[milk^]=[wool]=[coal]=[wool]=[coal]=[milk^]
```
The learnable slope: a kid counts the different loads on one hand, and so does a predicate bank
(`nd`). 35 % of clues are of this kind; they are what makes the free labels worth fourteen points
and what stops the class reading as arbitrary.

---

## 10. Witness table — 500 fresh clues (seeds 1e6 … 1e6+499)

Five candidates, so the floor is 20 %.

| witness | score |
|---|---|
| **the in-U intersection — a player who knows U** | **100.0 %** |
| the true rule (`solve`), verbatim and by index | **100.0 % / 100.0 %** |
| a player who knows U minus **two whole templates** (all 78 pairs) | 77.4 – 93.0 % (median 88.6) |
| **the full revision-3 attack, 60 labels** | **45.2 %** |
| … at 0 / 30 / 120 / 240 labels | 31.4 / 35.4 / 48.0 / 51.0 % |
| **the candidate carrying the fewest different loads** | **36.2 %** |
| **the candidate with the fewest heaped wagons** | **29.4 %** |
| **the candidate with the most same-load couplings** | **29.4 %** |
| **the candidate whose two end loads are the same** | **28.0 %** |
| the candidate with the longest block of one load | 26.6 % |
| the candidate satisfying the MOST example-consistent bank predicates | 25.4 % |
| the candidate least like an example, wagon by wagon | 23.4 % |
| **pick a random candidate (the floor)** | **20.6 %** |
| the candidate whose first wagon is heaped | 20.6 % |
| the candidate least like the other four (the odd one out) | 20.2 % |
| pick candidate 1 | 18.6 % |
| the candidate with the most heaped wagons | 17.8 % |
| the candidate with the fewest same-load couplings | 16.6 % |
| the candidate with the most different loads | 16.6 % |
| the candidate satisfying the FEWEST such predicates | 16.4 % |
| the candidate most like an example, wagon by wagon | 15.8 % |
| the candidate most like the other four (the medoid) | 15.8 % |
| **each of the 24 excluded rules, fitted to the clue** | **0 – 29 %** (pure tie-breaking, §4) |

A scan of **every** bank feature used as a fixed one-feature heuristic ("always answer the candidate
with the largest / smallest *x*") found nothing above **32.6 %** (`min nd`, i.e. the fewest different
loads — the cheap template doing its intended job), then `max nmixed` 29.6 %, `min nsingle` 29.4 %,
`max smaxrun` / `max sadjeq` 28.0 %. Those 28–36 % rows are the **foothold**: a demo-less player who
plays any of them beats the floor by eight to sixteen points, as tresk's "biggest clump" (33 %) and
mestrel's "fewest doubles" (32 %) do.

Other measured numbers (500 clues): uniqueness 500/500 · minimality 500/500 · exactly one candidate
obeys the rule 500/500 · all five candidates the same length 500/500 · five distinct candidates
500/500 · no candidate equal to an example 500/500 · **matched trap profiles 3 133/3 133** ·
examples per clue 2 → 495, 3 → 5 · candidate length 4/5/6/7 wagons → 120/123/134/123 ·
true-candidate position 93/96/105/108/98 · all 30 rules and all 13 templates drawn · over **3 000
seeds, 3 000 distinct clues and 0 fallback clues**.

---

## 11. Validation

`python tools/quickcheck.py challenges/lab/kaldrin.json --seeds 300 --cap max_score_code_chars=1024`
→ `OK kaldrin  gen=11.33ms score=8.43ms solve=8.46ms` (first-call figures; the steady-state numbers
are below), **no warnings**. It also passes with no `--cap` at all, since `max_score_code_chars`
became 1024 on 2026-09-05.

| quantity | value | cap |
|---|---|---|
| `score` source | **1 024 chars** | 1024 (the rule-family raise, `RULE_FAMILIES.md` §4) |
| `generate` source | 27 370 | 50 000 |
| `solve` source | 2 777 | 5 000 |
| `generate` | **2.75 ms mean**, 2.67 median, 4.78 p99, 8.73 max over 5 000 seeds | 100 ms |
| `score` | 0.73 ms; 0.031 ms on a 4 000-character answer | 50 ms |
| `solve` | 0.32 ms | 2 000 ms |
| clue | **230–433 chars** | 1024 |
| answer | ≤ 59 chars, or 1 | 1024 |

Module-level tables cost **3.1 s once per worker** (the 18 000-train pool, its 30-bit U mask, its
trap readouts and its 650-bit bank mask) — not charged to `max_generate_ms`, and well inside the
sandbox's budget for compiling a seven-class pool.

`score` was checked candidate-by-candidate against `solve` on 600 clues × 5 candidates × **10 answer
forms** (verbatim · index · index with spaces and a newline · a trailing newline · spaces inside the
couplings · ALL CAPS · the engine dropped · brackets stripped · words only · angle brackets) —
**12 000 checks, 0 disagreements**; every non-chosen candidate scores 0 both verbatim and by index.
The one form that does *not* score is prose wrapped round the answer (`"answer: [E]=[wool]…"`), and
for a legible reason: `swer` parses as a sand wagon, so the train no longer matches a candidate.
`score` returns 0 without raising for `""`, `"0"`, `"6"`, `"9"`, `"55"`, `"1 2"`, `"x"`, `"1"×100`,
`"["×4000`, `"None"`, `"-1"`, `"1.0"`, `"[]"`, `"true"`, `"0.5"`, `"^^^^"`, `"cccc"`, `"[E]"`,
`"coal"×500`, a train of four identical wagons, the clue itself, the example block alone, the
candidate block alone, and the unicode digits `"٢"` / `"²"`.
`generate` is deterministic (md5 of the first 200 clues stable across processes) and produces
**3 000 distinct clues over 3 000 seeds** with no fallback. `MASKOF`, the readable `P` and the
scorer's compressed predicate agree on 58 000 trains × 30 rules.
The 30 rules are rebuilt in the scorer from a **13-character table** (`"2111112822153"` — how many
parameters each template takes) plus one thirteen-branch predicate list, which is what bought room
for ten relational templates inside 1 024 characters.

---

## 12. Predicted classification

**Calibrated**, with the risk on the easy side and named.

* **Without a demo** the clue reads as multiple choice from round 1 (two trains, a gap, five trains
  of the same length), so every probe is well formed and the floor is a free 20 %. The engine that
  took 79–96 % off the revision-2 lineup classes pays **31 % at zero labels, 45 % once the free
  labels arrive, and then crawls** (51 % at 240 labels, all of it the cheap templates). The best
  cheap heuristics — "answer the one carrying the fewest different loads" (36 %), "the one with the
  fewest heaped wagons" (29 %), "the one whose two ends match" (28 %) — are the foothold.
  Expect **30–50 %**.
* **With a demo** the demo teaches the format in one look and one worked rule. The way up is to
  notice that this class talks about **where the heaps are, what is coupled to what, and which load
  is heaped** — and to write those predicates down; a player who does scores 100 %, one who maps 11
  of the 13 templates scores 77–93 % (median 89).

Mean across two Opus teams ≈ **0.40–0.55** → `calibrated`. If it comes back **too easy**, the levers
in order are: drop template 12 to single draw weight (measured: 28 % of clues, attack
29 / 34 / 39 %), then single-weight template 10 as well (23 %, attack 27 / 33 / 31 %), then k = 6
(−2.7). If **too hard**: put all three cheap templates on double weight (38 % of clues, attack
34 / 36 / 43.5 %), or k = 4 (+2).

**12-year-old test (target 4.3+).** The object is a **goods train**, drawn the way a six-year-old
lays one out on the carpet: an engine and four to seven wagons, each carrying something a child can
name — coal, logs, milk, pigs, sand, wool — and each either heaped up or flat. Nobody has to be told
what any of it is. The task is the puzzle-book one — *which of these five fits?* — and every rule is
a thing you **see**:

*every heaped wagon is at one of the two ends · the heaped wagons are all coupled together · every
heaped wagon is coupled to a wagon carrying the same load · no two heaped wagons carry the same load
· all the pigs wagons are heaped up · every load that travels heaped also travels flat · the load
right behind the engine is carried by no other wagon · each load is all in one place · wherever two
of a kind are coupled together they are at an end · the two end loads are coupled together
somewhere.*

Read them aloud: each is one breath, and each can be checked on a five-wagon train with a finger in
about three seconds. **Nothing in the class counts anything past four or adds anything up** — the
only sums a kid meets are "exactly two are heaped" and "exactly three different loads", counted on
one hand — and the one comparison of two counts that a grown-up immediately reaches for ("more
heaped than flat") is deliberately one of the wrong answers. That is the tavrik lesson applied on
purpose: tavrik's counted relations scored 3.83, tresk's and ospren's visual ones 4.5, and every
rule here is visual.
