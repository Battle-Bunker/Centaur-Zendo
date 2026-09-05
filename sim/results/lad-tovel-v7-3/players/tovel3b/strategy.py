"""Centaur Zendo — final strategy.

Every clue is a picture plus a trailing line "N verb".  N is exactly the number
of *eligible objects* in the picture and the answer is the picture with the verb
applied to all of them; N == 0 always means "answer == the clue unchanged".

  tovel  "bump"   an appointment with neighbours on both sides is pushed to the
                  next free day, leaving '>' behind          (confirmed 87/87)
  basten "nibble" a fish whose weed reaches its own row swims up to the weed and
                  eats the top segment                       (confirmed 69/69)
  molvic "home"   a shelf with a gap pulls its nearest stray item home (partial)
  felsim "tip"    a cup with one support and nothing on top tips off (guess)
  durnel / kelmar / norvel : unsolved -> skip unless N == 0 (skips are instant
                  and do not count against the fewer-answers tiebreak).
"""

import solvers

SOLVED = ("tovel", "basten", "molvic", "felsim")


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def solve(name, clue, memory):
    try:
        if clue.rsplit("\n", 1)[-1].split()[0] == "0":
            return clue
    except Exception:
        return clue
    if name not in SOLVED:
        return None
    try:
        return getattr(solvers, name)(clue)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
