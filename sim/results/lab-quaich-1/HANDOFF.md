# lab-quaich-1 — arena is set up and running; players not yet run

The designer agent had **no Agent/Task tool**, so per `sim/DESIGN_LOOP.md` step 4 it stopped
after step 3. Everything below is ready to go.

* run: `lab-quaich-1`   port: 47571   pool: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/pool-quaich-1` (1 challenge: `quaich`)
* arena root: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-quaich-1`
* team dirs:
  * quaicha: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-quaich-1/players/quaicha`
  * quaichb: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-quaich-1/players/quaichb`
* config: 6 training rounds, 0.5 s each, 5 s cooldown, 1 demo per window, 3 s final,
  training window 6 h (plenty of head-room).

## To run the players

Spawn two general-purpose Opus agents in parallel, each given the text of
`sim/PLAYER_AGENT_BRIEF.md` with {TEAM_DIR} set to that team's directory above,
{ROUNDS}=6, {COOLDOWN}=5, {ROUND_SECONDS}=0.5, and nothing else.

Then:

    python sim/arena.py teardown --run lab-quaich-1
    python sim/arena.py report   --run lab-quaich-1

If the server has died in the meantime, re-create it with:

    python sim/arena.py setup --run lab-quaich-1 --teams quaicha,quaichb \
      --challenge-dir /tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/pool-quaich-1 --arena-root /tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-quaich-1

(or point `--challenge-dir` at a fresh copy of `challenges/lab/quaich.json`).

## What to classify

Hit rate in the 3 s final: >=90 % cracked, 10-90 % partial, <10 % failed. The measured
difficulty gradient (see the design report) predicts ~15-32 % for a player who finds the
pairing but not the wholeness clause, ~0.4 % for a player who only finds the anagram.
