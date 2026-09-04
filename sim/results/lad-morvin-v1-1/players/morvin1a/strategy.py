"""morvin — final solver.

Clue is "N/k".  The answer is a picture of N: one 4-row upper-triangular block
of 10 cells per digit (rows of 4/3/2/1 cells), blocks 4 chars wide separated by
two spaces, preceded by a header line carrying each digit at offset 1 of its
block.  A block for digit d holds exactly d dots; the other cells are 'o'.

Which cells are 'o' is constrained.  Every accepted picture satisfies

    k == sum over blocks of [ (# vertical pairs with '.' directly above 'o')
                              + (1 if the block's top-left cell is '.') ]

but that is necessary, not sufficient: within a block, only some arrangements of
a given value are accepted.  LIB below holds one *server-confirmed* arrangement
for each (digit, value) pair, learned by probing (each probe changed exactly one
block so the result could be attributed).  Block contributions add, so a small
DP splits k across the blocks using only confirmed arrangements.

Confirmed empty: digit 6 value 5 and digit 9 value 1 are not achievable
(0/37 and 0/45 probes accepted), so they are absent from LIB.
"""

LIB = {
    0: {0: 'oooooooooo'},
    1: {0: 'ooooooooo.', 1: 'oooooooo.o'},
    2: {0: 'oooooooo..', 1: '.ooo.ooooo', 2: '.oo.oooooo'},
    3: {0: 'ooooooo...', 1: 'oooooo..o.', 2: '.ooo.o.ooo', 3: '..o.oooooo'},
    4: {0: 'oooooo....', 1: '.ooo..o.oo', 2: '..oo.o.ooo', 3: '.oooo..oo.',
        4: '....oooooo'},
    5: {0: 'ooooo.....', 1: 'oo.o.oo...', 2: '...o..oooo', 3: '..o...oooo',
        4: '....ooooo.', 5: '....oooo.o'},
    6: {0: 'oooo......', 1: 'oo...o.o..', 2: '.o....o.oo', 3: '...oo.o..o',
        4: '....oooo..'},
    7: {0: 'ooo.......', 1: '.o.oo.....', 2: '...o....oo', 3: '.......ooo',
        4: '....oo...o'},
    8: {0: 'oo........', 1: '.o..o.....', 2: '..o......o', 3: '......o..o'},
    9: {0: 'o.........', 2: '.........o'},
}


def _rows(cells):
    out = []
    i = 0
    for r in range(4):
        s = ' ' * r
        for _ in range(r, 4):
            s += cells[i]
            i += 1
        out.append(s)
    return out


ROWS = [{t: _rows(s) for t, s in LIB[d].items()} for d in range(10)]
MASK = [sum(1 << t for t in LIB[d]) for d in range(10)]
DIG = {str(i): i for i in range(10)}
HDR = {str(i): ' ' + str(i) + '  ' for i in range(10)}
MAXK = 60
CACHE = {}


def on_round_start(memory):
    CACHE.clear()


def solve(name, clue, memory):
    try:
        got = CACHE.get(clue)
        if got is not None:
            return got
        n, ks = clue.split('/')
        k = int(ks)
        if k < 0 or k > MAXK:
            return None
        ds = [DIG[ch] for ch in n]
        L = len(ds)
        # forward reachability over block prefixes
        reach = [1] * (L + 1)
        for x in range(L):
            cur = reach[x]
            m = MASK[ds[x]]
            nxt = 0
            t = 0
            while m:
                if m & 1:
                    nxt |= cur << t
                m >>= 1
                t += 1
            reach[x + 1] = nxt
        if not (reach[L] >> k) & 1:
            return None
        blocks = [None] * L
        rem = k
        for x in range(L - 1, -1, -1):
            m = MASK[ds[x]]
            t = 0
            while t <= rem:
                if (m >> t) & 1 and (reach[x] >> (rem - t)) & 1:
                    blocks[x] = ROWS[ds[x]][t]
                    rem -= t
                    break
                t += 1
            else:
                return None
        ans = ('  '.join(HDR[ch] for ch in n).rstrip() + '\n'
               + '  '.join(b[0] for b in blocks) + '\n'
               + '  '.join(b[1] for b in blocks) + '\n'
               + '  '.join(b[2] for b in blocks) + '\n'
               + '  '.join(b[3] for b in blocks))
        if len(CACHE) < 20000:
            CACHE[clue] = ans
        return ans
    except Exception:
        return None


def on_round_end(items, memory):
    pass
