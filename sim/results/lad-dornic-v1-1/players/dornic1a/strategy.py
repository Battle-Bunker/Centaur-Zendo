"""Round 3: version space + mutation experiments."""
import json, os, random, itertools, re
import vslib as V

DIR = os.path.dirname(os.path.abspath(__file__))
G = {}
RULE = ('tavrik', 'wisbek', 'borsel', 'tresk', 'dornic')
KIND = {'tavrik': 'word', 'wisbek': 'time', 'borsel': 'dice',
        'tresk': 'col', 'dornic': 'cards'}
PARSE = {'tavrik': lambda l: l.strip(),
         'wisbek': lambda l: tuple(int(x) for x in l.split(':')),
         'borsel': lambda l: [int(x) for x in l.split()],
         'tresk': lambda l: l.strip(),
         'dornic': V.parse_cards}
RSTR = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}


def _card_str(cs):
    return ' '.join((RSTR.get(r, str(r)) + s) for r, s in cs)


def _canon(cs):
    return sorted(cs, key=lambda c: (c[0], 'HDCS'.index(c[1])))


def _uniq(seq):
    out = []; seen = set()
    for x in seq:
        if x not in seen: seen.add(x); out.append(x)
    return out


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1
    memory["counts"] = {}
    if G: return
    clues = json.load(open(os.path.join(DIR, 'clues.json')))
    sel = json.load(open(os.path.join(DIR, 'sel.json')))
    P = {n: V.preds(KIND[n]) for n in RULE}
    G['P'] = P
    G['sel'] = {k: sum(1 << i for i in v) for k, v in sel.items()}
    corpus = {n: _uniq([l.strip() for c in clues[n] for l in c.split('\n') if l.strip()])
              for n in RULE}
    G['corpus'] = corpus
    syn = {}
    syn['tavrik'] = {0: []}
    syn['wisbek'] = {0: [f"{h}:{m:02d}" for h in range(1, 13) for m in range(60)]}
    syn['borsel'] = {L: [' '.join(str(x) for x in p)
                         for p in itertools.product(range(1, 7), repeat=L)]
                     for L in (3, 4, 5, 6)}
    syn['tresk'] = {0: [''.join(p) for L in (6, 7, 8)
                        for p in itertools.product('GRB', repeat=L)]}
    syn['dornic'] = {0: []}
    uni = {}
    for n in RULE:
        groups = {}
        for k, items in syn[n].items():
            if n == 'borsel':
                corp = [c for c in corpus[n] if len(c.split()) == k]
            else:
                corp = list(corpus[n])
            seen = set(corp)
            lst = corp + [x for x in items if x not in seen]
            ncorp = len(corp)
            objs = []
            for t in lst:
                try: objs.append((t, PARSE[n](t)))
                except Exception: pass
            groups[k] = (objs, ncorp)
        uni[n] = groups
    G['uni'] = uni
    G['masks'] = {n: {k: [V.mask_of(o, P[n]) for _, o in v[0]] for k, v in gr.items()}
                  for n, gr in uni.items()}
    G['rnd'] = random.Random(11)


def _mutations(name, lines, objs):
    out = []
    if name == 'tresk':
        for s in objs:
            r = s[::-1]
            if r != s: out.append((r, r))
        for s in objs:
            for i in range(len(s) - 1):
                if s[i] != s[i + 1]:
                    t = s[:i] + s[i + 1] + s[i] + s[i + 2:]
                    if t != s: out.append((t, t))
                    break
    elif name == 'borsel':
        for a in objs:
            r = a[::-1]
            if r != a: out.append((' '.join(map(str, r)), r))
        for a in objs:
            for i in range(len(a) - 1):
                if a[i] != a[i + 1]:
                    t = a[:i] + [a[i + 1], a[i]] + a[i + 2:]
                    out.append((' '.join(map(str, t)), t))
                    break
    elif name == 'dornic':
        m = {'H': 'D', 'D': 'H', 'C': 'S', 'S': 'C'}
        for cs in objs:
            t = _canon([(r, m[s]) for r, s in cs])
            out.append((_card_str(t), t))
        m2 = {'H': 'C', 'C': 'H', 'D': 'S', 'S': 'D'}
        for cs in objs:
            t = _canon([(r, m2[s]) for r, s in cs])
            out.append((_card_str(t), t))
    return out


