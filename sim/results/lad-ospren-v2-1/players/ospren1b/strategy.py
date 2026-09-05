"""Centaur Zendo brain.

Six of the seven classes are "here are examples of a hidden rule, now pick
which of the four candidates also obeys it".  We induce the rule by finding
every feature-value shared by all the positives, weighting each by how rare
that value is in the corpus of items we have seen, and letting the surviving
rules vote for the candidate(s) they accept.  The seventh (fennick) is a
picture class and is solved exactly.
"""

import json
import os

from parsing import parse
from features import EXTRACT
from fennick import solve_fennick

HERE = os.path.dirname(os.path.abspath(__file__))
MINFREQ = 0.05
POWER = 2.5
SATPOW = 6.0

STATS = {}


def _build(corpus):
    stats = {}
    for name, items in corpus.items():
        fn = EXTRACT.get(name)
        if not fn:
            continue
        tab = {}
        n = 0
        for it in items:
            try:
                d = fn(it)
            except Exception:
                continue
            n += 1
            for k, v in d.items():
                s = tab.get(k)
                if s is None:
                    s = tab[k] = {}
                s[v] = s.get(v, 0) + 1
        if n:
            for k in tab:
                for v in tab[k]:
                    tab[k][v] = max(tab[k][v] / float(n), MINFREQ)
        stats[name] = tab
    return stats


def on_round_start(memory):
    global STATS
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1
    corpus = {}
    try:
        with open(os.path.join(HERE, "corpus.json")) as fh:
            corpus = json.load(fh)
    except Exception:
        corpus = {}
    for name, items in (memory.get("corpus") or {}).items():
        corpus.setdefault(name, [])
        corpus[name] += items
    try:
        STATS = _build(corpus)
    except Exception:
        STATS = {}
    memory["examples"] = {}


def solve(name, clue, memory):
    try:
        if name == "fennick":
            return solve_fennick(clue)
        fn = EXTRACT.get(name)
        if fn is None:
            return None
        pos, cands = parse(clue)
        if len(cands) < 2 or not pos:
            return None
        pf = []
        for p in pos:
            try:
                pf.append(fn(p))
            except Exception:
                pass
        cf = []
        for c in cands:
            try:
                cf.append(fn(c))
            except Exception:
                cf.append({})
        if not pf:
            return "1"
        tab = STATS.get(name, {})
        nc = len(cands)
        score = [0.0] * nc
        first = pf[0]
        rest = pf[1:]
        for k, v in first.items():
            ok = True
            for d in rest:
                if d.get(k) != v:
                    ok = False
                    break
            if not ok:
                continue
            sat = [i for i in range(nc) if cf[i].get(k) == v]
            ns = len(sat)
            if ns == 0 or ns == nc:
                continue
            freq = tab.get(k, {}).get(v, MINFREQ)
            w = (freq ** -POWER) / (ns ** SATPOW)
            for i in sat:
                score[i] += w
        best = 0
        bs = score[0]
        for i in range(1, nc):
            if score[i] > bs:
                bs = score[i]
                best = i
        return str(best + 1)
    except Exception:
        return "1"


def on_round_end(items, memory):
    memory["examples"] = {}      # keep memory.json tiny: the logs hold everything
