"""Round 6: compose / reduce the known-good walls.

Known templates (clue value -> wall, key colour):
    2 -> D1/G     3 -> D3/E     10 -> D4/I     12 -> D2/X
Everything is recoloured so the clue's letter takes the key colour's place.
This round tests: erasing the other colours, cropping, concatenating two
walls (is the count additive?) and deleting one region of the key colour.
"""

D1 = '~~~OO~~~NNN~~~~JJJLLL~~~~~~GG~~~\nGGGOO~~~NNN~~~~JJJLLL~~~~~~GGGGG\nGGGOO~~NNN~~~~~~~OOO~~YY~~~GGGGG\nJJJ~~~~NNN~~~~~~~OOO~~YYOO~~GGG~\nJJJ~~~LLLKKK~~~~LLL~~~YYOO~~GGG~\n~~~~~~LLLKKK~~~~LLL~~~YYOO~~~~~~\n~YYLL~~~~GGG~~~~~~OO~~YY~~~~~LLL\n~YYLL~~~~GGG~~~OOOOOGGYYLLYY~LLL\n~YYLL~GG~~~GGG~OOOOOGG~~LLYY~KKK\n~~~~~~GG~~~GGG~~GGG~GGGGLLYY~KKK\n~~~~~~GG~~~JJJ~~GGG~~~GG~~~~~~~~\n~~~~~~~~~~~JJJ~~~~~~~~GG~~~~~~~~'
D2 = 'PP-------------------OO---------LL------CCC-----\nPP-------------XXPPCCOOXXCC-JJXXLLLLZZ--CCC-----\nPP--------ZZ---XXPPCCOOXXCC-JJXXLLLLZZ--JJJ-----\n---XX-----ZZ-ZZXXPPCC--XXCC-JJXXXXLLZZ--JJJ-----\n---XX-----ZZ-ZZ-----------------XX--CCXX--PPP---\n-XXXX--XX----ZZ------XXX--XXCCLLXXXXCCXX--PPP---\n-XX-XXXXXPPP---------XXX--XXCCLL--XXCCXX-CCC----\n-XX-XXXXXPPP--------OOO-XXXXCCLL--XXXX---CCC----\n----XXX-------------OOO-XX--ZZZ-ZZZ-XX--PPP---XX\n----XXX--------------CCCXXXXZZZ-ZZZ-XX--PPP---XX\n----XXX--------------CCC--XX-JJJZZZCCC--CCC---XX\n----XXX----LL--------OOOCCXX-JJJZZZCCC--CCC-----\n--OOOXXX---LL--XX----OOOCCXXX--XXX--XXX-XXX-----\n--OOOXXX---LL--XXCCPP---CCXXX--XXX--XXX-XXX-----\n-----JJJ-----XXXXCCPP----XXXXXXXXX-XXXXXX-ZZZ---\n-----JJJ-----XXPPCCPP----XXXXXXXXX-XXXXXX-ZZZ---\n-------CCC---XXPP------XXX---XXX----ZZZ--ZZZ----\n-------CCC-----PP------XXX---XXX----ZZZ--ZZZ----'
D3 = '........................EEE...\n.EEE.NNNVVV.EEE.........EEE.OO\n.EEE.NNNVVV.EEEEEYYNN.......OO\nYYY..VVV..EEE..EEYYNN..JJOO.OO\nYYY..VVV..EEE..EEYYNNJJJJOO...\n..NNNUUU.UUUEEE...OO.JJJJOO...\n..NNNUUU.UUUEEE...OO.JJ.......\n....OOO...JJJ.....OO.....VVJJ.\n....OOO...JJJ.EEOO....EEEVVJJ.\n...EEE...YYEEEEEOO....EEEVVJJ.\n...EEE...YYEEEEEOO..EEEVVV....\n.........YY.........EEEVVV....'
D4 = '*****XXX**II*******IIVVJJ*II****JJJ***II********\n*****XXX**II*******IIVVJJ*II****JJJ***II**IINN**\n******ZZZ*II*******IIVVJJ*II**********II**IINNII\n******ZZZ*CCII**IIJJXXZZ********JJ********IINNII\n*****VVV**CCII**IIJJXXZZ**II**NNJJ**********CCII\n*****VVV**CCIIIIIIJJXXZZ**II**NNJJ**********CCZZ\n**************II**********II**NN*******II***CCZZ\nIII***III*NNCCII*JJJ*****************NNIIVV***ZZ\nIII***III*NNCC***JJJ*******CCC*******NNIIVVJJ***\nNNN***III*NNCC*CCC*********CCCCCC****NN**VVJJ***\nNNN***III******CCC*********JJJCCC**********JJ***\n*IIIIIIJJJVVV***VVV**VVZZNNJJJ*******III*JJJ****\n*IIIIIIJJJVVV***VVV**VVZZNNNNN*******III*JJJ*II*\n***VVVIII*III**XXXJJJVVZZNNNNN*****III*IIIIIIII*\n***VVVIII*III**XXXJJJ***XXXIII*****III*IIIIIIII*\n*****VVVIIIVVV***ZZZ*VV*XXXIII****VVV***III*III*\n*****VVVIIIVVV***ZZZ*VV**VVVIII***VVV***III*III*\n*********************VV**VVVIII*****************'

