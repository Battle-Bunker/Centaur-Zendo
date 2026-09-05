"""Weighted feature-predicate voting over multiple-choice rule classes."""
import json, os
import vote

_HERE = os.path.dirname(os.path.abspath(__file__))
try:
    W = json.load(open(os.path.join(_HERE, "weights.json")))
except Exception:
    W = {}

def on_round_start(memory):
    global W
    try:
        W = json.load(open(os.path.join(_HERE, "weights.json")))
    except Exception:
        pass
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1

def solve(name, clue, memory):
    try:
        i, cand = vote.pick(name, clue, W)
        if cand is None:
            return None
        if name == "ospren":
            return str(i + 1)
        return cand
    except Exception:
        return None

def on_round_end(items, memory):
    pass
