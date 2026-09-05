"""FINAL strategy.

Only two classes are answered; the other five scored 0 across ~200 probes each,
so they are skipped (instant, and skips do not count against the precision
tiebreak).

garrow : the answer is the tank picture with vertical '|' cuts inserted.  Cut
         positions depend on how many columns contain the header letter:
           >=13 columns -> cut just after every 4th such column
           ==10 columns -> cut just after every 3rd such column
           otherwise    -> cut just after the first column of every 3-char
                           token of the header letter
         (measured ~100% for the >=13 branch, ~26% for the fallback branch)
fennick: when the caption is "0 fall" nothing falls, so the answer is the clue
         unchanged.  Every other caption value is unsolved -> skip.
"""
import re

_TOK = re.compile(r'([a-z])\1\1')


def on_round_start(memory):
    memory["cache"] = {}


def _garrow(clue):
    L = clue.rstrip('\n').split('\n')
    letter = L[0][0]
    rows = L[1:]
    W = len(rows[0])
    lcols = []
    for x in range(W):
        for r in rows:
            if r[x] == letter:
                lcols.append(x)
                break
    n = len(lcols)
    if n >= 13:
        cuts = sorted({lcols[i] + 1 for i in range(3, n, 4)})
    elif n == 10:
        cuts = sorted({lcols[i] + 1 for i in range(2, n, 3)})
    else:
        s = set()
        for r in rows:
            for m in _TOK.finditer(r):
                if m.group(1) == letter:
                    s.add(m.start() + 1)
        cuts = sorted(s)
    cuts = [c for c in cuts if 0 < c < W]
    if not cuts:
        return None
    out = []
    for r in rows:
        parts = []
        prev = 0
        for c in cuts:
            parts.append(r[prev:c])
            prev = c
        parts.append(r[prev:])
        out.append('|'.join(parts))
    return '\n'.join(out)


def solve(name, clue, memory):
    if name == 'garrow':
        cache = memory.get("cache")
        if cache is not None:
            a = cache.get(clue)
            if a is not None:
                return a
        try:
            a = _garrow(clue)
        except Exception:
            return None
        if cache is not None and len(cache) < 4000:
            cache[clue] = a
        return a
    if name == 'fennick':
        t = clue.rstrip()
        i = t.rfind('\n')
        if t[i + 1:i + 3] == '0 ':
            return clue
        return None
    return None


def on_round_end(items, memory):
    memory["cache"] = {}
