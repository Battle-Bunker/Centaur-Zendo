"""Centaur Zendo solver — team dornic1b.

Every class is the same puzzle in a different costume: one or two POSITIVE
examples, then a final NEGATIVE example, a blank line, then five candidates.
Exactly one candidate obeys the hidden rule.

We enumerate ~1000 cheap boolean properties of an item, keep those true of
every positive and false of the negative, and let each such property that
singles out exactly ONE candidate vote for it, weighted by how likely that
KIND of rule is for that class (learned from 274 scored answers + 3 demos):
  tavrik  letters      - contains / starts with / ends with X, number of vowels
  tresk   R,G,B string - substrings, runs, colour counts
  wisbek  clock times  - DIGIT rules (digit sum, repeated digit, hour digit
                         inside the minutes), not hand geometry
  dornic  card hands   - a named rank or card, suit counts, pairs/flush
  mestrel dominoes     - a named tile, how many of a pip, biggest pip
  kaldrin marked chain - marks, repeated goods, what follows what
  ospren  5x5 grid     - full/empty rows and columns, symmetry, counts
Deterministic, ~0.3 ms per challenge, never raises.
"""


import string

V = set('aeiou')

# ---------------- words (tavrik) ----------------
def f_word(w):
    k = set(); s = set(w); n = len(w)
    for c in s:
        k.add('has_'+c)
        if w.count(c) >= 2: k.add('twice_'+c)
        if w.count(c) >= 3: k.add('thrice_'+c)
    k.add('starts_'+w[0]); k.add('ends_'+w[-1])
    k.add('len_%d'%n)
    if n % 2 == 0: k.add('len_even')
    nv = sum(1 for c in w if c in V)
    k.add('nvow_%d'%nv)
    if nv % 2 == 0: k.add('nvow_even')
    nc = n - nv
    k.add('ncons_%d'%nc)
    k.add('ndist_%d'%len(s))
    if len(s) == n: k.add('alldist')
    else: k.add('hasrep')
    if any(w[i] == w[i+1] for i in range(n-1)): k.add('dbl')
    if w[0] in V: k.add('first_vowel')
    if w[-1] in V: k.add('last_vowel')
    if w[0] == w[-1]: k.add('first_eq_last')
    if list(w) == sorted(w): k.add('sorted_asc')
    pat = ''.join('V' if c in V else 'C' for c in w)
    k.add('cv_'+pat)
    if 'VV' in pat: k.add('vv_adj')
    if 'CCC' in pat: k.add('ccc')
    if 'CC' in pat: k.add('cc_adj')
    if all(pat[i] != pat[i+1] for i in range(n-1)): k.add('alternating')
    tot = sum(ord(c)-96 for c in w)
    k.add('sum_even' if tot % 2 == 0 else 'sum_odd')
    for m in (3,4,5): k.add('sum%d_%d'%(m, tot % m))
    k.add('nfh_%d'%sum(1 for c in w if c <= 'm'))
    if all(c <= 'm' for c in w): k.add('all_first_half')
    if all(c >= 'n' for c in w): k.add('all_second_half')
    if any(abs(ord(a)-ord(b)) == 1 for a in s for b in s): k.add('adj_alpha')
    if any(abs(ord(w[i])-ord(w[i+1])) == 1 for i in range(n-1)): k.add('adj_alpha_seq')
    if w == w[::-1]: k.add('palindrome')
    for L in (2,3):
        for i in range(n-L+1): k.add('sub_'+w[i:i+L])
    for i, c in enumerate(w):
        k.add('p%d_%s'%(i,c)); k.add('q%d_%s'%(n-i,c))
    vs = [c for c in w if c in V]
    if vs:
        k.add('v1_'+vs[0]); k.add('vlast_'+vs[-1])
        if len(set(vs)) == 1: k.add('one_vowel_kind')
        if vs == sorted(vs): k.add('vowels_sorted')
    return k

