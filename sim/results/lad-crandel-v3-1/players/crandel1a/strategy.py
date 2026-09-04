"""FINAL strategy.

Only one class was cracked: quaich.

Evidence (19 attempts across rounds 3 and 4 with axis "RGB" and heights = the
raw R/G/B counts):  exactly 2 scored 1, and those 2 are exactly the clues whose
counts satisfy count(R) < count(B) < count(G).  So the reference chart puts the
SMALLEST count on the R bar, the MIDDLE count on the B bar and the LARGEST count
on the G bar -- the raw-count chart is right only when the counts already sit in
that order.  Final answer therefore uses the sorted assignment, which reproduces
both known-correct answers exactly and generalises to the other 17.

House drawing style (learned from the fennick demo):
    a bar of height h = (h-1) rows of the column's own character with a '_' cap
    on row h; then the axis row; then '=' * width.

Every other class scored 0 on ~260 distinct hypotheses, so they are skipped:
a skip is instant (more challenges seen => more quaich) and does not count
against the fewer-answers tiebreak.
"""

CACHE = {}


def on_round_start(memory):
    CACHE.clear()


def quaich_answer(clue):
    r = clue.count("R")
    g = clue.count("G")
    b = clue.count("B")
    lo, mid, hi = sorted((r, g, b))
    h = (lo, hi, mid)          # R gets the smallest bar, G the tallest, B the middle
    out = []
    for lvl in range(hi, 0, -1):
        row = []
        for i, ch in enumerate("RGB"):
            if h[i] > lvl:
                row.append(ch)
            elif h[i] == lvl:
                row.append("_")
            else:
                row.append(" ")
        out.append("".join(row))
    out.append("RGB")
    out.append("===")
    return "\n".join(out)


def solve(name, clue, memory):
    if name != "quaich":
        return None
    try:
        a = CACHE.get(clue)
        if a is None:
            a = quaich_answer(clue)
            CACHE[clue] = a
        return a
    except Exception:
        return None


def on_round_end(items, memory):
    pass
