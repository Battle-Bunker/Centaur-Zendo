"""strategy.py — centaur solver.

Six classes are "pick the candidate that follows the hidden rule" puzzles:
positives above a blank line, four candidates below.  We score every simple
predicate that (a) holds for all positives and (b) singles out exactly one
candidate, ranking them by how surprising they are (empirical base rate).

fennick is a picture class: trees of letters; the shorter neighbour of a
one-wide gap topples into it ('\\' left, '/' right).
"""
import os, sys, json, math, collections
VOW=set('aeiou')

def _runs(s):
    r=[]
    for ch in s:
        if r and r[-1][0]==ch: r[-1][1]+=1
        else: r.append([ch,1])
    return r

def f_borsel_a(item):
    v=[int(x) for x in item.split()]
    n=len(v); f={}
    f['n']=n; f['sum']=sum(v); f['sum%2']=sum(v)%2; f['sum%3']=sum(v)%3; f['sum%4']=sum(v)%4; f['sum%5']=sum(v)%5
    f['max']=max(v); f['min']=min(v); f['range']=max(v)-min(v)
    f['first']=v[0]; f['last']=v[-1]; f['first==last']=v[0]==v[-1]; f['first<last']=v[0]<v[-1]
    f['sortedasc']=all(a<=b for a,b in zip(v,v[1:])); f['sorteddesc']=all(a>=b for a,b in zip(v,v[1:]))
    f['strictasc']=all(a<b for a,b in zip(v,v[1:])); f['strictdesc']=all(a>b for a,b in zip(v,v[1:]))
    f['palin']=v==v[::-1]
    f['distinct']=len(set(v)); f['alldistinct']=len(set(v))==n
    f['adjeq']=any(a==b for a,b in zip(v,v[1:]))
    f['nev']=sum(1 for x in v if x%2==0); f['nod']=n-f['nev']
    f['allev']=f['nev']==n; f['allod']=f['nod']==n
    f['evparity']=f['nev']%2
    f['firstmin']=v[0]==min(v); f['firstmax']=v[0]==max(v); f['lastmin']=v[-1]==min(v); f['lastmax']=v[-1]==max(v)
    f['maxmid']=v.index(max(v))==n//2 if n%2 else None
    f['allsame']=len(set(v))==1
    p=1
    for x in v: p*=x
    f['prod%2']=p%2; f['prod%3']=p%3
    f['mean*n']=sum(v)
    runs=[]
    for x in v:
        if runs and runs[-1][0]==x: runs[-1][1]+=1
        else: runs.append([x,1])
    f['maxrun']=max(l for _,l in runs)
    f['nruns']=len(runs)
    f['sumfl']=v[0]+v[-1]
    f['arith']=len(set(b-a for a,b in zip(v,v[1:])))==1 if n>2 else None
    f['nasc']=sum(1 for a,b in zip(v,v[1:]) if a<b)
    f['ndesc']=sum(1 for a,b in zip(v,v[1:]) if a>b)
    f['allparitysame']=len(set(x%2 for x in v))==1
    f['altparity']=all((a%2)!=(b%2) for a,b in zip(v,v[1:]))
    for k in range(1,7):
        f['has%d'%k]= k in v
        f['cnt%d'%k]= v.count(k)
    for k in range(1,7):
        f['allle%d'%k]=max(v)<=k
        f['allge%d'%k]=min(v)>=k
    f['sumeven']=sum(v)%2==0
    return f