# ---------------- RGB strings (tresk) ----------------
def f_rgb(s):
    k = set(); n = len(s)
    k.add('len_%d'%n)
    k.add('len_even' if n % 2 == 0 else 'len_odd')
    for c in 'RGB':
        cnt = s.count(c)
        k.add('cnt%s_%d'%(c,cnt))
        k.add('cnt%s_even'%c if cnt % 2 == 0 else 'cnt%s_odd'%c)
        if cnt == 0: k.add('no_'+c)
        if cnt >= 1: k.add('has_'+c)
        for m in (3,4): k.add('cnt%s_m%d_%d'%(c,m,cnt%m))
    for a in 'RGB':
        for b in 'RGB':
            if s.count(a) > s.count(b): k.add('more_%s_%s'%(a,b))
            if s.count(a) == s.count(b): k.add('eq_%s_%s'%(a,b))
    k.add('start_'+s[0]); k.add('end_'+s[-1])
    if s[0] == s[-1]: k.add('first_eq_last')
    runs = []
    cur = s[0]; ln = 1
    for ch in s[1:]:
        if ch == cur: ln += 1
        else: runs.append((cur,ln)); cur = ch; ln = 1
    runs.append((cur,ln))
    k.add('nruns_%d'%len(runs))
    k.add('nruns_even' if len(runs) % 2 == 0 else 'nruns_odd')
    mx = max(r[1] for r in runs)
    k.add('maxrun_%d'%mx)
    for j in range(1, mx+1): k.add('maxrun_ge_%d'%j)
    if mx == 1: k.add('no_adjacent_equal')
    else: k.add('has_adjacent_equal')
    for c in 'RGB':
        rm = max([r[1] for r in runs if r[0]==c] or [0])
        k.add('maxrun%s_%d'%(c,rm))
    if s == s[::-1]: k.add('palindrome')
    for L in (2,3,4):
        for i in range(n-L+1): k.add('sub_'+s[i:i+L])
    k.add('pfx2_'+s[:2]); k.add('sfx2_'+s[-2:])
    k.add('ndist_%d'%len(set(s)))
    return k

# ---------------- times (wisbek) ----------------
def f_time(t):
    k = set()
    h, m = t.split(':'); H = int(h); M = int(m)
    k.add('h_%d'%H); k.add('m_%d'%M)
    k.add('h_even' if H % 2 == 0 else 'h_odd')
    k.add('m_even' if M % 2 == 0 else 'm_odd')
    for d in range(2, 16):
        if M % d == 0: k.add('m_div_%d'%d)
        if H % d == 0: k.add('h_div_%d'%d)
    for ch in set(h+m): k.add('digit_'+ch)
    ds = sum(int(c) for c in h+m)
    k.add('dsum_%d'%ds); k.add('dsum_even' if ds % 2 == 0 else 'dsum_odd')
    for mm in (3,4,5): k.add('dsum%d_%d'%(mm, ds%mm))
    k.add('hm_sum_%d'%(H+M))
    k.add('hm_sum_even' if (H+M) % 2 == 0 else 'hm_sum_odd')
    if M > 30: k.add('m_gt30')
    if M < 30: k.add('m_lt30')
    if M == 30: k.add('m_eq30')
    if M == 0: k.add('oclock')
    if M % 5 == 0: k.add('on_mark')
    if M < 10: k.add('m_single_digit')
    if H > M: k.add('h_gt_m')
    if H == M: k.add('h_eq_m')
    if H < M: k.add('h_lt_m')
    digs = h + m
    if len(set(digs)) < len(digs): k.add('rep_digit')
    else: k.add('all_digits_distinct')
    if h in m or (len(h)==1 and h in m): k.add('h_digit_in_m')
    # hand geometry
    ang = (30*(H % 12) + 0.5*M) - 6*M
    ang = abs(ang) % 360
    if ang > 180: ang = 360 - ang
    k.add('ang_%d'%int(round(ang)))
    if abs(ang) < 1e-6: k.add('hands_together')
    if abs(ang-180) < 1e-6: k.add('hands_opposite')
    if abs(ang-90) < 1e-6: k.add('hands_right_angle')
    if ang < 90: k.add('ang_lt90')
    if ang > 90: k.add('ang_gt90')
    if abs(ang % 30) < 1e-6: k.add('ang_mult30')
    tot = (H % 12)*60 + M
    k.add('tot_even' if tot % 2 == 0 else 'tot_odd')
    for d in (3,4,5,6,7,10,11,12,15,20,30):
        if tot % d == 0: k.add('tot_div_%d'%d)
    k.add('mten_%s'%m[0]); k.add('mone_%s'%m[1])
    if int(m[0]) == int(m[1]): k.add('m_same_digits')
    if M == H*5: k.add('minute_points_at_hour')
    k.add('nd_%d'%len(h+m))
    return k

