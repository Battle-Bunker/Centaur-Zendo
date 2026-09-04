"""crandel — solved.

The answer is an ASCII picture: a stack of BLOCKS, each block written as
  * one separator row: '=' everywhere, 'v' on the first and last column of
    every item in that block's top row;
  * h content rows, in which items hang from the separator (top-aligned).

The clue "h a b / h a b / ... / h" summarises it, one group per block:
  h = block height (number of content rows)
  a = number of items reaching the block's BOTTOM row (full-height items)
  b = how many of those a items horizontally overlap an item of the NEXT
      block (the block directly below).
The final block has no block below it, so only its height is given and its
contents are free.

Construction: items live on a slot grid (width 2, pitch 3, so two items in
different blocks overlap iff they share a slot).  Block i gets a_i full-height
items on the slot interval [o_i, o_i+a_i-1] with o_{i+1} = o_i + (a_i - b_i),
which makes exactly b_i of block i's slots reappear in block i+1.  When block
i+1 is too narrow to absorb b_i overlaps, short (height-1) filler items are
added to it — they do not change its own `a`.
"""

LETTERS = "CSPTJD"
IW = 1      # item width in columns
SLOT = 2    # slot pitch: item width + one blank column

_CACHE = {}


def _build(clue):
    parts = clue.split('/')
    m = len(parts)
    H = [int(p[0]) for p in parts]
    A = [int(p[1]) for p in parts[:-1]]
    B = [int(p[2]) for p in parts[:-1]]
    A.append(max(1, B[-1]) if B else 1)
    B.append(0)
    o = [0] * m
    for i in range(m - 1):
        o[i + 1] = o[i] + (A[i] - B[i])
    F = [list(range(o[i], o[i] + A[i])) for i in range(m)]
    E = [[] for _ in range(m)]
    for i in range(m - 1):
        need = B[i] - len(set(F[i]) & set(F[i + 1]))
        s = o[i + 1] + A[i + 1]
        while need > 0 and s <= o[i] + A[i] - 1:
            E[i + 1].append(s)
            need -= 1
            s += 1
    maxslot = max(max(F[i] + E[i]) for i in range(m))
    W = SLOT * (maxslot + 1) - 1
    out = []
    for i in range(m):
        h = H[i]
        items = [(s, h) for s in F[i]] + [(s, 1) for s in E[i]]
        sep = ['='] * W
        for s, _ in items:
            sep[SLOT * s] = 'v'
            sep[SLOT * s + IW - 1] = 'v'
        out.append(''.join(sep))
        for r in range(h):
            line = ['.'] * W
            for s, ih in items:
                if r < ih:
                    ch = LETTERS[(s + i) % 6]
                    base = SLOT * s
                    for c in range(base, base + IW):
                        line[c] = ch
            out.append(''.join(line))
    return '\n'.join(out)


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    ans = _CACHE.get(clue)
    if ans is not None:
        return ans
    try:
        ans = _build(clue)
        if len(ans) > 1024:
            return None
    except Exception:
        return None
    _CACHE[clue] = ans
    return ans


def on_round_end(items, memory):
    pass
