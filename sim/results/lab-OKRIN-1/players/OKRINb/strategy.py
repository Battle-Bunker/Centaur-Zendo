"""OKRIN final strategy.

Rule discovered:
  * letter counts: the k-th alphabetically-smallest clue letter must appear k+2 times
  * the answer is a Toeplitz grid  g[r][c] = clue[(c-r) % n]  with cells masked to a
    fill char, filled greedily row-major until every letter's quota is met
  * which grid WIDTH (mod n) is accepted depends on the clue's rank-permutation;
    GOOD/BAD tables below are learned from round 6 (226 labelled answers).
"""

GOOD = {'42310': 2, '501234': 1, '3120': 1, '3021': 1, '3201': 1, '501243': 1, '43120': 1, '42103': 1, '43201': 1, '3012': 1, '40312': 1, '520431': 2, '513420': 1, '43021': 1, '543021': 4, '521034': 1, '542031': 4, '514302': 1, '40231': 1, '502431': 4, '3210': 1, '542310': 4, '521430': 2, '40132': 3, '512430': 4, '510432': 4, '530214': 1, '43210': 1, '532104': 2, '40321': 1, '42013': 2, '501342': 1, '3102': 1, '41320': 3, '532014': 1, '531042': 1, '40123': 1, '43012': 1, '41032': 1, '520134': 2, '41203': 1, '520143': 4, '510342': 4, '541023': 4, '43102': 1, '541032': 1, '41023': 1, '531024': 1, '512043': 2, '504321': 1}
BAD = {'513042': [2], '542130': [1, 4], '531402': [4], '512340': [1], '502341': [4], '42130': [1, 2, 3], '510423': [2, 4], '41302': [2, 3], '503214': [1], '40213': [1, 2], '523410': [1, 4], '521403': [1, 2], '534021': [4], '42031': [2], '523140': [1, 2, 4], '504123': [4], '42301': [2, 3], '513240': [4], '502314': [1], '532140': [1], '523104': [4], '503124': [2], '512403': [4], '530241': [2], '540213': [1], '534120': [4], '520314': [2], '530412': [1], '514023': [4], '540231': [4], '502134': [4], '540312': [4], '532410': [4], '41230': [1], '501423': [2], '513402': [4], '512034': [4], '524130': [4], '520413': [1, 4], '503241': [4], '501324': [2]}
PRIO = {3: (1, 2, 0), 4: (1, 3, 0, 2), 5: (1, 4, 2, 3, 0)}
FILL = "."

def on_round_start(memory):
    memory["r"] = memory.get("r", 0) + 1

def solve(name, clue, memory):
    try:
        n = len(clue)
        if n < 2:
            return None
        srt = sorted(clue)
        perm = [srt.index(ch) for ch in clue]
        key = str(n) + "".join(map(str, perm))
        r = GOOD.get(key)
        if r is None:
            prio = PRIO.get(n) or tuple(range(n))
            bad = BAD.get(key)
            r = prio[0]
            if bad:
                for cand in prio:
                    if cand not in bad:
                        r = cand
                        break
        base = 2 * n - 1
        W = base + ((r - base) % n)
        if W < n:
            W += n
        need = [p + 2 for p in perm]
        left = sum(need)
        rows = []
        row_i = 0
        while left > 0 and row_i < 40:
            out = []
            for c in range(W):
                i = (c - row_i) % n
                if need[i] > 0:
                    need[i] -= 1
                    left -= 1
                    out.append(clue[i])
                else:
                    out.append(FILL)
            rows.append("".join(out))
            row_i += 1
        return "\n".join(rows)
    except Exception:
        return None
