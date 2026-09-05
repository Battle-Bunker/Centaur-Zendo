"""Centaur Zendo strategy — durnel1a."""

from collections import Counter

# ---------------------------------------------------------------- molvic
def solve_molvic(clue):
    lines = clue.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith('|')]
    rows = [list(lines[i]) for i in idx]
    cells = [[(len(r) - 1) // 2, r] for r in rows]
    ncell = [ (len(r) - 1) // 2 for r in rows ]
    maj = []
    for k, r in enumerate(rows):
        c = Counter(r[1 + 2 * j] for j in range(ncell[k]) if r[1 + 2 * j] != ' ')
        maj.append(c.most_common(1)[0][0])
    W = max(ncell)
    for col in range(W):
        p = 1 + 2 * col
        for i in range(len(rows)):
            if p >= len(rows[i]) - 1:
                continue
            for j in range(i + 1, len(rows)):
                if p >= len(rows[j]) - 1:
                    continue
                a, b = rows[i][p], rows[j][p]
                if a == maj[j] and b == maj[i] and a != b:
                    rows[i][p], rows[j][p] = b, a
    out = list(lines)
    for k, i in enumerate(idx):
        out[i] = ''.join(rows[k]).rstrip()
    return '\n'.join(out)


# ---------------------------------------------------------------- fennick
def solve_fennick(clue):
    lines = clue.split('\n')
    body = list(lines)
    tail = []
    while body and (not body[-1] or body[-1][0] in '=0123456789'):
        tail.insert(0, body.pop())
    W = max(len(l) for l in body)
    g = [list(l.ljust(W)) for l in body]
    gr = len(g) - 1
    heights = {}
    for c in range(W):
        ch = g[gr][c]
        if ch not in '. ':
            h = 0
            r = gr
            while r >= 0 and g[r][c] == ch:
                h += 1
                r -= 1
            heights[c] = (ch, h)
    ev = []
    for c in range(W):
        if c in heights or g[gr][c] != '.':
            continue
        L, R = c - 1, c + 1
        if L in heights and R in heights:
            hl, hr = heights[L][1], heights[R][1]
            if hl < hr:
                cand, d = L, 1
            elif hr < hl:
                cand, d = R, -1
            else:
                continue
            opp = cand - d
            if not (0 <= opp < W and opp in heights):
                continue
            ev.append((cand, d, c))
    for cand, d, c in ev:
        ch, h = heights[cand]
        for r in range(gr - h + 1, gr):
            g[r][c] = g[r][cand]
            g[r][cand] = ' '
        cap = gr - h
        if cap >= 0:
            g[cap][c] = '/' if d == 1 else '\\'
            g[cap][cand] = ' '
    return '\n'.join([''.join(r).rstrip() for r in g] + tail)


def _zero(clue):
    """Number in the clue's parameter line (last line, or first for garrow)."""
    last = clue.rsplit('\n', 1)[-1].strip()
    tok = last.split()
    if tok and tok[0].isdigit():
        return int(tok[0])
    return None


VIREL_PROBE = False

def _virel(clue, k):
    lines = clue.split('\n')
    rows = lines[:-1]
    num = lines[-1].strip()
    if k == 0: return '\n'.join(rows)
    if k == 1: return num
    if k == 2: return ""
    if k == 3: return '\n'.join(rows[::-1]) + '\n' + num
    if k == 4: return rows[0]
    if k == 5: return rows[-1]
    if k == 6: return '\n'.join(rows[::-1])
    return None


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1
    memory["_vk"] = 0


def solve(name, clue, memory):
    try:
        if name == "molvic":
            return solve_molvic(clue)
        if name == "fennick":
            return solve_fennick(clue)
        if name == "virel":
            if not VIREL_PROBE:
                return None
            k = memory.get("_vk", 0)
            memory["_vk"] = k + 1
            return _virel(clue, k % 7)
        # unsolved classes: only answer the trivial "nothing happens" instances
        n = _zero(clue)
        if n == 0:
            return clue
        return None
    except Exception:
        return None


def on_round_end(items, memory):
    pass