# ---------------- cards (dornic) ----------------
RANKV = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13,'A':14}
def f_cards(line):
    k = set()
    cards = line.split()
    ranks = []; suits = []
    for c in cards:
        suits.append(c[-1]); ranks.append(RANKV[c[:-1]])
    n = len(cards); k.add('ncards_%d'%n)
    from collections import Counter
    rc = Counter(ranks); sc = Counter(suits)
    for s in 'CDHS':
        k.add('n%s_%d'%(s, sc.get(s,0)))
        if sc.get(s,0) > 0: k.add('has_'+s)
        else: k.add('no_'+s)
    k.add('nsuits_%d'%len(sc))
    if len(sc) == 1: k.add('flush')
    red = sc.get('H',0)+sc.get('D',0)
    k.add('nred_%d'%red); k.add('nblack_%d'%(n-red))
    k.add('red_even' if red % 2 == 0 else 'red_odd')
    if red == n: k.add('all_red')
    if red == 0: k.add('all_black')
    for r in ranks: k.add('rank_%d'%r)
    k.add('ndistinct_ranks_%d'%len(rc))
    cnts = sorted(rc.values(), reverse=True)
    k.add('shape_'+'-'.join(map(str,cnts)))
    if cnts[0] >= 2: k.add('has_pair')
    if cnts[0] >= 3: k.add('has_trips')
    if cnts[0] >= 4: k.add('has_quads')
    if cnts.count(2) >= 2: k.add('two_pair')
    if cnts[0] == 1: k.add('all_ranks_distinct')
    sr = sorted(set(ranks))
    if len(sr) == n and sr[-1]-sr[0] == n-1: k.add('straight')
    if any(sr[i]+1 == sr[i+1] for i in range(len(sr)-1)): k.add('has_consec')
    tot = sum(ranks)
    k.add('sum_%d'%tot); k.add('sum_even' if tot % 2 == 0 else 'sum_odd')
    for m in (3,4,5,10): k.add('sum%d_%d'%(m, tot % m))
    k.add('max_%d'%max(ranks)); k.add('min_%d'%min(ranks))
    k.add('span_%d'%(max(ranks)-min(ranks)))
    nf = sum(1 for r in ranks if r >= 11)
    k.add('nface_%d'%nf)
    if nf == 0: k.add('no_face')
    if 14 in ranks: k.add('has_ace')
    ne = sum(1 for r in ranks if r % 2 == 0)
    k.add('neven_%d'%ne)
    if ne == n: k.add('all_even')
    if ne == 0: k.add('all_odd')
    nl = sum(1 for r in ranks if r <= 7)
    k.add('nlow_%d'%nl)
    mx = max(sc.values())
    k.add('maxsuit_%d'%mx)
    if mx >= 3: k.add('three_same_suit')
    if mx >= 4: k.add('four_same_suit')
    for s in 'CDHS':
        if sc.get(s,0) >= 2: k.add('twoplus_'+s)
    return k

