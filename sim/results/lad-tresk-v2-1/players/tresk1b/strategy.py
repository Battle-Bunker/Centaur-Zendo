"""strategy.py - tresk1b"""
# Predicate universes for the five "rule family" classes.
VOWELS = set('aeiou')

def build_tavrik():
    P = []
    P.append(('doubleletter', lambda w: any(w[i]==w[i+1] for i in range(len(w)-1))))
    P.append(('nodouble', lambda w: not any(w[i]==w[i+1] for i in range(len(w)-1))))
    P.append(('alldistinct', lambda w: len(set(w))==len(w)))
    P.append(('firstlast', lambda w: w[0]==w[-1]))
    P.append(('startvowel', lambda w: w[0] in VOWELS))
    P.append(('endvowel', lambda w: w[-1] in VOWELS))
    P.append(('startcons', lambda w: w[0] not in VOWELS))
    P.append(('endcons', lambda w: w[-1] not in VOWELS))
    for k in range(2,4):
        P.append(('rep%d'%k, (lambda k: lambda w: any(w.count(ch)==k for ch in set(w)))(k)))
        P.append(('repge%d'%k, (lambda k: lambda w: any(w.count(ch)>=k for ch in set(w)))(k)))
    for n in range(3,12):
        P.append(('len%d'%n, (lambda n: lambda w: len(w)==n)(n)))
    for n in range(1,7):
        P.append(('nvow%d'%n, (lambda n: lambda w: sum(1 for c in w if c in VOWELS)==n)(n)))
        P.append(('ndist%d'%n, (lambda n: lambda w: len(set(w))==n)(n)))
    for ch in 'abcdefghijklmnopqrstuvwxyz':
        P.append(('has_'+ch, (lambda ch: lambda w: ch in w)(ch)))
        P.append(('start_'+ch, (lambda ch: lambda w: w[0]==ch)(ch)))
        P.append(('end_'+ch, (lambda ch: lambda w: w[-1]==ch)(ch)))
        P.append(('no_'+ch, (lambda ch: lambda w: ch not in w)(ch)))
    P.append(('lenodd', lambda w: len(w)%2==1))
    P.append(('leneven', lambda w: len(w)%2==0))
    P.append(('vowodd', lambda w: sum(1 for c in w if c in VOWELS)%2==1))
    P.append(('voweven', lambda w: sum(1 for c in w if c in VOWELS)%2==0))
    P.append(('sorted', lambda w: list(w)==sorted(w)))
    P.append(('adjalpha', lambda w: any(abs(ord(w[i])-ord(w[i+1]))==1 for i in range(len(w)-1))))
    P.append(('firstltlast', lambda w: w[0]<w[-1]))
    P.append(('firstgtlast', lambda w: w[0]>w[-1]))
    P.append(('novowelend', lambda w: w[-1] not in VOWELS))
    P.append(('twovowelsadj', lambda w: any(w[i] in VOWELS and w[i+1] in VOWELS for i in range(len(w)-1))))
    P.append(('novowadj', lambda w: not any(w[i] in VOWELS and w[i+1] in VOWELS for i in range(len(w)-1))))
    P.append(('palin', lambda w: w==w[::-1]))
    for a in 'abcdefghijklmnopqrstuvwxyz':
        for b in 'abcdefghijklmnopqrstuvwxyz':
            pass
    P.append(('doublevowel', lambda w: any(w[i]==w[i+1] and w[i] in VOWELS for i in range(len(w)-1))))
    P.append(('doublecons', lambda w: any(w[i]==w[i+1] and w[i] not in VOWELS for i in range(len(w)-1))))
    def maxrun(w):
        m=1;c=1
        for i in range(1,len(w)):
            if w[i]==w[i-1]: c+=1; m=max(m,c)
            else: c=1
        return m
    P.append(('threecons', lambda w: any(all(x not in VOWELS for x in w[i:i+3]) for i in range(len(w)-2))))
    P.append(('nothreecons', lambda w: not any(all(x not in VOWELS for x in w[i:i+3]) for i in range(len(w)-2))))
    P.append(('altvc', lambda w: all((w[i] in VOWELS) != (w[i+1] in VOWELS) for i in range(len(w)-1))))
    P.append(('samevowel', lambda w: len(set(c for c in w if c in VOWELS))==1))
    P.append(('twovowelkinds', lambda w: len(set(c for c in w if c in VOWELS))==2))
    P.append(('firstsecond_same', lambda w: w[0]==w[1]))
    P.append(('hasy', lambda w: 'y' in w))
    P.append(('lettertwice_any', lambda w: len(set(w))<len(w)))
    P.append(('mid_double', lambda w: any(w[i]==w[i+1] for i in range(1,len(w)-2))))
    return P

