"""strategy.py -- FINAL.

fennick : solved  (short trees topple into a one-wide slot)
garrow  : ~35%    (one cut per row that holds the header letter, through its
                   rightmost blob, just before that blob's N-th character)
virel   : ~15%    (5 rows of re-packed boxes, same box count / same dash total,
                   no box wider than 4, the clue itself as the last row)
norvel  : ~30% of the n=2 clues (snare = kick delayed by n slots)
tovel / basten / kelmar : never cracked -> skip (instant, and skips help the
                   fewer-answers tiebreak)
"""
import re, random

# ---------------------------------------------------------------- fennick
def _fennick(clue):
    ls = clue.split('\n')
    eq = max(i for i, l in enumerate(ls) if l and set(l) == {'='})
    grid = ls[:eq]; tail = ls[eq:]
    n = int(ls[-1].split()[0])
    w = max(len(l) for l in grid)
    grid = [list(l.ljust(w)) for l in grid]
    base = len(grid) - 1
    trees = {}; gaps = set()
    brow = grid[base]
    for c in range(w):
        ch = brow[c]
        if ch == '.':
            gaps.add(c)
        elif ch.isalpha():
            h = 0
            for r in range(base, -1, -1):
                if grid[r][c].isalpha():
                    h += 1
                else:
                    break
            trees[c] = h
    if n:
        cands = []
        for c, h in trees.items():
            for d in (-1, 1):
                far = trees.get(c + 2 * d)
                if (c + d) in gaps and far is not None and (c - d) in trees and h < far:
                    cands.append((h, c, d))
        cands.sort()
        for h, c, d in cands[:n]:
            for r in range(base - h, base):
                ch = grid[r][c]
                grid[r][c] = ' '
                grid[r][c + d] = '/' if (d == 1 and ch == '_') else ('\\' if (d == -1 and ch == '_') else ch)
    return '\n'.join(''.join(row).rstrip() for row in grid) + '\n' + '\n'.join(tail)

# ---------------------------------------------------------------- garrow
def _garrow(clue):
    ls = clue.split('\n')
    L = ls[0][0]; N = int(ls[0][1:])
    pic = ls[1:]
    trip = L * 3
    cuts = []
    for row in pic[1:-1]:
        i = row.rfind(trip)
        if i >= 0:
            cuts.append(i + N - 1)
    cuts = sorted(set(cuts))
    out = []
    for row in pic:
        prev = 0; parts = []
        for c in cuts:
            parts.append(row[prev:c]); prev = c
        parts.append(row[prev:])
        out.append('|'.join(parts))
    return '\n'.join(out)

# ---------------------------------------------------------------- virel
def _virel(clue):
    a, b = clue.split('\n')
    W = [len(x) for x in re.findall(r'\[(-*)\]', a)]
    k = len(W); T = sum(W)
    rng = random.Random(len(a) * 131 + T * 17 + k)
    seen = {tuple(W)}
    out = []
    tries = 0
    while len(out) < 4 and tries < 300:
        tries += 1
        v = [0] * k
        left = T
        while left:
            j = rng.randrange(k)
            if v[j] < 4:
                v[j] += 1; left -= 1
            elif all(x >= 4 for x in v):
                break
        if left:
            continue
        t = tuple(v)
        if t in seen:
            continue
        seen.add(t)
        out.append(''.join('[' + '-' * x + ']' for x in v))
    out.append(a)
    return '\n'.join(out)

# ---------------------------------------------------------------- norvel
def _norvel(clue):
    ls = clue.split('\n')
    n = int(ls[-1].split('=')[1])
    if n != 2:
        return None
    kb = [x for x in ls[0].split('|')[1:] if x != '']
    kick = ''.join(kb); tot = len(kick)
    s = ['.'] * tot
    for i in range(n, tot):
        if kick[i - n] == 'x':
            s[i] = 'x'
    return ls[0] + '\nsnare |' + '|'.join(''.join(s[i * 4:i * 4 + 4]) for i in range(len(kb))) + '|'


def on_round_start(memory):
    memory['rounds'] = memory.get('rounds', 0) + 1


def solve(name, clue, memory):
    try:
        if name == 'fennick':
            return _fennick(clue)
        if name == 'garrow':
            return _garrow(clue)
        if name == 'virel':
            return _virel(clue)
        if name == 'norvel':
            return _norvel(clue)
    except Exception:
        return None
    return None


def on_round_end(items, memory):
    pass
