"""Centaur Zendo strategy - round 3 probe."""
import re
from collections import Counter

MUSH = re.compile(r'\(~+\)')
BOX = re.compile(r'\[-*\]')
VEH = re.compile(r'([A-Z]{2}>)|(<[A-Z]{2})')
FISH = re.compile(r'><>|<><')


def _split(clue):
    lines = clue.split('\n')
    return lines[:-1], lines[-1]


# ---------------- kelmar ----------------------------------------------------
def kelmar(clue, i):
    lines = clue.split('\n')
    pic = lines[:-1]
    rows = pic[:-1]
    ground = list(pic[-1])
    H = len(rows)
    for m in MUSH.finditer(rows[0]):
        a, b = m.start(), m.end() - 1
        h = 0
        for r in rows:
            if r[a:b + 1].strip('.') != '':
                h += 1
            else:
                break
        if h != H:
            continue
        if a - 1 >= 0 and ground[a - 1] in '*Y':
            ground[a - 1] = '/'
        if b + 1 < len(ground) and ground[b + 1] in '*Y':
            ground[b + 1] = '\\'
    return '\n'.join(rows + [''.join(ground), lines[-1]])


# ---------------- molvic ----------------------------------------------------
def molvic(clue, i):
    lines = clue.split('\n')
    pic = lines[:-1]
    idx = [k for k, l in enumerate(pic) if l.startswith('|')]
    grids = []
    for k in idx:
        inner = pic[k][1:-1]
        grids.append([inner[j] for j in range(0, len(inner), 2)])
    home = [Counter([c for c in g if c != ' ']).most_common(1)[0][0] for g in grids]
    pos = {h: r for r, h in enumerate(home)}
    for r, g in enumerate(grids):
        for c in range(len(g)):
            a = g[c]
            if a == ' ' or a == home[r]:
                continue
            s = pos.get(a)
            if s is None or s <= r:
                continue
            if grids[s][c] == home[r]:
                grids[r][c], grids[s][c] = grids[s][c], grids[r][c]
    out = list(pic)
    for n, k in enumerate(idx):
        out[k] = '|' + ' '.join(grids[n]) + '|'
    return '\n'.join(out + [lines[-1]])


# ---------------- virel -----------------------------------------------------
def _row(nboxes, W):
    d = W - 2 * nboxes
    if d < 0:
        return None
    return '[-]' * d + '[]' * (nboxes - d)


def _smash(widths):
    out = []
    for w in widths:
        if w % 2 == 0:
            out += [2] * (w // 2)
        else:
            out += [3] + [2] * ((w - 3) // 2)
    out.sort(reverse=True)
    return ''.join('[' + '-' * (w - 2) + ']' for w in out)


def virel(clue, i):
    pic, tail = _split(clue)
    rows = [[len(m.group()) for m in BOX.finditer(l)] for l in pic]
    W = sum(rows[0])
    new = _row(9, W) or _row(W // 2, W) or _smash(rows[-1])
    return chr(10).join([new] + pic)


# ---------------- garrow ----------------------------------------------------
def _cuts(pic, L, N, rl, pad):
    body = pic[1:-1]
    W = len(pic[0])
    cnt = [0] * W
    empty = [True] * W
    for r in body:
        for c, ch in enumerate(r):
            if ch == L:
                cnt[c] += 1
            if ch != ':':
                empty[c] = False
    cuts = set()
    acc = 0
    for c in (range(W - 1, -1, -1) if rl else range(W)):
        acc += cnt[c]
        if acc >= N and cnt[c]:
            b = c - 1 if rl else c
            if pad and rl and b >= 1 and empty[b]:
                b -= 1
            cuts.add(b)
            acc = 0
    return {c for c in cuts if 0 <= c < W - 1}


def garrow(clue, i):
    lines = clue.split('\n')
    h = lines[0].split()
    L, N = h[0], int(h[1])
    pic = lines[1:]
    cs = _cuts(pic, L, N, True, False)
    return '\n'.join(''.join(ch + ('|' if c in cs else '')
                             for c, ch in enumerate(r)) for r in pic)


# ---------------- basten / durnel : only the no-op cases ---------------------
def basten(clue, i):
    pic, tail = _split(clue)
    if int(tail.split()[0]) == 0:
        return chr(10).join(pic)
    return None


def durnel(clue, i):
    pic, tail = _split(clue)
    if int(tail.split()[0]) == 0:
        return chr(10).join(pic)
    return None


# ---------------- fennick (long shot) ---------------------------------------
def fennick(clue, i):
    pic, tail = _split(clue)
    n = int(tail.split()[0])
    if n == 0:
        return '\n'.join(pic)
    return None


HANDLERS = {'kelmar': kelmar, 'molvic': molvic, 'virel': virel,
            'garrow': garrow, 'basten': basten, 'durnel': durnel,
            'fennick': fennick}


def on_round_start(memory):
    memory['rounds_played'] = memory.get('rounds_played', 0) + 1


def solve(name, clue, memory):
    try:
        f = HANDLERS.get(name)
        if f is None:
            return None
        return f(clue, memory.get('_index', 0))
    except Exception:
        return None


def on_round_end(items, memory):
    pass
