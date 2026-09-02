"""strategy.py — Centaur Zendo brain for team ada.

Solvers live in solvers.py.  Each class has N candidate *answer format*
variants; until a variant is confirmed by a score of 1 we cycle through them
and lock in whichever one scores.
"""
import os, sys, time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import solvers
from solvers import SOLVERS

# names we have given up on: answer nothing (protects the precision tiebreak)
SKIP = set()

# answer-format variants confirmed by a score of 1 on the server
FORCE = {
    'AHMES': 1, 'ALLWIN': 0, 'ANAPAL': 0, 'BASILISK': 0, 'CHAKRA': 0,
    'CRIBROT': 0, 'DUOMASK': 0, 'GRAYLING': 1, 'HAIL': 0, 'HANSOM': 0,
    'IDX': 0, 'MARIENBAD': 2, 'PP': 0, 'RUNIC': 1, 'SPQ': 3, 'SUNZI': 0,
    'TARE': 6, 'TOPPLE': 0, 'TWINE': 0, 'carre': 0, 'erewhon': 0,
    'hanjie': 0, 'ikos': 0, 'krom': 1, 'regina': 0, 'skerry': 0,
    'trico': 3, 'volute': 0, 'warren': 0, 'wolf': 1, 'zebu': 3,
}

_lock = {}       # name -> confirmed variant
_cache = {}      # (name, clue) -> answer, for repeated clues


def _variant(name, clue, nv):
    """Deterministic variant choice so scores can be attributed after the round."""
    h = 0
    for ch in clue:
        h = (h * 131 + ord(ch)) & 0xFFFFFFF
    return h % nv


def on_round_start(memory):
    global _lock
    solvers.build_palprimes()
    solvers.build_hail()
    solvers.build_life(5)
    solvers.build_life(6)
    _lock = dict(memory.get("lock", {}))
    _lock.update(FORCE)
    _cache.clear()
    memory.setdefault("stats", {})
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    if name in SKIP:
        return ""
    ent = SOLVERS.get(name)
    if ent is None:
        return ""
    key = (name, clue)
    hit = _cache.get(key)
    if hit is not None:
        return hit
    fn, nv = ent
    v = _lock.get(name)
    if v is None:
        v = _variant(name, clue, nv)
    try:
        ans = fn(clue, v)
    except Exception:
        ans = ""
    _cache[key] = ans
    return ans


def on_round_end(items, memory):
    lock = memory.setdefault("lock", {})
    stats = memory.setdefault("stats", {})
    for it in items:
        name = it.get("name")
        clue = it.get("clue")
        sc = it.get("score") or 0
        ent = SOLVERS.get(name)
        if ent is None:
            continue
        v = _lock.get(name)
        if v is None:
            v = _variant(name, clue, ent[1])
        st = stats.setdefault(name, {})
        cell = st.setdefault(str(v), [0, 0])
        cell[0] += 1
        cell[1] += sc
        if sc and name not in lock:
            lock[name] = v
    # a variant with hits always wins over the rotation
    for name, st in stats.items():
        best = max(st.items(), key=lambda kv: (kv[1][1], -kv[1][0]))
        if best[1][1] > 0:
            lock[name] = int(best[0])
