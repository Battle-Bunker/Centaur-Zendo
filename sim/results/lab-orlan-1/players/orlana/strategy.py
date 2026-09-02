"""orlan solver: rank candidate hops with a learned linear model."""
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
W = [-0.04555, -0.04555, -0.56555, -0.04159, 0.56159, -2.24391, -0.37316, 0.01987, 0.72596, 0.76451, -0.54906, -0.46265, 1.22665, -0.2319, 0.30175, -0.53365, 1.45177, -1.19585, 0.7309, 0.12148, 0.47527, -0.24805, 0.46469, -0.76455, 0.87075, -0.00993, -0.32119, -0.38207, -0.44898, 0.56124, 0.97651, 0.09404, -0.26353, 0.06907, -0.0, -0.0, -0.0]




def _hops(g, sym, R, C):
    out = []
    for r in range(R):
        row = g[r]
        for c in range(C):
            if row[c] != sym:
                continue
            for dr, dc in DIRS:
                rr, cc = r + dr, c + dc
                while 0 <= rr < R and 0 <= cc < C:
                    if g[rr][cc] == '.':
                        out.append((r, c, rr, cc))
                        break
                    rr, cc = rr + dr, cc + dc
    return out


def _nb(g, r, c, ch, R, C):
    n = 0
    for dr, dc in DIRS:
        rr, cc = r + dr, c + dc
        if 0 <= rr < R and 0 <= cc < C and g[rr][cc] == ch:
            n += 1
    return n


def _comps(g, sym, R, C):
    seen = set(); n = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] != sym or (r, c) in seen:
                continue
            n += 1; st = [(r, c)]; seen.add((r, c))
            while st:
                a, b = st.pop()
                for dr, dc in DIRS:
                    p = (a + dr, b + dc)
                    if p not in seen and 0 <= p[0] < R and 0 <= p[1] < C and g[p[0]][p[1]] == sym:
                        seen.add(p); st.append(p)
    return n


def _between(g, a, b):
    dr = b[0] - a[0]; dc = b[1] - a[1]
    n = max(abs(dr), abs(dc))
    sr = (dr > 0) - (dr < 0); sc = (dc > 0) - (dc < 0)
    return [g[a[0] + i * sr][a[1] + i * sc] for i in range(1, n)]


def _apply(g, src, dst):
    ng = [list(r) for r in g]
    s = ng[src[0]][src[1]]; ng[src[0]][src[1]] = '.'; ng[dst[0]][dst[1]] = s
    return [''.join(r) for r in ng]


def _fx(g, h, R, C, xs, os_, hb):
    src = (h[0], h[1]); dst = (h[2], h[3])
    ng = _apply(g, src, dst)
    dr = dst[0] - src[0]; dc = dst[1] - src[1]
    n = max(abs(dr), abs(dc)); sr = (dr > 0) - (dr < 0); sc = (dc > 0) - (dc < 0)
    j = [g[src[0] + i * sr][src[1] + i * sc] for i in range(1, n)]
    al = [x for x in xs if x[0] == dst[0] or x[1] == dst[1]]
    cl = [x for x in al if all(ch == '.' for ch in _between(ng, dst, x))]
    als = [x for x in xs if x[0] == src[0] or x[1] == src[1]]
    cls = [x for x in als if all(ch == '.' for ch in _between(g, src, x))]
    ha = _hops(ng, 'x', R, C); ob = _hops(g, 'o', R, C); oa = _hops(ng, 'o', R, C)
    nos = [(r, c) for r in range(R) for c in range(C) if ng[r][c] == 'o']
    f = []
    f.append(n)
    f.append(len(j)); f.append(j.count('x')); f.append(j.count('o')); f.append(j.count('#'))
    f.append(_nb(g, dst[0], dst[1], 'x', R, C)); f.append(_nb(g, dst[0], dst[1], 'o', R, C))
    f.append(_nb(g, dst[0], dst[1], '#', R, C)); f.append(_nb(g, dst[0], dst[1], '.', R, C))
    f.append(_nb(g, src[0], src[1], 'x', R, C)); f.append(_nb(g, src[0], src[1], 'o', R, C))
    f.append(_nb(g, src[0], src[1], '#', R, C)); f.append(_nb(g, src[0], src[1], '.', R, C))
    mdx = min([abs(dst[0]-x[0])+abs(dst[1]-x[1]) for x in xs]) if xs else 9
    mds = min([abs(src[0]-x[0])+abs(src[1]-x[1]) for x in xs]) if xs else 9
    f.append(mdx); f.append(mds); f.append(mdx - mds)
    f.append(len(al)); f.append(min([abs(dst[0]-x[0])+abs(dst[1]-x[1]) for x in al]) if al else 9)
    f.append(len(cl)); f.append(min([abs(dst[0]-x[0])+abs(dst[1]-x[1]) for x in cl]) if cl else 9)
    f.append(len(als)); f.append(len(cls))
    f.append(1 if (dst[0] in (0, R-1) or dst[1] in (0, C-1)) else 0)
    f.append(1 if (src[0] in (0, R-1) or src[1] in (0, C-1)) else 0)
    f.append(1 if sc == 0 else 0)
    f.append(len(ha) - len(hb)); f.append(len(oa) - len(ob))
    f.append(_comps(ng, 'o', R, C) - _comps(g, 'o', R, C))
    f.append(1 if dst in [(b[2], b[3]) for b in hb] else 0)
    f.append(sum(1 for b in ha if abs(b[2]-dst[0]) + abs(b[3]-dst[1]) == 1))
    f.append(sum(1 for o in nos for x in xs if o[0] == x[0] or o[1] == x[1]))
    f.append(sum(1 for o in nos for x in xs
                 if (o[0] == x[0] or o[1] == x[1]) and all(ch == '.' for ch in _between(ng, o, x))))
    f.append(abs(dst[0]-(R-1)/2.0) + abs(dst[1]-(C-1)/2.0))
    f.append(abs(src[0]-(R-1)/2.0) + abs(src[1]-(C-1)/2.0))
    f.append(len(os_)); f.append(len(xs))
    f.append(1.0)
    return f




def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    try:
        g = clue.strip().split("\n")
        R = len(g); C = len(g[0])
        xs = []; os_ = []
        for r in range(R):
            row = g[r]
            for c in range(C):
                ch = row[c]
                if ch == 'x': xs.append((r, c))
                elif ch == 'o': os_.append((r, c))
        hs = _hops(g, 'o', R, C)
        if not hs:
            return None
        cand = [h for h in hs
                if any((x[0] == h[2] or x[1] == h[3])
                       and abs(x[0]-h[2]) + abs(x[1]-h[3]) <= 3 for x in xs)]
        if not cand:
            cand = hs
        if len(cand) == 1:
            return "%d,%d>%d,%d" % cand[0]
        hb = _hops(g, 'x', R, C)
        best = None; bs = None
        for h in cand:
            f = _fx(g, h, R, C, xs, os_, hb)
            s = 0.0
            for wi, xi in zip(W, f):
                s += wi * xi
            if bs is None or s > bs:
                bs = s; best = h
        return "%d,%d>%d,%d" % best
    except Exception:
        return None
