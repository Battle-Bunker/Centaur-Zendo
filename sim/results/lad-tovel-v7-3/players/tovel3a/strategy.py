"""Centaur Zendo strategy.

Every clue ends with a line "<N> <word>": N = how many edits the answer needs.
N == 0  ->  the clue itself is the answer (verified: 100% hit rate).
"""
import re

FISH = re.compile(r'><>|<><')
TREE = re.compile(r'\(~+\)')
CELL = '\\__/'


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


# ---------------------------------------------------------------- helpers
def split_clue(clue):
    lines = clue.split('\n')
    tail = lines[-1]
    n = int(tail.split()[0])
    return lines[:-1], tail, n


def join(body, tail):
    return '\n'.join(body + [tail])


# ---------------------------------------------------------------- molvic
def solve_molvic(body, tail):
    idx = [i for i, l in enumerate(body) if '|' in l and l[:1] != ' ']
    labs = []
    grid = []
    for i in idx:
        lab, rest = body[i].split('|', 1)
        labs.append(lab.strip().lower())
        grid.append(rest.rstrip('|').split(' '))
    pos = {l: r for r, l in enumerate(labs)}
    C = len(grid[0])
    blanks = {r: [c for c in range(C) if grid[r][c] == '___'] for r in range(len(labs))}
    used = {r: 0 for r in range(len(labs))}
    moves = []
    for r in range(len(labs)):
        for c in range(C):
            v = grid[r][c]
            if v == '___' or v == labs[r]:
                continue
            hr = pos.get(v)
            if hr is None:
                continue
            if not blanks[hr]:
                continue
            if grid[hr][c] != labs[r]:
                continue
            if used[hr] >= len(blanks[hr]):
                continue
            dest = blanks[hr][used[hr]]
            used[hr] += 1
            moves.append((r, c, hr, dest, v))
    for (r, c, hr, dest, v) in moves:
        grid[r][c] = '___'
        grid[hr][dest] = v
    out = list(body)
    for k, i in enumerate(idx):
        lab, rest = body[i].split('|', 1)
        out[i] = lab + '|' + ' '.join(grid[k]) + '|'
    return join(out, tail)


# ---------------------------------------------------------------- kelmar
def solve_kelmar(body, tail):
    rows = body[:-1]
    ground = list(body[-1])
    trees = []
    for m in TREE.finditer(rows[0]):
        s, e = m.start(), m.end()
        h = 0
        for r in range(1, len(rows)):
            if rows[r][s:e] == "'" * (e - s):
                h += 1
            else:
                break
        trees.append((s, e, h))
    if not trees:
        return join(body, tail)
    mx = max(t[2] for t in trees)
    for (s, e, h) in trees:
        if h < mx:
            continue
        if s - 1 >= 0 and ground[s - 1] in '*Y':
            ground[s - 1] = '/'
        if e < len(ground) and ground[e] in '*Y':
            ground[e] = '\\'
    return join(rows + [''.join(ground)], tail)


# ---------------------------------------------------------------- felsim
def felsim_rows(body):
    rows = []
    keep = []
    for i, l in enumerate(body):
        if CELL in l:
            p = set()
            j = l.find(CELL)
            while j >= 0:
                p.add(j)
                j = l.find(CELL, j + 1)
            rows.append(p)
            keep.append(i)
    return rows, keep


def felsim_tips(rows):
    out = []
    R = len(rows)
    for r in range(R):
        above = rows[r - 1] if r > 0 else set()
        below = rows[r + 1] if r + 1 < R else None
        for p in rows[r]:
            if (p - 2) in above or (p + 2) in above:
                continue
            if below is None:
                continue
            l = (p - 2) in below
            rt = (p + 2) in below
            if l ^ rt:
                out.append((r, p, 'L' if l else 'R'))
    return out


def felsim_render(body, keep, rows):
    out = list(body)
    for k, i in enumerate(keep):
        W = max([p + 4 for p in rows[k]] + [0])
        buf = [' '] * W
        for p in sorted(rows[k]):
            buf[p:p + 4] = list(CELL)
        out[i] = ''.join(buf)
    return out