def f_borsel_b(item):
    import itertools as _it
    v=[int(x) for x in item.split()]; n=len(v); f={}
    s=sum(v); f['sum']=s
    for k in range(2,8): f['sum%%%d'%k]=s%k
    f['n']=n; f['max']=max(v); f['min']=min(v); f['range']=max(v)-min(v)
    f['first']=v[0]; f['last']=v[-1]; f['fl_eq']=v[0]==v[-1]; f['fl_sum']=v[0]+v[-1]
    f['nd']=len(set(v)); f['alldist']=len(set(v))==n
    f['nondec']=all(a<=b for a,b in zip(v,v[1:])); f['noninc']=all(a>=b for a,b in zip(v,v[1:]))
    f['inc']=all(a<b for a,b in zip(v,v[1:])); f['dec']=all(a>b for a,b in zip(v,v[1:]))
    f['palin']=v==v[::-1]
    f['adjeq']=sum(1 for a,b in zip(v,v[1:]) if a==b)
    f['hasadjeq']=f['adjeq']>0
    f['maxadjdiff']=max(abs(a-b) for a,b in zip(v,v[1:]))
    f['minadjdiff']=min(abs(a-b) for a,b in zip(v,v[1:]))
    f['sumadjdiff']=sum(abs(a-b) for a,b in zip(v,v[1:]))
    f['nev']=sum(1 for x in v if x%2==0); f['nod']=n-f['nev']
    f['allev']=f['nev']==n; f['allod']=f['nod']==n; f['nev%2']=f['nev']%2
    f['paritypat']=tuple(x%2 for x in v)
    f['altpar']=all((a%2)!=(b%2) for a,b in zip(v,v[1:]))
    f['samepar']=len(set(x%2 for x in v))==1
    for k in range(1,7):
        f['has%d'%k]=k in v; f['cnt%d'%k]=v.count(k)
        f['allle%d'%k]=max(v)<=k; f['allge%d'%k]=min(v)>=k
    f['ngt3']=sum(1 for x in v if x>3); f['nlt4']=n-f['ngt3']
    f['nge5']=sum(1 for x in v if x>=5); f['nle2']=sum(1 for x in v if x<=2)
    runs=[]
    for x in v:
        if runs and runs[-1][0]==x: runs[-1][1]+=1
        else: runs.append([x,1])
    f['nruns']=len(runs); f['maxrun']=max(l for _,l in runs)
    f['mode_cnt']=max(v.count(x) for x in set(v))
    f['posmax']=v.index(max(v)); f['posmin']=v.index(min(v))
    f['maxfirst']=v[0]==max(v); f['maxlast']=v[-1]==max(v)
    f['minfirst']=v[0]==min(v); f['minlast']=v[-1]==min(v)
    f['nasc']=sum(1 for a,b in zip(v,v[1:]) if a<b); f['ndes']=sum(1 for a,b in zip(v,v[1:]) if a>b)
    f['ascdes']=f['nasc']==f['ndes']
    f['pair7']=any(a+b==7 for a,b in _it.combinations(v,2))
    f['adj7']=any(a+b==7 for a,b in zip(v,v[1:]))
    f['consec']=any(abs(a-b)==1 for a,b in zip(v,v[1:]))
    f['sorted_eq']=tuple(sorted(v))
    f['mult']=tuple(sorted(sorted(set(v)) and [v.count(x) for x in sorted(set(v))]))
    p=1
    for x in v: p*=x
    f['prod%2']=p%2; f['prod%3']=p%3; f['prod%5']=p%5
    f['meanint']=(s%n==0)
    f['sumsq%2']=sum(x*x for x in v)%2
    f['peaks']=sum(1 for i in range(1,n-1) if v[i]>v[i-1] and v[i]>v[i+1])
    f['valleys']=sum(1 for i in range(1,n-1) if v[i]<v[i-1] and v[i]<v[i+1])
    f['zigzag']=all((v[i]-v[i-1])*(v[i+1]-v[i])<0 for i in range(1,n-1)) if n>2 else None
    f['dbl']=any(v.count(x)==2 for x in set(v))
    f['triple']=any(v.count(x)>=3 for x in set(v))
    f['diffs']=tuple(b-a for a,b in zip(v,v[1:]))
    f['arith']=len(set(b-a for a,b in zip(v,v[1:])))==1
    f['sumfirst2']=v[0]+v[1]
    f['contains_max_twice']=v.count(max(v))>=2
    f['contains_min_twice']=v.count(min(v))>=2
    f['n_uniq_once']=sum(1 for x in set(v) if v.count(x)==1)
    for i in range(n):
        f['p%d'%i]=v[i]; f['q%d'%i]=v[n-1-i]
        f['pmax%d'%i]= v[i]==max(v); f['pmin%d'%i]= v[i]==min(v)
    for k in range(4,31):
        f['sumge%d'%k]= s>=k
        f['sumle%d'%k]= s<=k
    return f

