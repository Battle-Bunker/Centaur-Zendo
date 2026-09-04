#!/usr/bin/env python3
"""The Ladder: persistent state + scheduler for the indefinite challenge-balancing loop.

  python ladder/ladder.py status                 ladder table + job queue (recomputed)
  python ladder/ladder.py launch <job-id>        mark a job running; for player jobs set up the arena and print briefs
  python ladder/ladder.py ingest <run>           read sim/results/<run>/ (events + meta) into state
  python ladder/ladder.py record-qual <class> '<json>'   store a judge's rubric scores
  python ladder/ladder.py add-version <class> <path> [note]   register a new version file (designer/refiner output)
  python ladder/ladder.py arena <class> [k]      set up an arena for the class's current version
  python ladder/ladder.py fail <job-id>          job failed/interrupted -> pending again
  python ladder/ladder.py done <job-id>          mark a non-player job done
  python ladder/ladder.py report                 regenerate ladder/REPORT.md
  python ladder/ladder.py retire <class>         manual status
All mutations rewrite ladder/state.json; commit after every step.
"""
import json, sys, os, glob, subprocess, collections, time, shutil, secrets
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "ladder" / "state.json"
SCRATCH = Path(os.environ.get("ZENDO_SCRATCH", "/tmp/claude-0/-home-user-Centaur-Zendo/7b495634-616e-5f1b-9d7a-c4523ae5e261/scratchpad"))
CADENCE = "4x0.5s/5s/3s/7cls/3demos"   # the format under which balance is measured (older runs are kept as history)
POOL_SIZE = 7
DIRECTIONS = ["toys and building", "playground and table games", "time and place", "wordplay (use words module)",
              "crafts and physical intuition", "school and home life", "food and the kitchen", "animals and nature",
              "clothes, dressing and packing", "music, rhythm and dance", "sport and scoring", "weather and seasons",
              "transport, maps and journeys", "shops, money and swapping"]


def load():
    return json.loads(STATE.read_text())


def save(s):
    STATE.write_text(json.dumps(s, indent=1, sort_keys=True))


def cur_file(c):
    return c["versions"][c["current_version"] - 1]["file"]


# ------------------------------------------------------------------ metrics
def finals(c, version=None, cadence=CADENCE):
    """Player finals on this class (current cadence only unless cadence=None)."""
    out = []
    for r in c.get("runs", []):
        if version is not None and r["version"] != version: continue
        if cadence is not None and r.get("cadence") != cadence: continue
        for p in r["players"]:
            if p.get("final_presented"): out.append(p)
    return out


def demo_split(c, version=None):
    """(mean rate with a demo, n, mean rate without, n) over current-cadence finals."""
    F = finals(c, version)
    w = [p["final_rate"] for p in F if p.get("demo")]
    wo = [p["final_rate"] for p in F if p.get("demo") is False]
    return ((sum(w) / len(w)) if w else None, len(w), (sum(wo) / len(wo)) if wo else None, len(wo))


def classify(c):
    if c["status"] in ("retired", "too_easy_textbook"): return c["status"]
    v = c["current_version"]
    if any(ver.get("untested_arena") for ver in c["versions"][v - 1:v]): pass
    F = finals(c, v)
    if not F: return "untested" if not c.get("runs") else "testing"
    m = sum(p["final_rate"] for p in F) / len(F)
    profiles = {p.get("profile", "?") for p in F}
    if len(F) >= 3 and m > 0.8: return "too_easy"
    if len(F) >= 4 and m < 0.15: return "too_hard"
    if len(F) >= 4 and 0.3 <= m <= 0.7 and len(profiles) >= 2: return "calibrated"
    return "testing"


def mean_rate(c, version=None):
    F = finals(c, version)
    return (sum(p["final_rate"] for p in F) / len(F)) if F else None


def qual_score(c):
    q = [x for x in c.get("qual", []) if x.get("version") == c["current_version"]]
    return (sum(x["score"] for x in q) / len(q)) if q else None


