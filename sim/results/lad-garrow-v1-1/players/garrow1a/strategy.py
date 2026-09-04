"""garrow — final strategy.

Clue  : "<X><n><Y><m>" + a 6-line grid (2 '#' borders, 4 content rows) whose
        content rows carry 2-character dominoes (aa, bb, cc, mm, oo, pp, ss, tt).
Answer: the same grid with '|' inserted at chosen cut columns.

What the data says (≈260 scored answers + 4 reference demos):
  * the answer is a vertical partition of the strip; 7 pieces (6 cuts) with
    every piece 3..7 columns wide is what every reference solution used
    (one used 8 pieces).
  * the number of dominoes of a named letter that a cut passes through
    ("severed") is the quantity the clue numbers track: every reference
    solution has severed(L) <= n_L.  Measured hit rates over 255 scored
    answers: severed == n_L with 7 pieces 6/21 (29%), severed == n_L-1 with
    7 pieces 21/179 (12%), severed <= n_L-2 0/27.  So we aim for
    severed(L) == n_L and fall back to n_L - 1 when no partition exists.
"""
import re, random

_hdr = re.compile(r'([a-z])(\d+)')
WMIN, WMAX = 3, 7
NCUTS = 6


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def _sev_table(rows, W, letter):
    """s[c] = number of `letter` dominoes split by a cut placed before column c."""
    s = [0] * W
    for row in rows:
        prev = row[0]
        for c in range(1, W):
            ch = row[c]
            if ch == prev and ch == letter:
                s[c] += 1
            prev = ch
    return s


def _sample(W, sx, tx, sy, ty, nc):
    """Uniformly random cut set: nc cuts, widths WMIN..WMAX, exact sever totals."""
    if tx < 0 or ty < 0:
        return None
    memo = {}

    def cnt(pos, k, ax, ay):
        if k == nc:
            r = W - pos
            return 1 if (WMIN <= r <= WMAX and ax == tx and ay == ty) else 0
        key = (pos, k, ax, ay)
        v = memo.get(key)
        if v is not None:
            return v
        s = 0
        hi = min(pos + WMAX, W - WMIN)
        for c in range(pos + WMIN, hi + 1):
            nx = ax + sx[c]
            ny = ay + sy[c]
            if nx > tx or ny > ty:
                continue
            s += cnt(c, k + 1, nx, ny)
        memo[key] = s
        return s

    total = cnt(0, 0, 0, 0)
    if total == 0:
        return None
    pos = k = ax = ay = 0
    cuts = []
    while k < nc:
        r = random.randrange(total)
        hi = min(pos + WMAX, W - WMIN)
        for c in range(pos + WMIN, hi + 1):
            nx = ax + sx[c]
            ny = ay + sy[c]
            if nx > tx or ny > ty:
                continue
            sub = cnt(c, k + 1, nx, ny)
            if r < sub:
                cuts.append(c)
                pos, k, ax, ay = c, k + 1, nx, ny
                total = sub
                break
            r -= sub
        else:
            return None
    return cuts


def solve(name, clue, memory):
    try:
        ls = clue.split('\n')
        if len(ls) < 3:
            return None
        pairs = _hdr.findall(ls[0])
        if len(pairs) < 2:
            return None
        grid = ls[1:]
        W = len(grid[0])
        rows = grid[1:-1]
        (X, a), (Y, b) = pairs[0], pairs[1]
        a = int(a)
        b = int(b)
        sx = _sev_table(rows, W, X)
        sy = _sev_table(rows, W, Y)
        cuts = None
        for da, nc in ((0, NCUTS), (-1, NCUTS), (0, 5), (-1, 7), (-1, 5), (-2, NCUTS)):
            cuts = _sample(W, sx, a + da, sy, b + da, nc)
            if cuts:
                break
        if not cuts:
            zero = [0] * W
            cuts = _sample(W, zero, 0, zero, 0, NCUTS)
        if not cuts:
            return None
        out = []
        for row in grid:
            p = 0
            parts = []
            for c in cuts:
                parts.append(row[p:c])
                p = c
            parts.append(row[p:])
            out.append('|'.join(parts))
        return '\n'.join(out)
    except Exception:
        return None


def on_round_end(items, memory):
    memory["last_correct"] = sum(it.get("score", 0) or 0 for it in items)
    memory["last_answered"] = len(items)
