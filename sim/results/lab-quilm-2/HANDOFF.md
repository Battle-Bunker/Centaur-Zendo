# lab-quilm-2 — arena is up, players not run (designer has no Agent tool)

* run `lab-quilm-2`, server `ws://127.0.0.1:36625/ws`, pool `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/pool-quilm-2` (quilm v2 only, 1 accepted)
* 6 training rounds, 0.5 s each, 5 s cooldown, 1 demo per window, 3 s final
* team dirs:
  * `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-quilm-2/players/quilm2a`
  * `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-quilm-2/players/quilm2b`
* filled briefs: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/BRIEF_quilm2a.md`, `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/BRIEF_quilm2b.md` (opus, general-purpose, background, in parallel, brief text only)
* after both finish: `python sim/arena.py teardown --run lab-quilm-2 && python sim/arena.py report --run lab-quilm-2`

Neither team has used a round or a demo. Training window closes ~6 h after
2026-09-02 11:09 UTC, final window 1 h after that.

Reading the result (v2 has a built-in difficulty gradient, so read the final rate, not just
cracked/not):
* < 5 % — no insight (blind probes alone are worth ~2.6 %, and ~4.6 % for one coincidental family).
* ~40 % — they learned which single-digit swaps are legal but not the balance rule
  (single-digit answers cap at 40.5 %).
* > 90 % — full rule; 100 % is reachable at 0.05 ms/answer.
