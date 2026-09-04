"""fennick — final strategy.

The class 'fennick' gives clue "<row>/<L d L d L d L d>" and wants an ASCII
bar chart: rows top-to-bottom, each column c holding letter row[c] repeated
`height[c]` times upward from the baseline, the bottom row equal to the clue
row, then a line of '=' as long as the row.

The checker is lenient: it validates that shape plus four per-letter facts
encoded by the key digits.  I could not identify the statistic (every
height-subset count, every neighbour/order statistic and every per-letter
aggregate I could construct was falsified by controlled rounds), so the
heights are sampled uniformly from 1..4 — the distribution whose measured
hit-rate was highest (~1.6%).  Fast (~0.15 ms) and exception-proof.
"""
import random

_R = random.Random()
_RI = _R.randint


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    try:
        left = clue.rsplit("/", 1)[0]
        n = len(left)
        hs = [0 if left[c] == "." else _RI(1, 4) for c in range(n)]
        H = max(hs)
        if H < 1:
            return None
        out = []
        for r in range(H, 0, -1):
            out.append("".join(left[c] if hs[c] >= r else "." for c in range(n)))
        out.append("=" * n)
        return "\n".join(out)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
