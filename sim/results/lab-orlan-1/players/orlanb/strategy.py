D4=((-1,0),(1,0),(0,-1),(0,1))
D8=((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))

FKEYS=("dist","vert","blocked",
 "oo1","oo2","oo3","ooc1","ooc2","ooc3",
 "ox1","ox2","ox3","oxc1","oxc2",
 "oh1","oh2","oh3",
 "sumoo","sumox","sumoh","minox","minoo","minoh",
 "t4x","t4o","t4h","t4e","t8x","t8o","t8h","t8e",
 "s4x","s4o","s4h","s4e","s8x","s8o","s8h",
 "coll3","maxrow","maxcol","xcov","xcov8","nrow","ncol")

def ctx(grid):
    R=len(grid); C=len(grid[0])
    os_=[];xs=[];hs=[]
    for r in range(R):
        row=grid[r]
        for c in range(C):
            v=row[c]
            if v=='o': os_.append((r,c))
            elif v=='x': xs.append((r,c))
            elif v=='#': hs.append((r,c))
    return (grid,R,C,os_,xs,hs)

def nbc(grid,R,C,r,c,dirs,skip=None,add=None):
    x=o=h=e=0
    for dr,dc in dirs:
        nr=r+dr; nc=c+dc
        if 0<=nr<R and 0<=nc<C:
            if add is not None and (nr,nc)==add: v='o'
            elif skip is not None and (nr,nc)==skip: v='.'
            else: v=grid[nr][nc]
            if v=='.': e+=1
            elif v=='o': o+=1
            elif v=='x': x+=1
            else: h+=1
    return x,o,h,e

def fvec(CT,m):
    grid,R,C,os_,xs,hs=CT
    r,c,nr,nc=m
    q=(nr,nc); p=(r,c)
    others=[u for u in os_ if u!=p]
    # pair stats over o set (others + q)
    oo=[0,0,0,0]; ooc=[0,0,0,0]; sumoo=0; minoo=99
    n=len(others)
    for i in range(n):
        a=others[i]
        for j in range(i+1,n):
            b=others[j]
            d=abs(a[0]-b[0])+abs(a[1]-b[1]); cdv=max(abs(a[0]-b[0]),abs(a[1]-b[1]))
            sumoo+=d
            if d<minoo: minoo=d
            if d<4: oo[d]+=1
            if cdv<4: ooc[cdv]+=1
    for a in others:
        d=abs(a[0]-nr)+abs(a[1]-nc); cdv=max(abs(a[0]-nr),abs(a[1]-nc))
        sumoo+=d
        if d<minoo: minoo=d
        if d<4: oo[d]+=1
        if cdv<4: ooc[cdv]+=1
    ox=[0,0,0,0]; oxc=[0,0,0,0]; sumox=0; minox=99
    allo=others+[q]
    for a in allo:
        for b in xs:
            d=abs(a[0]-b[0])+abs(a[1]-b[1]); cdv=max(abs(a[0]-b[0]),abs(a[1]-b[1]))
            sumox+=d
            if d<minox: minox=d
            if d<4: ox[d]+=1
            if cdv<4: oxc[cdv]+=1
    oh=[0,0,0,0]; sumoh=0; minoh=99
    for a in allo:
        for b in hs:
            d=abs(a[0]-b[0])+abs(a[1]-b[1])
            sumoh+=d
            if d<minoh: minoh=d
            if d<4: oh[d]+=1
    t4x,t4o,t4h,t4e=nbc(grid,R,C,nr,nc,D4,skip=p)
    t8x,t8o,t8h,t8e=nbc(grid,R,C,nr,nc,D8,skip=p)
    s4x,s4o,s4h,s4e=nbc(grid,R,C,r,c,D4)
    s8x,s8o,s8h,_=nbc(grid,R,C,r,c,D8)
    S=set(allo)
    coll3=0
    for a in S:
        for dr,dc in D8:
            if (a[0]+dr,a[1]+dc) in S and (a[0]+2*dr,a[1]+2*dc) in S: coll3+=1
    rows={};cols={}
    for a in allo:
        rows[a[0]]=rows.get(a[0],0)+1; cols[a[1]]=cols.get(a[1],0)+1
    xcov=1; xcov8=1
    for b in xs:
        c4=0;c8=0
        for dr,dc in D8:
            u=(b[0]+dr,b[1]+dc)
            if u in S:
                c8+=1
                if dr==0 or dc==0: c4+=1
        if c4==0: xcov=0
        if c8==0: xcov8=0
    # blocked count along path
    step=(0,1) if nc>c else (0,-1) if nc<c else (1,0) if nr>r else (-1,0)
    blocked=0; rr=r+step[0]; cc=c+step[1]
    while (rr,cc)!=q:
        if grid[rr][cc]!='.': blocked+=1
        rr+=step[0]; cc+=step[1]
    return (abs(nr-r)+abs(nc-c), 1 if nc==c else 0, blocked,
            oo[1],oo[2],oo[3],ooc[1],ooc[2],ooc[3],
            ox[1],ox[2],ox[3],oxc[1],oxc[2],
            oh[1],oh[2],oh[3],
            sumoo,sumox,sumoh,minox,minoo,minoh,
            t4x,t4o,t4h,t4e,t8x,t8o,t8h,t8e,
            s4x,s4o,s4h,s4e,s8x,s8o,s8h,
            coll3,max(rows.values()),max(cols.values()),xcov,xcov8,len(rows),len(cols))