def build_seq():   # borsel: list of ints
    P = []
    P.append(('allsame', lambda a: len(set(a))==1))
    P.append(('alldiff', lambda a: len(set(a))==len(a)))
    P.append(('alleven', lambda a: all(x%2==0 for x in a)))
    P.append(('allodd', lambda a: all(x%2==1 for x in a)))
    P.append(('sumeven', lambda a: sum(a)%2==0))
    P.append(('sumodd', lambda a: sum(a)%2==1))
    P.append(('nondec', lambda a: all(a[i]<=a[i+1] for i in range(len(a)-1))))
    P.append(('noninc', lambda a: all(a[i]>=a[i+1] for i in range(len(a)-1))))
    P.append(('inc', lambda a: all(a[i]<a[i+1] for i in range(len(a)-1))))
    P.append(('dec', lambda a: all(a[i]>a[i+1] for i in range(len(a)-1))))
    P.append(('palin', lambda a: a==a[::-1]))
    P.append(('firstlast', lambda a: a[0]==a[-1]))
    P.append(('adjeq', lambda a: any(a[i]==a[i+1] for i in range(len(a)-1))))
    P.append(('noadjeq', lambda a: not any(a[i]==a[i+1] for i in range(len(a)-1))))
    P.append(('adjdiff1', lambda a: any(abs(a[i]-a[i+1])==1 for i in range(len(a)-1))))
    P.append(('noadjdiff1', lambda a: not any(abs(a[i]-a[i+1])==1 for i in range(len(a)-1))))
    P.append(('hasrep', lambda a: len(set(a))<len(a)))
    for v in range(1,7):
        P.append(('has%d'%v, (lambda v: lambda a: v in a)(v)))
        P.append(('no%d'%v, (lambda v: lambda a: v not in a)(v)))
        P.append(('max%d'%v, (lambda v: lambda a: max(a)==v)(v)))
        P.append(('min%d'%v, (lambda v: lambda a: min(a)==v)(v)))
        P.append(('cnt%d_2'%v, (lambda v: lambda a: a.count(v)==2)(v)))
        P.append(('all_le%d'%v, (lambda v: lambda a: max(a)<=v)(v)))
        P.append(('all_ge%d'%v, (lambda v: lambda a: min(a)>=v)(v)))
        P.append(('first%d'%v, (lambda v: lambda a: a[0]==v)(v)))
        P.append(('last%d'%v, (lambda v: lambda a: a[-1]==v)(v)))
    for k in range(1,6):
        P.append(('ndist%d'%k, (lambda k: lambda a: len(set(a))==k)(k)))
        P.append(('rng%d'%k, (lambda k: lambda a: max(a)-min(a)==k)(k)))
        P.append(('nev%d'%k, (lambda k: lambda a: sum(1 for x in a if x%2==0)==k)(k)))
        P.append(('nod%d'%k, (lambda k: lambda a: sum(1 for x in a if x%2==1)==k)(k)))
    for s in range(2,31):
        P.append(('sum%d'%s, (lambda s: lambda a: sum(a)==s)(s)))
    for m in range(2,8):
        P.append(('summod%d'%m, (lambda m: lambda a: sum(a)%m==0)(m)))
    P.append(('rng0', lambda a: max(a)-min(a)==0))
    for i in range(1,7):
        for j in range(i+1,7):
            P.append(('both%d%d'%(i,j), (lambda i,j: lambda a: i in a and j in a)(i,j)))
    def modecnt(a):
        return max(a.count(x) for x in set(a))
    for k in range(1,7):
        P.append(('modecnt%d'%k, (lambda k: lambda a: modecnt(a)==k)(k)))
        P.append(('mode%d'%k, (lambda k: lambda a: max(set(a), key=lambda x:(a.count(x),-x))==k)(k)))
    P.append(('len%d3', lambda a: len(a)==3))
    for n in range(2,7):
        P.append(('len_%d'%n, (lambda n: lambda a: len(a)==n)(n)))
    P.append(('firsteq2nd', lambda a: a[0]==a[1]))
    P.append(('lasteq2nd', lambda a: a[-1]==a[-2]))
    P.append(('maxlast', lambda a: a[-1]==max(a)))
    P.append(('maxfirst', lambda a: a[0]==max(a)))
    P.append(('minlast', lambda a: a[-1]==min(a)))
    P.append(('minfirst', lambda a: a[0]==min(a)))
    P.append(('hasexactly2same', lambda a: any(a.count(x)==2 for x in set(a))))
    P.append(('hasexactly3same', lambda a: any(a.count(x)==3 for x in set(a))))
    return P

def build_tresk():
    L = 'RGB'
    P = []
    for ch in L:
        P.append(('start_'+ch, (lambda ch: lambda s: s[0]==ch)(ch)))
        P.append(('end_'+ch, (lambda ch: lambda s: s[-1]==ch)(ch)))
        P.append(('has_'+ch, (lambda ch: lambda s: ch in s)(ch)))
        P.append(('no_'+ch, (lambda ch: lambda s: ch not in s)(ch)))
        P.append(('dbl_'+ch, (lambda ch: lambda s: ch+ch in s)(ch)))
        P.append(('nodbl_'+ch, (lambda ch: lambda s: ch+ch not in s)(ch)))
        P.append(('tri_'+ch, (lambda ch: lambda s: ch*3 in s)(ch)))
        for k in range(0,8):
            P.append(('cnt_%s_%d'%(ch,k), (lambda ch,k: lambda s: s.count(ch)==k)(ch,k)))
        P.append(('cnteven_'+ch, (lambda ch: lambda s: s.count(ch)%2==0)(ch)))
        P.append(('cntodd_'+ch, (lambda ch: lambda s: s.count(ch)%2==1)(ch)))
        P.append(('most_'+ch, (lambda ch: lambda s: all(s.count(ch)>s.count(o) for o in L if o!=ch))(ch)))
        P.append(('fewest_'+ch, (lambda ch: lambda s: all(s.count(ch)<s.count(o) for o in L if o!=ch))(ch)))
    for a in L:
        for b in L:
            P.append(('sub_%s%s'%(a,b), (lambda a,b: lambda s: a+b in s)(a,b)))
            P.append(('nosub_%s%s'%(a,b), (lambda a,b: lambda s: a+b not in s)(a,b)))
            if a!=b:
                P.append(('more_%s%s'%(a,b), (lambda a,b: lambda s: s.count(a)>s.count(b))(a,b)))
                P.append(('eq_%s%s'%(a,b), (lambda a,b: lambda s: s.count(a)==s.count(b))(a,b)))
    P.append(('firstlast', lambda s: s[0]==s[-1]))
    P.append(('firstnelast', lambda s: s[0]!=s[-1]))
    P.append(('palin', lambda s: s==s[::-1]))
    P.append(('all3', lambda s: len(set(s))==3))
    P.append(('two', lambda s: len(set(s))==2))
    P.append(('noadjeq', lambda s: not any(s[i]==s[i+1] for i in range(len(s)-1))))
    P.append(('adjeq', lambda s: any(s[i]==s[i+1] for i in range(len(s)-1))))
    for n in range(4,14):
        P.append(('len%d'%n, (lambda n: lambda s: len(s)==n)(n)))
    P.append(('lenodd', lambda s: len(s)%2==1))
    P.append(('leneven', lambda s: len(s)%2==0))
    def runs(s):
        r=1
        for i in range(len(s)-1):
            if s[i]!=s[i+1]: r+=1
        return r
    for n in range(1,12):
        P.append(('runs%d'%n, (lambda n: lambda s: runs(s)==n)(n)))
    def maxrun(s):
        m=1; c=1
        for i in range(1,len(s)):
            if s[i]==s[i-1]: c+=1; m=max(m,c)
            else: c=1
        return m
    import re as _re
    for k in range(1,8):
        P.append(('maxrun%d'%k, (lambda k: lambda s: maxrun(s)==k)(k)))
        P.append(('maxrunge%d'%k, (lambda k: lambda s: maxrun(s)>=k)(k)))
        P.append(('maxrunle%d'%k, (lambda k: lambda s: maxrun(s)<=k)(k)))
    for ch in L:
        for j in (1,2,3):
            P.append(('nruns_%s_%d'%(ch,j), (lambda ch,j: lambda s: len(_re.findall(ch+'+', s))==j)(ch,j)))
        P.append(('startrun_'+ch, (lambda ch: lambda s: s[:2]==ch+ch)(ch)))
        P.append(('endrun_'+ch, (lambda ch: lambda s: s[-2:]==ch+ch)(ch)))
    P.append(('twodblkinds', lambda s: len(set(s[i] for i in range(len(s)-1) if s[i]==s[i+1]))>=2))
    P.append(('onedblkind', lambda s: len(set(s[i] for i in range(len(s)-1) if s[i]==s[i+1]))==1))
    for a in L:
        for b in L:
            for c in L:
                P.append(('sub3_%s%s%s'%(a,b,c), (lambda a,b,c: lambda s: a+b+c in s)(a,b,c)))
    return P

RANKS = {'A':1,'J':11,'Q':12,'K':13}
def cardval(c):
    r = c[:-1]
    return RANKS.get(r, 0) or int(r)
