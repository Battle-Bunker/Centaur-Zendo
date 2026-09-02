#!/usr/bin/env python3
"""Simulation arena for Centaur Zendo.

Runs a full game (training rounds + final) with the *real* engine, while keeping the
challenge pool confidential from the (LLM or human) players: the pool is copied into a
hidden directory, the server runs from there, and each team gets its own sandbox directory
containing only the reference client and the player guide.

  python sim/arena.py setup  --run NAME --teams alpha,beta,gamma [--cooldown 30] [--rounds 12]
  python sim/arena.py status --run NAME
  python sim/arena.py report --run NAME          # writes sim/results/NAME/REPORT.md
  python sim/arena.py teardown --run NAME        # stops the server, collects logs
"""
import argparse, json, os, shutil, signal, socket, subprocess, sys, time, secrets, collections
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "sim" / "results"


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def run_dir(name):
    d = RESULTS / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def setup(a):
    rd = run_dir(a.run)
    arena = Path(a.arena_root or (Path(os.environ.get("TMPDIR", "/tmp")) / f"zendo-arena-{a.run}"))
    hidden = arena / f".pool-{secrets.token_hex(4)}"
    hidden.mkdir(parents=True, exist_ok=True)
    pool = hidden / "challenges"
    pool.mkdir(exist_ok=True)
    src_pool = Path(a.challenge_dir or (REPO / "challenges"))
    n = 0
    for f in sorted(src_pool.glob("*.json")):
        shutil.copy(f, pool / f.name); n += 1
    teams = [t.strip() for t in a.teams.split(",") if t.strip()]
    tokens = {t: secrets.token_hex(6) for t in teams}
    port = a.port or free_port()
    cfg = {
        "cooldown_seconds": a.cooldown,
        "max_training_rounds": a.rounds,
        "training_seconds": a.training_seconds,      # generous: LLM players think for minutes between rounds
        "final_window_seconds": a.final_window,
        "round_seconds": 1.0,
        "final_seconds": 3.0,
        "open_registration": True,
        "challenge_dir": str(pool),
        "event_log": str(hidden / "events.jsonl"),
        "host": "127.0.0.1",
        "port": port,
        "admin_token": secrets.token_hex(8),
    }
    for kv in a.set or []:
        k, v = kv.split("=", 1)
        cfg[k] = json.loads(v)
    (hidden / "game.json").write_text(json.dumps(cfg, indent=1))
    log = open(hidden / "server.log", "ab")
    proc = subprocess.Popen(
        [sys.executable, "-m", "engine.server", "--config", str(hidden / "game.json"), "--start-now"],
        cwd=str(REPO), stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
        env={**os.environ, "PYTHONPATH": str(REPO)},
    )
    # per-team sandboxes: only the client + the player guide
    for t in teams:
        td = arena / "players" / t
        if td.exists():
            shutil.rmtree(td)
        td.mkdir(parents=True)
        for f in ["player.py", "strategy.py", "README.md", "requirements.txt"]:
            shutil.copy(REPO / "client" / f, td / f)
        shutil.copy(REPO / "docs" / "PLAYER_GUIDE.md", td / "PLAYER_GUIDE.md")
        (td / "connection.txt").write_text(
            f"ZENDO_URL=ws://127.0.0.1:{port}/ws\nZENDO_TEAM={t}\nZENDO_TOKEN={tokens[t]}\n")
    meta = {"run": a.run, "arena": str(arena), "hidden": str(hidden), "port": port, "pid": proc.pid,
            "teams": teams, "tokens": tokens, "admin_token": cfg["admin_token"], "config": cfg,
            "pool_size": n, "started_at": time.time()}
    (rd / "meta.json").write_text(json.dumps(meta, indent=1))
    # wait for the server
    for _ in range(100):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                break
        except OSError:
            time.sleep(0.1)
    print(json.dumps({k: meta[k] for k in ("run", "arena", "port", "pid", "teams", "pool_size")}, indent=1))
    for t in teams:
        print(f"  team {t}: {arena/'players'/t}")


def load_meta(name):
    return json.loads((run_dir(name) / "meta.json").read_text())


def status(a):
    m = load_meta(a.run)
    import urllib.request
    with urllib.request.urlopen(f"http://127.0.0.1:{m['port']}/api/state", timeout=5) as r:
        print(r.read().decode())


