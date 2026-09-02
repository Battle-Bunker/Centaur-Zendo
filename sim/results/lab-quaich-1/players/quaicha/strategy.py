"""quaich solver.

Clue: a string over {-, |, /}.  Let a=#'-', b=#'|', c=#'/'.
Every character is matched with one of a *different* kind; the multiplicities
are forced:  p = (a+b-c)/2 pairs of (-,|), q = a-p pairs of (/,-),
r = b-p pairs of (/,|).  The answer writes those pairs as runs:

  both / groups present :  /^r |^r  -^p |^p  /^q -^q     (split /^r|^r into
                           r copies of "/|" when r > q)
  no (/,|) pairs (r=0)  :  -^q /^q  -^p |^p              (split into "-/"*q
                           when q > p)
  no (/,-) pairs (q=0)  :  |^p -^p  |^r /^r              (split into "|-"*p
                           when p > r)

i.e. three blocks in a fixed order, and the *first* block may never be longer
than the last one -- if it would be, it is broken into unit blocks.
"""

_CACHE = {}


def on_round_start(memory):
    _CACHE.clear()


def _build(a, b, c):
    t = a + b - c
    if t < 0 or t % 2:
        return None
    p = t // 2
    q = a - p
    r = b - p
    if q < 0 or r < 0:
        return None
    if r and q:
        mid = "-" * p + "|" * p + "/" * q + "-" * q
        return ("/" * r + "|" * r + mid) if r <= q else ("/|" * r + mid)
    if r == 0:
        db = "-" * p + "|" * p
        return ("-" * q + "/" * q + db) if (q <= p or not p) else ("-/" * q + db)
    sb = "|" * r + "/" * r
    return ("|" * p + "-" * p + sb) if (p <= r or not p) else ("|-" * p + sb)


def solve(name, clue, memory):
    try:
        key = (clue.count('-'), clue.count('|'), clue.count('/'))
        try:
            return _CACHE[key]
        except KeyError:
            pass
        v = _build(*key)
        _CACHE[key] = v
        return v
    except Exception:
        return None
