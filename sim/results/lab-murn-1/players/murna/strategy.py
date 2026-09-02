"""Centaur Zendo — challenge class `murn`.

Clue format:  "<row>|<n>"  where <row> is a string over {'.', 'o', '#'}.

RULE (reverse-engineered from 1464 scored samples, 0 false pos / 0 false neg):
  The answer is a grid of newline-separated rows, all of length len(row).
  * the LAST row must be the clue row;
  * the grid must contain exactly n '#' in total;
  * for every pair of vertically adjacent rows (a above, b below) and every
    position i, letting d = number of '.' among b[i-1], b[i], b[i+1] (cells
    off the ends count as '.'):
        a[i] == '#'  requires d == 1
        a[i] == 'o'  requires d == 2
        a[i] == '.'  is always allowed
  So we build rows upward from the clue, spending the '#' budget on cells whose
  window below holds exactly one dot, and using free 'o's to keep the row dense
  enough to carry more '#' on the level above.
"""

_MASKS = (lambda i: True,
          lambda i: i % 3 != 2,
          lambda i: i % 3 != 0,
          lambda i: i % 3 != 1,
          lambda i: i % 2 == 0,
          lambda i: i % 4 != 3)


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def _chain(row, need, L, mask):
    cur = row
    above = []
    for _ in range(30):
        cells = []
        placed = 0
        nz = 0
        for i in range(L):
            d = 0
            if i == 0 or cur[i - 1] == '.': d += 1
            if cur[i] == '.': d += 1
            if i == L - 1 or cur[i + 1] == '.': d += 1
            if d == 1 and placed < need and mask(i):
                cells.append('#'); placed += 1; nz += 1
            elif d == 2 and mask(i):
                cells.append('o'); nz += 1
            else:
                cells.append('.')
        if nz == 0:
            return None
        r = "".join(cells)
        above.append(r)
        need -= placed
        if need == 0:
            return "\n".join(reversed(above)) + "\n" + row
        cur = r
    return None


def solve(name, clue, memory):
    try:
        row, sep, ns = clue.rpartition("|")
        if not sep:
            return None
        n = int(ns)
        L = len(row)
        need = n - row.count("#")
        if need < 0:
            return None
        if need == 0:
            return row
        for m in _MASKS:
            r = _chain(row, need, L, m)
            if r is not None:
                return r
        return None
    except Exception:
        return None


def on_round_end(items, memory):
    pass
