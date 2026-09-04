"""strategy.py -- Centaur Zendo, challenge class "tovel".

Clue format observed: "D1/D2/L/D4/D5"
  D1  = days in the month   (28..31)
  D2  = weekday index (0=Mo) that day 1 falls on
  L   = a single letter (A-Z)
  D4  = small int (2..6)
  D5  = int (1..27)

The one demo we have shows the correct solution is a text calendar:

 Mo  Tu  We  Th  Fr  Sa  Su
         1F  2F  3F  4W  5E
 6W  7F  8W  9F 10E 11F 12Y
13F 14W 15F 16E 17F 18F 19Y
20F 21W 22F 23Y 24F 25E 26A
27F 28A 29F 30W

-- a Monday-first week header, each day right-justified in a 3-char cell as
"<day><letter>", cells separated by a single space, no padding after the
last real day of the final row.  We are confident of the header/grid
skeleton; the per-day LETTER rule is still being reverse engineered from
demos across rounds (see NOTES.md).
"""

import time

WEEKDAY_HEADER = " Mo  Tu  We  Th  Fr  Sa  Su"


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory.setdefault("examples", {})
    memory["rounds_played"] += 1
    # index -> which letter-hypothesis to try this round, for experimentation
    memory.setdefault("hyp_hits", {})


def parse_clue(clue):
    parts = clue.split("/")
    if len(parts) != 5:
        return None
    d1, d2, letter, d4, d5 = parts
    return int(d1), int(d2), letter, int(d4), int(d5)


def weekday(day, start):
    return (day - 1 + start) % 7


def build_grid(days_in_month, start, letter_fn):
    """letter_fn(day, wd, week) -> single-char string"""
    rows = []
    row = []
    # leading blanks for the first (partial) week
    row.extend(["   "] * start)
    for day in range(1, days_in_month + 1):
        wd = weekday(day, start)
        wk = (day - 1 + start) // 7
        L = letter_fn(day, wd, wk)
        cell = f"{day}{L}"
        row.append(f"{cell:>3}")
        if wd == 6:  # Sunday -> end of row
            rows.append(" ".join(row))
            row = []
    if row:
        rows.append(" ".join(row))
    return WEEKDAY_HEADER + "\n" + "\n".join(rows)


# --- letter hypotheses -----------------------------------------------------
def letter_default(letter):
    def f(day, wd, wk):
        return letter
    return f


HYPOTHESES = ["default"]


def solve(name, clue, memory):
    if name != "tovel":
        return None
    try:
        deadline = time.perf_counter() + 0.010
        parsed = parse_clue(clue)
        if parsed is None:
            return None
        d1, d2, letter, d4, d5 = parsed
        cache = memory.setdefault("grid_cache", {})
        if clue in cache:
            return cache[clue]
        if time.perf_counter() > deadline:
            return ""
        answer = build_grid(d1, d2, letter_default(letter))
        if len(cache) < 200:
            cache[clue] = answer
        return answer
    except Exception:
        return ""


def on_round_end(items, memory):
    examples = memory.setdefault("examples", {})
    for it in items:
        bucket = examples.setdefault(it.get("name", "?"), [])
        bucket.append({"clue": it.get("clue"),
                       "answer": it.get("solution"),
                       "score": it.get("score")})
        if len(bucket) > 40:
            hits = [e for e in bucket if e.get("score")]
            recent = bucket[-40:]
            examples[it.get("name", "?")] = [e for e in hits if e not in recent] + recent
