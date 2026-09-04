"""Round 4 probe: staggered lego walls, tovel rota rules, new ideas elsewhere."""

A = ord('A')
DAYS = " Mo  Tu  We  Th  Fr  Sa  Su"
KEYPAD = {}
for _digit, _letters in [('2', 'ABC'), ('3', 'DEF'), ('4', 'GHI'), ('5', 'JKL'),
                         ('6', 'MNO'), ('7', 'PQRS'), ('8', 'TUV'),
                         ('9', 'WXYZ')]:
    for _c in _letters:
        KEYPAD[_c] = _digit
MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
}


# ---------------- LegoZendo2 ----------------
def stagger(top, bot, n, m=None, gap=1):
    """bottom row of m bricks; n top bricks offset by `gap` columns."""
    if m is None:
        m = n + 1
    m = max(m, 1)
    W = 2 * m
    rows = [['.'] * W for _ in range(6)]
    for i in range(m):
        for r in range(3, 6):
            rows[r][2 * i] = bot
            rows[r][2 * i + 1] = bot
    for i in range(n):
        c = 2 * i + gap
        if c + 1 < W:
            for r in range(0, 3):
                rows[r][c] = top
                rows[r][c + 1] = top
    return "\n".join("".join(r) for r in rows)


def stagger_sep(top, bot, n):
    """n top bricks, each straddling two bottom bricks, kept apart."""
    m = max(2 * n + 1, 1)
    W = 2 * m
    rows = [['.'] * W for _ in range(6)]
    for i in range(m):
        for r in range(3, 6):
            rows[r][2 * i] = bot
            rows[r][2 * i + 1] = bot
    for i in range(n):
        c = 4 * i + 1
        for r in range(0, 3):
            rows[r][c] = top
            rows[r][c + 1] = top
    return "\n".join("".join(r) for r in rows)


def flat(colour, m):
    return "\n".join([colour * 2 * m] * 3)


def H_lego(clue):
    a, b, n = clue[0], clue[1], int(clue[2:])
    return [
        lambda: stagger(a, b, n),
        lambda: stagger(b, a, n),
        lambda: stagger(a, a, n),
        lambda: stagger(a, b, n, m=n + 2),
        lambda: stagger(b, a, n, m=n + 2),
        lambda: flat(a, max(n, 1)),
        lambda: stagger_sep(a, b, n),
        lambda: "\n".join([(a * 2 + b * 2) * max(n, 1)] * 3),
    ]


# ---------------- tovel ----------------
def tovel_cal(a, b, assign):
    cells = ["   "] * b + ["%2d%s" % (d, assign[d]) for d in range(1, a + 1)]
    while len(cells) % 7:
        cells.append("   ")
    lines = [DAYS]
    for i in range(0, len(cells), 7):
        lines.append(" ".join(cells[i:i + 7]).rstrip())
    return "\n".join(lines)


def tv(a, b, c, cdays, others="JTG"):
    assign = {}
    j = 0
    for d in range(1, a + 1):
        if d in cdays:
            assign[d] = c
        else:
            o = others[j % len(others)]
            if o == c:
                o = others[(j + 1) % len(others)]
            assign[d] = o
            j += 1
    return tovel_cal(a, b, assign)


def H_tovel(clue):
    p = clue.split("/")
    a, b, c, d, e = int(p[0]), int(p[1]), p[2], int(p[3]), int(p[4])
    alld = range(1, a + 1)
    half = set(x for x in alld if x % 2 == e % 2)
    run = set(x for x in range(e, min(a, e + d - 1) + 1))
    return [
        lambda: tv(a, b, c, half),
        lambda: tv(a, b, c, {e}),
        lambda: tv(a, b, c, half | {e}, others="JTGM"),
        lambda: tv(a, b, c, run),
        lambda: tv(a, b, c, set(x for x in alld if (x - e) % 7 == 0)),
        lambda: tv(a, b, c, set(list(alld)[:d]) | {e}),
        lambda: tv(a, b, c, half, others="J"),
        lambda: tv(a, b, c, set(alld) - {e}),
        lambda: tv(a, b, c, set(x for x in alld if x % 3 == e % 3)),
        lambda: tv(a, b, c, set(alld)),
    ]


# ---------------- velk ----------------
def bubble_passes(s, k):
    a = list(s)
    for _ in range(k):
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
    return "".join(a)


def bubble_trace(s, k):
    a = list(s)
    out = ["".join(a)]
    for _ in range(k):
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
        out.append("".join(a))
    return "\n".join(out)


def bubble_swaps(s, k):
    a = list(s)
    done = 0
    for _ in range(len(a)):
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                done += 1
                if done >= k:
                    return "".join(a)
    return "".join(a)


def kth_perm(s, k):
    import itertools
    it = itertools.islice(itertools.permutations(sorted(s)), k, k + 1)
    for p in it:
        return "".join(p)
    return "".join(sorted(s))