# ------------------------------------------------------------------ queue
def plan(s):
    """Return the ordered list of jobs that should exist (creates missing ones as pending)."""
    jobs = s["jobs"]
    existing = {(j["kind"], j["class"], j.get("version")) for j in jobs if j["status"] in ("pending", "running")}
    def add(kind, cls, version=None, agents=1, **kw):
        key = (kind, cls, version)
        if key in existing: return
        existing.add(key)
        jobs.append({"id": f"{kind}-{cls}-v{version or 0}-{secrets.token_hex(2)}", "kind": kind, "class": cls,
                     "version": version, "status": "pending", "agents": agents, **kw})
    classes = s["classes"]
    # 1. untested current versions, then classes with the fewest finals (testing)
    order = []
    for n, c in classes.items():
        st = classify(c)
        c["status"] = st
        if st in ("retired", "too_easy_textbook"): continue
        v = c["current_version"]
        nf = len(finals(c, v))
        if st == "untested": order.append((0, nf, n))
        elif st == "testing": order.append((1, nf, n))
    for _, _, n in sorted(order):
        add("players", n, classes[n]["current_version"], agents=2)
    # 2. refine too_easy / too_hard (once per version)
    for n, c in classes.items():
        if c["status"] in ("too_easy", "too_hard") and c["current_version"] not in c.get("refined_versions", []):
            add("refiner", n, c["current_version"], agents=1)
    # 2b. re-skin refiners for classes that are balanced-ish but score badly with the kid judges
    for n, c in classes.items():
        q = qual_score(c)
        if q is not None and q < 3.5 and c["status"] not in ("retired", "too_easy_textbook") \
                and c["current_version"] not in c.get("refined_versions", []) and len(c["versions"]) < 2:
            add("refiner", n, c["current_version"], agents=1, reason="kid_score")
    # 3. judges for unjudged current versions (skip textbook)
    for n, c in classes.items():
        if c["status"] in ("retired", "too_easy_textbook"): continue
        if qual_score(c) is None:
            add("judge", n, c["current_version"], agents=1)
    # 4. designers when the candidate pipeline is short
    untested = sum(1 for c in classes.values() if c["status"] == "untested")
    designers_live = sum(1 for j in jobs if j["kind"] == "designer" and j["status"] in ("pending", "running"))
    if untested + designers_live < 2:
        used = s.setdefault("direction_cursor", 0)
        add("designer", f"new-{used}", None, agents=1, direction=DIRECTIONS[used % len(DIRECTIONS)])
        s["direction_cursor"] = used + 1
    rank = {"players": 0, "refiner": 1, "judge": 2, "designer": 3}
    pending = [j for j in jobs if j["status"] == "pending"]
    pending.sort(key=lambda j: (rank[j["kind"]], len(finals(classes[j["class"]])) if j["class"] in classes else 0))
    return pending


def running_agents(s):
    return sum(j["agents"] for j in s["jobs"] if j["status"] == "running")


# ------------------------------------------------------------------ commands
def cmd_status(a):
    s = load(); pending = plan(s); save(s)
    print(report_table(s))
    print(f"\nrunning agents: {running_agents(s)} / budget {s['budget']['max_agents']}")
    print("queue (pending, in priority order):")
    for j in pending[:12]:
        print(f"  {j['id']:<34} {j['kind']:<9} {j['class']:<12} agents={j['agents']} {j.get('direction','')}")
    for j in s["jobs"]:
        if j["status"] == "running": print(f"  RUNNING {j['id']} ({j['agents']} agents) run={j.get('run','')}")


def pick_profiles(s, c):
    used = collections.Counter(p.get("profile") for r in c.get("runs", []) for p in r["players"])
    # Opus profiles first; Sonnet profiles only once every Opus profile has played the class twice
    # (Sonnet players rarely discover that a scorer is a predicate, so their finals carry little signal).
    names = sorted(s["profiles"], key=lambda k: (used[k] + (s["profiles"][k]["model"] != "opus"),
                                                 s["profiles"][k]["model"] != "opus", k))
    return names[:2]


