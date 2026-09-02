"""LegoZendo solver.

Clue = <LETTER><N>.  Answer = an ASCII Lego build (2 rows per brick, 3 columns
per stud) whose LARGEST connected same-colour region of <LETTER> is exactly N
studs.  The whole build must be one connected blob (a disconnected/floating
brick is rejected).

N == 0  -> build with a different colour only.
N >= 2  -> one brick of N studs (3*N wide, 2 tall).
(N == 1 never occurs: a 1-stud region reads as 0.)

Everything is precomputed in on_round_start; solve() is one dict lookup.
"""

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TABLE = {}


def _build(c, n):
    if n <= 0:
        o = "A" if c != "A" else "B"
        row = o * 3
        return row + "\n" + row + "\n" + row + "\n" + row
    row = c * (3 * n)
    return row + "\n" + row


def on_round_start(memory):
    TABLE.clear()
    for c in ALPHA:
        for n in range(0, 41):
            TABLE[c + str(n)] = _build(c, n)


def solve(name, clue, memory):
    try:
        return TABLE[clue]
    except Exception:
        pass
    try:
        c = clue[0]
        if not ("A" <= c <= "Z"):
            return None
        n = int(clue[1:])
        if n > 300:
            return None
        return _build(c, n)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
