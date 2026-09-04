"""sarn2a — cells table + fallback probes."""
import re, json, os

_S = {}
V = set("aeiou")
HERE = os.path.dirname(os.path.abspath(__file__))


def collapse(w):
    o = []
    for c in w:
        if not o or o[-1] != c:
            o.append(c)
    return "".join(o)


def penB(w):
    c = collapse(w)
    if c[-1] in V:
        return False
    run = 0
    for ch in c:
        if ch not in V:
            run += 1
            if run > 1:
                return False
        else:
            run = 0
    return True


def fB(w):
    return len(w) - 1 - (1 if penB(w) else 0)


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1
    if _S.get("ready"):
        return
    cells = {}
    bad = {}
    try:
        raw = json.load(open(os.path.join(HERE, "cells.json")))
        for k, v in raw.items():
            cells[(k[0], int(k[1:]))] = v
    except Exception:
        pass
    try:
        raw = json.load(open(os.path.join(HERE, "bad.json")))
        for k, v in raw.items():
            bad[(k[0], int(k[1:]))] = set(v)
    except Exception:
        pass
    byB = {}
    bylen = {}
    try:
        import wordfreq
        from english_words import get_english_words_set
        real = get_english_words_set(["web2"], lower=True)
        pool = [w for w in wordfreq.top_n_list("en", 30000)
                if len(w) >= 2 and w.isalpha() and w.islower() and w in real]
    except Exception:
        pool = []
    for w in pool:
        v = fB(w)
        if 0 < v < 12 and w not in bad.get((w[0], v), ()):
            byB.setdefault((w[0], v), []).append(w)
        for d in (len(w) - 1, len(w) - 2):
            if 0 < d < 12 and w not in bad.get((w[0], d), ()):
                bylen.setdefault((w[0], len(w)), []).append(w)
                break
    _S.update(cells=cells, bad=bad, byB=byB, bylen=bylen, ready=True)


CLUE_RE = re.compile(r"^([a-z]+)(\d+)$")


def _pick(lst, used, rot):
    if not lst:
        return None
    n = len(lst)
    for t in range(min(n, 60)):
        w = lst[(rot + t) % n]
        if w not in used:
            return w
    return None


def solve(name, clue, memory):
    try:
        m = CLUE_RE.match(clue.strip().lower())
        if not m:
            return None
        L = m.group(1)[0]
        digits = [int(c) for c in m.group(2)]
        rot = 0
        cells = _S["cells"]
        used = set()
        words = []
        for d in digits:
            w = _pick(cells.get((L, d)), used, rot)
            if w is None:
                w = _pick(_S["byB"].get((L, d)), used, rot)
                if w is None:
                    w = _pick(_S["bylen"].get((L, d + 2)), used, rot)
                if w is None:
                    w = _pick(_S["bylen"].get((L, d + 1)), used, rot)
                if w is None:
                    return None
            used.add(w)
            words.append(w)
        return " ".join(words)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
