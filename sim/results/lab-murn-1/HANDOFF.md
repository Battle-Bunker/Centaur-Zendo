# lab-murn-1 — ready for player agents (designer could not spawn them)

The arena is **set up and the server is running**; challenge `murn` validated OK inside the
engine (`/admin/reports`: no errors, no warnings). The designer session has no Agent tool,
so steps 4–7 of `sim/DESIGN_LOOP.md` are left to the orchestrator.

* run name: `lab-murn-1`   port: 33411   pool: 1 challenge (`murn`)
* config: 6 training rounds, 5 s cooldown, 0.5 s rounds, 3 s final, training window 6 h
  (started 2026-09-02 ~10:28 UTC — plenty of head-room, but do not leave it for hours)
* team dirs:
  * murna: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-murn-1/players/murna`
  * murnb: `/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad/lab-murn-1/players/murnb`
* filled-in player briefs (give the agent the file's text and NOTHING else):
  * `sim/results/lab-murn-1/BRIEF_murna.md`
  * `sim/results/lab-murn-1/BRIEF_murnb.md`

To run: spawn two general-purpose Opus agents in parallel with those brief texts, wait for
both, then

    python sim/arena.py teardown --run lab-murn-1
    python sim/arena.py report   --run lab-murn-1

Classification thresholds for this class: a player who has the rule right scores ~100 %
(measured), a player with any of the natural wrong priors scores 0–5 %, and the one partial
witness (right support law, no quota) scores ~11 %. So the final hit-rate is close to
all-or-nothing: ≥90 % = cracked, ~10 % = has the support law but not the count, <5 % = failed.

If the arena has to be rebuilt from scratch:

    mkdir -p $SCRATCH/pool-murn-1 && cp challenges/lab/murn.json $SCRATCH/pool-murn-1/
    python sim/arena.py setup --run lab-murn-1 --teams murna,murnb \
        --challenge-dir $SCRATCH/pool-murn-1 --arena-root $SCRATCH/lab-murn-1