def pick_pool(s, target):
    """The target class plus POOL_SIZE-1 companions: live lab classes with the fewest finals on their
    current version (random tie-break), topped up from the textbook set if the lab is short."""
    import random as _r
    rng = _r.Random()
    classes = s["classes"]
    live = [n for n, c in classes.items() if n != target and c["status"] not in ("retired", "too_easy_textbook")
            and (REPO / cur_file(c)).exists()]
    live.sort(key=lambda n: (len(finals(classes[n], classes[n]["current_version"])), rng.random()))
    members = [target] + live[:POOL_SIZE - 1]
    if len(members) < POOL_SIZE:
        tb = [n for n, c in classes.items() if c["status"] == "too_easy_textbook" and (REPO / cur_file(c)).exists()]
        rng.shuffle(tb)
        members += tb[:POOL_SIZE - len(members)]
    return members


def cmd_launch(a):
    s = load(); jid = a[0]
    j = next(x for x in s["jobs"] if x["id"] == jid)
    if running_agents(s) + j["agents"] > s["budget"]["max_agents"]:
        sys.exit(f"budget exceeded: {running_agents(s)} running + {j['agents']}")
    j["status"] = "running"; j["started"] = time.time()
    if j["kind"] == "players":
        c = s["classes"][j["class"]]
        k = 1 + sum(1 for r in c.get("runs", []) if r["version"] == j["version"])
        run = f"lad-{j['class']}-v{j['version']}-{k}"
        profs = pick_profiles(s, c)
        teams = [f"{j['class']}{k}a", f"{j['class']}{k}b"]
        pool = SCRATCH / f"pool-{run}"; pool.mkdir(parents=True, exist_ok=True)
        members = pick_pool(s, j["class"])
        j["pool"] = {n: s["classes"][n]["current_version"] for n in members}
        for n in members:
            shutil.copy(REPO / cur_file(s["classes"][n]), pool / (n + ".json"))
        print("pool:", ", ".join(f"{n} v{v}" for n, v in j["pool"].items()))
        out = subprocess.run([sys.executable, str(REPO / "sim/arena.py"), "setup", "--run", run, "--teams", ",".join(teams),
                              "--challenge-dir", str(pool), "--arena-root", str(SCRATCH / run)], capture_output=True, text=True)
        if out.returncode: sys.exit(out.stderr)
        j["run"] = run; j["teams"] = dict(zip(teams, profs))
        tmpl = (REPO / "ladder/prompts/player.md").read_text()
        for t, p in j["teams"].items():
            prof = s["profiles"][p]
            brief = tmpl.replace("{TEAM_DIR}", str(SCRATCH / run / "players" / t)).replace("{PROFILE_BLOCK}", prof["priming"] + "\n" + prof.get("constraints", ""))
            (SCRATCH / run / f"BRIEF_{t}.md").write_text(brief)
            print(f"=== team {t}  profile={p}  model={prof['model']}  brief={SCRATCH / run / ('BRIEF_' + t + '.md')}")
    save(s); print("launched", jid)


def cmd_fail(a):
    s = load(); j = next(x for x in s["jobs"] if x["id"] == a[0]); j["status"] = "pending"; save(s); print("reset", a[0])


def cmd_done(a):
    s = load(); j = next(x for x in s["jobs"] if x["id"] == a[0]); j["status"] = "done"; save(s); print("done", a[0])


def run_cadence(meta):
    cfg = meta.get("config", {})
    demos = cfg.get("max_demos")
    return (f"{cfg.get('max_training_rounds')}x{cfg.get('round_seconds')}s/{cfg.get('cooldown_seconds'):g}s/"
            f"{cfg.get('final_seconds'):g}s/{meta.get('pool_size')}cls/{demos if demos is not None else 'win'}demos")


