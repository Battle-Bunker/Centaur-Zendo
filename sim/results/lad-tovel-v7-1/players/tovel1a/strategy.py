"""Final brain.

basten / kelmar : solved (100% over two training rounds)
durnel          : solved-ish (~87%)
molvic          : best rule consistent with every observation so far
garrow / norvel / tovel : not cracked -> echo when the count is 0 (always right),
                  otherwise SKIP (instant, keeps the round moving, protects the
                  fewer-answers tiebreak).
"""
import solvers
import molvic_family


def _n(name, clue):
    try:
        if name == 'garrow':
            return int(clue.split('\n', 1)[0].split()[1])
        return int(clue.rsplit('\n', 1)[1].split()[0])
    except Exception:
        return -1


def on_round_start(memory):
    memory['r'] = memory.get('r', 0) + 1


def solve(name, clue, memory):
    try:
        n = _n(name, clue)
        if n == 0:
            return clue
        if n < 0:
            return None
        if name == 'basten':
            return solvers.basten(clue)
        if name == 'kelmar':
            return solvers.kelmar(clue, 0)
        if name == 'durnel':
            return solvers.durnel(clue, 0)
        if name == 'molvic':
            return molvic_family.item_driven(clue, 'rcm', 'first')
    except Exception:
        return None
    return None


def on_round_end(items, memory):
    pass
