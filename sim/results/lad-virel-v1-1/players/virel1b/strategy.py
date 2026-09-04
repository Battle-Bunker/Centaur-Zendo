"""virel — FINAL.

Clue is "<digits, each 2..6>/<k>".  Let w = sum of the digits.
The answer is a "brick wall": lines of bracket groups, where a group with g
dashes has width g+2, every line is a composition of w into parts 2..6, and the
LAST line is the clue digits themselves.  The wall must have no fault line (no
interior column that is a joint in every row) and needs >= 5 lines.

Measured over ~2300 scored answers, the best generator found is: 7 lines, all
distinct, no column used as a joint by more than 4 lines.  ~15-18% accepted.
`k` never resolved into any constraint on the wall.

Speed: ~0.05 ms per challenge; all tables are built in on_round_start.
"""

import random

MINP, MAXP = 2, 6
POOL = 500          # cached distinct rows per width
NROWS = 7           # lines per wall
CAP = 4             # max lines that may share the same joint column


def _uniform(w, rng):
    """A random composition of w into parts 2..6."""
    lo = -(-w // MAXP)
    hi = w // MINP
    n = rng.randint(lo, hi)
    parts = [MINP] * n
    rem = w - MINP * n
    order = list(range(n))
    while rem > 0:
        rng.shuffle(order)
        for i in order:
            if rem <= 0:
                break
            room = MAXP - parts[i]
            if room > 0:
                add = min(room, rem, rng.randint(1, room))
                parts[i] += add
                rem -= add
    return parts


def _mk(parts):
    s = "".join("[" + "-" * (p - 2) + "]" for p in parts)
    j = []
    a = 0
    for p in parts[:-1]:
        a += p
        j.append(a)
    return s, tuple(j)


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1
    rng = random.Random(1618)
    pools = {}
    for w in range(4, 44):
        seen = set()
        rows = []
        for _ in range(POOL):
            try:
                s, j = _mk(_uniform(w, rng))
            except Exception:
                continue
            if s not in seen:
                seen.add(s)
                rows.append((s, j))
        if rows:
            pools[w] = rows
    memory["_p"] = pools
    memory["_rng"] = random.Random(31415)


def solve(name, clue, memory):
    try:
        pools = memory.get("_p")
        rng = memory.get("_rng")
        if pools is None:
            return None
        i = clue.find("/")
        dg = clue[:i] if i > 0 else clue
        w = 0
        for c in dg:
            w += int(c)
        pool = pools.get(w)
        if not pool:
            return None
        last, lastj = _mk([int(c) for c in dg])
        L = len(pool)
        cnt = {}
        for p in lastj:
            cnt[p] = 1
        picked = []
        used = {last}
        tries = 0
        while len(picked) < NROWS - 1 and tries < 70:
            tries += 1
            s, j = pool[rng.randrange(L)]
            if s in used:
                continue
            bad = False
            for p in j:
                if cnt.get(p, 0) >= CAP:
                    bad = True
                    break
            if bad:
                continue
            for p in j:
                cnt[p] = cnt.get(p, 0) + 1
            used.add(s)
            picked.append(s)
        if len(picked) < 4:
            return None
        picked.append(last)
        if max(cnt.values()) >= len(picked):
            return None            # fault line -> certain 0, skip instead
        return "\n".join(picked)
    except Exception:
        return None


def on_round_end(items, memory):
    memory.pop("_p", None)
    memory.pop("_rng", None)
