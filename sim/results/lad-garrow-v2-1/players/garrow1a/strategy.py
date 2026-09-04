"""garrow — final strategy.

Clue  = "L1 d1 L2 d2" (e.g. "b2c2") + a 6-line grid: two '#' border rows and
        four rows holding two-cell tokens ("aa", "bb", ... ).
Answer= the same grid with vertical '|' cuts inserted, splitting it into
        column pieces.

What six training rounds established (the rule itself was never fully cracked):
  * 2- and 3-piece answers NEVER score; 4 pieces is the best piece count.
  * one piece must hold exactly d1 tokens of L1 and d2 of L2, counting any
    token that overlaps the piece (a token cut in half counts for both sides);
    answers with no such piece score ~0.
  * the narrower that piece is (>= 3 columns), the better it scores, and the
    remaining pieces do best as 3-wide fillers plus one big remainder.
Best measured hit-rate: ~30%.
"""


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def _parse(clue):
    lines = clue.split("\n")
    head = lines[0]
    grid = lines[1:]
    L1 = head[0]; d1 = ord(head[1]) - 48
    L2 = head[2]; d2 = ord(head[3]) - 48
    W = len(grid[0])
    s1 = []; s2 = []
    for r in grid[1:-1]:
        i = 1; n = len(r) - 1
        while i < n:
            ch = r[i]
            if ch != '.' and r[i + 1] == ch:
                if ch == L1: s1.append(i)
                if ch == L2: s2.append(i)
                i += 2
            else:
                i += 1
    return grid, W, d1, s1, d2, s2


def _pre(starts, W):
    """pre[j] = number of token starts <= j-2;  count(a,b) = pre[b+1]-pre[a]."""
    arr = [0] * (W + 2)
    for s in starts:
        arr[s + 2] += 1
    t = 0
    for j in range(W + 2):
        t += arr[j]; arr[j] = t
    return arr


def _render(grid, cuts):
    out = []
    for r in grid:
        parts = []
        prev = 0
        for c in cuts:
            parts.append(r[prev:c]); prev = c
        parts.append(r[prev:])
        out.append("|".join(parts))
    return "\n".join(out)


def _build(W, a, b, minf=3):
    """Four pieces: [a,b) plus three others, each >= minf wide, biggest maximised."""
    La = a; Lb = W - b
    best = -1; bestcuts = None
    for i in (0, 1, 2, 3):
        j = 3 - i
        if (La == 0) != (i == 0):
            continue
        if (Lb == 0) != (j == 0):
            continue
        if La < minf * i or Lb < minf * j:
            continue
        cuts = [minf * k for k in range(1, i)]
        if a > 0: cuts.append(a)
        if b < W: cuts.append(b)
        for k in range(1, j):
            cuts.append(b + minf * k)
        cuts.sort()
        if len(cuts) != 3:
            continue
        bnd = [0] + cuts + [W]
        big = 0
        for t in range(len(bnd) - 1):
            w = bnd[t + 1] - bnd[t]
            if w > big: big = w
        if big > best:
            best = big; bestcuts = cuts
    return bestcuts


def solve(name, clue, memory):
    try:
        grid, W, d1, s1, d2, s2 = _parse(clue)
        p1 = _pre(s1, W); p2 = _pre(s2, W)
        widths = list(range(3, W + 1)) + [2, 1]
        for minf in (3, 1):
            for w in widths:
                lim = W - w
                for a in range(0, lim + 1):
                    b = a + w
                    if p1[b + 1] - p1[a] == d1 and p2[b + 1] - p2[a] == d2:
                        cuts = _build(W, a, b, minf)
                        if cuts is not None:
                            return _render(grid, cuts)
        # no window matches both counts: settle for one that matches either
        for pre, d in ((p1, d1), (p2, d2)):
            for w in range(3, W + 1):
                lim = W - w
                for a in range(0, lim + 1):
                    if pre[a + w + 1] - pre[a] == d:
                        cuts = _build(W, a, a + w, 3)
                        if cuts is not None:
                            return _render(grid, cuts)
        return None
    except Exception:
        return None


def on_round_end(items, memory):
    memory["last"] = {"presented": len(items),
                      "correct": sum(1 for it in items if it.get("score"))}
