"""LegoZendo2 solver.

Clue format:  <colourA><colourB><N>   e.g. "HW1", "PY0", "CZ11"  (N = 0..12)

The answer is an ASCII grid ('_' = empty) tiled with 6-cell LEGO pieces
(2x3 / 3x2 rectangles).  Empirically the server counts the number of
*staggered* left-right contacts between an A piece and a B piece: an A piece
whose right edge touches a B piece that sits one row lower (contact length 2).
Perfectly aligned side-by-side pieces (contact 3) and vertically stacked
pieces do NOT count.  Score = 1 iff that count equals N.

So: emit N staggered A|B units in a 12x32 grid, well separated.
For N == 0 emit a single A piece and a single B piece that do not touch.
"""

ROWS, COLS = 12, 32

# Each unit occupies rows r..r+3 and cols c..c+3.
SLOTS = [(r, c) for r in (0, 4, 8) for c in (0, 5, 10, 15, 20, 25)]

_ANSWERS = {}


def _blank():
    return [['_'] * COLS for _ in range(ROWS)]


def _put(g, r, c, h, w, ch):
    for i in range(h):
        row = g[r + i]
        for j in range(w):
            row[c + j] = ch


def build(a, b, n):
    """Minimal bounding grid: 4 rows, 5N-1 cols (N=0 -> 3x6)."""
    if n <= 0:
        rows = [[a, a, '_', '_', b, b] for _ in range(3)]
        return "\n".join("".join(r) for r in rows)
    n = min(n, 12)
    cols = 5 * n - 1
    g = [['_'] * cols for _ in range(4)]
    for k in range(n):
        c = 5 * k
        for i in range(3):
            g[i][c] = a; g[i][c + 1] = a
            g[i + 1][c + 2] = b; g[i + 1][c + 3] = b
    return "\n".join("".join(r) for r in g)


def on_round_start(memory):
    """Free time: precompute every possible answer so solve() is a dict lookup."""
    memory.clear()
    if _ANSWERS:
        return
    letters = [chr(o) for o in range(65, 91)]
    for a in letters:
        for b in letters:
            for n in range(13):
                _ANSWERS[a + b + str(n)] = build(a, b, n)


def solve(name, clue, memory):
    try:
        r = _ANSWERS.get(clue)
        if r is not None:
            return r
        # fallback: unseen shape of clue
        c = clue.strip().upper()
        if len(c) >= 3 and c[0].isalpha() and c[1].isalpha() and c[2:].isdigit():
            n = int(c[2:])
            if n > len(SLOTS):
                return None
            r = build(c[0], c[1], n)
            _ANSWERS[clue] = r
            return r
        return None
    except Exception:
        return None


def on_round_end(items, memory):
    pass
