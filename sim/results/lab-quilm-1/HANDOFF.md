# lab-quilm-1 — handoff (designer could not spawn player agents)

The arena is **already set up and running**. sim/DESIGN_LOOP.md steps 1-3 are done;
steps 4-7 (two Opus player agents, teardown, report, classify) need an orchestrator with
the Agent tool.

* run: `lab-quilm-1`   server: `ws://127.0.0.1:35521/ws`   pool: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/pool-quilm-1` (quilm only, 1 accepted)
* config: 6 training rounds, 0.5 s each, 5 s cooldown, 1 demo per window, 3 s final
* team dirs (give one to each agent as `{TEAM_DIR}`):
  * `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-quilm-1/players/quilma`
  * `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-quilm-1/players/quilmb`
* ready-to-paste briefs (sim/PLAYER_AGENT_BRIEF.md with the placeholders filled):
  `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/BRIEF_quilma.md`, `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/BRIEF_quilmb.md`
* spawn both in parallel: `subagent_type: general-purpose`, `model: opus`,
  `run_in_background: true`; give them the brief text and nothing else.
* when both finish:
  `python sim/arena.py teardown --run lab-quilm-1 && python sim/arena.py report --run lab-quilm-1`

Neither team has used a round or a demo yet (a throwaway team was used for the plumbing
smoke test and the arena was then rebuilt clean). Training window closes ~6 h after
2026-09-02 10:30 UTC; the final window is 1 h after that.
If the window has expired, re-run the setup command in NOTES_everyday.md with `--run lab-quilm-2`.

Classification thresholds: cracked = final hit-rate >= 90 %, partial = 10-90 %, failed = < 10 %.
Note when reading a "partial": with 50 distinct clues, a player who memorises demo
answers alone can reach ~12 % without any insight, so treat < ~15 % as failed-with-memorisation.
