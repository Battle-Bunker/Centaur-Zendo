# NOTES_sport — direction: sport and scoring

Brief: a small ASCII picture/list/table a kid recognises instantly (scoreboard, league table,
race result, darts board, bowling frame, pitch from above); the clue pins an arbitrary-but-natural
*measurement* of it that has no name and is **not** the object's famous operation. Close every
degenerate witness, leave a foothold, keep the drawing small, make the counted relation the
headline of every demo. Shipped: `challenges/lab/morvin.json`.

## 1. Brainstorm (12-year-old test applied to each)

Test 1 = can a kid name the object from one demo? Test 2 = is the pinned pattern *not* nameable
and not the object's famous operation? Test 3 = can the relation be the loudest thing in a small
drawing? Test 4 = is there a cheap template that satisfies the rule without insight?

| # | object (what the demo draws) | the measurement pinned by the clue | verdict |
|---|---|---|---|
| 1 | **Ten-pin rack** — 3–5 frames of the 4/3/2/1 pin triangle, `o` standing, `.` down, with the pins-down count written over each frame | pins that fell **although every pin immediately in front of them is still standing** | **PICKED.** T1 iconic; T2 no name for it (bowling's "split"/"sleeper" mean other things) and the famous operation (strike/spare bonus arithmetic) is falsified because the clue already gives the pinfall; T3 the counted pin is a hole with an intact wall in front of it; T4 the obvious templates cap at 34 % (measured) |
| 2 | **Race snapshot** — 6 lanes of a track/pool with one runner mark per lane | pairs of runners exactly level **in neighbouring lanes** ("neck and neck") | T1/T2/T3 good, but the answer is nearly unconstrained (any picture is legal), so the clue has no visible seed and the blind floor is set by one statistic only. Runner-up; kept as the fallback if morvin needs replacing |
| 3 | **League table** (P W D L Pts) | teams with **more wins than the team directly above them** | T1 great, T2 fair, but this is "an adjacent-column inversion", squarely inside the statistic family Opus players enumerate on tables (measured behaviour: they hunt statistics after rebuilding the grammar). Predicted too easy |
| 4 | **League table + form string** (`WWDLW`) | teams whose form contains a loss immediately followed by a win | Dies on T2: bigram counting is the first thing tried on a letter string (quaich's players found bigram frequencies unaided) |
| 5 | **Penalty shootout grid** (two rows of 5 `O`/`X`) | kicks scored immediately after the other team missed | T1/T2 fine, but 2×5 binary cells is a 1024-answer space per clue: too small, demos give it away |
| 6 | **High-jump card** (heights × `O`/`XO`/`XXO`) | first-time clearances right after a height that took three attempts | T2 excellent, T1 weak: a US/UK 12-year-old does not read a high-jump card on sight |
| 7 | **Basketball quarter scoreboard** | quarters in which the trailing team outscored the leader | T1 great, T2 poor: "lead change"/"comeback quarter" is nameable, and the numbers invite arithmetic, the anti-pattern |
| 8 | **Olympic medal table** (G S B per country) | countries whose three counts strictly decrease | T1 fine, T3 poor: nothing is *drawn*, it is a 3-column arithmetic predicate |
| 9 | **Goal timeline** (a 0–90 minute bar with goal marks per team) | goals scored within 5 minutes of the other team's goal | T2 good, T3 good, T4 bad: "adjacent marks within k" is a one-parameter sweep, a template family that solves it without the idea |
| 10 | **Archery/darts target** with arrow marks | arrows touching another arrow | T2 fails: the famous operation *is* scoring the rings, and the counted relation collapses to "adjacent pairs" |
| 11 | **Knockout bracket** | winners who won both rounds by one goal | T1 good, but the drawing costs 12–20 lines (a judge has already penalised 30-line demos) |
| 12 | **Football pitch from above** (`x`/`o` players) | attackers with no defender between them and the goal | Dies on T2: that is offside, a named rule, and the models reach for it immediately |

## 2. Why #1 wins

* The **clue is itself a bowling scoreline** — `7395/2` — so the seed is visible *inside* the
  picture (count the dots in a frame, it is the digit above it), which is the property every star
  in `STARS.md` shares.
* The rule is a **two-place, oriented, exact** relation — the shape that has actually worked
  (LegoZendo's 1-pin same-orientation join, virel's brick on its twin, basten's nose-not-tail,
  murn's exactly-two supports). Front, not back; *every* pin in front, not *some*.
* The object's famous operation (strike/spare bonus scoring, "how many did you knock down") is
  handed over in the clue, so it cannot be the answer.
* A 12-year-old can state the rule in one sentence — *"count the pins that fell even though the
  pins in front of them are still standing"* — and can point at instances in the drawing. They can
  also settle the orientation question the models will get wrong ("the ball comes from the point").
* The picture is **5 lines** whatever the clue.

## 3. What was shipped — `morvin`

**Rule (private).** Clue `<digits>/<n>`: 3–5 digits, each 1–9, are the pins knocked down in each
frame; `n` is 0–12. The answer is five lines: the digits again as a header row, then the frames'
pin decks side by side, each a 4/3/2/1 triangle with the **head pin (nearest the bowler) on the
last line** — `o` a pin standing, `.` a pin down. Frame *k* must show exactly digit-*k* dots.
Exactly `n` pins in the whole picture must be pins that **fell although every pin immediately in
front of them is still standing** ("in front" = the one or two pins of the next row toward the
head pin; the head pin has none in front of it and never counts). Nothing else is required: the
drawing may be indented or not, the frames may be any shape that meets the counts.

**Intended discovery path.**
1. One demo ⇒ "bowling frames", and the header digits are the dot counts (self-evident, both are
   printed). All the difficulty is `n`.
2. The natural first probe — knock the pins nearest the bowler first, the physical strike order —
   scores **100 % on the 23 % of clues with `n=0`** and 0 % elsewhere. That is the foothold, and
   it is a *hint*, not just a score: `n=0` forces every fallen pin to have a fallen pin in front of
   it, so `n` counts pins that **fell out of turn**.
3. From there the family is right and the demos discriminate inside it: every shipped demo has the
   EXISTS reading (some pin in front standing), the MIRROR reading (every pin *behind* standing)
   and the complement (standing pins with everything in front down) all *present but unequal to*
   `n`, plus a near miss (a fallen pin with one standing and one fallen pin in front) that shows
   "every" is doing work. 202 hand-built local statistics collapse to a unique rule in 3 demos.

**Degenerate witnesses closed.** Well-formed-but-blind picture (10.8 %); clue-derived seed — `n`
is never the frame count, the pin total or the standing total, and the digit header is verified;
minimal construction — there is none, the answer is a choice of *which* pins fall, not how many;
cheap templates — front-first plus `n` stray pins at the back tops out at 34 % because a stray
behind an already-cleared row is not counted; demo replay 0 %, previous demo patched to the new
digits 2 %, one fixed answer 0.1 %.

## 4. Witness table (800 fresh clues, one shot per clue, attacker knows the format perfectly)

| attack | overall | on `n=0` clues | on `n>0` clues |
|---|---|---|---|
| random legal racks (format only) — the blind floor | 10.8 % | 0.0 % | 12.2 % |
| **front-first: knock the pins nearest the bowler — the natural first probe** | **21.4 %** | **100.0 %** | 0.0 % |
| connected blob grown from the head pin | 18.2 % | 80.7 % | 0.2 % |
| reading-order: knock from the top of the drawing | 3.5 % | 0.0 % | 4.5 % |
| **EXISTS: fallen with SOME pin in front standing** (the near miss) | **30.9 %** | 100.0 % | 14.5 % |
| front-OR-back version | 29.0 % | 21.1 % | 28.1 % |
| ghosts, but only in the back two rows | 25.2 % | 5.8 % | 27.8 % |
| frames that contain at least one ghost | 25.0 % | 100.0 % | 4.9 % |
| MIRROR: fallen with every pin BEHIND standing (drawing read upside down) | 7.9 % | 0.0 % | 10.2 % |
| head pin counts too (no *fallen* pin in front) | 2.9 % | 0.0 % | 3.2 % |
| standing pins with all pins in front fallen (the complement) | 9.6 % | 0.0 % | 11.8 % |
| isolated fallen pins | 8.0 % | 0.0 % | 9.4 % |
| fallen pins in the back row | 8.8 % | 1.2 % | 14.5 % |
| fully cleared rows | 6.2 % | 0.0 % | 6.4 % |
| isolated standing pins | 8.2 % | 0.6 % | 9.9 % |
| touching standing pairs | 2.1 % | 0.0 % | 1.9 % |
| **templates**: best of 10 rotated knock-orders | 21.4 % | | |
| **templates**: oracle-tuned per-digit rack table (ceiling of any `n`-blind template) | 26.0 % | | |
| **templates**: front-first + `n` strays (random / back row / spread along the back) | 26.4 / 34.0 / 34.2 % | | |
| ... same, best of 20 retries per clue (unreachable upper bound, the player cannot see the score) | 64.3 % | | |
| copy the previous demo, patch the dot counts | 2.0 % | | |
| demo replay (previous clue's answer) | 0.0 % | | |
| one fixed answer for every clue | 0.1 % | | |
| empty, spaces, `0`, `1`, `x`, `1`×100, `o`×4000, the clue, a rack with no header | 0 % | | |
| **the true rule** (independent re-implementation, bowling pin numbering) | **100.0 %** | 100.0 % | 100.0 % |

Ceiling of every template ≤ 34 %, floor of the natural first probe 21 %, blind floor 11 %.
Gradient: 11 % (format) → 21 % (physical strike order) → 25–34 % (right family, wrong quantifier
or wrong direction) → 100 % (the rule).

**Hypothesis-family test.** 202 hand-built statistics of the picture (subject fallen/standing ×
direction front/back/side/any × quantifier all/any/none × target fallen/standing × 4 row
restrictions, plus 10 global tallies): survivors after 1 demo 4–46, after 2 demos 2–39, **after 3
demos exactly 2 in all six trials** — and those two are the same rule stated two ways ("all pins in
front standing" ≡ "no pin in front fallen"). The fairness floor holds: ≤ 6 demos plus probing is
enough for a team that computes statistics on the demos at all.

## 5. Demo guarantees (91 % of demos are grade 0; 1 % fall through to the weakest grade)

Every grade-0 demo carries: a counted pin with **two** standing pins in front of it; a counted pin
in the row immediately behind a **standing head pin** (kills the "back rows only" reading); a near
miss (one standing, one fallen pin in front); a fallen pin with everything in front of it already
down; at least one frame with no counted pin and one frame with ≥ 2; the head pin down in some
frames and standing in others; and `n` different from the three hard rivals and from at most one of
eleven soft ones. On `n=0` demos the head pin is necessarily down in *every* frame (the rule forces
it) — that is itself the picture of the foothold.

Three demos, as players see them:

```
7222/5                      4469/0                      7559/5
 7     2     2     2         4     4     6     9         7     5     5     9
o..o  oooo  o.oo  o.oo      oooo  oooo  o.oo  ...o      ....  oo.o  .ooo  .o..
 .o.   oo.   ooo   oo.       ..o   oo.   ..o   ...       oo.   .o.   .oo   ...
  ..    oo    .o    oo        .o    ..    ..    ..        ..    o.    ..    ..
   .     .     o     o         .     .     .     .         o     .     .     .
```

## 6. Validation

`python tools/quickcheck.py challenges/lab/morvin.json --seeds 200` → **OK**, no warnings
(gen 0.07 ms, score 0.09 ms, solve 47.8 ms worst).
Sizes: `score` **452** chars (cap 512), `solve` **3958** (cap 5000), `generate` 597; clue ≤ 8
chars, solution ≤ 142 chars. `generate` **0.015 ms** per call and deterministic (1500 re-draws
identical). 5000 fresh clues: `solve` scores 1 on **5000/5000**, mean 3.7 ms, median 1.7 ms,
p99 40 ms, max 68 ms. `score` on junk 0.0005 ms, 0.065 ms on a 1500-char answer; returns 0 or 1
only, never raises, 0 on the empty string. Scorer cross-checked against an independent
re-implementation (bowling pin numbers 1–10 with a hardcoded in-front list) on **24 000**
(clue, answer) pairs — real answers, 14 kinds of mutation (whitespace, indentation stripped,
tabs, case, deletions, insertions, line shuffles, reversed drawings, truncations) and other
clues' answers — with **0 disagreements**.
`solve()` leaks no template: counted pins land on all nine eligible cells (7–17 % each), fallen
pins are near-uniform over all ten (8–13 %), and the mean counted pins per frame position varies
only 1.03–1.39 across 3-, 4- and 5-frame clues.

## 7. Predicted classification

**On target (testing → calibrated), predicted mean final 35–60 % over two Opus players**: expect
one crack and one partial in the 20–35 % band (the foothold plus a near-miss reading). The
distinctive asset versus basten/tovel — which both stalled one step short at ~30 % — is that the
foothold is *informative* rather than merely scoring: `n=0` pays 100 % only for the physically
correct "the ball took the front pins first", which states the rule's shape out loud. The honest
risk in the other direction is a double crack (both players sweep local neighbourhood statistics
against 3 demos and the family collapses to one rule), which would put this at `too_easy`.
Predicted kid score **4.3–4.7/5**: the object is 5/5 (a bowling frame with the pinfall written
above it), the rule is one sentence a 12-year-old can check by pointing, and the kid's own
contribution — *which way is the bowler?* — is the half the models get wrong (the MIRROR reading
scores 8 %).

**Levers if it comes out too easy** (in order): require *both* pins in front to exist and be
standing, so only the three interior pins can ever count and the EXISTS reading dies at ~0 %;
drop the header row so the digit↔dot mapping has to be found; add a second clause (the last frame
must contain no counted pin). **If too hard**: raise the `n=0` share from 23 % to ~35 %, and
guarantee a counted pin and a near miss *side by side in the same frame* in every demo.

## morvin v1 ladder run `lad-morvin-v1-1` (2026-09-04, 6×0.5 s, 2 Opus players)

| team | profile | final | cracked | how |
|---|---|---|---|---|
| morvin1a | opus-default | 100% (3615/3615, 6 skips) | round 4 | library of server-confirmed (digit,value)→block arrangements + DP; never stated the rule |
| morvin1b | opus-kidproxy | 100% | round 3 | insight: "the dots are falling and some are stuck in mid-air" — floating dots = K |

Too easy for Opus (2 finals, both 100%). Two leaks: (1) the insight route is short — the kid
reading ("gravity puzzle in a numeral costume") is exactly the rule and the kid-proxy had it by
round 3; (2) the **tabulation route**: blocks are independent and K is additive across blocks, so
a player can probe one block at a time (hundreds of single-block probes) and build a
(digit, value) → arrangement library without ever understanding it. 1a did exactly that and
finished at 100% with a lookup table. 1a also flagged clues it believed unsatisfiable
(`316/9`, `366/12`, `769/11`) — its model was wrong (b solved everything), but check that
generate() never emits an unachievable K anyway.

Hardening levers for v2 (keep the pin-deck picture and the kid reading): (a) break additivity —
make K a property that spans blocks (e.g. count only floating pins in frames where the frame to
the left also has a floating pin; or count floating pins whose supporting pin is in the *next*
frame's deck) so single-block probing cannot build a table; (b) vary the deck (a 3-row deck of
6 pins for some frames) so per-digit tables do not transfer; (c) forbid the k=0 fill-from-front
foothold from being 23% of clues — keep it at ~10% as the foothold. Judge note: the rule is close
to nameable ("fell out of turn"); (a) also helps there.
