"""Centaur Zendo strategy - tavrik1b."""
import string

VOW = frozenset('aeiou')

def _primes(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2, int(n**0.5)+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j]=False
    return frozenset(i for i,v in enumerate(s) if v)
PRIMES = _primes(1000)

# ---------------------------------------------------------------- norvel
def solve_norvel(clue):
    lines = clue.split('\n')
    idx = {}
    for i, ln in enumerate(lines):
        if '|' in ln:
            idx[ln.split('|')[0].strip()] = i
    si = idx.get('snare')
    if si is None:
        return clue
    def flat(i):
        ln = lines[i]
        return ''.join(b for b in ln[ln.index('|'):].split('|') if b)
    sn = list(flat(si))
    hat = flat(idx['hat']) if 'hat' in idx else '.'*len(sn)
    kick = flat(idx['kick']) if 'kick' in idx else '.'*len(sn)
    L = len(sn)
    moves = []
    for p in range(L):
        if sn[p] == 'x' and hat[p] != 'x' and kick[p] != 'x':
            t = -1
            for q in range(p+1, L):
                if hat[q] == 'x':
                    t = q; break
            if t > p:
                moves.append((p, t))
    for p, t in moves:
        for q in range(p, t):
            if sn[q] != 'x' or q == p:
                sn[q] = '-'
        sn[t] = 'x'
    ln = lines[si]
    p = ln.index('|')
    w = len(ln[p:].split('|')[1])
    body = ''.join(sn)
    lines[si] = ln[:p] + '|' + '|'.join(body[k:k+w] for k in range(0, L, w)) + '|'
    return '\n'.join(lines)


# ---------------------------------------------------------------- features
def f_borsel(s):
    a = [int(x) for x in s.split()]
    n = len(a); st = set(a)
    d = {}
    for v in range(1, 7): d['cnt%d' % v] = a.count(v)
    mn = min(a); mx = max(a); sm = sum(a)
    d['min']=mn; d['max']=mx; d['range']=mx-mn; d['sum']=sm
    d['ndist']=len(st)
    d['nodd']=sum(1 for x in a if x & 1); d['neven']=n-d['nodd']
    d['mode']=max(a.count(v) for v in st)
    d['nadjeq']=sum(1 for i in range(n-1) if a[i]==a[i+1])
    d['nadjcons']=sum(1 for i in range(n-1) if abs(a[i]-a[i+1])==1)
    d['npairs']=sum(1 for v in st if a.count(v)==2)
    d['asc']=int(all(a[i]<=a[i+1] for i in range(n-1)))
    d['desc']=int(all(a[i]>=a[i+1] for i in range(n-1)))
    d['pal']=int(a==a[::-1]); d['fl']=int(a[0]==a[-1])
    d['consecval']=int(any(v+1 in st for v in st))
    return d

def f_tresk(s):
    d = {}
    cr=s.count('R'); cg=s.count('G'); cb=s.count('B')
    d['cntR']=cr; d['cntG']=cg; d['cntB']=cb
    for c in 'RGB':
        mr=0; cur=0
        for ch in s:
            cur = cur+1 if ch==c else 0
            if cur>mr: mr=cur
        d['run'+c]=mr
    for a in 'RGB':
        for b in 'RGB':
            d['bi'+a+b]=s.count(a+b)
    d['ndist']=len(set(s))
    d['nruns']=1+sum(1 for i in range(len(s)-1) if s[i]!=s[i+1])
    mr=1; cur=1
    for i in range(1,len(s)):
        cur = cur+1 if s[i]==s[i-1] else 1
        if cur>mr: mr=cur
    d['maxrun']=mr
    d['fl']=int(s[0]==s[-1]); d['pal']=int(s==s[::-1])
    d['first']=ord(s[0]); d['last']=ord(s[-1])
    d['cntR%2']=cr%2; d['cntG%2']=cg%2; d['cntB%2']=cb%2
    d['noadj']=int(all(s[i]!=s[i+1] for i in range(len(s)-1)))
    d['dRB']=cr-cb; d['dGB']=cg-cb; d['dRG']=cr-cg
    return d

