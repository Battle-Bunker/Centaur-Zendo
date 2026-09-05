"""Round 1: harvest clue formats as fast as possible (skip everything)."""

MAX_EXAMPLES_PER_NAME = 60


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory.setdefault("examples", {})
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    return None


def on_round_end(items, memory):
    examples = memory.setdefault("examples", {})
    for it in items:
        bucket = examples.setdefault(it.get("name", "?"), [])
        if len(bucket) < MAX_EXAMPLES_PER_NAME:
            bucket.append({"clue": it.get("clue"),
                           "answer": it.get("solution"),
                           "score": it.get("score")})
