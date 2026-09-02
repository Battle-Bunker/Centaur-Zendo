"""orlan solver.

Learned from ~66 confirmed-correct examples:
  * an answer is "r1,c1>r2,c2" (0-indexed row,col): move the 'o' at (r1,c1)
    to the empty cell (r2,c2), in a straight orthogonal line.  Walls '#' and
    enemies 'x' may be crossed; another 'o' may not.
  * the destination is ALWAYS within Manhattan distance 2 of an 'x' (66/66).
  * among those, prefer the destination with the most 'x' exactly two cells
    away in a straight line, then the fewest adjacent 'o', then reading order.
Measured ~25% correct vs ~7% for a random legal move.
"""

DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))
OFF2 = ((-2, 0), (2, 0), (0, -2), (0, 2))
NEAR2 = ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0),
         (0, -2), (0, 2), (-1, -1), (-1, 1), (1, -1), (1, 1))


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        g = clue.split("\n")
        nr = len(g)
        nc = len(g[0])
        xs = set()
        os_ = []
        for r in range(nr):
            row = g[r]
            for c in range(nc):
                v = row[c]
                if v == 'x':
                    xs.add((r, c))
                elif v == 'o':
                    os_.append((r, c))
        if not xs or not os_:
            return None
        near = set()
        for (xr, xc) in xs:
            for dr, dc in NEAR2:
                near.add((xr + dr, xc + dc))
        oset = set(os_)
        best = None
        for (r, c) in os_:
            for dr, dc in DIRS:
                rr = r + dr
                cc = c + dc
                while 0 <= rr < nr and 0 <= cc < nc:
                    v = g[rr][cc]
                    if v == 'o':
                        break
                    if v == '.' and (rr, cc) in near:
                        s2 = 0
                        for ar, ac in OFF2:
                            if (rr + ar, cc + ac) in xs:
                                s2 += 1
                        no = 0
                        for ar, ac in DIRS:
                            p = (rr + ar, cc + ac)
                            if p in oset and p != (r, c):
                                no += 1
                        k = (-s2, no, r, c, rr, cc)
                        if best is None or k < best:
                            best = k
                    rr += dr
                    cc += dc
        if best is None:
            return None
        return "%d,%d>%d,%d" % best[2:]
    except Exception:
        return None


def on_round_end(items, memory):
    try:
        memory["last_correct"] = sum(1 for it in items if it.get("score"))
        memory["last_presented"] = len(items)
    except Exception:
        pass
