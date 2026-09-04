"""Wordz.

Rule (deduced from demos + scored rounds):
  clue is a string of digits; the answer is one dictionary word per digit.
  Word i (1-indexed):  i odd  -> exactly d_i vowels      (a e i o u, with repeats)
                       i even -> exactly d_i consonants  (with repeats)
  Every word must be in the server's English dictionary (a web2-style list).
"""

VOWELS = set("aeiou")

# (parity, digit) -> word.  parity 0 = odd position (vowel count),
#                           parity 1 = even position (consonant count).
VW = {}
CW = {}
_CACHE = {}

# Hard-coded fallbacks: all verified in-dictionary, correct counts.
FALLBACK_V = {1: "the", 2: "you", 3: "about", 4: "because", 5: "information",
              6: "international", 7: "identification", 8: "telecommunication",
              9: "neurodegenerative"}
FALLBACK_C = {1: "to", 2: "the", 3: "that", 4: "which", 5: "through",
              6: "something", 7: "government", 8: "construction",
              9: "understanding"}


def _build():
    if VW:
        return
    words = []
    try:
        from wordfreq import top_n_list
        from english_words import get_english_words_set
        web2 = get_english_words_set(["web2"], lower=True)
        words = [w for w in top_n_list("en", 200000)
                 if w.isalpha() and w.isascii() and w.islower() and w in web2]
    except Exception:
        words = []
    for w in words:
        v = sum(1 for ch in w if ch in VOWELS)
        c = len(w) - v
        if v not in VW:
            VW[v] = w
        if c not in CW:
            CW[c] = w
    for d, w in FALLBACK_V.items():
        VW.setdefault(d, w)
    for d, w in FALLBACK_C.items():
        CW.setdefault(d, w)


def on_round_start(memory):
    _build()
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    try:
        hit = _CACHE.get(clue)
        if hit is not None:
            return hit
        out = []
        k = 0
        for ch in clue:
            d = ord(ch) - 48
            if d < 0 or d > 9:
                return None
            w = VW.get(d) if (k & 1) == 0 else CW.get(d)
            if w is None:
                return None
            out.append(w)
            k += 1
        if not out:
            return None
        ans = " ".join(out)
        if len(_CACHE) < 20000:
            _CACHE[clue] = ans
        return ans
    except Exception:
        return None


def on_round_end(items, memory):
    pass
