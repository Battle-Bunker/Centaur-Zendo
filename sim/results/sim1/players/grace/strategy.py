"""strategy.py — centaur zendo solvers."""

import time
from itertools import permutations
from fractions import Fraction

# ---------------------------------------------------------------- utilities

def _egypt(n, d):
    out = []
    for _ in range(12):
        if n == 0:
            break
        if d % n == 0:
            out.append(d // n)
            break
        q = -(-d // n)
        out.append(q)
        n, d = n * q - d, d * q
        g = _gcd(n, d)
        if g > 1:
            n //= g
            d //= g
    return out


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _debruijn(k, n, alpha):
    a = [0] * (k * n)
    seq = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                seq.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)
    db(1, 1)
    return ''.join(alpha[i] for i in seq)


def _spf(n):
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        if n % q == 0:
            return q
    d = 49
    while d * d <= n and d < 2000:
        if n % d == 0:
            return d
        d += 2
    if d * d > n:
        return n
    if _mr(n):
        return n
    best = n
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if _mr(m):
            if m < best:
                best = m
            continue
        f = _rho(m)
        stack.append(f)
        stack.append(m // f)
    return best


def _rho(n):
    if n % 2 == 0:
        return 2
    import random as _r
    while True:
        x = _r.randrange(2, n - 1)
        y = x
        c = _r.randrange(1, n - 1)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = _gcd(abs(x - y), n)
        if d != n:
            return d


def _bsgs(g, h, p):
    m = int(p ** 0.5) + 1
    tbl = {}
    e = 1
    for j in range(m):
        if e not in tbl:
            tbl[e] = j
        e = e * g % p
    factor = pow(g, p - 1 - m, p)
    y = h
    for i in range(m + 1):
        if y in tbl:
            return i * m + tbl[y]
        y = y * factor % p
    return None


# ---------------------------------------------------------------- regex NFA

class _RX:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.n = 0
        self.trans = {}
        self.eps = {}

    def new(self):
        s = self.n
        self.n += 1
        self.trans[s] = []
        self.eps[s] = []
        return s

    def parse(self):
        st, en = self.alt()
        return st, en

    def alt(self):
        parts = [self.cat()]
        while self.i < len(self.s) and self.s[self.i] == '|':
            self.i += 1
            parts.append(self.cat())
        if len(parts) == 1:
            return parts[0]
        st = self.new()
        en = self.new()
        for a, b in parts:
            self.eps[st].append(a)
            self.eps[b].append(en)
        return st, en

    def cat(self):
        items = []
        while self.i < len(self.s) and self.s[self.i] not in '|)':
            items.append(self.rep())
        if not items:
            st = self.new()
            return st, st
        st, cur = items[0]
        for a, b in items[1:]:
            self.eps[cur].append(a)
            cur = b
        return st, cur

    def rep(self):
        a, b = self.atom()
        while self.i < len(self.s) and self.s[self.i] in '*+?':
            c = self.s[self.i]
            self.i += 1
            st = self.new()
            en = self.new()
            self.eps[st].append(a)
            self.eps[b].append(en)
            if c == '*':
                self.eps[st].append(en)
                self.eps[b].append(a)
            elif c == '+':
                self.eps[b].append(a)
            else:
                self.eps[st].append(en)
            a, b = st, en
        return a, b

    def atom(self):
        c = self.s[self.i]
        if c == '(':
            self.i += 1
            a, b = self.alt()
            self.i += 1  # ')'
            return a, b
        if c == '[':
            j = self.s.index(']', self.i)
            chars = set(self.s[self.i + 1:j])
            self.i = j + 1
            st = self.new()
            en = self.new()
            for ch in chars:
                self.trans[st].append((ch, en))
            return st, en
        self.i += 1
        st = self.new()
        en = self.new()
        if c == '.':
            for ch in 'ab':
                self.trans[st].append((ch, en))
        else:
            self.trans[st].append((c, en))
        return st, en


def _closure(nfa, states):
    stack = list(states)
    out = set(states)
    while stack:
        s = stack.pop()
        for t in nfa.eps[s]:
            if t not in out:
                out.add(t)
                stack.append(t)
    return frozenset(out)


def _step(nfa, states, ch):
    out = set()
    for s in states:
        for c, t in nfa.trans[s]:
            if c == ch:
                out.add(t)
    return _closure(nfa, out)


def _duomask(clue, budget):
    r1, r2 = clue.split()
    n1 = _RX(r1)
    s1, e1 = n1.parse()
    n2 = _RX(r2)
    s2, e2 = n2.parse()
    a0 = _closure(n1, [s1])
    b0 = _closure(n2, [s2])
    seen = {(a0, b0)}
    q = [(a0, b0, '')]
    deadline = time.perf_counter() + budget
    while q:
        if time.perf_counter() > deadline:
            return ''
        nq = []
        for a, b, w in q:
            if e1 in a and e2 in b:
                return w
            for ch in 'ab':
                na = _step(n1, a, ch)
                nb = _step(n2, b, ch)
                if not na or not nb:
                    continue
                if (na, nb) in seen:
                    continue
                seen.add((na, nb))
                nq.append((na, nb, w + ch))
        q = nq
        if len(w if False else '') > 0:
            pass
    return ''


# ---------------------------------------------------------------- solvers

def _grayling(clue, budget):
    a, b, n = clue.split()
    n = int(n)
    L = len(a)
    av = int(a, 2)
    bv = int(b, 2)
    deadline = time.perf_counter() + budget
    path = [av]
    seen = {av}

    def hd(x, y):
        return bin(x ^ y).count('1')

    def dfs(cur, left):
        if time.perf_counter() > deadline:
            return False
        if left == 0:
            return cur == bv
        d = hd(cur, bv)
        if d > left or (left - d) % 2:
            return False
        for i in range(L):
            nxt = cur ^ (1 << (L - 1 - i))
            if nxt in seen:
                continue
            seen.add(nxt)
            path.append(nxt)
            if dfs(nxt, left - 1):
                return True
            path.pop()
            seen.discard(nxt)
        return False

    if not dfs(av, n):
        return None
    return [format(v, '0%db' % L) for v in path]


def _hail_seq(n):
    seq = [n]
    while n != 1 and len(seq) < 2000:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        seq.append(n)
    return seq


def _hansom(clue, budget):
    p, t = clue.split('|')
    pts = [tuple(map(int, q.split(','))) for q in p.split()]
    n = len(pts)
    if n > 8:
        order = list(range(n))
    else:
        best = None
        bestv = 1 << 60
        for perm in permutations(range(1, n)):
            o = (0,) + perm
            v = 0
            for i in range(n):
                x1, y1 = pts[o[i]]
                x2, y2 = pts[o[(i + 1) % n]]
                v += abs(x1 - x2) + abs(y1 - y2)
                if v >= bestv:
                    break
            if v < bestv:
                bestv = v
                best = o
        order = list(best)
    return order, pts


def _subset_sum(nums, target):
    reach = {0: None}
    for i, v in enumerate(nums):
        for s in list(reach.keys()):
            ns = s + v
            if ns <= target and ns not in reach:
                reach[ns] = (s, i)
        if target in reach:
            break
    if target not in reach:
        return None
    out = []
    cur = target
    while cur:
        s, i = reach[cur]
        out.append(i)
        cur = s
    out.reverse()
    return out


def _topple(digits, target, budget):
    deadline = time.perf_counter() + budget
    tgt = float(target)

    def rec_nodiv(vals, exprs):
        if len(vals) == 1:
            return exprs[0] if -1e-9 < vals[0] - tgt < 1e-9 else None
        if time.perf_counter() > deadline:
            return None
        L = len(vals)
        for i in range(L):
            for j in range(i + 1, L):
                a = vals[i]
                b = vals[j]
                ea = exprs[i]
                eb = exprs[j]
                rest = [vals[k] for k in range(L) if k != i and k != j]
                reste = [exprs[k] for k in range(L) if k != i and k != j]
                for val, e in ((a + b, ea + eb + '+'), (a * b, ea + eb + '*'),
                               (a - b, ea + eb + '-'), (b - a, eb + ea + '-')):
                    r = rec_nodiv(rest + [val], reste + [e])
                    if r:
                        return r
        return None

    def rec(vals, exprs):
        if len(vals) == 1:
            return exprs[0] if -1e-9 < vals[0] - tgt < 1e-9 else None
        if time.perf_counter() > deadline:
            return None
        L = len(vals)
        for i in range(L):
            for j in range(i + 1, L):
                a = vals[i]
                b = vals[j]
                ea = exprs[i]
                eb = exprs[j]
                rest = [vals[k] for k in range(L) if k != i and k != j]
                reste = [exprs[k] for k in range(L) if k != i and k != j]
                cands = [(a + b, ea + eb + '+'), (a * b, ea + eb + '*'),
                         (a - b, ea + eb + '-'), (b - a, eb + ea + '-')]
                if b:
                    cands.append((a / b, ea + eb + '/'))
                if a:
                    cands.append((b / a, eb + ea + '/'))
                for val, e in cands:
                    r = rec(rest + [val], reste + [e])
                    if r:
                        return r
        return None

    fv = [float(d) for d in digits]
    ex = [str(d) for d in digits]
    e = rec_nodiv(fv, ex)
    if e and _rpn_ok(e, target):
        return e
    e = rec(fv, ex)
    if e and _rpn_ok(e, target):
        return e
    return _topple_exact(digits, target, deadline)


def _rpn_ok(e, target):
    st = []
    for ch in e:
        if ch.isdigit():
            st.append(Fraction(int(ch)))
        else:
            if len(st) < 2:
                return False
            y = st.pop()
            x = st.pop()
            if ch == '+':
                st.append(x + y)
            elif ch == '-':
                st.append(x - y)
            elif ch == '*':
                st.append(x * y)
            else:
                if y == 0:
                    return False
                st.append(x / y)
    return len(st) == 1 and st[0] == target


def _topple_exact(digits, target, deadline):
    tgt = Fraction(target)

    def rec(vals, exprs):
        if len(vals) == 1:
            return exprs[0] if vals[0] == tgt else None
        if time.perf_counter() > deadline:
            return None
        L = len(vals)
        for i in range(L):
            for j in range(i + 1, L):
                a = vals[i]
                b = vals[j]
                ea = exprs[i]
                eb = exprs[j]
                rest = [vals[k] for k in range(L) if k != i and k != j]
                reste = [exprs[k] for k in range(L) if k != i and k != j]
                cands = [(a + b, ea + eb + '+'), (a * b, ea + eb + '*'),
                         (a - b, ea + eb + '-'), (b - a, eb + ea + '-')]
                if b:
                    cands.append((a / b, ea + eb + '/'))
                if a:
                    cands.append((b / a, eb + ea + '/'))
                for val, e in cands:
                    r = rec(rest + [val], reste + [e])
                    if r:
                        return r
        return None
    return rec([Fraction(d) for d in digits], [str(d) for d in digits])


def _lcs(a, b):
    la, lb = len(a), len(b)
    dp = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la - 1, -1, -1):
        ra = a[i]
        di = dp[i]
        dn = dp[i + 1]
        for j in range(lb - 1, -1, -1):
            di[j] = dn[j + 1] + 1 if ra == b[j] else (dn[j] if dn[j] >= di[j + 1] else di[j + 1])
    out = []
    i = j = 0
    while i < la and j < lb:
        if a[i] == b[j]:
            out.append(a[i])
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1
        else:
            j += 1
    return ''.join(out)


def _carre(clue):
    rows = clue.split('/')
    n = len(rows)
    g = [list(r) for r in rows]
    bh = 2 if n == 4 else (2 if n == 6 else 3)
    bw = n // bh if n % bh == 0 else n
    digits = [str(i) for i in range(1, n + 1)]

    def ok(r, c, v):
        for i in range(n):
            if g[r][i] == v or g[i][c] == v:
                return False
        return True

    cells = [(r, c) for r in range(n) for c in range(n) if g[r][c] == '.']

    def dfs(k):
        if k == len(cells):
            return True
        r, c = cells[k]
        for v in digits:
            if ok(r, c, v):
                g[r][c] = v
                if dfs(k + 1):
                    return True
                g[r][c] = '.'
        return False
    if dfs(0):
        return ['' .join(row) for row in g]
    return None


def _nonogram(clue, budget):
    a, b = clue.split('\n')
    rows = [tuple(int(x) for x in s.split(',') if x) for s in a.split('/')]
    cols = [tuple(int(x) for x in s.split(',') if x) for s in b.split('/')]
    W = len(cols)
    H = len(rows)
    deadline = time.perf_counter() + budget

    def lines(spec, width):
        res = []

        def rec(pos, idx, cur):
            if idx == len(spec):
                res.append(cur + [0] * (width - len(cur)))
                return
            for start in range(pos, width - sum(spec[idx:]) - (len(spec) - idx - 1) + 1):
                nc = cur + [0] * (start - len(cur)) + [1] * spec[idx]
                rec(start + spec[idx] + 1, idx + 1, nc)
        rec(0, 0, [])
        return res

    rowopts = [lines(r, W) for r in rows]
    grid = []

    def colok(partial):
        r = len(partial)
        for c in range(W):
            seq = [partial[i][c] for i in range(r)]
            runs = []
            cnt = 0
            for v in seq:
                if v:
                    cnt += 1
                elif cnt:
                    runs.append(cnt)
                    cnt = 0
            spec = cols[c]
            if cnt:
                # last run possibly extendable
                if len(runs) >= len(spec):
                    return False
                if cnt > spec[len(runs)]:
                    return False
                if runs != list(spec[:len(runs)]):
                    return False
            else:
                if runs != list(spec[:len(runs)]):
                    return False
                if len(runs) > len(spec):
                    return False
            rem = sum(spec) - sum(runs) - cnt
            if rem > (H - r):
                return False
        return True

    def dfs(i, partial):
        if time.perf_counter() > deadline:
            return None
        if i == H:
            for c in range(W):
                seq = [partial[k][c] for k in range(H)]
                runs = []
                cnt = 0
                for v in seq:
                    if v:
                        cnt += 1
                    elif cnt:
                        runs.append(cnt)
                        cnt = 0
                if cnt:
                    runs.append(cnt)
                if tuple(runs) != cols[c]:
                    return None
            return partial
        for opt in rowopts[i]:
            np = partial + [opt]
            if colok(np):
                r = dfs(i + 1, np)
                if r:
                    return r
        return None
    res = dfs(0, [])
    if not res:
        return None
    return [''.join('#' if v else '.' for v in row) for row in res]


def _parse_graph(clue):
    parts = clue.split()
    n = int(parts[0])
    adj = [set() for _ in range(n)]
    for p in parts[1:]:
        u, v = p.split('-')
        u, v = int(u), int(v)
        adj[u].add(v)
        adj[v].add(u)
    return n, adj


def _hampath(n, adj, budget):
    deadline = time.perf_counter() + budget
    path = []
    used = [False] * n

    def dfs(cur, depth):
        if time.perf_counter() > deadline:
            return False
        if depth == n:
            return True
        for nx in sorted(adj[cur], key=lambda x: len(adj[x])):
            if not used[nx]:
                used[nx] = True
                path.append(nx)
                if dfs(nx, depth + 1):
                    return True
                path.pop()
                used[nx] = False
        return False
    for st in range(n):
        path[:] = [st]
        used[:] = [False] * n
        used[st] = True
        if dfs(st, 1):
            return list(path)
        if time.perf_counter() > deadline:
            break
    return None


def _hamilton(n, adj, budget):
    deadline = time.perf_counter() + budget
    path = [0]
    used = [False] * n
    used[0] = True

    def dfs(cur, depth):
        if time.perf_counter() > deadline:
            return False
        if depth == n:
            return 0 in adj[cur]
        for nx in sorted(adj[cur], key=lambda x: len(adj[x])):
            if not used[nx]:
                used[nx] = True
                path.append(nx)
                if dfs(nx, depth + 1):
                    return True
                path.pop()
                used[nx] = False
        return False
    if dfs(0, 1):
        return path
    return None


def _color3(n, adj, budget):
    deadline = time.perf_counter() + budget
    order = sorted(range(n), key=lambda x: -len(adj[x]))
    col = [-1] * n

    def dfs(k):
        if time.perf_counter() > deadline:
            return False
        if k == n:
            return True
        v = order[k]
        used = {col[u] for u in adj[v] if col[u] >= 0}
        mx = max([c for c in col if c >= 0], default=-1)
        for c in range(min(3, mx + 2)):
            if c not in used:
                col[v] = c
                if dfs(k + 1):
                    return True
                col[v] = -1
        return False
    if dfs(0):
        return col
    return None


def _sat(clue, budget):
    clauses = []
    nv = 0
    for grp in clue.split():
        lits = [int(x) for x in grp.split(',')]
        clauses.append(lits)
        for l in lits:
            nv = max(nv, abs(l))
    # DPLL-ish brute force over 2^nv when small
    if nv <= 20:
        for mask in range(1 << nv):
            ok = True
            for cl in clauses:
                good = False
                for l in cl:
                    v = (mask >> (abs(l) - 1)) & 1
                    if (l > 0 and v) or (l < 0 and not v):
                        good = True
                        break
                if not good:
                    ok = False
                    break
            if ok:
                return nv, [((mask >> i) & 1) for i in range(nv)]
    return nv, None


def _islands(grid, conn8=False):
    H = len(grid)
    W = len(grid[0])
    seen = [[False] * W for _ in range(H)]
    comps = []
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if conn8:
        dirs += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for r in range(H):
        for c in range(W):
            if grid[r][c] == '#' and not seen[r][c]:
                stack = [(r, c)]
                seen[r][c] = True
                size = 0
                while stack:
                    x, y = stack.pop()
                    size += 1
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < H and 0 <= ny < W and not seen[nx][ny] and grid[nx][ny] == '#':
                            seen[nx][ny] = True
                            stack.append((nx, ny))
                comps.append(size)
    return comps


def _maze(clue):
    grid = clue.split('\n')
    H = len(grid)
    start = end = None
    for r in range(H):
        for c, ch in enumerate(grid[r]):
            if ch == 'S':
                start = (r, c)
            elif ch == 'E':
                end = (r, c)
    if not start or not end:
        return None
    prev = {start: None}
    q = [start]
    while q:
        nq = []
        for x, y in q:
            if (x, y) == end:
                q = []
                nq = []
                break
            for dx, dy, d in ((-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')):
                nx, ny = x + dx, y + dy
                if 0 <= nx < H and 0 <= ny < len(grid[nx]) and grid[nx][ny] != '#' and (nx, ny) not in prev:
                    prev[(nx, ny)] = ((x, y), d)
                    nq.append((nx, ny))
        q = nq
    if end not in prev:
        return None
    path = []
    cur = end
    while prev[cur] is not None:
        p, d = prev[cur]
        path.append((d, cur))
        cur = p
    path.reverse()
    return start, path


def _spiral(grid, cw=True):
    g = [list(r) for r in grid]
    out = []
    top, bot = 0, len(g) - 1
    left, right = 0, len(g[0]) - 1
    if cw:
        while top <= bot and left <= right:
            for c in range(left, right + 1):
                out.append(g[top][c])
            top += 1
            for r in range(top, bot + 1):
                out.append(g[r][right])
            right -= 1
            if top <= bot:
                for c in range(right, left - 1, -1):
                    out.append(g[bot][c])
                bot -= 1
            if left <= right:
                for r in range(bot, top - 1, -1):
                    out.append(g[r][left])
                left += 1
    else:
        while top <= bot and left <= right:
            for r in range(top, bot + 1):
                out.append(g[r][left])
            left += 1
            if top <= bot:
                for c in range(left, right + 1):
                    out.append(g[bot][c])
                bot -= 1
            if left <= right:
                for r in range(bot, top - 1, -1):
                    out.append(g[r][right])
                right -= 1
            if top <= bot:
                for c in range(right, left - 1, -1):
                    out.append(g[top][c])
                top += 1
    return ''.join(out)


def _zebu(clue):
    L = 'ABCDE'
    cons = []
    for c in clue.split():
        if '<' in c:
            x, y = c.split('<')
            cons.append(('<', x, y))
        elif '|' in c:
            x, y = c.split('|')
            cons.append(('|', x, y))
        elif '#' in c:
            x, k = c.split('#')
            cons.append(('#', x, int(k)))
    for perm in permutations(range(1, 6)):
        pos = dict(zip(L, perm))
        ok = True
        for t, x, y in cons:
            if t == '<':
                ok = pos[x] < pos[y]
            elif t == '|':
                ok = abs(pos[x] - pos[y]) == 1
            else:
                ok = pos[x] == y
            if not ok:
                break
        if ok:
            order = [''] * 5
            for ch in L:
                order[pos[ch] - 1] = ch
            return ''.join(order), pos
    return None


def _life_pred(target, budget):
    H = len(target)
    W = len(target[0])
    t = [sum(1 << x for x, ch in enumerate(row) if ch == '#') for row in target]
    c3 = _C3.get(W)
    if c3 is None:
        c3 = []
        for m in range(1 << W):
            c3.append([((m >> (x - 1)) & 1 if x > 0 else 0) + ((m >> x) & 1) +
                       ((m >> (x + 1)) & 1 if x < W - 1 else 0) for x in range(W)])
        _C3[W] = c3
    deadline = time.perf_counter() + budget
    memo = {}

    def next_rows(a, b, tr):
        k = (a, b, tr)
        got = memo.get(k)
        if got is not None:
            return got
        ca = c3[a]
        cb = c3[b]
        res = []

        def rec(pos, cur):
            x = pos - 2
            if x >= 0:
                n = ca[x] + cb[x] + c3[cur][x] - ((b >> x) & 1)
                live = 1 if (n == 3 or (n == 2 and (b >> x) & 1)) else 0
                if live != ((tr >> x) & 1):
                    return
            if pos == W:
                for x in (W - 2, W - 1):
                    if x < 0:
                        continue
                    n = ca[x] + cb[x] + c3[cur][x] - ((b >> x) & 1)
                    live = 1 if (n == 3 or (n == 2 and (b >> x) & 1)) else 0
                    if live != ((tr >> x) & 1):
                        return
                res.append(cur)
                return
            rec(pos + 1, cur)
            rec(pos + 1, cur | (1 << pos))
        rec(0, 0)
        memo[k] = res
        return res

    rows = [0] * H

    def dfs(i, a, b):
        if time.perf_counter() > deadline:
            raise TimeoutError
        if i == H:
            return 0 in next_rows(a, b, t[H - 1])
        if i == 0:
            for r in range(1 << W):
                rows[0] = r
                if dfs(1, 0, r):
                    return True
            return False
        for c in next_rows(a, b, t[i - 1]):
            rows[i] = c
            if dfs(i + 1, b, c):
                return True
        return False

    try:
        if dfs(0, 0, 0):
            return [''.join('#' if (r >> x) & 1 else '.' for x in range(W)) for r in rows]
    except TimeoutError:
        return None
    return None


def _isqrt(n):
    x = int(n ** 0.5)
    while x * x > n:
        x -= 1
    while (x + 1) * (x + 1) <= n:
        x += 1
    return x


def _totient(n):
    r = n
    p = 2
    m = n
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            r -= r // p
        p += 1
    if m > 1:
        r -= r // m
    return r


def _divisors(n):
    d = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            d.append(i)
            if i != n // i:
                d.append(n // i)
        i += 1
    return sorted(d)


def _isprime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def _period(n):
    m = n
    while m % 2 == 0:
        m //= 2
    while m % 5 == 0:
        m //= 5
    if m == 1:
        return 0
    k = 1
    v = 10 % m
    while v != 1 and k < 10000:
        v = v * 10 % m
        k += 1
    return k


# ---------------------------------------------------------------- framework

_COUNT = {}
_HAIL_FIRST = {}
_C3 = {}


def _mr(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _pp(clue, budget):
    k = len(clue)
    deadline = time.perf_counter() + budget
    for L in range(max(k, 1), 13):
        h = (L + 1) // 2
        cands = set()
        for st in range(0, L - k + 1):
            fixed = {}
            bad = False
            for i, ch in enumerate(clue):
                pos = st + i
                hp = pos if pos < h else L - 1 - pos
                if hp in fixed and fixed[hp] != ch:
                    bad = True
                    break
                fixed[hp] = ch
            if bad or fixed.get(0) == '0':
                continue
            free = [i for i in range(h) if i not in fixed]
            if len(free) > 4:
                continue
            base = [None] * h
            for i, ch in fixed.items():
                base[i] = ch
            n_free = len(free)
            for combo in range(10 ** n_free):
                dig = list(base)
                cc = combo
                for i in range(n_free - 1, -1, -1):
                    dig[free[i]] = "0123456789"[cc % 10]
                    cc //= 10
                if dig[0] == '0':
                    continue
                half = ''.join(dig)
                cands.add(half + (half[::-1] if L % 2 == 0 else half[-2::-1]))
        for cand in sorted(cands, key=int):
            if time.perf_counter() > deadline:
                return ""
            if _mr(int(cand)):
                return cand
    return ""



def on_round_start(memory):
    _COUNT.clear()
    if not _HAIL_FIRST:
        cache = {1: 0}
        for n in range(2, 60000):
            m = n
            stack = []
            while m not in cache:
                stack.append(m)
                m = m // 2 if m % 2 == 0 else 3 * m + 1
            val = cache[m]
            for x in reversed(stack):
                val += 1
                cache[x] = val
            c = cache[n]
            if c not in _HAIL_FIRST:
                _HAIL_FIRST[c] = n
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    i = _COUNT.get(name, 0)
    _COUNT[name] = i + 1
    try:
        r = _solve(name, clue, i)
    except Exception:
        raise
    if not r:
        raise ValueError("skip")
    return r


def _solve(name, clue, v):
    if name == "SPQ":
        return str(_spf(int(clue)))

    if name == "IDX":
        g, h, p = [int(x) for x in clue.split()]
        x = _bsgs(g, h, p)
        return str(x) if x is not None else ""

    if name == "wolf":
        cands = set(range(256))
        for pair in clue.split():
            a, b = pair.split('>')
            n = len(a)
            for i in range(n):
                nb = (int(a[(i - 1) % n]) << 2) | (int(a[i]) << 1) | int(a[(i + 1) % n])
                want = int(b[i])
                cands = {r for r in cands if (r >> nb) & 1 == want}
        if not cands:
            return ""
        return format(min(cands), '08b')

    if name == "BASILISK":
        s, r = clue.split(':')
        f, t = r.split('>')
        val = int(s, int(f))
        t = int(t)
        if val == 0:
            return "0"
        out = []
        while val:
            out.append("0123456789abcdefghijklmnopqrstuvwxyz"[val % t])
            val //= t
        return ''.join(reversed(out))

    if name == "SUNZI":
        x = 0
        mod = 1
        for part in clue.split():
            a, m = part.split('%')
            a, m = int(a), int(m)
            # solve x ≡ a mod m together with x ≡ x mod mod
            g = _gcd(mod, m)
            inv = pow(mod // g, -1, m // g)
            x = x + mod * (((a - x) // g * inv) % (m // g))
            mod = mod * m // g
            x %= mod
        return str(x % mod)

    if name == "CRIBROT":
        c, crib = clue.split('|')
        for s in range(26):
            d = ''.join(chr((ord(ch) - 97 - s) % 26 + 97) if 'a' <= ch <= 'z' else ch for ch in c)
            if crib in d:
                return d
        return ""

    if name == "TWINE":
        a, b, k = clue.split('|')
        return _lcs(a, b)

    if name == "AHMES":
        n, d = clue.split('/')
        den = _egypt(int(n), int(d))
        return ' '.join(str(q) for q in den)

    if name == "ALLWIN":
        alpha, n = clue.split()
        return _debruijn(len(alpha), int(n), alpha)

    if name == "HAIL":
        n0 = int(clue)
        return str(_HAIL_FIRST.get(n0, ""))

    if name == "TARE":
        nums, t = clue.split('|')
        nums = [int(x) for x in nums.split()]
        idx = _subset_sum(nums, int(t))
        if idx is None:
            return ""
        sel = set(idx)
        return ''.join('1' if i in sel else '0' for i in range(len(nums)))

    if name == "TOPPLE":
        d, t = clue.split('=')
        e = _topple([int(c) for c in d], int(t), 0.015)
        return e or ""

    if name == "HANSOM":
        order, pts = _hansom(clue, 0.012)
        return ' '.join(str(i) for i in order)

    if name == "MARIENBAD":
        piles = [int(x) for x in clue.split()]
        x = 0
        for p in piles:
            x ^= p
        move = None
        for i, p in enumerate(piles):
            t = p ^ x
            if t < p:
                move = (i, p - t, t)
                break
        if move is None:
            move = (0, 1, piles[0] - 1)
        i, take, newv = move
        np = list(piles)
        np[i] = newv
        return ' '.join(str(x) for x in np)

    if name == "DUOMASK":
        return _duomask(clue, 0.012)

    if name == "GRAYLING":
        p = _grayling(clue, 0.012)
        if not p:
            return ""
        return ' '.join(p)

    if name == "carre":
        g = _carre(clue)
        if not g:
            return ""
        return '/'.join(g)

    if name == "hanjie":
        g = _nonogram(clue, 0.030)
        if not g:
            return ""
        return '\n'.join(g)

    if name == "ikos":
        n, adj = _parse_graph(clue)
        p = _hamilton(n, adj, 0.020)
        if not p:
            p = _hampath(n, adj, 0.010)
        if not p:
            return ""
        return ' '.join(str(x) for x in p)

    if name == "trico":
        n, adj = _parse_graph(clue)
        col = _color3(n, adj, 0.020)
        if col is None:
            return ""
        return ''.join(str(c) for c in col)

    if name == "krom":
        nv, asg = _sat(clue, 0.015)
        if asg is None:
            return ""
        return ''.join(str(x) for x in asg)

    if name == "volute":
        g = clue.split('\n')
        return _spiral(g, cw=True)

    if name == "warren":
        r = _maze(clue)
        if not r:
            return ""
        start, path = r
        return ''.join(d for d, _ in path)

    if name == "skerry":
        g = clue.split('\n')
        return str(len(_islands(g)))

    if name == "regina":
        g = clue.split('\n')
        n = len(g)
        blocked = [[ch == 'X' for ch in row] for row in g]
        res = [0] * n

        def dfs(c, rows, d1, d2):
            if c == n:
                return True
            for r in range(n):
                if blocked[r][c]:
                    continue
                bit = 1 << r
                if rows & bit:
                    continue
                a = 1 << (r - c + n)
                b = 1 << (r + c)
                if (d1 & a) or (d2 & b):
                    continue
                res[c] = r
                if dfs(c + 1, rows | bit, d1 | a, d2 | b):
                    return True
            return False
        if dfs(0, 0, 0, 0):
            return ''.join(str(x) for x in res)
        return ""

    if name == "zebu":
        r = _zebu(clue)
        if not r:
            return ""
        order, pos = r
        return order

    if name == "RUNIC":
        runs = []
        prev = clue[0]
        cnt = 0
        for ch in clue:
            if ch == prev:
                cnt += 1
            else:
                runs.append((prev, cnt))
                prev = ch
                cnt = 1
        runs.append((prev, cnt))
        return ''.join('%d%s' % (c, ch) for ch, c in runs)

    if name == "ANAPAL":
        st, sub = clue.split('|')
        n = len(st)
        cnt = {}
        for ch in st:
            cnt[ch] = cnt.get(ch, 0) + 1
        odd = [ch for ch, c in cnt.items() if c % 2]
        if len(odd) > 1:
            return ""
        mid = odd[0] if odd else ''
        h = n // 2
        base = dict((ch, c // 2) for ch, c in cnt.items())
        k = len(sub)
        for s0 in range(0, n - k + 1):
            avail = dict(base)
            half = [None] * h
            good = True
            for j, ch in enumerate(sub):
                pos = s0 + j
                if n % 2 and pos == h:
                    if ch != mid:
                        good = False
                        break
                    continue
                hp = pos if pos < h else n - 1 - pos
                if half[hp] is None:
                    half[hp] = ch
                    avail[ch] = avail.get(ch, 0) - 1
                    if avail[ch] < 0:
                        good = False
                        break
                elif half[hp] != ch:
                    good = False
                    break
            if not good:
                continue
            pool = []
            for ch in sorted(avail):
                pool.extend([ch] * avail[ch])
            idx = 0
            for i in range(h):
                if half[i] is None:
                    half[i] = pool[idx]
                    idx += 1
            first = ''.join(half)
            return first + mid + first[::-1]
        return ""

    if name == "PP":
        return _pp(clue, 0.020)

    if name == "CHAKRA":
        N = int(clue)
        a0 = _isqrt(N)
        if a0 * a0 == N:
            return ""
        m, dd, a = 0, 1, a0
        n1, n0 = 1, a0
        d1, d0 = 0, 1
        for _ in range(200):
            if n0 * n0 - N * d0 * d0 == 1:
                return '%d %d' % (n0, d0)
            m = dd * a - m
            dd = (N - m * m) // dd
            a = (a0 + m) // dd
            n1, n0 = n0, a * n0 + n1
            d1, d0 = d0, a * d0 + d1
        return ""

    if name == "erewhon":
        g = _life_pred(clue.split('\n'), 0.020)
        return '\n'.join(g) if g else ""

    return ""


def on_round_end(items, memory):
    pass
