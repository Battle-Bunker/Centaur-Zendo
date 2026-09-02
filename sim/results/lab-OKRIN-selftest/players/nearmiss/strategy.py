import random
DIRS = ((0,1,-1),(0,-1,1),(1,0,1),(-1,0,-1))
def klass(cells,p,k):
    req=None
    for a,b,d in DIRS:
        u=cells.get((p[0]+a,p[1]+b))
        if u is not None:
            w=(u+d)%k
            if req is None: req=w
            elif req!=w: return None
    return req
def grow(cells,need,k,r,budget):
    if sum(need)==0: return True
    budget[0]-=1
    if budget[0]<0: return False
    cand=[];seen=set()
    for (i,j) in list(cells):
        for a,b,_ in DIRS:
            p=(i+a,j+b)
            if p in cells or p in seen or p[0]<0 or p[1]<0: continue
            seen.add(p)
            w=klass(cells,p,k)
            if w is not None and need[w]>0: cand.append((need[w]+r.random(),p,w))
    cand.sort(reverse=True)
    for _s,p,w in cand:
        cells[p]=w; need[w]-=1
        if grow(cells,need,k,r,budget): return True
        del cells[p]; need[w]+=1
    return False
def build(clue, counts, vert=-1):
    k=len(clue); r=random.Random(clue)
    for _ in range(12):
        cells={(0,j):j for j in range(k)}
        need=[counts[t]-1 for t in range(k)]
        if grow(cells,need,k,r,[1500]):
            H=max(i for i,j in cells)+1; W=max(j for i,j in cells)+1
            return "\n".join("".join(clue[cells[(i,j)]] if (i,j) in cells else "." for j in range(W)) for i in range(H))
    return ""
def solve(name, clue, memory):
    try:
        k=len(clue); R=sorted(clue)
        return build(clue,[t+2 for t in range(k)])
    except Exception:
        return ""
