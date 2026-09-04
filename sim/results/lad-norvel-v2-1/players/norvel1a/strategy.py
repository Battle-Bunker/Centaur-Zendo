"""norvel - final.

Read the clue as "<thump pattern>/<n>" and answer with a two-drum grid whose
snap line is the thump's answer.  Two regimes, measured over six rounds:

* thump with no run of 4+ rests ("dense"): snap = the exact complement of the
  first n measures, silent in the rest  (~67% correct).  If that leaves fewer
  than 4 steps where neither drum plays, trim snap hits off the end until it
  does (10/10 in round 6, 0/24 before the fix).
* thump with a long rest run ("sparse"): fill whole measures until the two
  drums together never leave more than 2 steps silent, then steer the leftover
  silence into the 6-10 step band where hits cluster (~15-18%).
"""


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def _comp(m):
    return "".join('.' if c == 'x' else 'x' for c in m)


def _grid(t, s):
    return ("      |" + "|".join(["1234"] * len(t)) + "|\n"
            "thump |" + "|".join(t) + "|\n"
            " snap |" + "|".join(s) + "|")


def _longest_silence(pat, cells):
    b = c = 0
    for i in range(len(pat)):
        if pat[i] == 'x' or cells[i] == 'x':
            c = 0
        else:
            c += 1
            if c > b:
                b = c
    return b


def _silence(pat, cells):
    return sum(1 for i in range(len(pat)) if pat[i] == '.' and cells[i] == '.')


def _gapsafe_sel(pat, maxgap):
    M = len(pat) // 4
    filled = [c == 'x' for c in pat]
    sel = []
    for _ in range(M + 1):
        run = 0
        bad = -1
        for i, v in enumerate(filled):
            if v:
                run = 0
            else:
                run += 1
                if run > maxgap:
                    bad = i
                    break
        if bad < 0:
            break
        m = bad // 4
        if m in sel:
            break
        sel.append(m)
        for j in range(m * 4, m * 4 + 4):
            filled[j] = True
    return sel


def solve(name, clue, memory):
    try:
        pat, ntxt = clue.rsplit('/', 1)
        n = int(ntxt.strip())
        pat = pat.strip()
        L = len(pat)
        if L < 4 or L % 4 or n < 0:
            return None
        M = L // 4
        t = [pat[i * 4:i * 4 + 4] for i in range(M)]
        comp = [_comp(m) for m in t]
        tgap = _longest_silence(pat, '.' * L)

        if tgap <= 3:
            s = [comp[i] if i < n else '....' for i in range(M)]
            cells = list("".join(s))
            need = 4 - _silence(pat, cells)
            if need > 0:                       # validated fix: trim off the end
                for i in range(L - 1, -1, -1):
                    if need <= 0:
                        break
                    if cells[i] == 'x':
                        cells[i] = '.'
                        need -= 1
            return _grid(t, ["".join(cells[i * 4:i * 4 + 4]) for i in range(M)])

        sel = set(_gapsafe_sel(pat, 2))
        cells = list("".join(comp[i] if i in sel else '....' for i in range(M)))
        sil = _silence(pat, cells)
        if sil > 10:                           # too airy: answer more measures
            rest = sorted((i for i in range(M) if i not in sel),
                          key=lambda i: (-t[i].count('.'), i))
            for i in rest:
                if sil <= 10:
                    break
                for j in range(i * 4, i * 4 + 4):
                    if pat[j] == '.' and cells[j] == '.':
                        cells[j] = 'x'
                        sil -= 1
        elif sil < 6:                          # too busy: open a little space
            for i in range(L - 1, -1, -1):
                if sil >= 6:
                    break
                if cells[i] == 'x':
                    cells[i] = '.'
                    if _longest_silence(pat, cells) > 3:
                        cells[i] = 'x'
                    else:
                        sil += 1
        return _grid(t, ["".join(cells[i * 4:i * 4 + 4]) for i in range(M)])
    except Exception:
        return None
