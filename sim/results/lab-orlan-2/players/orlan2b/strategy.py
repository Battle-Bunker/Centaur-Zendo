"""strategy.py - orlan.

WHAT THE CHALLENGE IS (inferred from 6 rounds + 5 demos):
  clue    = a 5x5 / 5x6 / 6x5 / 6x6 grid of '.', '#', 'o', 'x'
  answer  = a move "r,c>r,c" of one of MY pieces ('o') onto an empty cell.

CONFIRMED (48/48 correct answers observed):
  * source is always an 'o', destination always a '.'
  * the move is always orthogonal (a uniform sample of *diagonal* moves
    scored 0/21)
  * the destination is always the SECOND EMPTY CELL along that ray:
    occupied cells ('#', 'x', 'o') are transparent and do not count as
    steps.  Moves landing on the 1st empty cell scored 0/78.
  That leaves ~8 candidate moves per clue.

NOT CRACKED: which of those ~8 is wanted.  Uniform choice measures ~14%.
Two filters have independent support on uniformly-sampled data:
    source NOT orthogonally adjacent to another 'o'   (pos 25% vs neg 50%)
    destination orthogonally adjacent to an 'x'       (pos 75% vs neg 20%)
Applying both lexicographically scores ~36-39% on held-out correct answers.
"""

ORTHO = ((-1, 0), (1, 0), (0, -1), (0, 1))


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        g = clue.split("\n")
        R = len(g)
        C = len(g[0])
        best = None
        bkey = None
        for r in range(R):
            row = g[r]
            for c in range(C):
                if row[c] != 'o':
                    continue
                # source isolation: no friendly piece orthogonally adjacent
                so = 0
                if r and g[r - 1][c] == 'o':
                    so = 1
                elif r + 1 < R and g[r + 1][c] == 'o':
                    so = 1
                elif c and row[c - 1] == 'o':
                    so = 1
                elif c + 1 < C and row[c + 1] == 'o':
                    so = 1
                lone = (so == 0)
                for dr, dc in ORTHO:
                    k = 0
                    rr, cc = r + dr, c + dc
                    while 0 <= rr < R and 0 <= cc < C:
                        if g[rr][cc] == '.':
                            k += 1
                            if k == 2:
                                break
                        rr += dr
                        cc += dc
                    else:
                        continue
                    if k != 2:
                        continue
                    tr, tc = rr, cc
                    dx = False
                    if tr and g[tr - 1][tc] == 'x':
                        dx = True
                    elif tr + 1 < R and g[tr + 1][tc] == 'x':
                        dx = True
                    elif tc and g[tr][tc - 1] == 'x':
                        dx = True
                    elif tc + 1 < C and g[tr][tc + 1] == 'x':
                        dx = True
                    key = (lone, dx)
                    if bkey is None or key > bkey:
                        bkey = key
                        best = (r, c, tr, tc)
        if best is None:
            return None
        return "%d,%d>%d,%d" % best
    except Exception:
        return None


def on_round_end(items, memory):
    pass
