"""Round 1: pure harvest. Skip everything instantly to see as many clues as possible."""

MAX_EXAMPLES_PER_NAME = 400


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
        bucket.append({"clue": it.get("clue"),
                       "answer": it.get("solution"),
                       "score": it.get("score")})
        if len(bucket) > MAX_EXAMPLES_PER_NAME:
            examples[it.get("name", "?")] = bucket[-MAX_EXAMPLES_PER_NAME:]
