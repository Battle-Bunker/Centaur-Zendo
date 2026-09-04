"""garrow — fence the field into pens.

Clue: "L1n1L2n2" + a walled field of two-wide animals (tt, oo, ...).
Answer: the same grid with vertical fences '|' inserted at the same column
gaps in every row.  An animal counts for every pen it touches.  Accepted iff
  * exactly n pens hold 2+ animals of L, for each (L,n) in the header
  * there are 4..8 pens
  * no pen is empty
"""
import garrow_core as G


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1
    G.solve("a1b1\n####\n#aa#\n#bb#\n#aa#\n#bb#\n####")   # warm the regex cache


def solve(name, clue, memory):
    try:
        return G.solve(clue, 3) or G.solve(clue, 2) or G.solve(clue, 1)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
