"""murn — solved.

Clue is "<row>|<N>".  The answer is a grid of lines, each as wide as the clue
row, whose LAST line IS the clue row, containing exactly N '#' above it.
For any cell above the bottom line, let k be the number of non-'.' cells in the
line directly below it within +-1 column.  Then:

    k == 1  ->  the cell may be 'o'
    k == 2  ->  the cell may be '#'
    always  ->  the cell may be '.'

(a non-'.' cell also never sits directly on top of the same symbol).

We build upward from the clue row with bitmasks, greedily taking every k == 2
slot as a '#' until N are placed, and padding with 'o' in the k == 1 slots
whenever another row is still needed.
"""

MAX_LEN = 1024


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def gen(row, N):
    W = len(row)
    if W == 0:
        return None
    if N <= 0:
        return row
    FULL = (1 << W) - 1
    ndm = hm = om = 0
    bit = 1
    for ch in row:
        if ch != '.':
            ndm |= bit
            if ch == '#':
                hm |= bit
            else:
                om |= bit
        bit <<= 1
    rem = N
    out = []
    for _ in range(60):
        a = ndm >> 1
        c = (ndm << 1) & FULL
        s1 = a ^ ndm ^ c
        carry = (a & ndm) | (ndm & c) | (a & c)
        cand = carry & ~s1 & ~hm & FULL
        newh = 0
        placed = 0
        while cand and placed < rem:
            low = cand & -cand
            newh |= low
            cand -= low
            placed += 1
        rem -= placed
        newo = (s1 & ~carry & ~om & FULL) if rem > 0 else 0
        if not (newh | newo):
            return None
        out.append((newh, newo))
        if rem <= 0:
            break
        ndm = newh | newo
        hm = newh
        om = newo
    if rem > 0:
        return None
    lines = []
    for h, o in reversed(out):
        arr = ['.'] * W
        while h:
            low = h & -h
            arr[low.bit_length() - 1] = '#'
            h -= low
        while o:
            low = o & -o
            arr[low.bit_length() - 1] = 'o'
            o -= low
        lines.append("".join(arr))
    lines.append(row)
    ans = "\n".join(lines)
    if len(ans) > MAX_LEN:
        return None
    return ans


def solve(name, clue, memory):
    try:
        i = clue.rfind("|")
        if i < 1:
            return None
        return gen(clue[:i], int(clue[i + 1:]))
    except Exception:
        return None


def on_round_end(items, memory):
    pass
