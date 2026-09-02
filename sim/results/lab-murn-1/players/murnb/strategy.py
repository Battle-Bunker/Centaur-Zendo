"""murn: the answer is a grid of rows (newline separated), all the same width,
whose LAST row is the clue row and which contains exactly N '#' in total.
A cell above the bottom row is legal only if, among the three cells directly
below it (c-1, c, c+1, in-bounds), exactly 2 are non-'.' for a '#', and
exactly 1 for an 'o'.  '.' is unconstrained.  Grid height is free.

Build upward: each level place '#' on every column with support 2; if more are
still needed keep an adjacent pair alive (adding an 'o' on a support-1 column
when necessary) so the next level has capacity again.
"""

MAXLEVELS = 40


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def _sup(below, W):
    s = [0] * W
    for c in range(W):
        n = 0
        if c and below[c - 1] != ".":
            n += 1
        if below[c] != ".":
            n += 1
        if c + 1 < W and below[c + 1] != ".":
            n += 1
        s[c] = n
    return s


def build(row, K):
    W = len(row)
    if K < 0:
        return None
    below = row
    rows = []                                   # bottom-up
    rem = K
    for _ in range(MAXLEVELS):
        if rem <= 0:
            break
        s = _sup(below, W)
        c2 = [c for c in range(W) if s[c] == 2]
        new = ["."] * W
        if rem <= len(c2):
            for c in c2[:rem]:
                new[c] = "#"
            rem = 0
        else:
            for c in c2:
                new[c] = "#"
            rem -= len(c2)
            # keep an adjacent pair alive for the next level
            if not any(new[c] != "." and new[c + 1] != "." for c in range(W - 1)):
                done = False
                for c in range(W - 1):
                    if new[c] != "." and s[c + 1] == 1:
                        new[c + 1] = "o"; done = True; break
                    if new[c + 1] != "." and s[c] == 1:
                        new[c] = "o"; done = True; break
                if not done:
                    for c in range(W - 1):
                        if s[c] == 1 and s[c + 1] == 1:
                            new[c] = "o"; new[c + 1] = "o"; done = True; break
            if all(ch == "." for ch in new):
                return None
        line = "".join(new)
        rows.append(line)
        below = line
    if rem > 0:
        return None
    rows.reverse()
    rows.append(row)
    out = "\n".join(rows)
    return out if len(out) <= 1024 else None


def solve(name, clue, memory):
    try:
        row, _, n = clue.rpartition("|")
        return build(row, int(n) - row.count("#"))
    except Exception:
        return None


def on_round_end(items, memory):
    pass
