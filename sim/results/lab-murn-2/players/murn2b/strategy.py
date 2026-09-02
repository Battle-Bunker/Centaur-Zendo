"""murn: build a tower of 'partial count' rows above the clue row.

Rule inferred from 6 demos:
  * the answer is R rows of the clue's length, joined by '\n'
  * the LAST row is the clue board
  * for every pair of adjacent rows, the upper row satisfies
        upper[i] == '.'  OR  upper[i] == ".o#"[ c mod 3 ]
    where c = number of non-'.' cells in lower[i-1..i+1] ('.' padding)
  * the total number of '#' in all rows ABOVE the clue equals n
"""

SYM = ".o#"


def counts(row, L):
    nd = [1 if c != "." else 0 for c in row]
    out = []
    prev = 0
    for i in range(L):
        c = nd[i]
        if i:
            c += nd[i - 1]
        if i + 1 < L:
            c += nd[i + 1]
        out.append(c % 3)
    return out


def _greedy(B, n, L):
    rows = [B]
    cur = B
    rem = n
    for _ in range(30):
        if rem <= 0:
            break
        c = counts(cur, L)
        hs = [i for i, v in enumerate(c) if v == 2]
        if len(hs) >= rem:
            keep = set(hs[:rem])
            new = "".join("#" if i in keep else "." for i in range(L))
            rows.append(new)
            rem = 0
            break
        new = "".join(SYM[v] for v in c)
        if "o" not in new and "#" not in new:
            return None
        rem -= len(hs)
        rows.append(new)
        cur = new
    if rem != 0:
        return None
    return rows


def _spread(B, n, L, k):
    """two rows above the clue: k hashes in the first, n-k in the second."""
    c1 = counts(B, L)
    hs1 = [i for i, v in enumerate(c1) if v == 2]
    os1 = [i for i, v in enumerate(c1) if v == 1]
    if k > len(hs1) or n - k < 1:
        return None
    keep = set(hs1[:k]) | set(os1)
    r1 = "".join(SYM[c1[i]] if i in keep else "." for i in range(L))
    if "o" not in r1 and "#" not in r1:
        return None
    c2 = counts(r1, L)
    hs2 = [i for i, v in enumerate(c2) if v == 2]
    if len(hs2) < n - k:
        return None
    keep2 = set(hs2[: n - k])
    r2 = "".join("#" if i in keep2 else "." for i in range(L))
    return [B, r1, r2]


def validate(rows, B, n, L):
    if len(rows) < 2 or rows[0] != B:
        return False
    tot = 0
    for idx in range(len(rows)):
        r = rows[idx]
        if len(r) != L:
            return False
        if idx and "o" not in r and "#" not in r:
            return False
        if idx:
            tot += r.count("#")
    if tot != n:
        return False
    for t in range(len(rows) - 1):
        c = counts(rows[t], L)
        up = rows[t + 1]
        for i in range(L):
            ch = up[i]
            if ch == ".":
                continue
            if SYM[c[i]] != ch:
                return False
    return True


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    try:
        B, ns = clue.split("|")
        n = int(ns)
        L = len(B)
        rows = _spread(B, n, L, min(n - 1, 99))
        if rows is None or not validate(rows, B, n, L):
            rows = _spread(B, n, L, 0)
        if rows is None or not validate(rows, B, n, L):
            rows = _greedy(B, n, L)
        if rows is None or not validate(rows, B, n, L):
            return None
        return "\n".join(reversed(rows))
    except Exception:
        return None


def on_round_end(items, memory):
    pass