def _vs(name, lines, curated, mutfirst, skip=0, corpus_first=True):
    P = G['P'][name]; parse = PARSE[name]
    objs = [parse(l) for l in lines]
    M = V.mask_of(objs[0], P)
    for o in objs[1:]:
        M &= V.mask_of(o, P)
    if curated: M &= G['sel'][name]
    given = set(l.strip() for l in lines)
    if mutfirst:
        for txt, obj in _mutations(name, lines, objs):
            if txt in given: continue
            if (V.mask_of(obj, P) & M) == M:
                return txt
    key = len(objs[0]) if name == 'borsel' else 0
    gr = G['uni'][name]
    if key not in gr: return None
    uni, ncorp = gr[key]; ms = G['masks'][name][key]
    N = len(uni)
    if corpus_first:
        order = range(N)
    else:
        order = itertools.chain(range(ncorp, N), range(ncorp))
    n = 0
    for i in order:
        if (ms[i] & M) == M and uni[i][0] not in given:
            if n >= skip: return uni[i][0]
            n += 1
    return None


def _mut_only(name, lines):
    objs = [PARSE[name](l) for l in lines]
    given = set(l.strip() for l in lines)
    for txt, obj in _mutations(name, lines, objs):
        if txt not in given: return txt
    return None


# ------------------------- basten -----------------------------------------
def _fish_slots(g, W, rows):
    s = []
    for r in rows:
        for c in range(W - 2):
            if g[r][c] == '.' and g[r][c + 1] == '.' and g[r][c + 2] == '.':
                s.append((r, c))
    return s


