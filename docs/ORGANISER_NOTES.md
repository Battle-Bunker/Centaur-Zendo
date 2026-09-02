# Organiser notes

## Judgement calls made while building (overturn as you see fit)

| # | Decision | Why | Where to change |
|---|----------|-----|-----------------|
| 1 | Clues and solutions are plain strings (structured data is JSON-encoded by convention). | Simplest possible wire format for kids' bots. | `SPEC.md` §2, `engine/game.py` |
| 2 | No hidden "secret" channel from `generate` to `score`: the clue must carry everything the scorer needs. | Keeps the short scorer honest ("verify-easy, find-hard") and Zendo-like: the scorer *is* nature's rule. | `SPEC.md` §2 |
| 3 | Training time limit = `12 × cooldown + 60 s` **and** a hard cap of 12 rounds, both enforced. | Matches the "61 minutes for 5-minute cooldowns" example; a 30 s cooldown therefore gives 7 minutes, not 15.5. The hard cap makes the round count independent of how fast teams react. | `GameConfig.training_seconds`, `max_training_rounds` |
| 4 | One demo per cooldown window, available at game start and after every completed round; unused demos do not accumulate. | "Between rounds" read literally; a demo before round one gives round zero something to look at. | `engine/game.py` demo bookkeeping |
| 5 | The final uses one shared (challenge, seed) sequence for every team. | Fairness: teams face identical problems in the same order. | `GameConfig.final_shared_sequence`, `final_seed` |
| 6 | Leaderboard: ran-final first, then correct desc, then fewer answers, then name. | Rewards precision; a no-show never outranks a team that tried. | `Game.leaderboard()` |
| 7 | Challenge selection within a round is uniform over the accepted pool. | No weighting yet; easy to add per-challenge weights to the JSON later. | `CompiledPool.random_challenge` |
| 8 | Late/stale answers get an `error{code:"stale"}` reply rather than silence. | Helps players debug timing; the client tolerates one trailing stale frame after `round_over`. | `engine/game.py` |
| 9 | Additional caps beyond the four requested: submission (solution) length 1024 chars, equal to the clue cap; generate 100 ms, score 50 ms, solve 2 s wall-clock per call; 20 validation seeds. | A round must not be stalled by a slow scorer. | `engine/config.py` |
| 10 | Sandbox = restricted builtins + module allow-list + subprocess + wall-clock kill. Not a security boundary. | Adequate for a supervised kids' event; organisers should read submissions before loading them. | `docs/CHALLENGE_AUTHORING.md` |
| 11 | Open registration by default: an unknown team name in `join` is created with the supplied token. | Zero-admin setup for a classroom. Set `open_registration=false` and pre-register for a public event. | `GameConfig.open_registration` |
| 12 | Simulation used a 30 s cooldown with an effectively unlimited training window and the 12-round hard cap. | LLM players think for minutes between rounds, so the wall-clock limit was not the binding constraint. | `sim/arena.py --training-seconds` |

## Challenge ideas rejected by the original 256-char scorer cap

(The default cap was raised to 512 when the human-designed `LegoZendo` scorer needed ~440 chars even fully golfed.)

Every brainstorming agent hit the cap. Raising `max_score_code_chars` to about **320–350**
would unlock most of these (details in `challenges/NOTES_*.md`):

| would need ≈ | idea | direction |
|---|---|---|
| 265 | Minesweeper reconstruction | grids |
| 270 | Knight's tour on a small board | grids |
| 300 | Zeckendorf representation | numbers |
| 300 | Word search in a letter grid | strings |
| 300 | Weighted interval scheduling, two-resource knapsack | optimisation |
| 320 | 24-game with division (`TOPPLE` currently drops `/`) | optimisation |
| 320 | Find n with φ(n)=m | numbers |
| 330 | Truth table → minimal sum-of-products | logic |
| 400 | Max-flow / min-cut lite; polyomino exact cover | optimisation / grids |
| 450 | String-rewriting (MIU / Post) derivations | strings |

Ideas that no cap can rescue: anything needing a dictionary in the scorer (real-word
anagrams, crosswords, "decrypts to English"), and abc-triples / anything needing
factorisation of several numbers inside the scorer.

## Held-in-reserve challenges that already fit the cap

`NONCE` (hash prefix search), `NOFIX` (derangement anagram), `VIGCRIB` (Vigenère with
known key length), `CRATE` (bin packing), `HOARD` (knapsack), `BLANKET` (set cover),
`polska` (RPN program induction; full spec in `challenges/NOTES_logic.md` §8), `dama`
(n-queens completion). See the NOTES files for sketches.

## Challenge design lab (fast cadence: 6 rounds × 0.5 s, 5 s thinking, 3 s final)

Five designer agents each built a challenge from a lateral direction and iterated against pairs of fresh
Opus player agents in private arenas (`sim/DESIGN_LOOP.md`, results under `sim/results/lab-*`,
challenges under `challenges/lab/`). Classification per player: cracked ≥ 90 % in the final, partial
10–90 %, failed < 10 %.

| class | direction | v1 outcome | v2 outcome | verdict |
|---|---|---|---|---|
| `quaich` | invented 3-cycle bracket notation | cracked (r5–6, 3 demos) + partial 23 % | — | on target |
| `OKRIN` | sparse clue, forced completion, 3 clauses | cracked (r4, 3 demos) + partial 73 % | — | on target |
| `murn` | invented support physics | cracked r6 + cracked r5 | (see results) | see `NOTES_physics.md` |
| `orlan` | invented board game | partial 32 % + partial 29 % (law never found) | (see results) | see `NOTES_game.md` |
| `quilm` | everyday object (seven-segment) | cracked r4 + r6 | cracked r3 + r5 (faster) | too easy for Opus; good for kids |

What made the on-target ones work, and the principles now in `sim/DESIGN_LOOP.md`:

* **Two or three independent clauses**, each scoring 0 alone. Demos only show satisfying examples, so
  the second clause costs a round of falsifying probes. The failed players converged on a statistical
  proxy (a bigram model, a lookup table) that plateaued and *felt* like progress.
* **Close the degenerate witness.** LegoZendo v1 was "cracked" by a 2×3N rectangle without anyone
  finding the rule; the solution set must force the insight (forced completion, seeds, counts).
* **Absolute-readout rules are scan-solvable.** If `property(answer) == clue`, a fixed answer sent
  against every clue reads the property off (quilm v1). Prefer relational rules (answer built against
  the clue).
* **The three-word test.** If the puzzle can be named in three words ("move one matchstick"), the model
  holds a prior over the whole rule and recognition replaces inference (quilm v2, all 31 textbook
  classes). Recognising the object must be necessary but not sufficient.
* **Rejection-only clauses are undiscoverable.** A constraint that only ever shows up as a 0 (quilm's
  anagram exclusion, OKRIN's seed clause) belongs in `generate()`, not `score()`.
* **Players' toolkit is stable across all runs**: a skip-only harvest round (~450–800 free clues),
  then rounds used as factorial experiments cycling candidate answers by `memory["_index"]`, then
  constraint propagation over the labelled answers. Design against that, not against guessing.
* **The final is a throughput benchmark once solved.** Every player flagged that 100 % teams are
  separated only by socket round-trips. Consider scoring the final on a fixed number of presented
  challenges, or `correct − λ·wrong`, if insight rather than throughput should decide ties.
