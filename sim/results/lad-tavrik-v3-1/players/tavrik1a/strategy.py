"""Centaur Zendo strategy: rule-family multiple choice + norvel drum slips."""
import re

VOWELS = set("aeiou")

# ---------------------------------------------------------------- norvel
_BAR = re.compile(r'^(\w+)\s*\|(.*)\|\s*$')

def solve_norvel(clue):
    lines = clue.split("\n")
    rows = {}
    order = []
    for idx, L in enumerate(lines):
        m = _BAR.match(L)
        if m:
            rows[m.group(1)] = [idx, m.group(2)]
            order.append(m.group(1))
    hat = rows["hat"][1].replace("|", "")
    kick = rows["kick"][1].replace("|", "")
    sn_raw = rows["snare"][1]
    # map positions in raw string (with pipes) to grid index
    pos = []
    for i, ch in enumerate(sn_raw):
        if ch != "|":
            pos.append(i)
    snare = sn_raw.replace("|", "")
    n = len(snare)
    out = list(sn_raw)
    for p in range(n):
        if snare[p] != "x":
            continue
        if hat[p] == "x" or kick[p] == "x":
            continue
        # slip: slide right until the hat plays (stop before the next snare hit)
        q = p + 1
        while q < n and hat[q] != "x" and snare[q] != "x":
            q += 1
        if q >= n:
            continue
        if snare[q] == "x" and hat[q] != "x":
            q -= 1
            if q <= p:
                continue
        for r in range(p, q):
            out[pos[r]] = "-"
        out[pos[q]] = "x"
    lines[rows["snare"][0]] = _BAR.match(lines[rows["snare"][0]]).group(1) + \
        lines[rows["snare"][0]][len(_BAR.match(lines[rows["snare"][0]]).group(1)):]
    newline = "".join(out)
    prefix = lines[rows["snare"][0]].split("|")[0]
    lines[rows["snare"][0]] = prefix + "|" + newline + "|"
    return "\n".join(lines)


# ---------------------------------------------------------------- features
def f_word(w):
    f = set()
    n = len(w)
    f.add("len:%d" % n)
    f.add("lenpar:%d" % (n % 2))
    f.add("len>=%d" % (6 if n >= 6 else 0))
    for ch in set(w):
        f.add("has:" + ch)
    for ch in "abcdefghijklmnopqrstuvwxyz":
        if ch not in w:
            f.add("lacks:" + ch)
    f.add("first:" + w[0])
    f.add("last:" + w[-1])
    f.add("first2:" + w[:2])
    f.add("last2:" + w[-2:])
    if w[0] in VOWELS: f.add("startvowel")
    else: f.add("startcons")
    if w[-1] in VOWELS: f.add("endvowel")
    else: f.add("endcons")
    nv = sum(1 for c in w if c in VOWELS)
    f.add("nv:%d" % nv)
    f.add("nvpar:%d" % (nv % 2))
    nc = n - nv
    f.add("nc:%d" % nc)
    f.add("ncpar:%d" % (nc % 2))
    d = len(set(w))
    f.add("nd:%d" % d)
    if d == n: f.add("alldistinct")
    else: f.add("hasrepeat")
    if any(w[i] == w[i + 1] for i in range(n - 1)): f.add("doubleletter")
    if any(abs(ord(w[i]) - ord(w[i + 1])) == 1 for i in range(n - 1)): f.add("adjconsec")
    s = set(w)
    if any(chr(o) in s and chr(o + 1) in s for o in range(97, 122)): f.add("hasconsecpair")
    if list(w) == sorted(w): f.add("sortedasc")
    if w == w[::-1]: f.add("palin")
    if w[0] == w[-1]: f.add("firsteqlast")
    if w[0] < w[-1]: f.add("first<last")
    if w[0] > w[-1]: f.add("first>last")
    tot = sum(ord(c) - 96 for c in w)
    for k in (2, 3, 4, 5, 7):
        f.add("sum%%%d:%d" % (k, tot % k))
    f.add("vpat:" + "".join("v" if c in VOWELS else "c" for c in w))
    if any(w[i] in VOWELS and w[i + 1] in VOWELS for i in range(n - 1)): f.add("vv")
    if any(w[i] not in VOWELS and w[i + 1] not in VOWELS for i in range(n - 1)): f.add("cc")
    for d in range(1, min(6, n)):
        if any(w[i] == w[i + d] for i in range(n - d)):
            f.add("repdist:%d" % d)
    vs = "".join(sorted(set(c for c in w if c in VOWELS)))
    f.add("vset:" + vs)
    for v in "aeiou":
        if v in w: f.add("hasv:" + v)
        else: f.add("nov:" + v)
    f.add("maxlet:" + max(w))
    f.add("minlet:" + min(w))
    f.add("vfirstpos:%d" % next((i for i, c in enumerate(w) if c in VOWELS), -1))
    return f


