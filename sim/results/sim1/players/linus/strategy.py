import re, time, itertools, math, random
from functools import lru_cache

DEADLINE = [0.0]
def tleft():
    return DEADLINE[0] - time.perf_counter()

# ---------- helpers ----------
def to_base(n, b):
    if n == 0: return "0"
    digs = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = []
    while n:
        out.append(digs[n % b]); n //= b
    return "".join(reversed(out))

# ---------- AHMES : egyptian fractions ----------
def s_AHMES(clue):
    a, b = clue.split("/"); a = int(a); b = int(b)
    parts = []
    while a and len(parts) < 12:
        d = -(-b // a)
        parts.append(str(d))
        a, b = a * d - b, b * d
        g = math.gcd(a, b) or 1
        a //= g; b //= g
    return " ".join(parts)

# ---------- BASILISK : base conversion ----------
def s_BASILISK(clue):
    num, bases = clue.split(":")
    fr, to = bases.split(">")
    return to_base(int(num, int(fr)), int(to))

# ---------- CHAKRA : Pell x^2 - N y^2 = 1 ----------
def s_CHAKRA(clue):
    N = int(clue)
    a0 = int(math.isqrt(N))
    if a0 * a0 == N: return ""
    m, d, a = 0, 1, a0
    num1, num = 1, a0
    den1, den = 0, 1
    while num * num - N * den * den != 1:
        m = d * a - m
        d = (N - m * m) // d
        a = (a0 + m) // d
        num1, num = num, a * num + num1
        den1, den = den, a * den + den1
    return "%d %d" % (num, den)

# ---------- CRIBROT : caesar with crib ----------
def s_CRIBROT(clue):
    ct, crib = clue.split("|")
    for k in range(26):
        pt = "".join(chr((ord(c) - 97 + k) % 26 + 97) for c in ct)
        if crib in pt: return pt
    return ""

# ---------- DUOMASK : string matching both regexes ----------
def s_DUOMASK(clue):
    p1, p2 = clue.split(" ")
    r1 = re.compile(p1 + r"\Z").match; r2 = re.compile(p2 + r"\Z").match
    for L in range(0, 17):
        if tleft() < 0.002: break
        for bits in range(1 << L):
            s = "".join("ab"[(bits >> i) & 1] for i in range(L))
            if r1(s) and r2(s): return s
    return ""

# ---------- GRAYLING : hypercube path of exact length ----------
def s_GRAYLING(clue):
    a, b, n = clue.split()
    n = int(n); L = len(a)
    A = int(a, 2); B = int(b, 2)
    path = [A]; seen = {A}
    def dfs(cur, steps):
        if steps == 0: return cur == B
        d = bin(cur ^ B).count("1")
        if d > steps or (steps - d) & 1: return False
        for i in range(L):
            nxt = cur ^ (1 << i)
            if nxt in seen: continue
            seen.add(nxt); path.append(nxt)
            if dfs(nxt, steps - 1): return True
            seen.discard(nxt); path.pop()
        return False
    if not dfs(A, n): return ""
    f = "0%db" % L
    return " ".join(format(v, f) for v in path)

# ---------- HAIL : collatz ----------
_HAILMAP = {}
_HAILMAP = {}
def s_HAIL(clue):
    if not _HAILMAP:
        memo = {1: 0}
        for cand in range(1, 30000):
            x = cand; st = []
            while x not in memo:
                st.append(x); x = 3*x+1 if x & 1 else x >> 1
            v = memo[x]
            while st:
                y = st.pop(); v += 1; memo[y] = v
            t = memo[cand]
            if t not in _HAILMAP: _HAILMAP[t] = cand
    return str(_HAILMAP.get(int(clue), ""))

# ---------- HANSOM : taxicab tour ----------
def s_HANSOM(clue):
    pts, k = clue.split("|")
    P = [tuple(map(int, p.split(","))) for p in pts.split()]
    n = len(P)
    d = [[abs(P[i][0]-P[j][0])+abs(P[i][1]-P[j][1]) for j in range(n)] for i in range(n)]
    best = None; bestv = None
    if n <= 8:
        rng = range(1, n)
        for perm in itertools.permutations(rng):
            v = d[0][perm[0]]
            prev = perm[0]
            for x in perm[1:]:
                v += d[prev][x]; prev = x
            v += d[prev][0]
            if bestv is None or v < bestv: bestv = v; best = perm
        return "0 " + " ".join(map(str, best))
    o = list(range(n))
    improved = True
    while improved and tleft() > 0.003:
        improved = False
        for i in range(1, n-1):
            for j in range(i+1, n):
                a, b_, c, dd = o[i-1], o[i], o[j], o[(j+1) % n]
                if d[a][b_]+d[c][dd] > d[a][c]+d[b_][dd]:
                    o[i:j+1] = o[i:j+1][::-1]; improved = True
    return " ".join(map(str, o))

# ---------- MARIENBAD : nim ----------
def s_MARIENBAD(clue):
    h = [int(x) for x in clue.split()]
    x = 0
    for v in h: x ^= v
    if x == 0:
        for i, v in enumerate(h):
            if v > 0:
                h[i] -= 1; return " ".join(map(str, h))
        return ""
    for i, v in enumerate(h):
        t = v ^ x
        if t < v:
            h[i] = t; return " ".join(map(str, h))
    return ""

# ---------- RUNIC : run length encoding ----------
def s_RUNIC(clue):
    out = []; ch = clue[0]; c = 0
    for x in clue:
        if x == ch: c += 1
        else: out.append("%d%s" % (c, ch)); ch = x; c = 1
    out.append("%d%s" % (c, ch))
    return "".join(out)

# ---------- SPQ : semiprime factorisation ----------
def _rho(n):
    if n % 2 == 0: return 2
    while True:
        c = random.randrange(1, n); x = random.randrange(0, n); y = x; d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n; y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n: return d

def _isprime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True

def s_SPQ(clue):
    n = int(clue)
    for p in (2,3,5,7,11,13):
        if n % p == 0: return str(p)
    if _isprime(n): return str(n)
    d = _rho(n)
    while not _isprime(d): d = _rho(d)
    e = n // d
    if not _isprime(e):
        f = _rho(e)
        while not _isprime(f): f = _rho(f)
        d = min(d, f)
    return str(min(d, n // d))

# ---------- SUNZI : CRT ----------
def s_SUNZI(clue):
    x = 0; M = 1
    for t in clue.split():
        a, m = t.split("%"); a = int(a); m = int(m)
        inv = pow(M % m, -1, m)
        x = x + M * (((a - x) % m) * inv % m)
        M *= m
        x %= M
    return str(x % M)

# ---------- TARE : subset sum ----------
def s_TARE(clue):
    vals, t = clue.split("|"); t = int(t)
    V = [int(x) for x in vals.split()]
    n = len(V)
    reach = {0: 0}
    for i, v in enumerate(V):
        add = {}
        for s, m in reach.items():
            ns = s + v
            if ns <= t and ns not in reach and ns not in add:
                add[ns] = m | (1 << i)
        reach.update(add)
        if t in reach: break
    m = reach.get(t)
    if m is None: return ""
    return "".join("1" if (m >> i) & 1 else "0" for i in range(n))

# ---------- TWINE : LCS ----------
def s_TWINE(clue):
    a, b, k = clue.split("|")
    la, lb = len(a), len(b)
    dp = [[0]*(lb+1) for _ in range(la+1)]
    for i in range(la-1, -1, -1):
        di = dp[i]; dn = dp[i+1]; ai = a[i]
        for j in range(lb-1, -1, -1):
            di[j] = dn[j+1]+1 if ai == b[j] else (dn[j] if dn[j] >= di[j+1] else di[j+1])
    out = []; i = j = 0
    while i < la and j < lb:
        if a[i] == b[j]: out.append(a[i]); i += 1; j += 1
        elif dp[i+1][j] >= dp[i][j+1]: i += 1
        else: j += 1
    return "".join(out)

# ---------- carre : latin square ----------
def s_carre(clue):
    rows = [list(r) for r in clue.split("/")]
    n = len(rows)
    syms = [str(i+1) for i in range(n)]
    cells = [(r, c) for r in range(n) for c in range(n) if rows[r][c] == "."]
    def dfs(k):
        if k == len(cells): return True
        r, c = cells[k]
        used = set(rows[r])
        for i in range(n): used.add(rows[i][c])
        for s in syms:
            if s in used: continue
            rows[r][c] = s
            if dfs(k+1): return True
            rows[r][c] = "."
        return False
    if not dfs(0): return ""
    return "/".join("".join(r) for r in rows)

# ---------- erewhon ----------
_LIFE = {}
def _life_prep(W):
    if W in _LIFE: return _LIFE[W]
    N = 1 << W
    A3 = []
    for v in range(N):
        A3.append(tuple(((v >> (j-1)) & 1 if j > 0 else 0) + ((v >> j) & 1) +
                        ((v >> (j+1)) & 1 if j < W-1 else 0) for j in range(W)))
    CM = [[0]*4 for _ in range(W)]
    for j in range(W):
        for c in range(N):
            k = A3[c][j]
            if k < 4: CM[j][k] |= (1 << c)
    U = {}
    for j in range(W):
        for base in range(7):
            for bj in (0, 1):
                for t in (0, 1):
                    m = 0
                    for k in range(4):
                        n = base + k
                        live = 1 if (n == 3 or (n == 2 and bj)) else 0
                        if live == t: m |= CM[j][k]
                    U[(j, base, bj, t)] = m
    _LIFE[W] = (A3, U, N)
    return _LIFE[W]

def s_erewhon(clue):
    g = clue.split("\n")
    R = len(g); W = len(g[0])
    if W > 8: return ""
    A3, U, N = _life_prep(W)
    target = [sum(1 << j for j in range(W) if g[r][j] == "#") for r in range(R)]
    full = (1 << W) - 1
    def allowed(a, b, t):
        a3 = A3[a]; b3 = A3[b]
        m = -1
        for j in range(W):
            base = a3[j] + b3[j] - ((b >> j) & 1)
            m &= U[(j, base, (b >> j) & 1, (t >> j) & 1)]
            if not m: return 0
        return m
    fail = set()
    res = [0]*R
    def dfs(r, a, b):
        # rows 0..r-1 fixed as ..a,b ; b is row r ; choose row r+1
        if tleft() < 0.002: return False
        key = (r, a, b)
        if key in fail: return False
        m = allowed(a, b, target[r])
        if r == R-1:
            if m & 1:
                return True
            fail.add(key); return False
        c = m
        while c:
            low = c & -c
            v = low.bit_length() - 1
            res[r+1] = v
            if dfs(r+1, b, v): return True
            c ^= low
        fail.add(key); return False
    for r0 in range(N):
        res[0] = r0
        if dfs(0, 0, r0):
            out = ["".join("#" if (res[r] >> j) & 1 else "." for j in range(W))
                   for r in range(R)]
            return "\n".join(out)
    return ""

# ---------- hanjie : nonogram ----------
def _lines(clue_part):
    out = []
    for t in clue_part.split("/"):
        t = t.strip()
        out.append([int(x) for x in t.split(",")] if t else [])
    return out

def _patterns(clue, n):
    res = []
    if not clue:
        return [0]
    k = len(clue); tot = sum(clue)
    slack = n - tot - (k - 1)
    if slack < 0: return []
    def rec(i, pos, mask):
        if i == k:
            res.append(mask); return
        for start in range(pos, n - (sum(clue[i:]) + (k - i - 1)) + 1):
            m = mask
            for j in range(clue[i]): m |= 1 << (start + j)
            rec(i + 1, start + clue[i] + 1, m)
    rec(0, 0, 0)
    return res

def s_hanjie(clue):
    a, b = clue.split("\n")
    rc = _lines(a); cc = _lines(b)
    R = len(rc); C = len(cc)
    pats = [_patterns(r, C) for r in rc]
    for p in pats:
        if not p: return ""
    colpats = [_patterns(c, R) for c in cc]
    # column prefix masks: for each column, set of achievable prefixes
    colpre = []
    for j in range(C):
        s = set()
        for m in colpats[j]:
            for r in range(R + 1):
                s.add((r, m & ((1 << r) - 1)))
        colpre.append(s)
    grid = [0] * R
    def dfs(r):
        if tleft() < 0.002: return False
        if r == R: return True
        for m in pats[r]:
            grid[r] = m
            ok = True
            for j in range(C):
                pref = 0
                for i in range(r + 1):
                    if (grid[i] >> j) & 1: pref |= 1 << i
                if (r + 1, pref) not in colpre[j]: ok = False; break
            if ok and dfs(r + 1): return True
        return False
    if not dfs(0): return ""
    g = ["".join("#" if (grid[r] >> c) & 1 else "." for c in range(C)) for r in range(R)]
    return "\n".join(g)

# ---------- graphs ----------
def _parse_graph(clue):
    parts = clue.split()
    n = int(parts[0])
    edges = [tuple(map(int, p.split("-"))) for p in parts[1:]]
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    return n, edges, adj

def s_ikos(clue):
    n, edges, adj = _parse_graph(clue)
    seen = [False]*n; path = []
    deg = [len(a) for a in adj]
    adj = [sorted(a, key=lambda x: deg[x]) for a in adj]
    def dfs(v, d):
        if tleft() < 0.003: return False
        seen[v] = True; path.append(v)
        if d == n: return True
        for w in adj[v]:
            if not seen[w] and dfs(w, d+1): return True
        seen[v] = False; path.pop(); return False
    for s in range(n):
        if dfs(s, 1): return " ".join(map(str, path))
        del path[:]
        for i in range(n): seen[i] = False
    return ""

def s_trico(clue):
    n, edges, adj = _parse_graph(clue)
    col = [-1]*n
    order = sorted(range(n), key=lambda v: -len(adj[v]))
    def dfs(k):
        if tleft() < 0.003: return False
        if k == n: return True
        v = order[k]
        used = 0
        for u in adj[v]:
            c = col[u]
            if c >= 0: used |= 1 << c
        for c in range(3):
            if used >> c & 1: continue
            col[v] = c
            if dfs(k+1): return True
            col[v] = -1
        return False
    if not dfs(0): return ""
    return "".join(map(str, col))

# ---------- krom : 3-SAT ----------
def s_krom(clue):
    cls = []
    n = 0
    for t in clue.split():
        lits = [int(x) for x in t.split(",")]
        cls.append(lits)
        for l in lits:
            if abs(l) > n: n = abs(l)
    def dpll(clauses, assign):
        if tleft() < 0.003: return None
        c2 = []
        for c in clauses:
            sat = False; rest = []
            for l in c:
                v = assign.get(abs(l))
                if v is None: rest.append(l)
                elif (v == 1) == (l > 0): sat = True; break
            if sat: continue
            if not rest: return None
            c2.append(rest)
        for c in c2:
            if len(c) == 1:
                l = c[0]; a2 = dict(assign); a2[abs(l)] = 1 if l > 0 else 0
                return dpll(c2, a2)
        if not c2: return assign
        l = c2[0][0]; v = abs(l)
        for val in (1 if l > 0 else 0, 0 if l > 0 else 1):
            a2 = dict(assign); a2[v] = val
            r = dpll(c2, a2)
            if r is not None: return r
        return None
    r = dpll(cls, {})
    if r is None: return ""
    return "".join(str(r.get(i, 1)) for i in range(1, n+1))

# ---------- regina ----------
def s_regina(clue):
    g = clue.split("\n")
    n = len(g)
    blocked = [[g[r][c] == "X" for c in range(n)] for r in range(n)]
    res = [0]*n
    usedr = [False]*n; d1 = set(); d2 = set()
    def dfs(c):
        if tleft() < 0.003: return False
        if c == n: return True
        bc = blocked
        for r in range(n):
            if usedr[r] or bc[r][c]: continue
            if (r+c) in d1 or (r-c) in d2: continue
            usedr[r] = True; d1.add(r+c); d2.add(r-c); res[c] = r
            if dfs(c+1): return True
            usedr[r] = False; d1.discard(r+c); d2.discard(r-c)
        return False
    if dfs(0): return "".join(map(str, res))
    return ""

# ---------- skerry ----------
def s_skerry(clue):
    g = clue.split("\n")
    R = len(g)
    seen = set(); n = 0
    for r in range(R):
        row = g[r]
        for c in range(len(row)):
            if row[c] == "#" and (r, c) not in seen:
                n += 1; st = [(r, c)]; seen.add((r, c))
                while st:
                    x, y = st.pop()
                    for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                        if 0 <= nx < R and 0 <= ny < len(g[nx]) and g[nx][ny] == "#" and (nx, ny) not in seen:
                            seen.add((nx, ny)); st.append((nx, ny))
    return str(n)

# ---------- volute : spiral ----------
def s_volute(clue):
    g = clue.split("\n")
    R = len(g); C = len(g[0])
    out = []
    top, bot, left, right = 0, R-1, 0, C-1
    while top <= bot and left <= right:
        out.append(g[top][left:right+1])
        top += 1
        for r in range(top, bot+1): out.append(g[r][right])
        right -= 1
        if top <= bot:
            out.append(g[bot][left:right+1][::-1])
            bot -= 1
        if left <= right:
            for r in range(bot, top-1, -1): out.append(g[r][left])
            left += 1
    return "".join(out)

# ---------- warren : maze ----------
def s_warren(clue):
    g = clue.split("\n")
    R = len(g)
    S = E = None
    for r in range(R):
        row = g[r]
        i = row.find("S")
        if i >= 0: S = (r, i)
        i = row.find("E")
        if i >= 0: E = (r, i)
    from collections import deque
    prev = {S: None}
    q = deque([S])
    while q:
        cur = q.popleft()
        if cur == E: break
        x, y = cur
        for nx, ny, ch in ((x-1,y,"U"),(x+1,y,"D"),(x,y-1,"L"),(x,y+1,"R")):
            if 0 <= nx < R and 0 <= ny < len(g[nx]) and g[nx][ny] != "#" and (nx,ny) not in prev:
                prev[(nx,ny)] = (cur, ch); q.append((nx,ny))
    if E not in prev: return ""
    path = []; cur = E
    while prev[cur] is not None:
        p, ch = prev[cur]; path.append(ch); cur = p
    path.reverse()
    return "".join(path)

# ---------- wolf : wolfram CA rule ----------
def s_wolf(clue):
    tbl = [0]*8
    known = 0
    for p in clue.split():
        x, y = p.split(">")
        n = len(x)
        xi = [1 if c == "1" else 0 for c in x]
        for i in range(n):
            k = xi[i-1]*4 + xi[i]*2 + xi[(i+1) % n]
            b = 1 if y[i] == "1" else 0
            tbl[k] = b
            known |= 1 << k
        if known == 255: break
    return "".join(str(tbl[7-i]) for i in range(8))

# ---------- zebu ----------
def s_zebu(clue):
    cons = []
    for t in clue.split():
        if "<" in t: cons.append(("<",) + tuple(t.split("<")))
        elif "|" in t: cons.append(("|",) + tuple(t.split("|")))
        else:
            x, v = t.split("#"); cons.append(("#", x, int(v)))
    allv = "ABCDE"
    for perm in itertools.permutations(range(1, 6)):
        a = dict(zip(allv, perm)); ok = True
        for c in cons:
            k = c[0]
            if k == "<":
                if a[c[1]] >= a[c[2]]: ok = False; break
            elif k == "|":
                d = a[c[1]] - a[c[2]]
                if d != 1 and d != -1: ok = False; break
            else:
                if a[c[1]] != c[2]: ok = False; break
        if ok:
            r = [""]*5
            for v in allv: r[a[v]-1] = v
            return "".join(r)
    return ""

# ---------- ANAPAL ----------
def s_ANAPAL(clue):
    s, t = clue.split("|")
    L = len(s)
    from collections import Counter
    cnt = Counter(s)
    for p in range(L - len(t) + 1):
        arr = [None]*L
        ok = True
        for i, ch in enumerate(t):
            j = p + i; k = L - 1 - j
            if arr[j] is not None and arr[j] != ch: ok = False; break
            if arr[k] is not None and arr[k] != ch: ok = False; break
            arr[j] = ch; arr[k] = ch
        if not ok: continue
        used = Counter(x for x in arr if x is not None)
        rem = cnt - used
        if any(v < 0 for v in (cnt - used).values()) or sum(used.values()) > L:
            continue
        bad = False
        for ch in used:
            if used[ch] > cnt[ch]: bad = True; break
        if bad: continue
        rem = Counter(cnt)
        for ch, v in used.items(): rem[ch] -= v
        # fill remaining mirrored pairs
        free = [i for i in range(L) if arr[i] is None]
        pairs = []
        mid = None
        for i in free:
            j = L-1-i
            if i < j: pairs.append(i)
            elif i == j: mid = i
        pool = []
        for ch, v in rem.items(): pool.extend([ch]*v)
        pool.sort()
        # need each pair to consume 2 of same char
        avail = Counter(pool)
        okf = True
        for i in pairs:
            got = None
            for ch in list(avail):
                if avail[ch] >= 2: got = ch; break
            if got is None: okf = False; break
            avail[got] -= 2
            arr[i] = got; arr[L-1-i] = got
        if not okf: continue
        if mid is not None:
            left = [ch for ch in avail if avail[ch] > 0]
            if not left: continue
            arr[mid] = left[0]; avail[left[0]] -= 1
        if any(v > 0 for v in avail.values()): continue
        if None in arr: continue
        return "".join(arr)
    return ""


# ---------- PP : smallest palindromic prime containing the clue ----------
def _pp(clue, prefix_only):
    L0 = len(clue)
    digs = "0123456789"
    Ls = [L0] if L0 % 2 else []
    L = L0 + (1 if L0 % 2 == 0 else 2)
    cand_lens = ([L0] if L0 % 2 == 1 else []) + [L0 + 1 if L0 % 2 == 0 else L0 + 2]
    lens = []
    l = L0
    while len(lens) < 5:
        if l % 2 == 1 or l == 2: lens.append(l)
        l += 1
    for L in lens:
        if tleft() < 0.002: break
        cands = set()
        rng = [0] if prefix_only else range(L - L0 + 1)
        for p in rng:
            arr = [None]*L; ok = True
            for i, ch in enumerate(clue):
                j = p + i; k = L - 1 - j
                if (arr[j] is not None and arr[j] != ch) or (arr[k] is not None and arr[k] != ch):
                    ok = False; break
                arr[j] = ch; arr[k] = ch
            if not ok: continue
            half = L // 2
            free = [i for i in range(half) if arr[i] is None]
            if len(free) > 3: continue
            mid = half if L % 2 else None
            midfree = mid is not None and arr[mid] is None
            for combo in itertools.product(digs, repeat=len(free)):
                a = arr[:]
                for idx, d in zip(free, combo):
                    a[idx] = d; a[L-1-idx] = d
                if a[0] == "0": continue
                if midfree:
                    for d in digs:
                        a[mid] = d; cands.add("".join(a))
                else:
                    cands.add("".join(a))
        for s in sorted(cands):
            if _isprime(int(s)): return s
    return ""

def s_PP(clue):
    L0 = len(clue)
    digs = "0123456789"
    lens = []
    l = L0
    while len(lens) < 5:
        if l % 2 == 1 or l == 2: lens.append(l)
        l += 1
    for L in lens:
        if tleft() < 0.002: break
        cands = set()
        for p in range(L - L0 + 1):
            arr = [None]*L; ok = True
            for i, ch in enumerate(clue):
                j = p + i; k = L - 1 - j
                if (arr[j] is not None and arr[j] != ch) or (arr[k] is not None and arr[k] != ch):
                    ok = False; break
                arr[j] = ch; arr[k] = ch
            if not ok: continue
            half = L // 2
            free = [i for i in range(half) if arr[i] is None]
            if len(free) > 3: continue
            mid = half if L % 2 else None
            midfree = mid is not None and arr[mid] is None
            for combo in itertools.product(digs, repeat=len(free)):
                a = arr[:]
                for idx, d in zip(free, combo):
                    a[idx] = d; a[L-1-idx] = d
                if a[0] == "0": continue
                if midfree:
                    for d in digs:
                        a[mid] = d; cands.add("".join(a))
                else:
                    cands.add("".join(a))
        for s in sorted(cands):
            if _isprime(int(s)): return s
    return ""

# ---------- IDX : discrete logarithm ----------
def s_IDX(clue):
    g, h, p = [int(x) for x in clue.split()]
    g %= p; h %= p
    m = int(math.isqrt(p)) + 1
    tbl = {}
    e = 1
    for j in range(m):
        if e not in tbl: tbl[e] = j
        e = e * g % p
    try:
        f = pow(g, -m, p)
    except Exception:
        return ""
    y = h
    for i in range(m + 1):
        j = tbl.get(y)
        if j is not None:
            return str(i * m + j)
        y = y * f % p
    return ""

# ---------- ALLWIN : de Bruijn sequence ----------
def s_ALLWIN(clue):
    alpha, n = clue.split()
    n = int(n); k = len(alpha)
    a = [0] * (k * n + 1)
    seq = []
    def db(t, p):
        if t > n:
            if n % p == 0:
                seq.extend(a[1:p+1])
        else:
            a[t] = a[t-p]; db(t+1, p)
            for j in range(a[t-p]+1, k):
                a[t] = j; db(t+1, t)
    db(1, 1)
    s = "".join(alpha[i] for i in seq)
    return s


# ---------- TOPPLE : reverse polish expression ----------
def s_TOPPLE(clue):
    lhs, rhs = clue.split("=")
    target = int(rhs)
    items = [(int(d), d) for d in lhs]
    def rec(lst):
        if tleft() < 0.002: return None
        n = len(lst)
        if n == 1:
            return lst[0][1] if lst[0][0] == target else None
        for i in range(n):
            for j in range(n):
                if i == j: continue
                a = lst[i]; b = lst[j]
                rest = [lst[k] for k in range(n) if k != i and k != j]
                for op in "+-*":
                    if op in "+*" and i > j: continue
                    if op == "+": v = a[0] + b[0]
                    elif op == "*": v = a[0] * b[0]
                    elif op == "-": v = a[0] - b[0]
                    else:
                        if b[0] == 0 or a[0] % b[0]: continue
                        v = a[0] // b[0]
                    r = rec(rest + [(v, a[1] + b[1] + op)])
                    if r is not None: return r
        return None
    r = rec(items)
    return r or ""


# ============================ dispatcher ============================
FINAL = False
BUDGET = 0.014
_pc = time.perf_counter
_D = DEADLINE

SOLVERS = {}
for _k, _v in list(globals().items()):
    if _k.startswith("s_"):
        SOLVERS[_k[2:]] = _v

CACHE = {}

class _Skip(Exception):
    pass

def on_round_start(memory):
    DEADLINE[0] = _pc() + 5.0
    try:
        s_HAIL("27"); _life_prep(6)
    except Exception:
        pass
    CACHE.clear()
    old = memory.get("cache")
    if isinstance(old, dict):
        CACHE.update(old)
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1

def solve(name, clue, memory):
    k = name + "\x00" + clue
    a = CACHE.get(k)
    if a is not None:
        return a
    f = SOLVERS.get(name)
    if f is None:
        raise _Skip(name)
    _D[0] = _pc() + BUDGET
    try:
        a = f(clue)
    except Exception:
        raise _Skip(name)
    if not a:
        raise _Skip(name)
    CACHE[k] = a
    return a

def on_round_end(items, memory):
    if len(CACHE) < 60000:
        memory["cache"] = CACHE