# ---------------- kaldrin chains ----------------
def f_chain(line):
    k = set()
    toks = [t for t in line.replace('[','').split(']') if t.strip('=')]
    toks = [t.strip('=') for t in line.split('[') if t]
    toks = []
    for part in line.split('=')[1:]:
        t = part.strip()[1:-1]
        toks.append(t)
    goods = [t.rstrip('^') for t in toks]
    car = [t.endswith('^') for t in toks]
    n = len(toks); k.add('len_%d'%n)
    k.add('len_even' if n % 2 == 0 else 'len_odd')
    from collections import Counter
    gc = Counter(goods)
    for g in set(goods):
        k.add('has_'+g); k.add('cnt_%s_%d'%(g, gc[g]))
        if gc[g] >= 2: k.add('twice_'+g)
    k.add('ndistinct_%d'%len(gc))
    nc = sum(car); k.add('ncar_%d'%nc)
    k.add('ncar_even' if nc % 2 == 0 else 'ncar_odd')
    if nc == 0: k.add('no_caret')
    if nc == n: k.add('all_caret')
    k.add('first_'+goods[0]); k.add('last_'+goods[-1])
    if car[0]: k.add('first_caret')
    if car[-1]: k.add('last_caret')
    if any(goods[i] == goods[i+1] for i in range(n-1)): k.add('adj_same')
    else: k.add('no_adj_same')
    if len(gc) == 1: k.add('all_same_good')
    runs = 1
    for i in range(n-1):
        if goods[i] != goods[i+1]: runs += 1
    k.add('nruns_%d'%runs)
    mx = 1; cur = 1
    for i in range(n-1):
        if goods[i] == goods[i+1]: cur += 1; mx = max(mx,cur)
        else: cur = 1
    k.add('maxrun_%d'%mx)
    for i in range(n-1):
        k.add('big_%s_%s'%(goods[i],goods[i+1]))
    for g in set(goods):
        idx = [i for i in range(n) if goods[i]==g]
        if all(car[i] for i in idx): k.add('always_caret_'+g)
        if not any(car[i] for i in idx): k.add('never_caret_'+g)
    for i in range(n):
        if car[i]: k.add('car_at_%d'%i); k.add('car_from_end_%d'%(n-i))
    k.add('most_'+max(gc, key=lambda g:(gc[g],g)))
    if any(car[i] and car[i+1] for i in range(n-1)): k.add('two_carets_adj')
    return k

