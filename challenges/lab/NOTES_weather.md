# Direction: weather and seasons

Brief: a small ASCII picture a kid recognises instantly; the clue pins an arbitrary-but-natural
*measurement* of it that has no name and is not the object's famous operation; close every
degenerate witness; leave a foothold; target ~50 % for Opus centaur players over 6x0.5 s rounds.

Read first: LADDER.md, REPORT.md, DESIGN_LOOP.md (12-year-old test twice, levers 7-9), SPEC 2-4,
LegoZendo/Wordz, CHALLENGE_AUTHORING (incl. 3b), STARS.md, NOTES_game "conclusion", and the last
run sections of NOTES_fennick / nature / kitchen / time / music / clothes.

What those runs say, in one line each, and how it shaped this design:
* players rebuild the picture grammar perfectly and then **hunt statistics** -> the difficulty must
  be *which* statistic, and it must be visible;
* **the counted relation must be the loudest thing in the drawing** (basten 7->33 %, garrow 15->64 %
  came from redrawing, not from rule changes);
* a **cheap template or a distribution-matching sampler that satisfies the rule** is the leak that
  reaches 88-100 % (velk v1, tovel v2) - test those, not only wrong rules;
* the **natural first probe must score sometimes**, or players decide the grader is exact-match and
  farm demos (tovel v3);
* a rule outside the players' generative prior is unreachable however clean the evidence
  (NOTES_game conclusion) - so the rule has to be a sentence a kid would say while pointing;
* positive-only clauses (nature/basten) buy nothing: demos only ever show satisfying pictures, so a
  "must also contain X" clause is invisible and only taxes the player who has the rule.

## Brainstorm (12 ideas, each against the 12-year-old test)

Test A = a kid names the object from one demo. Test B = the pinned pattern has no name and is not
the object's famous operation. Test C = the relation can be *drawn* so it is the headline.

1. **Puddle map / where the water collects on a bumpy road.** A = 5/5. B = **fails**: this is
   "trapping rain water", a programming-contest classic with a Wikipedia-shaped answer; exactly the
   RLVR anti-pattern DESIGN_LOOP forbids. Rejected on sight.
2. **A week's forecast strip, count the days the weather changed.** A = 5/5, B = fails ("number of
   transitions" is nameable and is the first thing anyone counts). Rejected.
3. **Forecast said vs what happened (two symbol rows), count the days it said sun and it rained.**
   A = 5/5, B = 3/5 (a cell of a 4x4 confusion matrix). C = 4/5. Rejected because the hypothesis
   space is *enumerable*: 16 ordered symbol pairs, and players can test a construction per pair -
   one round and it is over.
4. **High/low temperature bars with a freezing line; count the days whose LOW is exactly on the
   line ("it just froze").** A = 5/5, B = 4/5, C = 4/5. Rejected as too thin: 7 items, one bit each,
   and "exactly on the line" is the second thing a statistic-hunter tries. Also a bar chart, which
   fennick already owns.
5. **Sun, clouds and the shadows they cast on a hillside** (shadow shifted by the cloud's height).
   A = 5/5, B = 5/5 (a projection with an offset - genuinely un-named). Rejected on the constructive
   trap: the player draws the clouds, so they can put every cloud at height 0 and the offset
   disappears; pinning the sun in the clue makes a fixed-offset guess win 1/6 of clues; and two
   insights (the shift *and* what is counted) is orlan's failure mode.
6. **Slanting rain and shelter: count the plants standing in the lee of a taller one.** A = 5/5,
   B = 4/5. Rejected because of the **binary-parameter trap**: if the wind direction is in the clue,
   a player who always builds "taller thing on the left" wins ~50 % of clues without any insight.
   Recorded as a general rule: never make the rule depend on a coin-flip parameter of the clue.
7. **Icicles under a gutter over a snowdrift; count the icicles whose tip stops exactly one row
   short of the snow.** A = 4/5, B = 3/5 - per column this is "a + b = H - 1", an arithmetic
   coincidence, and players compute per-column gaps as their first statistic. Rejected.
8. **A month of weather symbols in a calendar grid; count the days whose weather repeats the same
   weekday last week.** A = 5/5, B = 4/5, but it is a calendar with a weekly-offset rule, which is
   tovel's territory (its strongest rival template is literally "the same thing every week").
   Rejected for collection diversity.
9. **Clouds above, puddles below; count the puddles exactly as wide as the cloud over them.**
   A = 5/5, B = 4/5, C = 5/5 - but this is norvel's relation (a run with the same span as a run in
   the other row) with a weather skin, and virel's twin-span relation as well. Rejected for
   diversity: the collection already has two exact-span classes.