def suit(c): return c[-1]
RED = set('HD')

def build_dornic():
    P = []
    def vals(h): return [cardval(c) for c in h]
    def suits(h): return [suit(c) for c in h]
    P.append(('haspair', lambda h: len(set(vals(h)))<len(h)))
    P.append(('nopair', lambda h: len(set(vals(h)))==len(h)))
    P.append(('allsamesuit', lambda h: len(set(suits(h)))==1))
    P.append(('allsuits4', lambda h: len(set(suits(h)))==4))
    P.append(('allred', lambda h: all(s in RED for s in suits(h))))
    P.append(('allblack', lambda h: all(s not in RED for s in suits(h))))
    P.append(('hasface', lambda h: any(v>10 for v in vals(h))))
    P.append(('noface', lambda h: all(v<=10 for v in vals(h))))
    P.append(('hasace', lambda h: 1 in vals(h)))
    P.append(('noace', lambda h: 1 not in vals(h)))
    P.append(('alleven', lambda h: all(v%2==0 for v in vals(h))))
    P.append(('allodd', lambda h: all(v%2==1 for v in vals(h))))
    P.append(('sumeven', lambda h: sum(vals(h))%2==0))
    P.append(('sumodd', lambda h: sum(vals(h))%2==1))
    P.append(('sortedasc', lambda h: vals(h)==sorted(vals(h))))
    P.append(('trips', lambda h: any(vals(h).count(v)>=3 for v in set(vals(h)))))
    P.append(('notrips', lambda h: not any(vals(h).count(v)>=3 for v in set(vals(h)))))
    P.append(('twopair', lambda h: sum(1 for v in set(vals(h)) if vals(h).count(v)>=2)>=2))
    P.append(('samecolourpair', lambda h: any(len(set(suit(c) in RED for c in h if cardval(c)==v))==1 and [cardval(x) for x in h].count(v)>=2 for v in set(vals(h)))))
    P.append(('consec', lambda h: any((v+1) in vals(h) for v in vals(h))))
    P.append(('noconsec', lambda h: not any((v+1) in vals(h) for v in vals(h))))
    for n in range(3,9):
        P.append(('n%d'%n, (lambda n: lambda h: len(h)==n)(n)))
    for s in 'SHDC':
        P.append(('hassuit_'+s, (lambda s: lambda h: s in suits(h))(s)))
        P.append(('nosuit_'+s, (lambda s: lambda h: s not in suits(h))(s)))
        for k in range(0,6):
            P.append(('cntsuit_%s%d'%(s,k), (lambda s,k: lambda h: suits(h).count(s)==k)(s,k)))
    for k in range(0,7):
        P.append(('nred%d'%k, (lambda k: lambda h: sum(1 for s in suits(h) if s in RED)==k)(k)))
        P.append(('nblack%d'%k, (lambda k: lambda h: sum(1 for s in suits(h) if s not in RED)==k)(k)))
        P.append(('nsuits%d'%k, (lambda k: lambda h: len(set(suits(h)))==k)(k)))
        P.append(('nface%d'%k, (lambda k: lambda h: sum(1 for v in vals(h) if v>10)==k)(k)))
        P.append(('neven%d'%k, (lambda k: lambda h: sum(1 for v in vals(h) if v%2==0)==k)(k)))
        P.append(('nodd%d'%k, (lambda k: lambda h: sum(1 for v in vals(h) if v%2==1)==k)(k)))
        P.append(('ndistr%d'%k, (lambda k: lambda h: len(set(vals(h)))==k)(k)))
    for v in range(1,14):
        P.append(('hasrank%d'%v, (lambda v: lambda h: v in vals(h))(v)))
        P.append(('norank%d'%v, (lambda v: lambda h: v not in vals(h))(v)))
        P.append(('max%d'%v, (lambda v: lambda h: max(vals(h))==v)(v)))
        P.append(('min%d'%v, (lambda v: lambda h: min(vals(h))==v)(v)))
    P.append(('redeven', lambda h: sum(1 for s in suits(h) if s in RED)%2==0))
    P.append(('moreredthanblack', lambda h: sum(1 for s in suits(h) if s in RED)>len(h)/2))
    P.append(('moreblack', lambda h: sum(1 for s in suits(h) if s not in RED)>len(h)/2))
    for m in range(2,8):
        P.append(('summod%d'%m, (lambda m: lambda h: sum(vals(h))%m==0)(m)))
    P.append(('pairsamecolour', lambda h: any(len(set((suit(c) in RED) for c in h if cardval(c)==v))==1 for v in set(vals(h)) if vals(h).count(v)==2)))
    P.append(('pairdiffcolour', lambda h: any(len(set((suit(c) in RED) for c in h if cardval(c)==v))==2 for v in set(vals(h)) if vals(h).count(v)==2)))
    P.append(('allranksle10', lambda h: max(vals(h))<=10))
    P.append(('run3', lambda h: any(all((v+i) in vals(h) for i in range(3)) for v in vals(h))))
    P.append(('anytwosuitsequal', lambda h: len(set(suits(h)))<len(h)))
    P.append(('sortedbyval', lambda h: vals(h)==sorted(vals(h))))
    for k in range(0,7):
        P.append(('npairs%d'%k, (lambda k: lambda h: sum(1 for v in set(vals(h)) if vals(h).count(v)>=2)==k)(k)))
    P.append(('sumdig', lambda h: sum(vals(h))%10==0))
    P.append(('spadecount_eq_heart', lambda h: suits(h).count('S')==suits(h).count('H')))
    return P

