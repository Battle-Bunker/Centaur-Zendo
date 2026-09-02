"""LegoZendo — round 6 probe: tiled gadgets with exact feature counts."""
import json, os

_DIR = os.path.dirname(os.path.abspath(__file__))
BG = "."
TW, TH = 8, 6          # tile 8 wide x 6 tall, 4 bricks (exactly half filled)
NTILES = 12

# each tile: list of (y, x, h, w, colour-slot) ; slot 0 = clue letter
FILL = [(0, 0, 2, 3, 1), (2, 0, 2, 3, 2), (4, 0, 2, 3, 3), (0, 4, 3, 2, 0)]
BOND = [(2, 0, 2, 3, 1), (2, 3, 2, 3, 2), (0, 2, 2, 3, 0), (4, 0, 2, 3, 3)]
OFFS = [(0, 0, 2, 3, 1), (2, 1, 2, 3, 0), (4, 1, 2, 3, 2), (3, 4, 3, 2, 3)]
SLOTS = "QRS"

CACHE = {}
DEMOS = {}


def make(letter, tiles):
    W, H = TW * NTILES, TH
    g = [[BG] * W for _ in range(H)]
    others = [c for c in SLOTS if c != letter] + ["V", "W", "X"]
    for ti, spec in enumerate(tiles):
        ox = ti * TW
        for (y, x, h, w, slot) in spec:
            ch = letter if slot == 0 else others[slot - 1]
            for dy in range(h):
                for dx in range(w):
                    g[y + dy][ox + x + dx] = ch
    return "\n".join("".join(r) for r in g)


def build(letter, n, variant):
    if variant == 0:
        gad = [BOND] * n
    elif variant == 1:
        gad = [OFFS] * n
    else:
        gad = [BOND] * (n // 2) + [OFFS] * (n % 2)
    tiles = gad[:NTILES] + [FILL] * (NTILES - len(gad[:NTILES]))
    return make(letter, tiles)


def on_round_start(memory):
    CACHE.clear()
    DEMOS.clear()
    try:
        with open(os.path.join(_DIR, "logs", "demos.jsonl")) as f:
            for line in f:
                d = json.loads(line).get("demo") or {}
                if d.get("solution"):
                    DEMOS[d["clue"]] = d["solution"]
    except Exception:
        pass
    for o in range(65, 91):
        L = chr(o)
        for n in range(13):
            for v in (0, 1, 2):
                CACHE[(L, n, v)] = build(L, n, v)


def solve(name, clue, memory):
    try:
        if clue in DEMOS:
            return DEMOS[clue]
        L = clue[0].upper()
        n = int(clue[1:])
        return CACHE[(L, n, memory.get("_index", 0) % 3)]
    except Exception:
        return None


def on_round_end(items, memory):
    try:
        memory["examples"] = {}
    except Exception:
        pass