def parse_run(run):
    """Per team: overall rounds/final, demos by class, and per-class training/final tallies."""
    rd = REPO / "sim/results" / run
    meta = json.loads((rd / "meta.json").read_text())
    ev = rd / "events.jsonl"
    if not ev.exists(): ev = Path(meta["hidden"]) / "events.jsonl"
    def blank():
        return {"rounds": [], "demos": 0, "demo_names": [], "final_correct": 0, "final_presented": 0,
                "by_class": collections.defaultdict(lambda: {"rounds": [], "final_correct": 0, "final_items": 0})}
    per = collections.defaultdict(blank)
    names = set()
    for line in ev.read_text().splitlines():
        try: e = json.loads(line)
        except Exception: continue
        if e.get("dir") != "round": continue
        m = e["msg"]; t = e["team"]
        if m.get("event") == "demo":
            per[t]["demos"] += 1; per[t]["demo_names"].append(m.get("name")); continue
        if "presented" not in m: continue
        tally = collections.defaultdict(lambda: [0, 0])
        for it in m.get("items", []):
            names.add(it["name"]); tally[it["name"]][1] += 1; tally[it["name"]][0] += int(it.get("score") or 0)
        if m["kind"] == "final":
            per[t]["final_correct"] = m["correct"]; per[t]["final_presented"] = m["presented"]
            for n, (cc, pp) in tally.items():
                per[t]["by_class"][n]["final_correct"] = cc; per[t]["by_class"][n]["final_items"] = pp
        else:
            per[t]["rounds"].append([m["correct"], m["presented"]])
            for n in names:
                cc, pp = tally.get(n, [0, 0]); per[t]["by_class"][n]["rounds"].append([cc, pp])
    return meta, names, per


def cmd_ingest(a):
    s = load(); run = a[0]
    meta, names, per = parse_run(run)
    cadence = run_cadence(meta)
    job = next((j for j in s["jobs"] if j.get("run") == run), None)
    target = job["class"] if job else (next(iter(names)) if len(names) == 1 else a[1])
    pool = (job or {}).get("pool") or {n: s["classes"].get(n, {}).get("current_version", 1) for n in names}
    if target not in pool: pool[target] = (job or {}).get("version") or s["classes"][target]["current_version"]
    for cls, version in pool.items():
        c = s["classes"].setdefault(cls, {"status": "testing", "versions": [{"v": 1, "file": f"challenges/lab/{cls}.json"}],
                                          "current_version": 1, "runs": [], "qual": []})
        players = []
        for t, d in per.items():
            bc = d["by_class"].get(cls, {"rounds": [], "final_correct": 0, "final_items": 0})
            single = len(pool) == 1
            fc, fp = (d["final_correct"], d["final_presented"]) if single else (bc["final_correct"], bc["final_items"])
            rounds = d["rounds"] if single else bc["rounds"]
            fr = fc / fp if fp else None
            crack = next((i + 1 for i, (cc, pp) in enumerate(rounds) if pp and cc / pp >= 0.9), None)
            players.append({"team": t, "profile": (job or {}).get("teams", {}).get(t, "opus-default"),
                            "final_rate": fr, "final_correct": fc, "final_presented": fp,
                            "cracked_round": crack, "demos": d["demo_names"].count(cls) if not single else d["demos"],
                            "demo": d["demo_names"].count(cls) > 0 if d["demo_names"] or not single else None,
                            "rounds": rounds})
        c["runs"] = [r for r in c["runs"] if r["run"] != run] + [{"run": run, "version": version, "cadence": cadence,
                                                                  "pool": sorted(pool), "target": cls == target, "players": players}]
        c["status"] = classify(c)
        for p in players:
            print(f"{cls} v{version} {p['team']} ({p['profile']}): final={None if p['final_rate'] is None else round(p['final_rate'], 3)} "
                  f"cracked_round={p['cracked_round']} demo={p['demo']} rounds={p['rounds']}")
        print(f"  {cls}: status {c['status']}")
    if job: job["status"] = "done"
    save(s)
    print("cadence:", cadence)


def cmd_record_qual(a):
    s = load(); cls = a[0]; q = json.loads(a[1])
    c = s["classes"][cls]
    q.setdefault("version", c["current_version"]); q.setdefault("judge", "sonnet")
    c.setdefault("qual", []).append(q)
    for j in s["jobs"]:
        if j["kind"] == "judge" and j["class"] == cls and j["status"] == "running": j["status"] = "done"
    save(s); print(cls, "qual", q["score"])


