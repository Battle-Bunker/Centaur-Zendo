"""strategy.py - tovel1b

House convention (learned from demos): the answer is the WHOLE clue with the
picture edited in place; the trailing "N word" line is kept verbatim.  N is a
COUNT of the events to draw, not a parameter.
"""

import re

QUOTE = chr(39)
BACK = chr(92)


def _tail_n(clue):
    """Number on the trailing (or, for garrow, leading) caption line."""
    lines = clue.split("\n")
    m = re.match(r"^\s*(\d+)\s+\w+\s*$", lines[-1])
    if m:
        return int(m.group(1))
    m = re.match(r"^\s*\S+\s+(\d+)\s+\w+\s*$", lines[0])
    if m:
        return int(m.group(1))
    return None


# ---------------------------------------------------------------- norvel
def solve_norvel(clue):
    lines = clue.split("\n")
    rows = [i for i, ln in enumerate(lines) if "|" in ln]
    if len(rows) < 3:
        return None
    hi, si, ki = rows[0], rows[1], rows[2]

    def steps(ln):
        return [i for i, ch in enumerate(ln) if ch in "x."]

    hp, sp, kp = steps(lines[hi]), steps(lines[si]), steps(lines[ki])
    n = min(len(hp), len(sp), len(kp))
    hat = [lines[hi][p] for p in hp[:n]]
    sn = [lines[si][p] for p in sp[:n]]
    kick = [lines[ki][p] for p in kp[:n]]
    out = list(sn)
    for j in range(n):
        if sn[j] == "x" and hat[j] == "." and kick[j] == ".":
            k = None
            for t in range(j + 1, n):
                if hat[t] == "x":
                    k = t
                    break
            if k is None:
                continue
            for t in range(j, k):
                out[t] = "-"
            out[k] = "x"
    row = list(lines[si])
    for idx, p in enumerate(sp[:n]):
        row[p] = out[idx]
    lines[si] = "".join(row)
    return "\n".join(lines)


# ---------------------------------------------------------------- kelmar
def solve_kelmar(clue):
    lines = clue.split("\n")
    n = _tail_n(clue)
    if n is None:
        return None
    pic = lines[:-1]
    if len(pic) < 3:
        return None
    ground = pic[-1]
    trunk_row = pic[1]
    trees = []
    for m in re.finditer(QUOTE + "+", trunk_row):
        a, b = m.start(), m.end() - 1
        h = 0
        for r in range(1, len(pic) - 1):
            if a < len(pic[r]) and pic[r][a] == QUOTE:
                h += 1
        trees.append((a, b, h, b - a + 1))
    if not trees:
        return clue
    hmax = max(t[2] for t in trees)
    picks = []
    for i, ch in enumerate(ground):
        if ch != "*":
            continue
        if any(a <= i <= b for a, b, h, w in trees):
            continue
        for a, b, h, w in trees:
            if h != hmax:
                continue
            if b == i - 1:
                picks.append((i, "L"))
                break
            if a == i + 1:
                picks.append((i, "R"))
                break
    # Only answer when the picture forces the answer: the count of flowers
    # standing beside a tallest tree must equal the stated number of leans.
    # (Measured over 160 logged items: base==N -> 72/72 correct,
    #  base!=N -> 0/88.  So skipping the rest is free precision.)
    if len(picks) != n:
        return None
    g = list(ground)
    for i, side in picks:
        g[i] = BACK if side == "L" else "/"
    pic[-1] = "".join(g)
    return "\n".join(pic + [lines[-1]])


# ---------------------------------------------------------------- dispatch
def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        if name == "norvel":
            return solve_norvel(clue)
        if name == "kelmar":
            return solve_kelmar(clue)
        # Everything else: only the "no events" clues are safe -- the picture
        # is unchanged.  Anything else, skip (fast, and good for the tiebreak).
        if _tail_n(clue) == 0:
            return clue
        return None
    except Exception:
        return None


def on_round_end(items, memory):
    pass
