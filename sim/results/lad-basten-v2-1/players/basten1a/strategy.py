"""FINAL strategy for challenge class `basten`.

The clue is a seabed line: digits 1-3 at their columns are seaweed stems of that
height, dots are empty gravel, and "/N" is a scene parameter.  The answer is an
ASCII aquarium: a '~' surface row, water rows ('.') with '|' seaweed growing up
from the floor, a '#' gravel floor, and fish ('><>' / '<><') swimming in the
water.  Tank height and fish density are tuned per N from measured hit rates.
"""

BG, SURF, FLOOR, PLANT = '.', '~', '#', '|'
FR, FL = '><>', '<><'

# n -> (extra water rows above the tallest stem, fish per row; 0 = pack the row)
PLAN = {2: (1, -1), 3: (2, -1), 4: (1, -1), 5: (2, -1),
        6: (1, 0), 7: (1, 0), 8: (1, -1)}
DEFAULT = (1, -1)


def build(clue):
    body, ns = clue.rsplit('/', 1)
    n = int(ns)
    W = len(body)
    ds = [(i, int(c)) for i, c in enumerate(body) if c.isdigit()]
    if not ds:
        ds = []
        mx = 1
    else:
        mx = max(v for _, v in ds)
    extra, per = PLAN.get(n, DEFAULT)
    H = mx + extra
    if H < 1:
        H = 1
    grid = [[BG] * W for _ in range(H)]
    for c, v in ds:
        for k in range(min(v, H)):
            grid[H - 1 - k][c] = PLANT
    k = n if per < 0 else 0          # 0 means "fill every slot"
    d = 0
    for r in range(H):
        row = grid[r]
        slots = []
        c = 0
        while c + 2 < W:
            if row[c] == BG and row[c + 1] == BG and row[c + 2] == BG:
                slots.append(c)
                c += 4
            else:
                c += 1
        if not slots:
            continue
        if k <= 0 or k >= len(slots):
            pick = slots
        else:
            step = len(slots) / float(k)
            pick = [slots[min(len(slots) - 1, int((i + 0.5) * step))]
                    for i in range(k)]
        for c in pick:
            if row[c] == BG and row[c + 1] == BG and row[c + 2] == BG:
                f = FR if d % 2 == 0 else FL
                row[c], row[c + 1], row[c + 2] = f
                d += 1
    return '\n'.join([SURF * W] + [''.join(x) for x in grid] + [FLOOR * W])


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    try:
        return build(clue)
    except Exception:
        return None


def on_round_end(items, memory):
    memory["_last"] = len(items)
