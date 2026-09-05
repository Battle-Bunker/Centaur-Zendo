import json, os, re
try:
    import zfeat
except Exception:
    zfeat = None

_D = os.path.dirname(os.path.abspath(__file__))
WEIGHTS = {}; CFG = {}; ALLOW = {}
try:
    _M = json.load(open(os.path.join(_D, "model.json")))
    WEIGHTS = _M.get("W", {}) or {}
    CFG = _M.get("cfg", {}) or {}
    _H = _M.get("hand", {}) or {}
    for _n, _c in CFG.items():
        if _c and _c[0] and _n in _H:
            ALLOW[_n] = set(_H[_n])
except Exception:
    pass

FAMRE = re.compile(r'(\d+|coal|pigs|sand|logs|wool|milk)')
_FC = {}

def famc(k):
    v = _FC.get(k)
    if v is None:
        v = FAMRE.sub('#', k)
        if len(v) > 1 and v[-1] in 'CDHSRGB':
            v = v[:-1] + '#'
        _FC[k] = v
    return v


def on_round_start(memory):
    memory["n"] = memory.get("n", 0) + 1
    # warm the feature-name cache
    try:
        for nm, fn in zfeat.EXTRACT.items():
            pass
    except Exception:
        pass


def solve(name, clue, memory):
    if zfeat is None:
        return None
    try:
        fn = zfeat.EXTRACT.get(name)
        if fn is None:
            return None
        ex, cands, ans = zfeat.parse(name, clue)
        nc = len(cands)
        if nc < 2 or not ex:
            return None
        EF = [fn(e) for e in ex]
        CF = [fn(c) for c in cands]
        W = WEIGHTS.get(name) or {}
        c = CFG.get(name) or [0, 0, 0.3, True, 0.0]
        partial = bool(c[3]); minw = c[4]
        allow = ALLOW.get(name)
        score = [0.0] * nc
        e0 = EF[0]; rest = EF[1:]
        MISS = zfeat._MISS
        for k, v in e0.items():
            bad = False
            for o in rest:
                if o.get(k, MISS) != v:
                    bad = True
                    break
            if bad:
                continue
            f = famc(k)
            if allow is not None and f not in allow:
                continue
            wt = W.get(f, 1.0)
            if wt < minw:
                continue
            hit = -1; h = 0
            for i in range(nc):
                if CF[i].get(k, MISS) == v:
                    h += 1
                    if h == 1:
                        hit = i
            if h == 0 or h == nc:
                continue
            if h == 1:
                score[hit] += wt
            elif partial:
                u = wt / (h * h)
                for i in range(nc):
                    if CF[i].get(k, MISS) == v:
                        score[i] += u
        best = 0; bs = score[0]
        for i in range(1, nc):
            if score[i] > bs:
                bs = score[i]; best = i
        return ans[best]
    except Exception:
        return None


def on_round_end(items, memory):
    pass