BASE = {2: (D1, "G"), 3: (D3, "E"), 10: (D4, "I"), 12: (D2, "X")}
POOL_A = "BCDFHKMPQRSTVWYZ"
POOL_B = "ZYWVTSRQPMKHFDCB"
MAXLEN = 1024
_cache = {}


def _empty_of(grid):
    best = None; n = -1
    for ch in set(grid):
        if ch == "\n":
            continue
        c = grid.count(ch)
        if c > n:
            n = c; best = ch
    return best


def _colours(grid, empty):
    out = []
    for ch in grid:
        if ch != empty and ch != "\n" and ch not in out:
            out.append(ch)
    return out


def _recolour(grid, src, target, pool, empty):
    mapping = {src: target}
    used = {target}
    pi = 0
    for ch in _colours(grid, empty):
        if ch == src:
            continue
        while pool[pi] in used:
            pi += 1
        mapping[ch] = pool[pi]; used.add(pool[pi])
    return grid.translate(str.maketrans(mapping))


def _erase_others(grid, keep, empty):
    out = []
    for ch in grid:
        if ch == "\n" or ch == empty or ch == keep:
            out.append(ch)
        else:
            out.append(empty)
    return "".join(out)


def _crop(grid, empty):
    rows = grid.split("\n")
    keep = [i for i, r in enumerate(rows) if any(c != empty for c in r)]
    if not keep:
        return grid
    r0, r1 = keep[0], keep[-1]
    cols = [j for j in range(len(rows[0])) if any(rows[i][j] != empty for i in range(r0, r1 + 1))]
    c0, c1 = cols[0], cols[-1]
    return "\n".join(r[c0:c1 + 1] for r in rows[r0:r1 + 1])


def _hcat(a, b, empty, gap=2):
    ra = a.split("\n"); rb = b.split("\n")
    h = max(len(ra), len(rb))
    wa = len(ra[0]); wb = len(rb[0])
    ra = ra + [empty * wa] * (h - len(ra))
    rb = rb + [empty * wb] * (h - len(rb))
    return "\n".join(ra[i] + empty * gap + rb[i] for i in range(h))


def _vcat(a, b, empty, gap=1):
    ra = a.split("\n"); rb = b.split("\n")
    w = max(len(ra[0]), len(rb[0]))
    ra = [r.ljust(w, empty) for r in ra]
    rb = [r.ljust(w, empty) for r in rb]
    return "\n".join(ra + [empty * w] * gap + rb)


def _regions(grid, colour, empty):
    rows = grid.split("\n")
    H = len(rows); W = len(rows[0])
    seen = set(); out = []
    for r in range(H):
        for c in range(W):
            if rows[r][c] == colour and (r, c) not in seen:
                st = [(r, c)]; seen.add((r, c)); cells = []
                while st:
                    y, x = st.pop(); cells.append((y, x))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        p = (y + dy, x + dx)
                        if 0 <= p[0] < H and 0 <= p[1] < W and p not in seen and rows[p[0]][p[1]] == colour:
                            seen.add(p); st.append(p)
                out.append(cells)
    out.sort(key=lambda cs: (-len(cs), cs[0]))
    return out


def _delete(grid, cells, empty):
    rows = [list(r) for r in grid.split("\n")]
    for (y, x) in cells:
        rows[y][x] = empty
    return "\n".join("".join(r) for r in rows)


def _mono(ch):
    band = ("%s~" % (ch * 3)) * 8
    return "\n".join((band if r in (1, 2, 6, 7) else "~" * 32)[:32] for r in range(12))


REG = {}


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1
    for val, (grid, key) in BASE.items():
        REG[val] = _regions(grid, key, _empty_of(grid))
    _precompute()


