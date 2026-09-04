"""fennick — a shelf of books, drawn from the side.

CLUE   "<shelf>/<L:n L:n L:n L:n>"
       shelf: one char per slot; a letter is a book's spine, '.' is a gap.
       tail : for four named letters, how many of those books LEAN over.

ANSWER the shelf seen from the side:
         H rows of air, the shelf line itself, then the shelf board '===='.
       Every line is padded with spaces to the shelf's width.  A book of
       height h standing in slot c is its own letter repeated h times going
       up from the shelf line, with a '_' lid one row above the top.  A book
       that has tipped over draws its whole body and its lid one column to
       the side, and its lid is '/' (tipped right) or '\' (tipped left).

PHYSICS a book tips over iff  (a) the slot on one side of it is empty,
       (b) it is still touching a book on its other side — a book with gaps
       on BOTH sides just stands up straight — and (c) the book across that
       empty slot is strictly taller, so there is something to rest against.

Any shelf that obeys the physics and has exactly the stated number of
leaners for each named letter scores 1, so we build the simplest one:
every book stands 2 high, and each book that has to lean is cut to 1 so it
tips against its 2-high neighbour.  Nothing else can then tip, because a
book only tips towards something TALLER than itself.
"""


def _slot(base, n, i):
    """(direction, supporting book) if the book in slot i is able to tip."""
    for d in (-1, 1):
        a = i + d
        if 0 <= a < n and base[a] == '.':
            b = i + d + d
            o = i - d
            if 0 <= b < n and 0 <= o < n and base[b] != '.' and base[o] != '.':
                return d, b
            return None
    return None


def solve_fennick(clue):
    p = clue.index('/')
    base = clue[:p]
    n = len(base)

    want = []
    for tok in clue[p + 1:].split():
        k = int(tok[2:])
        if k:
            want.append((tok[0], k))
    if not want:
        lid = ''.join(' ' if c == '.' else '_' for c in base)
        return lid + '\n' + base + '\n' + '=' * n

    want.sort(key=lambda t: -t[1])
    elig = {}
    for L, k in want:
        e = []
        for i in range(n):
            if base[i] == L:
                s = _slot(base, n, i)
                if s:
                    e.append((i, s[0], s[1]))
        if len(e) < k:
            return None
        elig[L] = e

    chosen = {}
    targets = set()
    budget = [3000]

    def rec(wi, pool, k):
        if wi == len(want):
            return True
        if k == want[wi][1]:
            w = wi + 1
            return rec(w, elig[want[w][0]] if w < len(want) else (), 0)
        budget[0] -= 1
        if budget[0] < 0:
            return False
        for idx in range(len(pool)):
            i, d, j = pool[idx]
            if i in chosen or i in targets or j in chosen:
                continue
            chosen[i] = d
            targets.add(j)
            if rec(wi, pool[idx + 1:], k + 1):
                return True
            del chosen[i]
            targets.discard(j)
        return False

    if not rec(0, elig[want[0][0]], 0):
        return None

    top = [' '] * n
    mid = [' '] * n
    for i in range(n):
        c = base[i]
        if c == '.':
            continue
        d = chosen.get(i)
        if d is None:
            top[i] = '_'
            mid[i] = c
        else:
            mid[i + d] = '/' if d > 0 else '\\'
    return ''.join(top) + '\n' + ''.join(mid) + '\n' + base + '\n' + '=' * n


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    try:
        return solve_fennick(clue)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