def H_velk(clue):
    s, k = clue.split("|")
    k = int(k)
    return [
        lambda: bubble_passes(s, k),
        lambda: bubble_trace(s, k),
        lambda: bubble_swaps(s, k),
        lambda: kth_perm(s, k),
        lambda: kth_perm(s, k - 1),
        lambda: "".join(KEYPAD[c] for c in s),
        lambda: " ".join(MORSE[c] for c in s),
        lambda: "".join(sorted(s)[:k]),
        lambda: "".join(sorted(s, reverse=True)[:k]),
        lambda: "\n".join(bubble_trace(s, len(s)).split("\n")),
        lambda: "".join(c for c in s if c not in sorted(s)[:k]),
        lambda: str(sum(1 for i in range(len(s) - 1) if s[i] > s[i + 1])),
        lambda: chr(A + (sum(ord(c) - A for c in s) % 26)),
        lambda: "".join(chr(A + (ord(c) - A + i) % 26) for i, c in enumerate(s)),
    ]


# ---------------- murn ----------------
def bounce(s, n):
    cells = list(s)
    L = len(cells)
    d = [1] * L
    for _ in range(n):
        new = ['.'] * L
        nd = [1] * L
        for i in range(L):
            if cells[i] == '#':
                new[i] = '#'
        for i in range(L):
            if cells[i] == 'o':
                j = i + d[i]
                if not (0 <= j < L) or cells[j] == '#' or new[j] == 'o':
                    d[i] = -d[i]
                    j = i
                new[j] = 'o'
                nd[j] = d[i]
        cells = new
        d = nd
    return "".join(cells)


def spread(s, n):
    cells = list(s)
    L = len(cells)
    for _ in range(n):
        new = list(cells)
        for i in range(L):
            if cells[i] == 'o':
                for j in (i - 1, i + 1):
                    if 0 <= j < L and cells[j] == '.':
                        new[j] = 'o'
        cells = new
    return "".join(cells)


def H_murn(clue):
    s, n = clue.split("|")
    n = int(n)
    return [
        lambda: bounce(s, n),
        lambda: spread(s, n),
        lambda: "\n".join(spread(s, i) for i in range(n + 1)),
        lambda: s.replace('o', '.').replace('#', 'o'),
        lambda: "".join(sorted(s)),
        lambda: str(sum(i for i, c in enumerate(s) if c == 'o')),
        lambda: str(len([c for c in s if c != '.']) * n),
        lambda: "\n".join([s[i % len(s):] + s[:i % len(s)] for i in range(n)]),
        lambda: s[::-1] + "|" + str(n),
        lambda: "".join('o' if c == '#' else ('#' if c == 'o' else c) for c in s),
        lambda: str(max((len(x) for x in s.split('#')), default=0)),
        lambda: str(s.count('o') + s.count('#') - n),
        lambda: "".join('.' if c == 'o' else c for c in s),
        lambda: str(n * s.count('#')),
    ]


# ---------------- kelmar ----------------
def queue_sim(s, wv):
    """each mark is a job of wv[ch] units; one server, one unit per tick."""
    t = 0
    busy = 0
    maxq = 0
    q = 0
    for ch in s:
        if ch in wv:
            q += wv[ch]
        if q > 0:
            q -= 1
        maxq = max(maxq, q)
        t += 1
    return t + q, maxq


def H_kelmar(clue):
    s, w = clue.split("/")
    wv = {w[0]: int(w[1]), w[2]: int(w[3])}
    fin, maxq = queue_sim(s, wv)
    marks = [(i, ch) for i, ch in enumerate(s) if ch in wv]
    return [
        lambda: str(fin),
        lambda: str(maxq),
        lambda: str(fin - len(s)),
        lambda: "".join(str(wv[ch]) if ch in wv else '.' for ch in s),
        lambda: "".join(ch * wv[ch] if ch in wv else ch for ch in s),
        lambda: str(sum(wv[ch] for _, ch in marks) + len(marks)),
        lambda: ",".join(str(i) for i, _ in marks),
        lambda: str(len(marks)),
        lambda: "_" * len(s),
        lambda: "".join('X' if ch in wv else '_' for ch in s),
        lambda: str(sum((i + 1) * wv[ch] for i, ch in marks)),
        lambda: str(max(wv.values()) * len(marks)),
        lambda: s.replace('_', ' '),
        lambda: str(len(s) + sum(wv[ch] for _, ch in marks)),
    ]


