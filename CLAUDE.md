# Centaur Zendo — resume instructions for any Claude session

This repo runs an **indefinite optimisation ladder**: challenge classes are bred, played by diverse
AI player agents in confidential arenas, judged for 12-year-old understandability, and refined until
the collection is a diverse set of classes that Opus-level centaur players crack about half the time.

**If you are resuming (after compaction, a quota cut, or a new session):**
1. Read `ladder/LADDER.md` (the loop, roles, budget rules, what a tick is).
2. Run `python ladder/ladder.py status` — the current ladder and the job queue.
3. Continue the loop from the queue. Never exceed the agent budget in `ladder/state.json`.
4. After every completed job: `python ladder/ladder.py ingest <run>` / `record-qual`, then
   `python ladder/ladder.py report`, then commit and push.

Game format (2026-09-04): 4 training rounds × 0.5 s, 7 classes per game, 3 demo requests per team per
game (one class each); clues must reveal the answer's shape, the rule usually needs a demo.

Two class paradigms: picture classes (object in the clue, answer = the picture edited) and
rule-family classes (`docs/RULE_FAMILIES.md`: hidden rule from a finite universe, clue = a minimal
set of positive examples, answer = another instance; obvious rule types deliberately excluded).

Engine/docs: `SPEC.md`, `docs/`, `sim/DESIGN_LOOP.md`. Results: `sim/results/`. Lab: `challenges/lab/`.
