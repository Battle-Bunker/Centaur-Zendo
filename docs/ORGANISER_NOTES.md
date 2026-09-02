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