10. **Frost on window panes; count the panes with frost in exactly two corners.** A = 4/5, B = 4/5,
    C = 3/5 (a grid of little boxes reads as a window only just). Held in reserve.
11. **Weather-vane field: a grid of wind arrows and a few clouds; count the arrows pointing at a
    cloud.** A = 4/5, B = 3/5 ("arrow points at X" is the direction field's famous operation).
    Rejected.
12. **Rain showers falling on a garden row; count the plants standing right at the edge of a
    shower, dry, just missing the rain.** A = **5/5** (rain, flowers, a little tree - a kid names it
    from one demo). B = **5/5**: the garden's famous operation is "which plants get watered"; this
    counts the ones that *just missed*, which has no name and is the nose-vs-tail asymmetry that
    beat one player on basten and one on virel. C = **5/5**: a shower's edge is a vertical line in
    the drawing and the counted plant sits in the column beside it, one row below the last drop -
    the contrast "wet at the boundary vs dry at the boundary" can be drawn side by side in every
    demo. **Chosen.**

Choice: **idea 12**, shipped as `challenges/lab/kelmar.json` (neutral name, unique across
`challenges/` and `challenges/lab/`).

## kelmar - the class

**Clue** `<ground>/*<a>Y<b>`, e.g. `__*__*____*__Y__*____*___Y___Y____*________*__Y____/*3Y1`.
`<ground>` is one row of bare earth `_`, 42-52 columns, with 5-8 flowers `*` and 4-7 small trees `Y`
planted at least 3 columns apart and never in the outer two columns. `a`, `b` in 1..3, `a+b <= 5`,
`a <= flowers-3`, `b <= trees-3` (so a digit is never the number of plants of that kind and there
are always spare plants of both kinds). The glyph is written next to its digit, so which digit
belongs to which plant is never a gratuitous ambiguity.

**Answer** a picture of rain falling on that garden:

```
      #####  #######  ####             ####    ####
      '''''  '''''''  ''''             ''''    ''''
      '''''  '''''''  ''''             ''''    ''''
      '''''  '''''''  ''''             ''''    ''''
__*__*____*__Y__*____*___Y___Y____*________*__Y____
  .  ^    w  w  w    ^   w   .    .        ^  ^        <- ^ = counted, w = wet (not shown to players)
```

The scorer drops blank lines, right-strips, and requires the **last** line to be the clue's ground
row verbatim. Every line above it is a sky row: `#`, `|`, `/`, `'` read as rain, space, `.`, `_` as
dry sky, anything else is rejected. There must be **at least two sky rows, all identical** (the rain
falls straight down), each as long as the ground row; every maximal run of rain (a *shower*) at
least **3 columns wide**; consecutive showers separated by at least **2 dry columns**; at least
**2 showers**. Sky height (2-4), which rain glyph, dots or spaces for dry sky, indentation and blank
lines are all free.

**The rule.** Exactly `a` flowers and exactly `b` trees stand in the column **immediately left or
immediately right of a shower** - dry, right at the edge of the rain, just missing it. Wet plants
never count; plants two or more columns clear never count. Everything else - which plants, how many
showers, how wide, how much of the garden gets rained on - is free.

**Intended discovery path.** Demo 1 gives the whole grammar (the clue is the bottom line, the rain
is a block, the picture is 3 lines and a garden). All the difficulty is "what do the two digits
count?". The obvious readings - *how many got rained on*, *how many stayed dry*, *how many
showers*, *how many showers have a plant under them* - are falsified in every shipped demo, so
rounds 2-3 burn on them and on the near miss *the plant under the last drop*. The crack is the
sentence a 12-year-old says while pointing at the picture: **"that one is standing right on the edge
of the shower and staying dry"**. Getting the relation but only from one side, or without telling
flowers from trees, still pays 27-46 %, so the gradient has no cliff.

**Degenerate witnesses closed.**
* *Well-formed picture only*: the two counts must both be exact, so format alone is 6-8 %.
* *Clue-derived seed*: the ground row must be copied verbatim, so no answer transfers between clues
  (demo replay 0.0 %, one fixed picture 7.0 %, grafting the previous demo's sky 9.2 %).
* *Minimal construction*: `a,b >= 1` and >= 2 showers kill "no rain" and "one shower"; a single
  shower has only two edges, so a+b >= 3 forces real placement.
* *Cheap templates*: solid rain with 2-wide holes 16.2 %, one big shower 4.0 %, regular stripes
  7.8 %, rain over the first a+b plants 0.0 %.
* *Distribution-matching sampler*: a sampler that learns solve()'s shower-count/width/gap
  distribution from 120 demos scores 10.0 %; the best of 15 hand-swept density settings is 13.2 %.
* *One-shot search*: each clue is answered once, so per-clue sweeping is impossible; a player needs
  a *procedure* that works on a fresh garden.

**Foothold (lever 7).** The natural first probe - "make it rain on that many plants" - scores
6.2 %, i.e. about 1 in 16 items, ~28 hits in a 0.5 s round. Nobody will conclude the grader is
exact-match, and every wrong reading of the relation still pays something.

## Witness table (400 fresh clues; every attacker knows the grammar perfectly and builds a legal
picture satisfying its own hypothesis, 500 tries per clue)

| attacker's law | rate |
|---|---|
| **the true rule (`solve`)** | **100.0 %** |
| the true rule, rebuilt independently by the attack harness | 99.2 % |
| **showers with a plant at their edge** (count showers, not plants - the same insight) | **84.8 %** |
| the rule with the two glyphs not told apart (a+b at the edges) | 39.5-46.2 % |
| the rule, digits swapped | 37.8 % |
| only the RIGHT edge counts | 33.2 % |
| right relation, sloppy execution (hang a shower beside a of them, ignore the rest) | 30.2 % |
| only the LEFT edge counts | 27.5 % |
| the rule, flowers only | 23.5 % |
| **solid rain with 2-wide holes at the first a+b plants** (best insight-free template) | **16.2 %** |
| within 2 dry columns of the rain | 16.2 % |
| best blind sampler, 15 density settings swept | 13.2 % |
| distribution-matching sampler learnt from 120 demos | 10.0 % |
| graft the previous demo's sky onto this clue | 9.2 % |
| random legal picture | 6.0-8.2 % |
| **"rain on a of them / b of them" (the natural first probe)** | **6.2 %** |
| showers containing a flower / a tree | 4.5-8.0 % |
| at the last WET column (the nose-vs-tail near miss) | 7.0-7.5 % |
| two columns clear of the rain | 5.2-7.8 % |
| regular stripes 4 rain / 3 dry | 7.8 % |
| one fixed picture for every clue | 7.0 % |
| a of them / b of them stay dry | 4.5-5.8 % |
| one big shower + a decoy | 4.0 % |
| beside rain, wet or dry | 1.0-2.0 % |
| rain over the first a+b plants | 0.0 % |
| previous clue's answer replayed | 0.0 % |
| empty / clue echoed / ground row alone / `"1"*100` / 4000 chars of junk | 0.0 % |

Tiers: **6-13 % (no idea) -> 16 % (best template) -> 27-33 % (one side of the relation, or the
relation applied carelessly) -> 39-46 % (the relation, glyphs not separated) -> 85 % (the relation
counted per shower) -> 100 % (the rule)**. Nothing above 16 % is reachable without the insight.

## Fairness floor

34 hand-built "count a relation in this picture" laws (wet / dry / at an edge / left edge only /
right edge only / first wet column / last wet column / within 2 / deep / far / under the widest
shower / in the first shower / in an odd shower / showers-with-one-under / showers-with-one-beside /
counts of plants / showers / gaps / and ten mixed pairs), evaluated against shipped demos:
survivors after 1 demo 2-5, after 2 demos 1-2, after 3 demos 1-2, and the last survivor is the true
rule in 6/6 trials (its only sibling is "showers with a plant at their edge", which is the same
insight). A centaur team that enumerates picture statistics at all gets there in two demos; the
whole difficulty is *looking there*, which is what the drawing is for.

**Demo guarantees** (the hill-climber in `solve()` chases them): 83 % of demos falsify **all** of
wet / dry / last-wet-column / beside-rain / showers-with-one-under / two-clear per glyph type and
shower count / gap count / widest shower / total wet plants, **and** show all five contrasts - a
plant on a shower's last wet column, a plant two columns clear, a plant deep inside a shower, a
plant far from any rain, and a shower that catches nobody. The remaining 17 % miss exactly one item.
Layout, rain glyph, dry glyph, sky height (2/3/4 rows), shower count (3-6) and widths (3-9) all vary
between demos, so no demo is a template for the next.

## Validation

`python tools/quickcheck.py challenges/lab/kelmar.json --seeds 200` -> **OK, no warnings**
(`gen=0.07 ms score=0.15 ms solve=250.8 ms`). Sizes: **score 497 / 512**, **solve 4984 / 5000**,
generate 801; clue 47-57 chars, solution 100-264 chars.

* 1200 fresh seeds: `generate` deterministic (identical on a repeat call), **mean 0.030 ms, max
  0.084 ms** (brief's < 1 ms met); `solve()` scores 1 on **1200/1200**, mean 33.8 ms, median 17.9 ms,
  p95 130 ms, max 277 ms (13 % of the 2 s cap, below quickcheck's 25 % warning).
* Scorer vs an **independent re-implementation** (column walk, no regex) on **14 800** (clue,
  answer) pairs - shipped demos plus 24 structural mutations each plus junk: **0 disagreements**.
* **11 400 junk strings**: 0 raises, 0 non-binary returns, 0 false positives, worst 0.046 ms.
* Leniency, 300 clues, all **100 %**: dots or spaces for dry sky, blank lines around the picture,
  trailing spaces, 2 or 5 sky rows, rain redrawn with `/`, CRLF.
* Strictness, 300 clues, all **0 %**: sky rows not identical, ground row missing or altered, one sky
  row only, empty sky, all rain, a text label added. Shifting the whole sky one column scores 4.3 %
  (a genuine coincidence rate, not a leniency hole).

## Predicted classification

**testing / on target, mean final 40-60 %** - the likeliest split is one crack in round 3-4 (the
picture states the relation, and two demos pin it for anyone enumerating picture statistics) and one
player parked at 25-45 % on "one side only" or "the relation without telling flowers from trees".
Predicted kid score **4.4-4.8 / 5**: rain falling on flowers is named instantly, the sentence "three
flowers and one tree are standing right on the edge of the rain" is one a 12-year-old says out loud,
and the counting is 3-of-8, not a statistic.

**The risk is too_easy, not too_hard** (the insight is one step past "who got rained on", and 85 %
is available from the shower-side reading of the same insight). Levers, in order:
1. count only plants at the edge of a shower **wider than the gap beside it** (kills the sloppy
   construction, keeps the sentence);
2. count **showers** that have exactly one plant at an edge, so the two readings stop agreeing;
3. make some showers stop short of the ground (virga: rain drawn as hanging blocks, only the bottom
   sky row counts) - adds a second, equally kid-legible clause;
4. a third glyph on the ground that never counts.
If it comes back under 15 %: drop the tree digit (one count only, which lifts the blind floor from
~7 % to ~25 %), or guarantee two counted plants side by side with a wet boundary plant between them.

Scratch harness for every number above (not committed):
`$SCRATCH/weather/{core,show,attack,hyp,selftest,ship,build}.py`.

## Arena (players NOT run; the orchestrator opens it)

```
pool   $SCRATCH/pool-kelmar-1/kelmar.json
setup  python sim/arena.py setup --run lab-kelmar-1 --teams kelmar1a,kelmar1b \
         --challenge-dir $SCRATCH/pool-kelmar-1 --arena-root $SCRATCH/lab-kelmar-1
```

---------------------------------------------------------------------------

# Iteration 2 — 2026-09-04 (v2, first version built for the 4-round / 3-demo / 7-class format)

## What the runs said

`lad-kelmar-v1-1` and `lad-crandel-v3-1`: **kelmar scored 0 % for all four Opus players.** Three of
them spent no demo on it — the clue `..*...Y..*../*2Y1` read as "a string plus a legend" and one
player logged it as a possible bar chart. The one player who did buy a demo read the sky rows as
"houses that grow by one" and never saw rain. So v1 failed both halves of the demo-economy test:
the clue revealed nothing about the answer's shape, and one demo was not enough to reach a
two-digit rule over ~60 probes a round.

Diagnosis, in the words of LADDER.md's format-shift note: *put the object in the clue, one clause,
the demo must teach the rule in one look.*

## What changed in v2

| | v1 | v2 |
|---|---|---|
| clue | `<ground>/*a Yb` — one line, a string and a legend | **the scene**: 2–3 empty sky rows of dots, the ground row, then the count line |
| ground row | 42–52 columns, 10–14 plants | **26–32 columns, 6–9 plants** (edges visible by eye) |
| counts | two (`a` flowers **and** `b` trees) | **one** (`N` plants) |
| showers | ≥3 wide, gap ≥2 | **3–6 wide**, gap ≥2 (the cap is load-bearing, see below) |
| scorer | last line must be the ground row verbatim | **any line containing `*`, `Y` or a digit is ignored** — echoing the ground row and/or the count line is free, so is leaving them out |
| demo look | any rain glyph, dots *or spaces* for dry sky | dots always, so the demo **is** the clue with rain painted into it |

Clue (seed 14) and the demo as it renders:

```
CLUE                            ANSWER (the demo)
..........................      ''''..'''..'''''....'''''.
..........................      ''''..'''..'''''....'''''.
..........................      ''''..'''..'''''....'''''.
_____Y___*__*__Y__Y___*___      _____Y___*__*__Y__Y___*___
2
        ^   ^  W  w  o   W      (key, never shown: ^ counts, w = on the last wet
                                 column, W = deep in the rain, o = two columns clear)
```

Both counted plants (`Y` at col 5, `*` at col 9) hang off the same little shower, one on each side;
six columns to the right the `Y` at col 15 stands on the shower's **last wet column** and does not
count, and the `Y` at col 18 stands **two columns clear** and does not count either. That triple is
guaranteed in every demo and lands within 9 columns in 95 % of them.

## One count or two — measured, then chosen

Blind floor over random legal pictures: **26.3 % with one count, 13.7 % with two.** Two counts is
the harder class, but in a 26–32 column garden only 75 % of demos can show a flower *and* a tree at
an edge **and** the three teaching contrasts, and "two flowers and one tree are standing right at
the edge of a shower" is no longer one breath. With three demos for seven classes the demo has to
teach in one look, so the second count was dropped and the higher floor was kept as the foothold.
The two glyphs stay in the drawing as a decoy dimension ("count the flowers at the edge") that
costs a round to kill.

## The 3–6 column width cap is load-bearing

Without a maximum width the class collapses to **solid rain with 2-wide holes over N plants** — a
2-wide hole at a plant makes exactly that plant an edge plant, so the template satisfies the rule by
construction. Measured: **34.3 % with a cap of 8, 22.0 % with 7, 0.0 % with the shipped cap of 6**,
because 6-wide showers cannot cover a 26–32 column garden. This is the same lesson as lever 8: test
the cheapest thing that *satisfies* the rule, not only the wrong rules.

## Witness table (500 fresh clues, shipped `kelmar.json`)

Every attacker except the two demo-less ones knows the grammar perfectly and rejection-samples legal
pictures (500 tries per clue) until its own hypothesis holds.

| attacker's law | rate |
|---|---|
| **the true rule (`solve`)** | **100.0 %** |
| showers with a plant at their edge, counted per SHOWER (the same insight) | 79.2 % |
| only the RIGHT edge counts | 49.8 % |
| only the LEFT edge counts | 49.4 % |
| plants within two dry columns of the rain | 35.8 % |
| **best blind sampler over 14 density settings** (best insight-free construction) | **34.6 %** |
| random legal showers (grammar only) | 28.4 % |
| rain on exactly N plants (the natural first probe) | 25.8 % |
| N showers | 23.0 % |
| plants on the LAST WET column (the nose-vs-tail near miss) | 21.6 % |
| N showers, each hung over a plant | 19.6 % |
| demo-less: N showers drawn over N plants | 17.4 % |
| demo replay (the previous clue's answer) | 15.4 % |
| plants exactly two columns clear | 14.6 % |
| N plants left dry, rain on all the others | 14.0 % |
| beside the rain, wet or dry | 9.8 % |
| one constant picture for every clue | 4.4 % |
| demo-less: freehand rain (widths 2–9, gaps 1–6) | 2.4 % |
| solid rain with 2-wide holes at N plants | 0.0 % |
| rain everywhere / clue returned unchanged (dry) / clue's picture without the count line | 0.0 % |
| empty / `x` / `1`*100 / 4000 chars of junk / a line of text / the ground row alone | 0.0 % |

**No insight-free construction exceeds 35 %.** The two rows above 49 % are the intended relation in
weaker form (one side of it only, or counted per shower instead of per plant); `solve()` makes the
per-shower reading disagree with the true one in 83 % of demos, so it is falsifiable from a demo.

**Foothold.** A demo-less team that draws freehand rain scores 2.4 % (its widths and gaps are
usually illegal), but the format sweep every player runs in round 1 finds the plateau immediately:

```
regular stripes, width w repeated with gap G     G=1     G=2     G=3     G=4
  w=2                                            0.0 %   0.0 %   0.0 %   0.0 %
  w=3                                            0.0 %  35.2 %  30.0 %  20.4 %
  w=4                                            0.0 %  31.8 %  30.8 %  25.6 %
  w=5                                            0.0 %  34.0 %  27.4 %  19.2 %
  w=6                                            0.0 %  28.2 %  28.6 %  20.2 %
  w=7, w=8                                       0.0 %   0.0 %   0.0 %   0.0 %
```

So a team with no demo can still score 20–35 % on this class and learn that it is picture-graded and
structural — which is exactly what the two failed runs did not get from any of their seven classes.

## Demo guarantees (measured over 400 shipped demos)

* a plant on a shower's last wet column: **100 %**; a plant exactly two columns clear: **100 %**;
  both within 9 columns of a counted plant: **95 %**; a plant deep inside the rain: 89 %.
* the per-shower sibling reading disagrees with the true one: **83 %** (it cannot for N = 1).
* all eight loud rivals (wet / dry / last wet column / two clear / within two / beside / per-shower /
  shower count) falsified at once: **72 %**; each one individually 83–100 %.
* both glyphs present at an edge when N ≥ 2: 76 % (kills "count the flowers at the edge" in one look).
* rain glyph (`|` / `'`), sky height (2–3) and shower count (2–5) vary between demos.

## Fairness floor

Of **20** hand-built "the digit counts THIS relation" laws, evaluated on shipped demos: **2.8 survive
one demo** (max 5), 1.4 survive two, 1.1 survive three, and whenever exactly one law survives three
demos it is the true rule (175/175 trials). One demo leaves a team with two or three live candidates
and ~120 probes over two rounds to separate them — the calibration target for this format.

## Validation

`python tools/quickcheck.py challenges/lab/kelmar.json --seeds 200` → **OK, no warnings**
(`gen=0.06 ms score=0.23 ms solve=51 ms`). Sizes: **score 496 / 512**, **solve 2329 / 5000**,
generate 659; clue 82–133 chars, solution 80–131.

* 2000 fresh seeds: `generate` deterministic, **mean 0.027 ms, max 0.14 ms** (< 1 ms met);
  `solve()` scores 1 on **2000/2000**, mean 37.5 ms, p95 44 ms, max 67 ms.
* Scorer vs an **independent re-implementation** (column walk, no regex) on **6300** (clue, answer)
  pairs — shipped demos plus 20 structural mutations each: **0 disagreements**.
* **2880 junk strings**: 0 raises, 0 non-binary returns, 0 false positives, worst 0.085 ms.
* Lenient, all **100 %**: dots / spaces / underscores for dry sky; rain as `#`, `|`, `/` or `'`; a
  cloud row on top; the ground row kept, dropped or even altered; the count line kept; blank lines;
  trailing spaces; CRLF; 2 or 5 sky rows.
* Strict, all **0 %**: one sky row only, sky rows not identical, empty sky, all rain, a text label
  added. Shifting the whole sky one column scores 22.3 % — the coincidence rate, not a hole.

## What a demo-less player can infer

The clue is a garden under an empty sky with a number under it, so the answer's shape is not in
doubt: *rows the width of the ground row, in the sky, with something drawn in them* — the picture
edited, not a code. What they cannot infer is what the number counts, and (until they sweep) that
the rain has to come in 3–6 wide showers with a 2-column gap.

## Predicted classification

**testing / on target, mean final 35–60 %.** Likeliest split: the player who spends a demo here
enumerates picture statistics, is left with two or three laws, and cracks it in round 3–4 about half
the time; the player who does not gets 20–35 % from the stripe plateau, and a player who reads the
relation per shower instead of per plant parks at ~79 %. Kid score should hold at 4.5+: it is rain
falling on a garden and the sentence is "two plants are standing right at the edge of a shower, just
out of the rain".

Risk, in order: (1) **too_easy** if the per-shower reading is enough for a crack — lever: require
each counted plant to be at the edge of a shower *wider than the gap next to it*, or count showers
with exactly one plant at an edge so the two readings stop agreeing; (2) the 26–35 % floor makes
hypothesis discrimination noisy — lever: bring back the second count (blind floor 13.7 %) now that
the clue carries the scene; (3) if it still comes back under 15 %, widen the garden to 34 columns so
there is room for a fourth shower, and let `solve()` put the counted plants on both sides of the
same shower every time.

Scratch harness for every number above (not committed):
`$SCRATCH/k2/{core,build,witness,selftest,holes,check}.py`.

## Arena (players NOT run; the orchestrator opens it)

```
pool   $SCRATCH/pool-kelmar-2/kelmar.json   (cp challenges/lab/kelmar.json into it)
setup  python sim/arena.py setup --run lad-kelmar-v2-1 --teams kelmar2a,kelmar2b \
         --challenge-dir $SCRATCH/pool-kelmar-2 --arena-root $SCRATCH/lad-kelmar-v2-1
```
