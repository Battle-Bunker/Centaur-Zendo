"""Round 5: even index -> compact gap layout, odd index -> no-gap layout."""
LET = "SCHDV"


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def _build(clue, pitch):
    f = clue.split('/')
    n = len(f)
    hs = []; d2 = []; d3 = []
    for x in f:
        hs.append(int(x[0]))
        if len(x) > 2:
            d2.append(int(x[1])); d3.append(int(x[2]))
        else:
            d2.append(0); d3.append(0)
    d2[n-1] = max(1, d3[n-2]) if n >= 2 else 1
    m = max(d2)
    for i in range(n-1):
        need = d2[i] + (d2[i+1] - d3[i] if d2[i+1] > d3[i] else 0)
        if need > m:
            m = need
    shelves = []
    prev = None
    maxslot = 0
    for i in range(n):
        if i == 0:
            F = list(range(d2[0])); C = []
        else:
            t = d3[i-1]; P = prev
            if d2[i] >= t:
                fresh = [s for s in range(m) if s not in P]
                F = P[:t] + fresh[:d2[i]-t]; C = []
            else:
                F = P[:d2[i]]; C = P[d2[i]:t]
        items = [(s, hs[i]) for s in F] + [(s, 1) for s in C]
        items.sort()
        if items[-1][0] > maxslot:
            maxslot = items[-1][0]
        shelves.append(items)
        prev = F
    W = pitch * maxslot + 1
    out = []
    li = 0
    for i in range(n):
        rail = ['='] * W
        for (s, _) in shelves[i]:
            rail[pitch*s] = 'v'
        out.append(''.join(rail))
        rows = [['.'] * W for _ in range(hs[i])]
        for (s, ih) in shelves[i]:
            ch = LET[li % 5]
            li += 1
            j = pitch*s
            for r in range(ih):
                rows[r][j] = ch
        for r in rows:
            out.append(''.join(r))
    return '\n'.join(out)


def solve(name, clue, memory):
    try:
        return _build(clue, 2 if (memory.get("_index", 0) & 1) == 0 else 1)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
