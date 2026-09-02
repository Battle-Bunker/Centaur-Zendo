import json, os, collections
import gen, pool

_DIR = os.path.dirname(os.path.abspath(__file__))
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

KNOWN = {}        # n -> (template string, its dominant letter)
POOL = []         # list of (bricks, template using marks a..g)
BYSIZE = {}       # n -> list of pool indices with a plausible size
TT = {}           # clue letter -> translation table for marks
SWAP = {}         # (dom, letter) -> table
_state = {'i': 0}


def _dom(s):
    return collections.Counter(c for c in s if c.isalpha()).most_common(1)[0][0]


def on_round_start(memory):
    B = json.load(open(os.path.join(_DIR, 'bases.json')))
    KNOWN.clear()
    KNOWN[0] = (gen.sep_bricks(1, 'B'), 'B')
    KNOWN[2] = (B['J2'], 'J')
    KNOWN[3] = (B['M3'], 'M')
    KNOWN[4] = (gen.holed2(4, 'B'), 'B')
    KNOWN[5] = (B['H5'], 'H')
    for st in memory.get('winners', {}).items():
        pass
    # translation tables: mark 'a' -> clue letter, 'b'..'g' -> distinct others
    for L in ALPHA:
        others = [c for c in "BCDEFGHIJKLMNOPQRSTUVWXYZ" if c != L][:6]
        m = {'a': L}
        for k, c in zip('bcdefg', others):
            m[k] = c
        TT[L] = str.maketrans(m)
    POOL.clear()
    seed = 0
    while len(POOL) < 900 and seed < 6000:
        g = pool.build(seed); seed += 1
        if g:
            POOL.append((sum(1 for c in g if c.isalpha()) // 6, g))
    BYSIZE.clear()
    for n in range(13):
        lo, hi = max(1, 13*n - 22), 13*n + 22
        idx = [i for i, (b, _) in enumerate(POOL) if lo <= b <= hi]
        BYSIZE[n] = idx or list(range(len(POOL)))
    _state['i'] = 0
    memory.setdefault('winners', {})


def _remap(base, dom, L):
    if dom == L:
        return base
    key = (dom, L)
    t = SWAP.get(key)
    if t is None:
        t = str.maketrans({dom: L, L: dom})
        SWAP[key] = t
    return base.translate(t)


def solve(name, clue, memory):
    try:
        L = clue[0]
        n = int(clue[1:])
        w = memory.get('winners', {}).get(str(n))
        if w:
            return _remap(w[0], w[1], L)
        k = KNOWN.get(n)
        if k:
            return _remap(k[0], k[1], L)
        i = _state['i']
        _state['i'] = i + 1
        if i % 2 == 0:
            lst = BYSIZE[n]
            g = POOL[lst[(i // 2) % len(lst)]][1]
        else:
            g = POOL[(i * 7 + n * 131) % len(POOL)][1]
        return g.translate(TT[L])
    except Exception:
        return None


def on_round_end(items, memory):
    win = memory.setdefault('winners', {})
    for it in items:
        if it.get('score') == 1:
            try:
                n = str(int(it['clue'][1:]))
            except Exception:
                continue
            if n not in win:
                sol = it['solution']
                win[n] = [sol, _dom(sol)]