def _variant(letter, n, v):
    """Build variant v for clue letter/number n."""
    if n == 0:
        return _mono(letter)
    if n in (10, 12):
        g, k = BASE[n]
        e = _empty_of(g)
        if v % 2 == 1 and n == 10:
            return _recolour(_erase_others(g, k, e), k, letter, POOL_A, e)
        return _recolour(g, k, letter, POOL_A, e)
    if n == 2:
        g, k = BASE[2]; e = _empty_of(g)
        if v % 4 == 0:
            return _recolour(g, k, letter, POOL_A, e)
        if v % 4 == 1:
            return _recolour(_erase_others(g, k, e), k, letter, POOL_A, e)
        if v % 4 == 2:
            return _recolour(_crop(_erase_others(g, k, e), e), k, letter, POOL_A, e)
        rows = g.split("\n")
        return _recolour("\n".join(r[::-1] for r in rows), k, letter, POOL_A, e)
    if n == 3:
        g, k = BASE[3]; e = _empty_of(g)
        if v % 3 == 0:
            return _recolour(g, k, letter, POOL_A, e)
        if v % 3 == 1:
            return _recolour(_erase_others(g, k, e), k, letter, POOL_A, e)
        return _recolour(_crop(_erase_others(g, k, e), e), k, letter, POOL_A, e)
    if n in (4, 5, 6):
        pa = {4: (2, 2), 5: (2, 3), 6: (3, 3)}[n]
        g1, k1 = BASE[pa[0]]; g2, k2 = BASE[pa[1]]
        e = _empty_of(g1)
        g2 = g2.replace(_empty_of(g2), e)
        a = _recolour(g1, k1, letter, POOL_A, e)
        b = _recolour(g2, k2, letter, POOL_B, e)
        if v % 3 == 0:
            out = _hcat(a, b, e)
        elif v % 3 == 1:
            out = _vcat(a, b, e)
        else:
            a = _crop(_erase_others(g1, k1, e), e); b = _crop(_erase_others(g2, k2, e), e)
            out = _hcat(_recolour(a, k1, letter, POOL_A, e), _recolour(b, k2, letter, POOL_B, e), e)
        if len(out) <= MAXLEN:
            return out
        return _recolour(g1, k1, letter, POOL_A, e)
    # n in 1,7,8,9,11 -> delete one region of the key colour from a bigger wall
    base = {1: 2, 7: 10, 8: 10, 9: 10, 11: 12}[n]
    g, k = BASE[base]; e = _empty_of(g)
    regs = REG[base]
    cells = regs[v % len(regs)]
    return _recolour(_delete(g, cells, e), k, letter, POOL_A, e)



# ---------------------------------------------------------------- final answers
# A lone "staircase pair" (two same-orientation bricks offset by one column) is
# worth exactly 1: deleting one such region from D1 dropped its value 2 -> 1,
# and joining two walls adds their values.  So n copies of it should score n.
UNIT = ["###..", "###..", "..###", "..###"]


def _pack(letter, k):
    """A wall of k separated staircase pairs -> value k."""
    H, W = 12, 32
    g = [["~"] * W for _ in range(H)]
    slots = [(r, c) for r in (1, 7) for c in (0, 6, 12, 18, 24)]
    for i in range(min(k, len(slots))):
        r0, c0 = slots[i]
        for dr, row in enumerate(UNIT):
            for dc, ch in enumerate(row):
                if ch == "#":
                    g[r0 + dr][c0 + dc] = letter
    return "\n".join("".join(row) for row in g)


# n -> (how the answer is built).  Every entry except 7 and 9 scored 100% in
# training round 6; 7 and 9 use the packing above.
PLAN = {0: ("v", 0), 1: ("v", 2), 2: ("v", 0), 3: ("v", 0), 4: ("v", 0),
        5: ("v", 0), 6: ("v", 1), 7: ("pack", 7), 8: ("v", 2), 9: ("pack", 9),
        10: ("v", 0), 11: ("v", 4), 12: ("v", 0)}

ANSWERS = {}
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _precompute():
    ANSWERS.clear()
    for letter in LETTERS:
        for n, (kind, arg) in PLAN.items():
            try:
                if kind == "pack":
                    s = _pack(letter, arg)
                else:
                    s = _variant(letter, n, arg)
                if s and len(s) <= MAXLEN:
                    ANSWERS[letter + str(n)] = s
            except Exception:
                pass


def solve(name, clue, memory):
    a = ANSWERS.get(clue)
    if a is not None:
        return a
    try:
        letter = clue[0].upper()
        n = int(clue[1:])
        return ANSWERS.get(letter + str(n))
    except Exception:
        return None


def on_round_end(items, memory):
    pass
