"""Centaur Zendo - class `tovel`.

Clue: days/first_weekday/LETTER/k/m  ->  answer: a rendered month calendar
where every day carries a letter.

What was learned:
  * layout: header " Mo  Tu  We  Th  Fr  Sa  Su", each cell "%2d%s"
    (day number then its letter), cells joined by one space, 7 per row,
    leading blanks for `first_weekday`, every row rstripped.
  * the letter rule: L must sit on day m and then every other day,
    k+1 times in total (days m, m+2, ..., m+2k).  Verified at k=1 for every
    weekday of m, and at k=2 when day m is a Monday.  At k=2 with m on a
    Tue/Wed, and at every k>=3, no construction tried ever scored, so those
    are skipped: a skip is instant, scores the same 0 as a wrong answer and
    keeps the answered-count tiebreak clean.
"""

HDR = ' Mo  Tu  We  Th  Fr  Sa  Su'
BLANK = '   '
DNUM = ['%2d' % d for d in range(32)]


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        a = clue.split('/')
        kf = a[3]
        if kf == '1':
            k = 1
        elif kf == '2':
            k = 2
        else:
            return None
        m = int(a[4])
        w = int(a[1])
        if k == 2 and (w + m - 1) % 7 != 0:
            return None
        days = int(a[0])
        L = a[2]
        X = 'A' if L != 'A' else 'B'
        chain = (m, m + 2) if k == 1 else (m, m + 2, m + 4)
        cells = [BLANK] * w
        ap = cells.append
        for d in range(1, days + 1):
            ap(DNUM[d] + (L if d in chain else X))
        out = [HDR]
        for i in range(0, len(cells), 7):
            out.append(' '.join(cells[i:i + 7]).rstrip())
        return '\n'.join(out)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
