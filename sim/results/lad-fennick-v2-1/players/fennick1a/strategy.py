"""Final strategy.

The single challenge class `fennick` renders an ASCII bar chart over the clue
body.  Format is fully reverse-engineered (see NOTES.md); the per-letter bar
HEIGHT rule was not cracked, and the checker is exact-match (40 candidate
height rules tested across rounds 3-4, all 0/1200).  Since a wrong answer and
a skip both score 0, and the tiebreak rewards FEWER answers, we skip.
"""

def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1

def solve(name, clue, memory):
    return None

def on_round_end(items, memory):
    pass