def teardown(a):
    m = load_meta(a.run)
    try:
        os.killpg(m["pid"], signal.SIGTERM)
    except ProcessLookupError:
        pass
    time.sleep(0.5)
    rd = run_dir(a.run)
    hidden = Path(m["hidden"]); arena = Path(m["arena"])
    for f in ["events.jsonl", "server.log", "game.json"]:
        if (hidden / f).exists():
            shutil.copy(hidden / f, rd / f)
    for t in m["teams"]:
        td = arena / "players" / t
        dst = rd / "players" / t
        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)
        for f in ["strategy.py", "memory.json", "NOTES.md"]:
            if (td / f).exists():
                shutil.copy(td / f, dst / f)
        if (td / "logs").exists():
            shutil.copytree(td / "logs", dst / "logs")
    print(f"collected into {rd}")


def report(a):
    m = load_meta(a.run)
    rd = run_dir(a.run)
    ev = rd / "events.jsonl"
    if not ev.exists():
        ev = Path(m["hidden"]) / "events.jsonl"
    rounds = []
    for line in ev.read_text().splitlines():
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("dir") == "round" and "presented" in e.get("msg", {}):
            rounds.append(e)  # skip round_start markers and demos
    # per team per round
    by_team = collections.defaultdict(list)
    for e in rounds:
        by_team[e["team"]].append(e["msg"])
    lines = [f"# Simulation report: {m['run']}", "",
             f"Pool size: {m['pool_size']} challenges. Cooldown {m['config']['cooldown_seconds']}s, "
             f"max {m['config']['max_training_rounds']} training rounds, final {m['config']['final_seconds']}s.", ""]
    lines += ["## Correct answers per round (training rounds 1..N, then FINAL)", ""]
    teams = sorted(by_team)
    maxr = max((len([r for r in rs if r.get("kind") == "training"]) for rs in by_team.values()), default=0)
    hdr = "| team | " + " | ".join(f"r{i+1}" for i in range(maxr)) + " | FINAL (correct/answered) |"
    lines += [hdr, "|" + "---|" * (maxr + 2)]
    for t in teams:
        tr = [r for r in by_team[t] if r.get("kind") == "training"]
        fi = [r for r in by_team[t] if r.get("kind") == "final"]
        cells = [f"{r.get('correct',0)}/{r.get('answered',0)}" for r in tr] + [""] * (maxr - len(tr))
        f = f"**{fi[0].get('correct',0)}**/{fi[0].get('answered',0)}" if fi else "-"
        lines.append(f"| {t} | " + " | ".join(cells) + f" | {f} |")
    lines += ["", "## Per-challenge hit rate by team (all training rounds) — presented / correct", ""]
    names = sorted({it["name"] for rs in by_team.values() for r in rs for it in r.get("items", [])})
    lines += ["| challenge | " + " | ".join(teams) + " |", "|" + "---|" * (len(teams) + 1)]
    for n in names:
        row = []
        for t in teams:
            p = c = 0
            for r in by_team[t]:
                if r.get("kind") != "training":
                    continue
                for it in r.get("items", []):
                    if it["name"] == n:
                        p += 1; c += it.get("score", 0)
            row.append(f"{c}/{p}" if p else "-")
        lines.append(f"| {n} | " + " | ".join(row) + " |")
    lines += ["", "## Final round per-challenge (correct/presented)", ""]
    lines += ["| challenge | " + " | ".join(teams) + " |", "|" + "---|" * (len(teams) + 1)]
    for n in names:
        row = []
        for t in teams:
            p = c = 0
            for r in by_team[t]:
                if r.get("kind") != "final":
                    continue
                for it in r.get("items", []):
                    if it["name"] == n:
                        p += 1; c += it.get("score", 0)
            row.append(f"{c}/{p}" if p else "-")
        lines.append(f"| {n} | " + " | ".join(row) + " |")
    out = rd / "REPORT.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nwritten {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("setup"); s.add_argument("--run", required=True); s.add_argument("--teams", required=True)
    s.add_argument("--cooldown", type=float, default=30); s.add_argument("--rounds", type=int, default=12)
    s.add_argument("--training-seconds", type=float, default=6 * 3600)
    s.add_argument("--final-window", type=float, default=3600)
    s.add_argument("--port", type=int); s.add_argument("--arena-root"); s.add_argument("--challenge-dir")
    s.add_argument("--set", action="append", metavar="KEY=JSON", help="override a GameConfig field")
    for c in ("status", "teardown", "report"):
        p = sub.add_parser(c); p.add_argument("--run", required=True)
    a = ap.parse_args()
    {"setup": setup, "status": status, "teardown": teardown, "report": report}[a.cmd](a)


if __name__ == "__main__":
    main()