def cmd_add_version(a):
    s = load(); cls, path = a[0], a[1]; note = a[2] if len(a) > 2 else ""
    c = s["classes"].setdefault(cls, {"status": "untested", "versions": [], "current_version": 0, "runs": [], "qual": []})
    v = len(c["versions"]) + 1
    c["versions"].append({"v": v, "file": path, "note": note, "added": time.time()})
    c["current_version"] = v
    if v > 1: c.setdefault("refined_versions", []).append(v - 1)
    for j in s["jobs"]:
        # refiners for this class are finished by their new version; designers are closed explicitly
        # with `done <job>` (several may run concurrently, and add-version cannot tell whose class this is)
        if j["kind"] == "refiner" and j["class"] == cls and j["status"] == "running":
            j["status"] = "done"
    c["status"] = classify(c)
    save(s); print(cls, "version", v, path)


def cmd_retire(a):
    s = load(); s["classes"][a[0]]["status"] = "retired"; save(s)


def report_table(s):
    rows = []
    for n, c in s["classes"].items():
        v = c["current_version"]; F = finals(c, v)
        m = mean_rate(c, v); q = qual_score(c)
        cracks = sum(1 for p in F if p["final_rate"] >= 0.9)
        profs = ",".join(sorted({p.get("profile", "?") for p in F})) or "-"
        bal = (1 - abs(m - 0.5) / 0.5) if m is not None else None
        dw, nw, dwo, nwo = demo_split(c, v)
        H = [p for p in finals(c, None, cadence=None) if p not in F]      # older-cadence history, any version
        hist = (sum(p["final_rate"] for p in H) / len(H)) if H else None
        rows.append((n, v, c["status"], m, bal, q, len(F), cracks, profs, dw, nw, dwo, nwo, hist, len(H)))
    rows.sort(key=lambda r: (-(r[4] or -1), r[0].lower()))
    out = ["| class | v | status | mean final | balance | with demo | no demo | kid score | finals | cracks | profiles | old-cadence history |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    pct = lambda x, k: "-" if x is None else f"{x:.0%} ({k})"
    for n, v, st, m, bal, q, nf, cr, profs, dw, nw, dwo, nwo, hist, nh in rows:
        out.append(f"| {n} | {v} | {st} | {'-' if m is None else f'{m:.0%}'} | {'-' if bal is None else f'{bal:.2f}'} | "
                   f"{pct(dw, nw)} | {pct(dwo, nwo)} | {'-' if q is None else f'{q:.1f}'} | {nf} | {cr} | {profs} | {pct(hist, nh)} |")
    return "\n".join(out)


def cmd_report(a):
    s = load(); plan(s); save(s)
    hdr = (f"# Ladder report — {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}\n\nCadence {CADENCE} (only runs at this cadence count; "
           f"earlier 6-round/one-demo-per-window runs are kept in state.json as history); balance = 1 − |mean − 0.5| / 0.5 (1.0 is perfect). "
           f"'with demo' / 'no demo' = mean final rate of players who did / did not spend a demo on the class (count). Kid score is the mean judge rubric (1–5).\n\n")
    body = report_table(s)
    tb = [n for n, c in s["classes"].items() if c["status"] == "too_easy_textbook"]
    foot = f"\n\nTextbook classes held at `too_easy_textbook` (100 % finals in sim1/sim2, not in the ladder): {', '.join(sorted(tb, key=str.lower))}\n"
    (REPO / "ladder/REPORT.md").write_text(hdr + body + foot)
    print(hdr + body + foot)


def cmd_arena(a):
    s = load(); cls = a[0]; c = s["classes"][cls]
    print(cur_file(c))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"status": cmd_status, "launch": cmd_launch, "ingest": cmd_ingest, "record-qual": cmd_record_qual,
     "add-version": cmd_add_version, "fail": cmd_fail, "done": cmd_done, "report": cmd_report,
     "retire": cmd_retire, "arena": cmd_arena}[cmd](sys.argv[2:])
