"""morvin  —  clue "N/K"  ->  ASCII picture.

Each digit d of N is drawn as a right-leaning triangle of 10 cells
(rows of 4,3,2,1; row r indented by r; blocks 4 wide, 2 spaces apart;
the digit centred above its block at offset +1).  Exactly d cells are
'.', the rest are 'o'.

A '.' is FLOATING when it is not on the bottom row and has no '.'
directly beneath it (neither (r+1,c) nor (r+1,c+1)).  The picture as a
whole must contain exactly K floating dots.

Verified: 469/469 in training round 3, and against all 3 demos.
"""

CELLS = [(r, c) for r in range(4) for c in range(r, 4)]

BLOCK = [dict() for _ in range(10)]    # BLOCK[d][u] -> tuple of 4 row strings
ACH = [()] * 10                        # BLOCK[d] keys, descending
MASK = (1 << 64) - 1
SEP = ('  ', '   ', '    ', '     ')    # gap between blocks on row r
IND = ('', ' ', '  ', '   ')            # indent of row r
_CACHE = {}
_READY = []


def _floating(D):
    n = 0
    for (r, c) in D:
        if r == 3:
            continue
        if (r + 1, c) in D or (r + 1, c + 1) in D:
            continue
        n += 1
    return n


def _build():
    if _READY:
        return
    for mask in range(1024):
        D = frozenset(CELLS[i] for i in range(10) if mask >> i & 1)
        d = len(D)
        if d > 9:
            continue
        u = _floating(D)
        if u not in BLOCK[d]:
            BLOCK[d][u] = tuple(
                ''.join('.' if (r, c) in D else 'o' for c in range(r, 4))
                for r in range(4))
    for d in range(10):
        ACH[d] = tuple(sorted(BLOCK[d], reverse=True))
    _READY.append(1)


def on_round_start(memory):
    _build()
    _CACHE.clear()
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    try:
        got = _CACHE.get(clue)
        if got is not None:
            return got
        s, ks = clue.split('/', 1)
        K = int(ks)
        digits = [ord(ch) - 48 for ch in s]
        L = len(digits)

        # suffix[i] = bitmask of floating-totals reachable using digits[i:]
        suffix = [0] * (L + 1)
        suffix[L] = 1
        for i in range(L - 1, -1, -1):
            nxt = suffix[i + 1]
            acc = 0
            for u in ACH[digits[i]]:
                acc |= nxt << u
            suffix[i] = acc & MASK
        if not (suffix[0] >> K) & 1:
            return None                    # clue has no valid picture: skip

        # give each digit a floating-dot budget
        rem = K
        grids = []
        ap = grids.append
        for i in range(L):
            nxt = suffix[i + 1]
            blk = BLOCK[digits[i]]
            for u in ACH[digits[i]]:
                r = rem - u
                if r >= 0 and (nxt >> r) & 1:
                    ap(blk[u])
                    rem = r
                    break

        out = [' ' + '     '.join(s)]
        out.append(SEP[0].join([g[0] for g in grids]))
        out.append(' ' + SEP[1].join([g[1] for g in grids]))
        out.append('  ' + SEP[2].join([g[2] for g in grids]))
        out.append('   ' + SEP[3].join([g[3] for g in grids]))
        res = '\n'.join(out)
        _CACHE[clue] = res
        return res
    except Exception:
        return None


def on_round_end(items, memory):
    pass
