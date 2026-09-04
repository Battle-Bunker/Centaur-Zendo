"""strategy.py — sarn2b — FINAL.

Everything scored in training had: one word per digit, every word starting with
the clue's letter.  Only two shapes ever scored, so those are the only shapes we
spend time on:

    3-digit clue -> word lengths exactly the digits      (7 / 435 = 1.6%)
    4-digit clue -> word lengths = digits + 2            (2 /  16 = 12.5%)

5- and 6-digit clues never scored once in 449 attempts, so we skip them: a skip
is instant, costs no answer for the precision tiebreak, and buys more challenges.
"""

import random
import re

from wordfreq import top_n_list
from english_words import get_english_words_set

CLUE_RE = re.compile(r"^([a-z])(\d+)$")
RANKED = {}                       # (letter, length) -> [words]
RND = random.Random(20260904)
EXTRA = {}


def _build():
    if RANKED:
        return
    try:
        real = get_english_words_set(["web2"], lower=True, alpha=True)
        for w in top_n_list("en", 40000):
            if w.isalpha() and w.isascii() and w in real:
                RANKED.setdefault((w[0], len(w)), []).append(w)
        for w in real:                    # fill any (letter, length) gaps
            if w.isascii() and w.isalpha():
                k = (w[0], len(w))
                if k not in RANKED:
                    EXTRA.setdefault(k, []).append(w)
        for k, v in EXTRA.items():
            RANKED[k] = v
    except Exception:
        pass
    if not RANKED:                                  # last-ditch fallback
        for c in "abcdefghijklmnopqrstuvwxyz":
            for n in range(1, 10):
                RANKED[(c, n)] = [(c * n)]


def on_round_start(memory):
    _build()


# offset added to every digit, per number of digits; None = skip the challenge
OFFSET = {3: 0, 4: 2}


def solve(name, clue, memory):
    try:
        m = CLUE_RE.match(clue)
        if m is None:
            m = CLUE_RE.match(clue.strip().lower())
            if m is None:
                return None
        ds = m.group(2)
        off = OFFSET.get(len(ds))
        if off is None:
            return None
        L = m.group(1)
        pick = RND.choice
        out = []
        for ch in ds:
            bag = RANKED.get((L, int(ch) + off))
            if not bag:
                return None
            out.append(pick(bag))
        return " ".join(out)
    except Exception:
        return None
