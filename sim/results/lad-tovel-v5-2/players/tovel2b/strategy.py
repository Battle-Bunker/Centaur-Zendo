"""Round 3: fennick solver + big hypothesis sweep."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solvers import fennick_solve
import hyp4 as hyp3

VARIANTS = hyp3.VARIANTS
_counts = {}


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1
    _counts.clear()


def solve(name, clue, memory):
    try:
        if name == "fennick":
            return fennick_solve(clue)
        fns = VARIANTS.get(name)
        if not fns:
            return None
        i = _counts.get(name, 0)
        _counts[name] = i + 1
        return fns[i % len(fns)](clue)
    except Exception:
        return None


def on_round_end(items, memory):
    memory["last_round_items"] = len(items)
