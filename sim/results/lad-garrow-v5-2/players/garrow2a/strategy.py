"""FINAL strategy.

Cracked:
  virel  - prepend a row of boxes tiling the same width whose box spans coincide
           with EXACTLY N spans of the clue's top row.        (100% in rounds 3+4)
  durnel - a cart rolls onto the first pit ahead of it, filling it and reversing;
           pits are resolved right-to-left, the cart approaching from the left has
           priority, an empty cart (no cargo tower) blocks its pit, and a cart
           cannot pass under a '###' bridge lower than its cargo.   (~25-40%)
  molvic - fill the first empty shelf slot with that shelf's own stock found
           elsewhere; repeat N times.                     (reliable at N<=1)
Unsolved (answer only the free N==0 cases, skip the rest for speed/precision):
  garrow, fennick, tovel, norvel
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib

TOK = lib.TOK
IDENTITY_ONLY = ("garrow", "fennick", "tovel", "norvel")


# ---------------- virel ----------------
def _spans(sizes):
    out = []; p = 0
    for s in sizes:
        out.append((p, s + 2)); p += s + 2
    return out


def virel(clue):
    L = clue.split("\n")
    n = int(L[-1].strip())
    W = len(L[0])
    top = set(_spans([len(x) for x in re.findall(r"\[(-*)\]", L[0])]))
    memo = {}

    def rec(p, k):
        if p == W:
            return [] if k == 0 else None
        key = (p, k)
        if key in memo:
            return memo[key]
        memo[key] = None
        for w in (2, 3, 4, 5, 6):
            if p + w > W:
                break
            mk = 1 if (p, w) in top else 0
            if mk > k:
                continue
            sub = rec(p + w, k - mk)
            if sub is not None:
                memo[key] = [w] + sub
                return memo[key]
        return memo[key]

    r = rec(0, n)
    if r is None:
        row = "[]" * (W // 2) if W % 2 == 0 else "[-]" + "[]" * ((W - 3) // 2)
    else:
        row = "".join("[" + "-" * (w - 2) + "]" for w in r)
    return row + "\n" + "\n".join(L[:-1])


# ---------------- durnel ----------------
def durnel(clue):
    L, sky, ground, carts, pits, n, W = lib.durnel_parse(clue)
    if n == 0:
        return clue
    rows = len(sky)

    def clear(c, p):
        a, b = (c["pos"] + 3, p) if c["pos"] < p else (p + 3, c["pos"])
        if not all(ch == "." for ch in ground[a:b]):
            return False
        if c["h"]:
            lo = min(c["pos"], p); hi = max(c["pos"], p) + 3
            for k in range(c["h"]):
                if "#" in sky[rows - 1 - k][lo:hi]:
                    return False
        return True

    for _ in range(n):
        chosen = None
        for p in reversed(pits):
            lf = rt = None
            for c in carts:
                if c["pos"] < p and c["dir"] == ">" and clear(c, p):
                    lf = c
                if c["pos"] > p and c["dir"] == "<" and rt is None and clear(c, p):
                    rt = c
            pick = lf if lf is not None else rt
            if pick is None or pick["h"] == 0:
                continue
            chosen = (p, pick); break
        if chosen is None:
            break
        p, c = chosen
        ground = lib.durnel_move(sky, ground, c, p)
        pits.remove(p)
    return lib.durnel_render(L, sky, ground)


# ---------------- molvic ----------------
def molvic(clue):
    L, sh, n = lib.molvic_parse(clue)
    if n == 0:
        return clue
    R = len(sh); C = len(sh[0][2])
    for _ in range(n):
        moved = False
        for k in range(R):
            row = sh[k][2]; want = sh[k][1]
            for ci in range(C):
                if row[ci] != "___":
                    continue
                src = None
                for a in range(R):
                    if a == k:
                        continue
                    cells = sh[a][2]
                    if sh[a][1] == want:
                        continue
                    for b in range(C):
                        if cells[b] == want:
                            src = (a, b); break
                    if src:
                        break
                if src:
                    row[ci] = want
                    sh[src[0]][2][src[1]] = "___"
                    moved = True
                    break
            if moved:
                break
        if not moved:
            break
    return lib.molvic_render(L, sh)


def on_round_start(memory):
    memory["_n"] = memory.get("_n", 0) + 1


def solve(name, clue, memory):
    try:
        if name == "virel":
            return virel(clue)
        if name == "durnel":
            return durnel(clue)
        if name == "molvic":
            return molvic(clue)
        # unsolved classes: take the free "0 <verb>" cases, skip everything else
        if name == "garrow":
            return clue if clue[:12].split()[1] == "0" else None
        last = clue[-12:].rsplit("\n", 1)[-1]
        return clue if last[:1] == "0" else None
    except Exception:
        return None


def on_round_end(items, memory):
    pass
