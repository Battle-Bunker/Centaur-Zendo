"""Centaur Zendo strategy - tovel4a."""
import re

_ROW = re.compile(r'^([A-Z]{3})\s+\|(.*)\|$')

# ---------------- garrow ----------------
def solve_garrow(clue):
    L = clue.rstrip('\n').split('\n')
    tail = L[-1].split()
    letter = tail[0]; n = int(tail[1])
    if n == 0:
        return clue
    tok = letter * 2
    body = L[1:4]
    segs = [l.split('|') for l in body]
    nb = len(segs[0])
    for b in range(nb):
        c = 0
        for r in range(3):
            c += segs[r][b].count(tok)
        if c >= 2:
            for r in range(3):
                segs[r][b] = segs[r][b].replace(':', '*')
    out = [L[0]] + ['|'.join(segs[r]) for r in range(3)] + [L[4]]
    return '\n'.join(out)

# ---------------- tovel ----------------
def solve_tovel(clue):
    L = clue.rstrip('\n').split('\n')
    n = int(L[-1].split()[0])
    if n == 0:
        return clue
    weeks = L[1:-1]
    pos = {}   # day -> (line_idx, char_idx)
    letter = {}
    for li, line in enumerate(weeks):
        for c in range(7):
            a = 4 * c
            if a + 2 < len(line):
                s = line[a:a + 2].strip()
                if s.isdigit():
                    d = int(s)
                    pos[d] = (li, a + 2)
                    letter[d] = line[a + 2]
    if not pos:
        return clue
    mx = max(pos)
    occ = [d for d in range(1, mx + 1) if letter.get(d, '.') != '.']
    runs = []; cur = []
    for d in range(1, mx + 2):
        if d in pos and letter.get(d, '.') != '.':
            cur.append(d)
        else:
            if cur:
                runs.append(cur); cur = []
    bump = []
    for r in runs:
        if len(r) >= 3:
            bump.extend(r[1:-1])
    bump.sort()
    used = set()
    new = dict(letter)
    for d in bump:
        ch = letter[d]
        new[d] = '>'
        t = d + 1
        while t <= mx:
            if letter.get(t, '.') == '.' and t not in used:
                break
            t += 1
        if t <= mx:
            new[t] = ch
            used.add(t)
    lines = [list(w) for w in weeks]
    for d, (li, ci) in pos.items():
        lines[li][ci] = new[d]
    return '\n'.join([L[0]] + [''.join(x) for x in lines] + [L[-1]])

# ---------------- molvic ----------------
def solve_molvic(clue):
    L = clue.rstrip('\n').split('\n')
    n = int(L[-1].split()[0])
    if n == 0:
        return clue
    idx = []; labels = []; cells = []
    for i, line in enumerate(L):
        m = _ROW.match(line)
        if m:
            idx.append(i); labels.append(m.group(1).lower())
            cells.append(m.group(2).split(' '))
    if not idx:
        return clue
    empt = [[j for j, v in enumerate(c) if v == '___'] for c in cells]
    best = {}
    for r, c in enumerate(cells):
        lab = labels[r]
        for j, v in enumerate(c):
            if v != '___' and v != lab:
                k = (j, r)
                if v not in best or k > best[v]:
                    best[v] = k
    moves = []
    for v, (j, r) in best.items():
        if v not in labels:
            continue
        h = labels.index(v)
        if not empt[h]:
            continue
        moves.append((v, j, r, h))
    if len(moves) != n:
        return None
    for v, j, r, h in moves:
        cells[r][j] = '___'
        cells[h][empt[h][0]] = v
    out = list(L)
    for k, i in enumerate(idx):
        m = _ROW.match(L[i])
        pre = L[i][:L[i].index('|') + 1]
        out[i] = pre + ' '.join(cells[k]) + '|'
    return '\n'.join(out)

# ---------------- rule families ----------------
import json as _json, os as _os, sys as _sys
_DIR = _os.path.dirname(_os.path.abspath(__file__))
if _DIR not in _sys.path:
    _sys.path.insert(0, _DIR)
import rules as _rules
try:
    _W = _json.load(open(_os.path.join(_DIR, 'weights.json')))
except Exception:
    _W = {}

PIC = {'garrow': solve_garrow, 'tovel': solve_tovel, 'molvic': solve_molvic}
RF = ('borsel', 'kaldrin', 'mestrel')


def on_round_start(memory):
    memory['rounds_played'] = memory.get('rounds_played', 0) + 1


def solve(name, clue, memory):
    try:
        if name in PIC:
            return PIC[name](clue)
        if name == 'felsim':
            # only the zero-edit case is solvable for us; skip the rest
            if clue.rstrip('\n').rsplit('\n', 1)[-1].split()[0] == '0':
                return clue
            return None
        if name in RF:
            return _rules.choose(name, clue, _W)[1]
    except Exception:
        return None
    return None


def on_round_end(items, memory):
    pass
