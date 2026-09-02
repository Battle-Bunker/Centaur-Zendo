"""quilm = seven-segment matchstick puzzle.

Clue "S/k": S is a digit string drawn with matchsticks (7-segment digits).
Answer: a same-length digit string reachable by MOVING exactly k matches,
i.e. sum(segments removed) == sum(segments added) == k.
"""

SEG = (63, 6, 91, 79, 102, 109, 125, 7, 127, 111)   # 0-9, bits a..g

# COST[d][e] = (removed, added) turning digit d into digit e
_pc = lambda x: bin(x).count("1")
COST = [[(_pc(SEG[d] & ~SEG[e]), _pc(SEG[e] & ~SEG[d])) for e in range(10)]
        for d in range(10)]

# TBL[d][(r,a)] -> e  (a single digit substitution with that exact cost)
TBL = []
OPT = []
for d in range(10):
    t = {}
    o = []
    for e in range(10):
        if e == d:
            continue
        r, a = COST[d][e]
        if r <= 4 and a <= 4:
            o.append((r, a, e))
            if (r, a) not in t:
                t[(r, a)] = e
    # prefer "balanced" small edits first
    o.sort(key=lambda x: (x[0] + x[1]))
    TBL.append(t)
    OPT.append(o)

DIG = [str(i) for i in range(10)]


def _search(s, k):
    """Return a same-length digit string reachable by moving exactly k matches."""
    n = len(s)
    ds = [ord(c) - 48 for c in s]

    # 1) one substitution that costs exactly (k, k)
    for i in range(n):
        e = TBL[ds[i]].get((k, k))
        if e is not None:
            out = list(s)
            out[i] = DIG[e]
            return "".join(out)   # a 1-digit edit can never be an anagram

    # 2) two substitutions
    for i in range(n):
        ti = OPT[ds[i]]
        for j in range(i + 1, n):
            tj = TBL[ds[j]]
            for r1, a1, e1 in ti:
                if r1 > k or a1 > k:
                    continue
                e2 = tj.get((k - r1, k - a1))
                if e2 is not None:
                    out = list(s)
                    out[i] = DIG[e1]
                    out[j] = DIG[e2]
                    res = "".join(out)
                    if sorted(res) != sorted(s):
                        return res

    # 3) general DP over positions (state = (removed, added), capped at k)
    states = {(0, 0): ()}
    for i in range(n):
        d = ds[i]
        nxt = {}
        for (R, A), path in states.items():
            if (R, A) not in nxt:
                nxt[(R, A)] = path + (d,)
            for r, a, e in OPT[d]:
                nR = R + r
                nA = A + a
                if nR <= k and nA <= k:
                    key = (nR, nA)
                    if key not in nxt:
                        nxt[key] = path + (e,)
        states = nxt
    path = states.get((k, k))
    if path is not None:
        return "".join(DIG[x] for x in path)
    return None


def on_round_start(memory):
    memory.setdefault("cache", {})


def solve(name, clue, memory):
    try:
        s, _, kk = clue.rpartition("/")
        cache = memory["cache"]
        hit = cache.get(clue)
        if hit is not None:
            return hit
        r = _search(s, int(kk))
        if r is not None:
            cache[clue] = r
        return r
    except Exception:
        return None


def on_round_end(items, memory):
    c = memory.get("cache", {})
    if len(c) > 4000:
        memory["cache"] = {}
