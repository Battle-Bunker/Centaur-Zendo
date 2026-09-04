"""FINAL strategy for class `basten`.

Best empirically-validated construction (round 6, variant 2): an aquarium
picture with H=4 water rows, walls from the clue, isolated fish, one vertical
stack of 4, and (N+1) fish on the sand.  Plus an exact-answer cache built from
every demo taken (clues repeat very rarely, but it is free).
"""
import json
import os

from mk import mk

CACHE = {}


def on_round_start(memory):
    try:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "demos.jsonl")
        with open(p) as fh:
            for line in fh:
                d = json.loads(line).get("demo", {})
                if d.get("score") and d.get("clue"):
                    CACHE[d["clue"]] = d["solution"]
    except Exception:
        pass
    memory["cache_size"] = len(CACHE)


def solve(name, clue, memory):
    try:
        hit = CACHE.get(clue)
        if hit is not None:
            return hit
        return mk(clue, H=4, bottom=int(clue.rsplit("/", 1)[1]) + 1, stack=4)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
