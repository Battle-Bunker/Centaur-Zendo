"""Round 3 brain: rule-family solvers via predicate-intersection + picture probes."""
import json, os, random, collections, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path: sys.path.insert(0, _HERE)
from zpools import (tresk_preds, borsel_preds, dornic_preds, tavrik_preds,
                    wisbek_preds, RANKS, RV)

RND = random.Random(20260905)
S = {}
DECK = [(r, s) for r in RANKS for s in 'SHDC']
FAMILY = ('tresk', 'borsel', 'dornic', 'tavrik', 'wisbek')
PROBE = True          # round-3 exploration on/off


def _safe(p, x):
    try: return bool(p(x))
    except Exception: return False


def _mask(P, order, x):
    m = 0
    for i, n in enumerate(order):
        if _safe(P[n], x): m |= 1 << i
    return m


def _build(key, P, universe):
    order = sorted(P)
    masks = [_mask(P, order, x) for x in universe]
    base = [0] * len(order)
    for m in masks:
        for i in range(len(order)):
            if m >> i & 1: base[i] += 1
    n = float(len(universe))
    S[key] = {'P': P, 'order': order, 'univ': universe, 'masks': masks,
              'base': [b / n for b in base],
              'index': {x: i for i, x in enumerate(universe)}}


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1
    memory["_v"] = {}
    S['count'] = collections.Counter()

    # wisbek: exact universe
    _build('wisbek', wisbek_preds(), [(h, m) for h in range(1, 13) for m in range(60)])
    # borsel: exact universe of rows length 3..5
    bu = []
    for L in (3, 4, 5):
        stack = [()]
        for _ in range(L):
            stack = [t + (v,) for t in stack for v in range(1, 7)]
        bu.extend(stack)
    _build('borsel', borsel_preds(), bu)
    # tavrik: words 4..7
    words = [w for w in json.load(open(os.path.join(_HERE, 'words.json')))
             if 4 <= len(w) <= 7]
    RND.shuffle(words)
    _build('tavrik', tavrik_preds(), words)
    # tresk: sampled strings
    seen = set()
    tu = []
    for _ in range(26000):
        L = RND.randint(6, 10)
        s = ''.join(RND.choice('BGR') for _ in range(L))
        if s not in seen:
            seen.add(s); tu.append(s)
    _build('tresk', tresk_preds(), tu)
    # dornic: no precomputed universe (too big)
    Pd = dornic_preds()
    du = [tuple(sorted(RND.sample(DECK, RND.randint(4, 6)), key=lambda c: (RV[c[0]], c[1])))
          for _ in range(1200)]
    orderd = sorted(Pd)
    based = []
    for n in orderd:
        p = Pd[n]
        based.append(sum(1 for x in du if _safe(p, x)) / float(len(du)))
    S['dornic'] = {'P': Pd, 'order': orderd, 'base': based,
                   'bidx': dict((n, based[i]) for i, n in enumerate(orderd))}


# ---------------- parse / format ----------------
def _p_dornic(l): return tuple((c[:-1], c[-1]) for c in l.split())
def _f_dornic(x): return ' '.join(r + s for r, s in x)
PARSE = {'tresk': lambda l: l,
         'borsel': lambda l: tuple(int(v) for v in l.split()),
         'dornic': _p_dornic,
         'tavrik': lambda l: l,
         'wisbek': lambda l: (int(l.split(':')[0]), int(l.split(':')[1]))}
FMT = {'tresk': lambda x: x,
       'borsel': lambda x: ' '.join(str(v) for v in x),
       'dornic': _f_dornic,
       'tavrik': lambda x: x,
       'wisbek': lambda x: '%d:%02d' % x}


def _consistent_mask(st, d):
    P, order, idx = st['P'], st['order'], st['index']
    m = None
    for x in d:
        i = idx.get(x)
        mm = st['masks'][i] if i is not None else _mask(P, order, x)
        m = mm if m is None else (m & mm)
    return m if m is not None else 0


def _mutants(key, d, n):
    """Small edits of the clue lines - fast, and usually already in the universe."""
    out = []
    if key == 'borsel':
        for _ in range(n):
            r = list(RND.choice(d))
            for _ in range(RND.randint(1, 2)):
                r[RND.randrange(len(r))] = RND.randint(1, 6)
            out.append(tuple(r))
    elif key == 'tresk':
        for _ in range(n):
            r = list(RND.choice(d))
            k = RND.random()
            if k < 0.75:
                for _ in range(RND.randint(1, 2)):
                    r[RND.randrange(len(r))] = RND.choice('BGR')
            else:
                RND.shuffle(r)
            out.append(''.join(r))
    return out


