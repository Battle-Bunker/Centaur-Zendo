# Player-agent brief (template; fill in /tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-murn-2/players/murn2a, 6, 5, 0.5)

You are the AI half of a "centaur" team playing Centaur Zendo. Your working directory is
`/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-murn-2/players/murn2a` (call it TEAM_DIR); it contains `PLAYER_GUIDE.md` (read it fully first), the
reference client `player.py`, the strategy file `strategy.py` (the file you edit), and
`connection.txt` with your server URL, team name and token.

RULES OF THE GAME (strict — this is a confidentiality test of the game, not of you):
* Work ONLY inside TEAM_DIR. Do not read, list, grep or search anything outside it — in
  particular never look at the game repository (/home/user/Centaur-Zendo), its `challenges/`
  folder, `engine/`, `SPEC.md`, any other team's directory, or any process list / server
  files. The only information you may use about the challenges is what the server sends
  you. Do not use web search.
* You get at most 6 training rounds of 0.5 s each, with a 5-second
  cooldown between them, one demo per window, and then ONE 3-second final. The final score
  is the number of correct answers in the final; ties are broken by fewer answers submitted.

LOOP (repeat until your training rounds are used up):
1. Run a round: `cd TEAM_DIR && set -a && . ./connection.txt && set +a && python player.py wait-round`
   (round zero: run it as-is with the default random strategy to collect data).
2. Read `logs/summary.txt` and the latest `logs/round_N.txt`. For each challenge name,
   hypothesise what the clue means and what a correct answer looks like. Keep a running
   `NOTES.md` in TEAM_DIR: per challenge name — your current hypothesis, evidence,
   confidence, what you'll test next.
3. Spend your demo wisely: `python player.py demo NAME` shows one solved example (clue +
   correct solution) of that class. You get one per window (after each round, before the
   next). Demos are recorded in `logs/demos.jsonl`.
4. Edit `strategy.py`: implement solvers for the classes you understand; for unknown ones,
   answer cheap informative guesses (or return None to skip) — every answer costs time in
   the round and speed matters. Guard every solver with try/except and keep each answer
   under ~10 ms. Test your solvers locally against the clues in your logs before running
   the next round (scratch scripts inside TEAM_DIR are fine).
5. Go to 1. The client waits for the cooldown automatically.

When rounds are exhausted (`python player.py status` shows rounds_used), review
`strategy.py` for speed and robustness, then run `python player.py final` exactly once (the
final opens as soon as your training rounds are used) and report.

Be efficient with your own time: ~2–4 minutes of analysis and coding per round is the pace.

REPORT BACK (concise): a table of your per-round correct/answered, what you believe each
challenge class is (name → rule) with your confidence, which demos you used and why, your
final score, and what feedback about the game's design/fairness/fun you would give the
organisers.
