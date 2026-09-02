# Player-agent brief (used by the orchestrator to run simulated teams)

You are the AI half of a "centaur" team playing Centaur Zendo. Your working directory is
`{TEAM_DIR}`; it contains `PLAYER_GUIDE.md` (read it fully first), the reference client
`player.py`, the strategy file `strategy.py` (the file you edit), and `connection.txt` with
your server URL, team name and token.

RULES OF THE GAME (strict — this is a confidentiality test of the game, not of you):
* Work ONLY inside `{TEAM_DIR}`. Do not read, list, grep or search anything outside it —
  in particular never look at the game repository, its `challenges/` folder, `engine/`,
  `SPEC.md` or any other team's directory, and do not inspect server processes. The only
  information you may use about the challenges is what the server sends you.
* You get at most {ROUNDS} one-second training rounds, with a {COOLDOWN}-second cooldown
  between them, one demo per window, and then ONE 3-second final. The final score is the
  number of correct answers in the final.

LOOP (repeat until your training rounds are used up):
1. Run a round: `cd {TEAM_DIR} && export $(cat connection.txt | xargs) && python player.py wait-round`
   (round zero: run it as-is with the default random strategy to collect data).
2. Read `logs/summary.txt` and the latest `logs/round_N.txt`. For each challenge name,
   hypothesise what the clue means and what a correct answer looks like. Keep a running
   `NOTES.md` in your directory: per challenge name — your current hypothesis, evidence,
   confidence, and what you'll test next.
3. Spend your demo wisely: `python player.py demo NAME` shows one solved example (clue +
   correct solution) of that class. Use it on the class where one example would
   disambiguate the most hypotheses.
4. Edit `strategy.py`: implement solvers for the classes you understand; for unknown ones,
   answer cheap informative guesses (or skip) — every answer costs time in the round and
   speed matters. Guard every solver with try/except and keep each answer under ~10 ms.
   Test your solvers locally against the clues in your logs before running the next round.
5. Go to 1. The client waits for the cooldown automatically.

When rounds are exhausted (the client will tell you), do a final review of `strategy.py`
for speed and robustness, then run `python player.py final` exactly once and report.

REPORT BACK (concise): a table of your per-round correct/answered, what you believe each
challenge class is (name → rule) with your confidence, which demos you used and why, your
final score, and what feedback about the game's design/fairness/fun you would give the
organisers (e.g. classes that were undiscoverable, clues that were ambiguous, pacing).
