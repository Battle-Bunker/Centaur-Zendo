"""strategy.py — THE ONE FILE YOU EDIT.

You get a challenge `name` (like "PP" or "Z7"), a `clue` (a string), and a
`memory` dict that is saved to memory.json and handed back to you next round.
Return a string.  If your string is what that challenge wanted, you score 1.

    solve(name, clue, memory) -> str        <- required
    on_round_start(memory)                  <- optional, called before a round
    on_round_end(items, memory)             <- optional, called after a round

Nobody tells you what a challenge means.  You find out the way scientists do:
guess, look at the 0/1 scores in logs/, guess better.

>>> HOW TO PLAY WITH YOUR AI ASSISTANT <<<
1. Run a round with this file as-is.  It answers randomly and remembers
   everything.  You will score almost nothing.  That is the plan.
2. Open logs/summary.txt and logs/round_1.txt.
3. Paste them to your AI assistant and ask:
      "Here are clue/answer/score examples from a challenge called X.
       What rule could the clue for X be asking for?  Give me three
       hypotheses and a tiny Python function for the most likely one."
4. Add that function below, run another round, and see if X's hit-rate moves.
5. Keep it FAST: a round is one second long and the next challenge arrives the
   instant you answer.  Slow guesses cost you challenges.  When you have no
   idea, return "" quickly instead of thinking hard.
"""

import random
import string

# A few short words to throw at the wall.  Random answers are not a joke: they
# are how you collect clue/score pairs for the first round.
WORDS = ["a", "the", "cat", "sum", "yes", "no", "one", "two", "red", "zendo"]

MAX_EXAMPLES_PER_NAME = 40   # keep memory.json small enough to paste to an AI


def on_round_start(memory):
    """Called once before the round starts.  Do slow setup HERE, not in solve.

    (Precompute tables, load caches from `memory`, compile regexes...  Anything
    you do here is free; anything you do in solve() costs you challenges.)
    """
    memory.setdefault("rounds_played", 0)
    memory.setdefault("examples", {})     # name -> [{clue, answer, score}, ...]
    memory["rounds_played"] += 1


# Return None to SKIP a challenge (instant, counts as neither answered nor wrong;
# skipping helps the fewer-answers tiebreak). memory["_index"] holds the position of
# the current challenge within the round, handy for cycling through candidate formats.
def solve(name, clue, memory):
    """Return your answer for one challenge, as a string.  Be quick.

    This default is "round zero" behaviour: answer something random and short so
    that every challenge produces a data point.  Replace the guessing with real
    solvers as you work each challenge class out, e.g.:

        if name == "XX":
            return my_fast_xx_solver(clue)
    """
    # Once you know a challenge, answer it here and return early:
    #
    #   if name == "SOMENAME":
    #       try:
    #           return solve_somename(clue)
    #       except Exception:
    #           return ""          # never crash, never stall
    #
    r = random.Random()
    return r.choice([
        str(r.randrange(0, 100)),                                # a small number
        "".join(r.choice(string.ascii_lowercase) for _ in range(r.randint(1, 5))),
        r.choice(WORDS),
        "0",
        "1",
        clue,                        # sometimes the clue itself is the answer
        clue[::-1],                  # ...or the clue backwards
    ])


def on_round_end(items, memory):
    """Called after the round with every item the server showed you.

    Each item is {index, name, clue, solution, score}.  We stash a few examples
    per challenge name so that next round (and your AI assistant) can see what
    has already been tried.  logs/round_<n>.txt has the same data, prettier.
    """
    examples = memory.setdefault("examples", {})
    for it in items:
        bucket = examples.setdefault(it.get("name", "?"), [])
        bucket.append({"clue": it.get("clue"),
                       "answer": it.get("solution"),
                       "score": it.get("score")})
        if len(bucket) > MAX_EXAMPLES_PER_NAME:      # trim, but never lose a hit
            hits = [e for e in bucket if e.get("score")]
            recent = bucket[-MAX_EXAMPLES_PER_NAME:]
            examples[it.get("name", "?")] = [e for e in hits
                                             if e not in recent] + recent
