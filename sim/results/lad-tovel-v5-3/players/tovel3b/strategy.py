"""FINAL strategy.

fennick : solved exactly (trees fall into single-column gaps; the shorter of the
          two neighbours falls, ties nobody, a tree with gaps on both sides never
          falls).  100% in training.
basten  : add `<><` fish to the bottom water row.  Number of fish = (max fish that
          fit with one space between them) + num - 4.   ~70% in training.
kelmar  : grass/gap stripes, 3 on / 3 off, phase anchored on the right edge.
          ~60% in training (num>=2).
others  : skipped (instant, keeps the round fast and helps the precision tiebreak).
"""

CACHE = {}


def on_round_start(memory):
    CACHE.clear()


# ------------------------------------------------------------------ fennick
def _fennick(clue):
    L = clue.split('\n')
    eq = -1
    for i, l in enumerate(L):
        if l and l[0] == '=' and set(l) == {'='}:
            eq = i; break
    if eq < 0:
        return None
    W = len(L[eq])
    g = [list(l.ljust(W)) for l in L[:eq]]
    ground = len(g) - 1
    base = g[ground]
    H = [0] * W
    for c in range(W):
        ch = base[c]
        if ch != '.' and ch != ' ':
            h = 1; r = ground - 1
            while r >= 0 and g[r][c] == ch:
                h += 1; r -= 1
            H[c] = h
    falls = []
    for c in range(W):
        if H[c]:
            continue
        if (c > 0 and H[c-1] == 0) or (c + 1 < W and H[c+1] == 0):
            continue
        lh = H[c-1] if c else 0
        rh = H[c+1] if c + 1 < W else 0
        if lh and rh:
            if lh < rh: t, d = c - 1, 1
            elif rh < lh: t, d = c + 1, -1
            else: continue
        elif lh: t, d = c - 1, 1
        elif rh: t, d = c + 1, -1
        else: continue
        if (t > 0 and H[t-1] == 0) and (t + 1 < W and H[t+1] == 0):
            continue
        falls.append((t, d))
    for col, d in falls:
        ch = base[col]; h = H[col]; nc = col + d
        for r in range(ground - 1, ground - h, -1):
            g[r][col] = ' '
            if 0 <= nc < W: g[r][nc] = ch
        cap = ground - h
        if cap >= 0:
            g[cap][col] = ' '
            if 0 <= nc < W: g[cap][nc] = '/' if d > 0 else '\\'
    out = [''.join(r).rstrip() for r in g]
    out.extend(L[eq:])
    return '\n'.join(out)


# ------------------------------------------------------------------ basten
def _basten(clue):
    L = clue.split('\n')
    num = int(L[-1].strip())
    pic = L[:-1]
    ground = len(pic) - 1
    row = list(pic[ground - 1])
    W = len(row)
    slots = []; c = 0
    while c + 3 <= W:
        if row[c] == '.' and row[c+1] == '.' and row[c+2] == '.':
            slots.append(c); c += 4
        else:
            c += 1
    want = len(slots) + num - 4
    if want > len(slots):                     # need tighter packing
        slots = []; c = 0
        while c + 3 <= W:
            if row[c] == '.' and row[c+1] == '.' and row[c+2] == '.':
                slots.append(c); c += 3
            else:
                c += 1
    if want < 0: want = 0
    for c in slots[:want]:
        row[c] = '<'; row[c+1] = '>'; row[c+2] = '<'
    out = list(pic)
    out[ground - 1] = ''.join(row)
    return '\n'.join(out)


# ------------------------------------------------------------------ kelmar
def _kelmar(clue):
    L = clue.split('\n')
    num = int(L[-1].strip())
    base = L[-2]
    W = len(base)
    h = 2 if num <= 1 else 3
    per = 2 * h
    q = (W + 1) % per
    line = ''.join("'" if (i - q) % per < h else '.' for i in range(W))
    return '\n'.join([line] * (len(L) - 2) + [base])


SOLVERS = {'fennick': _fennick, 'basten': _basten, 'kelmar': _kelmar}


def solve(name, clue, memory):
    f = SOLVERS.get(name)
    if f is None:
        return None
    hit = CACHE.get(clue)
    if hit is not None:
        return hit
    try:
        a = f(clue)
    except Exception:
        return None
    if len(CACHE) < 4000:
        CACHE[clue] = a
    return a


def on_round_end(items, memory):
    pass
