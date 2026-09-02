"""English word lists for challenge generators and scorers.

Available inside the sandbox as the pre-imported module ``words`` (also ``import words``).

    words.WORDS        frozenset of lowercase English words (large; for checking answers)
    words.COMMON       list of ~20k common words, most frequent first (for generating clues)
    words.is_word(w)   True if w.lower() is in WORDS
    words.vowels(w)    number of vowels (a e i o u; y counts as a consonant)
    words.consonants(w) number of letters that are not vowels
    words.pick(rng, pred=None, n=1)  random COMMON word(s) satisfying pred

Backed by the ``english-words`` (web2) and ``wordfreq`` packages when installed; otherwise a
bundled 20k common-word list serves as both WORDS and COMMON.
"""
from __future__ import annotations
import os

VOWELS = frozenset("aeiou")
_here = os.path.dirname(__file__)


def _load_common() -> list[str]:
    try:
        from wordfreq import top_n_list  # type: ignore
        raw = top_n_list("en", 40000)
    except Exception:
        raw = []
    if not raw:
        with open(os.path.join(_here, "data", "common_words.txt")) as f:
            return [w.strip() for w in f if w.strip()]
    return [w for w in raw if w.isalpha() and w.isascii() and 3 <= len(w) <= 12][:20000]


def _dictionary() -> frozenset[str] | None:
    try:
        from english_words import get_english_words_set  # type: ignore
        return frozenset(w for w in get_english_words_set(["web2"], lower=True) if w.isalpha())
    except Exception:
        return None


_DICT = _dictionary()
COMMON: list[str] = _load_common()
if _DICT is not None:                       # keep only real dictionary words (drops slang/names)
    COMMON = [w for w in COMMON if w in _DICT][:20000]
WORDS: frozenset[str] = (_DICT or frozenset()) | frozenset(COMMON)


def is_word(w: str) -> bool:
    return isinstance(w, str) and w.lower() in WORDS


def vowels(w: str) -> int:
    return sum(ch in VOWELS for ch in w.lower())


def consonants(w: str) -> int:
    return sum(ch.isalpha() and ch not in VOWELS for ch in w.lower())


def pick(rng, pred=None, n: int = 1):
    """Random common word(s) satisfying pred (a callable on the word). Returns a str when n == 1."""
    pool = COMMON if pred is None else [w for w in COMMON if pred(w)]
    if not pool:
        raise ValueError("no common word satisfies the predicate")
    out = [rng.choice(pool) for _ in range(n)]
    return out[0] if n == 1 else out
