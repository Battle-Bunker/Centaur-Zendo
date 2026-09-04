"""tovel — final strategy.

Clue "A/B/C/D/E":
  A = days in the month, B = weekday of day 1 (Mon=0), C = a letter,
  D = a small number, E = a day of the month.
Answer: the month rendered as a calendar, every day tagged with a letter.
Letter C runs from day E for as long as it takes to cover W(D) working
days (Mon-Fri); every other day cycles through D other letters.
"""

HDR = ' '.join([' Mo', ' Tu', ' We', ' Th', ' Fr', ' Sa', ' Su'])
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
W = {2: 4, 3: 7, 4: 8, 5: 9, 6: 12}
OTHERS = {ch: [x for x in ALPHA if x != ch] for ch in ALPHA}


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        p = clue.split('/')
        A = int(p[0]); B = int(p[1]); C = p[2]; D = int(p[3]); E = int(p[4])
        need = W.get(D, 2 * D)
        end = E
        seen = 0
        d = E
        while d <= A:
            if (B + d - 1) % 7 <= 4:
                seen += 1
                end = d
                if seen >= need:
                    break
            d += 1
        if seen < need:                      # cannot fit: run to the end
            end = A
        o = OTHERS.get(C) or [x for x in ALPHA if x != C]
        o = o[:D] if D >= 1 else o[:1]
        no = len(o)
        cells = ['   '] * B
        i = 0
        for d in range(1, A + 1):
            if E <= d <= end:
                ch = C
            else:
                ch = o[i % no]; i += 1
            cells.append('%2d%s' % (d, ch))
        out = [HDR]
        for j in range(0, len(cells), 7):
            out.append(' '.join(cells[j:j + 7]).rstrip())
        return '\n'.join(out)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