# ---------------- basten ----------------
def H_basten(clue):
    s, n = clue.split("/")
    n = int(n)
    digs = [(i, int(c)) for i, c in enumerate(s) if c.isdigit()]
    tot = sum(d for _, d in digs)
    # bus: capacity n picks up passengers along the road
    trips = 0
    load = 0
    for _, d in digs:
        load += d
        while load > n:
            load -= n
            trips += 1
    return [
        lambda: str(-(-tot // n)) if n else "0",
        lambda: str(trips),
        lambda: str(tot % n) if n else "0",
        lambda: "".join(c if c.isdigit() else '.' for c in s) + "/" + str(n),
        lambda: str(len(s) - len(digs)),
        lambda: str(sum(1 for _, d in digs if d == n)),
        lambda: str(max(digs[i + 1][0] - digs[i][0]
                        for i in range(len(digs) - 1))) if len(digs) > 1 else "0",
        lambda: str(min(digs[i + 1][0] - digs[i][0]
                        for i in range(len(digs) - 1))) if len(digs) > 1 else "0",
        lambda: str(digs[n - 1][0]) if 0 < n <= len(digs) else "0",
        lambda: str(digs[n - 1][1]) if 0 < n <= len(digs) else "0",
        lambda: "".join('.' if not c.isdigit() else c for c in s)[::-1],
        lambda: str(tot * n),
        lambda: str(len(digs) * n),
        lambda: str(tot + len(s)),
    ]


# ---------------- orlan ----------------
def voronoi(rows):
    from collections import deque
    H = len(rows)
    W = len(rows[0])
    owner = [[rows[r][c] if rows[r][c] in 'ox' else None for c in range(W)]
             for r in range(H)]
    dist = [[0 if rows[r][c] in 'ox' else -1 for c in range(W)]
            for r in range(H)]
    q = deque((r, c) for r in range(H) for c in range(W) if rows[r][c] in 'ox')
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and rows[nr][nc] == '.':
                if dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    owner[nr][nc] = owner[r][c]
                    q.append((nr, nc))
                elif dist[nr][nc] == dist[r][c] + 1 and owner[nr][nc] != owner[r][c]:
                    owner[nr][nc] = '.'
    out = []
    for r in range(H):
        out.append("".join(rows[r][c] if rows[r][c] != '.'
                           else (owner[r][c] or '.') for c in range(W)))
    return "\n".join(out)


def flood_count(rows, ch):
    from collections import deque
    H = len(rows)
    W = len(rows[0])
    seen = set()
    n = 0
    q = deque((r, c) for r in range(H) for c in range(W) if rows[r][c] == ch)
    seen |= set(q)
    while q:
        r, c = q.popleft()
        n += 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and (nr, nc) not in seen \
                    and rows[nr][nc] != '#':
                seen.add((nr, nc))
                q.append((nr, nc))
    return n


def H_orlan(clue):
    rows = clue.split("\n")
    H = len(rows)
    W = len(rows[0])
    return [
        lambda: voronoi(rows),
        lambda: str(flood_count(rows, 'x')),
        lambda: str(flood_count(rows, 'o')),
        lambda: 'x' if flood_count(rows, 'x') > flood_count(rows, 'o') else 'o',
        lambda: "\n".join("".join('*' if rows[r][c] == '.' else rows[r][c]
                                  for c in range(W)) for r in range(H)),
        lambda: "\n".join(r.replace('x', '.').replace('o', '.') for r in rows),
        lambda: str(sum(1 for r in range(H) for c in range(W)
                        if rows[r][c] == 'x'
                        and any(0 <= r + dr < H and 0 <= c + dc < W
                                and rows[r + dr][c + dc] == 'o'
                                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))))),
        lambda: "\n".join("".join(rows[r][c] if rows[r][c] != '.' else
                                  ('o' if (r + c) % 2 else 'x')
                                  for c in range(W)) for r in range(H)),
        lambda: clue.replace('o', 'O').replace('x', 'X'),
        lambda: "\n".join(sorted(rows)),
        lambda: str(H * W - clue.count('#') - clue.count('\n')),
        lambda: clue + "\n" + clue,
        lambda: "\n".join("".join(rows[r][W - 1 - c] for c in range(W))
                          for r in range(H)),
        lambda: str(clue.count('#')),
    ]


BUILDERS = {
    "LegoZendo2": H_lego,
    "velk": H_velk,
    "murn": H_murn,
    "kelmar": H_kelmar,
    "basten": H_basten,
    "orlan": H_orlan,
    "tovel": H_tovel,
}


def on_round_start(memory):
    memory["probe_log"] = []
    memory["counters"] = {}


def solve(name, clue, memory):
    try:
        b = BUILDERS.get(name)
        if b is None:
            return None
        hs = b(clue)
        cnt = memory["counters"]
        h = cnt.get(name, 0)
        cnt[name] = h + 1
        hid = h % len(hs)
        memory["probe_log"].append([memory.get("_index", -1), name, hid])
        return hs[hid]()
    except Exception:
        return ""


def on_round_end(items, memory):
    memory["items"] = [{"i": it.get("index"), "n": it.get("name"),
                        "c": it.get("clue"), "s": it.get("score")}
                       for it in items]
