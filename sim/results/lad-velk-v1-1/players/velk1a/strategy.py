"""velk solver — clue "WORD|k".

Answer: a crossing ("braid") diagram.
  * row 0 is the word, letters separated by single spaces;
  * between two rows a separator line of n vertical bars, with one adjacent
    pair replaced by a crossing mark ('\' or '/') showing that those two
    letters swap;
  * there are exactly 2k-1 crossings, and they ALTERNATE: the strand that
    started in position 0 (the "hunt") takes part in crossings 1, 3, 5 ...
    (k of them), and the crossings in between involve any other pair.
  * mark is '\' when the hunt moves right, '/' when it moves left.

Verified: 515/515 in training round 2 across 8 variants of the free choices
(filler position, filler mark, hunt direction), so only the structure matters.

Everything below is precomputed per (n, k) shape: a %-format template plus an
itemgetter, so answering a clue is one dict lookup, one C-level itemgetter and
one string interpolation.
"""

from operator import itemgetter

MAXLEN = 1024
_CACHE = {}


def _template(n, k):
    """Return (template, itemgetter) for words of length n with parameter k."""
    if n < 2 or k < 1:
        return None
    perm = list(range(n))          # perm[p] = index (in the word) at position p
    t = 0                          # position of the hunt strand
    rows = [tuple(perm)]
    seps = []
    bar = ["|" if j % 2 == 0 else " " for j in range(2 * n - 1)]
    for s in range(2 * k - 1):
        if s % 2 == 0:                              # hunt crossing
            right = t < n - 1
            i = t if right else t - 1
            mark = "\\" if right else "/"
            t = t + 1 if right else t - 1
        else:                                       # filler crossing
            i = -1
            for j in range(n - 1):
                if j != t and j + 1 != t:
                    i = j
                    break
            if i < 0:
                return None
            mark = "\\"
        line = bar[:]
        line[2 * i] = " "
        line[2 * i + 1] = mark
        line[2 * i + 2] = " "
        seps.append("".join(line).rstrip())
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
        rows.append(tuple(perm))
    idx = []
    parts = []
    row_tmpl = " ".join(["%s"] * n)
    for r, row in enumerate(rows):
        if r:
            parts.append(seps[r - 1])
        parts.append(row_tmpl)
        idx.extend(row)
    tmpl = "\n".join(parts)
    if len(tmpl) - 2 * len(idx) + len(idx) > MAXLEN:
        return None
    return tmpl, itemgetter(*idx)


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1
    _CACHE.clear()
    for n in range(2, 13):
        for k in range(1, 13):
            _CACHE[(n, k)] = _template(n, k)


def solve(name, clue, memory):
    try:
        word, _, num = clue.partition("|")
        got = _CACHE.get((len(word), int(num)))
        if got is None:
            return None
        return got[0] % got[1](word)
    except Exception:
        try:
            got = _template(len(word), int(num))
            _CACHE[(len(word), int(num))] = got
            return got[0] % got[1](word) if got else None
        except Exception:
            return None


def on_round_end(items, memory):
    memory["examples"] = {}
