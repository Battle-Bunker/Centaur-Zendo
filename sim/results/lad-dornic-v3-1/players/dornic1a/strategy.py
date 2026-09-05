"""Centaur Zendo — team dornic1a.

Every class in this pool is the same meta-puzzle:

    <positive example>            (2, sometimes 3, lines/blocks)
    <positive example>
    (blank line)
    <5 candidate instances>       (ospren numbers its blocks; answer = the text)

Exactly one candidate obeys a hidden rule drawn from a per-class family that is
never revealed.  Rather than guess the family, we evaluate a broad bank of
boolean features (zen.py) on the positives and on each candidate:

  * a feature true for EVERY positive and for EXACTLY ONE candidate is a
    possible statement of the rule -> it votes for that candidate;
  * ties, and clues where no feature isolates a candidate, fall back to
    "which candidate shares the most positive-consistent features" - measured
    at ~50% on no-vote clues versus 20% for a blind guess.

Never skips: a blind answer is worth 20%, a skip is worth 0.
"""
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

try:
    import zen as Z
    _FEAT = Z.FEAT
    _OK = True
except Exception:                                    # pragma: no cover
    _FEAT = {}
    _OK = False

BUDGET = 0.030          # hard stop; a slow answer costs the whole round


def _parse(clue):
    """-> (positives, options).  Handles both clue layouts and 2-or-3 positives."""
    blocks = clue.split("\n\n")
    if len(blocks) == 2:
        pos = [l for l in blocks[0].split("\n") if l.strip()]
        opts = [l for l in blocks[1].split("\n") if l.strip()]
        return pos, opts
    pos = []
    opts = []
    for b in blocks:
        lines = b.split("\n")
        if lines and lines[0].strip().isdigit():
            opts.append("\n".join(lines[1:]).strip("\n"))
        else:
            pos.append(b.strip("\n"))
    return pos, opts


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    idx = memory.get("_index", 0)
    opts = None
    try:
        pos, opts = _parse(clue)
        if not opts:
            return None
        if not _OK or name not in _FEAT or len(pos) < 1:
            return opts[idx % len(opts)]
        t0 = time.perf_counter()
        fn = _FEAT[name]
        pf = Z.PARSE[name]
        fp = [fn(pf(p)) for p in pos]
        fo = [fn(pf(o)) for o in opts]
        n = len(fo)
        votes = [0] * n
        sim = [0] * n
        pairs = []
        f0 = fp[0]
        rest = fp[1:]
        for k, v in f0.items():
            if not v:
                continue
            ok = True
            for f in rest:
                if not f.get(k):
                    ok = False
                    break
            if not ok:
                continue
            hit = -1
            cnt = 0
            for i in range(n):
                if fo[i].get(k):
                    sim[i] += 1
                    cnt += 1
                    hit = i
            if cnt == 1:
                votes[hit] += 1
            elif cnt == 2 and len(pairs) < 60:
                pairs.append(tuple(i for i in range(n) if fo[i].get(k)))
        if time.perf_counter() - t0 > BUDGET:
            return opts[idx % n]
        # conjunctions: two 2-candidate features meeting in one candidate are a
        # possible compound rule ("both divisible by 3", ...).  Used only to
        # break ties / rescue clues where nothing isolates a candidate.
        conj = [0] * n
        np_ = len(pairs)
        for a in range(np_):
            pa = pairs[a]
            for b in range(a + 1, np_):
                pb = pairs[b]
                if pa[0] == pb[0] or pa[0] == pb[1]:
                    if not (pa[1] == pb[0] or pa[1] == pb[1]):
                        conj[pa[0]] += 1
                elif pa[1] == pb[0] or pa[1] == pb[1]:
                    conj[pa[1]] += 1
        best = 0
        for i in range(1, n):
            if (votes[i], conj[i], sim[i]) > (votes[best], conj[best], sim[best]):
                best = i
        return opts[best]
    except Exception:
        try:
            if opts:
                return opts[idx % len(opts)]
            return _parse(clue)[1][idx % 5]
        except Exception:
            return None


def on_round_end(items, memory):
    pass