def linemoves(CT):
    grid,R,C,os_,xs,hs=CT
    out=[]
    for (r,c) in os_:
        row=grid[r]
        for cc in range(C):
            if cc!=c and row[cc]=='.': out.append((r,c,r,cc))
        for rr in range(R):
            if rr!=r and grid[rr][c]=='.': out.append((r,c,rr,c))
    return out

W=[-1.6259820655407968, 0.43498630606630373, -1.6437683608927254, 0.30268092382627215, -1.6682986175962222, 0.03630798051224728, 2.031632543945102, 0.8650799938363323, 0.3768108436370552, 1.2438489602861278, 4.0987772745988, 0.13848815230703654, -0.3438763521536721, -0.1580213034172961, -1.2852239528077227, -2.0518184343700456, -0.23847405133389063, 0.3385379151421814, -1.281279425960768, -0.8135624115416635, 0.5071574411910038, 1.0652001119524148, -0.4832805911999045, 1.4901515671468588, -1.6430713531848478, 0.2986644826480061, -0.978340292353119, -3.004648960420633, 0.05905200933100659, -1.2833771823340017, 1.0093654497160323, 1.3213733708050839, -0.8863606813033891, -0.021620257723271395, 1.6111381203195563, 0.580304839113108, 0.6982658396636493, 0.4480034177017558, 0.5169504698406832, 0.9273703733230281, -0.11684520362034106, 0.27948496679595264, -1.3425558734480467, 0.3970561588749249, 0.2871164570985277]
NW=len(W)
_R=tuple(range(NW))

def on_round_start(memory):
    memory.setdefault("rounds_played",0); memory["rounds_played"]+=1

def solve(name, clue, memory):
    ms=None
    try:
        g=clue.split("\n")
        CT=ctx(g)
        ms=linemoves(CT)
        L=len(ms)
        if not L: return None
        if L==1: return "%d,%d>%d,%d" % ms[0]
        V=[fvec(CT,m) for m in ms]
        s=[0.0]*NW; q=[0.0]*NW
        for v in V:
            for j in _R:
                x=v[j]; s[j]+=x; q[j]+=x*x
        wsc=[0.0]*NW
        for j in _R:
            var=q[j]/L-(s[j]/L)**2
            wsc[j]=W[j]/(var**0.5) if var>1e-12 else W[j]
        bi=0; bs=-1e18
        for i in range(L):
            v=V[i]; sc=0.0
            for j in _R: sc+=wsc[j]*v[j]
            if sc>bs: bs=sc; bi=i
        return "%d,%d>%d,%d" % ms[bi]
    except Exception:
        try:
            return "%d,%d>%d,%d" % ms[0]
        except Exception:
            return None

def on_round_end(items, memory): pass
