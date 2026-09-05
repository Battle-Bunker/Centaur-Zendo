"""Final brain: answer only the two classes with a measured positive hit-rate.
Everything else is skipped (instant, and skips help the fewer-answers tiebreak)."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import final_core


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1
    memory.setdefault("cache", {})


def solve(name, clue, memory):
    try:
        if name == "virel":
            return final_core.virel(clue)
        if name == "fennick":
            return final_core.fennick(clue)
    except Exception:
        return None
    return None


def on_round_end(items, memory):
    pass