# ---------------- mestrel dominoes ----------------
def f_dom(line):
    k = set()
    tiles = []
    for part in line.split(']'):
        part = part.strip()
        if not part: continue
        a,b = part.lstrip('[').split('|')
        tiles.append((int(a), int(b)))
    n = len(tiles); k.add('ntiles_%d'%n)
    k.add('ntiles_even' if n % 2 == 0 else 'ntiles_odd')
    from collections import Counter
    pips = Counter()
    for a,b in tiles: pips[a]+=1; pips[b]+=1
    for v in range(7):
        k.add('cntpip_%d_%d'%(v, pips.get(v,0)))
        if pips.get(v,0) > 0: k.add('haspip_%d'%v)
        else: k.add('nopip_%d'%v)
    tc = Counter(tuple(sorted(t)) for t in tiles)
    for t,c in tc.items():
        k.add('tile_%d_%d'%t)
        if c >= 2: k.add('rep_tile_%d_%d'%t)
    if any(c >= 2 for c in tc.values()): k.add('has_repeated_tile')
    else: k.add('all_tiles_distinct')
    nd = sum(1 for a,b in tiles if a == b)
    k.add('ndoubles_%d'%nd)
    if nd == 0: k.add('no_double')
    if nd > 0: k.add('has_double')
    k.add('ndoub_even' if nd % 2 == 0 else 'ndoub_odd')
    tot = sum(a+b for a,b in tiles)
    k.add('sum_%d'%tot); k.add('sum_even' if tot % 2 == 0 else 'sum_odd')
    for m in (3,4,5,7,10): k.add('sum%d_%d'%(m, tot % m))
    allp = [x for t in tiles for x in t]
    k.add('maxpip_%d'%max(allp)); k.add('minpip_%d'%min(allp))
    k.add('ndistinctpip_%d'%len(set(allp)))
    if all((a+b) % 2 == 0 for a,b in tiles): k.add('all_tile_sum_even')
    if all(a % 2 == 0 and b % 2 == 0 for a,b in tiles): k.add('all_pips_even')
    if all(a+b >= 6 for a,b in tiles): k.add('all_tile_sum_ge6')
    if all(tiles[i][1] == tiles[i+1][0] for i in range(n-1)): k.add('chain_strict')
    if all(set(tiles[i]) & set(tiles[i+1]) for i in range(n-1)): k.add('chain_loose')
    if any(set(tiles[i]) & set(tiles[i+1]) for i in range(n-1)): k.add('some_adj_share')
    k.add('first_double' if tiles[0][0]==tiles[0][1] else 'first_not_double')
    k.add('last_double' if tiles[-1][0]==tiles[-1][1] else 'last_not_double')
    for v in range(7):
        if all(v in t for t in tiles): k.add('all_contain_%d'%v)
    k.add('firsttile_%d_%d'%tuple(sorted(tiles[0])))
    k.add('lasttile_%d_%d'%tuple(sorted(tiles[-1])))
    k.add('nblank_%d'%pips.get(0,0))
    sums = [a+b for a,b in tiles]
    k.add('maxtilesum_%d'%max(sums)); k.add('mintilesum_%d'%min(sums))
    if len(set(sums)) == 1: k.add('all_tile_sums_equal')
    return k

