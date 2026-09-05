"""strategy.py - team kelmar1a."""

import re

LETTERS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# ---------------------------------------------------------------- helpers
def split_pic(clue):
    """Return (picture_lines, tail_lines) splitting at the '===' rule line."""
    lines = clue.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("="):
            return lines[:i], lines[i:]
    return lines[:-1], lines[-1:]


def pad(lines):
    w = max(len(l) for l in lines)
    return [list(l.ljust(w)) for l in lines], w


def join(grid, orig):
    out = []
    for row, o in zip(grid, orig):
        s = "".join(row).rstrip()
        if len(s) < len(o):
            s = "".join(row)[: len(o)]
        out.append(s)
    return out


# ---------------------------------------------------------------- durnel
def solve_durnel(clue):
    pic, tail = split_pic(clue)
    grid, W = pad(pic)
    G = len(pic) - 1
    ground = grid[G]
    cars = []
    s = "".join(ground)
    for m in re.finditer(r"<([A-Z])\1|([A-Z])\2>", s):
        p = m.start()
        d = -1 if m.group(0)[0] == "<" else 1
        h = 0
        for r in range(G):
            if grid[r][p + 1] in LETTERS:
                h += 1
        cars.append((p, d, h))
    bridges = []
    for r in range(G):
        for m in re.finditer(r"#+", "".join(grid[r])):
            bridges.append((m.start(), m.end() - 1, G - r - 1))
    for p, d, h in cars:
        turn = False
        for a, b, cl in bridges:
            if cl < h and ((d > 0 and a > p + 2) or (d < 0 and b < p)):
                turn = True
                break
        if turn:
            if d > 0:
                ch = grid[G][p]
                grid[G][p], grid[G][p + 1], grid[G][p + 2] = "<", ch, ch
            else:
                ch = grid[G][p + 1]
                grid[G][p], grid[G][p + 1], grid[G][p + 2] = ch, ch, ">"
    return "\n".join(join(grid, pic) + tail)


# ---------------------------------------------------------------- fennick
def solve_fennick(clue):
    pic, tail = split_pic(clue)
    grid, W = pad(pic)
    G = len(pic) - 1
    h = [0] * W
    occ = [False] * W
    for c in range(W):
        if grid[G][c] in LETTERS:
            occ[c] = True
            n = 0
            for r in range(G + 1):
                if grid[r][c] in LETTERS:
                    n += 1
            h[c] = n
    falls = []
    for c in range(W):
        if not occ[c]:
            continue
        for d in (-1, 1):
            g = c + d
            f = c + 2 * d
            o = c - d
            if (0 <= g < W and 0 <= f < W and not occ[g] and occ[f]
                    and h[f] > h[c] and 0 <= o < W and occ[o]):
                falls.append((c, d))
                break
    for c, d in falls:
        for r in range(G):
            ch = grid[r][c]
            if ch != " ":
                grid[r][c] = " "
                grid[r][c + d] = ("\\" if d < 0 else "/") if ch == "_" else ch
    return "\n".join(join(grid, pic) + tail)


# ---------------------------------------------------------------- kelmar
def solve_kelmar(clue, variant):
    """Objects (* or Y) touching a FULL-HEIGHT tree lean.  Verified: the number of
    such objects equals the clue's N on 67/67 samples."""
    lines = clue.split("\n")
    tail = lines[-1]
    pic = lines[:-1]
    grid, W = pad(pic)
    G = len(pic) - 1
    maxh = len(pic) - 2
    top = "".join(grid[0])
    for m in re.finditer(r"\(~+\)", top):
        a, b = m.start(), m.end() - 1
        ht = 0
        for r in range(1, G):
            if grid[r][a] == "'":
                ht += 1
        if ht != maxh:
            continue
        for c, side in ((a - 1, -1), (b + 1, 1)):
            if 0 <= c < W and grid[G][c] in "*Y":
                if variant == 0:
                    grid[G][c] = "\\" if side > 0 else "/"
                else:
                    grid[G][c] = "\\"
    return "\n".join(join(grid, pic) + [tail])


