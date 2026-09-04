"""basten1b round 6.

clue = mask/N.  Picture: width len(mask), '~' top row, '#' bed row, height 8
(6,7,8 all legal; 5 and 9 always score 0).  Each digit in mask is a reed of that
height standing on the bed, drawn '|'.  Fish '><>'/'<><' swim in the water.
The scored property is how many fish stand right beside a reed ("sheltered"):
it must be at least N, and there is a sweet spot a little above N.
Round 6: lock in N<=3, sweep the offset for N=4..5 and offset x free for N>=6.
"""

FISH = ('><>', '<><')
H = 8


def _parse(clue):
    s = clue.strip()
    i = s.rfind('/')
    return s[:i], int(s[i + 1:])


def _build(mask, want, nfree):
    w = len(mask)
    bed = H - 1
    g = [['.'] * w for _ in range(H)]
    g[0] = ['~'] * w
    g[bed] = ['#'] * w
    reeds = []
    for c, ch in enumerate(mask):
        if ch.isdigit() and int(ch) > 0:
            reeds.append(c)
            for r in range(bed - int(ch), bed):
                if 1 <= r < bed:
                    g[r][c] = '|'
    bars = set()
    for r in range(1, bed):
        for c in range(w):
            if g[r][c] == '|':
                bars.add((r, c))

    def dots(r, c):
        return 0 <= c and c + 2 < w and g[r][c] == '.' \
            and g[r][c + 1] == '.' and g[r][c + 2] == '.'

    perreed = []
    for c in reeds:
        s = []
        for r in range(bed - 1, 0, -1):
            if (r, c) in bars:
                if dots(r, c + 1):
                    s.append((r, c + 1))
                if dots(r, c - 3):
                    s.append((r, c - 3))
        perreed.append(s)
    shelter = []
    lap = 0
    while True:
        got = False
        for s in perreed:
            if lap < len(s):
                shelter.append(s[lap]); got = True
        if not got:
            break
        lap += 1

    used = set()
    placed = []

    def put(r, c):
        for k in range(-2, 3):
            if (r, c + k) in used:
                return False
        for k in range(3):
            used.add((r, c + k))
        placed.append((r, c))
        return True

    for r, c in shelter:
        if len(placed) >= want:
            break
        put(r, c)

    if nfree:
        freeslots = []
        for r in range(1, bed):
            row = []
            c = 0
            while c + 2 < w:
                if dots(r, c) and (r, c - 1) not in bars and (r, c + 3) not in bars:
                    row.append((r, c)); c += 4
                else:
                    c += 1
            if row:
                o = (r * 3) % len(row)
                row = row[o:] + row[:o]
            freeslots.extend(row)
        seen = set()
        for r, c in freeslots:
            if len(placed) >= want + nfree:
                break
            if r in seen:
                continue
            if put(r, c):
                seen.add(r)
        for r, c in freeslots:
            if len(placed) >= want + nfree:
                break
            put(r, c)

    for i, (r, c) in enumerate(placed):
        b = FISH[i % 2]
        g[r][c] = b[0]; g[r][c + 1] = b[1]; g[r][c + 2] = b[2]
    return "\n".join("".join(row) for row in g)


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


# best (offset above N, free fish) per N, measured over rounds 5 and 6
TABLE = {2: (2, 0), 3: (2, 0), 4: (2, 0), 5: (3, 0), 6: (5, 0), 8: (5, 0)}


def solve(name, clue, memory):
    try:
        mask, N = _parse(clue)
        if N == 7:                       # thin evidence: split between the two best
            off, fr = (2, 2) if int(memory.get("_index", 0)) % 2 else (3, 1)
        else:
            off, fr = TABLE.get(N, (3, 1))
        return _build(mask, N + off, fr)
    except Exception:
        return None
