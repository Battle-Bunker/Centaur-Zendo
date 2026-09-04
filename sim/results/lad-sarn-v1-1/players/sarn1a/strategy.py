"""strategy.py — team sarn1a.

THE RULE (worked out from the logs)
  clue   = <letter><digits>            e.g. "h328"
  answer = one word per digit, in order; every word starts with <letter>;
           word i is exactly digit_i + 1 letters long; the words are distinct;
           and every word must belong to the server's own (secret) word list,
           which holds only about a quarter of the commonest English words.

  evidence: "have he his" for h132 (real words, wrong lengths) -> 0
            "have his house" -> 0  but  "have his happening" -> 1

So the whole game is a search: find one member of the server's list for each
(first letter, word length) slot.  Only 15 letters and digits 1..9 ever appear,
so there are 135 slots.

  * every word in an answer that scores 1 is a confirmed member  (memory["good"])
  * failures are weak evidence — "at least one of these is not a member" — so
    analyze.py runs belief propagation over all rounds and leaves a posterior
    per word in memory["post"].
  * for a slot with no confirmed word yet we cycle a fresh candidate on every
    challenge (rotating maximises the chance that some answer is all-members).
"""

import re

_CLUE_RE = re.compile(r"^\s*([A-Za-z]+)\s*([0-9]+)\s*$")

_CONF = {}      # slot -> [confirmed words]
_TRY = {}       # slot -> [candidate words, best posterior first]
_NTRY = {}      # slot -> len(_TRY[slot])
_PRIOR = 0.27
_POOL = 40      # how many candidates per slot to rotate through
_REUSE = True   # round 6 settled it: the same word twice is accepted (36% vs 23%)
_SKIP_UNKNOWN = 4   # skip a challenge needing this many unconfirmed slots


def _load_words():
    try:
        from wordfreq import top_n_list
        words = top_n_list("en", 200000)
    except Exception:
        words = []
    dic = set()
    try:
        from english_words import get_english_words_set
        dic |= get_english_words_set(["web2"], lower=True)
        dic |= get_english_words_set(["gcide"], lower=True)
    except Exception:
        pass
    out, seen = [], set()
    for w in words:
        if not w or not w.isalpha() or not w.islower() or w in seen:
            continue
        if dic and w not in dic:
            continue
        seen.add(w)
        out.append(w)
    return out


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1
    good = memory.setdefault("good", {})
    for k, v in list(good.items()):
        if isinstance(v, str):
            good[k] = [v]
    post = memory.setdefault("post", {})

    cands = {}
    for w in _load_words():
        cands.setdefault(w[0] + str(len(w)), []).append(w)

    _CONF.clear(); _TRY.clear(); _NTRY.clear()
    for slot, pool in cands.items():
        _CONF[slot] = list(good.get(slot, []))
        conf = set(_CONF[slot])
        rest = [w for w in pool if w not in conf and post.get(w, _PRIOR) > 0.05]
        # frequency order, but push down anything the evidence dislikes
        rest.sort(key=lambda w: -post.get(w, _PRIOR))
        _TRY[slot] = rest[:_POOL] or pool[:1]
        _NTRY[slot] = len(_TRY[slot])
    memory["confirmed_slots"] = len(good)


def solve(name, clue, memory):
    try:
        m = _CLUE_RE.match(clue)
        if m is None:
            return None
        letter = m.group(1)[0].lower()
        rot = memory.get("_index", 0)
        # experiment: when the same digit occurs twice, does the server accept
        # the same word twice?  Even challenges reuse it, odd ones stay distinct.
        reuse = _REUSE if _REUSE is not None else (rot % 2 == 0)
        digits = m.group(2)
        slots = [letter + str(int(d) + 1) for d in digits]
        unknown = 0
        for slot in set(slots):
            if not _CONF.get(slot):
                unknown += 1
        if unknown >= _SKIP_UNKNOWN:      # hopeless: skip, it is instant and free
            return None
        out = []
        picked = {}
        for slot in slots:
            if reuse and slot in picked:
                out.append(picked[slot])
                continue
            w = None
            for c in _CONF.get(slot, ()):          # confirmed members first
                if c not in out:
                    w = c
                    break
            if w is None:
                pool = _TRY.get(slot)
                if not pool:
                    return None
                n = _NTRY[slot]
                for k in range(n):                 # rotate the candidate
                    c = pool[(rot + k) % n]
                    if c not in out:
                        w = c
                        break
                if w is None:
                    return None
            out.append(w)
            picked[slot] = w
        return " ".join(out)
    except Exception:
        return None


def on_round_end(items, memory):
    good = memory.setdefault("good", {})
    for it in items:
        if not it.get("score"):
            continue
        for w in (it.get("solution") or "").split():
            slot = w[0] + str(len(w))
            lst = good.setdefault(slot, [])
            if isinstance(lst, str):
                lst = good[slot] = [lst]
            if w not in lst:
                lst.append(w)
    memory["confirmed_slots"] = len(good)