def f_time(t):
    f = set()
    try:
        h, m = t.split(":")
        H = int(h); M = int(m)
    except Exception:
        return f
    ds = h + m
    f.add("h:%d" % H); f.add("m:%d" % M)
    for k in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 20, 25, 30):
        if M % k == 0: f.add("mdiv%d" % k)
    if H and M % H == 0: f.add("hdividesm")
    if M and H % M == 0: f.add("mdividesh")
    for k in (2, 3, 4, 5, 6):
        if H % k == 0: f.add("hdiv%d" % k)
    tot = H * 60 + M
    for k in (2, 3, 4, 5, 6, 7, 10):
        f.add("tot%%%d:%d" % (k, tot % k))
        f.add("hm%%%d:%d" % (k, (H + M) % k))
    for c in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20):
        if M == c * H: f.add("m=%dh" % c)
    for k in (8, 9, 11, 12):
        f.add("hm%%%d:%d" % (k, (H + M) % k))
    for k in (8, 9, 11, 12):
        f.add("tot%%%d:%d" % (k, (H * 60 + M) % k))
    if M == H: f.add("m=h")
    if M == H * H: f.add("m=hh")
    if H + M == 60: f.add("sum60")
    for d in "0123456789":
        if d in ds: f.add("dig:" + d)
        else: f.add("nodig:" + d)
    f.add("mten:%d" % (M // 10))
    f.add("mone:%d" % (M % 10))
    f.add("digsum:%d" % sum(int(c) for c in ds))
    f.add("digsumpar:%d" % (sum(int(c) for c in ds) % 2))
    for k in (2, 3, 5):
        f.add("digsum%%%d:%d" % (k, sum(int(c) for c in ds) % k))
    if len(set(ds)) == len(ds): f.add("digdistinct")
    if ds == ds[::-1]: f.add("digpalin")
    if M > 30: f.add("mgt30")
    if M < 30: f.add("mlt30")
    if M >= 30: f.add("mge30")
    if H in (2, 3, 5, 7, 11): f.add("hprime")
    if M in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59): f.add("mprime")
    if M in (0, 1, 4, 9, 16, 25, 36, 49): f.add("msquare")
    if H in (1, 4, 9): f.add("hsquare")
    if M % 10 == H % 10: f.add("sameunits")
    if str(M).zfill(2)[0] == str(M).zfill(2)[1]: f.add("mrepdig")
    if M > H: f.add("m>h")
    f.add("nplen:%d" % len(ds))
    # clock angle
    ang = abs((H % 12) * 30 + M * 0.5 - M * 6)
    ang = min(ang, 360 - ang)
    f.add("angdiv30:%d" % (int(round(ang)) % 30 == 0))
    if abs(ang) < 1: f.add("handstogether")
    if abs(ang - 180) < 1: f.add("handsopposite")
    if abs(ang - 90) < 1: f.add("handsright")
    f.add("hpar:%d" % (H % 2))
    f.add("mpar:%d" % (M % 2))
    return f


def f_nums(vals):
    f = set()
    n = len(vals)
    f.add("len:%d" % n)
    s = sum(vals)
    f.add("sum:%d" % s)
    for k in (2, 3, 4, 5, 6, 7):
        f.add("sum%%%d:%d" % (k, s % k))
    mx = max(vals); mn = min(vals)
    f.add("max:%d" % mx); f.add("min:%d" % mn)
    f.add("rng:%d" % (mx - mn))
    for v in range(1, 10):
        if v in vals: f.add("has:%d" % v)
        else: f.add("lacks:%d" % v)
        f.add("cnt%d:%d" % (v, vals.count(v)))
    d = len(set(vals))
    f.add("nd:%d" % d)
    if d == n: f.add("alldistinct")
    else: f.add("hasdup")
    ne = sum(1 for v in vals if v % 2 == 0)
    f.add("nev:%d" % ne); f.add("nevpar:%d" % (ne % 2))
    f.add("nodd:%d" % (n - ne)); f.add("noddpar:%d" % ((n - ne) % 2))
    if ne == n: f.add("alleven")
    if ne == 0: f.add("allodd")
    if any(vals[i] == vals[i + 1] for i in range(n - 1)): f.add("adjeq")
    if any(vals[i + 1] - vals[i] == 1 for i in range(n - 1)): f.add("adjinc1")
    if any(vals[i] - vals[i + 1] == 1 for i in range(n - 1)): f.add("adjdec1")
    if any(abs(vals[i] - vals[i + 1]) == 1 for i in range(n - 1)): f.add("adjabs1")
    if any(abs(vals[i] - vals[i + 1]) == 2 for i in range(n - 1)): f.add("adjabs2")
    if all(vals[i] <= vals[i + 1] for i in range(n - 1)): f.add("nondec")
    if all(vals[i] >= vals[i + 1] for i in range(n - 1)): f.add("noninc")
    if all(vals[i] < vals[i + 1] for i in range(n - 1)): f.add("strictinc")
    if all(vals[i] > vals[i + 1] for i in range(n - 1)): f.add("strictdec")
    if vals == vals[::-1]: f.add("palin")
    f.add("first:%d" % vals[0]); f.add("last:%d" % vals[-1])
    if vals[0] == vals[-1]: f.add("firsteqlast")
    if vals[0] < vals[-1]: f.add("first<last")
    if vals[0] > vals[-1]: f.add("first>last")
    f.add("firstpar:%d" % (vals[0] % 2)); f.add("lastpar:%d" % (vals[-1] % 2))
    for i, v in enumerate(vals[:6]):
        f.add("p%d:%d" % (i, v))
        f.add("p%dpar:%d" % (i, v % 2))
    run = 1; best = 1
    for i in range(1, n):
        if vals[i] == vals[i - 1]: run += 1; best = max(best, run)
        else: run = 1
    f.add("maxrun:%d" % best)
    f.add("cntmax:%d" % vals.count(mx))
    f.add("cntmin:%d" % vals.count(mn))
    f.add("sumfl:%d" % (vals[0] + vals[-1]))
    p = 1
    for v in vals: p *= v
    for k in (2, 3, 4, 5):
        f.add("prod%%%d:%d" % (k, p % k))
    f.add("ngt3:%d" % sum(1 for v in vals if v > 3))
    f.add("mid:%d" % vals[n // 2])
    return f


_RANK = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
         "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13}

def f_hand(line):
    f = set()
    cards = line.split()
    ranks = []; suits = []
    for c in cards:
        s = c[-1]; r = c[:-1]
        if r not in _RANK: return f
        ranks.append(_RANK[r]); suits.append(s)
    n = len(cards)
    f.add("n:%d" % n); f.add("npar:%d" % (n % 2))
    for s in "SHDC":
        k = suits.count(s)
        f.add("cnt%s:%d" % (s, k))
        if k: f.add("has%s" % s)
        else: f.add("no%s" % s)
    f.add("nsuits:%d" % len(set(suits)))
    if len(set(suits)) == 1: f.add("flush")
    red = sum(1 for s in suits if s in "HD")
    f.add("red:%d" % red); f.add("redpar:%d" % (red % 2))
    f.add("black:%d" % (n - red)); f.add("blackpar:%d" % ((n - red) % 2))
    if red == n: f.add("allred")
    if red == 0: f.add("allblack")
    for r in range(1, 14):
        if r in ranks: f.add("hasr:%d" % r)
        else: f.add("nor:%d" % r)
    tot = sum(ranks)
    f.add("rsum:%d" % tot)
    for k in (2, 3, 4, 5, 7):
        f.add("rsum%%%d:%d" % (k, tot % k))
    f.add("rmax:%d" % max(ranks)); f.add("rmin:%d" % min(ranks))
    f.add("rrng:%d" % (max(ranks) - min(ranks)))
    d = len(set(ranks))
    f.add("nrd:%d" % d)
    if d == n: f.add("rdistinct")
    else: f.add("haspair")
    if any(ranks.count(r) >= 3 for r in set(ranks)): f.add("hastrip")
    sr = sorted(set(ranks))
    if any(sr[i + 1] - sr[i] == 1 for i in range(len(sr) - 1)): f.add("consec2")
    run = 1; best = 1
    for i in range(1, len(sr)):
        if sr[i] - sr[i - 1] == 1: run += 1; best = max(best, run)
        else: run = 1
    f.add("maxrun:%d" % best)
    ne = sum(1 for r in ranks if r % 2 == 0)
    f.add("nev:%d" % ne); f.add("nevpar:%d" % (ne % 2))
    f.add("nodd:%d" % (n - ne)); f.add("noddpar:%d" % ((n - ne) % 2))
    faces = sum(1 for r in ranks if r >= 11)
    f.add("nface:%d" % faces)
    if faces == 0: f.add("noface")
    if 1 in ranks: f.add("hasace")
    f.add("first:%d" % ranks[0]); f.add("lastr:%d" % ranks[-1])
    f.add("firsts:" + suits[0]); f.add("lasts:" + suits[-1])
    if suits[0] == suits[-1]: f.add("sfl")
    if any(suits[i] == suits[i + 1] for i in range(n - 1)): f.add("adjsuit")
    f.add("nlow:%d" % sum(1 for r in ranks if r <= 6))
    f.add("nhigh:%d" % sum(1 for r in ranks if r >= 9))
    return f


def f_colors(s):
    f = set()
    n = len(s)
    f.add("len:%d" % n); f.add("lenpar:%d" % (n % 2))
    for c in "RBG":
        k = s.count(c)
        f.add("cnt%s:%d" % (c, k))
        f.add("cnt%spar:%d" % (c, k % 2))
        if k: f.add("has" + c)
        else: f.add("no" + c)
    f.add("first:" + s[0]); f.add("last:" + s[-1])
    if s[0] == s[-1]: f.add("firsteqlast")
    if s == s[::-1]: f.add("palin")
    if any(s[i] == s[i + 1] for i in range(n - 1)): f.add("hasdouble")
    else: f.add("noadjsame")
    for c in "RBG":
        if c * 2 in s: f.add("dbl" + c)
        if c * 3 in s: f.add("trp" + c)
    run = 1; best = 1
    for i in range(1, n):
        if s[i] == s[i - 1]: run += 1; best = max(best, run)
        else: run = 1
    f.add("maxrun:%d" % best)
    for k in (2, 3, 4, 5, 6):
        if best >= k: f.add("maxrun>=%d" % k)
    for c in "RBG":
        r = 1; bb = 0
        for i in range(n):
            if s[i] == c:
                r = r + 1 if i and s[i-1] == c else 1
                if r > bb: bb = r
        f.add("run%s:%d" % (c, bb))
        for k in (2, 3, 4, 5):
            if bb >= k: f.add("run%s>=%d" % (c, k))
        for k in (1, 2, 3, 4, 5, 6, 7):
            if s.count(c) >= k: f.add("cnt%s>=%d" % (c, k))
    cR, cB, cG = s.count("R"), s.count("B"), s.count("G")
    if cR == cB: f.add("R=B")
    if cR > cB: f.add("R>B")
    if cB > cR: f.add("B>R")
    if cG == cR: f.add("G=R")
    if cG > cR: f.add("G>R")
    if cB > cG: f.add("B>G")
    mx = max(cR, cB, cG)
    f.add("major:" + ("R" if cR == mx else "") + ("B" if cB == mx else "") + ("G" if cG == mx else ""))
    for a in "RBG":
        for b in "RBG":
            if a + b in s: f.add("bi:" + a + b)
    f.add("nblocks:%d" % (1 + sum(1 for i in range(1, n) if s[i] != s[i - 1])))
    f.add("half:" + ("e" if s[:n // 2].count("R") == s[n // 2:].count("R") else "n"))
    return f


def f_grid(g):
    f = set()
    rows = g
    n = len(rows); m = len(rows[0])
    cnt = sum(r.count("#") for r in rows)
    f.add("n:%d" % cnt); f.add("npar:%d" % (cnt % 2))
    f.add("n5:%d" % (cnt // 5))
    if rows == [r[::-1] for r in rows]: f.add("symLR")
    if rows == rows[::-1]: f.add("symUD")
    if rows == [r[::-1] for r in rows[::-1]]: f.add("sym180")
    cols = ["".join(rows[i][j] for i in range(n)) for j in range(m)]
    if cols == rows: f.add("symT")
    rc = [r.count("#") for r in rows]
    cc = [c.count("#") for c in cols]
    f.add("rcmax:%d" % max(rc)); f.add("rcmin:%d" % min(rc))
    f.add("ccmax:%d" % max(cc)); f.add("ccmin:%d" % min(cc))
    f.add("emptyrows:%d" % rc.count(0)); f.add("emptycols:%d" % cc.count(0))
    f.add("fullrows:%d" % rc.count(m)); f.add("fullcols:%d" % cc.count(n))
    if len(set(rc)) == 1: f.add("rowseq")
    if len(set(cc)) == 1: f.add("colseq")
    if len(set(rows)) < n: f.add("duprow")
    f.add("tl:" + rows[0][0]); f.add("br:" + rows[-1][-1])
    corners = sum(1 for c in (rows[0][0], rows[0][-1], rows[-1][0], rows[-1][-1]) if c == "#")
    f.add("corners:%d" % corners)
    f.add("center:" + rows[n // 2][m // 2])
    has2 = False
    for i in range(n - 1):
        for j in range(m - 1):
            if rows[i][j] == rows[i][j+1] == rows[i+1][j] == rows[i+1][j+1] == "#":
                has2 = True; break
        if has2: break
    if has2: f.add("has2x2")
    # connected components (4-neighbour)
    cells = set((i, j) for i in range(n) for j in range(m) if rows[i][j] == "#")
    comps = 0; seen = set(); iso = 0
    for c in cells:
        if c in seen: continue
        comps += 1
        stack = [c]; seen.add(c); size = 0
        while stack:
            (i, j) = stack.pop(); size += 1
            for (a, b) in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)):
                if (a, b) in cells and (a, b) not in seen:
                    seen.add((a, b)); stack.append((a, b))
        if size == 1: iso += 1
    f.add("comps:%d" % comps); f.add("iso:%d" % iso)
    if comps == 1: f.add("connected")
    if iso == cnt: f.add("allisolated")
    # bounding box
    if cells:
        ri = [i for i, j in cells]; ci = [j for i, j in cells]
        f.add("bbh:%d" % (max(ri) - min(ri) + 1)); f.add("bbw:%d" % (max(ci) - min(ci) + 1))
        if max(ri) - min(ri) == max(ci) - min(ci): f.add("bbsquare")
    f.add("diag:%d" % sum(1 for i in range(min(n, m)) if rows[i][i] == "#"))
    f.add("border:%d" % (sum(1 for j in range(m) if rows[0][j] == "#") +
                         sum(1 for j in range(m) if rows[-1][j] == "#") +
                         sum(1 for i in range(1, n-1) if rows[i][0] == "#") +
                         sum(1 for i in range(1, n-1) if rows[i][-1] == "#")))
    f.add("rowpat:" + ("y" if len(set(rc)) <= 2 else "n"))
    at = ["".join(rows[n-1-i][m-1-j] for i in range(n)) for j in range(m)]
    if rows == at: f.add("symAT")
    r90 = ["".join(rows[n-1-i][j] for i in range(n)) for j in range(m)]
    if rows == r90: f.add("symR90")
    f.add("rcset:" + ",".join(str(x) for x in sorted(rc)))
    f.add("ccset:" + ",".join(str(x) for x in sorted(cc)))
    q = [0, 0, 0, 0]
    for i in range(n):
        for j in range(m):
            if rows[i][j] == "#":
                q[(0 if i < n // 2 else 2) + (0 if j < m // 2 else 1)] += 1
    f.add("quad:" + ",".join(str(x) for x in q))
    f.add("quadmax:%d" % max(q))
    if len(set(q)) == 1: f.add("quadeq")
    n2 = 0
    for i in range(n - 1):
        for j in range(m - 1):
            if rows[i][j] == rows[i][j+1] == rows[i+1][j] == rows[i+1][j+1] == "#":
                n2 += 1
    f.add("n2x2:%d" % n2)
    top = sum(rc[:n // 2]); bot = sum(rc[n // 2 + 1:])
    f.add("tbeq:%d" % (top == bot))
    lft = sum(cc[:m // 2]); rgt = sum(cc[m // 2 + 1:])
    f.add("lreq:%d" % (lft == rgt))
    f.add("touchborder:%d" % (1 if any(rows[0][j] == "#" or rows[-1][j] == "#" for j in range(m))
                              or any(rows[i][0] == "#" or rows[i][-1] == "#" for i in range(n)) else 0))
    per = 0
    for i in range(n):
        for j in range(m):
            if rows[i][j] == "#":
                for (a, b) in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)):
                    if not (0 <= a < n and 0 <= b < m) or rows[a][b] != "#":
                        per += 1
    f.add("per:%d" % per)
    return f


# ---------------------------------------------------------------- engine
LOW = ("first2:", "last2:", "vpat:", "sum%", "maxlet:", "minlet:", "vfirstpos:",
       "bi:", "rcset:", "ccset:", "quad:", "per:", "digsum:", "rsum:", "sum:",
       "prod%", "sumfl:", "mid:", "nplen:", "rowpat:", "half:", "major:",
       "tot%", "hm%", "angdiv30:")
HIGH = ("mdiv", "m=", "cnt", "run", "maxrun", "sym", "has", "lacks", "no",
        "doubleletter", "alldistinct", "repdist:", "hasv:", "nov:", "vset:",
        "digsumpar", "mrepdig", "hdividesm", "adjinc1", "adjdec1", "adjabs1",
        "palin", "nondec", "noninc", "strictinc", "strictdec", "connected",
        "comps:", "iso:", "haspair", "flush", "consec2", "fullrows", "fullcols")


LEARNED = {'borsel': {'adjabs': 0.55, 'adjdec': 0.55, 'adjeq': 0.55, 'adjinc': 0.55, 'cnt': 0.55, 'cntmax': 0.55, 'cntmin': 1.276, 'first': 0.797, 'first<last': 0.713, 'firsteqlast': 0.922, 'firstpar': 0.55, 'has': 0.613, 'lacks': 0.55, 'last': 0.55, 'lastpar': 0.55, 'max': 1.573, 'maxrun': 0.55, 'mid': 0.903, 'nd': 1.503, 'ngt': 0.55, 'nondec': 1.222, 'noninc': 0.663, 'p': 0.55, 'p0par': 0.55, 'p1par': 0.55, 'p2par': 1.178, 'p3par': 0.55, 'p4par': 0.55, 'prod%': 0.55, 'rng': 1.052, 'sum%': 0.55, 'sumfl': 0.768}, 'dornic': {'adjsuit': 0.859, 'black': 0.826, 'blackpar': 0.55, 'cntC': 1.077, 'cntD': 1.265, 'cntS': 1.474, 'consec': 0.593, 'first': 1.126, 'firsts': 0.843, 'hasC': 0.629, 'hasD': 0.784, 'hasH': 0.919, 'hasr': 0.55, 'lastr': 1.113, 'lasts': 0.55, 'maxrun': 0.789, 'nev': 1.406, 'nevpar': 1.495, 'nface': 1.373, 'nhigh': 0.777, 'nlow': 0.561, 'noC': 1.077, 'nodd': 0.754, 'noddpar': 0.767, 'nor': 0.574, 'nsuits': 1.377, 'rdistinct': 0.55, 'red': 1.506, 'redpar': 0.638, 'rmax': 1.113, 'rmin': 1.126, 'rrng': 1.799, 'rsum%': 1.047, 'sfl': 0.697}, 'ospren': {'bbh': 1.314, 'bbsquare': 1.067, 'border': 1.061, 'br': 0.77, 'ccmax': 0.55, 'ccmin': 0.55, 'corners': 1.608, 'diag': 0.657, 'duprow': 1.058, 'fullcols': 1.338, 'fullrows': 1.594, 'has2x': 0.648, 'lreq': 0.59, 'n2x': 0.624, 'per': 0.851, 'quadmax': 1.131, 'rcmax': 1.099, 'rcmin': 0.729, 'rowpat': 1.141, 'symLR': 1.335, 'symUD': 1.559, 'tbeq': 0.954, 'tl': 0.917, 'touchborder': 0.901}, 'tavrik': {'adjconsec': 0.562, 'cc': 0.716, 'first<last': 0.603, 'first>last': 0.786, 'has': 0.775, 'hasconsecpair': 0.668, 'hasrepeat': 1.19, 'hasv': 0.55, 'lacks': 0.55, 'last': 1.472, 'maxlet': 0.694, 'minlet': 0.55, 'nc': 0.843, 'ncpar': 1.105, 'nov': 0.55, 'nvpar': 0.688, 'repdist': 1.639, 'startvowel': 1.037, 'sum%': 0.55, 'vfirstpos': 1.037, 'vset': 0.933}, 'tresk': {'bi': 0.55, 'cntB': 0.917, 'cntB>=': 0.718, 'cntBpar': 0.55, 'cntG': 1.371, 'cntG>=': 0.847, 'cntGpar': 0.8, 'cntR': 1.264, 'cntR>=': 0.704, 'cntRpar': 0.823, 'dblB': 0.55, 'dblG': 0.55, 'dblR': 0.55, 'half': 0.55, 'hasdouble': 0.762, 'maxrun': 0.55, 'maxrun>=': 0.63, 'runB': 0.752, 'runB>=': 0.55, 'runG': 0.55, 'runG>=': 0.55, 'runR': 0.562, 'runR>=': 0.55, 'trpB': 0.858, 'trpG': 0.55, 'trpR': 0.846}, 'wisbek': {'angdiv': 0.948, 'dig': 0.55, 'digdistinct': 0.815, 'digsum%': 0.55, 'digsumpar': 0.55, 'hdiv': 0.639, 'hdividesm': 0.55, 'hm%': 0.585, 'hpar': 0.717, 'hprime': 0.632, 'hsquare': 1.433, 'm=3h': 1.29, 'm=4h': 1.352, 'm>h': 0.756, 'mdiv': 0.55, 'mge': 0.804, 'mgt': 0.584, 'mlt': 0.55, 'mone': 0.55, 'mpar': 0.632, 'mprime': 0.893, 'mrepdig': 1.374, 'mten': 0.554, 'nodig': 0.55, 'nplen': 1.472, 'tot%': 0.55}}


def fam(f):
    b = f.split(":")[0]
    i = len(b)
    while i and b[i - 1].isdigit():
        i -= 1
    return b[:i]


PLAIN = ("dornic",)


def prior(f):
    for p in LOW:
        if f.startswith(p):
            return 0.25
    for p in HIGH:
        if f.startswith(p):
            return 1.6
    return 1.0


def pick(pos_feats, cand_feats, lw=None, use_prior=True):
    if not pos_feats or not cand_feats:
        return 0
    consistent = set(pos_feats[0])
    for p in pos_feats[1:]:
        consistent &= p
    k = len(cand_feats)
    scores = [0.0] * k
    for f in consistent:
        hits = [i for i in range(k) if f in cand_feats[i]]
        h = len(hits)
        if h == 0 or h == k:
            continue
        w = 1.0 / (h * h)
        if use_prior:
            w *= prior(f)
            if lw:
                w *= lw.get(fam(f), 1.0)
        for i in hits:
            scores[i] += w
    best = 0; bv = -1.0
    for i in range(k):
        if scores[i] > bv:
            bv = scores[i]; best = i
    return best


def parse_mc(clue):
    blocks = clue.split("\n\n")
    pos = [l for l in blocks[0].split("\n") if l.strip()]
    cands = [l for l in blocks[1].split("\n") if l.strip()]
    return pos, cands


def parse_ospren(clue):
    blocks = [b for b in clue.split("\n\n") if b.strip()]
    pos = []
    cands = []
    for b in blocks:
        lines = [l for l in b.split("\n") if l.strip()]
        if lines and lines[0].strip().isdigit():
            cands.append((lines[0].strip(), lines[1:]))
        else:
            pos.append(lines)
    return pos, cands


FEAT = {"tavrik": f_word, "wisbek": f_time, "tresk": f_colors, "dornic": f_hand}


def solve_mc(name, clue):
    if name == "ospren":
        pos, cands = parse_ospren(clue)
        pf = [f_grid(g) for g in pos]
        cf = [f_grid(g) for (_, g) in cands]
        i = pick(pf, cf, LEARNED.get("ospren"), True)
        return cands[i][0], "\n".join(cands[i][1]), i
    pos, cands = parse_mc(clue)
    if name == "borsel":
        fn = lambda s: f_nums([int(x) for x in s.split()])
    else:
        fn = FEAT[name]
    pf = [fn(p) for p in pos]
    cf = [fn(c) for c in cands]
    i = pick(pf, cf, LEARNED.get(name), name not in PLAIN)
    return str(i + 1), cands[i], i


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1
    memory["cache"] = {}


MC = ("tavrik", "wisbek", "tresk", "dornic", "borsel", "ospren")


def solve(name, clue, memory):
    try:
        if name == "norvel":
            return solve_norvel(clue)
        if name in MC:
            num, text, _ = solve_mc(name, clue)
            return num
    except Exception:
        return None
    return None


def on_round_end(items, memory):
    pass