def solve_felsim(body, tail, variant):
    rows, keep = felsim_rows(body)
    tips = felsim_tips(rows)
    if not tips:
        return join(body, tail)
    if variant == 0:                       # they fall, and whatever that frees falls too
        for _ in range(8):
            t = felsim_tips(rows)
            if not t:
                break
            for (r, p, side) in t:
                rows[r].discard(p)
    elif variant == 1:                     # it rolls off and settles on the pile
        for (r, p, side) in tips:
            rows[r].discard(p)
            rr, pp = r, p
            while rr + 1 < len(rows):
                np_ = pp + 2 if side == 'L' else pp - 2
                bl = rows[rr + 1]
                if np_ in bl:
                    break
                rr, pp = rr + 1, np_
                if rr + 1 >= len(rows):
                    break
                l = (pp - 2) in rows[rr + 1]; rt = (pp + 2) in rows[rr + 1]
                if l and rt or not (l or rt):
                    break
                side = 'L' if l else 'R'
            rows[rr].add(pp)
    else:                                  # it swaps down with the one holding it up
        for (r, p, side) in tips:
            q = p - 2 if side == 'L' else p + 2
            rows[r].discard(p)
            rows[r + 1].discard(q)
            rows[r + 1].add(p + 2 if side == 'L' else p - 2)
            rows[r].add(q + 2 if side == 'L' else q - 2)
    return join(felsim_render(body, keep, rows), tail)


# ---------------------------------------------------------------- norvel
def solve_norvel(body, tail, variant):
    labs = []
    bars = []
    for l in body:
        if '|' in l:
            lab, rest = l.split('|', 1)
            labs.append(lab)
            bars.append(rest.rstrip('|').split('|'))
    h, s, k = bars[0], bars[1], bars[2]
    nb = len(h)
    for i in range(nb):
        hb = list(h[i]); sb = list(s[i]); kb = list(k[i])
        spots = [j for j in range(4) if sb[j] == 'x' and hb[j] == '.' and kb[j] == '.']
        if not spots:
            continue
        j = spots[0]
        if variant == 0:
            hb = hb[-1:] + hb[:-1]
        elif variant == 1:
            hb = hb[1:] + hb[:1]
        else:
            if i + 1 < nb:
                nxt = list(s[i + 1])
                if nxt[j] == '.':
                    nxt[j] = 'x'; sb[j] = '.'
                    s[i + 1] = ''.join(nxt)
        h[i] = ''.join(hb); s[i] = ''.join(sb); k[i] = ''.join(kb)
    out = []
    bi = 0
    for l in body:
        if '|' in l:
            out.append(labs[bi] + '|' + '|'.join(bars[bi]) + '|')
            bi += 1
        else:
            out.append(l)
    return join(out, tail)


# ---------------------------------------------------------------- tovel
DAYRE = re.compile(r'(\d+)(\S)')


def tovel_parse(body):
    cells = {}
    for r, l in enumerate(body[1:], 1):
        for m in DAYRE.finditer(l):
            cells[int(m.group(1))] = (r, m.start(2), m.group(2))
    return cells


def solve_tovel(body, tail, variant):
    cells = tovel_parse(body)
    if not cells:
        return join(body, tail)
    days = sorted(cells)
    grid = {d: cells[d][2] for d in days}
    busy = {d for d in days if grid[d] != '.'}
    mids = [d for d in days if d in busy and (d - 1) in busy and (d + 1) in busy]
    if not mids:
        return join(body, tail)
    first, last = days[0], days[-1]
    if variant == 0:                       # the first of the three moves on
        for d in mids:
            t = d - 1
            ch = grid[t]; grid[t] = '.'
            for f in range(t + 1, last + 1):
                if grid.get(f, 'x') == '.':
                    grid[f] = ch; break
    elif variant == 1:                     # forward, wrapping round the month
        for d in mids:
            ch = grid[d]; grid[d] = '.'
            order = list(range(d + 1, last + 1)) + list(range(first, d))
            for f in order:
                if grid.get(f, 'x') == '.':
                    grid[f] = ch; break
    else:                                  # forward, days freed on the way count
        for d in mids:
            ch = grid[d]; grid[d] = '.'
            for f in list(range(d + 1, last + 1)) + list(range(first, d)):
                if grid.get(f, 'x') == '.':
                    grid[f] = ch; break
    out = [list(l) for l in body]
    for d in days:
        r, c, _ = cells[d]
        out[r][c] = grid[d]
    return join([''.join(l) for l in out], tail)


