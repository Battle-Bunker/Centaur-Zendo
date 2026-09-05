import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine, fennick, garrow

RULE = engine.EXTRACT
GARROW_MODES = 5
PROBE_GARROW = False


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        if name in RULE:
            return engine.pick(name, clue)
        if name == "fennick":
            r = fennick.solve_fennick(clue)
            return r[0] if r else None
        if name == "garrow" and PROBE_GARROW:
            i = memory.get("_index", 0)
            return garrow.solve_garrow(clue, i % GARROW_MODES)
    except Exception:
        return None
    return None


def on_round_end(items, memory):
    memory["last"] = [{"n": it.get("name"), "c": it.get("clue"),
                       "a": it.get("solution"), "s": it.get("score")}
                      for it in items]