def _solve_masked(key, clue, extra=None, collect=1, rank=None, use_mut=True, cap=4000):
    st = S[key]
    d = [PARSE[key](l) for l in clue.split('\n')]
    C = _consistent_mask(st, d)
    dset = set(d)
    univ, masks, idx = st['univ'], st['masks'], st['index']
    hits = []
    if use_mut:
        for x in _mutants(key, d, 200):
            i = idx.get(x)
            if i is None or x in dset: continue
            if masks[i] & C != C: continue
            if extra is not None and not extra(x, d): continue
            hits.append(x)
            if len(hits) >= collect: break
    n = len(univ)
    start = RND.randrange(n)
    if len(hits) < collect:
        for j in range(min(n, cap)):
            i = start + j
            if i >= n: i -= n
            if masks[i] & C == C:
                x = univ[i]
                if x in dset: continue
                if extra is not None and not extra(x, d): continue
                hits.append(x)
                if len(hits) >= collect: break
    if hits:
        if rank is not None and len(hits) > 1:
            hits.sort(key=lambda x: rank(x, d), reverse=True)
        return FMT[key](hits[0])
    bits = [i for i in range(len(st['order'])) if C >> i & 1]
    bits.sort(key=lambda i: st['base'][i])
    for keep in (max(1, len(bits) * 2 // 3), max(1, len(bits) // 3), 1, 0):
        M = 0
        for i in bits[:keep]: M |= 1 << i
        for j in range(n):
            i = start + j
            if i >= n: i -= n
            if masks[i] & M == M:
                x = univ[i]
                if x in dset: continue
                if extra is not None and not extra(x, d): continue
                return FMT[key](x)
    return FMT[key](RND.choice(univ))


# ---------------- dornic (generated candidates) ----------------
def _dornic_cands(d, disjoint, n=180):
    used = set(x for h in d for x in h)
    pool = [c for c in DECK if c not in used] if disjoint else DECK
    byrank = collections.defaultdict(list)
    for c in pool: byrank[c[0]].append(c)
    out = []
    sizes = [len(h) for h in d]
    for _ in range(n // 2):
        base = list(RND.choice(d))
        h = []
        ok = True
        for c in base:
            alt = byrank.get(c[0])
            if not alt: ok = False; break
            h.append(RND.choice(alt))
        if ok and len(set(h)) == len(h):
            out.append(tuple(sorted(set(h), key=lambda c: (RV[c[0]], c[1]))))
    for _ in range(n // 2):
        k = RND.choice(sizes)
        if len(pool) >= k:
            out.append(tuple(sorted(RND.sample(pool, k), key=lambda c: (RV[c[0]], c[1]))))
    return out


def _solve_dornic(clue, disjoint=True):
    st = S['dornic']; P, order, base = st['P'], st['order'], st['base']
    d = [_p_dornic(l) for l in clue.split('\n')]
    C = [n for n in order if all(_safe(P[n], x) for x in d)]
    bidx = st['bidx']
    C.sort(key=lambda n: bidx[n])
    preds = [P[n] for n in C]
    cands = _dornic_cands(d, disjoint)
    dset = set(d)
    for x in cands:
        if x in dset: continue
        good = True
        for p in preds:
            if not _safe(p, x): good = False; break
        if good: return _f_dornic(x)
    for drop in range(1, len(preds)):
        sub = preds[:len(preds) - drop]
        for x in cands:
            if x in dset: continue
            if all(_safe(p, x) for p in sub): return _f_dornic(x)
    return _f_dornic(cands[0]) if cands else ''


# ---------------- pictures ----------------
def _basten(clue, v):
    L = clue.split('\n')
    N = int(L[-1]); pic = [list(r) for r in L[:-1]]
    H = len(pic); W = len(pic[0])
    rows = list(range(1, H - 1))
    def place(count, mode):
        g = [r[:] for r in pic]
        spots = [(r, c) for r in rows for c in range(W - 2)]
        if mode == 'top': spots.sort(key=lambda rc: (rc[0], rc[1]))
        elif mode == 'spread': RND.shuffle(spots)
        else: RND.shuffle(spots)
        placed = 0
        for (r, c) in spots:
            if placed >= count: break
            if any(g[r][c + i] != '.' for i in range(3)): continue
            if c > 0 and g[r][c - 1] != '.': continue
            if c + 3 < W and g[r][c + 3] != '.': continue
            f = '><>' if (placed % 2 == 0) else '<><'
            for i in range(3): g[r][c + i] = f[i]
            placed += 1
        return '\n'.join(''.join(x) for x in g)
    if v == 0: return place(N, 'spread')
    if v == 1: return place(2 * N, 'spread')
    if v == 2: return place(N, 'top')
    if v == 3: return place(N + 1, 'spread')
    if v == 4: return place(2 * N, 'top')
    return place(N - 1, 'spread')


def _kelmar(clue, v):
    L = clue.split('\n')
    N = int(L[-1]); ground = L[-2]; rows = L[:-2]
    W = len(ground)
    stars = [i for i, ch in enumerate(ground) if ch == '*']
    ys = [i for i, ch in enumerate(ground) if ch == 'Y']
    def render(cols):
        s = ''.join('|' if i in cols else '.' for i in range(W))
        return '\n'.join([s] * len(rows) + [ground])
    if v == 0:
        s = set()
        for x in stars:
            for j in range(x - 2, x + 4):
                if 0 <= j < W: s.add(j)
        return render(s)
    if v == 1:
        s = set()
        for y in ys:
            for j in range(y - 1, y + 5):
                if 0 <= j < W: s.add(j)
        return render(s)
    if v == 2:
        return render(set(range(W)) - set(range(0, W, 3)))
    return render(set(i for i in range(W) if ground[i] != '_'))


def _ed_le1(a, b):
    if abs(len(a) - len(b)) > 1: return False
    if len(a) == len(b):
        return sum(1 for x, y in zip(a, b) if x != y) <= 1
    if len(a) > len(b): a, b = b, a
    for i in range(len(b)):
        if b[:i] + b[i + 1:] == a: return True
    return False


def _nov_tavrik(w, d): return not any(_ed_le1(w, x) for x in d)
def _nov_borsel(r, d):
    m = tuple(sorted(r))
    return all(m != tuple(sorted(x)) for x in d)
def _nov_wisbek(t, d): return all(t[0] != x[0] for x in d)
def _rank_borsel(r, d):
    return min(sum(1 for a, b in zip(r, x) if a != b) for x in d)


def _basten4(clue, v):
    L = clue.split('\n')
    N = int(L[-1]); pic = [list(r) for r in L[:-1]]
    H = len(pic); W = len(pic[0])
    rows = list(range(1, H - 1))
    count = 2 * N
    g = [r[:] for r in pic]
    rr = rows if v != 1 else (rows[1:] or rows)
    spots = [(r, c) for r in rr for c in range(W - 2)]
    if v == 2:
        spots.sort(key=lambda rc: (-rc[0], rc[1]))
    else:
        RND.shuffle(spots)
    placed = 0
    for (r, c) in spots:
        if placed >= count: break
        if g[r][c] != '.' or g[r][c + 1] != '.' or g[r][c + 2] != '.': continue
        if v == 3:
            if c > 0 and g[r][c - 1] in '<>': continue
            if c + 3 < W and g[r][c + 3] in '<>': continue
        f = '><>' if (v != 4 or placed % 2 == 0) else '<><'
        g[r][c] = f[0]; g[r][c + 1] = f[1]; g[r][c + 2] = f[2]
        placed += 1
    return '\n'.join(''.join(x) for x in g)


def solve(name, clue, memory):
    try:
        c = S['count'][name]; S['count'][name] = c + 1
        idx = memory.get('_index')
        if name == 'wisbek':
            return _solve_masked('wisbek', clue, extra=_nov_wisbek, use_mut=False)
        if name == 'tavrik':
            return _solve_masked('tavrik', clue, extra=_nov_tavrik, use_mut=False)
        if name == 'borsel':
            return _solve_masked('borsel', clue, extra=_nov_borsel, collect=4,
                                 rank=_rank_borsel, use_mut=True, cap=3000)
        if name == 'tresk':
            lens = set(len(l) for l in clue.split('\n'))
            return _solve_masked('tresk', clue,
                                 extra=lambda x, d: len(x) not in lens, cap=8000)
        if name == 'dornic':
            return _solve_dornic(clue, disjoint=True)
        if name == 'basten':
            v = c % 5
            memory['_v'][str(idx)] = v
            return _basten4(clue, v)
        return None
    except Exception:
        return None


def on_round_end(items, memory):
    vm = memory.get('_v', {})
    log = [{'name': it.get('name'), 'v': vm.get(str(it.get('index')), 0),
            'clue': it.get('clue'), 'ans': it.get('solution'),
            'score': it.get('score')} for it in items]
    memory['examples'] = {}
    res = collections.defaultdict(lambda: [0, 0])
    for it in log:
        res[(it['name'], it['v'])][0] += it['score']; res[(it['name'], it['v'])][1] += 1
    memory['variant_results'] = {'%s|%s' % k: v for k, v in sorted(res.items())}
    try:
        with open(os.path.join(_HERE, 'work', 'r%d_items.json' % memory.get('rounds_played', 0)), 'w') as f:
            json.dump(log, f)
    except Exception:
        pass
