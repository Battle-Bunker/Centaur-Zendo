# Centaur Zendo — Player Guide

Welcome. You are going to write a bot that plays a guessing game against a
server, and you are going to write it *with* an AI assistant. That partnership
— human + machine — is what "centaur" means here.

This is the only document you need. Everything below is public and true. What
is *not* here (what the challenges actually want) is the game.

---

## 1. What the game is

The server has a pool of **challenge classes**. Each class has a short, unhelpful
name — things like `PP`, `Z7`, `gloam`. When the server presents a challenge it
sends you the name and a **clue** (a string). You send back a **solution**
(a string). The server replies with a **score: 1 or 0**. That is all the
feedback you ever get.

Nobody will tell you what `PP` means. Like the game *Zendo*, you are guessing
nature's rule from examples. You make guesses, you look at which ones scored 1,
you form a hypothesis, you test it next round.

Rounds are **half a second long** by default (the live value is `round_seconds` in the `welcome` message). Inside that window the server will throw as many
challenges at you as you can answer. At the very end of the session there is one
**three-second final test**, and only that final counts for the score.

So the loop of the whole game is:

> guess badly → read your logs → work out the rule (with your AI) → write a fast
> solver → guess well → repeat, 6 times → win the final.

---

## 2. The timeline

| thing | value (check `status` — the organiser can change these) |
|---|---|
| training round length | **0.5 seconds** |

> These are the defaults. **The live values are in the `config` block of the `welcome` message and in `python client/player.py status`; trust those over this table.**
| cooldown between your rounds | **5 minutes** by default (measured start → start) |
| max training rounds | **4** |
| training window | 4 × cooldown + 60 s (about **21 minutes** at the 5-minute default) |
| classes in the pool | **7** per game (drawn from a larger collection; the `welcome` message lists them) |
| demos | **3 per game**, total. Each one names a single class and shows one solved example of it. |
| final test | **3 seconds**, once, in a **10 minute** window after training ends (or as soon as you have used all your training rounds) |
| score | number of challenges you answer **correctly in the final** |
| tiebreak | fewer total answers wins (precision), then team name |

Notes that matter:

* The cooldown is measured **start to start**. Starting a round at 10:00:00 means
  your next round can start at 10:05:00, no matter how the round went.
* You have **4 rounds, ever**. There is no way to get a 5th. Don't burn one on
  a change you haven't tested locally.
* You do not have to use all 4. If you have nothing new to try, wait.
* You have **3 demos, ever**, and 7 classes. You cannot see a worked example of
  every class. Choosing *which* classes to ask about is most of the strategy.
* The training window closes on the clock too, so all 4 rounds only fit if you keep
  moving. Set your bot to `watch` and it will take every round the moment it is
  allowed.
* The **tiebreak rewards precision**: two teams on 40 correct are separated by
  who sent fewer answers. Skipping a challenge you cannot solve is not just
  faster, it is worth points in a tie.

---

## 3. What a round looks like from your side

```
you   -> {"type": "start_round"}
server -> round_started   round_id, kind, duration_ms, started_at, deadline
server -> challenge       index 0, name, clue
you   -> answer           round_id, index 0, solution        (or skip)
server -> result          index 0, score 0|1
server -> challenge       index 1, name, clue        <- arrives IMMEDIATELY
you   -> answer           index 1, ...
   ... over and over until the deadline ...
server -> round_over      presented, answered, correct, items[...]
```

Three consequences, and they are the whole strategy of the game:

1. **The server does not wait.** Challenge `i+1` is sent the instant it has
   scored answer `i`. The round is a treadmill and *you* set its speed.
2. **Speed is everything.** If your bot takes 100 ms per challenge you will see
   ~10 challenges in a round. At 1 ms you see hundreds. More challenges means
   more data while training, and more points in the final.
3. **Skipping is instant.** `skip` scores 0, but it costs you almost no time and
   moves you straight to the next challenge. A slow wrong answer is strictly
   worse than a fast skip.

When the deadline passes mid-challenge, that unanswered challenge is simply
dropped — you are not punished for it, you just got fewer items.

---

## 4. What you know

* At `welcome` the server sends you the **complete list of challenge names** in
  the pool. You know how many classes exist and what they are called.
* A **clue is a string**, at most 1024 characters.
* A **solution is a string**, at most 1024 characters (the same cap as a clue). Anything longer is cut off
  by the client before it is sent. If you want to send structured data, JSON-
  encode it — that is the house convention.
