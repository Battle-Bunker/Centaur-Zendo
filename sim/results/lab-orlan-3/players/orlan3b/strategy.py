"""strategy.py — class `orlan` (the only class in this pool).

The clue is a grid of '.', '#', 'o', 'x'.  A correct answer is a string
"r1,c1>r2,c2": move the 'o' at (r1,c1) onto an empty '.' at (r2,c2) lying in the
same row or the same column.  Which of the ~20 such moves the server wants is
scored by a small conditional-logit model fitted to every correct answer we
collected in training (best measured live hit-rate: ~10%, vs ~4% for a random
legal move).

Everything is guarded; a bad clue returns None (an instant skip).
"""

# feature order: tnearx, snearo, tedge, t_near_edge, trow_o_b, s_edge_line,
#                trow_w, tcol_x
WV = [-0.6116, -0.78, 1.1465, -1.0786, 2.4792, -0.5103, 0.5605, 0.8931]
NF = 8


def on_round_start(memory):
    memory.setdefault("rounds_played", 0)
    memory["rounds_played"] += 1


def solve(name, clue, memory):
    try:
        g = clue.split("\n")
        while g and g[-1] == "":
            g.pop()
        nr = len(g)
        nc = len(g[0])
        Ol = []
        Xl = []
        El = []
        for r in range(nr):
            row = g[r]
            for c in range(nc):
                ch = row[c]
                if ch == "o":
                    Ol.append((r, c))
                elif ch == "x":
                    Xl.append((r, c))
                elif ch == ".":
                    El.append((r, c))
        if not Ol or not El:
            return None
        cands = []
        for s in Ol:
            sr = s[0]
            sc = s[1]
            for t in El:
                if sr == t[0] or sc == t[1]:
                    cands.append((s, t))
        if not cands:
            return None
        if len(cands) == 1:
            s, t = cands[0]
            return "%d,%d>%d,%d" % (s[0], s[1], t[0], t[1])
        rowo = [row.count("o") for row in g]
        roww = [row.count("#") for row in g]
        colx = [0] * nc
        for p in Xl:
            colx[p[1]] += 1
        feats = []
        for (s, t) in cands:
            sr, sc = s
            tr, tc = t
            tn = 99
            for (ar, ac) in Xl:
                d = abs(tr - ar) + abs(tc - ac)
                if d < tn:
                    tn = d
            sn = abs(sr - tr) + abs(sc - tc)
            for (ar, ac) in Ol:
                if ar == sr and ac == sc:
                    continue
                d = abs(sr - ar) + abs(sc - ac)
                if d < sn:
                    sn = d
            tne = tr
            if nr - 1 - tr < tne:
                tne = nr - 1 - tr
            if tc < tne:
                tne = tc
            if nc - 1 - tc < tne:
                tne = nc - 1 - tc
            if sr == tr:
                a = sc
                ln = nc
            else:
                a = sr
                ln = nr
            feats.append([tn, sn,
                          1 if (tr == 0 or tr == nr - 1 or tc == 0 or tc == nc - 1) else 0,
                          tne, rowo[tr],
                          1 if (a == 0 or a == ln - 1) else 0,
                          roww[tr], colx[tc]])
        n = len(feats)
        mns = [0.0] * NF
        sds = [1.0] * NF
        for j in range(NF):
            m = 0.0
            for f in feats:
                m += f[j]
            m /= n
            v = 0.0
            for f in feats:
                d = f[j] - m
                v += d * d
            v = (v / n) ** 0.5
            mns[j] = m
            sds[j] = v if v else 1.0
        best_i = 0
        best_s = None
        for i in range(n):
            f = feats[i]
            sc_ = 0.0
            for j in range(NF):
                sc_ += WV[j] * (f[j] - mns[j]) / sds[j]
            if best_s is None or sc_ > best_s:
                best_s = sc_
                best_i = i
        s, t = cands[best_i]
        return "%d,%d>%d,%d" % (s[0], s[1], t[0], t[1])
    except Exception:
        return None


def on_round_end(items, memory):
    pass