def f_tavrik(w):
    d = {}
    st=set(w)
    for c in st: d['c_'+c]=w.count(c)
    n=len(w)
    d['ndist']=len(st)
    nv=sum(1 for c in w if c in VOW)
    d['nvow']=nv; d['ncons']=n-nv
    d['ndistvow']=len(set(c for c in w if c in VOW))
    d['ndouble']=sum(1 for i in range(n-1) if w[i]==w[i+1])
    d['maxlet']=max(w.count(c) for c in st)
    d['nrep']=sum(1 for c in st if w.count(c)>1)
    d['first']=ord(w[0])-96; d['last']=ord(w[-1])-96
    d['fv']=int(w[0] in VOW); d['lv']=int(w[-1] in VOW)
    d['fl']=int(w[0]==w[-1])
    d['nalphaadj']=sum(1 for i in range(n-1) if abs(ord(w[i])-ord(w[i+1]))==1)
    d['alphapair']=int(any(chr(ord(c)+1) in st for c in st))
    mc=0; cur=0
    for c in w:
        cur = cur+1 if c not in VOW else 0
        if cur>mc: mc=cur
    d['maxcons']=mc
    mv=0; cur=0
    for c in w:
        cur = cur+1 if c in VOW else 0
        if cur>mv: mv=cur
    d['maxvow']=mv
    d['pal']=int(w==w[::-1])
    d['sorted']=int(list(w)==sorted(w))
    d['cvpal']=int((lambda p: p==p[::-1])(''.join('v' if c in VOW else 'c' for c in w)))
    return d

