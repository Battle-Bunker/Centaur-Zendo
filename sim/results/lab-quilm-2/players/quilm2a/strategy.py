"""quilm  —  clue "<digits>/<K>"

Rule (reverse-engineered, verified on 44/44 known correct answers):
render the digit string on seven-segment displays and MOVE EXACTLY K
matchsticks.  So the answer is a same-length digit string X with

    sum_i |seg(n_i) \ seg(x_i)|  ==  sum_i |seg(x_i) \ seg(n_i)|  ==  K

Leading zeros in the answer are fine.  An answer that is a mere ANAGRAM of
the clue's digits is rejected by the server, so those are avoided.
"""

_SEG = {'0': 0b0111111, '1': 0b0000110, '2': 0b1011011, '3': 0b1001111,
        '4': 0b1100110, '5': 0b1101101, '6': 0b1111101, '7': 0b0000111,
        '8': 0b1111111, '9': 0b1101111}
_DIGITS = "0123456789"


def _pc(x):
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c


# OFFON[a] -> tuple of (off, on, b) over every digit b (off/on <= 4 only)
OFFON = {}
for _a in _DIGITS:
    _ma = _SEG[_a]
    OFFON[_a] = tuple((_pc(_ma & ~_SEG[_b]), _pc(_SEG[_b] & ~_ma), _b)
                      for _b in _DIGITS
                      if _pc(_ma & ~_SEG[_b]) <= 4 and _pc(_SEG[_b] & ~_ma) <= 4)

# SWAP[k][a] -> tuple of digits b reachable from a with exactly k off and k on
SWAP = {}
for _k in range(1, 5):
    SWAP[_k] = {a: tuple(b for off, on, b in OFFON[a] if off == _k and on == _k)
                for a in _DIGITS}

_CACHE = {}
_MAXCACHE = 200000


def on_round_start(memory):
    _CACHE.clear()


def _dp1(s, K):
    """fast DP: returns one solution or None."""
    L = len(s)
    dp = {(0, 0): ()}
    for i in range(L):
        opts = OFFON[s[i]]
        nd = {}
        for (o, n), pick in dp.items():
            for do, dn, b in opts:
                no = o + do
                nn = n + dn
                if no > K or nn > K:
                    continue
                key = (no, nn)
                if key not in nd:
                    nd[key] = pick + (b,)
        if not nd:
            return None
        dp = nd
    pick = dp.get((K, K))
    return "".join(pick) if pick else None


def _dp(s, K):
    """wider DP that keeps alternatives so an anagram answer can be dodged."""
    L = len(s)
    dp = {(0, 0): [()]}
    for i in range(L):
        opts = OFFON[s[i]]
        nd = {}
        for (o, n), picks in dp.items():
            for do, dn, b in opts:
                no = o + do
                nn = n + dn
                if no > K or nn > K:
                    continue
                key = (no, nn)
                cur = nd.get(key)
                if cur is None:
                    nd[key] = cur = []
                if len(cur) < 12:
                    for pk in picks:
                        cur.append(pk + (b,))
                        if len(cur) >= 12:
                            break
        if not nd:
            return None
        dp = nd
    picks = dp.get((K, K))
    if not picks:
        return None
    ss = sorted(s)
    for pk in picks:
        cand = "".join(pk)
        if sorted(cand) != ss:
            return cand
    return "".join(picks[0])


def solve(name, clue, memory):
    try:
        r = _CACHE.get(clue)
        if r is not None:
            return r
        s, _, ks = clue.partition("/")
        K = int(ks)
        tbl = SWAP.get(K)
        if tbl is not None:
            # one-position fix whose new digit is absent from the clue ->
            # guaranteed not to be an anagram
            for i, ch in enumerate(s):
                for b in tbl[ch]:
                    if b not in s:
                        r = s[:i] + b + s[i + 1:]
                        if len(_CACHE) < _MAXCACHE:
                            _CACHE[clue] = r
                        return r
            ss = sorted(s)
            for i, ch in enumerate(s):
                for b in tbl[ch]:
                    r = s[:i] + b + s[i + 1:]
                    if sorted(r) != ss:
                        if len(_CACHE) < _MAXCACHE:
                            _CACHE[clue] = r
                        return r
        r = _dp1(s, K)
        if r is None:
            return None
        if sorted(r) == sorted(s):
            r2 = _dp(s, K)
            if r2 is not None:
                r = r2
        if len(_CACHE) < _MAXCACHE:
            _CACHE[clue] = r
        return r
    except Exception:
        return None


def on_round_end(items, memory):
    pass