* A **score is exactly 0 or 1**. There is no partial credit and no error message.
  A crash in your solver, a timeout, an empty answer: all just 0.
* Every challenge class is **deterministic given its clue**. The same clue always
  wants the same kind of answer. (Some classes may accept more than one correct
  answer, but the clue always contains everything needed to find one.)
* Every challenge class is **solvable by a good program in well under a second** —
  usually in milliseconds. There is a reference solver for every class living on
  the server, so nothing in the pool is impossible or requires a lucky guess.
* You can spend a **demo** to see the reference solver's answer for one class:
  you get back a real clue, a real correct solution, and its score. One worked
  example, on request — and you only get three of them for seven classes.
* Clues are meant to reveal the **shape** of an answer — what kind of thing to send
  back (a grid, a word list, a number, the picture in the clue with something added).
  Often the clue *contains* the object and the answer is that object edited. You may
  not know the *rule* without a demo, but you should usually be able to guess the
  *format*; a class where you cannot even guess the format is the one to spend a
  demo on.
* Your own history: every clue, answer and score you have ever seen is in your
  logs. That is your dataset.

### 4b. What answers tend to look like (one made-up example)

Many classes are **pictures**, and the clue usually *contains* the object. A
typical shape is "here is the thing; send it back with something added". An
invented class, not in any pool, just to show the house style:

```
clue:                              answer:
.....                              ..o..
.....                              .....
.....                              o...o
#####                              #####
3 pebbles                          3 pebbles
```

The clue is an empty box drawn in ASCII plus a line of text; the answer is the
same drawing with three `o` pebbles placed by some rule you have to discover
(which cells score is the puzzle — the *format* is not). **House rule:** for a
picture class the answer is the clue's picture with the edit applied; the
trailing text line of the clue may be kept or left out — the scorer ignores it
either way. Other classes want a
list of words, a single number, or a grid the same size as the clue's. When a
clue is nothing but a code like `B12`, the class is telling you it needs a demo.

## 5. What you do NOT know

* **What any challenge means.** Not one of them. The name is a label, not a hint,
  and the description the author wrote is private.
* Which classes are easy and which are hard.
* How often each class comes up in the final (assume anything in the pool can
  appear; the final uses the same pool as training).
* Whether the clue you are looking at is typical of that class.

You infer all of this. That is the game.

---

## 6. The demos — three cheats, choose them well

`python player.py demo NAME` asks the server to run its own reference solver on a
fresh clue of class `NAME` and show you:

```
demo PP
  clue    : <a real clue>
  solution: <an answer that scores 1>
  score   : 1
```

Rules: **three demos per game, total**, on any classes you like (the same class
twice is allowed), at any time during training when you are not in a round. There
are seven classes in the pool, so at least four of them you must crack from clues
and 0/1 feedback alone. `status` shows `demos remaining`. A demo never shows you a
clue whose answer is the clue unchanged (a "0 fall" case): the server redraws until the
answer actually differs, so every demo shows the edit.

How to spend them:

* **Do not spend one before your first round.** A skip-only round shows you all
  seven clue formats for free; only then do you know which classes look
  impenetrable and which you can already guess the shape of.
* Spend a demo on the class you are **most confused about** *and* that appears
  often — the final draws from the same seven. A class whose clue already tells
  you the answer's shape may not need one at all: probe it instead.
* Classes are built so that the **shape** of the answer can usually be read off
  the clue (what kind of data to send). What a demo buys you is the *rule*: which
  of the many well-formed answers score — or, for a class whose clue is opaque,
  the format itself. Some classes are worth almost nothing
  without that example and are worth everything with it — those are the ones to
  spend on.
* A demo answers "what does a correct answer *look like*", which is usually the
  hard half. Show the demo output to your AI assistant along with 20 of your own
  failed attempts at the same class.
* Two teams with the same skill will finish with different scores depending on
  which three classes they asked about. That is intended. Think about it.

---

## 7. Your client

Everything you need is in `client/`:

```
client/player.py    the client. You do not need to change this.
client/strategy.py  THE ONE FILE YOU EDIT.
client/logs/        written for you after every round
client/memory.json  your bot's memory, kept between rounds
```

Install once: `pip install -r client/requirements.txt` (just `websockets`).

### Commands

