# Challenge design loop (for designer agents)

Goal: a challenge class that Opus-level centaur players **sometimes crack and sometimes
don't** (partial success across two players: one crack + one partial/fail, or two partials) under the fast cadence: **4 training rounds of 0.5 s, 5 s cooldown, 3 demo requests per
game for a pool of 7 classes, then a 3 s final.** Difficulty must come from **lateral
thinking, novel (invented) rules and reduced clue information**, not from more advanced
mathematics or bigger search.

**The demo economy (2026-09-04).** A team sees seven classes and may ask for a solved example
of only three of them. A balanced class therefore sits *right on the edge of needing a demo*:
- the **clue alone must reveal the shape of an answer** — what kind of data to send (a grid the
  size of the clue's row, a list of words, one number, a picture of the object named by the
  clue) — so that a team without a demo can produce well-formed answers and score *sometimes*
  (the foothold, lever 7);
- the **rule** (which well-formed answers score) should usually need the example, so that
  teams that spend a demo here do markedly better than teams that spend it elsewhere.
Two identical teams with different demo choices should finish with different scores. A class
whose clue is an opaque code (nothing about the answer's type can be inferred) fails the
first half; a class that is cracked without a demo by most Opus players fails the second.

**The most reliable way to reveal the answer's shape: put the object in the clue.** The clue
carries the uncut / unfilled / unmarked picture and the answer is *the same picture, edited*:
garrow's clue is the whole pizza and the answer adds knife lines; fennick's clue is the shelf and
the answer draws the books; norvel's clue is the kick row and the answer adds the snare row under
it. A player who has never seen a demo can still send back the clue's picture with a plausible
edit, which is a well-formed attempt (the foothold), and the demo then teaches the rule.
House rule (published in the player guide, 2026-09-05): the scorer must accept the answer with
the clue's trailing parameter line kept OR dropped — a validation player lost rounds to that
inconsistency across classes. Test both in the witness table. A clue
that is only digits (morvin v2: `1|8|7|9/3`) tells a demo-less player nothing about the drawing
convention and scores 2/5 on `clue_shape`; prefer drawing the object into the clue over adding
legends or labels.

## What the players actually do (measured in sim1/sim2, read before designing)
* Round 1 is usually a **skip-only harvest** (~450 clues per 0.5 s round, zero cost).
* They cycle several candidate answer *formats* per class within one round using
  `memory["_index"]`, reading back which scored. **One round ≈ 450 graded binary probes.**
  Over 4 rounds that is ~1,800 probes plus 3 demos for 7 classes.
* Any **named textbook object** (CRT, Pell, Nim, nonogram, de Bruijn...) is recognised from
  the name and clue shape in round 1 with no demo. Pun names are read instantly.
* Demos are decisive when the rule is novel: `LegoZendo` (a human-invented rule) needed
  **3–4 demos** and was the last class cracked in a 32-class pool; every textbook class
  needed 0–1.
* Once *any* rule consistent with the feedback is found, players submit the **minimal
  witness** (e.g. one 2×3N rectangle for LegoZendo) and never learn the intended rule. If
  your scorer admits a trivial family of answers, the insight is optional.

## The 12-year-old test (read this twice)

The best challenge is one a smart 12-year-old could understand from ONE demo and contribute
insight to, but that an Opus-level agent alone struggles with for many rounds. Two halves:

1. **The object must be evocable by a kid from one demo.** LegoZendo's demo is a picture of
   bricks; any bright kid says "that's Lego!" instantly. Seven-segment digits, dominoes,
   dice, clocks, calendars, hopscotch, jigsaws, skipping rhymes, braids, shoelaces, Tetris,
   snakes-and-ladders, playing cards, coins, keyboards, music, sports scores, recipes: use
   the world kids live in, not the world of contests. Draw it (ASCII art is fine).
2. **The pinned pattern must NOT be nameable.** Once the object is recognised, "which pattern
   does the clue pin?" must still take real experimentation: LegoZendo counts *1-pin
   connections between same-letter bricks of the same orientation* — nobody has a name for
   that. If the rule is the object's famous operation ("move one matchstick", "knight's
   tour", "sum to seven") the model recognises the genre and the game is over (quilm).
   Good rules are arbitrary-but-natural *measurements* of the object: count the joins of a
   certain width, the bricks that hang over an edge, the dominoes whose pips face each other,
   the clock hands that would collide.

Anti-patterns (these are what an LLM produces by default, and what an LLM cracks by default):
number theory, graph theory, SAT, ciphers, automata, formal grammars, "find x such that",
anything with a Wikipedia page, anything from a programming contest. If your idea would be at
home in an RLVR training set, throw it away. The same priors that generate a problem make it
guessable by the same model; deliberately reach for the concrete, the childish, the physical,
the social.

## Hardening levers (in order of leverage)
1. **Force the insight through the solution set**: the clue should give a partial object
   that must be *completed*, or constraints that exclude the degenerate witness, so that
   scoring 1 requires the rule and not a trivial construction.
2. **Reduce clue information**: the clue is a few characters; the structure comes from the
   rule, not the clue. The scorer still verifies from the clue alone (SPEC §2: no secrets).
3. **Compose two independent clauses** (players must discover both; demos only ever show
   satisfying examples, so negative evidence costs them a round each).
4. **Make `solve()` output varied and non-revealing**: randomise cosmetics (filler,
   letters, layout) with `random.Random(clue)`, include decoys that satisfy nothing, and
   never emit the minimal witness. Demos are the main leak.
5. **Neutral names**: no puns, no abbreviations of the concept. Use a random short word.
6. Never: encode the rule in the name; use a named puzzle; rely on obscure knowledge.
7. **Leave a foothold** (learned on tovel v3, 2026-09-04): after closing witnesses, check
   that some cheap, natural first probe still scores *sometimes* (5–30 %) — e.g. the minimal
   construction on the easiest parameter value. If every cheap probe scores 0, Opus players
   conclude the grader is exact-match, call the decoys "arbitrary data" and farm demos; the
   kid-proxy on tovel v3 saw the rule's shape ("K and O take turns") and never tested it.
   Hardening and footholds trade off: the witness table must show both the ceiling of every
   template (≤ ~60 %) and the floor of the natural first probe (> 0).
8. **Test templates, not only wrong rules**: the leaks that reached 88–100 % (velk v1, tovel
   v2) were cheap constructions that *satisfy the true rule* without insight (alternate the
   clue strand with free filler; a solid stripe from day n). Every witness table must include
   "the simplest thing that satisfies the rule" and "copy the demo's shape, adjust one knob".
9. **Salience beats rule changes for softening**: basten 7 % → 33 % and garrow 15 % → 64 %
   came from redrawing the demo (fewer fish so nibblers dominate; uneven slices so neatness is
   visibly irrelevant) with the rule untouched. Players rebuild the picture grammar perfectly
   and then hunt statistics; the counted relationship must be the loudest thing in the picture.

Fairness floor: a strong human+AI team must be able to get it from ≤6 demos plus probing
with real insight. Deterministic generator; property-based scorer; the scorer must reject
junk and the empty string; caps: score ≤ 512 chars, clue ≤ 1024, solution ≤ 1024, generate
≤ 50k, solve ≤ 5k; the `words` module (English dictionary: `words.WORDS`, `words.COMMON`,
`is_word`, `vowels`, `consonants`, `pick`) is pre-imported for word-based ideas; generate < 100 ms, score < 50 ms on junk, solve < 2 s.

## Procedure (max 3 iterations, 2 players per iteration)
1. Write `challenges/lab/<NAME>.json` (SPEC §2 fields; `author` = your direction name;
   `description` = honest private notes incl. the intended discovery path and the
   degenerate witnesses you closed). Validate: `python tools/quickcheck.py challenges/lab/<NAME>.json -v`.
   Self-test the scorer against hand-built adversarial answers (minimal witnesses, corner
   cases, disconnected/wrong-count variants) — anything trivial that scores 1 is a leak.
2. Private pool: `mkdir -p $SCRATCH/pool-<NAME>-<k> && cp challenges/lab/<NAME>.json $SCRATCH/pool-<NAME>-<k>/`
   where `$SCRATCH=/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad`.
3. Arena (defaults are already 4 rounds / 5 s / 0.5 s / 3 demos; the ladder builds 7-class pools — do NOT pass --port, a free one is chosen):
   `python sim/arena.py setup --run lab-<NAME>-<k> --teams <NAME>a,<NAME>b --challenge-dir $SCRATCH/pool-<NAME>-<k> --arena-root $SCRATCH/lab-<NAME>-<k>`
   It prints each team's directory.
4. Spawn **two player agents in parallel** with the Agent tool (`subagent_type:
   general-purpose`, `model: opus`, `run_in_background: true`), each given the text of
   `sim/PLAYER_AGENT_BRIEF.md` with `{TEAM_DIR}` = that team's directory, `{ROUNDS}`=4,
   `{COOLDOWN}`=5, `{ROUND_SECONDS}`=0.5. Give them NOTHING else. Wait for both to finish.
5. `python sim/arena.py teardown --run lab-<NAME>-<k>` then `python sim/arena.py report --run lab-<NAME>-<k>`.
   Read `sim/results/lab-<NAME>-<k>/REPORT.md`, each player's `NOTES.md` and their reports.
6. Classify each player on the class: **cracked** (final hit-rate ≥ 90 %), **partial**
   (10–90 %), **failed** (< 10 %). Record what rule they *believed* and which demos/probes
   got them there.
7. Decide: all cracked ⇒ harden (levers above; close the witness they used); none cracked
   and no partial progress ⇒ soften slightly (one more bit of clue, a more telling demo).
   Mixed ⇒ you are on target; one more iteration to confirm if budget allows.
8. Keep the final JSON in `challenges/lab/<NAME>.json` (overwrite each iteration; keep
   earlier versions as `<NAME>.v1.json`, `<NAME>.v2.json` for the record). Do not commit.

If the Agent tool is unavailable to you, stop after step 3 and report the arena details;
the orchestrator will run the players.

## Report format
Name, one-paragraph rule (private), the discovery path you intended, per-iteration table
(iteration → version → players → outcome, demos used, rounds to crack, rule they
believed), the witness leaks you closed, and your final classification (too easy / on
target / too hard) with evidence.

## Calibrating for the thin channel (added 2026-09-04 after the first 7-class run)
With 7 classes in the pool a class sees ~60 probes per 0.5 s round, 4 rounds, and a demo only if
the player chooses it. Measured: a collection tuned for the old single-class format scored 0 % on
6 of 7 classes with or without demos. Design for this budget:
* **One clause.** A kid says the rule in one breath; the demo plus ~120 probes must suffice.
  Two-clause rules (weekday window + blocked middle + anchor) are for the old format.
* **The clue carries the object**; the answer is the clue's picture edited. A demo-less player
  can then send the picture with a plausible edit and score sometimes (the foothold).
* **Demos must teach the rule in one look**: every demo shows the counted relation loudly and
  a near-miss beside it; with three demos for seven classes nobody gets a second example.
* Target per class, two Opus players in a 7-pool: the player who spends a demo on it cracks it
  about half the time; the player who does not scores 5–30 % from the foothold.

## The checksum caption (2026-09-05, picture pool run 4)

Measured across 10 Opus finals: a caption that **counts the edits in the answer** ("3 fall",
"2 turn", "2 lean") is the single design feature that decides whether a class is crackable. With
it, a player tests a hypothesis offline against ~70 harvested clues (does my rule make exactly n
edits?) and needs no training round; without it (a free parameter such as a fish count or `X/n/d`)
every hypothesis costs a slice of a round and the class is demo-or-nothing — and players never
spend a demo on a class whose answer *shape* is already obvious from the clue. Rules:
1. Every picture class carries a checksum caption that names the verb and counts the edits.
2. The without-demo rate is then set by how guessable the **edit itself** is from the clue. durnel
   (turn a lorry round = reverse its arrow) was guessed and cracked 100 % blind; fennick (a stack
   shears one column and its lid becomes a slash) was not, 11 % blind, ~95 % with a demo. Aim for
   the fennick shape: the picture shows *what* changes, the demo shows *how* it changes.
3. Keep ~12 % of clues at n = 0 so the echoed clue scores: it verifies the format for free.
