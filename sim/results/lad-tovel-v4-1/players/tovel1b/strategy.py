"""tovel — FINAL strategy.

Model learned from 6 demos + 132 scoring answers:
  clue = <days>/<first weekday>/<letter X>/<a>/<b>
  Day b always carries X and is always a Mon/Tue/Wed.
  For a=1 a *unique maximal* "every other day" chain X.X starting at day b
  scores 1 every time (23/23).  For a=2 the chain X.X.X works when b is a
  Monday (58%).  Larger a is only partly understood, so several candidate
  shapes are cycled so that at least one family gets played.
"""

HEADER = " Mo  Tu  We  Th  Fr  Sa  Su"
POOL = "BCDFGHJKLMNPQRSTVWXYZ"

# candidate offset families (offsets of the extra X days, relative to b)
S_CHAIN = (2, 4, 6, 8, 10)            # every other calendar day
S_COL = {                              # from the clue generator's b-range limits
    0: (2, 4, 9, 11, 16),
    1: (2, 8, 10, 15, 17),
    2: (2, 7, 9, 14, 16),
}
S_GRID = (2, 4, 7, 9, 11)             # 3 per week, repeating weekly
S_WORK = (2, 4, 8, 10, 14)            # every other working day
S_DEMO = (2, 3, 5, 7, 9)              # shape shared by the two a=5 demos


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        p = clue.split("/")
        nd = int(p[0]); wd = int(p[1]); X = p[2][:1]; a = int(p[3]); b = int(p[4])
        if not (1 <= b <= nd) or a < 1:
            return None
        col = (b - 1 + wd) % 7
        if a == 1:
            offs = S_CHAIN[:1]
        elif (a == 2 and col == 0) or (a == 3 and col == 0):
            offs = S_CHAIN[:a]
        else:
            k = memory.get("_index", 0) & 3
            if a >= 5 and k == 3:
                offs = S_DEMO[:a]
            elif k == 0:
                offs = S_CHAIN[:a]
            elif k == 1:
                offs = S_COL.get(col, S_CHAIN)[:a]
            elif k == 2:
                offs = S_GRID[:a]
            else:
                offs = S_WORK[:a]

        # three filler letters, deterministic and cheap
        h = (ord(X) * 7 + nd * 3 + b) % 21
        f0 = POOL[h]
        if f0 == X:
            f0 = POOL[(h + 1) % 21]
        f1 = POOL[(h + 7) % 21]
        if f1 == X or f1 == f0:
            f1 = POOL[(h + 8) % 21]
        f2 = POOL[(h + 14) % 21]
        if f2 == X or f2 == f0 or f2 == f1:
            f2 = POOL[(h + 15) % 21]
        fil = (f0, f1, f2)

        seq = [fil[(d * 5 + h) % 3] for d in range(nd)]
        days = [b]
        for o in offs:
            if b + o <= nd:
                days.append(b + o)
        last = days[-1]
        for d in days:
            seq[d - 1] = X
        # extra X blocks of three consecutive days, kept >=3 away from the
        # marked days so they cannot create a competing every-other-day chain
        for e in (b - 9, b - 15, last + 6, last + 12):
            if e >= 1 and e + 2 <= nd and (e + 2 <= b - 3 or e >= last + 3):
                seq[e - 1] = X; seq[e] = X; seq[e + 1] = X

        cells = ["   "] * wd
        for d in range(1, nd + 1):
            cells.append("%2d%s" % (d, seq[d - 1]))
        out = [HEADER]
        for i in range(0, len(cells), 7):
            out.append(" ".join(cells[i:i + 7]).rstrip())
        return "\n".join(out)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
