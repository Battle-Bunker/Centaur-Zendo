"""quilm - seven-segment "add matchsticks" puzzle.

clue "A B"  ->  two B-digit numbers x, y such that on a seven-segment display
every digit of y is the corresponding digit of x with segments ADDED (strict
superset: each digit must change), and exactly A segments are added in total.

Solution: x = 111...1 ; each '1' (2 segments) can grow by
1->'7'(+1) 1->'4'(+2) 1->'3'(+3) 1->'9'(+4) 1->'8'(+5).
Distribute A over B positions, each getting 1..5.
"""

_G2D = {1: "7", 2: "4", 3: "3", 4: "9", 5: "8"}
_TABLE = {}


def _build(a, b):
    if b < 1 or a < b or a > 5 * b:
        return None
    rem = a
    ys = []
    for i in range(b):
        rp = b - 1 - i
        g = min(5, rem - rp)
        if g < 1:
            g = 1
        ys.append(_G2D[g])
        rem -= g
    if rem != 0:
        return None
    return "1" * b + " " + "".join(ys)


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1
    _TABLE.clear()
    for b in range(1, 13):
        for a in range(b, 5 * b + 1):
            s = _build(a, b)
            if s:
                _TABLE["%d %d" % (a, b)] = s


def solve(name, clue, memory):
    r = _TABLE.get(clue)
    if r is not None:
        return r
    try:
        a, b = clue.split()
        return _build(int(a), int(b))
    except Exception:
        return None


def on_round_end(items, memory):
    pass
