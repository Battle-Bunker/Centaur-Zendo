"""strategy.py — Centaur Zendo bot (garrow2b)."""
import re

# ---------------------------------------------------------------- helpers
NUM_RE = re.compile(r"^\s*(\d+)(\s+\w+)?\s*$")
GARROW_RE = re.compile(r"^\s*(\S+)\s+(\d+)\s+slices\s*$")


def clue_n(clue):
    """The count of edits the clue advertises, or None."""
    lines = clue.split("\n")
    m = NUM_RE.match(lines[-1])
    if m:
        return int(m.group(1))
    m = GARROW_RE.match(lines[0])
    if m:
        return int(m.group(2))
    return None


# ---------------------------------------------------------------- fennick
def solve_fennick(clue):
    lines = clue.split("\n")
    ri = None
    for i, l in enumerate(lines):
        if l and set(l.strip()) == {"="}:
            ri = i
    if ri is None:
        return None
    pic = lines[:ri]
    tail = lines[ri:]
    w = max(len(l) for l in pic)
    g = [list(l.ljust(w)) for l in pic]
    base = g[-1]
    H = len(g)

    def height(c):
        h = 1
        for r in range(H - 2, -1, -1):
            if g[r][c].isalpha():
                h += 1
            else:
                break
        return h

    falls = []
    for c in range(1, w - 1):
        if base[c] == "." and base[c - 1].isalpha() and base[c + 1].isalpha():
            hl, hr = height(c - 1), height(c + 1)
            if hl == hr:
                continue
            src = c - 1 if hl < hr else c + 1
            lf = base[src - 1] if src > 0 else "X"
            rt = base[src + 1] if src + 1 < w else "X"
            if lf == "." and rt == ".":
                continue      # a tower with a gap on both sides never falls
            falls.append((src, 1 if src == c - 1 else -1))
    out = [row[:] for row in g]
    for col, d in falls:
        for r in range(H - 1):
            ch = g[r][col]
            if ch == " ":
                continue
            out[r][col] = " "
            nc = col + d
            if 0 <= nc < w:
                out[r][nc] = ch if ch != "_" else ("/" if d > 0 else "\\")
    return "\n".join([("".join(row)).rstrip() for row in out] + tail)


# ---------------------------------------------------------------- molvic
SHELF_RE = re.compile(r"^(\S+)(\s+)\|(.*)\|$")


def solve_molvic(clue):
    lines = clue.split("\n")
    rows = []
    for i, l in enumerate(lines):
        m = SHELF_RE.match(l)
        if m:
            rows.append([i, m.group(1).lower(), m.group(3).split(" "),
                         m.group(1) + m.group(2)])
    if len(rows) < 2:
        return None
    labels = [r[1] for r in rows]
    grid = [r[2] for r in rows]
    ncol = len(grid[0])
    nr = len(rows)
    gaps = [[c for c in range(ncol) if grid[r][c] == "___"] for r in range(nr)]
    ptr = [0] * nr
    new = [row[:] for row in grid]
    for c in range(ncol):
        for i in range(nr):
            gi = grid[i][c]
            if gi == "___" or gi == labels[i]:
                continue
            for j in range(i + 1, nr):
                if gi == labels[j] and grid[j][c] == labels[i]:
                    for src, dst in ((i, j), (j, i)):
                        if ptr[dst] < len(gaps[dst]):
                            new[dst][gaps[dst][ptr[dst]]] = labels[dst]
                            ptr[dst] += 1
                            new[src][c] = "___"
    out = list(lines)
    for k, r in enumerate(rows):
        out[r[0]] = r[3] + "|" + " ".join(new[k]) + "|"
    return "\n".join(out)


# ---------------------------------------------------------------- durnel
CAR_RE = re.compile(r"(<)([A-Z]{2})|([A-Z]{2})(>)")


def solve_durnel(clue, n):
    lines = clue.split("\n")
    ri = None
    for i, l in enumerate(lines):
        if l and set(l.strip()) == {"="}:
            ri = i
    if ri is None:
        return None
    road = lines[ri - 1]
    cars = []  # (start, end_exclusive, letters, dir)
    for m in CAR_RE.finditer(road):
        if m.group(1):
            cars.append([m.start(), m.end(), m.group(2), -1])
        else:
            cars.append([m.start(), m.end(), m.group(3), 1])

    def looks(i, d):
        """what the car meets looking in direction d: 'hole','car',None"""
        s, e = cars[i][0], cars[i][1]
        pos = (e if d > 0 else s - 1)
        while 0 <= pos < len(road):
            ch = road[pos]
            if ch == ".":
                pos += d
                continue
            if ch in "\\_/":
                return "hole"
            return "car"
        return None

    turn = []
    for i in range(len(cars)):
        if looks(i, cars[i][3]) == "hole" and looks(i, -cars[i][3]) != "hole":
            turn.append(i)
    if len(turn) != n:
        return None
    ro = list(road)
    for i in turn:
        s, e, let, d = cars[i]
        if d < 0:
            ro[s], ro[s + 1], ro[s + 2] = let[0], let[1], ">"
        else:
            ro[s], ro[s + 1], ro[s + 2] = "<", let[0], let[1]
    lines[ri - 1] = "".join(ro)
    return "\n".join(lines)


# ---------------------------------------------------------------- virel
BOX_RE = re.compile(r"\[-*\]")


def virel_parse(clue):
    L = clue.split("\n")
    n = None
    body = L
    if re.fullmatch(r"\s*\d+\s*", L[-1]):
        n = int(L[-1]); body = L[:-1]
    rows = [[len(b) for b in BOX_RE.findall(l)] for l in body]
    return [r for r in rows if r], n, body


def virel_render(row):
    return "".join("[" + "-" * (w - 2) + "]" for w in row)


def virel_build(clue, which=None):
    rows, n, body = virel_parse(clue)
    if not rows:
        return None
    # empirically: the top row is never the source; second-from-bottom scores best
    src = rows[max(0, len(rows) - 2)]
    usage = {}
    for r in rows:
        p = 0
        for w in r[:-1]:
            p += w
            usage[p] = usage.get(p, 0) + 1
    out = []
    pos = 0
    for w in src:
        k = w // 2
        if w % 2 == 0:
            out.extend([2] * k)
        else:
            best = None
            for i in range(k):
                cand = [2] * k
                cand[i] = 3
                p = pos; cost = 0
                for x in cand[:-1]:
                    p += x; cost += usage.get(p, 0)
                if best is None or cost < best[0]:
                    best = (cost, cand)
            out.extend(best[1])
        pos += w
    return "\n".join([virel_render(out)] + body)


VMODES = ["last", "fewest", "byN", "byNegN"]


# ---------------------------------------------------------------- api
def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        n = clue_n(clue)
        if n == 0 and name != "virel":
            return clue
        if name == "fennick":
            return solve_fennick(clue)
        if name == "molvic":
            return solve_molvic(clue)
        if name == "virel":
            return virel_build(clue)
    except Exception:
        return None
    return None


def on_round_end(items, memory):
    pass
