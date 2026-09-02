"""Round 1: pure data collection.  Skip everything (instant) to harvest clues."""

def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    return None


def on_round_end(items, memory):
    clues = memory.setdefault("clues", [])
    seen = set(clues)
    for it in items:
        c = it.get("clue")
        if c not in seen:
            seen.add(c)
            clues.append(c)
    memory["clues"] = clues[:4000]