def f_wisbek(s):
    h, m = s.split(':'); h=int(h); m=int(m)
    ds = str(h) + '%02d' % m
    d={}
    d['h']=h; d['m']=m
    dsum=sum(int(c) for c in ds); d['dsum']=dsum
    msum=(m//10)+(m%10); d['msum']=msum
    d['mt']=m//10; d['mu']=m%10
    d['ndist']=len(set(ds))
    for k in (2,3,4,5,6,7,8,9,10,11,12,15):
        d['m%%%d'%k]=m%k
    for k in (2,3,4,5,6):
        d['h%%%d'%k]=h%k
    d['dsum%2']=dsum%2; d['dsum%3']=dsum%3; d['dsum%5']=dsum%5
    d['tot%5']=(h*60+m)%5
    d['hm%2']=(h+m)%2; d['hm%3']=(h+m)%3
    d['mprime']=int(m in PRIMES); d['hprime']=int(h in PRIMES)
    d['totprime']=int((h*60+m) in PRIMES)
    d['msum_eq_h']=int(msum==h)
    d['mdivh']=int(h>0 and m%h==0)
    d['mgt']=int(m>h)
    d['mt_eq_h']=int(m//10==h); d['mu_eq_h']=int(m%10==h)
    d['mt_eq_mu']=int(m//10==m%10)
    d['rep']=int(len(set(ds))<len(ds))
    d['pal']=int(ds==ds[::-1])
    d['hdig_in_m']=int(any(c in ('%02d'%m) for c in str(h)))
    d['m5h']=int(m==5*(h%12))
    d['incr']=int(all(ds[i]<ds[i+1] for i in range(len(ds)-1)))
    d['decr']=int(all(ds[i]>ds[i+1] for i in range(len(ds)-1)))
    d['hm']=h+m; d['mh']=m-h
    d['nodd']=sum(1 for c in ds if int(c)&1)
    hh = h % 12
    d['m5h10']=(m-5*hh)%10
    d['m5h5']=(m-5*hh)%5
    d['mk_h_par']=(((m//5)-hh)%2) if m%5==0 else 7
    ang=int(round(abs(((hh*30+m*0.5)-(m*6))%360)*2))
    if ang>720: ang=1440-ang
    d['ang2']=ang
    d['ang_mult60']=int(ang%60==0)
    d['ang_mult180']=int(ang%180==0)
    d['mon5']=int(m%5==0)
    d['dsum_lt10']=int(dsum<10)
    d['hpar_mpar']=(h+m)%2
    d['handdist']=abs((m//5)-hh) if m%5==0 else 7
    return d

RANKV = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13}
def f_dornic(s):
    rs=[]; su=[]
    for tok in s.split():
        rs.append(RANKV[tok[:-1]]); su.append(tok[-1])
    d={}
    for x in 'CDHS': d['s'+x]=su.count(x)
    d['maxsuit']=max(d['sC'],d['sD'],d['sH'],d['sS'])
    d['nsuits']=len(set(su))
    S=set(rs)
    d['ndistrank']=len(S)
    d['maxrankcnt']=max(rs.count(v) for v in S)
    d['npairs']=sum(1 for v in S if rs.count(v)==2)
    d['span']=max(rs)-min(rs); d['minr']=min(rs); d['maxr']=max(rs)
    sm=sum(rs); d['sum%2']=sm%2
    d['nface']=sum(1 for v in rs if v>=11)
    d['nred']=sum(1 for x in su if x=='D' or x=='H'); d['nblack']=len(su)-d['nred']
    d['nlow']=sum(1 for v in rs if v<=5)
    d['nodd']=sum(1 for v in rs if v&1); d['neven']=len(rs)-d['nodd']
    d['nconsec']=sum(1 for v in S if v+1 in S)
    d['c3']=int(any(v+1 in S and v+2 in S for v in S))
    d['ace']=int(1 in S); d['king']=int(13 in S)
    for v in S: d['r_%d'%v]=rs.count(v)
    d['alldist']=int(len(S)==len(rs))
    srt=sorted(S)
    d['gapmax']=max([b-a for a,b in zip(srt,srt[1:])] or [0])
    d['suitcons']=sum(1 for i in range(len(rs)) if any(rs[j]==rs[i]+1 and su[j]==su[i] for j in range(len(rs))))
    return d

def f_ospren(lines):
    g = tuple(tuple(1 if ch=='#' else 0 for ch in r) for r in lines)
    n=len(g); m=len(g[0])
    T=tuple(zip(*g))
    fl=tuple(tuple(reversed(r)) for r in g)
    fu=tuple(reversed(g))
    d={}
    cnt=sum(sum(r) for r in g); d['cnt']=cnt
    d['lr']=int(g==fl); d['ud']=int(g==fu)
    d['r180']=int(g==tuple(tuple(reversed(r)) for r in fu))
    d['tr']=int(g==T)
    d['anti_s']=int(g==tuple(zip(*tuple(tuple(reversed(r)) for r in fu))))
    rc=[sum(r) for r in g]; cc=[sum(c) for c in T]
    d['maxrow']=max(rc); d['minrow']=min(rc); d['maxcol']=max(cc); d['mincol']=min(cc)
    d['nemptyrow']=rc.count(0); d['nemptycol']=cc.count(0)
    d['nfullrow']=rc.count(m); d['nfullcol']=cc.count(n)
    d['ndistrow']=len(set(g)); d['ndistcol']=len(set(T))
    d['corners']=g[0][0]+g[0][-1]+g[-1][0]+g[-1][-1]
    k=min(n,m)
    d['diag']=sum(g[i][i] for i in range(k))
    d['adiag']=sum(g[i][m-1-i] for i in range(k))
    d['border']=sum(g[0])+sum(g[-1])+sum(g[i][0]+g[i][-1] for i in range(1,n-1))
    d['center']=g[n//2][m//2]
    best=0
    for r in g:
        c=0
        for v in r:
            c=c+1 if v else 0
            if c>best: best=c
    d['hrun']=best
    best=0
    for r in T:
        c=0
        for v in r:
            c=c+1 if v else 0
            if c>best: best=c
    d['vrun']=best
    d['n2x2']=sum(1 for i in range(n-1) for j in range(m-1)
                  if g[i][j] and g[i][j+1] and g[i+1][j] and g[i+1][j+1])
    seen=set(); sizes=[]
    for i in range(n):
        for j in range(m):
            if g[i][j] and (i,j) not in seen:
                st=[(i,j)]; seen.add((i,j)); sz=0
                while st:
                    a,b=st.pop(); sz+=1
                    for da,db in ((0,1),(1,0),(0,-1),(-1,0)):
                        x=a+da; y=b+db
                        if 0<=x<n and 0<=y<m and g[x][y] and (x,y) not in seen:
                            seen.add((x,y)); st.append((x,y))
                sizes.append(sz)
    d['comps']=len(sizes); d['maxcomp']=max(sizes) if sizes else 0
    d['nisol']=sizes.count(1)
    d['cnt%2']=cnt%2
    d['rowsetsize']=len(set(rc)); d['colsetsize']=len(set(cc))
    return d

# ---------------------------------------------------------------- weights
W_DEFAULT = 1.0
WEIGHTS = {"borsel": {"asc": 2, "cnt1": 3, "cnt2": 3, "cnt3": 3, "cnt4": 3, "cnt5": 3, "cnt6": 3, "consecval": 1.2, "desc": 2, "first": 0.0, "fl": 1.2, "last": 0.0, "len": 0.0, "max": 2.5, "min": 2.5, "mode": 2.5, "nadjcons": 1.2, "nadjeq": 2.5, "ndist": 2.5, "neven": 1.0, "nodd": 1.0, "npairs": 0.5, "pal": 2, "range": 2.5, "sum": 0.3, "sum%2": 0.0, "sum%3": 0.0, "sum%4": 0.0, "sum%5": 0.0, "sumprime": 0.0}, "tresk": {"biBB": 0.4, "biBG": 0.4, "biBR": 0.4, "biGB": 0.4, "biGG": 0.4, "biGR": 0.4, "biRB": 0.4, "biRG": 0.4, "biRR": 0.4, "cntB": 3, "cntB%2": 0.0, "cntG": 3, "cntG%2": 0.0, "cntR": 3, "cntR%2": 0.0, "dGB": 0.5, "dRB": 0.5, "dRG": 0.5, "first": 1.0, "fl": 1.2, "last": 1.0, "len": 0.0, "maxrun": 2.5, "ndist": 2.0, "noadj": 2.0, "nruns": 1.5, "pal": 2.0, "runB": 2.5, "runG": 2.5, "runR": 2.5}, "tavrik": {"alphapair": 0.4, "cvpal": 1.2, "first": 0.4, "fl": 2.5, "fv": 1.5, "last": 1.5, "len": 0.0, "lv": 1.5, "maxcons": 1.8, "maxlet": 3.0, "maxvow": 1.8, "nalphaadj": 0.4, "ncons": 1.0, "ndist": 1.5, "ndistvow": 2.0, "ndouble": 3.5, "nrep": 2.5, "nvow": 2.5, "pal": 2.5, "sorted": 2.0, "sum": 0.0, "sum%2": 0.0, "sum%3": 0.0}, "wisbek": {"ang2": 0.6, "ang_mult180": 1.0, "ang_mult60": 1.0, "decr": 3.0, "dsum": 1.8, "dsum%2": 0.3, "dsum%3": 0.4, "dsum%4": 0.0, "dsum%5": 0.3, "dsum%6": 0.0, "dsum_lt10": 3.0, "h": 0.5, "h%2": 0.5, "h%3": 0.8, "h%4": 0.4, "h%5": 0.4, "h%6": 0.5, "handdist": 1.2, "hdig_in_m": 2.5, "hm": 0.3, "hm%2": 2.0, "hm%3": 0.3, "hm%4": 0.0, "hm%5": 0.0, "hm%6": 0.0, "hpar_mpar": 2.0, "hprime": 1.0, "incr": 3.5, "m": 0.4, "m%10": 1.2, "m%11": 0.8, "m%12": 0.6, "m%15": 1.2, "m%2": 0.4, "m%3": 1.5, "m%4": 0.5, "m%5": 1.8, "m%6": 0.6, "m%7": 0.8, "m%8": 0.5, "m%9": 1.5, "m5h": 2.5, "m5h10": 2.5, "m5h5": 1.2, "mdivh": 2.0, "mgt": 0.8, "mh": 0.3, "mk_h_par": 1.5, "mon5": 2.0, "mprime": 1.5, "msum": 1.2, "msum_eq_h": 2.5, "mt": 0.8, "mt_eq_h": 1.8, "mt_eq_mu": 2.0, "mu": 0.8, "mu_eq_h": 1.8, "ndig": 0.0, "ndist": 1.5, "nodd": 1.2, "pal": 3.0, "rep": 3.5, "tot": 0.0, "tot%2": 0.0, "tot%3": 0.3, "tot%4": 0.0, "tot%5": 0.4, "tot%6": 0.0, "totprime": 0.6}, "dornic": {"ace": 1.5, "alldist": 1.0, "c3": 2.0, "gapmax": 1.5, "king": 1.5, "maxr": 2.0, "maxrankcnt": 2.0, "maxsuit": 2.5, "minr": 2.0, "n": 0.0, "nblack": 2.0, "nconsec": 1.5, "ndistrank": 1.2, "neven": 1.5, "nface": 2.0, "nlow": 1.5, "nodd": 1.5, "npairs": 0.8, "nred": 2.0, "nsuits": 2.0, "sC": 1.8, "sD": 1.8, "sH": 1.8, "sS": 1.8, "span": 2.5, "suitcons": 2.0, "sum": 0.0, "sum%2": 0.3, "sum%3": 0.0, "sum%4": 0.0, "sum%5": 0.0, "sum%7": 0.0}, "ospren": {"adiag": 1.8, "anti_s": 3.5, "border": 1.5, "bot": 0.0, "center": 1.5, "cnt": 2.5, "cnt%2": 0.3, "colsetsize": 1.5, "comps": 2.5, "corners": 2.5, "diag": 1.8, "hrun": 1.2, "left": 0.0, "lr": 3.5, "maxcol": 1.5, "maxcomp": 2.0, "maxrow": 1.5, "mincol": 2.5, "minrow": 2.5, "n2x2": 1.8, "ndistcol": 1.8, "ndistrow": 1.8, "nemptycol": 3.0, "nemptyrow": 3.0, "nfullcol": 3.0, "nfullrow": 3.0, "nisol": 2.0, "r180": 3.5, "right": 0.0, "rowsetsize": 1.5, "top": 0.0, "tr": 3.5, "ud": 3.5, "vrun": 1.2}}
M_EQ, M_GE, M_LE, M_SIM = 1.0, 0.5, 1.0, 0.1

FEAT = {'borsel':f_borsel,'tresk':f_tresk,'tavrik':f_tavrik,
        'wisbek':f_wisbek,'dornic':f_dornic,'ospren':f_ospren}


def choose(name, P, C):
    wts = WEIGHTS.get(name, {})
    nc = len(C)
    votes = [0.0]*nc
    sim = [0.0]*nc
    keys = set(P[0])
    for p in P[1:]:
        keys &= set(p)
    for k in keys:
        w = wts.get(k, 1.0)
        if w <= 0.0:
            continue
        lo = hi = P[0][k]
        for p in P[1:]:
            v = p[k]
            if v < lo: lo = v
            elif v > hi: hi = v
        cv = [c.get(k, 0) for c in C]
        mn = min(cv); mx = max(cv)
        if lo == hi:
            sel = -1; cn = 0
            for i in range(nc):
                if cv[i] == lo:
                    sel = i; cn += 1; sim[i] += w
            if cn == 1:
                votes[sel] += w*M_EQ
        else:
            for i in range(nc):
                if lo <= cv[i] <= hi: sim[i] += w*0.6
        if lo > mn:
            sel = -1; cn = 0
            for i in range(nc):
                if cv[i] >= lo:
                    sel = i; cn += 1
            if cn == 1: votes[sel] += w*M_GE
        if hi < mx:
            sel = -1; cn = 0
            for i in range(nc):
                if cv[i] <= hi:
                    sel = i; cn += 1
            if cn == 1: votes[sel] += w*M_LE
    best = 0; bv = votes[0] + M_SIM*sim[0]
    for i in range(1, nc):
        v = votes[i] + M_SIM*sim[i]
        if v > bv: bv = v; best = i
    return best


def blocks(clue):
    return [b for b in clue.split('\n\n') if b.strip()]


def solve(name, clue, memory):
    if name == 'norvel':
        try:
            return solve_norvel(clue)
        except Exception:
            return clue
    cands = None
    try:
        bl = blocks(clue)
        if name == 'ospren':
            pos = [bl[0].split('\n'), bl[1].split('\n')]
            cands = []
            for b in bl[2:]:
                L = b.split('\n')
                cands.append((L[0].strip(), L[1:]))
            if not cands:
                return None
            P = [f_ospren(p) for p in pos]
            C = [f_ospren(g) for _, g in cands]
            return cands[choose(name, P, C)][0]
        pos = bl[0].split('\n')
        cands = []
        for b in bl[1:]:
            cands.extend(b.split('\n'))
        if not cands:
            return None
        F = FEAT.get(name)
        if F is None:
            return cands[0]
        P = [F(p) for p in pos]
        C = [F(c) for c in cands]
        return cands[choose(name, P, C)]
    except Exception:
        try:
            if cands:
                c0 = cands[0]
                return c0[0] if isinstance(c0, tuple) else c0
        except Exception:
            pass
        return None


def on_round_start(memory):
    memory['rounds_played'] = memory.get('rounds_played', 0) + 1


def on_round_end(items, memory):
    pass
