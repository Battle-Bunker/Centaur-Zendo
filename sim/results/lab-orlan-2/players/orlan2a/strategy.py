"""strategy.py — orlan (final).

Move model (fits all 60 known-correct answers, including all 7 demos):
an 'o' moves two *non-wall* steps in one orthogonal direction.  '#' cells are
transparent: they are skipped, they neither block the move nor count as a step.
The intermediate non-wall cell and the landing cell must both be '.'.

Selection heuristic (learned from the unbiased sample, ~57% there vs 17% for a
uniform pick inside the same move set): prefer moving a stone that stands
orthogonally next to an enemy 'x', then the lowest such stone on the board,
then the leftmost, then the latest direction in the order up, down, left, right.
"""

DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))    # index 0..3 = up, down, left, right


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        g = clue.split("\n")
        if g and g[-1] == "":
            g = g[:-1]
        H = len(g)
        if not H:
            return None
        W = len(g[0])
        best = None
        bkey = None
        for r in range(H):
            row = g[r]
            for c in range(W):
                if row[c] != "o":
                    continue
                # enemies orthogonally adjacent to this stone
                sx = 0
                if r and g[r - 1][c] == "x":
                    sx += 1
                if r + 1 < H and g[r + 1][c] == "x":
                    sx += 1
                if c and row[c - 1] == "x":
                    sx += 1
                if c + 1 < W and row[c + 1] == "x":
                    sx += 1
                for di in range(4):
                    dr, dc = DIRS[di]
                    tr = r; tc = c; steps = 0; ok = True
                    while steps < 2:
                        tr += dr; tc += dc
                        if not (0 <= tr < H and 0 <= tc < W):
                            ok = False; break
                        ch = g[tr][tc]
                        if ch == "#":
                            continue
                        if ch != ".":
                            ok = False; break
                        steps += 1
                    if not ok:
                        continue
                    key = (-sx, -r, c, -di)
                    if bkey is None or key < bkey:
                        bkey = key
                        best = (r, c, tr, tc)
        if best is None:
            return None
        return "%d,%d>%d,%d" % best
    except Exception:
        return None


def on_round_end(items, memory):
    pass
