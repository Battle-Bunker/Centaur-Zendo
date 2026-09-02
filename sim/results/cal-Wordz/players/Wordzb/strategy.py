# Wordz: solution = one word per clue digit.
#   odd  position (1st,3rd,5th...) -> word must have exactly d VOWELS (aeiou)
#   even position (2nd,4th,6th...) -> word must have exactly d CONSONANTS
# Only words in the server's lexicon count, so we use words confirmed by
# previously-scoring answers.

VOW = {1: "ron", 2: "toon", 3: "tenure", 4: "aileen", 5: "innovative",
       6: "simplification", 7: "denominational"}
CON = {2: "sec", 3: "chow", 4: "bulky", 5: "twenty", 6: "lyricist",
       7: "husbandry", 8: "thoughtless"}

# untested candidates for the two gaps (cycled so the logs reveal which work)
C1 = ["one", "area", "idea", "audio", "auto", "ohio", "iowa", "aloe", "ionia", "aurora"]
C9 = ["constructing", "strengthens", "abstractness", "handcrafted", "spendthrift",
      "brandywine", "grandchildren", "switchblade", "thunderstorms", "blacksmiths"]


def on_round_start(memory):
    pass


def solve(name, clue, memory):
    try:
        i = memory.get("_index", 0)
        out = []
        for p, ch in enumerate(clue):
            d = ord(ch) - 48
            if p & 1:
                w = CON.get(d)
                if w is None:
                    if d == 1:
                        w = C1[i % len(C1)]
                    elif d == 9:
                        w = C9[i % len(C9)]
                    else:
                        return None
            else:
                w = VOW.get(d)
                if w is None:
                    return None
            out.append(w)
        return " ".join(out)
    except Exception:
        return None


def on_round_end(items, memory):
    pass