def _basten(clue, v):
    L = clue.split('\n')
    num = int(L[-1].strip()); g = [list(r) for r in L[:-1]]
    W = len(g[0]); water = list(range(1, len(g) - 1))
    def put(r, c, i):
        f = '><>' if i % 2 == 0 else '<><'
        for k in range(3): g[r][c + k] = f[k]
    placed = 0
    if v == 0:                                # bottom row, greedy left
        for r in reversed(water):
            for c in range(W - 2):
                if placed >= num: break
                if g[r][c] == '.' and g[r][c+1] == '.' and g[r][c+2] == '.':
                    put(r, c, placed); placed += 1
            if placed >= num: break
    elif v == 1:                              # spaced out: one dot between fish
        for r in reversed(water):
            c = 0
            while c < W - 2 and placed < num:
                if g[r][c] == '.' and g[r][c+1] == '.' and g[r][c+2] == '.' and \
                   (c == 0 or g[r][c-1] == '.'):
                    put(r, c, placed); placed += 1; c += 4
                else:
                    c += 1
            if placed >= num: break
    elif v == 2:                              # one fish per gap, widest first
        r = water[-1]
        gaps = []
        c = 0
        while c < W:
            if g[r][c] == '.':
                s = c
                while c < W and g[r][c] == '.': c += 1
                gaps.append((c - s, s, c - 1))
            else: c += 1
        gaps.sort(key=lambda t: -t[0])
        for wdt, s, e in gaps:
            if placed >= num or wdt < 3: break
            put(r, s + (wdt - 3) // 2, placed); placed += 1
    elif v == 3:                              # spread across rows, bottom up
        rows = list(reversed(water))
        i = 0
        while placed < num and i < 200:
            r = rows[i % len(rows)]
            for c in range(W - 2):
                if g[r][c] == '.' and g[r][c+1] == '.' and g[r][c+2] == '.':
                    put(r, c, placed); placed += 1; break
            i += 1
    elif v == 5:                              # num fish, each touching a plant
        plants = [(r, c) for r in water for c in range(W) if g[r][c] == '|']
        cand = []
        for r in reversed(water):
            for c in range(W - 2):
                if g[r][c] == '.' and g[r][c+1] == '.' and g[r][c+2] == '.':
                    if (c > 0 and g[r][c-1] == '|') or (c + 3 < W and g[r][c+3] == '|'):
                        cand.append((r, c))
        for (r, c) in cand:
            if placed >= num: break
            if g[r][c] == '.' and g[r][c+1] == '.' and g[r][c+2] == '.':
                put(r, c, placed); placed += 1
        for r in reversed(water):
            for c in range(W - 2):
                if placed >= num: break
                if g[r][c] == '.' and g[r][c+1] == '.' and g[r][c+2] == '.':
                    put(r, c, placed); placed += 1
    elif v == 6:                              # num fish, all facing right
        for r in reversed(water):
            for c in range(W - 2):
                if placed >= num: break
                if g[r][c] == '.' and g[r][c+1] == '.' and g[r][c+2] == '.':
                    put(r, c, 0); placed += 1
            if placed >= num: break
    else:                                     # v==4 top down greedy
        for r in water:
            for c in range(W - 2):
                if placed >= num: break
                if g[r][c] == '.' and g[r][c+1] == '.' and g[r][c+2] == '.':
                    put(r, c, placed); placed += 1
            if placed >= num: break
    return '\n'.join(''.join(r) for r in g)


# ------------------------- kelmar -----------------------------------------
def _kelmar(clue, v, c=0):
    L = clue.split('\n')
    num = int(L[-1].strip()); base = L[-2]; rows = L[:-2]
    W = len(base)
    gl = {1: "'", 2: "|"}.get(num) or K3[c % len(K3)]
    marks = [(i, ch) for i, ch in enumerate(base) if ch in '*Y']
    pos = [i for i, _ in marks]
    fill = set()
    if v == 0:                       # one band per run of same-type markers
        runs = []
        for i, ch in marks:
            if runs and runs[-1][0] == ch: runs[-1][1].append(i)
            else: runs.append((ch, [i]))
        for ch, ps in runs:
            a = ps[0]
            fill.update(range(max(0, a - 1), min(W, a + 2)))
    elif v == 1:                     # num evenly spaced bands of 3
        k = max(1, num)
        for j in range(k):
            a = int((j + 0.5) * W / k) - 1
            fill.update(range(max(0, a), min(W, a + 3)))
    elif v == 2:                     # interior of every gap >= 3
        for a, b in zip(pos, pos[1:]):
            if b - a >= 4: fill.update(range(a + 1, b))
    else:                            # midpoints between consecutive markers
        for a, b in zip(pos, pos[1:]):
            m = (a + b) // 2
            fill.update(range(max(0, m - 1), min(W, m + 2)))
    row = ''.join(gl if i in fill else '.' for i in range(W))
    return '\n'.join([row] * len(rows) + [base])


BEST = {'tavrik': 'VC', 'wisbek': 'CVC', 'tresk': 'CVC',
        'borsel': 'VF', 'dornic': 'MUTVS'}
K3 = ['!', '#', 'I', ':', '*', '^']


def solve(name, clue, memory):
    """Final configuration - every mode below was measured in training."""
    try:
        if name in RULE:
            lines = [l for l in clue.split('\n') if l.strip()]
            mode = BEST[name]
            if mode == 'VC':    return _vs(name, lines, True, False, corpus_first=False)
            if mode == 'CVC':   return _vs(name, lines, True, False)
            if mode == 'VF':    return _vs(name, lines, False, False, corpus_first=False)
            if mode == 'MUTVS': return _vs(name, lines, True, True)
            return None
        if name == 'basten':
            return _basten(clue, 5)
        if name == 'kelmar':
            c = memory["counts"].get(name, 0)
            memory["counts"][name] = c + 1
            return _kelmar(clue, 1, c)
    except Exception:
        return None
    return None
def on_round_end(items, memory):
    pass
