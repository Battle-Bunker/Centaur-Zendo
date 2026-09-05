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
verified identical to the readable predicate `P` on the whole pool and on 40 000 random trains, and
the compressed scorer predicate was verified identical to both on 46 000 trains × 30 rules.

Template mix over 500 clues: all 30 rules are drawn; the three cheap templates are **34 %** of clues
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
| the flat wagons are all coupled together | .27 | — | **breaks the antichain**: "every heaped wagon is at an end" implies it at n ≥ 4 |
| every flat wagon is at one of the two ends | .27 | — | same, the other way round |
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

**22 trap families**, fitted to each clue from the examples. They are what a first-time player
tries: the train read backwards (loads only, and loads-with-heaps) · no two of a kind coupled · at
least *k* couples · at least *k* `<load>` wagons · exactly these loads · at least *k* different
loads · no load on more than *k* wagons · at least *k* heaped wagons · the heaped ones all first /
all last · the wagons taking turns heaped and flat · no two heaped wagons coupled · the wagon behind
the engine (or the last one) heaped · the first and last wagons identical · every load on two or
more wagons · all the wagons carrying different loads · **wagons with the same load always match,
both heaped or both flat** · **more heaped wagons than flat ones** (the one arithmetic comparison,
excluded on purpose) · the load behind the engine is `<v>` · the load at the back is `<v>` · the two
wagons behind the engine carrying the same load · the last two carrying the same load.

Measured over 500 clues: **6.3 fitted traps per clue, 3 147 in all, and every one of them is
satisfied by ALL FIVE candidates or by NONE (3 147 / 3 147 = 100 %)** — §5b of Revision 2 in its
strong form. No trap, no count of traps and no combination of traps separates the lineup, and a
player whose universe is U *plus* all 22 trap families is worth exactly a player who knows U.

TRAPS_TABLE

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
6. **Three cheap templates at 34 % of clues** are the learnable slope. Measured dial, same engine,
   400 clues, attack at 0 / 30 / 60 / 120 / 240 labels:

   | cheap draw weight | share of clues | attack |
   |---|---|---|
   | single | 23 % | 27.0 / 33.0 / 31.2 / 35.8 / 37.2 |
   | template 10 doubled | 28 % | 29.4 / 33.8 / 39.2 / 41.2 / 45.6 |
   | **templates 10 and 12 doubled (shipped)** | **34 %** | **29.2 / 37.2 / 40.2 / 45.0 / 48.5** |
   | all three doubled | 38 % | 34.2 / 36.2 / 43.5 / 48.8 / 51.8 |

   The shipped row sits in the middle of the recipe's 35–55 % band at 30–60 labels.

---

ATTACK_SECTION

---

ABLATION_SECTION

---

DEMOS_SECTION

---

WITNESS_SECTION

---

VALIDATION_SECTION

---

CLASSIFICATION_SECTION