# ---------------------------------------------------------------- basten
def basten_parse(clue):
    lines = clue.split("\n")
    N = int(lines[-1].strip())
    pic = lines[:-1]
    grid, W = pad(pic)
    G = len(pic) - 1
    plants = {}
    for c in range(W):
        h = 0
        for r in range(G):
            if grid[r][c] == "|":
                h += 1
        if h:
            plants[c] = h
    return lines, pic, grid, W, G, N, plants


def solve_basten(clue, variant):
    lines, pic, grid, W, G, N, plants = basten_parse(clue)
    cols = sorted(plants)
    if variant == 0:                      # a bubble above the N tallest plants
        order = sorted(cols, key=lambda c: (-plants[c], c))
        k = 0
        for i in range(N):
            c = order[i % len(order)]
            r = G - plants[c] - 1 - (i // len(order))
            if 1 <= r < G:
                grid[r][c] = "o"
    elif variant == 1:                    # N bubbles spread along the top row
        for i in range(N):
            c = int((i + 1) * W / (N + 1))
            if 0 <= c < W:
                grid[1][c] = "o"
    elif variant == 2 or variant == 3:    # slide every plant N columns
        d = N if variant == 2 else -N
        for r in range(G):
            row = grid[r][:]
            for c in range(W):
                if grid[r][c] == "|":
                    grid[r][c] = "."
            for c in range(W):
                if row[c] == "|" and 0 <= c + d < W:
                    grid[r][c + d] = "|"
    elif variant == 4:                    # exactly N plants
        if len(cols) > N:
            for c in sorted(cols, key=lambda c: (plants[c], c))[: len(cols) - N]:
                for r in range(G):
                    if grid[r][c] == "|":
                        grid[r][c] = "."
        else:
            gaps = sorted(((cols[i + 1] - cols[i], i) for i in range(len(cols) - 1)),
                          reverse=True)
            for j in range(N - len(cols)):
                if j < len(gaps):
                    c = (cols[gaps[j][1]] + cols[gaps[j][1] + 1]) // 2
                    grid[G - 1][c] = "|"
    else:                                 # add N segments, tallest plants first
        add = N
        h = dict(plants)
        order = sorted(cols, key=lambda c: (-plants[c], c))
        i = 0
        while add > 0 and i < 100:
            c = order[i % len(order)]
            if h[c] < G - 1:
                h[c] += 1
                grid[G - h[c]][c] = "|"
                add -= 1
            i += 1
    return "\n".join(join(grid, pic) + [lines[-1]])


# ---------------------------------------------------------------- tovel
def tovel_days(body):
    out = []
    for i, l in enumerate(body):
        for m in re.finditer(r"(\d+)\.", l):
            out.append((int(m.group(1)), i, m.end() - 1, m.start()))
    return out


def solve_tovel(clue, variant):
    lines = clue.split("\n")
    letter, n, d = lines[-1].strip().split("/")
    n = int(n)
    d = int(d)
    body = lines[:-1]
    days = tovel_days(body)
    last = max(x[0] for x in days)
    wd = {}
    for day, li, dot, start in days:
        wd[day] = start // 4
    tail = True
    numform = False
    if variant == 0:                    # the n-th <weekday of day d> of the month
        same = sorted(day for day in wd if wd[day] == wd.get(d))
        marked = {same[n - 1]} if len(same) >= n else {same[-1]}
    elif variant == 1:                  # every n days from d, no code line
        marked = set(range(d, last + 1, n))
        tail = False
    elif variant == 2:                  # only day d, no code line
        marked = {d}
        tail = False
    elif variant == 3:                  # every day congruent to d modulo n
        marked = {day for day in wd if (day - d) % n == 0}
    elif variant == 4:                  # n weeks after d
        marked = {d + 7 * n} if d + 7 * n <= last else {d}
    else:                               # every n days, letter over the number
        marked = set(range(d, last + 1, n))
        numform = True
    out = [list(l) for l in body]
    for day, li, dot, start in days:
        if day in marked:
            if numform:
                for j in range(start, dot):
                    out[li][j] = " "
                out[li][dot - 1] = letter
            else:
                out[li][dot] = letter
    res = ["".join(r) for r in out]
    if tail:
        res.append(lines[-1])
    return "\n".join(res)


# ---------------------------------------------------------------- virel
def blocks_of(row):
    return [len(x) for x in re.findall(r"\[-*\]", row)]


def spans_of(widths):
    s = 0
    out = []
    for w in widths:
        out.append((s, s + w))
        s += w
    return out


def solve_virel(clue):
    """A new course on top whose blocks coincide with exactly N blocks below."""
    lines = clue.split("\n")
    N = int(lines[-1].strip())
    rows = lines[:-1]
    W = len(rows[0])
    below = set(spans_of(blocks_of(rows[0])))
    dead = set()

    def dfs(pos, matched, acc):
        if pos == W:
            return acc if matched == N else None
        if matched > N or (pos, matched) in dead:
            return None
        for w in (2, 3, 4, 5, 6):
            e = pos + w
            if e > W or (W - e == 1):
                continue
            r = dfs(e, matched + (1 if (pos, e) in below else 0), acc + [w])
            if r is not None:
                return r
        dead.add((pos, matched))
        return None

    got = dfs(0, 0, [])
    if got is None:
        return None
    new = "".join("[" + "-" * (w - 2) + "]" for w in got)
    return "\n".join([new] + rows)


# ---------------------------------------------------------------- norvel
def solve_norvel(clue, variant):
    lines = clue.split("\n")
    n = int(lines[-1].split("=")[1])
    kick = lines[0]
    snare = lines[1]
    pre = 6
    kb = kick[pre:]
    cells = [i for i, ch in enumerate(kb) if ch != "|"]
    T = len(cells)
    hits = [k for k, i in enumerate(cells) if kb[i] == "x"]
    tail = True
    mirror = False
    if n == 2:
        sh = n
    elif variant == 0:
        sh = n
    elif variant == 1:
        sh = 2 * n
    elif variant == 2:
        sh = 2
    elif variant == 3:
        sh = -n
    elif variant == 4:
        sh = n
        tail = False
    else:
        sh = 0
        mirror = True
    if mirror:
        out = {T - 1 - h for h in hits}
    else:
        out = {(h + sh) % T for h in hits}
    sb = list(snare)
    for s in out:
        sb[pre + cells[s]] = "x"
    res = [kick, "".join(sb)] + lines[2:]
    if not tail:
        res = res[:-1]
    return "\n".join(res)


# ---------------------------------------------------------------- driver
# FINAL SETTINGS
#   durnel  / fennick / kelmar / virel : solved, 100% in training
#   tovel   : best guess (every n days from d, code line dropped) ~8%
#   norvel  : only n == 2 is understood (kick rotated n steps) ~50%
#   basten  : never cracked - skip (a skip is instant and keeps the tiebreak)


def on_round_start(memory):
    memory["_n"] = {}


def solve(name, clue, memory):
    try:
        if name == "durnel":
            return solve_durnel(clue)
        if name == "fennick":
            return solve_fennick(clue)
        if name == "kelmar":
            return solve_kelmar(clue, 0)
        if name == "virel":
            return solve_virel(clue)
        if name == "tovel":
            return solve_tovel(clue, 1)
        if name == "norvel":
            if clue.rsplit("=", 1)[-1].strip() == "2":
                return solve_norvel(clue, 0)
            return None
        return None
    except Exception:
        return None


def on_round_end(items, memory):
    pass