# ---------------- grids (ospren) ----------------
def f_grid(g):
    k = set()
    rows = g if isinstance(g, list) else g.split('\n')
    R = len(rows); C = len(rows[0])
    cells = [[1 if ch == '#' else 0 for ch in r] for r in rows]
    tot = sum(sum(r) for r in cells)
    k.add('cnt_%d'%tot)
    k.add('cnt_even' if tot % 2 == 0 else 'cnt_odd')
    for m in (3,4,5): k.add('cnt%d_%d'%(m, tot % m))
    if tot > R*C/2: k.add('majority_filled')
    for i in range(R):
        s = sum(cells[i]); k.add('row%d_%d'%(i,s))
        if s == C: k.add('rowfull_%d'%i)
        if s == 0: k.add('rowempty_%d'%i)
    for j in range(C):
        s = sum(cells[i][j] for i in range(R)); k.add('col%d_%d'%(j,s))
        if s == R: k.add('colfull_%d'%j)
        if s == 0: k.add('colempty_%d'%j)
    if any(sum(cells[i]) == C for i in range(R)): k.add('some_row_full')
    if any(all(cells[i][j] for i in range(R)) for j in range(C)): k.add('some_col_full')
    if all(sum(cells[i]) > 0 for i in range(R)): k.add('all_rows_nonempty')
    if all(any(cells[i][j] for i in range(R)) for j in range(C)): k.add('all_cols_nonempty')
    rs = [sum(r) for r in cells]
    cs = [sum(cells[i][j] for i in range(R)) for j in range(C)]
    if len(set(rs)) == 1: k.add('rows_equal_count')
    if len(set(cs)) == 1: k.add('cols_equal_count')
    k.add('maxrow_%d'%max(rs)); k.add('minrow_%d'%min(rs))
    k.add('maxcol_%d'%max(cs)); k.add('mincol_%d'%min(cs))
    if all(rows[i] == rows[i][::-1] for i in range(R)): k.add('sym_lr')
    if rows == rows[::-1]: k.add('sym_ud')
    if [r[::-1] for r in rows][::-1] == rows: k.add('sym_180')
    tr = [''.join(rows[i][j] for i in range(R)) for j in range(C)]
    if tr == rows: k.add('sym_diag')
    if [r[::-1] for r in tr][::-1] == rows: k.add('sym_antidiag')
    if cells[R//2][C//2]: k.add('center')
    corners = cells[0][0]+cells[0][C-1]+cells[R-1][0]+cells[R-1][C-1]
    k.add('ncorners_%d'%corners)
    if corners == 4: k.add('all_corners')
    if corners == 0: k.add('no_corners')
    border = sum(cells[0]) + sum(cells[R-1]) + sum(cells[i][0]+cells[i][C-1] for i in range(1,R-1))
    k.add('nborder_%d'%border)
    if border == 2*R+2*C-4: k.add('border_full')
    if border == 0: k.add('border_empty')
    if all(cells[i][i] for i in range(min(R,C))): k.add('diag_full')
    if all(cells[i][C-1-i] for i in range(min(R,C))): k.add('antidiag_full')
    if any(cells[i][j] and cells[i][j+1] and cells[i+1][j] and cells[i+1][j+1]
           for i in range(R-1) for j in range(C-1)): k.add('has_2x2')
    else: k.add('no_2x2')
    # connected components (4-neighbour) of filled cells
    seen = set(); comp = 0
    for i in range(R):
        for j in range(C):
            if cells[i][j] and (i,j) not in seen:
                comp += 1; st = [(i,j)]; seen.add((i,j))
                while st:
                    a,b = st.pop()
                    for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
                        x,y = a+da,b+db
                        if 0<=x<R and 0<=y<C and cells[x][y] and (x,y) not in seen:
                            seen.add((x,y)); st.append((x,y))
    k.add('ncomp_%d'%comp)
    if comp == 1: k.add('connected')
    if len(set(rows)) < R: k.add('two_rows_same')
    if len(set(tr)) < C: k.add('two_cols_same')
    for i in range(R): k.add('rowpat%d_%s'%(i, rows[i]))
    return k

P = {
# letters: "has X" / "starts with X" / "ends with X" / "N vowels"
'tavrik': {'has':2.0,'starts':2.0,'ends':2.0,'nvow':1.8,'twice':1.0,'dbl':1.2,
  'alldist':0.9,'hasrep':0.9,'first_vowel':1.0,'last_vowel':1.0,'first_eq_last':1.0,
  'len':0.7,'len_even':0.5,'nvow_even':0.6,'ndist':0.4,'ncons':0.6,'one_vowel_kind':0.9,
  'vowels_sorted':0.4,'v1':0.8,'vlast':0.8,'sorted_asc':0.6,'palindrome':1.0,
  'alternating':0.6,'cv':0.2,'cvy':0.2,'vv_adj':0.5,'cc_adj':0.4,'ccc':0.4,
  'sub':0.35,'adj_alpha':0.25,'all_first_half':0.5,'all_second_half':0.5,
  'sum_even':0.25,'sum_odd':0.25,'sum3':0.1,'sum4':0.1,'sum5':0.1,'nfh':0.05,
  'max_gt_t':0.3,'min_lt_e':0.3,'y_end':1.0,
  'p0':0.3,'p1':0.3,'p2':0.3,'p3':0.3,'p4':0.3,'p5':0.3,'p6':0.3,'p7':0.3,'p8':0.3,
  'q1':0.3,'q2':0.3,'q3':0.3,'q4':0.3,'q5':0.3,'q6':0.3,'q7':0.3,'q8':0.3},
# RGB: substrings, runs, colour counts
'tresk': {'sub':1.4,'pfx2':1.4,'sfx2':1.4,'start':1.6,'end':1.6,'first_eq_last':1.2,
  'cntR':1.2,'cntG':1.2,'cntB':1.2,'no':1.5,'has':1.2,'more':1.3,'eq':1.3,
  'maxrun':1.2,'maxrunR':1.2,'maxrunG':1.2,'maxrunB':1.2,'no_adjacent_equal':1.4,
  'has_adjacent_equal':1.1,'nruns':0.8,'nruns_even':0.7,'nruns_odd':0.7,
  'palindrome':1.2,'ndist':0.8,'len':0.7,'len_even':0.5,'len_odd':0.5,
  'cntR_m3':0.35,'cntG_m3':0.35,'cntB_m3':0.35,'cntR_m4':0.3,'cntG_m4':0.3,'cntB_m4':0.3},
# times: digit rules, not clock geometry
'wisbek': {'dsum':1.7,'dsum_even':1.4,'dsum_odd':1.4,'h_digit_in_m':1.7,
  'rep_digit':1.4,'all_digits_distinct':1.4,'digit':1.4,'on_mark':1.4,'oclock':1.3,
  'm_gt30':1.3,'m_lt30':1.3,'m_eq30':1.3,'m_single_digit':1.2,'m_same_digits':1.3,
  'm_even':1.1,'m_odd':1.1,'h_even':1.1,'h_odd':1.1,'m_div':0.8,'h_div':0.8,
  'mten':0.8,'mone':0.8,'h':0.55,'m':0.4,'hm_sum':0.35,'hm_sum_even':0.7,'hm_sum_odd':0.7,
  'dsum3':0.5,'dsum4':0.5,'dsum5':0.5,'h_gt_m':0.6,'h_eq_m':0.6,'h_lt_m':0.6,
  'minute_points_at_hour':0.4,'tot_even':0.3,'tot_odd':0.3,'tot_div':0.15,
  'ang':0.08,'ang_lt90':0.15,'ang_gt90':0.15,'ang_mult30':0.2,'hands_together':0.5,
  'hands_opposite':0.5,'hands_right_angle':0.5,'nd':0.0},
# cards: a named rank, a named card, suit counts
'dornic': {'rank':1.3,'card':1.0,'max':1.0,'min':0.8,'span':0.8,
  'nsuits':1.5,'three_same_suit':1.5,'four_same_suit':1.5,'maxsuit':1.1,
  'nC':1.2,'nD':1.2,'nH':1.2,'nS':1.2,'has':1.3,'no':1.3,'twoplus':0.9,
  'flush':1.8,'has_pair':1.6,'two_pair':1.6,'has_trips':1.6,'has_quads':1.6,
  'all_ranks_distinct':1.3,'straight':1.8,'has_consec':1.0,'has_ace':1.5,
  'no_face':1.3,'nface':1.1,'all_red':1.6,'all_black':1.6,'nred':1.0,'nblack':0.4,
  'red_even':0.5,'red_odd':0.5,'all_even':1.6,'all_odd':1.6,'neven':0.8,
  'ndistinct_ranks':0.9,'shape':0.9,'sum_even':0.9,'sum_odd':0.9,'sum':0.0,
  'sum3':0.3,'sum4':0.3,'sum5':0.3,'sum10':0.25,'nlow':0.5,'ncards':0.4},
# dominoes: a named tile, how many of a pip, biggest/smallest pip
'mestrel': {'tile':1.2,'cntpip':0.9,'haspip':1.2,'nopip':1.2,'maxpip':1.0,'minpip':1.0,
  'maxtilesum':0.9,'mintilesum':0.9,'rep_tile':0.8,'has_repeated_tile':1.3,
  'all_tiles_distinct':1.3,'ndoubles':1.0,'no_double':1.4,'has_double':1.4,
  'ndoub_even':0.6,'ndoub_odd':0.6,'ndistinctpip':0.9,'all_tile_sum_even':1.1,
  'all_pips_even':1.3,'all_tile_sum_ge6':0.9,'chain_strict':1.6,'chain_loose':1.6,
  'some_adj_share':0.9,'first_double':1.0,'last_double':1.0,'first_not_double':1.0,
  'last_not_double':1.0,'all_contain':1.3,'firsttile':0.9,'lasttile':0.9,'nblank':0.7,
  'all_tile_sums_equal':1.3,'ntiles':0.7,'sum':0.0,'sum_even':0.9,'sum_odd':0.9,
  'sum3':0.35,'sum4':0.3,'sum5':0.35,'sum7':0.3,'sum10':0.25},
# chain: marks, repeats, what follows what
'kaldrin': {'has':1.5,'twice':1.4,'cnt':1.0,'most':1.0,'last':1.4,'first':1.2,
  'big':0.9,'always_caret':1.2,'never_caret':1.1,'car_at':1.2,'car_from_end':1.0,
  'ncar':1.0,'ncar_even':0.8,'ncar_odd':0.8,'no_caret':1.4,'all_caret':1.4,
  'first_caret':1.2,'last_caret':1.3,'adj_same':1.1,'no_adj_same':1.1,
  'all_same_good':1.4,'nruns':0.9,'maxrun':1.0,'ndistinct':1.0,'len':0.8,
  'two_carets_adj':0.9},
}
def w(name,key):
    d=P.get(name,{})
    if key in d: return d[key]
    parts=key.split('_')
    for i in range(len(parts),0,-1):
        p='_'.join(parts[:i])
        if p in d: return d[p]
    return 1.0


import re as _re
_FR1=_re.compile(r'_-?\d+$'); _FR2=_re.compile(r'_-?\d+_-?\d+$')
P['mestrel']['tile']=1.8; P['mestrel']['cntpip']=1.3
_GRIDBOOST=frozenset(('rowfull','rowempty','colfull','colempty'))
FEAT={'tavrik':f_word,'tresk':f_rgb,'wisbek':f_time,'dornic':f_cards,
      'kaldrin':f_chain,'mestrel':f_dom,'ospren':f_grid}
_WC={n:{} for n in FEAT}

def _w(name,key):
    c=_WC[name]; v=c.get(key)
    if v is None:
        if name=='ospren':
            v=1.4 if key.split('_')[0] in _GRIDBOOST else 1.0
        else:
            v=w(name,_FR1.sub('',_FR2.sub('',key)))
        c[key]=v
    return v

def parse(name, clue):
    blocks=clue.split('\n\n')
    if name=='ospren':
        exs=[]; cands=[]
        for b in blocks:
            ls=b.split('\n')
            if len(ls)==6 and ls[0].strip().isdigit(): cands.append('\n'.join(ls[1:]))
            else: exs.append(b)
        return exs,cands
    return blocks[0].split('\n'), blocks[1].split('\n')

def choose(name, clue):
    f=FEAT[name]
    exs,cands=parse(name,clue)
    if name=='dornic':
        K=[f(x)|{'card_'+c for c in x.split()} for x in exs]
        C=[f(x)|{'card_'+c for c in x.split()} for x in cands]
    else:
        K=[f(x) for x in exs]; C=[f(x) for x in cands]
    pos=K[:-1]; neg=K[-1]
    inter=set(pos[0])
    for p in pos[1:]: inter&=p
    union=set()
    for p in pos: union|=p
    v=[0.0]*len(C)
    for k in sorted(inter-neg):
        hit=-1; n=0
        for i,s in enumerate(C):
            if k in s:
                hit=i; n+=1
                if n>1: break
        if n==1: v[hit]+=_w(name,k)
    for k in sorted(neg-union):
        miss=-1; n=0
        for i,s in enumerate(C):
            if k not in s:
                miss=i; n+=1
                if n>1: break
        if n==1: v[miss]+=_w(name,k)
    return cands[v.index(max(v))]

def on_round_start(memory):
    memory["rounds_played"]=memory.get("rounds_played",0)+1

def solve(name, clue, memory):
    try:
        return choose(name, clue)
    except Exception:
        try: return clue.split('\n\n')[-1].split('\n')[0]
        except Exception: return None

def on_round_end(items, memory):
    pass
