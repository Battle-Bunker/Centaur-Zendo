"""FINAL strategy — self-contained, no imports beyond stdlib.

Cracked:
  basten, N==3 : one `><>` per water row, pushed right until it hits the first
                 post (or the right wall).                        33/33 in training
  fennick, N==0: the picture is unchanged ("0 fall").             14/14 in training
  norvel, n==2 : snare = kick echoed 2 steps later, echoes that would land on a
                 kick hit are dropped, echoes past the end are lost.  ~46%
Everything else is skipped: a skip is instant, scores the same 0 as a wrong
answer, and does not count against the fewer-answers tiebreak.
"""


def on_round_start(memory):
    memory["final"] = True


# ---------- basten ----------
def _basten(clue):
    L = clue.split('\n')
    if int(L[-1].strip()) != 3:
        return None
    top, floor, body = L[0], L[-2], L[1:-2]
    W = len(floor)
    rows = []
    for r in body:
        row = list(r.ljust(W))
        start = None
        placed = False
        for c in range(W + 1):
            wall = (c == W) or (row[c] == '|')
            if wall:
                if start is not None and c - start >= 3:
                    row[c-3] = '>'
                    row[c-2] = '<'
                    row[c-1] = '>'
                    placed = True
                    break
                start = None
            elif start is None:
                start = c
        rows.append(''.join(row))
    return '\n'.join([top] + rows + [floor])


# ---------- fennick ----------
def _fennick(clue):
    L = clue.split('\n')
    if int(L[-1].split()[0]) != 0:
        return None
    out = []
    for line in L:
        if line and line.count('=') == len(line):
            out.append(line)
            return '\n'.join(out)
        out.append(line.rstrip())
    return None


# ---------- norvel ----------
def _norvel(clue):
    L = clue.split('\n')
    n = int(L[2].split('=')[1])
    if n != 2:
        return None
    kick = L[0][6:]
    bars = [b for b in kick.split('|') if b != '']
    seq = ''.join(bars)
    ln = len(seq)
    out = ['.'] * ln
    for i in range(ln):
        if seq[i] == 'x':
            j = i + 2
            if j < ln and seq[j] != 'x':
                out[j] = 'x'
    snare = ''.join(out)
    sb = [snare[i:i+4] for i in range(0, ln, 4)]
    return L[0] + '\n' + L[1][:6] + '|' + '|'.join(sb) + '|'


_HANDLERS = {'basten': _basten, 'fennick': _fennick, 'norvel': _norvel}


def solve(name, clue, memory):
    f = _HANDLERS.get(name)
    if f is None:
        return None
    try:
        return f(clue)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
