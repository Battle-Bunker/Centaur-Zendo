"""LegoZendo solver.

THE RULE (recovered from 3 demos + 1221 scored answers; 0 mismatches):
  A clue is <COLOUR LETTER><N>, e.g. "Q9".  An answer is an ASCII picture of
  Lego bricks: every piece is a 3-wide x 2-tall or 2-wide x 3-tall block of one
  letter, drawn on a background of any spare character (we use ':').
  It scores 1 iff, for the clue's colour, the number of brick PAIRS that share
  an orientation and meet along exactly one cell edge -- equivalently, are
  offset by (+/-2, +/-2), a "staircase" join -- is exactly N.
  Grid size, other colours and every other kind of join are free.

We therefore answer with N well-separated staircase pairs of that colour (plus
two lone filler bricks of another colour), in the smallest grid that fits.
All answers are precomputed in on_round_start, so solve() is a dict lookup.
"""

BG = ':'
MAXN = 30
TABLE = {}


def _layout(n):
    best = None
    for rows in range(1, n + 1):
        cols = -(-n // rows)
        w = cols * 6 - 1
        h = max(rows * 5 - 1, 6)
        if best is None or (w + 5) * h < best[0]:
            best = ((w + 5) * h, rows, cols, w, h)
    return best[1], best[2], best[3], best[4]


def _make(ch, n):
    other = 'A' if ch != 'A' else 'B'
    if n <= 0:
        rows_n, cols_n, w, h = 1, 1, 3, 6
    else:
        rows_n, cols_n, w, h = _layout(n)
    W = w + 4
    g = [[BG] * W for _ in range(h)]

    def put(r, c, wd, ht, x):
        for i in range(ht):
            row = g[r + i]
            for j in range(wd):
                row[c + j] = x

    if n <= 0:
        put(0, 0, 3, 2, ch)                    # a lone brick: no joins at all
    else:
        k = 0
        for b in range(rows_n):
            for c in range(cols_n):
                if k >= n:
                    break
                r0, c0 = b * 5, c * 6
                put(r0, c0, 3, 2, ch)          # each staircase pair scores 1
                put(r0 + 2, c0 + 2, 3, 2, ch)
                k += 1
    put(0, w + 1, 3, 2, other)
    put(4, w + 1, 3, 2, other)
    return "\n".join("".join(r) for r in g)


def on_round_start(memory):
    global TABLE
    try:
        if not TABLE:
            TABLE = {(ch, n): _make(ch, n)
                     for ch in map(chr, range(65, 91))
                     for n in range(MAXN + 1)}
    except Exception:
        TABLE = {}
    try:
        memory["rounds_played"] = memory.get("rounds_played", 0) + 1
    except Exception:
        pass


def solve(name, clue, memory):
    try:
        return TABLE[(clue[0], int(clue[1:]))]
    except Exception:
        return None


def on_round_end(items, memory):
    pass