def f_wisbek(item):
    h,m=item.split(':'); H=int(h); M=int(m); f={}
    ds=lambda s:sum(int(c) for c in s)
    f['h']=H; f['m']=M; f['m-h']=M-H; f['m+h']=M+H; f['m*h']=M*H
    f['mdig']=ds(m); f['hdig']=ds(h); f['alldig']=ds(h)+ds(m)
    f['m%h']=M%H if H else None; f['m//h']=M//H if H else None
    f['m==2h']=M==2*H; f['m==3h']=M==3*H; f['m==4h']=M==4*H; f['m==5h']=M==5*H
    f['m%5']=M%5; f['m%10']=M%10; f['m%3']=M%3; f['m%2']=M%2; f['m%15']=M%15; f['m%4']=M%4
    f['h%2']=H%2; f['h%3']=H%3
    f['mten']=M//10; f['mone']=M%10
    f['msorted']=M//10<=M%10
    f['mdigeq']=M//10==M%10
    f['mdigdiff']=abs(M//10-M%10)
    f['hsingle']=H<10
    f['digits']=tuple(sorted(set(h+m)))
    f['ndigits']=len(set(h+m))
    f['has0']='0' in h+m; f['has5']='5' in h+m
    for d in '0123456789': f['d'+d]= d in (h+m)
    f['mgt30']=M>30; f['mlt30']=M<30
    f['hle6']=H<=6
    f['revm']=int(m[::-1])
    f['m==revh']= m.lstrip('0')==h[::-1]
    f['total']=H*60+M
    f['total%5']=(H*60+M)%5
    f['mdivh']= (H!=0 and M%H==0)
    f['hdivm']= (M!=0 and M%H==0) if H else None
    f['mminh']=M-H
    f['sum_all_dig%2']=(ds(h)+ds(m))%2
    f['mdig%2']=ds(m)%2
    return f

def f_tavrik(item):
    w=item.strip(); f={}
    n=len(w); f['n']=n; f['n%2']=n%2
    f['first']=w[0]; f['last']=w[-1]; f['fl']=w[0]==w[-1]
    f['sv']=w[0] in VOW; f['ev']=w[-1] in VOW
    nv=sum(1 for c in w if c in VOW); f['nv']=nv; f['nc']=n-nv; f['nv%2']=nv%2
    f['dbl']=any(a==b for a,b in zip(w,w[1:]))
    f['rep']=len(set(w))<n
    f['nd']=len(set(w))
    f['asc']=all(a<=b for a,b in zip(w,w[1:]))
    f['desc']=all(a>=b for a,b in zip(w,w[1:]))
    f['rare']=any(c in 'jqxz' for c in w)
    f['palin']=w==w[::-1]
    f['dblvow']=any(a==b and a in VOW for a,b in zip(w,w[1:]))
    f['dblcon']=any(a==b and a not in VOW for a,b in zip(w,w[1:]))
    f['adjalpha']=any(ord(b)-ord(a)==1 for a,b in zip(w,w[1:]))
    f['y']='y' in w
    f['nvowruns']=sum(1 for i,c in enumerate(w) if c in VOW and (i==0 or w[i-1] not in VOW))
    f['maxrun']=max(l for _,l in _runs(w))
    f['ends_ing']=w.endswith('ing'); f['ends_ed']=w.endswith('ed'); f['ends_s']=w.endswith('s')
    f['firstalpha']=ord(w[0])-96
    f['sumalpha']=sum(ord(c)-96 for c in w)
    f['vowset']=tuple(sorted(set(c for c in w if c in VOW)))
    f['onevowtype']=len(f['vowset'])==1
    f['firstlt_last']=w[0]<w[-1]
    for c in 'abcdefghijklmnopqrstuvwxyz':
        f['has_'+c]= c in w
    return f

def f_tresk(item):
    s=item.strip(); f={}
    n=len(s); f['n']=n; f['n%2']=n%2
    R=s.count('R'); G=s.count('G'); B=s.count('B')
    f['R']=R; f['G']=G; f['B']=B
    f['R%2']=R%2; f['G%2']=G%2; f['B%2']=B%2
    f['R==G']=R==G; f['R==B']=R==B; f['G==B']=G==B
    f['maj']=max(((R,'R'),(G,'G'),(B,'B')))[1]
    f['first']=s[0]; f['last']=s[-1]; f['fl']=s[0]==s[-1]
    rr=_runs(s); f['nruns']=len(rr); f['nruns%2']=len(rr)%2
    mr=max(l for _,l in rr); f['maxrun']=mr
    for k in range(2,7): f['run>=%d'%k]= mr>=k
    f['palin']=s==s[::-1]
    f['allthree']= R>0 and G>0 and B>0
    f['nzero']=sum(1 for x in (R,G,B) if x==0)
    f['maxrunchar']=max(rr,key=lambda x:x[1])[0]
    f['nchanges']=len(rr)-1
    f['setcolors']=tuple(sorted(set(s)))
    f['Rmost']= R>G and R>B; f['Gmost']= G>R and G>B; f['Bmost']= B>R and B>G
    f['n%3']=n%3
    f['runlens']=tuple(sorted(l for _,l in rr))
    f['nrunsR']=sum(1 for c,_ in rr if c=='R')
    f['nrunsG']=sum(1 for c,_ in rr if c=='G')
    f['nrunsB']=sum(1 for c,_ in rr if c=='B')
    f['hasRR']='RR' in s; f['hasGG']='GG' in s; f['hasBB']='BB' in s
    f['R-G']=R-G; f['R-B']=R-B; f['G-B']=G-B
    return f

RANKV={'A':1,'J':11,'Q':12,'K':13}
def _card(c):
    r=c[:-1]; s=c[-1]
    return (RANKV.get(r, int(r) if r.isdigit() else 0), s)

def f_dornic(item):
    cards=[_card(x) for x in item.split()]
    ranks=sorted(r for r,_ in cards); suits=[s for _,s in cards]
    f={}; n=len(cards)
    f['n']=n; f['n%2']=n%2
    f['sum']=sum(ranks); f['sum%2']=sum(ranks)%2; f['sum%3']=sum(ranks)%3; f['sum%5']=sum(ranks)%5
    f['max']=max(ranks); f['min']=min(ranks); f['range']=max(ranks)-min(ranks)
    f['nd_rank']=len(set(ranks)); f['nd_suit']=len(set(suits))
    f['pair']=len(set(ranks))<n
    for s in 'CDHS':
        f['cnt'+s]=suits.count(s); f['has'+s]= s in suits
    red=sum(1 for s in suits if s in 'DH'); f['red']=red; f['black']=n-red
    f['red%2']=red%2; f['black%2']=(n-red)%2
    f['allred']=red==n; f['allblack']=red==0
    f['nface']=sum(1 for r in ranks if r>=11); f['nace']=ranks.count(1)
    f['neven']=sum(1 for r in ranks if r%2==0); f['nodd']=n-f['neven']
    f['neven%2']=f['neven']%2
    cons=sum(1 for a,b in zip(ranks,ranks[1:]) if b-a==1)
    f['ncons']=cons; f['hascons']=cons>0
    best=1;cur=1
    for a,b in zip(ranks,ranks[1:]):
        if b-a==1: cur+=1; best=max(best,cur)
        elif b!=a: cur=1
    f['longestrun']=best
    for r in range(1,14):
        f['hasr%d'%r]= r in ranks
    f['maxsuitcnt']=max(suits.count(s) for s in 'CDHS')
    f['gaps']=tuple(sorted(b-a for a,b in zip(ranks,ranks[1:])))
    f['allsamesuit']=len(set(suits))==1
    f['sumranks%4']=sum(ranks)%4
    f['high_suit']=[s for r,s in cards if r==max(ranks)][0]
    f['low_suit']=[s for r,s in cards if r==min(ranks)][0]
    f['nlow']=sum(1 for r in ranks if r<=6)
    f['nhigh']=sum(1 for r in ranks if r>=9)
    f['spread_even']=len(set(r%2 for r in ranks))==1
    return f

def _sym(g):
    return g
def f_ospren(item):
    rows=[r for r in item.split('\n') if r.strip()]
    n=len(rows); m=len(rows[0])
    cells=set((r,c) for r in range(n) for c in range(m) if rows[r][c]=='#')
    f={}
    k=len(cells); f['k']=k; f['k%2']=k%2; f['k%3']=k%3
    f['hmir']=all((n-1-r,c) in cells for r,c in cells)
    f['vmir']=all((r,m-1-c) in cells for r,c in cells)
    f['rot180']=all((n-1-r,m-1-c) in cells for r,c in cells)
    f['tr']=all((c,r) in cells for r,c in cells)
    f['atr']=all((m-1-c,n-1-r) in cells for r,c in cells)
    f['rot90']=all((c,n-1-r) in cells for r,c in cells)
    rowc=[sum(1 for c in range(m) if (r,c) in cells) for r in range(n)]
    colc=[sum(1 for r in range(n) if (r,c) in cells) for c in range(m)]
    f['nrows']=sum(1 for x in rowc if x); f['ncols']=sum(1 for x in colc if x)
    f['nfullrow']=sum(1 for x in rowc if x==m); f['nfullcol']=sum(1 for x in colc if x==n)
    f['hasfullrow']=f['nfullrow']>0; f['hasfullcol']=f['nfullcol']>0
    f['nemptyrow']=n-f['nrows']; f['nemptycol']=m-f['ncols']
    f['center']=(n//2,m//2) in cells
    f['ncorner']=sum(1 for p in [(0,0),(0,m-1),(n-1,0),(n-1,m-1)] if p in cells)
    f['border']=sum(1 for r,c in cells if r in (0,n-1) or c in (0,m-1))
    f['rowc_sorted']=tuple(sorted(rowc)); f['colc_sorted']=tuple(sorted(colc))
    # components
    seen=set(); comps=0; sizes=[]
    for p in cells:
        if p in seen: continue
        comps+=1; st=[p]; seen.add(p); sz=0
        while st:
            r,c=st.pop(); sz+=1
            for q in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
                if q in cells and q not in seen: seen.add(q); st.append(q)
        sizes.append(sz)
    f['ncomp']=comps; f['maxcomp']=max(sizes) if sizes else 0
    f['connected']=comps==1
    f['isolated']=sum(1 for r,c in cells if not any(q in cells for q in ((r+1,c),(r-1,c),(r,c+1),(r,c-1))))
    f['noadj']=f['isolated']==k
    f['nsq']=sum(1 for r in range(n-1) for c in range(m-1) if all(q in cells for q in ((r,c),(r,c+1),(r+1,c),(r+1,c+1))))
    f['diagsym']=f['tr']
    f['allsym']=f['hmir'] and f['vmir']
    f['rowc']=tuple(rowc); f['colc']=tuple(colc)
    f['maxrowc']=max(rowc); f['maxcolc']=max(colc)
    f['nrowsame']=len(set(rowc)); f['ncolsame']=len(set(colc))
    f['top']=sum(1 for r,c in cells if r<n//2); f['bot']=sum(1 for r,c in cells if r>n//2)
    f['topbot']=f['top']==f['bot']
    f['left']=sum(1 for r,c in cells if c<m//2); f['right']=sum(1 for r,c in cells if c>m//2)
    f['leftright']=f['left']==f['right']
    f['maindiag']=sum(1 for r,c in cells if r==c)
    f['antidiag']=sum(1 for r,c in cells if r+c==n-1)
    return f

FEAT={'borsel':f_borsel_a,'borsel_b':f_borsel_b,'wisbek':f_wisbek,'tavrik':f_tavrik,'tresk':f_tresk,'dornic':f_dornic,'ospren':f_ospren}


def parse(name, clue):
    if name=='ospren':
        blocks=clue.split('\n\n')
        pos=[]; cands=[]; labels=[]
        for b in blocks:
            lines=[l for l in b.split('\n') if l.strip()]
            if not lines: continue
            if lines[0].strip().isdigit():
                labels.append(lines[0].strip()); cands.append('\n'.join(lines[1:]))
            else:
                pos.append('\n'.join(lines))
        return pos,cands,labels
    blocks=[b for b in clue.split('\n\n') if b.strip()]
    pos=[l for l in blocks[0].split('\n') if l.strip()]
    cands=[l for l in blocks[1].split('\n') if l.strip()]
    return pos,cands,cands

STATS={}
WEIGHTS={}

def _banned(name,key,v):
    if name=='tavrik' and key.startswith('has_') and v is False: return True
    return False

def build_stats(clues_by_name):
    st={}
    work=[]
    for name, clues in clues_by_name.items():
        if name not in FEAT: continue
        work.append((name,name,clues))
        if name=='borsel': work.append(('borsel_b','borsel',clues))
    for name, pname, clues in work:
        fn=FEAT[name]; cnt=collections.Counter(); tot=0
        for clue in clues:
            try: pos,cands,_=parse(pname,clue)
            except Exception: continue
            for it in pos+cands:
                try: d=fn(it)
                except Exception: continue
                tot+=1
                for k,v in d.items():
                    if v is None: continue
                    try: cnt[(k,v)]+=1
                    except TypeError: pass
        st[name]=(cnt,tot)
    return st

def choose(name, clue, fkey=None, useW=False):
    fn=FEAT[fkey or name]
    pos,cands,labels=parse(name,clue)
    pf=[fn(p) for p in pos]; cf=[fn(c) for c in cands]
    cnt,tot=STATS.get(fkey or name,(collections.Counter(),1))
    k=len(pf)
    best=[-1e18]*len(cands); total=[0.0]*len(cands)
    for key in pf[0]:
        v=pf[0].get(key)
        if v is None: continue
        try: hash(v)
        except TypeError: continue
        if _banned(name,key,v): continue
        bad=False
        for d in pf[1:]:
            if d.get(key)!=v: bad=True; break
        if bad: continue
        hit=-1; nh=0
        for i,d in enumerate(cf):
            if d.get(key)==v:
                nh+=1; hit=i
                if nh>1: break
        if nh!=1: continue
        p=(cnt.get((key,v),0)+0.5)/(tot+1.0)
        if p<1e-4: p=1e-4
        if p>0.999: p=0.999
        s=-((k+1)*math.log(p)+3*math.log(1.0-p))
        if useW:
            s*= WEIGHTS.get(fkey or name,{}).get(key,0.5)*2.0
        total[hit]+=s
        if s>best[hit]: best[hit]=s
    win=max(range(len(cands)), key=lambda i:(best[i], total[i]))
    return cands[win], labels[win]

# ---------------- fennick ----------------

def solve_fennick(clue):
    lines=clue.split('\n')
    si=-1
    for i,l in enumerate(lines):
        if l and set(l)=={'='}: si=i; break
    if si<0: return None
    grid=lines[:si]
    W=max(len(r) for r in grid)
    g=[list(r.ljust(W)) for r in grid]
    H=len(g)
    h=[0]*W
    for c in range(W):
        n=0
        for r in range(H):
            if g[r][c].isalpha(): n+=1
        h[c]=n
    falls=[]
    for gap in range(1,W-1):
        if h[gap]==0 and h[gap-1]>0 and h[gap+1]>0:
            if h[gap-1]<h[gap+1]:
                c=gap-1
                if c-1>=0 and h[c-1]>0: falls.append((c,1))
            elif h[gap+1]<h[gap-1]:
                c=gap+1
                if c+1<W and h[c+1]>0: falls.append((c,-1))
    for c,d in falls:
        for r in range(H-1):
            ch=g[r][c]
            if ch==' ': continue
            g[r][c]=' '
            if ch=='_': g[r][c+d]='\\' if d==-1 else '/'
            else: g[r][c+d]=ch
    out=[''.join(row).rstrip() for row in g]
    return '\n'.join(out+lines[si:])

# ---------------- client hooks ----------------

def on_round_start(memory):
    global STATS
    memory.setdefault('rounds_played',0)
    memory['rounds_played']+=1
    data={}
    try:
        base=os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base,'clues_round1.json')) as fh:
            data=json.load(fh)
    except Exception:
        data={}
    extra=memory.get('seen_clues') or {}
    for k,v in extra.items():
        data.setdefault(k,[])
        data[k]=data[k]+list(v)
    try:
        STATS=build_stats(data)
    except Exception:
        STATS={}
    global WEIGHTS
    try:
        with open(os.path.join(base,'weights.json')) as fh:
            WEIGHTS=json.load(fh)
    except Exception:
        WEIGHTS={}
    memory['cache']={}

def solve(name, clue, memory):
    try:
        cache=memory.get('cache')
        if cache is not None:
            hit=cache.get(clue)
            if hit is not None: return hit
        if name=='fennick':
            ans=solve_fennick(clue)
        elif name in FEAT:
            text,label=choose(name,clue,None,False)
            if name=='ospren':
                ans = label
            else:
                ans = text
        else:
            ans=None
        if cache is not None and ans is not None:
            cache[clue]=ans
        return ans
    except Exception:
        return None

def on_round_end(items, memory):
    seen=memory.setdefault('seen_clues',{})
    for it in items:
        n=it.get('name'); c=it.get('clue')
        if not n or not c: continue
        b=seen.setdefault(n,[])
        if len(b)<400: b.append(c)
