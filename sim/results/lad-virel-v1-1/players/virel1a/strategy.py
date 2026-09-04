"""virel: brick wall.

clue "D1..Dk/N":  W = sum(Di).  Answer = H lines, each a composition of W into
parts 2..6, rendered "[" + "-"*(p-2) + "]".  The LAST line must be the clue row.
Exactly N bricks must occupy an identical (start, length) slot in two
vertically adjacent rows.  H >= 5.  No vertical joint may run through all rows.
"""

import random

_RND = random.Random(20260904)
_RI = _RND.randint
_TOK = ("", "", "[]", "[-]", "[--]", "[---]", "[----]")
_CAT = "".join


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def _fill(out, start, g, bmask):
    """append parts summing to g (laid from `start`); no brick may hit bmask"""
    ri = _RI
    for _ in range(8):
        n0 = len(out)
        rem = g
        pos = start
        ok = True
        while rem > 6:
            p = ri(2, 6 if rem >= 8 else rem - 2)
            if (bmask >> (pos * 8 + p)) & 1:
                ok = False
                break
            out.append(p)
            pos += p
            rem -= p
        if ok and rem:
            if (bmask >> (pos * 8 + rem)) & 1:
                ok = False
            else:
                out.append(rem)
        if ok:
            return True
        del out[n0:]
    return False


def _gen_row(bricks, bmask, W, t):
    """composition of W sharing exactly t bricks with the row (bricks, bmask)"""
    n = len(bricks)
    if t > n:
        return None
    sample = _RND.sample
    for _ in range(20):
        row = []
        prev = 0
        ok = True
        if t:
            keep = sorted(sample(bricks, t))
            for s, l in keep:
                if s > prev and not _fill(row, prev, s - prev, bmask):
                    ok = False
                    break
                row.append(l)
                prev = s + l
            if not ok:
                continue
        if prev < W and not _fill(row, prev, W - prev, bmask):
            continue
        c = 0
        pos = 0
        for p in row:
            if (bmask >> (pos * 8 + p)) & 1:
                c += 1
            pos += p
        if c == t:
            return row
    return None


def _masks(parts):
    """(brick list, brick mask, joint mask)"""
    bricks = []
    bm = 0
    jm = 0
    pos = 0
    for p in parts:
        bricks.append((pos, p))
        bm |= 1 << (pos * 8 + p)
        pos += p
        jm |= 1 << pos
    return bricks, bm, jm ^ (1 << pos)


def _wall(clue_parts, W, N, H):
    pairs = H - 1
    base = N // pairs
    share = [base] * pairs
    for i in range(N - base * pairs):
        share[i] += 1
    shuffle = _RND.shuffle
    for _ in range(4):
        shuffle(share)
        bricks, bm, jm = _masks(clue_parts)
        rows = [clue_parts]
        inter = jm
        ok = True
        for t in share:
            r = _gen_row(bricks, bm, W, t)
            if r is None:
                ok = False
                break
            rows.append(r)
            bricks, bm, jm = _masks(r)
            inter &= jm
        if ok and not inter:
            rows.reverse()
            return rows
    return None


def solve(name, clue, memory):
    try:
        cache = memory.get("_c")
        if cache is None:
            cache = memory["_c"] = {}
        hit = cache.get(clue)
        if hit is not None:
            return hit
        left, right = clue.split("/")
        parts = [ord(c) - 48 for c in left]
        W = 0
        for p in parts:
            W += p
        N = int(right)
        H = 5
        rows = _wall(parts, W, N, H)
        while rows is None and H < 13:
            H += 1
            rows = _wall(parts, W, N, H)
        if rows is None:
            return None
        out = "\n".join([_CAT([_TOK[p] for p in r]) for r in rows])
        if len(cache) < 5000:
            cache[clue] = out
        return out
    except Exception:
        return None
