"""FINAL strategy for kelmar1a.

Confirmed knowledge
-------------------
* LegoZendo2: clue is <letter><letter><N>.  A completely solid 18x48 rectangle
  of one letter scores 1 whenever N == 0 (8/8 across rounds 2 and 4, with the
  wall letter unrelated to the clue letters).  For N > 0 every construction we
  tried scored 0, so N counts *something* we never identified.
* Every other class scored 0 on ~110 distinct hypotheses, so we skip them:
  a skip is instant and costs neither time nor the fewer-answers tiebreak.
* A small hedge cycles six untested LegoZendo2 constructions on one in three of
  the N > 0 challenges; if one of them is the rule it is worth far more than the
  throughput it costs.
"""

# ---------------------------------------------------------------- constants
ROWS, COLS = 18, 48
BR, BC = ROWS // 3, COLS // 2          # 6 brick-rows x 24 brick-cols

SOLID = "\n".join(["A" * COLS] * ROWS)          # proven answer for N == 0

_cache = {}                                      # clue -> answer (hedges)
_hedge_n = 0


def _blank():
    return [[":"] * COLS for _ in range(ROWS)]


def _fill(letter="A"):
    return [[letter] * COLS for _ in range(ROWS)]


def _brick(g, br, bc, ch):
    for dy in range(3):
        row = g[br * 3 + dy]
        for dx in range(2):
            row[bc * 2 + dx] = ch


def _emit(g):
    return "\n".join("".join(r) for r in g)


def _spots(n):
    """n brick positions that never touch one another (gap of 1 brick each way)."""
    out = []
    for br in (1, 3):
        for bc in range(1, BC - 1, 2):
            out.append((br, bc))
            if len(out) >= n:
                return out
    return out


def _v_cells(n, a, b):                      # exactly n empty cells
    g = _fill("A")
    for i in range(n):
        g[1 + (i // 12) * 6][2 + (i % 12) * 4] = ":"
    return _emit(g)


def _v_colour(n, ch):                       # exactly n isolated bricks of `ch`
    other = "A" if ch != "A" else "B"
    g = _fill(other)
    for br, bc in _spots(n):
        _brick(g, br, bc, ch)
    return _emit(g)


def _v_stack(n, a, b):                      # n isolated a-on-b contacts
    bg = "C"
    if a == "C" or b == "C":
        bg = "D"
    g = _fill(bg)
    k = 0
    for bc in range(1, BC - 1, 2):
        if k >= n:
            break
        _brick(g, 2, bc, a)
        _brick(g, 3, bc, b)
        k += 1
    return _emit(g)


def _v_colours(n, a, b):                    # exactly n distinct colours used
    letters = "ABCDEFGHIJKL"[:max(1, n)]
    g = _fill(letters[0])
    for i, ch in enumerate(letters[1:]):
        _brick(g, 1 + 2 * (i // 11), 1 + 2 * (i % 11), ch)
    return _emit(g)


def _v_bricks(n, a, b):                     # exactly n isolated bricks, nothing else
    g = _blank()
    for br, bc in _spots(n):
        _brick(g, br, bc, "A")
    return _emit(g)


def _hedge(n, a, b, k):
    if k == 0:
        return _v_cells(n, a, b)
    if k == 1:
        return _v_colour(n, b)
    if k == 2:
        return _v_colour(n, a)
    if k == 3:
        return _v_stack(n, a, b)
    if k == 4:
        return _v_colours(n, a, b)
    return _v_bricks(n, a, b)


def on_round_start(memory):
    global _hedge_n
    _hedge_n = 0
    _cache.clear()


def solve(name, clue, memory):
    global _hedge_n
    if name != "LegoZendo2":
        return None
    try:
        if clue[2:] == "0":
            return SOLID
        got = _cache.get(clue)
        if got is not None:
            return got
        _hedge_n += 1
        if _hedge_n % 3:
            return None
        ans = _hedge(int(clue[2:]), clue[0], clue[1], (_hedge_n // 3) % 6)
        _cache[clue] = ans
        return ans
    except Exception:
        return None


def on_round_end(items, memory):
    pass
