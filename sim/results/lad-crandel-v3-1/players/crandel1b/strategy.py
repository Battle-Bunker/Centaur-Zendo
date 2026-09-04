"""FINAL. Only `quaich` is understood; everything else is skipped (skips are ~3x
faster than answers, so skipping the six unknown classes roughly doubles the
number of quaich challenges seen inside the 3-second final, and it also wins the
fewer-answers tiebreak).

quaich: the clue is a row of R/G/B beads. The answer is a bar chart of how many
of each colour there are, columns in the order R, G, B, each bar drawn with its
own letter, empty cells '.', on a fixed axis len(clue)//2 tall (which is exactly
the largest a bar can ever be), with a '===' baseline underneath.
"""

ORDER = ("R", "G", "B")


def on_round_start(memory):
    memory["n"] = memory.get("n", 0) + 1


def solve(name, clue, memory):
    if name != "quaich":
        return None
    try:
        r = clue.count("R")
        g = clue.count("G")
        b = clue.count("B")
        out = []
        for h in range(len(clue) >> 1, 0, -1):
            out.append(("R" if r >= h else ".") +
                       ("G" if g >= h else ".") +
                       ("B" if b >= h else "."))
        out.append("===")
        return "\n".join(out)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
