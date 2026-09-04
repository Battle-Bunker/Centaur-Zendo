"""strategy.py — garrow.

The clue is "<X><n><Y><m>" plus a 6-line ASCII strip (4 inner rows of two-letter
blobs inside a # border).  The answer is that same strip with vertical cuts "|"
inserted so that exactly n slices hold more X letters than Y letters and exactly
m hold more Y than X (slices with none of either letter are spare).

Primary solver: bitmask DP, exactly n+m strictly-dominant slices, min width 3.
Fallback: DP that also allows spare (X/Y-free) slices, slice widths 3..8, which
is what the server's own examples look like.  Both run in well under a
millisecond; never raises, never prints.
"""

import re
_HDR = re.compile(r'([a-z])(\d+)([a-z])(\d+)')

def _cuts(lines, X, nx, Y, ny, minw):
    grid = lines
    W = len(grid[0])
    K = nx + ny
    px = [0]*(W+1); py = [0]*(W+1)
    for c in range(W):
        cx = cy = 0
        for row in grid:
            ch = row[c]
            if ch == X: cx += 1
            elif ch == Y: cy += 1
        px[c+1] = px[c] + cx
        py[c+1] = py[c] + cy
    maskX = [0]*(W+1); maskY = [0]*(W+1)
    for i in range(W):
        pxi = px[i]; pyi = py[i]
        mx = my = 0
        for j in range(i+minw, W+1):
            dx = px[j]-pxi; dy = py[j]-pyi
            if dx > dy: mx |= 1 << j
            elif dy > dx: my |= 1 << j
        maskX[i] = mx; maskY[i] = my
    dp = [[0]*(K+1) for _ in range(K+1)]
    dp[0][0] = 1
    for k in range(K):
        row = dp[k]
        nxt = dp[k+1]
        for x in range(min(k, nx)+1):
            m = row[x]
            if not m: continue
            ax = 0; ay = 0
            while m:
                low = m & -m
                i = low.bit_length()-1
                m ^= low
                ax |= maskX[i]; ay |= maskY[i]
            if x+1 <= nx: nxt[x+1] |= ax
            nxt[x] |= ay
    target = 1 << W
    if not (dp[K][nx] & target):
        return None
    # backtrack
    cuts = []
    pos = W; x = nx
    for k in range(K, 0, -1):
        found = False
        if x > 0:
            m = dp[k-1][x-1]
            while m:
                low = m & -m
                i = low.bit_length()-1
                m ^= low
                if i <= pos-minw and (px[pos]-px[i]) > (py[pos]-py[i]):
                    pos = i; x -= 1; found = True; break
        if not found:
            m = dp[k-1][x]
            while m:
                low = m & -m
                i = low.bit_length()-1
                m ^= low
                if i <= pos-minw and (py[pos]-py[i]) > (px[pos]-px[i]):
                    pos = i; found = True; break
        if not found:
            return None
        if k > 1:
            cuts.append(pos)
    if pos != 0:
        return None
    cuts.reverse()
    return cuts


def solve_garrow(clue):
    nl = clue.index('\n')
    hdr = clue[:nl]
    m = _HDR.match(hdr)
    if not m:
        return None
    X = m.group(1); nx = int(m.group(2)); Y = m.group(3); ny = int(m.group(4))
    grid = clue[nl+1:].split('\n')
    for minw in (3, 2, 1):
        cuts = _cuts(grid, X, nx, Y, ny, minw)
        if cuts is not None:
            break
    else:
        return None
    out = []
    for row in grid:
        parts = []
        prev = 0
        for c in cuts:
            parts.append(row[prev:c]); prev = c
        parts.append(row[prev:])
        out.append('|'.join(parts))
    return '\n'.join(out)




def _gprep(clue):
    nl = clue.index('\n')
    m = _HDR.match(clue[:nl])
    X = m.group(1); nx = int(m.group(2)); Y = m.group(3); ny = int(m.group(4))
    grid = clue[nl+1:].split('\n')
    W = len(grid[0])
    px = [0]*(W+1); py = [0]*(W+1)
    for c in range(W):
        cx = cy = 0
        for row in grid:
            ch = row[c]
            if ch == X: cx += 1
            elif ch == Y: cy += 1
        px[c+1] = px[c]+cx; py[c+1] = py[c]+cy
    return grid, W, X, nx, Y, ny, px, py


def gen_cuts(W, nx, ny, px, py, wmin, wmax, allow_nonzero_tie=False):
    """slices: strictly X-dom (nx of them), strictly Y-dom (ny), rest must be
    free of both letters.  widths in [wmin, wmax]."""
    NEG = None
    # dp[pos][x][y] = predecessor (prev_pos) or None
    size_x = nx+1; size_y = ny+1
    prev = [[[NEG]*size_y for _ in range(size_x)] for _ in range(W+1)]
    seen = [[[False]*size_y for _ in range(size_x)] for _ in range(W+1)]
    seen[0][0][0] = True
    for i in range(W):
        si = seen[i]
        any_here = False
        for x in range(size_x):
            for y in range(size_y):
                if si[x][y]: any_here = True; break
            if any_here: break
        if not any_here: continue
        hi = min(W, i+wmax)
        for j in range(i+wmin, hi+1):
            if j != W and W-j < wmin:
                continue
            dx = px[j]-px[i]; dy = py[j]-py[i]
            if dx > dy: ddx, ddy = 1, 0
            elif dy > dx: ddx, ddy = 0, 1
            elif dx == 0: ddx, ddy = 0, 0
            elif allow_nonzero_tie: ddx, ddy = 0, 1
            else: continue
            for x in range(size_x-ddx):
                row = si[x]
                for y in range(size_y-ddy):
                    if row[y] and not seen[j][x+ddx][y+ddy]:
                        seen[j][x+ddx][y+ddy] = True
                        prev[j][x+ddx][y+ddy] = (i, x, y)
    if not seen[W][nx][ny]:
        return None
    cuts = []
    st = (W, nx, ny)
    while st[0] != 0:
        p = prev[st[0]][st[1]][st[2]]
        if p is None:
            return None
        if p[0] != 0:
            cuts.append(p[0])
        st = p
    cuts.reverse()
    return cuts


def _grender(grid, cuts):
    out = []
    for row in grid:
        parts = []; prev = 0
        for c in cuts:
            parts.append(row[prev:c]); prev = c
        parts.append(row[prev:])
        out.append('|'.join(parts))
    return '\n'.join(out)


def solve_gen(clue):
    grid, W, X, nx, Y, ny, px, py = _gprep(clue)
    for (a, b, t) in ((3, 8, False), (3, 8, True), (2, 10, False), (2, 10, True),
                      (2, 14, True), (1, W, True)):
        cuts = gen_cuts(W, nx, ny, px, py, a, b, t)
        if cuts is not None:
            return _grender(grid, cuts)
    return None


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    if name != "garrow":
        return None
    try:
        a = solve_garrow(clue)
        if a is not None:
            return a
    except Exception:
        pass
    try:
        return solve_gen(clue)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
