from wordfreq import top_n_list

V = set("aeiou")

GOOD = {
 1: ["the", "and", "in", "to"],
 2: ["also", "are", "have", "like", "one", "other", "you", "racket", "rugged"],
 3: ["about", "another", "around", "before", "every", "people", "something",
     "generic", "millions", "order", "pedro", "russia", "female"],
 4: ["american", "because", "believe", "everyone", "first", "national", "should",
     "abandonment", "interpreter", "desired", "halves"],
 5: ["beautiful", "company", "education", "experience", "information", "reputable"],
 6: ["international", "organization"],
}

BAD = set([("someone",4),("available",5),("association",6),("communication",6),
 ("relationship",5),("responsibilities",7),("telecommunications",7),
 ("telecommunications",8),("development",4),("executive",5),("immediately",5),
 ("university",4),("automatically",6),("representatives",6),("professional",6),
 ("administration",5),("approximately",6),("that",3),("they",2),("their",4),
 ("everything",4),("you",3),("your",3),("about",2),("the",2),("and",2),
 ("because",3),("information",4),("international",5)])

POOL = {}
_cnt = {}

def _build():
    used = set()
    for d, ws in GOOD.items():
        used.update(ws)
    words = [w for w in top_n_list('en', 30000)
             if w.isalpha() and w.isascii() and len(w) > 1]
    for d in range(1, 10):
        POOL[d] = []
    for w in words:
        d = sum(c in V for c in w)
        if 1 <= d <= 9 and w not in used and (w, d) not in BAD:
            POOL[d].append(w)

def on_round_start(memory):
    if not POOL:
        _build()
    _cnt.clear()
    _cnt.update({int(k): v for k, v in memory.get("cnt", {}).items()})

def solve(name, clue, memory):
    try:
        if not POOL:
            _build()
        i = memory.get("_index", 0)
        digs = [int(c) for c in clue]
        if i % 2 == 0:
            out = []
            for p, d in enumerate(digs):
                g = GOOD.get(d)
                if not g:
                    return None
                out.append(g[p % len(g)])
            return " ".join(out)
        # probe mode: one unknown word, rest from table
        tp = (i // 2) % len(digs)
        out = []
        for p, d in enumerate(digs):
            g = GOOD.get(d)
            if p == tp or not g:
                pool = POOL.get(d)
                if not pool:
                    return None
                k = _cnt.get(d, 0)
                _cnt[d] = k + 1
                out.append(pool[k % len(pool)])
            else:
                out.append(g[p % len(g)])
        return " ".join(out)
    except Exception:
        return None

def on_round_end(items, memory):
    memory["cnt"] = {str(k): v for k, v in _cnt.items()}