def build_wisbek():
    P = []
    def hm(t):
        a,b = t.split(':'); return int(a), int(b)
    P.append(('meven', lambda t: hm(t)[1]%2==0))
    P.append(('modd', lambda t: hm(t)[1]%2==1))
    P.append(('heven', lambda t: hm(t)[0]%2==0))
    P.append(('hodd', lambda t: hm(t)[0]%2==1))
    P.append(('m2h', lambda t: hm(t)[1]==2*hm(t)[0]))
    P.append(('m3h', lambda t: hm(t)[1]==3*hm(t)[0]))
    P.append(('m4h', lambda t: hm(t)[1]==4*hm(t)[0]))
    P.append(('m5h', lambda t: hm(t)[1]==5*hm(t)[0]))
    P.append(('mrep', lambda t: t.split(':')[1][0]==t.split(':')[1][1]))
    P.append(('mdigdiff', lambda t: t.split(':')[1][0]!=t.split(':')[1][1]))
    P.append(('hdivm', lambda t: hm(t)[1]!=0 and hm(t)[1]%hm(t)[0]==0))
    P.append(('mgth', lambda t: hm(t)[1]>hm(t)[0]))
    P.append(('mlth', lambda t: hm(t)[1]<hm(t)[0]))
    P.append(('mlt30', lambda t: hm(t)[1]<30))
    P.append(('mge30', lambda t: hm(t)[1]>=30))
    P.append(('mprime', lambda t: hm(t)[1] in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59)))
    P.append(('hprime', lambda t: hm(t)[0] in (2,3,5,7,11)))
    P.append(('palin', lambda t: (lambda s: s==s[::-1])(t.replace(':',''))))
    for k in range(2,16):
        P.append(('mmod%d'%k, (lambda k: lambda t: hm(t)[1]%k==0)(k)))
    for k in range(2,7):
        P.append(('hmod%d'%k, (lambda k: lambda t: hm(t)[0]%k==0)(k)))
    for s in range(0,30):
        P.append(('dsum%d'%s, (lambda s: lambda t: sum(int(c) for c in t if c.isdigit())==s)(s)))
        P.append(('mdsum%d'%s, (lambda s: lambda t: sum(int(c) for c in t.split(':')[1])==s)(s)))
        P.append(('hpm%d'%s, (lambda s: lambda t: hm(t)[0]+hm(t)[1]==s)(s)))
        P.append(('mmh%d'%s, (lambda s: lambda t: hm(t)[1]-hm(t)[0]==s)(s)))
    for k in range(2,8):
        P.append(('dsummod%d'%k, (lambda k: lambda t: sum(int(c) for c in t if c.isdigit())%k==0)(k)))
        P.append(('totmod%d'%k, (lambda k: lambda t: ((hm(t)[0]%12)*60+hm(t)[1])%k==0)(k)))
    for h in range(1,13):
        P.append(('h%d'%h, (lambda h: lambda t: hm(t)[0]==h)(h)))
    for d in '0123456789':
        P.append(('hasdig'+d, (lambda d: lambda t: d in t.replace(':',''))(d)))
        P.append(('nodig'+d, (lambda d: lambda t: d not in t.replace(':',''))(d)))
    P.append(('mten0', lambda t: t.split(':')[1][0]=='0'))
    P.append(('mtenslth', lambda t: int(t.split(':')[1][0])<int(t.split(':')[1][1])))
    P.append(('mtensgth', lambda t: int(t.split(':')[1][0])>int(t.split(':')[1][1])))
    P.append(('h2dig', lambda t: len(t.split(':')[0])==2))
    P.append(('h1dig', lambda t: len(t.split(':')[0])==1))
    P.append(('alldistinctdig', lambda t: (lambda s: len(set(s))==len(s))(t.replace(':',''))))
    for k in range(-30,31):
        P.append(('m5hk%d'%k, (lambda k: lambda t: hm(t)[1]-5*hm(t)[0]==k)(k)))
    P.append(('mfive', lambda t: hm(t)[1]%5==0))
    P.append(('mnum_gt6', lambda t: hm(t)[1]%5==0 and hm(t)[1]>30))
    P.append(('mnum_lt6', lambda t: hm(t)[1]%5==0 and hm(t)[1]<30))
    for k in range(0,13):
        P.append(('mnum%d'%k, (lambda k: lambda t: hm(t)[1]%5==0 and hm(t)[1]//5==k)(k)))
    P.append(('hmsamedig', lambda t: str(hm(t)[0])[-1]==t.split(':')[1][-1]))
    P.append(('mtenseqh', lambda t: int(t.split(':')[1][0])==hm(t)[0]))
    return P

# ---- extra predicate batches -------------------------------------------------

def extra_tavrik():
    P = []
    P.append(('endsdouble', lambda w: len(w)>1 and w[-1]==w[-2]))
    P.append(('startsdouble', lambda w: len(w)>1 and w[0]==w[1]))
    P.append(('strictsorted', lambda w: all(w[i]<w[i+1] for i in range(len(w)-1))))
    P.append(('revsorted', lambda w: list(w)==sorted(w, reverse=True)))
    P.append(('secondvowel', lambda w: len(w)>1 and w[1] in VOWELS))
    P.append(('secondcons', lambda w: len(w)>1 and w[1] not in VOWELS))
    P.append(('firstisalphamin', lambda w: w[0]==min(w)))
    P.append(('lastisalphamax', lambda w: w[-1]==max(w)))
    P.append(('firstisalphamax', lambda w: w[0]==max(w)))
    P.append(('hasqxz', lambda w: any(c in w for c in 'qxzj')))
    P.append(('noqxz', lambda w: not any(c in w for c in 'qxzj')))
    P.append(('firstlastvowelsame', lambda w: (w[0] in VOWELS)==(w[-1] in VOWELS)))
    P.append(('twodoubles', lambda w: sum(1 for i in range(len(w)-1) if w[i]==w[i+1])>=2))
    P.append(('exactly1double', lambda w: sum(1 for i in range(len(w)-1) if w[i]==w[i+1])==1))
    for k in range(1,5):
        P.append(('ncons%d'%k, (lambda k: lambda w: sum(1 for c in w if c not in VOWELS)==k)(k)))
    P.append(('morevowels', lambda w: sum(1 for c in w if c in VOWELS)*2>len(w)))
    P.append(('halfvowels', lambda w: sum(1 for c in w if c in VOWELS)*2==len(w)))
    for s in ('th','ch','sh','ing','er','le','ea','oo','ee','ll','ss','tt','st','ck','ly','on','an','in','re'):
        P.append(('sub_'+s, (lambda s: lambda w: s in w)(s)))
    P.append(('firstlast_adj', lambda w: abs(ord(w[0])-ord(w[-1]))==1))
    P.append(('sameletterends', lambda w: w[0]==w[-1]))
    P.append(('vowelfirsthalf', lambda w: all(c in 'aeiou' or ord(c)<ord('n') for c in w)))
    P.append(('allfirsthalf', lambda w: all(c<='m' for c in w)))
    P.append(('allsecondhalf', lambda w: all(c>='n' for c in w)))
    P.append(('anyletter3x', lambda w: any(w.count(c)>=3 for c in set(w))))
    P.append(('twoletters2x', lambda w: sum(1 for c in set(w) if w.count(c)==2)>=2))
    P.append(('one2x', lambda w: sum(1 for c in set(w) if w.count(c)==2)==1))
    return P

def extra_seq():
    P = []
    P.append(('symmetric', lambda a: a==a[::-1]))
    P.append(('firstmax', lambda a: a[0]==max(a)))
    P.append(('lastmax', lambda a: a[-1]==max(a)))
    P.append(('firstmin', lambda a: a[0]==min(a)))
    P.append(('hasconsec', lambda a: any(x+1 in a for x in a)))
    P.append(('noconsec', lambda a: not any(x+1 in a for x in a)))
    P.append(('sumgt', lambda a: sum(a) > 3*len(a)))
    P.append(('sumlt', lambda a: sum(a) <= 3*len(a)))
    P.append(('exactly1rep', lambda a: sum(1 for x in set(a) if a.count(x)>1)==1))
    P.append(('exactly2rep', lambda a: sum(1 for x in set(a) if a.count(x)>1)==2))
    P.append(('anytwice', lambda a: any(a.count(x)==2 for x in set(a))))
    P.append(('samevalue_ends', lambda a: a[0]==a[-1]))
    P.append(('middleeq', lambda a: len(a)>=3 and a[len(a)//2]==a[len(a)//2-1]))
    P.append(('allsameparity', lambda a: len(set(x%2 for x in a))==1))
    P.append(('mixparity', lambda a: len(set(x%2 for x in a))==2))
    P.append(('evenlen', lambda a: len(a)%2==0))
    P.append(('oddlen', lambda a: len(a)%2==1))
    for k in range(0,6):
        P.append(('nrises%d'%k, (lambda k: lambda a: sum(1 for i in range(len(a)-1) if a[i]<a[i+1])==k)(k)))
        P.append(('nfalls%d'%k, (lambda k: lambda a: sum(1 for i in range(len(a)-1) if a[i]>a[i+1])==k)(k)))
        P.append(('nlevel%d'%k, (lambda k: lambda a: sum(1 for i in range(len(a)-1) if a[i]==a[i+1])==k)(k)))
    for v in range(1,7):
        P.append(('cnt%d_1'%v, (lambda v: lambda a: a.count(v)==1)(v)))
        P.append(('cnt%d_3'%v, (lambda v: lambda a: a.count(v)==3)(v)))
    P.append(('maxtwice', lambda a: a.count(max(a))>=2))
    P.append(('mintwice', lambda a: a.count(min(a))>=2))
    P.append(('sumdivlen', lambda a: sum(a)%len(a)==0))
    P.append(('anydouble', lambda a: any(2*x in a for x in a if 2*x!=x)))
    return P

def extra_tresk():
    L='RGB'
    P = []
    for i in range(0,4):
        for ch in L:
            P.append(('pos%d_%s'%(i,ch), (lambda i,ch: lambda s: len(s)>i and s[i]==ch)(i,ch)))
            P.append(('neg%d_%s'%(i,ch), (lambda i,ch: lambda s: len(s)>i and s[-1-i]==ch)(i,ch)))
    def runs(s):
        r=1
        for i in range(len(s)-1):
            if s[i]!=s[i+1]: r+=1
        return r
    for k in range(2,12):
        P.append(('runsge%d'%k, (lambda k: lambda s: runs(s)>=k)(k)))
        P.append(('runsle%d'%k, (lambda k: lambda s: runs(s)<=k)(k)))
    for ch in L:
        for m in (2,3,4):
            P.append(('cntmod_%s_%d'%(ch,m), (lambda ch,m: lambda s: s.count(ch)%m==0)(ch,m)))
        P.append(('cntge2_'+ch, (lambda ch: lambda s: s.count(ch)>=2)(ch)))
        P.append(('cntge3_'+ch, (lambda ch: lambda s: s.count(ch)>=3)(ch)))
        P.append(('half_'+ch, (lambda ch: lambda s: s.count(ch)*2==len(s))(ch)))
        P.append(('majority_'+ch, (lambda ch: lambda s: s.count(ch)*2>len(s))(ch)))
    P.append(('lenmod3', lambda s: len(s)%3==0))
    P.append(('lenmod4', lambda s: len(s)%4==0))
    for k in range(4,14):
        P.append(('lenge%d'%k, (lambda k: lambda s: len(s)>=k)(k)))
        P.append(('lenle%d'%k, (lambda k: lambda s: len(s)<=k)(k)))
    P.append(('sortedstr', lambda s: list(s)==sorted(s)))
    P.append(('firsteqsecond', lambda s: len(s)>1 and s[0]==s[1]))
    P.append(('lasteqprev', lambda s: len(s)>1 and s[-1]==s[-2]))
    P.append(('allthree', lambda s: len(set(s))==3))
    P.append(('onlyone', lambda s: len(set(s))==1))
    P.append(('countsalldiff', lambda s: len(set(s.count(c) for c in 'RGB'))==3))
    P.append(('twoequalcounts', lambda s: len(set(s.count(c) for c in 'RGB'))==2))
    return P

def extra_dornic():
    P = []
    def vals(h): return [cardval(c) for c in h]
    def suits(h): return [suit(c) for c in h]
    def hi(h): return max(range(len(h)), key=lambda i: cardval(h[i]))
    def lo(h): return min(range(len(h)), key=lambda i: cardval(h[i]))
    P.append(('hired', lambda h: suit(h[hi(h)]) in RED))
    P.append(('hiblack', lambda h: suit(h[hi(h)]) not in RED))
    P.append(('lored', lambda h: suit(h[lo(h)]) in RED))
    P.append(('loblack', lambda h: suit(h[lo(h)]) not in RED))
    P.append(('hiodd', lambda h: max(vals(h))%2==1))
    P.append(('hieven', lambda h: max(vals(h))%2==0))
    P.append(('loodd', lambda h: min(vals(h))%2==1))
    P.append(('loeven', lambda h: min(vals(h))%2==0))
    for s in 'SHDC':
        P.append(('hisuit_'+s, (lambda s: lambda h: suit(h[hi(h)])==s)(s)))
        P.append(('losuit_'+s, (lambda s: lambda h: suit(h[lo(h)])==s)(s)))
    P.append(('endssamecolour', lambda h: (suit(h[hi(h)]) in RED)==(suit(h[lo(h)]) in RED)))
    P.append(('redeqblack', lambda h: sum(1 for s in suits(h) if s in RED)*2==len(h)))
    P.append(('lenodd', lambda h: len(h)%2==1))
    P.append(('leneven', lambda h: len(h)%2==0))
    P.append(('bothcolours', lambda h: len(set(s in RED for s in suits(h)))==2))
    P.append(('missingonesuit', lambda h: len(set(suits(h)))==3))
    P.append(('threesamesuit', lambda h: any(suits(h).count(s)>=3 for s in 'SHDC')))
    P.append(('adjsamesuit', lambda h: any(suits(h)[i]==suits(h)[i+1] for i in range(len(h)-1))))
    P.append(('adjconsec', lambda h: any(vals(h)[i]+1==vals(h)[i+1] for i in range(len(h)-1))))
    P.append(('rng_all', lambda h: max(vals(h))-min(vals(h))>=10))
    for k in range(2,13):
        P.append(('rng%d'%k, (lambda k: lambda h: max(vals(h))-min(vals(h))==k)(k)))
    for k in range(10,60):
        P.append(('sumeq%d'%k, (lambda k: lambda h: sum(vals(h))==k)(k)))
    P.append(('allle7', lambda h: max(vals(h))<=7))
    P.append(('allge5', lambda h: min(vals(h))>=5))
    P.append(('pairsuited', lambda h: any(len(set(suit(c) for c in h if cardval(c)==v))==1 for v in set(vals(h)) if vals(h).count(v)>=2)))
    P.append(('samerank2colours', lambda h: any(len(set(suit(c) in RED for c in h if cardval(c)==v))==2 for v in set(vals(h)) if vals(h).count(v)>=2)))
    P.append(('nfacege2', lambda h: sum(1 for v in vals(h) if v>10)>=2))
    P.append(('facessamesuit', lambda h: len(set(suit(c) for c in h if cardval(c)>10))<=1))
    P.append(('acepresentandking', lambda h: 1 in vals(h) and 13 in vals(h)))
    for k in range(2,7):
        P.append(('lenmod%d'%k, (lambda k: lambda h: len(h)%k==0)(k)))
    P.append(('nredodd', lambda h: sum(1 for s in suits(h) if s in RED)%2==1))
    P.append(('nblackodd', lambda h: sum(1 for s in suits(h) if s not in RED)%2==1))
    P.append(('run3any', lambda h: any(all((v+i) in vals(h) for i in range(3)) for v in set(vals(h)))))
    P.append(('norun2', lambda h: not any((v+1) in vals(h) for v in set(vals(h)))))
    return P

def extra_wisbek():
    P = []
    def hm(t):
        a,b=t.split(':'); return int(a), int(b)
    P.append(('mgt30', lambda t: hm(t)[1]>30))
    P.append(('mlt15', lambda t: hm(t)[1]<15))
    P.append(('mopp', lambda t: hm(t)[1]==((hm(t)[0]+6)%12)*5))
    P.append(('mquarter', lambda t: hm(t)[1] in (0,15,30,45)))
    P.append(('mhalf', lambda t: hm(t)[1] in (0,30)))
    P.append(('digsinc', lambda t: (lambda s: all(s[i]<=s[i+1] for i in range(len(s)-1)))(t.replace(':',''))))
    P.append(('digsdec', lambda t: (lambda s: all(s[i]>=s[i+1] for i in range(len(s)-1)))(t.replace(':',''))))
    P.append(('hdiginm', lambda t: str(hm(t)[0])[-1] in t.split(':')[1]))
    P.append(('mcontainsh', lambda t: t.split(':')[0] in t.split(':')[1]))
    P.append(('sumdigprime', lambda t: sum(int(c) for c in t if c.isdigit()) in (2,3,5,7,11,13,17,19,23)))
    for k in range(0,10):
        P.append(('mones%d'%k, (lambda k: lambda t: int(t.split(':')[1][1])==k)(k)))
        P.append(('mtens%d'%k, (lambda k: lambda t: int(t.split(':')[1][0])==k)(k)))
    P.append(('monesev', lambda t: int(t.split(':')[1][1])%2==0))
    P.append(('mtensev', lambda t: int(t.split(':')[1][0])%2==0))
    P.append(('mdigsum_eq_h', lambda t: sum(int(c) for c in t.split(':')[1])==hm(t)[0]))
    P.append(('mdigprod', lambda t: (lambda a,b: int(a)*int(b))(*t.split(':')[1])==hm(t)[0]))
    P.append(('mdigdiff_h', lambda t: abs(int(t.split(':')[1][0])-int(t.split(':')[1][1]))==hm(t)[0]))
    P.append(('meqh', lambda t: hm(t)[1]==hm(t)[0]))
    P.append(('mmulth', lambda t: hm(t)[0]!=0 and hm(t)[1]%hm(t)[0]==0))
    P.append(('hmultm', lambda t: hm(t)[1]!=0 and hm(t)[0]%hm(t)[1]==0))
    P.append(('mprime2', lambda t: hm(t)[1] in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59)))
    P.append(('msquare', lambda t: hm(t)[1] in (0,1,4,9,16,25,36,49)))
    P.append(('hsquare', lambda t: hm(t)[0] in (1,4,9)))
    P.append(('bothdigsame', lambda t: len(set(t.replace(':','')))==1))
    for k in range(2,10):
        P.append(('mmodk%d'%k, (lambda k: lambda t: hm(t)[1]%k==0)(k)))
    P.append(('mgt45', lambda t: hm(t)[1]>45))
    P.append(('mbetween', lambda t: 15<=hm(t)[1]<=45))
    P.append(('handssame', lambda t: hm(t)[1]==5*(hm(t)[0]%12)))
    for k in range(1,12):
        P.append(('handsahead%d'%k, (lambda k: lambda t: hm(t)[1]==5*((hm(t)[0]+k)%12))(k)))
    return P

_orig_tavrik = build_tavrik
def build_tavrik():
    return _orig_tavrik() + extra_tavrik()
_orig_seq = build_seq
def build_seq():
    return _orig_seq() + extra_seq()
_orig_tresk = build_tresk
def build_tresk():
    return _orig_tresk() + extra_tresk()
_orig_dornic = build_dornic
def build_dornic():
    return _orig_dornic() + extra_dornic()
_orig_wisbek = build_wisbek
def build_wisbek():
    return _orig_wisbek() + extra_wisbek()



NORIG = {'tavrik': 160, 'borsel': 168, 'tresk': 182, 'dornic': 184, 'wisbek': 286}


import collections

PARSE = {
 'tavrik': lambda s: s,
 'borsel': lambda s: [int(x) for x in s.split()],
 'tresk' : lambda s: s,
 'dornic': lambda s: s.split(),
 'wisbek': lambda s: s,
}
BUILD = {
 'tavrik': build_tavrik, 'borsel': build_seq, 'tresk': build_tresk,
 'dornic': build_dornic, 'wisbek': build_wisbek,
}
PREDS = {}
FUNCS = {}
def init():
    for k, f in BUILD.items():
        PREDS[k] = f()
        FUNCS[k] = [p[1] for p in PREDS[k]]

def split_clue(clue):
    parts = clue.split('\n\n')
    ex = [l for l in parts[0].split('\n') if l.strip()]
    cand = [l for l in parts[1].split('\n') if l.strip()] if len(parts) > 1 else []
    return ex, cand

def choose(name, clue):
    ex, cand = split_clue(clue)
    if len(cand) < 2:
        return None
    p = PARSE[name]
    try:
        E = [p(x) for x in ex]
    except Exception:
        return None
    C = []
    for x in cand:
        try:
            C.append(p(x))
        except Exception:
            C.append(None)
    n = len(C)
    w = WEIGHTS[name]
    sc = [0.0] * n
    sc2 = [0.0] * n
    masks = []
    any_iso = False
    any_iso2 = False
    nor = NORIG[name]
    for pi, f in enumerate(FUNCS[name]):
        ok = True
        try:
            for e in E:
                if not f(e):
                    ok = False; break
        except Exception:
            ok = False
        if not ok:
            continue
        mask = 0
        for i, c in enumerate(C):
            if c is None: continue
            try:
                if f(c): mask |= 1 << i
            except Exception:
                pass
        if mask == 0:
            continue
        if mask & (mask - 1) == 0:
            sc[mask.bit_length() - 1] += w[pi]
            any_iso = True
        else:
            masks.append(mask)
    if any_iso:
        best = 0
        for i in range(1, n):
            if sc[i] > sc[best]: best = i
        return cand[best]
    pv = [0] * n
    L = len(masks)
    if L <= 120:
        for a in range(L):
            ma = masks[a]
            for b in range(a + 1, L):
                m = ma & masks[b]
                if m and (m & (m - 1)) == 0:
                    pv[m.bit_length() - 1] += 1
    if any(pv):
        return cand[pv.index(max(pv))]
    cnt = [0] * n
    for m in masks:
        for i in range(n):
            if m >> i & 1: cnt[i] += 1
    if any(cnt):
        return cand[cnt.index(max(cnt))]
    return cand[0]


WEIGHTS = {'tavrik': [0.35628, 0.05553, 0.05505, 0.63284, 0.60619, 0.05505, 0.05505, 0.05505, 0.05533, 0.05505, 0.10941, 0.40644, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 1.0, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.05505, 0.0803, 0.05505, 0.05505, 0.02235, 0.0803, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.05505, 0.022, 0.05505, 0.05505, 0.05505, 0.02627, 0.20656, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.10555, 0.02299, 0.05505, 0.05505, 0.05505, 0.02221, 0.05568, 0.05505, 0.05505, 0.02215, 0.05505, 0.05505, 0.05505, 0.02172, 0.05938, 0.05505, 0.05505, 0.02172, 0.0596, 0.05505, 0.14696, 0.02242, 0.05774, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.12939, 0.02417, 0.05505, 0.05505, 0.05505, 0.022, 0.20656, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.05505, 0.02194, 0.05554, 0.05505, 0.30492, 0.02284, 0.05505, 0.05505, 0.10555, 0.10548, 0.05505, 0.05505, 0.05505, 0.02172, 0.15606, 0.05505, 0.05505, 0.02172, 0.10555, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.05505, 0.02172, 0.05505, 0.05505, 0.05667, 0.05505, 0.52717, 0.05505, 0.05762, 0.05505, 0.05505, 0.05505, 0.06124, 0.05505, 0.05505, 0.05505, 0.05554, 0.05505, 0.05505, 0.05533, 0.05505, 0.05505, 0.05505, 0.05505, 0.05749, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00898, 0.13866, 0.00726, 0.44985, 0.00605, 0.00628, 0.00605, 0.30728, 0.00605, 0.00605, 0.00657, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.00605, 0.58384, 0.00626, 0.00605, 0.00605, 0.35744, 0.00605, 0.00781], 'borsel': [0.08248, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.02108, 0.01055, 0.00642, 0.00642, 0.01117, 0.05029, 0.00642, 0.00642, 0.26885, 0.0073, 0.00642, 0.05222, 0.00642, 0.00642, 0.05222, 0.00922, 0.00642, 0.00642, 0.07695, 0.00852, 0.00822, 0.00642, 0.00642, 0.00642, 0.00822, 0.00642, 0.00642, 0.07066, 0.00642, 0.70721, 0.01351, 0.00985, 0.01145, 0.00642, 0.00642, 0.00642, 0.02298, 0.00642, 1.0, 0.03309, 0.00789, 0.03333, 0.02536, 0.00642, 0.07066, 0.00684, 0.00642, 0.07066, 0.00642, 0.00642, 0.00642, 0.29146, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.08248, 0.00642, 0.00642, 0.00642, 0.30891, 0.00642, 0.00642, 0.00642, 0.02596, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.0935, 0.00642, 0.00765, 0.00642, 0.00642, 0.08248, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.01178, 0.00642, 0.00642, 0.00642, 0.00642, 0.03309, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.20273, 0.00807, 0.00822, 0.00963, 0.00642, 0.00728, 0.00684, 0.01216, 0.00818, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.09754, 0.10649, 0.0083, 0.00642, 0.13489, 0.00842, 0.00807, 0.00963, 0.01117, 0.00642, 0.0083, 0.00842, 0.01705, 0.0073, 0.00642, 0.40162, 0.07066, 0.07066, 0.00807, 0.05029, 0.04391, 0.0073, 0.08373, 0.00642, 0.00642, 0.01055, 0.02108, 0.00642, 0.08418, 0.26335, 0.00698, 0.07066, 0.00682, 0.06819, 0.00642, 0.00642, 0.00728, 0.00642, 0.00642, 0.01216, 0.00642, 0.00642, 0.00642, 0.00642, 0.00642, 0.12954, 0.00642, 0.00682, 0.00642, 0.00642, 0.00642, 0.0594, 0.00642, 0.00642, 0.00642, 0.00806, 0.00806, 0.01269, 0.29038], 'tresk': [0.05649, 0.05649, 0.05649, 0.02316, 0.07814, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.08897, 0.05649, 0.05649, 0.14102, 0.08897, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.02316, 0.05936, 0.05649, 0.05706, 0.05649, 0.05649, 0.05649, 0.05649, 0.07783, 0.05649, 0.05649, 0.05649, 0.08818, 0.05856, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.02316, 0.05856, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.12043, 0.08084, 0.05649, 0.05649, 0.12043, 0.10144, 0.05649, 0.05649, 0.07814, 0.05649, 0.05649, 0.05649, 0.05649, 0.31333, 0.05649, 0.07814, 0.05649, 0.31252, 0.12802, 0.12144, 0.05649, 0.31333, 0.05936, 0.05649, 0.05649, 0.26667, 0.05649, 0.31584, 0.05649, 0.12144, 0.05649, 0.31252, 0.05649, 0.05968, 0.05649, 0.31584, 0.05856, 0.05649, 0.05649, 0.05716, 1.0, 0.05649, 0.91461, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.14653, 0.17019, 0.05649, 0.05649, 0.67015, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05706, 0.05649, 0.07093, 0.46882, 0.05649, 0.06091, 0.06091, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05754, 0.05724, 0.05649, 0.05649, 0.05649, 0.15954, 0.05649, 0.05649, 0.05649, 0.05649, 0.05824, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05713, 0.05706, 0.05649, 0.05649, 0.05649, 0.0627, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05649, 0.05856, 0.05649, 0.05649, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00956, 0.00749, 0.00824, 0.01012, 0.07946, 0.00749, 0.00838, 0.07244, 0.00813, 0.07244, 0.00749, 0.00749, 0.00797, 0.00886, 0.00749, 0.00839, 0.03997, 0.00749, 0.00749, 0.00749, 0.09753, 0.00749, 0.57104, 0.00749, 0.00956, 0.03997, 0.00815, 0.02115, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.09202, 0.01378, 0.00789, 0.00749, 0.00749, 0.00749, 0.00749, 0.03918, 0.00749, 0.06624, 0.00749, 0.00749, 0.00749, 0.00749, 0.07143, 0.00802, 0.07143, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00749, 0.00974, 0.00749, 0.00749, 0.00749, 0.01031, 0.02209], 'dornic': [0.35419, 0.33136, 0.31548, 0.31548, 0.31548, 0.31548, 0.3671, 0.31548, 0.31548, 0.32742, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.11548, 0.31548, 0.31548, 0.32839, 0.31548, 0.31548, 0.31548, 0.32017, 0.27032, 0.47032, 0.31548, 0.47032, 0.3929, 0.31548, 0.31548, 0.31548, 0.11548, 0.31548, 0.31548, 0.31548, 0.58492, 0.31548, 0.31548, 0.31548, 0.12534, 0.32534, 0.31548, 0.78, 0.47032, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.33136, 0.31548, 0.31548, 0.31548, 0.78, 0.31548, 0.31548, 0.31548, 0.31548, 0.59077, 0.32943, 0.31548, 0.31548, 0.31548, 0.32017, 0.31548, 0.31548, 0.32943, 0.31548, 0.47032, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.73869, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.12742, 0.31548, 0.31548, 0.3929, 0.13498, 0.31548, 0.3929, 0.3929, 0.34866, 0.31548, 0.3929, 0.4214, 0.11548, 0.31548, 0.4214, 0.33147, 0.18303, 0.31548, 0.57335, 0.3259, 0.16131, 0.31548, 0.31548, 0.31548, 0.378, 0.31548, 0.31548, 0.31548, 0.27032, 0.47032, 0.31548, 0.87132, 0.41226, 1.0, 0.31548, 0.33512, 0.24585, 0.34856, 0.31548, 0.31548, 0.11548, 0.31548, 0.31548, 0.43037, 0.11548, 0.43037, 0.31548, 0.31548, 0.11548, 0.31548, 0.31548, 0.61226, 0.32534, 0.47032, 0.31548, 0.31548, 0.78, 0.78, 0.31548, 0.47032, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.33136, 0.35419, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.31548, 0.3343, 0.45744, 0.06048, 0.29294, 0.06048, 0.25677, 0.22377, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.1379, 0.06048, 0.06048, 0.06048, 0.06048, 0.06596, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.11914, 0.21532, 0.06048, 0.1121, 0.06048, 0.06048, 0.06048, 0.37016, 0.06048, 0.21532, 0.069, 0.37016, 0.1121, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.21532, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.07242, 0.06048, 0.09919, 0.34226, 0.06665, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.06048, 0.07339, 0.09919, 0.06048, 0.06048], 'wisbek': [0.16291, 0.16251, 0.1595, 0.38837, 0.20703, 0.563, 0.50116, 0.15998, 0.39318, 0.16114, 0.43784, 0.16534, 0.1595, 0.16077, 0.16964, 0.1595, 0.25455, 0.1595, 0.16291, 0.21216, 0.19092, 0.64124, 0.17462, 0.1595, 0.1595, 0.16634, 0.21229, 0.39318, 1.0, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.26029, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.25455, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.17765, 0.1595, 0.25455, 0.1595, 0.25455, 0.1595, 0.1595, 0.16608, 0.16534, 0.1595, 0.1595, 0.1595, 0.25455, 0.1595, 0.1595, 0.28543, 0.16634, 0.1595, 0.1595, 0.25455, 0.1595, 0.1595, 0.1595, 0.1595, 0.3496, 0.1595, 0.1595, 0.19119, 0.16778, 0.1595, 0.1595, 0.16328, 0.1595, 0.1595, 0.1595, 0.19192, 0.1595, 0.1595, 0.1595, 0.28214, 0.1595, 0.1595, 0.16992, 0.16248, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.17726, 0.1661, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1652, 0.28722, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.16536, 0.16291, 0.31462, 0.21216, 0.19119, 0.19092, 0.17423, 0.64124, 0.19119, 0.17462, 0.59875, 0.16307, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.16458, 0.06534, 0.20703, 0.26364, 0.16875, 0.06621, 0.41197, 0.34035, 0.1595, 0.0595, 0.40443, 0.06324, 0.1595, 0.06231, 0.1595, 0.06474, 0.1595, 0.0595, 0.1595, 0.0595, 0.1595, 0.18027, 0.15996, 0.4146, 0.1595, 0.31184, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.20703, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.15998, 0.1595, 0.1595, 0.1595, 0.1595, 0.15993, 0.1595, 0.1595, 0.1595, 0.1595, 0.15993, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.64124, 0.1595, 0.20703, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.1595, 0.80965, 0.1595, 0.02264, 0.02325, 0.06003, 0.0125, 0.0125, 0.03157, 0.03146, 0.02706, 0.0125, 0.01934, 0.06529, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.3554, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.01591, 0.0338, 0.0125, 0.0125, 0.0125, 0.11329, 0.08799, 0.11329, 0.0125, 0.0125, 0.0125, 0.0125, 0.01591, 0.06516, 0.04392, 0.49424, 0.02762, 0.0125, 0.0125, 0.01934, 0.36058, 0.20694, 0.01298, 0.23711, 0.23236, 0.0125, 0.10755, 0.06003, 0.06003, 0.01769, 0.01299, 0.0125, 0.06003, 0.0125]}

def solve_fennick(clue):
    lines = clue.split('\n')
    eq = next(i for i,l in enumerate(lines) if l.startswith('===='))
    pic = [list(l) for l in lines[:eq]]
    W = max(len(r) for r in pic)
    for r in pic:
        while len(r) < W: r.append(' ')
    g = eq-1
    ground = pic[g]
    n = 0
    if eq+1 < len(lines):
        t = lines[eq+1].split()
        if t and t[0].isdigit(): n = int(t[0])
    is_t = [c < len(ground) and ground[c] not in ('.',' ') for c in range(W)]
    h = [0]*W
    for c in range(W):
        if not is_t[c]: continue
        k = 0; r = g
        while r >= 0 and pic[r][c] not in (' ','_'):
            k += 1; r -= 1
        h[c] = k
    falls = []   # (col, dir)
    c = 0
    while c < W:
        if is_t[c]: c += 1; continue
        s = c
        while c < W and not is_t[c]: c += 1
        e = c-1
        L = s-1; R = e+1
        if L < 0 or R >= W or e != s: continue
        if h[L] < h[R]:
            if L-1 >= 0 and is_t[L-1]: falls.append((L, 1))
        elif h[R] < h[L]:
            if R+1 < W and is_t[R+1]: falls.append((R, -1))
    out = [row[:] for row in pic]
    for (c,d) in falls:
        for r in range(0, g):
            ch = pic[r][c]
            if ch == ' ': continue
            out[r][c] = ' '
            out[r][c+d] = ('/' if d==1 else '\\') if ch=='_' else ch
    res = [''.join(r).rstrip() for r in out]
    return '\n'.join(res + lines[eq:]), len(falls), n



_READY = [False]

def on_round_start(memory):
    if not _READY[0]:
        init()
        _READY[0] = True

RULE_CLASSES = ('tavrik', 'borsel', 'tresk', 'dornic', 'wisbek')

def solve(name, clue, memory):
    try:
        if name in RULE_CLASSES:
            return choose(name, clue)
        if name == 'fennick':
            return solve_fennick(clue)[0]
        return None
    except Exception:
        return None

def on_round_end(items, memory):
    pass