```bash
export ZENDO_URL=ws://the-server:8080/ws
export ZENDO_TEAM=our-team
export ZENDO_TOKEN=our-secret

python client/player.py status        # phase, rounds used, when you can go again
python client/player.py round         # play ONE training round now
python client/player.py wait-round    # sleep until the cooldown is over, then play
python client/player.py watch         # keep playing rounds until they run out
python client/player.py demo PP       # spend one of your three demos on class PP
python client/player.py final         # run the 3-second final (once!)
```

Useful flags: `--url --team --token`, `--strategy path/to/strategy.py`
(try a new brain without touching the old one), `--log-dir`, `--memory`,
`--max-rounds N` (for `watch`).

### The one file you edit

```python
def solve(name, clue, memory) -> str:   # required. Return your answer.
def on_round_start(memory): ...         # optional. Slow setup goes HERE.
def on_round_end(items, memory): ...    # optional. items = everything you saw.
```

`memory` is an ordinary dict. It is loaded from `memory.json` before the round and
saved after it, so anything you put in it survives to the next round. Keep it
JSON-friendly (dicts, lists, strings, numbers).

If your `solve` returns `None`, the client sends `skip` (instant, and it does not
count as an answer for the tiebreak). If it raises an exception, the client also
skips and carries on — one bug cannot end your round; the crash is recorded in the
round log so you can fix it. Returning `""` is an *answer* (a wrong one), not a
skip. Non-string return values are converted to strings; over-long ones are cut.
`memory["_index"]` is set to the index of the current challenge within the round
before each call, handy for cycling through candidate answer formats.

### The logs

After every round the client writes:

* `logs/round_<n>.jsonl` — every message in and out, with timestamps. The
  complete raw record.
* `logs/round_<n>.txt` — the human (and AI) readable version: a header, then a
  table of `index / name / clue / answer / score`, then a per-name tally with
  presented / correct / hit-rate.
* `logs/summary.txt` — one line per round, plus your **running hit-rate for every
  challenge name across all rounds**. This is the file that tells you where to
  spend your next hour.
* `logs/demos.jsonl` — every demo you have ever taken.

The client also prints its own **mean answer latency** (the time from receiving a
challenge to sending the answer). Watch that number. If it climbs, your solver
got slow and your round just got smaller.

---

## 8. A workflow that works

**Round zero — collect data, expect nothing.**
Run the shipped `strategy.py` unchanged. It answers with random short strings and
records every clue it sees. You will score close to zero. That is correct: you
have just bought yourself a few hundred clue/answer/score examples.

**Between rounds — this is where the game is actually played.**
You have five minutes of cooldown. Use all of it.

1. Read `logs/summary.txt`. Which names appear most? Which have a hit-rate above
   zero (you got lucky — *why*)?
2. Open `logs/round_<n>.txt` and pick the class you want to crack.
3. Paste the clue/answer/score rows into your AI assistant and ask:
   > "These are clues from a challenge called `Z7` and my random answers, with
   > 1 = correct and 0 = wrong. What rule might the clue be describing? Give me
   > three hypotheses, ranked, and a short Python function for the best one."
4. Ask it to argue against itself: "what other rule fits all of these?"
5. Spend your demo on whichever class the conversation kept getting stuck on.
6. Write the solver into `strategy.py`, behind `if name == "Z7":`.
7. **Test it locally before you spend a round.** Take clues from your log file
   and run your function on them by hand. A round costs five minutes; a local
   test costs five seconds.
8. Guard it: wrap it in `try/except` and give it a time budget. If it hasn't
   found an answer in a few milliseconds, return `""` and move on.
9. Run the round. Compare hit-rates in `summary.txt`. Hypothesis confirmed or
   killed — either way you learned something.

**Late rounds — protect what works.**
Never change a solver that is scoring 1 without keeping a copy. Use
`--strategy strategy_v2.py` to try a risky idea and keep the good brain intact.
Before the final: run a normal round with exactly the code you plan to use, look
at the numbers, and change nothing afterwards.

**The final.** Three seconds, one attempt, same challenge pool. There is nothing
clever to do at the last minute — the final just runs whatever you already built.
Make sure your bot is fast, silent, and never crashes.

---

## 9. Tips for going fast

The round is a treadmill; every millisecond you spend is a challenge you don't
see. Target **5–20 ms per challenge at most**, and much less if you can.

* **Precompute in `on_round_start`.** Building a prime table, a dictionary, a
  regex, a lookup of anything: do it there. It is completely free. Doing it
  inside `solve` pays the cost on every single challenge.
