"""FINAL strategy.

Solved:
  fennick - the shorter pile beside a single-column gap leans into it (100%)
  durnel  - a car whose load would hit a bridge ahead turns round (100%)
  virel   - add a course of bricks with exactly n bricks directly on a brick (100%)
Partial:
  kelmar  - only the "0 lean" cases (identity); others skipped
  tovel   - m == 2 solved (3 marks); other m are hedged guesses
  norvel  - midpoint-of-kick-gaps, only for n == 2
Unsolved:
  basten  - skipped (a skip costs no time and helps the precision tiebreak)
"""
import re

BLK = re.compile(r'\[-*\]')
CAR_RE = re.compile(r'<[A-Z]{2}|[A-Z]{2}>')
HASH = re.compile(r'#+')


# ---------------- fennick ----------------
def solve_fennick(clue):
    lines = clue.split('\n')
    sep = -1
    for i, l in enumerate(lines):
        if l and set(l) == {'='}:
            sep = i
            break
    if sep < 0:
        return None
    pic = lines[:sep]
    H = len(pic); W = max(len(r) for r in pic)
    g = [list(r.ljust(W)) for r in pic]
    hs = [sum(1 for y in range(H) if g[y][x].isalpha()) for x in range(W)]
    def h(i): return hs[i] if 0 <= i < W else 0
    leans = []
    for gp in range(W):
        if h(gp) != 0:
            continue
        l, r = h(gp - 1), h(gp + 1)
        if l > 0 and r > 0 and l != r:
            if l < r:
                c = gp - 1
                if h(c - 1) > 0:
                    leans.append((c, gp))
            else:
                c = gp + 1
                if h(c + 1) > 0:
                    leans.append((c, gp))
    for c, gp in leans:
        hh = hs[c]; top = H - 1 - hh
        g[top][c] = ' '
        g[top][gp] = '/' if gp > c else '\\'
        for y in range(H - hh, H - 1):
            g[y][gp] = g[y][c]; g[y][c] = ' '
    return '\n'.join([''.join(r).rstrip() for r in g] + lines[sep:])


# ---------------- durnel ----------------
def solve_durnel(clue):
    lines = clue.split('\n')
    sep = -1
    for i, l in enumerate(lines):
        if l and set(l) == {'='}:
            sep = i
            break
    if sep < 0:
        return None
    pic = lines[:sep]
    W = max(len(r) for r in pic)
    g = [list(r.ljust(W)) for r in pic]
    H = len(g)
    road = ''.join(g[H - 1])
    blocks = []
    for y in range(H - 1):
        for m in HASH.finditer(''.join(g[y])):
            blocks.append((y, m.start(), m.end() - 1))
    for m in CAR_RE.finditer(road):
        s = m.start(); tok = m.group()
        right = tok[2] == '>'
        h = 0
        for y in range(H - 2, -1, -1):
            if g[y][s].isalpha():
                h += 1
            else:
                break
        lim = H - 1 - h
        for y, a, b in blocks:
            if right and b < s + 2:
                continue
            if (not right) and a > s:
                continue
            if y >= lim:
                letters = tok.strip('<>')
                new = ('<' + letters) if right else (letters + '>')
                g[H - 1][s], g[H - 1][s + 1], g[H - 1][s + 2] = new[0], new[1], new[2]
                break
    return '\n'.join([''.join(r).rstrip() for r in g] + lines[sep:])


# ---------------- virel ----------------
def _spans(row):
    out = []; t = 0
    for b in BLK.findall(row):
        out.append((t, t + len(b) - 1)); t += len(b)
    return out


def solve_virel(clue):
    lines = clue.split('\n')
    rows = lines[:-1]; n = int(lines[-1].strip())
    W = len(rows[0]); below = set(_spans(rows[0]))
    res = []; dead = set()
    def rec(pos, used):
        if pos == W:
            return used == n
        if used > n or (pos, used) in dead:
            return False
        for s in (3, 4, 5, 6, 2):
            np = pos + s
            if np > W or (np != W and W - np < 2):
                continue
            u = used + (1 if (pos, np - 1) in below else 0)
            if u > n:
                continue
            res.append(s)
            if rec(np, u):
                return True
            res.pop()
        dead.add((pos, used))
        return False
    if not rec(0, 0):
        return None
    new = ''.join('[' + '-' * (s - 2) + ']' for s in res)
    return '\n'.join([new] + rows)


# ---------------- kelmar (only the trivial cases) ----------------
def solve_kelmar(clue):
    if clue.rstrip().endswith('0 lean'):
        return clue
    return None


# ---------------- norvel ----------------
def solve_norvel(clue):
    lines = clue.split('\n')
    kick = lines[0]
    n = int(lines[2].split('=')[1])
    if n != 2:
        return None
    snare = list(lines[1]); tail = lines[2:]
    nb = kick.count('|') - 1; S = nb * 4
    def pos(i): return 6 + 1 + (i // 4) * 5 + (i % 4)
    kb = [1 if kick[pos(i)] == 'x' else 0 for i in range(S)]
    groups = []; i = 0
    while i < S:
        if kb[i]:
            j = i
            while j + 1 < S and kb[j + 1]:
                j += 1
            groups.append((i, j - i + 1)); i = j + 1
        else:
            i += 1
    out = [0] * S
    for k in range(len(groups) - 1):
        st, w = groups[k]
        ns = (st + groups[k + 1][0]) // 2
        for t in range(ns, min(ns + w, S)):
            out[t] = 1
    for i in range(S):
        p = pos(i)
        if p < len(snare):
            snare[p] = 'x' if out[i] else '.'
    return '\n'.join([kick, ''.join(snare)] + tail)


# ---------------- tovel ----------------
def solve_tovel(clue, alt):
    lines = clue.split('\n')
    code = lines[-1]
    letter, m, d = code.split('/'); m = int(m); d = int(d)
    if m <= 2:
        count = 3
    else:
        count = (m + 1) if alt else (2 * m - 1)
    rows = [list(r) for r in lines[:-1]]
    cells = {}
    for y in range(1, len(rows)):
        r = rows[y]
        for b in range(7):
            i = b * 4
            if i + 2 < len(r) and r[i + 2] == '.':
                t = ''.join(r[i:i + 2]).strip()
                if t.isdigit():
                    cells[int(t)] = (y, i + 2)
    for k in range(count):
        day = d + k * m
        if day in cells:
            y, x = cells[day]
            rows[y][x] = letter
    return '\n'.join([''.join(r) for r in rows] + [code])


def solve(name, clue, memory):
    try:
        if name == "fennick":
            return solve_fennick(clue)
        if name == "durnel":
            return solve_durnel(clue)
        if name == "virel":
            return solve_virel(clue)
        if name == "kelmar":
            return solve_kelmar(clue)
        if name == "norvel":
            return solve_norvel(clue)
        if name == "tovel":
            return solve_tovel(clue, memory.get("_index", 0) % 2)
        # basten: no working hypothesis - skip (free, and helps the tiebreak)
        return None
    except Exception:
        return None


def on_round_end(items, memory):
    pass