# ---------------------------------------------------------------- durnel
BAY = '\\_/'


def durnel_parse(body):
    while body and body[-1].strip() and set(body[-1].strip()) <= {'='}:
        body = body[:-1]
    road = body[-1]
    above = body[:-1]
    W = max(len(l) for l in body)
    above = [l.ljust(W) for l in above]
    road = road.ljust(W)
    bays = []
    j = road.find(BAY)
    while j >= 0:
        bays.append(j); j = road.find(BAY, j + 1)
    carts = []
    for m in re.finditer(r'([A-Z])\1>', road):
        carts.append((m.start(), m.group()[0], 'R'))
    for m in re.finditer(r'<([A-Z])\1', road):
        carts.append((m.start(), m.group()[1], 'L'))
    carts.sort()
    k = len(above)
    H = {}
    for c, let, d in carts:
        h = 0
        for r in range(k - 1, -1, -1):
            if above[r][c:c + 3] == let * 3:
                h += 1
            else:
                break
        H[c] = h
    obst = [(r, m.start(), m.end()) for r, l in enumerate(above) for m in re.finditer(r'#+', l)]
    return above, road, bays, carts, H, obst, k, W


def durnel_movers(body):
    above, road, bays, carts, H, obst, k, W = durnel_parse(body)
    cand = []
    for c, let, d in carts:
        h = H[c]
        rows = set(range(k - h, k))
        if not rows:
            continue
        blocked_ahead = any(r in rows and ((a >= c + 3) if d == 'R' else (e <= c))
                            for r, a, e in obst)
        if not blocked_ahead:
            continue
        bs = sorted([x for x in bays if (x > c if d == 'R' else x < c)], key=lambda x: abs(x - c))
        for b in bs:
            lo, hi = (c + 3, b) if d == 'R' else (b + 3, c)
            if any(r in rows and not (e <= lo or a >= hi) for r, a, e in obst):
                continue
            cand.append((abs(b - c), c, let, d, b, h))
            break
    cand.sort()
    used = set()
    picked = []
    for dist, c, let, d, b, h in cand:
        if b in used:
            continue
        used.add(b)
        picked.append((c, let, d, b, h))
    return above, road, bays, carts, H, obst, k, W, picked


def solve_durnel(body, tail, variant):
    above, road, bays, carts, H, obst, k, W, picked = durnel_movers(body)
    rows = [list(l.ljust(W)) for l in body[:len(above)]]
    rd = list(road)
    for (c, let, d, b, h) in picked:
        for j in range(3):
            rd[c + j] = '.'
        for r in range(k - h, k):
            for j in range(3):
                rows[r][c + j] = ' '
        txt = ('<' + let + let) if d == 'R' else (let + let + '>')
        for j in range(3):
            rd[b + j] = txt[j]
        for r in range(k - h, k):
            for j in range(3):
                rows[r][b + j] = let
    out = [''.join(r).rstrip() for r in rows] + [''.join(rd).rstrip()] + body[len(above) + 1:]
    return join(out, tail)


# ---------------------------------------------------------------- main
def solve(name, clue, memory):
    try:
        body, tail, n = split_clue(clue)
    except Exception:
        return None
    if n == 0:
        return clue
    i = memory.get('_index', 0)
    try:
        if name == 'molvic':
            return solve_molvic(body, tail)
        if name == 'kelmar':
            return solve_kelmar(body, tail)
        if name == 'felsim':
            return solve_felsim(body, tail, i % 3)
        if name == 'norvel':
            return solve_norvel(body, tail, i % 3)
        if name == 'tovel':
            return solve_tovel(body, tail, i % 3)
        if name == 'durnel':
            return solve_durnel(body, tail, 0)
    except Exception:
        return None
    return None


def on_round_end(items, memory):
    pass