* **Cache by clue.** `memory` persists between rounds, so a dict of
  `clue -> answer` means a repeated clue is answered instantly. Cache the
  *shape* of the work too, not just exact hits.
* **Never print in `solve`.** Terminal output is slow — surprisingly, absurdly
  slow — and you are doing it hundreds of times a second. The client deliberately
  writes nothing to disk or screen during a round for exactly this reason. If you
  must record something, append it to a list in `memory`.
* **Give every solver a time budget.** Something like:

  ```python
  import time
  def solve(name, clue, memory):
      deadline = time.perf_counter() + 0.010     # 10 ms, hard stop
      for candidate in generate_candidates(clue):
          if time.perf_counter() > deadline:
              return ""                          # bail out, take the 0, move on
          if looks_right(candidate):
              return candidate
      return ""
  ```

* **Return `""` early when you have no idea.** An empty answer always scores 0 —
  but so does a wrong one, and the empty one costs no time. (Skipping also helps
  your tiebreak, since it doesn't count as an answer.)
* **Avoid unbounded loops.** `while True`, deep recursion, brute force over a
  huge space: these eat your whole round on one challenge.
* **Do the cheap check first.** If a class needs a rare property, test the cheap
  necessary condition before the expensive sufficient one.
* **Don't import heavy modules inside `solve`.** Import at the top of the file.
* Measure. The client prints mean / median / max latency after each round, and
  `summary.txt` keeps the history. If max is huge but mean is small, one clue is
  pathological — cap it.

---

## 10. The protocol (public, from the engine spec §6)

The client already speaks all of this; it is here so you can see exactly what is
going on, and write your own client if you would rather.

WebSocket at `/ws`, JSON text frames, one object per frame.

**Client → Server**

| type | fields |
|---|---|
| `join` | `team`, `token` |
| `start_round` | — |
| `answer` | `round_id`, `index`, `solution` (str) |
| `skip` | `round_id`, `index` |
| `demo` | `name` |
| `start_final` | — |
| `status` | — |
| `ping` | — |

**Server → Client**

| type | fields |
|---|---|
| `welcome` | `team`, `phase`, `challenges: [names]`, `config: {round_seconds, final_seconds, cooldown_seconds, max_training_rounds, max_solution_chars, max_clue_chars, training_ends_at, final_ends_at}`, `rounds_used`, `next_round_available_at`, `demo_available`, `server_time` |
| `round_started` | `round_id`, `kind: "training"\|"final"`, `duration_ms`, `started_at`, `deadline` |
| `challenge` | `round_id`, `index`, `name`, `clue` |
| `result` | `round_id`, `index`, `score` |
| `round_over` | `round_id`, `kind`, `presented`, `answered`, `correct`, `items: [{index,name,clue,solution,score}]`, `rounds_used`, `next_round_available_at`, `demo_available` |
| `demo_result` | `name`, `clue`, `solution`, `score` |
| `status` | `phase`, `server_time`, `training_ends_at`, `final_ends_at`, `rounds_used`, `next_round_available_at`, `demo_available`, `final_score`, `leaderboard` |
| `error` | `code`, `message`, optional `retry_at` |
| `pong` | `server_time` |

Rules of the wire:

* One socket per team at a time. A new `join` for the same team replaces the old
  socket **and aborts any round in flight** — so don't run two copies of your bot.
* Every round message carries `round_id`. Answers for a stale or unknown
  `(round_id, index)` are ignored with `error{code:"stale"}`.
* Messages that arrive after the deadline are ignored.
* Refusals come back as `error` with a `code`: `cooldown` (too soon —
  `retry_at` tells you when), `phase` (wrong part of the game), `round_cap`
  (your training rounds are gone), `busy` (a round is already running).
* All timestamps are server unix-time floats. Trust `server_time`, not your own
  clock.

---

## 11. Fair play

* One team, one bot, one socket. Don't run several clients for the same team.
* Your bot must work it out at run time from clues and scores. Reading the
  server's files, the challenge JSON, or another team's logs is not playing the
  game.
* Asking an AI assistant for help is not cheating — it is the entire point.
  Asking it to break into the server is a different activity, and a worse one.
* If something in the protocol looks broken, tell the organiser. Finding a bug is
  good; quietly farming it is not.

Good luck. Guess boldly, log everything, and go fast.
