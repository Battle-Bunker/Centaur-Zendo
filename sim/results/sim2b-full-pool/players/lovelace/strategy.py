"""Core solvers for Centaur Zendo challenge classes."""
import re, math, time
from itertools import permutations

DIG = "0123456789abcdefghijklmnopqrstuvwxyz"

# ---------- PP : shortest palindrome by appending ----------
def s_PP(clue):
    s = clue
    for k in range(len(s)):
        t = s[k:]
        if t == t[::-1]:
            return s + s[:k][::-1]
    return s

# ---------- BASILISK : base conversion  N:a>b ----------
def s_BASILISK(clue):
    lhs, b = clue.split('>')
    n, a = lhs.split(':')
    v = int(n, int(a)); b = int(b)
    if v == 0: return "0"
    neg = v < 0; v = abs(v); out = []
    while v:
        out.append(DIG[v % b]); v //= b
    return ('-' if neg else '') + ''.join(reversed(out))

# ---------- SUNZI : CRT ----------
def s_SUNZI(clue):
    r0, m0 = 0, 1
    for part in clue.split():
        r, m = part.split('%'); r = int(r); m = int(m)
        g = math.gcd(m0, m)
        lcm = m0 // g * m
        diff = (r - r0) // g
        inv = pow(m0 // g, -1, m // g) if m // g > 1 else 0
        r0 = (r0 + m0 * (diff * inv % (m // g))) % lcm
        m0 = lcm
    return str(r0 % m0)

# ---------- TARE : subset sum ----------
def s_TARE(clue):
    nums_s, t = clue.split('|'); t = int(t)
    nums = [int(x) for x in nums_s.split()]
    layers = [1]
    b = 1
    for v in nums:
        b |= b << v
        layers.append(b)
    if not (layers[-1] >> t) & 1:
        return None
    cur = t; chosen = []
    for i in range(len(nums) - 1, -1, -1):
        if (layers[i] >> cur) & 1:
            continue
        chosen.append(i); cur -= nums[i]
    chosen.reverse()
    return chosen, nums

# ---------- HAIL : collatz ----------
def s_HAIL(clue):
    n = int(clue); seq = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        seq.append(n)
    return seq

# ---------- skerry : island count ----------
def s_skerry(clue):
    g = clue.split('\n'); R = len(g); C = len(g[0])
    seen = set(); n = 0
    for r in range(R):
        row = g[r]
        for c in range(C):
            if row[c] == '#' and (r, c) not in seen:
                n += 1; st = [(r, c)]; seen.add((r, c))
                while st:
                    x, y = st.pop()
                    for a, b in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                        if 0 <= a < R and 0 <= b < C and g[a][b] == '#' and (a,b) not in seen:
                            seen.add((a,b)); st.append((a,b))
    return n

# ---------- volute : spiral read ----------
def s_volute(clue, ccw=False):
    g = [list(r) for r in clue.split('\n')]
    R = len(g); C = len(g[0])
    out = []
    top, bot, left, right = 0, R-1, 0, C-1
    if not ccw:
        while top <= bot and left <= right:
            for c in range(left, right+1): out.append(g[top][c])
            top += 1
            for r in range(top, bot+1): out.append(g[r][right])
            right -= 1
            if top <= bot:
                for c in range(right, left-1, -1): out.append(g[bot][c])
                bot -= 1
            if left <= right:
                for r in range(bot, top-1, -1): out.append(g[r][left])
                left += 1
    else:
        while top <= bot and left <= right:
            for r in range(top, bot+1): out.append(g[r][left])
            left += 1
            for c in range(left, right+1): out.append(g[bot][c])
            bot -= 1
            if left <= right:
                for r in range(bot, top-1, -1): out.append(g[r][right])
                right -= 1
            if top <= bot:
                for c in range(right, left-1, -1): out.append(g[top][c])
                top += 1
    return ''.join(out)

# ---------- wolf : wolfram rule ----------
def s_wolf(clue):
    bits = {}
    for pair in clue.split():
        a, b = pair.split('>')
        n = len(a)
        for i in range(n):
            idx = (int(a[(i-1) % n]) << 2) | (int(a[i]) << 1) | int(a[(i+1) % n])
            bits[idx] = int(b[i])
    rule = 0
    for k, v in bits.items():
        rule |= v << k
    return rule

# ---------- krom : 3-SAT ----------
def s_krom(clue):
    cls = []
    nv = 0
    for c in clue.split():
        lits = [int(x) for x in c.split(',')]
        pm = nm = 0
        for l in lits:
            v = abs(l); nv = max(nv, v)
            if l > 0: pm |= 1 << (v-1)
            else: nm |= 1 << (v-1)
        cls.append((pm, nm))
    for a in range(1 << nv):
        na = ~a
        for pm, nm in cls:
            if not (a & pm) and not (na & nm):
                break
        else:
            return [(1 if (a >> i) & 1 else 0) for i in range(nv)]
    return None

# ---------- graph parse ----------
def _graph(clue):
    parts = clue.split()
    n = int(parts[0])
    adj = [set() for _ in range(n)]
    edges = []
    for p in parts[1:]:
        a, b = p.split('-'); a = int(a); b = int(b)
        adj[a].add(b); adj[b].add(a); edges.append((a,b))
    return n, adj, edges

# ---------- trico : 3-colouring ----------
def s_trico(clue):
    n, adj, edges = _graph(clue)
    order = sorted(range(n), key=lambda v: -len(adj[v]))
    col = [-1]*n
    def bt(i):
        if i == n: return True
        v = order[i]
        used = {col[u] for u in adj[v] if col[u] >= 0}
        for c in range(3):
            if c in used: continue
            col[v] = c
            if bt(i+1): return True
            col[v] = -1
        return False
    return col if bt(0) else None

# ---------- ikos : hamiltonian cycle ----------
def s_ikos(clue, budget=0.008):
    n, adj, edges = _graph(clue)
    end = time.perf_counter() + budget
    path = [0]; used = [False]*n; used[0] = True
    def bt(d):
        if time.perf_counter() > end: raise TimeoutError
        if d == n:
            return 0 in adj[path[-1]]
        cand = sorted(adj[path[-1]], key=lambda u: len(adj[u]))
        for u in cand:
            if not used[u]:
                used[u] = True; path.append(u)
                if bt(d+1): return True
                path.pop(); used[u] = False
        return False
    try:
        if bt(1): return path
    except TimeoutError:
        return None
    return None

# ---------- carre : latin square ----------
def s_carre(clue):
    rows = clue.split('/')
    n = len(rows)
    g = [list(r) for r in rows]
    digits = [str(i) for i in range(1, n+1)]
    blanks = [(r,c) for r in range(n) for c in range(n) if g[r][c] == '.']
    def bt(i):
        if i == len(blanks): return True
        r, c = blanks[i]
        rowset = set(g[r]); colset = {g[k][c] for k in range(n)}
        for d in digits:
            if d in rowset or d in colset: continue
            g[r][c] = d
            if bt(i+1): return True
            g[r][c] = '.'
        return False
    if bt(0):
        return '/'.join(''.join(r) for r in g)
    return None

# ---------- DUOMASK : string matching both regexes ----------
def s_DUOMASK(clue, budget=0.008):
    a, b = clue.split()
    ra = re.compile(a + r'\Z'); rb = re.compile(b + r'\Z')
    end = time.perf_counter() + budget
    for L in range(0, 13):
        for m in range(1 << L):
            s = ''.join('ab'[(m >> i) & 1] for i in range(L))
            if ra.match(s) and rb.match(s):
                return s
        if time.perf_counter() > end:
            return None
    return None

# ---------- IDX : discrete log ----------
def s_IDX(clue):
    g, h, p = [int(x) for x in clue.split()]
    g %= p; h %= p
    m = int(math.isqrt(p)) + 1
    tbl = {}
    e = 1
    for j in range(m):
        if e not in tbl: tbl[e] = j
        e = e * g % p
    f = pow(g, p - 1 - m, p)
    y = h
    for i in range(m):
        j = tbl.get(y)
        if j is not None:
            return i * m + j
        y = y * f % p
    return None

# ---------- CHAKRA : Pell x^2 - N y^2 = 1 ----------
def s_CHAKRA(clue):
    N = int(clue)
    a0 = int(math.isqrt(N))
    if a0 * a0 == N: return None
    m, d, a = 0, 1, a0
    num1, num = 1, a0
    den1, den = 0, 1
    while num * num - N * den * den != 1:
        m = d * a - m
        d = (N - m * m) // d
        a = (a0 + m) // d
        num1, num = num, a * num + num1
        den1, den = den, a * den + den1
    return num, den

# ---------- SPQ : semiprime factoring ----------
def _rho(n):
    if n % 2 == 0: return 2
    import random as _r
    x = 2; y = 2; c = 1; d = 1
    while True:
        c += 1
        x = y = 2; d = 1
        while d == 1:
            x = (x*x + c) % n
            y = (y*y + c) % n; y = (y*y + c) % n
            d = math.gcd(abs(x-y), n)
        if d != n: return d

def s_SPQ(clue):
    n = int(clue)
    for p in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47):
        if n % p == 0: return (p, n // p)
    d = _rho(n)
    a, b = d, n // d
    return (min(a,b), max(a,b))

# ---------- MARIENBAD : nim ----------
def s_MARIENBAD(clue):
    p = [int(x) for x in clue.split()]
    x = 0
    for v in p: x ^= v
    if x == 0: 
        for i, v in enumerate(p):
            if v: return i, 1, [q - (1 if j==i else 0) for j,q in enumerate(p)]
        return None
    for i, v in enumerate(p):
        t = v ^ x
        if t < v:
            np = list(p); np[i] = t
            return i, v - t, np
    return None

# ---------- zebu ----------
def s_zebu(clue):
    cons = clue.split()
    letters = ['A','B','C','D','E']
    n = 5
    idx = {c: i for i, c in enumerate(letters)}
    parsed = []
    for t in cons:
        if '<' in t:
            a, b = t.split('<'); parsed.append(('<', idx[a], idx[b]))
        elif '|' in t:
            a, b = t.split('|'); parsed.append(('|', idx[a], idx[b]))
        elif '#' in t:
            a, v = t.split('#'); parsed.append(('#', idx[a], int(v)))
    for perm in permutations(range(1, n+1)):
        ok = True
        for k, a, b in parsed:
            if k == '<':
                if perm[a] >= perm[b]: ok = False; break
            elif k == '|':
                if abs(perm[a] - perm[b]) != 1: ok = False; break
            else:
                if perm[a] != b: ok = False; break
        if ok:
            return letters, perm
    return None

# ---------- ANAPAL : minimum window ----------
def s_ANAPAL(clue):
    s, t = clue.split('|')
    need = {}
    for ch in t: need[ch] = need.get(ch, 0) + 1
    miss = len(t); cnt = {}; l = 0; best = None
    for r, ch in enumerate(s):
        c = cnt.get(ch, 0)
        if need.get(ch, 0) > c: miss -= 1
        cnt[ch] = c + 1
        while miss == 0:
            if best is None or r - l < best[1] - best[0]:
                best = (l, r)
            lc = s[l]; cnt[lc] -= 1
            if cnt[lc] < need.get(lc, 0): miss += 1
            l += 1
    if best is None: return None
    return best[0], best[1], s[best[0]:best[1]+1]

# ---------- CRIBROT : caesar with crib ----------
def s_CRIBROT(clue):
    c, crib = clue.split('|')
    for k in range(26):
        d = ''.join(chr((ord(ch) - 97 + k) % 26 + 97) if 'a' <= ch <= 'z' else ch for ch in c)
        if crib in d:
            return k, d
    return None

# ---------- RUNIC : run length encoding ----------
def s_RUNIC(clue):
    runs = []
    prev = clue[0]; n = 1
    for ch in clue[1:]:
        if ch == prev: n += 1
        else: runs.append((prev, n)); prev = ch; n = 1
    runs.append((prev, n))
    return runs

# ---------- ALLWIN : de Bruijn sequence ----------
def s_ALLWIN(clue):
    alpha, n = clue.split(); n = int(n)
    k = len(alpha)
    a = [0] * (k * n)
    seq = []
    def db(t, p):
        if t > n:
            if n % p == 0:
                seq.extend(a[1:p+1])
        else:
            a[t] = a[t-p]
            db(t+1, p)
            for j in range(a[t-p]+1, k):
                a[t] = j
                db(t+1, t)
    db(1, 1)
    return ''.join(alpha[i] for i in seq)

# ---------- TWINE : LCS ----------
def s_TWINE(clue):
    a, b, k = clue.split('|')
    la, lb = len(a), len(b)
    dp = [[0]*(lb+1) for _ in range(la+1)]
    for i in range(la-1, -1, -1):
        ai = a[i]; di = dp[i]; dn = dp[i+1]
        for j in range(lb-1, -1, -1):
            di[j] = dn[j+1] + 1 if ai == b[j] else (dn[j] if dn[j] >= di[j+1] else di[j+1])
    out = []; i = j = 0
    while i < la and j < lb:
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        elif dp[i+1][j] >= dp[i][j+1]: i += 1
        else: j += 1
    return ''.join(out)

# ---------- HANSOM : taxicab tour of exact length ----------
def s_HANSOM(clue):
    pts_s, t = clue.split('|'); t = int(t)
    P = [tuple(int(v) for v in p.split(',')) for p in pts_s.split()]
    n = len(P)
    D = [[abs(P[i][0]-P[j][0]) + abs(P[i][1]-P[j][1]) for j in range(n)] for i in range(n)]
    size = 1 << n
    dp = [[0]*n for _ in range(size)]
    for i in range(n): dp[1 << i][i] = 1
    for mask in range(size):
        row = dp[mask]
        for last in range(n):
            v = row[last]
            if not v: continue
            if not (mask >> last) & 1: continue
            Dl = D[last]
            for nx in range(n):
                if (mask >> nx) & 1: continue
                dp[mask | (1 << nx)][nx] |= v << Dl[nx]
    full = size - 1
    for last in range(n):
        if (dp[full][last] >> t) & 1:
            # reconstruct
            order = [last]; mask = full; cur = t; cl = last
            while mask != (1 << cl):
                pm = mask ^ (1 << cl)
                for prev in range(n):
                    if not (pm >> prev) & 1: continue
                    d = D[prev][cl]
                    if d <= cur and (dp[pm][prev] >> (cur - d)) & 1:
                        cur -= d; mask = pm; cl = prev; order.append(prev)
                        break
                else:
                    return None
            order.reverse()
            return order, P
    return None

# ---------- GRAYLING : hypercube path of exact length ----------
def s_GRAYLING(clue, budget=0.006):
    a, b, k = clue.split(); k = int(k)
    n = len(a)
    A = int(a, 2); B = int(b, 2)
    end = time.perf_counter() + budget
    path = [A]; seen = {A}
    def hd(x, y): return bin(x ^ y).count('1')
    def bt(rem, cur):
        if time.perf_counter() > end: raise TimeoutError
        if rem == 0:
            return cur == B
        d = hd(cur, B)
        if d > rem or (rem - d) % 2: return False
        for i in range(n):
            nx = cur ^ (1 << i)
            if nx in seen: continue
            seen.add(nx); path.append(nx)
            if bt(rem-1, nx): return True
            path.pop(); seen.discard(nx)
        return False
    try:
        if bt(k, A):
            return [format(v, '0%db' % n) for v in path]
    except TimeoutError:
        return None
    return None

# ---------- regina : n-queens with blocked cells ----------
def s_regina(clue):
    G = clue.split('\n'); R = len(G); C = len(G[0])
    sol = []
    def bt(r, cols, d1, d2):
        if r == R: return True
        row = G[r]
        for c in range(C):
            if row[c] == 'X' or c in cols or (r-c) in d1 or (r+c) in d2: continue
            sol.append(c); cols.add(c); d1.add(r-c); d2.add(r+c)
            if bt(r+1, cols, d1, d2): return True
            sol.pop(); cols.discard(c); d1.discard(r-c); d2.discard(r+c)
        return False
    if bt(0, set(), set(), set()):
        return sol, G
    return None

# ---------- warren : maze ----------
def s_warren(clue):
    G = clue.split('\n'); R = len(G); C = max(len(r) for r in G)
    start = goal = None
    for r in range(R):
        for c in range(len(G[r])):
            if G[r][c] == 'S': start = (r, c)
            elif G[r][c] == 'E': goal = (r, c)
    if start is None or goal is None: return None
    from collections import deque
    prev = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == goal: break
        r, c = cur
        for dr, dc, ch in ((-1,0,'U'),(1,0,'D'),(0,-1,'L'),(0,1,'R')):
            a, b = r+dr, c+dc
            if 0 <= a < R and 0 <= b < len(G[a]) and G[a][b] != '#' and (a,b) not in prev:
                prev[(a,b)] = (cur, ch); q.append((a,b))
    if goal not in prev: return None
    out = []; cur = goal
    while prev[cur] is not None:
        p, ch = prev[cur]; out.append(ch); cur = p
    out.reverse()
    return ''.join(out)

# ---------- hanjie : nonogram ----------
def _lines(clue_part):
    return [[int(x) for x in grp.split(',') if x != ''] for grp in clue_part.split('/')]

def _row_options(clue, width):
    res = []
    def rec(i, pos, cur):
        if i == len(clue):
            res.append(cur + [0]*(width-len(cur)))
            return
        need = sum(clue[i:]) + (len(clue)-i-1)
        for s in range(pos, width - need + 1):
            nc = cur + [0]*(s-len(cur)) + [1]*clue[i]
            if len(nc) > width: break
            rec(i+1, len(nc)+1, nc)
    rec(0, 0, [])
    return res

def s_hanjie(clue, budget=0.012):
    rp, cp = clue.split('\n')
    rows = _lines(rp); cols = _lines(cp)
    R = len(rows); C = len(cols)
    opts = [_row_options(r, C) for r in rows]
    csum = [sum(cc) + len(cc) - 1 if cc else 0 for cc in cols]
    end_t = time.perf_counter() + budget
    sol = [None]*R
    def bt(r, states):
        if time.perf_counter() > end_t: raise TimeoutError
        if r == R:
            for c in range(C):
                k, n = states[c]
                cc = cols[c]
                if n:
                    if k >= len(cc) or n != cc[k] or k + 1 != len(cc): return False
                else:
                    if k != len(cc): return False
            return True
        rem = R - r - 1
        for o in opts[r]:
            ns = []
            ok = True
            for c in range(C):
                k, n = states[c]
                cc = cols[c]
                if o[c]:
                    n += 1
                    if k >= len(cc) or n > cc[k]: ok = False; break
                else:
                    if n:
                        if n != cc[k]: ok = False; break
                        k += 1; n = 0
                if n:
                    need = (cc[k] - n) + sum(cc[k+1:]) + (len(cc) - k - 1)
                elif k < len(cc):
                    need = sum(cc[k:]) + (len(cc) - k - 1)
                else:
                    need = 0
                if need > rem: ok = False; break
                ns.append((k, n))
            if ok:
                sol[r] = o
                if bt(r+1, ns): return True
        return False
    try:
        if bt(0, [(0,0)]*C):
            return [''.join('#' if v else '.' for v in row) for row in sol]
    except TimeoutError:
        return None
    return None

# ---------- TOPPLE : 24-game ----------
def s_TOPPLE(clue, budget=0.008):
    lhs, rhs = clue.split('=')
    ds = [int(c) for c in lhs]; t = int(rhs)
    end_t = time.perf_counter() + budget
    def go(vals, exprs):
        if time.perf_counter() > end_t: raise TimeoutError
        L = len(vals)
        if L == 1:
            return exprs[0] if vals[0] == t else None
        for i in range(L):
            for j in range(i+1, L):
                rv = [vals[k] for k in range(L) if k != i and k != j]
                re_ = [exprs[k] for k in range(L) if k != i and k != j]
                a, b = vals[i], vals[j]; sa, sb = exprs[i], exprs[j]
                cands = [(a+b, '('+sa+'+'+sb+')'), (a*b, '('+sa+'*'+sb+')'),
                         (a-b, '('+sa+'-'+sb+')'), (b-a, '('+sb+'-'+sa+')')]
                if b and a % b == 0: cands.append((a//b, '('+sa+'/'+sb+')'))
                if a and b % a == 0: cands.append((b//a, '('+sb+'/'+sa+')'))
                for v, e in cands:
                    r = go(rv+[v], re_+[e])
                    if r: return r
        return None
    try:
        return go(ds, [str(d) for d in ds])
    except TimeoutError:
        return None

# ---------- AHMES : egyptian fractions (greedy) ----------
def s_AHMES(clue, maxterms=12):
    a, b = clue.split('/'); a = int(a); b = int(b)
    g = math.gcd(a, b); a //= g; b //= g
    out = []
    while a and len(out) < maxterms:
        if b % a == 0:
            out.append(b // a); a = 0; break
        q = -(-b // a)
        out.append(q)
        a, b = a * q - b, b * q
        g = math.gcd(a, b)
        if g > 1: a //= g; b //= g
    return out if a == 0 else None

# ---------- erewhon : grid transforms ----------
def s_erewhon(clue, v=0):
    G = clue.split('\n')
    if v == 0: return clue[::-1]
    if v == 1: return '\n'.join(reversed(G))
    if v == 2: return '\n'.join(r[::-1] for r in G)
    if v == 3: return '\n'.join(''.join(c) for c in zip(*G))
    if v == 4: return '\n'.join(''.join(c) for c in zip(*G[::-1]))
    if v == 5: return '\n'.join(''.join(c) for c in list(zip(*G))[::-1])
    return clue

# ---------- ANAPAL v2 : anagram palindrome with given prefix ----------
def s_ANAPAL2(clue):
    s, t = clue.split('|')
    n = len(s); m = len(t)
    cnt = {}
    for ch in s: cnt[ch] = cnt.get(ch, 0) + 1
    half = n // 2
    for start in range(n - m + 1):
        res = [None] * n
        ok = True
        for i, ch in enumerate(t):
            for pos in (start + i, n - 1 - start - i):
                if res[pos] is None: res[pos] = ch
                elif res[pos] != ch: ok = False; break
            if not ok: break
        if not ok: continue
        used = {}
        for x in res:
            if x is not None: used[x] = used.get(x, 0) + 1
        rem = {}
        bad = False
        for ch, c in cnt.items():
            d = c - used.get(ch, 0)
            if d < 0: bad = True; break
            if d: rem[ch] = d
        if bad: continue
        for ch in used:
            if ch not in cnt: bad = True; break
        if bad: continue
        mid_free = (n % 2 == 1 and res[half] is None)
        odd = [c for c, v in rem.items() if v % 2]
        if mid_free:
            if len(odd) != 1: continue
        elif odd:
            continue
        if mid_free:
            c = odd[0]; res[half] = c
            rem[c] -= 1
            if rem[c] == 0: del rem[c]
        keys = [c for c in rem]
        ki = 0
        for i in range(half):
            if res[i] is not None: continue
            while ki < len(keys) and rem.get(keys[ki], 0) < 2: ki += 1
            if ki >= len(keys): ok = False; break
            c = keys[ki]
            res[i] = c; res[n-1-i] = c; rem[c] -= 2
        if not ok or any(x is None for x in res): continue
        return ''.join(res)
    return None

# ---------- PP v2 : shortest palindromic supersequence ----------
def s_PP2(clue):
    s = clue; n = len(s)
    if n <= 1: return s
    dp = [[0]*n for _ in range(n)]
    for i in range(n-2, -1, -1):
        for j in range(i+1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] if j > i+1 else 0
            else:
                a = dp[i+1][j]; b = dp[i][j-1]
                dp[i][j] = (a if a < b else b) + 1
    left = []; right = []
    i, j = 0, n-1
    while i < j:
        if s[i] == s[j]:
            left.append(s[i]); right.append(s[j]); i += 1; j -= 1
        elif dp[i+1][j] <= dp[i][j-1]:
            left.append(s[i]); right.append(s[i]); i += 1
        else:
            left.append(s[j]); right.append(s[j]); j -= 1
    mid = s[i] if i == j else ''
    return ''.join(left) + mid + ''.join(reversed(right))

# ---------- life ----------
def s_life(clue, torus=False):
    G = clue.split('\n'); R = len(G); C = len(G[0])
    out = []
    for r in range(R):
        row = []
        for c in range(C):
            n = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0: continue
                    a, b = r+dr, c+dc
                    if torus: a %= R; b %= C
                    elif not (0 <= a < R and 0 <= b < C): continue
                    if G[a][b] == '#': n += 1
            alive = G[r][c] == '#'
            row.append('#' if (n == 3 or (alive and n == 2)) else '.')
        out.append(''.join(row))
    return '\n'.join(out)

def s_regina_count(clue):
    G = clue.split('\n'); R = len(G); C = len(G[0])
    total = [0]
    def bt(r, cols, d1, d2):
        if r == R: total[0] += 1; return
        row = G[r]
        for c in range(C):
            if row[c] == 'X' or c in cols or (r-c) in d1 or (r+c) in d2: continue
            cols.add(c); d1.add(r-c); d2.add(r+c)
            bt(r+1, cols, d1, d2)
            cols.discard(c); d1.discard(r-c); d2.discard(r+c)
    bt(0, set(), set(), set())
    return total[0]

# ---------- PP v3 : smallest palindromic prime containing clue ----------
_SMALL_P = (2,3,5,7,11,13,17,19,23,29,31,37)
def _isprime(n):
    if n < 2: return False
    for p in _SMALL_P:
        if n % p == 0: return n == p
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in _SMALL_P:
        x = pow(a, d, n)
        if x == 1 or x == n-1: continue
        for _ in range(r-1):
            x = x * x % n
            if x == n-1: break
        else:
            return False
    return True

from itertools import product as _product

def s_PP3(clue, budget=0.010):
    m = len(clue)
    end_t = time.perf_counter() + budget
    if m == 1 and _isprime(int(clue)): return clue
    if clue == '11': return '11'
    L = m if m % 2 else m + 1
    while L <= m + 8:
        h = (L + 1) // 2
        best = None
        for p in range(L - m + 1):
            d = [None] * L
            ok = True
            for i, ch in enumerate(clue):
                for pos in (p + i, L - 1 - p - i):
                    if d[pos] is None: d[pos] = ch
                    elif d[pos] != ch: ok = False; break
                if not ok: break
            if not ok: continue
            free = [i for i in range(h) if d[i] is None]
            for combo in _product('0123456789', repeat=len(free)):
                if time.perf_counter() > end_t: return None
                for i, c in zip(free, combo): d[i] = c
                if d[0] == '0': continue
                half = d[:h]
                full = ''.join(half) + ''.join(reversed(half[:L // 2]))
                v = int(full)
                if _isprime(v):
                    if best is None or v < best: best = v
                    break
        if best is not None:
            return str(best)
        L += 2
    return None

# ---------- HAIL : smallest n with exactly k collatz steps ----------
_HAILTAB = {}
def build_hail(limit=200000):
    if _HAILTAB: return _HAILTAB
    st = [0] * (limit + 1)
    for n in range(2, limit + 1):
        m = n; c = 0
        while m >= n:
            m = m // 2 if m % 2 == 0 else 3 * m + 1
            c += 1
        c += st[m] if m <= limit else 0
        st[n] = c
        if c not in _HAILTAB: _HAILTAB[c] = n
    _HAILTAB[0] = 1
    return _HAILTAB

# ---------- erewhon : Game-of-Life predecessor ----------
_LF = {}
def build_life(C=6):
    if C in _LF: return _LF[C]
    N = 1 << C
    cnt3 = [[0]*C for _ in range(N)]
    for x in range(N):
        for j in range(C):
            v = 0
            for k in (j-1, j, j+1):
                if 0 <= k < C and (x >> k) & 1: v += 1
            cnt3[x][j] = v
    cmask = [[0]*4 for _ in range(C)]
    for j in range(C):
        for x in range(N):
            cmask[j][cnt3[x][j]] |= 1 << x
    # M[j][bj][base][tj]
    M = [[[[0, 0] for _ in range(8)] for _ in range(2)] for _ in range(C)]
    for j in range(C):
        for bj in (0, 1):
            for base in range(8):
                for tj in (0, 1):
                    m = 0
                    for v in range(4):
                        tot = base + v
                        alive = 1 if (tot == 3 or (bj and tot == 2)) else 0
                        if alive == tj: m |= cmask[j][v]
                    M[j][bj][base][tj] = m
    _LF[C] = (cnt3, M, N)
    return _LF[C]

def s_erewhon(clue, budget=0.012):
    G = clue.split('\n')
    R = len(G); C = len(G[0])
    if C > 8: return None
    cnt3, M, N = build_life(C)
    tgt = [sum(1 << j for j in range(C) if G[r][j] == '#') for r in range(R)]
    full = N - 1
    def allowed(a, b, t):
        m = (1 << N) - 1
        ca = cnt3[a]; cb = cnt3[b]
        for j in range(C):
            bj = (b >> j) & 1
            m &= M[j][bj][ca[j] + cb[j] - bj][(t >> j) & 1]
            if not m: return 0
        return m
    end_t = time.perf_counter() + budget
    rows = [0] * R
    def bits(m):
        while m:
            low = m & -m
            yield low.bit_length() - 1
            m ^= low
    def dfs(r, a, b):
        if time.perf_counter() > end_t: raise TimeoutError
        if r == R:
            return (allowed(a, b, tgt[R-1]) >> 0) & 1 == 1
        m = allowed(a, b, tgt[r-1])
        for c in bits(m):
            rows[r] = c
            if dfs(r+1, b, c): return True
        return False
    try:
        for r0 in range(N):
            rows[0] = r0
            if dfs(1, 0, r0):
                return '\n'.join(''.join('#' if (rows[r] >> j) & 1 else '.' for j in range(C)) for r in range(R))
    except TimeoutError:
        return None
    return None

# ---------- regina v2 : n-queens, one per column, avoiding X ----------
def s_regina2(clue):
    G = clue.split('\n'); R = len(G); C = len(G[0])
    sol = [0] * C
    def bt(c, rows, d1, d2):
        if c == C: return True
        for r in range(R):
            if G[r][c] == 'X': continue
            if r in rows or (r - c) in d1 or (r + c) in d2: continue
            sol[c] = r; rows.add(r); d1.add(r - c); d2.add(r + c)
            if bt(c + 1, rows, d1, d2): return True
            rows.discard(r); d1.discard(r - c); d2.discard(r + c)
        return False
    if bt(0, set(), set(), set()):
        return ''.join(str(r) for r in sol)
    return None

# ---------- ikos v2 : hamiltonian cycle, warnsdorff + pruning ----------
def s_ikos2(clue, budget=0.020):
    parts = clue.split()
    n = int(parts[0])
    adjm = [0] * n
    for p in parts[1:]:
        a, b = p.split('-'); a = int(a); b = int(b)
        adjm[a] |= 1 << b; adjm[b] |= 1 << a
    end_t = time.perf_counter() + budget
    full = (1 << n) - 1
    path = [0] * n
    start = 0
    def bt(d, cur, visited):
        if time.perf_counter() > end_t: raise TimeoutError
        if d == n:
            return (adjm[cur] >> start) & 1 == 1
        rem = full & ~visited
        cand = adjm[cur] & rem
        if not cand: return False
        # prune: every remaining vertex needs >=1 unvisited neighbour (or be adj to start)
        m = rem
        while m:
            low = m & -m; v = low.bit_length() - 1; m ^= low
            av = adjm[v] & (rem | (1 << cur) | (1 << start))
            if av == 0: return False
            if av & (av - 1) == 0 and v != cur:
                pass
        order = []
        m = cand
        while m:
            low = m & -m; v = low.bit_length() - 1; m ^= low
            order.append((bin(adjm[v] & rem).count('1'), v))
        order.sort()
        for _, v in order:
            path[d] = v
            if bt(d + 1, v, visited | (1 << v)): return True
        return False
    try:
        if bt(1, start, 1 << start):
            return ' '.join(str(x) for x in path)
    except TimeoutError:
        return None
    return None

# ---------- ikos v3 : hamiltonian path ----------
def s_ikos3(clue, budget=0.020):
    parts = clue.split()
    n = int(parts[0])
    adjm = [0] * n
    for p in parts[1:]:
        a, b = p.split('-'); a = int(a); b = int(b)
        adjm[a] |= 1 << b; adjm[b] |= 1 << a
    end_t = time.perf_counter() + budget
    full = (1 << n) - 1
    path = [0] * n
    def bt(d, cur, visited):
        if time.perf_counter() > end_t: raise TimeoutError
        if d == n: return True
        rem = full & ~visited
        cand = adjm[cur] & rem
        if not cand: return False
        order = []
        m = cand
        while m:
            low = m & -m; v = low.bit_length() - 1; m ^= low
            order.append((bin(adjm[v] & rem).count('1'), v))
        order.sort()
        for _, v in order:
            path[d] = v
            if bt(d + 1, v, visited | (1 << v)): return True
        return False
    try:
        starts = sorted(range(n), key=lambda v: bin(adjm[v]).count('1'))
        for s0 in starts:
            path[0] = s0
            if bt(1, s0, 1 << s0):
                return ' '.join(str(x) for x in path)
    except TimeoutError:
        return None
    return None

# ---------- HANSOM v2 : taxicab tour, exact length if possible else minimal ----------
def s_HANSOM2(clue):
    pts_s, t = clue.split('|'); t = int(t)
    P = [tuple(int(v) for v in p.split(',')) for p in pts_s.split()]
    n = len(P)
    if n == 1: return "0"
    if n > 10: return None
    D = [[abs(P[i][0]-P[j][0]) + abs(P[i][1]-P[j][1]) for j in range(n)] for i in range(n)]
    size = 1 << n
    # bitset DP of achievable lengths, start fixed at 0
    dp = [[0]*n for _ in range(size)]
    dp[1][0] = 1
    for mask in range(size):
        if not mask & 1: continue
        row = dp[mask]
        for last in range(n):
            v = row[last]
            if not v: continue
            Dl = D[last]
            for nx in range(n):
                if (mask >> nx) & 1: continue
                dp[mask | (1 << nx)][nx] |= v << Dl[nx]
    full = size - 1
    # try exact cycle length t
    for last in range(1, n):
        d = D[last][0]
        if d <= t and (dp[full][last] >> (t - d)) & 1:
            order = [last]; mask = full; cur = t - d; cl = last
            while mask != 1:
                pm = mask ^ (1 << cl)
                for prev in range(n):
                    if not (pm >> prev) & 1: continue
                    dd = D[prev][cl]
                    if dd <= cur and (dp[pm][prev] >> (cur - dd)) & 1:
                        cur -= dd; mask = pm; cl = prev; order.append(prev); break
                else:
                    return None
            order.reverse()
            return ' '.join(str(i) for i in order)
    # fallback: minimum cycle
    INF = float('inf')
    md = [[INF]*n for _ in range(size)]
    md[1][0] = 0
    par = [[-1]*n for _ in range(size)]
    for mask in range(size):
        if not mask & 1: continue
        for last in range(n):
            c = md[mask][last]
            if c == INF: continue
            for nx in range(n):
                if (mask >> nx) & 1: continue
                nm = mask | (1 << nx); nc = c + D[last][nx]
                if nc < md[nm][nx]:
                    md[nm][nx] = nc; par[nm][nx] = last
    best = INF; bl = -1
    for last in range(1, n):
        c = md[full][last] + D[last][0]
        if c < best: best = c; bl = last
    if bl < 0: return None
    order = []; mask = full; cl = bl
    while cl != -1:
        order.append(cl); p = par[mask][cl]; mask ^= (1 << cl); cl = p
    order.reverse()
    return ' '.join(str(i) for i in order)

# ---------- TOPPLE v2 : RPN expression from the digits hitting the target ----------
def s_TOPPLE2(clue, budget=0.010, allow_div=False):
    lhs, rhs = clue.split('=')
    ds = [int(c) for c in lhs]; t = int(rhs)
    end_t = time.perf_counter() + budget
    def go(vals, exprs):
        if time.perf_counter() > end_t: raise TimeoutError
        L = len(vals)
        if L == 1:
            return exprs[0] if vals[0] == t else None
        for i in range(L):
            for j in range(i+1, L):
                rv = [vals[k] for k in range(L) if k != i and k != j]
                re_ = [exprs[k] for k in range(L) if k != i and k != j]
                a, b = vals[i], vals[j]; sa, sb = exprs[i], exprs[j]
                cands = [(a+b, sa+sb+'+'), (a*b, sa+sb+'*'),
                         (a-b, sa+sb+'-'), (b-a, sb+sa+'-')]
                if allow_div:
                    if b and a % b == 0: cands.append((a//b, sa+sb+'/'))
                    if a and b % a == 0: cands.append((b//a, sb+sa+'/'))
                for v, e in cands:
                    r = go(rv+[v], re_+[e])
                    if r: return r
        return None
    try:
        return go(ds, [str(d) for d in ds])
    except TimeoutError:
        return None

# ---------- LegoZendo : build a brick wall whose <letter> bricks total N studs ----------
_LZ_POOL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def s_LegoZendo(clue):
    L = clue[0]
    N = int(clue[1:])
    others = [c for c in _LZ_POOL if c != L]
    o = iter(others)
    def brick(ch, x, n):
        return (ch, x, n)
    if N == 0:
        W = 7
        levels = [[brick(next(o), 1, 1)],
                  [brick(next(o), 0, 1), brick(L, 3, 1)],
                  [brick(next(o), 4, 1)]]
    elif N == 1:
        W = 7
        levels = [[brick(next(o), 1, 1)],
                  [brick(next(o), 0, 1), brick(L, 3, 1)],
                  [brick(next(o), 4, 1)]]
    elif N <= 3:
        W = 3 * N + 1
        levels = [[brick(next(o), 1, 1)],
                  [brick(L, 0, N)],
                  [brick(next(o), 3 * N - 3, 1)]]
    else:
        a = (N + 1) // 2; b = N - a
        W = 3 * a + 1
        levels = [[brick(next(o), 1, 1)],
                  [brick(L, 1, a)],
                  [brick(L, 0, b)],
                  [brick(next(o), 3 * b - 3, 1)]]
    out = []
    for lv in levels:
        row = ['.'] * W
        for ch, x, n in lv:
            for k in range(x, x + 3 * n):
                row[k] = ch
        s = ''.join(row)
        out.append(s); out.append(s)
    return '\n'.join(out)

# ============================ DISPATCH ============================
_CNT = {}
UNKNOWN = ("LegoZendo",)

def _v(name, k):
    i = _CNT.get(name, 0)
    _CNT[name] = i + 1
    return i % k

def on_round_start(memory):
    _CNT.clear()
    build_hail(500000)
    for _c in (4, 5, 6, 7, 8): build_life(_c)
    memory["probe"] = []
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1

def on_round_end(items, memory):
    probe = {x[0]: x[1] for x in memory.get("probe", [])}
    tally = {}; hits = {}
    for it in items:
        n = it.get("name"); sc = it.get("score", 0)
        h = hits.setdefault(n, [0, 0]); h[1] += 1; h[0] += sc
        v = probe.get(it.get("index"))
        if v is None: continue
        e = tally.setdefault(n, {}).setdefault(str(v), [0, 0])
        e[1] += 1; e[0] += sc
    memory["probe_summary"] = tally
    memory["hits"] = hits
    memory["probe"] = []


def solve(name, clue, memory):
    try:
        return _solve(name, clue, memory)
    except Exception:
        return None


def _solve(name, clue, memory):
    if name == "PP":          return s_PP3(clue)
    if name == "ANAPAL":      return s_ANAPAL2(clue)
    if name == "HAIL":        return str(_HAILTAB.get(int(clue), 1))
    if name == "erewhon":     return s_erewhon(clue, 0.015)
    if name == "skerry":      return str(s_skerry(clue))
    if name == "SUNZI":       return s_SUNZI(clue)
    if name == "BASILISK":    return s_BASILISK(clue)
    if name == "DUOMASK":     return s_DUOMASK(clue)
    if name == "TWINE":       return s_TWINE(clue)
    if name == "volute":      return s_volute(clue)
    if name == "carre":       return s_carre(clue)
    if name == "warren":      return s_warren(clue)
    if name == "ALLWIN":      return s_ALLWIN(clue)
    if name == "TARE":
        r = s_TARE(clue)
        if r is None: return None
        cs = set(r[0])
        return ''.join('1' if i in cs else '0' for i in range(len(r[1])))
    if name == "AHMES":
        d = s_AHMES(clue)
        return None if d is None else ' '.join(str(x) for x in d)
    if name == "CRIBROT":
        r = s_CRIBROT(clue)
        return None if r is None else r[1]
    if name == "CHAKRA":
        r = s_CHAKRA(clue)
        return None if r is None else '%d %d' % r
    if name == "SPQ":         return str(s_SPQ(clue)[0])
    if name == "IDX":
        r = s_IDX(clue); return None if r is None else str(r)
    if name == "RUNIC":
        return ''.join('%d%s' % (n, c) for c, n in s_RUNIC(clue))
    if name == "MARIENBAD":
        r = s_MARIENBAD(clue)
        return None if r is None else ' '.join(str(x) for x in r[2])
    if name == "wolf":        return format(s_wolf(clue), '08b')
    if name == "krom":
        a = s_krom(clue)
        return None if a is None else ''.join(str(b) for b in a)
    if name == "trico":
        c = s_trico(clue)
        return None if c is None else ''.join(str(x) for x in c)
    if name == "ikos":        return s_ikos3(clue, 0.020)
    if name == "regina":      return s_regina2(clue)
    if name == "TOPPLE":      return s_TOPPLE2(clue, 0.015)
    if name == "LegoZendo":   return s_LegoZendo(clue)
    if name == "HANSOM":
        r = s_HANSOM2(clue)
        if r is None: return None
        pts_s, t = clue.split('|'); t = int(t)
        P = [tuple(int(v) for v in q.split(',')) for q in pts_s.split()]
        o = [int(x) for x in r.split()]
        L = sum(abs(P[o[i]][0]-P[o[(i+1) % len(o)]][0]) + abs(P[o[i]][1]-P[o[(i+1) % len(o)]][1]) for i in range(len(o)))
        return r
    if name == "hanjie":
        g = s_hanjie(clue, 0.020)
        return None if g is None else '\n'.join(g)
    if name == "GRAYLING":
        p = s_GRAYLING(clue, 0.012)
        return None if p is None else ' '.join(p)
    if name == "zebu":
        r = s_zebu(clue)
        if r is None: return None
        letters, perm = r
        order = [None] * len(perm)
        for i, pos in enumerate(perm): order[pos-1] = letters[i]
        return ''.join(order)
    return None
