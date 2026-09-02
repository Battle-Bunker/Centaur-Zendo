def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1

def solve(name, clue, memory):
    return None

def on_round_end(items, memory):
    seen = memory.setdefault("clues", [])
    for it in items:
        seen.append(it.get("clue"))
    memory["clues"] = seen[-3000:]
