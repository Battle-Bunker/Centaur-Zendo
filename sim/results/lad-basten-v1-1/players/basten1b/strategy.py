"""strategy.py — team basten1b — FINAL.

Challenge class `basten` = a side-on picture of a fish tank.

  clue = "<column spec>/<N>"
  * width           = len(column spec)
  * a digit d at column c = a seaweed stalk in column c, d cells tall, growing
    up off the gravel                                     (verified on 3 demos)
  * row 0 is all '~' (the surface), the last row all '#' (the gravel), and the
    water in between is '.' with fish '<><' / '><>' swimming in it.
  * the picture height is NOT N.  Measured: heights of maxweed+3 and maxweed+4
    score, maxweed+2 and maxweed+6 never score.
  * fish must have at least one blank column between them (touching fish never
    score) and both orientations must appear (all-left and all-right pictures
    scored 0/58 each while the same picture with mixed orientations scored 10%).

Measured hit rates (max-density fish, mixed orientation):
    height maxweed+3 : 8.3%      height maxweed+4 : 10.3%
    height maxweed+2 : 0%        height maxweed+6 : 0%
  and by N: N>=6 ~9%, N=4/5 ~4-6%, N<=3 ~1% (sparse tanks do best there).
"""

FL = "<><"
FR = "><>"


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


class R:
    __slots__ = ("s",)

    def __init__(self, s):
        self.s = s & 0x7FFFFFFF

    def nxt(self, m):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return (self.s >> 7) % m if m > 0 else 0


def build(clue, extra, k, rng):
    i = clue.rfind("/")
    spec = clue[:i]
    w = len(spec)
    weeds = []
    mx = 1
    for c in range(w):
        ch = spec[c]
        if "1" <= ch <= "9":
            d = ord(ch) - 48
            weeds.append((c, d))
            if d > mx:
                mx = d
    h = mx + extra
    if h < 4:
        h = 4
    grid = [["."] * w for _ in range(h)]
    grid[0] = ["~"] * w
    grid[h - 1] = ["#"] * w
    for c, d in weeds:
        r = h - 1 - d
        if r < 1:
            r = 1
        while r < h - 1:
            grid[r][c] = "|"
            r += 1
    for r in range(1, h - 1):
        row = grid[r]
        if k > 90:
            c = 0
            while c <= w - 3:
                if row[c] == "." and row[c + 1] == "." and row[c + 2] == ".":
                    f = FL if rng.nxt(2) else FR
                    row[c] = f[0]
                    row[c + 1] = f[1]
                    row[c + 2] = f[2]
                    c += 4
                else:
                    c += 1
        else:
            free = []
            for c in range(w - 2):
                if row[c] == "." and row[c + 1] == "." and row[c + 2] == ".":
                    free.append(c)
            n = 0
            while n < k and free:
                c = free.pop(rng.nxt(len(free)))
                if row[c] != "." or row[c + 1] != "." or row[c + 2] != ".":
                    continue
                if c > 0 and row[c - 1] in "<>":
                    continue
                if c + 3 < w and row[c + 3] in "<>":
                    continue
                f = FL if rng.nxt(2) else FR
                row[c] = f[0]
                row[c + 1] = f[1]
                row[c + 2] = f[2]
                n += 1
    return "\n".join("".join(x) for x in grid)


def solve(name, clue, memory):
    try:
        i = clue.rfind("/")
        n = int(clue[i + 1:])
        idx = memory.get("_index", 0)
        rng = R((hash(clue) & 0x7FFFFFFF) + idx * 7919 + 104729)
        if n <= 3:
            if idx & 1:
                return build(clue, 5, 2, rng)
            return build(clue, 3, 3, rng)
        if idx & 1:
            return build(clue, 4, 99, rng)
        return build(clue, 3, 99, rng)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
