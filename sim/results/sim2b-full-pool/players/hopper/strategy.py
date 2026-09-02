"""strategy.py - centaur zendo solvers"""
import math, random, itertools, sys, re, time
from fractions import Fraction as F

sys.setrecursionlimit(20000)

# ---------------- helpers ----------------
class _Bust(Exception):
    pass

_BUD = [0]

def _tick(n=1):
    _BUD[0] -= n
    if _BUD[0] < 0:
        raise _Bust()

DIG = "0123456789abcdefghijklmnopqrstuvwxyz"

def to_base(n, b, up=False):
    if n == 0: return "0"
    s = ""
    while n:
        s = DIG[n % b] + s
        n //= b
    return s.upper() if up else s

def egcd(a, b):
    if b == 0: return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)

def inv(a, m):
    g, x, _ = egcd(a % m, m)
    return x % m

def is_prime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x == 1 or x == n-1: continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

def pollard(n):
    if n % 2 == 0: return 2
    while True:
        x = random.randrange(2, n); y = x; c = random.randrange(1, n); d = 1
        while d == 1:
            x = (x*x + c) % n
            y = (y*y + c) % n; y = (y*y + c) % n
            d = math.gcd(abs(x-y), n)
        if d != n: return d

def factorize(n):
    if n == 1: return []
    if is_prime(n): return [n]
    for p in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47):
        if n % p == 0: return [p] + factorize(n//p)
    d = pollard(n)
    return factorize(d) + factorize(n//d)

# ---------------- BASILISK: base conversion ----------------
def s_BASILISK(clue, v):
    body, rest = clue.split(":")
    fb, tb = rest.split(">")
    n = int(body, int(fb))
    return to_base(n, int(tb), v == 1)

# ---------------- SUNZI: CRT ----------------
def s_SUNZI(clue, v):
    rs = []; ms = []
    for t in clue.split():
        a, m = t.split("%"); rs.append(int(a)); ms.append(int(m))
    M = 1
    for m in ms: M *= m
    x = 0
    for a, m in zip(rs, ms):
        Mi = M // m
        x += a * Mi * inv(Mi, m)
    return str(x % M)

# ---------------- wolf: elementary CA rule ----------------
def s_wolf(clue, v):
    pairs = [p.split(">") for p in clue.split()]
    for rule in range(256):
        ok = True
        for a, b in pairs:
            n = len(a)
            out = []
            for i in range(n):
                idx = (a[i-1] == "1")*4 + (a[i] == "1")*2 + (a[(i+1) % n] == "1")
                out.append("1" if (rule >> idx) & 1 else "0")
            if "".join(out) != b: ok = False; break
        if ok:
            return str(rule) if v == 0 else "rule " + str(rule)
    return None

# ---------------- volute: spiral read ----------------
def spiral(g, cw=True):
    g = [list(r) for r in g]
    out = []
    top, bot, left, right = 0, len(g)-1, 0, len(g[0])-1
    if cw:
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
            if top <= bot:
                for c in range(left, right+1): out.append(g[bot][c])
                bot -= 1
            if left <= right:
                for r in range(bot, top-1, -1): out.append(g[r][right])
                right -= 1
            if top <= bot:
                for c in range(right, left-1, -1): out.append(g[top][c])
                top += 1
    return "".join(out)

def s_volute(clue, v):
    g = clue.split("\n")
    return spiral(g, v == 0)

# ---------------- RUNIC: run length encode ----------------
def s_RUNIC(clue, v):
    runs = []
    prev = clue[0]; cnt = 1
    for ch in clue[1:]:
        if ch == prev: cnt += 1
        else: runs.append((prev, cnt)); prev = ch; cnt = 1
    runs.append((prev, cnt))
    if v == 0: return "".join("%d%s" % (n, c) for c, n in runs)
    if v == 1: return "".join("%s%d" % (c, n) for c, n in runs)
    if v == 2: return " ".join("%d%s" % (n, c) for c, n in runs)
    return " ".join("%s%d" % (c, n) for c, n in runs)

# ---------------- HAIL: collatz ----------------
def s_HAIL(clue, v):
    n = int(clue); seq = [n]
    while n != 1:
        n = n//2 if n % 2 == 0 else 3*n+1
        seq.append(n)
    if v == 0: return str(len(seq)-1)
    if v == 1: return str(max(seq))
    if v == 2: return " ".join(map(str, seq))
    return str(len(seq))

# ---------------- SPQ: semiprime factor ----------------
def s_SPQ(clue, v):
    n = int(clue)
    f = sorted(factorize(n))
    if v == 0: return "%d %d" % (f[0], f[-1])
    if v == 1: return "%d*%d" % (f[0], f[-1])
    if v == 2: return "%d,%d" % (f[0], f[-1])
    return str(f[0])

# ---------------- carre: latin square ----------------
def s_carre(clue, v):
    g = [list(r) for r in clue.split("/")]
    n = len(g)
    digs = [str(i+1) for i in range(n)]
    blanks = [(r, c) for r in range(n) for c in range(n) if g[r][c] == "."]
    def bt(i):
        _tick()
        if i == len(blanks): return True
        r, c = blanks[i]
        row = set(g[r]); col = set(g[k][c] for k in range(n))
        for d in digs:
            if d not in row and d not in col:
                g[r][c] = d
                if bt(i+1): return True
                g[r][c] = "."
        return False
    if bt(0):
        return "/".join("".join(r) for r in g)
    return None

# ---------------- krom: SAT ----------------
def s_krom(clue, v):
    clauses = []
    nv = 0
    for t in clue.split():
        lits = [int(x) for x in t.split(",")]
        clauses.append(lits)
        for l in lits: nv = max(nv, abs(l))
    assign = [None]*(nv+1)
    def dpll(ci):
        # simple backtracking over variables with clause check
        return None
    # iterative backtracking on variables
    order = list(range(1, nv+1))
    val = [0]*(nv+1)
    # precompute clause list
    def sat_check(k):
        for cl in clauses:
            und = False; ok = False
            for l in cl:
                a = abs(l)
                if a > k: und = True; continue
                if (val[a] == 1) == (l > 0): ok = True; break
            if not ok and not und: return False
        return True
    def bt(k):
        _tick()
        if k > nv: return True
        for b in (1, 0):
            val[k] = b
            if sat_check(k) and bt(k+1): return True
        val[k] = 0
        return False
    if not bt(1): return None
    bits = [str(val[i]) for i in range(1, nv+1)]
    if v == 0: return "".join(bits)
    if v == 1: return " ".join(str(i if val[i] else -i) for i in range(1, nv+1))
    if v == 2: return ",".join(bits)
    return "".join("T" if val[i] else "F" for i in range(1, nv+1))

# ---------------- MARIENBAD: nim ----------------
def s_MARIENBAD(clue, v):
    piles = [int(x) for x in clue.split()]
    x = 0
    for p in piles: x ^= p
    if x == 0: return None
    for i, p in enumerate(piles):
        t = p ^ x
        if t < p:
            new = list(piles); new[i] = t
            if v == 0: return " ".join(map(str, new))
            if v == 1: return "%d %d" % (i, p - t)
            if v == 2: return "%d %d" % (i+1, p - t)
            return "%d,%d" % (i, p - t)
    return None

# ---------------- ALLWIN: de Bruijn ----------------
def debruijn(alpha, n):
    k = len(alpha)
    a = [0]*(k*n)
    seq = []
    def db(t, p):
        if t > n:
            if n % p == 0: seq.extend(a[1:p+1])
        else:
            a[t] = a[t-p]; db(t+1, p)
            for j in range(a[t-p]+1, k):
                a[t] = j; db(t+1, t)
    db(1, 1)
    return "".join(alpha[i] for i in seq)

def s_ALLWIN(clue, v):
    alpha, n = clue.split()
    n = int(n)
    s = debruijn(alpha, n)
    if v == 0: return s
    return s + s[:n-1]

# ---------------- ANAPAL: palindromic anagram containing pattern ---------
def s_ANAPAL(clue, v):
    S, P = clue.split("|")
    n = len(S)
    cnt = {}
    for ch in S: cnt[ch] = cnt.get(ch, 0) + 1
    odd = [c for c, k in cnt.items() if k % 2]
    if len(odd) > 1: return None
    half = n // 2
    mid = odd[0] if odd else None
    base = {c: k // 2 for c, k in cnt.items()}
    for st in range(0, n - len(P) + 1):
        full = [None] * n
        bad = False
        for i, ch in enumerate(P):
            for j in (st + i, n - 1 - st - i):
                if full[j] is not None and full[j] != ch: bad = True; break
                full[j] = ch
            if bad: break
        if bad: continue
        if n % 2 and full[half] is not None and full[half] != mid: continue
        hc = dict(base)
        for i in range(half):
            c = full[i]
            if c is not None:
                if hc.get(c, 0) <= 0: bad = True; break
                hc[c] -= 1
        if bad: continue
        pool = []
        for c, k in hc.items(): pool.extend([c] * k)
        pi = 0
        for i in range(half):
            if full[i] is None:
                full[i] = pool[pi]; pi += 1
                full[n-1-i] = full[i]
        if n % 2: full[half] = mid
        return "".join(full)
    return None

# ---------------- CRIBROT: caesar with crib ----------------
def s_CRIBROT(clue, v):
    ct, crib = clue.split("|")
    for sh in range(26):
        pt = "".join(chr((ord(c)-97-sh) % 26 + 97) if c.isalpha() else c for c in ct)
        if crib in pt:
            return pt if v == 0 else str(sh)
    return None

# ---------------- TARE: subset sum ----------------
def s_TARE(clue, v):
    nums, t = clue.split("|")
    a = [int(x) for x in nums.split()]
    t = int(t)
    n = len(a)
    # dp over reachable sums with parent tracking
    reach = {0: None}
    for i, x in enumerate(a):
        new = dict(reach)
        for s, p in reach.items():
            ns = s + x
            if ns <= t and ns not in new: new[ns] = (s, i)
        reach = new
        if t in reach: break
    if t not in reach: return None
    idxs = []
    cur = t
    while reach[cur] is not None:
        s, i = reach[cur]; idxs.append(i); cur = s
    idxs.sort()
    if v == 0: return " ".join(str(a[i]) for i in idxs)
    if v == 1: return " ".join(str(i) for i in idxs)
    if v == 2: return " ".join(str(i+1) for i in idxs)
    return "".join("1" if i in set(idxs) else "0" for i in range(n))

# ---------------- graphs ----------------
def parse_graph(clue):
    t = clue.split(); n = int(t[0])
    adj = [set() for _ in range(n)]
    for e in t[1:]:
        a, b = e.split("-"); a = int(a); b = int(b)
        adj[a].add(b); adj[b].add(a)
    return n, adj

def s_trico(clue, v):
    n, adj = parse_graph(clue)
    col = [-1]*n
    order = sorted(range(n), key=lambda x: -len(adj[x]))
    pos = {x: i for i, x in enumerate(order)}
    def bt(i):
        _tick()
        if i == n: return True
        vtx = order[i]
        used = set(col[u] for u in adj[vtx])
        for c in range(3):
            if c not in used:
                col[vtx] = c
                if bt(i+1): return True
                col[vtx] = -1
        return False
    if not bt(0): return None
    if v == 0: return "".join(str(c) for c in col)
    if v == 1: return " ".join(str(c) for c in col)
    if v == 2: return "".join("RGB"[c] for c in col)
    return ",".join(str(c) for c in col)

def hamilton(n, adj, cycle):
    for start in range(n):
        path = [start]; used = [False]*n; used[start] = True
        def bt():
            _tick()
            if len(path) == n:
                return (not cycle) or (start in adj[path[-1]])
            for u in sorted(adj[path[-1]], key=lambda x: len(adj[x])):
                if not used[u]:
                    used[u] = True; path.append(u)
                    if bt(): return True
                    path.pop(); used[u] = False
            return False
        if bt(): return list(path)
        if not cycle and start > 2: break
    return None

def s_ikos(clue, v):
    n, adj = parse_graph(clue)
    p = hamilton(n, adj, True)
    if p is None: p = hamilton(n, adj, False)
    if p is None: return None
    if v == 0: return " ".join(map(str, p))
    if v == 1: return " ".join(map(str, p + [p[0]]))
    if v == 2: return ",".join(map(str, p))
    return "-".join(map(str, p))

# ---------------- AHMES: egyptian fractions ----------------
def s_AHMES(clue, v):
    a, b = clue.split("/"); a = int(a); b = int(b)
    dens = []
    while a:
        d = -(-b // a)
        dens.append(d)
        a, b = a*d - b, b*d
        g = math.gcd(a, b) or 1
        a //= g; b //= g
    if v == 0: return "+".join("1/%d" % d for d in dens)
    if v == 1: return " ".join(str(d) for d in dens)
    if v == 2: return ",".join(str(d) for d in dens)
    return " + ".join("1/%d" % d for d in dens)

# ---------------- CHAKRA: pell ----------------
def pell(N):
    a0 = int(math.isqrt(N))
    if a0*a0 == N: return None
    m, d, a = 0, 1, a0
    num1, num = 1, a0
    den1, den = 0, 1
    while num*num - N*den*den != 1:
        m = d*a - m
        d = (N - m*m)//d
        a = (a0 + m)//d
        num1, num = num, a*num + num1
        den1, den = den, a*den + den1
    return num, den

def s_CHAKRA(clue, v):
    r = pell(int(clue))
    if r is None: return None
    x, y = r
    if v == 0: return "%d %d" % (x, y)
    if v == 1: return "%d,%d" % (x, y)
    return str(x)

# ---------------- IDX: discrete log ----------------
def s_IDX(clue, v):
    a, b, m = [int(x) for x in clue.split()]
    a %= m; b %= m
    nsq = int(math.isqrt(m)) + 1
    tbl = {}
    cur = 1
    for j in range(nsq):
        if cur not in tbl: tbl[cur] = j
        cur = cur*a % m
    factor = pow(inv(a, m), nsq, m)
    y = b
    for i in range(nsq+1):
        if y in tbl:
            return str(i*nsq + tbl[y])
        y = y*factor % m
    return None

# ---------------- TWINE: LCS ----------------
def s_TWINE(clue, v):
    p = clue.split("|")
    a, b = p[0], p[1]
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n-1, -1, -1):
        ai = a[i]; di = dp[i]; di1 = dp[i+1]
        for j in range(m-1, -1, -1):
            di[j] = di1[j+1]+1 if ai == b[j] else (di1[j] if di1[j] >= di[j+1] else di[j+1])
    if v == 1: return str(dp[0][0])
    res = []; i = j = 0
    while i < n and j < m:
        if a[i] == b[j]: res.append(a[i]); i += 1; j += 1
        elif dp[i+1][j] >= dp[i][j+1]: i += 1
        else: j += 1
    return "".join(res)

# ---------------- skerry: islands ----------------
def s_skerry(clue, v):
    g = clue.split("\n")
    R = len(g); C = len(g[0])
    seen = [[False]*C for _ in range(R)]
    cnt = 0; big = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] == "#" and not seen[r][c]:
                cnt += 1; sz = 0
                st = [(r, c)]; seen[r][c] = True
                while st:
                    y, x = st.pop(); sz += 1
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < R and 0 <= nx < C and g[ny][nx] == "#" and not seen[ny][nx]:
                            seen[ny][nx] = True; st.append((ny, nx))
                big = max(big, sz)
    return str(cnt) if v == 0 else str(big)

# ---------------- zebu: CSP ----------------
def s_zebu(clue, v):
    toks = clue.split()
    names = sorted(set(t[0] for t in toks) | set(t[2] for t in toks if t[2].isalpha()))
    idx = {nm: i for i, nm in enumerate(names)}
    n = len(names)
    cons = []
    for t in toks:
        A = t[0]; op = t[1]; B = t[2]
        cons.append((idx[A], op, idx.get(B, -1), int(B) if B.isdigit() else 0))
    dom = list(range(1, 6))
    for assign in itertools.product(dom, repeat=n):
        ok = True
        for a, op, b, k in cons:
            if op == "#":
                if assign[a] != k: ok = False; break
            elif op == "<":
                if not assign[a] < assign[b]: ok = False; break
            elif op == "|":
                if assign[a] == assign[b]: ok = False; break
        if ok:
            if v == 0: return "".join(str(x) for x in assign)
            if v == 1: return " ".join("%s=%d" % (names[i], assign[i]) for i in range(n))
            if v == 2: return " ".join(str(x) for x in assign)
            return ",".join(str(x) for x in assign)
    return None

# ---------------- HANSOM: closed taxicab tour within budget --------------
def s_HANSOM(clue, v):
    pts, t = clue.split("|"); t = int(t)
    P = [tuple(int(z) for z in p.split(",")) for p in pts.split()]
    n = len(P)
    D = [[abs(P[i][0]-P[j][0]) + abs(P[i][1]-P[j][1]) for j in range(n)] for i in range(n)]
    D0 = D[0]
    best = None; bl = None
    for perm in itertools.permutations(range(1, n)):
        tot = D0[perm[0]]
        prev = perm[0]
        for k in range(1, n-1):
            tot += D[prev][perm[k]]; prev = perm[k]
            if tot >= t: break
        else:
            tot += D0[prev]
            if tot <= t:
                return "0 " + " ".join(map(str, perm))
            if bl is None or tot < bl: bl = tot; best = perm
    if best is None: return None
    return "0 " + " ".join(map(str, best))


# ---------------- warren: maze ----------------
def s_warren(clue, v):
    g = clue.split("\n")
    R = len(g)
    S = E = None
    for r in range(R):
        for c in range(len(g[r])):
            if g[r][c] == "S": S = (r, c)
            elif g[r][c] == "E": E = (r, c)
    if S is None or E is None: return None
    from collections import deque
    prev = {S: None}
    q = deque([S])
    while q:
        cur = q.popleft()
        if cur == E: break
        r, c = cur
        for dr, dc, ch in ((-1,0,"U"),(1,0,"D"),(0,-1,"L"),(0,1,"R")):
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < len(g[nr]) and g[nr][nc] != "#" and (nr, nc) not in prev:
                prev[(nr, nc)] = (cur, ch); q.append((nr, nc))
    if E not in prev: return None
    path = []; cur = E
    while prev[cur] is not None:
        pp, ch = prev[cur]; path.append(ch); cur = pp
    path.reverse()
    return "".join(path)


# ---------------- GRAYLING: hypercube walk of exact length ----------------
def s_GRAYLING(clue, v):
    a, b, k = clue.split(); k = int(k)
    n = len(a)
    path = [a]
    seen = {a}
    def bt(cur, steps):
        _tick()
        if steps == k:
            return cur == b
        d = 0
        for i in range(n):
            if cur[i] != b[i]: d += 1
        rem = k - steps
        if d > rem or (rem - d) % 2: return False
        for i in range(n):
            nxt = cur[:i] + ("1" if cur[i] == "0" else "0") + cur[i+1:]
            if nxt in seen: continue
            seen.add(nxt); path.append(nxt)
            if bt(nxt, steps+1): return True
            path.pop(); seen.discard(nxt)
        return False
    if not bt(a, 0): return None
    return " ".join(path)


# ---------------- erewhon: Life predecessor (bounded) ----------------
_EW = {}
_EWPAR = {}

def _build_ew(C):
    W = []
    for x in range(1 << C):
        w = []
        for j in range(C):
            s2 = (x >> j) & 1
            if j > 0: s2 += (x >> (j-1)) & 1
            if j < C-1: s2 += (x >> (j+1)) & 1
            w.append(s2)
        W.append(w)
    tbl = []
    for a in range(1 << C):
        Wa = W[a]
        for b in range(1 << C):
            Wb = W[b]
            d = {}
            for c in range(1 << C):
                Wc = W[c]
                t = 0
                for j in range(C):
                    nb = Wa[j] + Wb[j] + Wc[j] - ((b >> j) & 1)
                    if nb == 3 or (nb == 2 and ((b >> j) & 1)):
                        t |= 1 << j
                d.setdefault(t, []).append(c)
            tbl.append(d)
    return tbl

def s_erewhon(clue, v):
    rows = clue.split("\n")
    R = len(rows); C = len(rows[0])
    if C > 7 or R > 9: return None
    tbl = _EW.get(C)
    if tbl is None:
        tbl = _EW[C] = _build_ew(C)
    tgt = []
    for r in rows:
        m = 0
        for j, ch in enumerate(r):
            if ch == "#": m |= 1 << j
        tgt.append(m)
    N = 1 << C
    states = {(0, p0): None for p0 in range(N)}
    for r in range(R - 1):
        nxt = {}
        t = tgt[r]
        for (a, b) in states:
            for c in tbl[a*N + b].get(t, ()):
                if (b, c) not in nxt:
                    nxt[(b, c)] = (a, b)
        if not nxt: return None
        states = nxt
        _EWPAR[r] = nxt
    t = tgt[R-1]
    fin = None
    for (a, b) in states:
        if 0 in tbl[a*N + b].get(t, ()):
            fin = (a, b); break
    if fin is None: return None
    cells = [fin[1], fin[0]]
    cur = fin
    for r in range(R - 2, -1, -1):
        cur = _EWPAR[r][cur]
        cells.append(cur[0])
    cells = cells[:R]
    cells.reverse()
    return "\n".join("".join("#" if (m >> j) & 1 else "." for j in range(C)) for m in cells)


# ---------------- zebu: zebra permutation puzzle ----------------
_ZP = None
def s_zebu(clue, v):
    global _ZP
    if _ZP is None:
        _ZP = list(itertools.permutations((1, 2, 3, 4, 5)))
    idx = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
    cons = []
    for t in clue.split():
        A = idx[t[0]]; op = t[1]; B = t[2]
        cons.append((A, op, idx[B] if B in idx else -1, int(B) if B.isdigit() else 0))
    for a in _ZP:
        ok = True
        for A, op, B, k in cons:
            if op == "#":
                if a[A] != k: ok = False; break
            elif op == "<":
                if a[A] >= a[B]: ok = False; break
            else:
                if abs(a[A] - a[B]) != 1: ok = False; break
        if ok:
            inv = [""] * 5
            for i, val in enumerate(a): inv[val-1] = "ABCDE"[i]
            return "".join(inv)
    return None


# ---------------- hanjie: nonogram ----------------
def _lines(part):
    return [[int(x) for x in g.split(",") if x != ""] for g in part.split("/")]

def _gen(cl, width):
    res = []
    cl = [x for x in cl if x]
    def rec(i, pos, mask):
        if i == len(cl):
            res.append(mask); return
        need = sum(cl[i:]) + (len(cl)-i-1)
        for start in range(pos, width-need+1):
            m = mask
            for k in range(start, start+cl[i]): m |= 1 << k
            rec(i+1, start+cl[i]+1, m)
    rec(0, 0, 0)
    return res

def s_hanjie(clue, v):
    a, b = clue.split("\n")
    rows = _lines(a); cols = _lines(b)
    R = len(rows); C = len(cols)
    rp = [_gen(r, C) for r in rows]
    cp = [_gen(c, R) for c in cols]
    if not all(rp) or not all(cp): return None
    PS = []
    for j in range(C):
        pl = []
        for i in range(R):
            m = (1 << (i+1)) - 1
            pl.append(frozenset(p & m for p in cp[j]))
        PS.append(pl)
    colbits = [0]*C
    chosen = [0]*R
    def bt(i):
        _tick()
        if i == R: return True
        for p in rp[i]:
            ok = True
            for j in range(C):
                nb = colbits[j] | (((p >> j) & 1) << i)
                if nb not in PS[j][i]: ok = False; break
                colbits[j] = nb
            if ok:
                chosen[i] = p
                if bt(i+1): return True
            for j in range(C):
                colbits[j] &= (1 << i) - 1
        return False
    if not bt(0): return None
    return "\n".join("".join("#" if (chosen[i] >> j) & 1 else "." for j in range(C)) for i in range(R))


# ---------------- regina: n-queens with blocked squares ----------------
def s_regina(clue, v):
    g = clue.split("\n")
    n = len(g)
    pos = []
    def bt(c, rows, d1, d2):
        _tick()
        if c == n: return True
        for r in range(n):
            if g[r][c] == "." and not (rows >> r) & 1 and (r-c+n) not in d1 and (r+c) not in d2:
                pos.append(r); d1.add(r-c+n); d2.add(r+c)
                if bt(c+1, rows | (1 << r), d1, d2): return True
                d1.discard(r-c+n); d2.discard(r+c); pos.pop()
        return False
    if not bt(0, 0, set(), set()): return None
    return "".join(map(str, pos))


# ---------------- DUOMASK: regex intersection ----------------
_RX = {}
def s_DUOMASK(clue, v):
    p1, p2 = clue.split()
    e = _RX.get(clue)
    if e is None:
        e = _RX[clue] = (re.compile(p1 + r"\Z"), re.compile(p2 + r"\Z"))
    r1, r2 = e
    t0 = time.perf_counter()
    for L in range(1, 15):
        if time.perf_counter() - t0 > 0.030: return None
        for tup in itertools.product("ab", repeat=L):
            s2 = "".join(tup)
            if r1.match(s2) and r2.match(s2):
                return s2
    return None


# ---------------- PP: smallest palindromic prime containing clue ----------
def s_PP(clue, v):
    k = len(clue)
    t0 = time.perf_counter()
    for L in range(k, k + 8):
        if L > 2 and L % 2 == 0:
            continue
        half = (L + 1) // 2
        m = L - half
        lo = 10 ** (half - 1) if half > 1 else 1
        hi = 10 ** half
        cnt = 0
        for h in range(lo, hi):
            sh = str(h)
            if sh[0] not in "1379":
                continue
            full = sh + sh[m-1::-1] if m else sh
            if clue in full and is_prime(int(full)):
                return full
            cnt += 1
            if not (cnt & 8191) and time.perf_counter() - t0 > 0.045:
                return None
    return None


# ---------------- HAIL: smallest n with given collatz stopping time -------
_HAIL = {}
def _build_hail(lim=400000):
    memo = {1: 0}
    first = {}
    for n in range(1, lim):
        stack = []
        m = n
        while m not in memo:
            stack.append(m)
            m = m//2 if m % 2 == 0 else 3*m+1
        val = memo[m]
        while stack:
            x = stack.pop(); val += 1; memo[x] = val
        if val not in first: first[val] = n
    return first

def s_HAIL(clue, v):
    n = _HAIL.get(int(clue))
    return None if n is None else str(n)


# ---------------- wolf: elementary CA rule, 8-bit binary ----------------
def s_wolf(clue, v):
    pairs = [p.split(">") for p in clue.split()]
    for rule in range(256):
        ok = True
        for a, b in pairs:
            n = len(a)
            out = []
            for i in range(n):
                idx = (a[i-1] == "1")*4 + (a[i] == "1")*2 + (a[(i+1) % n] == "1")
                out.append("1" if (rule >> idx) & 1 else "0")
            if "".join(out) != b: ok = False; break
        if ok:
            return format(rule, "08b")
    return None


# ---------------- TOPPLE: 24-game in RPN ----------------
def _rpn(node):
    if node[0] == "n": return [node[1]]
    return _rpn(node[2]) + _rpn(node[3]) + [node[1]]

def s_TOPPLE(clue, v):
    L, R = clue.split("=")
    target = F(int(R))
    nums = [(F(int(c)), ("n", c)) for c in L]
    def rec(vals):
        _tick()
        if len(vals) == 1:
            return vals[0][1] if vals[0][0] == target else None
        m = len(vals)
        for i in range(m):
            for j in range(m):
                if i == j: continue
                rest = [vals[k] for k in range(m) if k != i and k != j]
                a, ea = vals[i]; b, eb = vals[j]
                for val, op in ((a+b, "+"), (a-b, "-"), (a*b, "*")):
                    if val < 0: continue
                    r = rec(rest + [(val, ("o", op, ea, eb))])
                    if r: return r
        return None
    t = rec(nums)
    return None if t is None else "".join(_rpn(t))



# ---------------- LegoZendo: experiments ----------------
def _lego(bricks, L, W, H):
    g = [["_"]*W for _ in range(H)]
    for (r, c) in bricks:
        for j in range(3):
            g[r][c+j] = L
    out = []
    for row in g:
        out.append("".join(row)); out.append("".join(row))
    return "\n".join(out)

def s_LegoZendo(clue, v):
    L = clue[0]
    n = max(1, int(clue[1:]))
    row = L * (3 * n)
    return row + "\n" + row

# ---------------- dispatch ----------------
SOLVERS = {
    "BASILISK": (s_BASILISK, 1), "SUNZI": (s_SUNZI, 1), "volute": (s_volute, 1),
    "RUNIC": (s_RUNIC, 1), "SPQ": (s_SPQ, 1), "carre": (s_carre, 1),
    "krom": (s_krom, 1), "MARIENBAD": (s_MARIENBAD, 1), "ALLWIN": (s_ALLWIN, 1),
    "CRIBROT": (s_CRIBROT, 1), "TARE": (s_TARE, 1), "trico": (s_trico, 1),
    "ikos": (s_ikos, 1), "AHMES": (s_AHMES, 1), "CHAKRA": (s_CHAKRA, 1),
    "IDX": (s_IDX, 1), "TWINE": (s_TWINE, 1), "skerry": (s_skerry, 1),
    "warren": (s_warren, 1), "GRAYLING": (s_GRAYLING, 1),
    "ANAPAL": (s_ANAPAL, 1),
    "erewhon": (s_erewhon, 1), "zebu": (s_zebu, 1), "hanjie": (s_hanjie, 1),
    "regina": (s_regina, 1), "DUOMASK": (s_DUOMASK, 1),
    "PP": (s_PP, 1), "HAIL": (s_HAIL, 1), "wolf": (s_wolf, 1),
    "TOPPLE": (s_TOPPLE, 1), "HANSOM": (s_HANSOM, 1), "LegoZendo": (s_LegoZendo, 1),
}

# variant forced for classes whose format is confirmed
FIXED = {"BASILISK": 0, "SUNZI": 0, "volute": 0, "RUNIC": 0, "SPQ": 3,
         "carre": 0, "krom": 0, "MARIENBAD": 0, "ALLWIN": 0, "CRIBROT": 0,
         "TARE": 3, "trico": 0, "ikos": 0, "AHMES": 1, "CHAKRA": 0,
         "IDX": 0, "TWINE": 0, "skerry": 0, "warren": 0, "GRAYLING": 0,
         "erewhon": 0, "hanjie": 0, "DUOMASK": 0, "wolf": 0, "PP": 0, "HAIL": 0,
         "zebu": 0, "regina": 0, "TOPPLE": 0, "LegoZendo": 0, "ANAPAL": 0,
         "HANSOM": 0, "erewhon": 0}


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1
    memory["examples"] = {}
    if 6 not in _EW:
        _EW[6] = _build_ew(6)
    if not _HAIL:
        _HAIL.update(_build_hail())


def solve(name, clue, memory):
    e = SOLVERS.get(name)
    if e is None:
        return None
    fn, nv = e
    _BUD[0] = 60000
    try:
        f = FIXED.get(name)
        v = f if f is not None else ((sum(map(ord, clue)) % nv) if nv > 1 else 0)
        return fn(clue, v)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
