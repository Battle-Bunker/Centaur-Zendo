import random, math

_rand = random.random
CH = '-|/'

WA = {'--': -8.148, '-|': 6.239, '-/': -8.950,
      '|-': -5.161, '||': -8.200, '|/': 12.897,
      '/-': 3.071,  '/|': 1.809,  '//': 5.292}
WB = {'--': -10.143, '-|': 6.848, '-/': -10.813,
      '|-': -1.106,  '||': -9.425, '|/': 11.034,
      '/-': 2.555,   '/|': 4.216,  '//': 6.836}
BETA = 0.12
TA = dict((k, math.exp(BETA * v)) for k, v in WA.items())
TB = dict((k, math.exp(BETA * v)) for k, v in WB.items())
K = 16


def on_round_start(memory):
    memory["rounds_played"] = memory.get("rounds_played", 0) + 1


def _run(clue, W, T, K):
    nm = clue.count('-') - 1
    nb = clue.count('|')
    ns = clue.count('/') - 1
    if nm < 0 or ns < 0:
        return None
    if nm + nb + ns == 0:
        return '/-'
    best = None
    bs = -1e18
    for _ in range(K):
        cnt = {'-': nm, '|': nb, '/': ns}
        opts = [(c, cnt[c]) for c in '-/' if cnt[c] > 0]
        if not opts:
            return '/' + '|' * nb + '-'
        tot = 0.0
        for _c, v in opts:
            tot += v
        r = _rand() * tot
        b = opts[-1][0]
        for c, v in opts:
            r -= v
            if r <= 0:
                b = c
                break
        cnt[b] -= 1
        n = cnt['-'] + cnt['|'] + cnt['/']
        prev = '/'
        out = []
        sc = 0.0
        for step in range(n):
            ws = []
            tot = 0.0
            last = (step == n - 1)
            for c in CH:
                k = cnt[c]
                if k > 0:
                    if step == 0 and c == '-' and (cnt['|'] or cnt['/']):
                        continue
                    v = k * T[prev + c]
                    if last:
                        v *= T[c + b]
                    ws.append((c, v))
                    tot += v
            if tot <= 0.0:
                break
            r = _rand() * tot
            c = ws[-1][0]
            for cc, v in ws:
                r -= v
                if r <= 0:
                    c = cc
                    break
            out.append(c)
            sc += W[prev + c]
            cnt[c] -= 1
            prev = c
        sc += W[prev + b] + W[b + '-']
        if sc > bs:
            bs = sc
            best = '/' + ''.join(out) + b + '-'
    return best


def solve(name, clue, memory):
    try:
        return _run(clue, WB, TB, K)
    except Exception:
        return None


def on_round_end(items, memory):
    memory["last"] = [len(items), sum(it.get("score", 0) for it in items)]
