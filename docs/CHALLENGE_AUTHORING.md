# Writing a Centaur Zendo challenge

A challenge is **data**, not code you install: one JSON document with three Python
source strings. The server loads a directory of them, validates each one at start-up,
and only the ones that pass go into the live pool.

Players never see this file. They see the challenge **name** and each **clue**, plus a
0/1 result per answer. Everything they learn, they learn by guessing and being told
"yes" or "no" — so a good challenge is one whose rule can be *inferred* from examples.

* Run the validator on your file before submitting: `python tools/quickcheck.py mine.json`
* Or use the web form at `/submit`, which runs the same checks and shows the report.

---

## 1. The interface

```json
{
  "name": "PP",
  "author": "your name",
  "description": "Private notes for organisers. Never shown to players.",
  "generate": "def generate(seed):\n    ...\n",
  "solve":    "def solve(clue):\n    ...\n",
  "score":    "def score(clue, solution):\n    ...\n"
}
```

| function | signature | contract |
|---|---|---|
| `generate` | `generate(seed: int) -> str` | The clue. **Deterministic**: the same seed must always produce the same string. Always seed your own RNG: `r = random.Random(seed)`. |
| `solve` | `solve(clue: str) -> str` | A reference answer that scores 1. Used to validate the challenge and to power a player's one "demo" per round. |
| `score` | `score(clue: str, solution: str) -> int` | Exactly `1` or `0`. Must return `0` for `""`. Any exception or non-0/1 return counts as 0. |

Each source is a **module body**, exec'd on its own. Helper functions at the top level
are fine (see `isp` in the worked example below); nothing is shared between the three
sources, so a helper that both `solve` and `score` need must be written twice.

Field rules

* `name` — 1–16 chars of `[A-Za-z0-9_-]`, unique in the pool. This is the only label
  players get, so make it obscure but memorable: `PP`, `Z7`, `gloam`.
* `description` — private. Say what the rule is, so an organiser can review it.
* Clues and solutions are **strings**. Structured data is JSON-encoded by convention
  (`"[1, 2, 3]"`), or use a simple space/slash-separated format like `"31/34"`.

### Caps

| cap | default | applies to |
|---|---|---|
| `max_score_code_chars` | **256** | `score` source |
| `max_generate_code_chars` | 50000 | `generate` source |
| `max_solve_code_chars` | 5000 | `solve` source |
| `max_clue_chars` | 1024 | every string `generate` returns |
| `max_solution_chars` | 4096 | solutions, from players and from `solve` |
| `max_generate_ms` | 100 | one `generate` call |
| `max_score_ms` | **50** | one `score` call — on the real solution *and* on junk |
| `max_solve_ms` | 2000 | one `solve` call (validation and demos only) |

The engine measures wall-clock time per call inside a worker process. A call over its
limit is killed; during a game a slow `score` simply scores 0, which is unfair to the
player — so leave yourself a wide margin (aim for ≤ 10 ms).

---

## 2. Execution model (the sandbox)

Each source is compiled and exec'd into a fresh namespace with **restricted builtins**.

Available builtins:

```
abs all any ascii bin bool bytearray bytes callable chr complex dict divmod enumerate
filter float format frozenset getattr hasattr hash hex id int isinstance issubclass iter
len list map max min next object oct ord pow print range repr reversed round set setattr
slice sorted str sum tuple type zip True False None
Exception ValueError TypeError KeyError IndexError ZeroDivisionError ArithmeticError
StopIteration RuntimeError AssertionError OverflowError LookupError RecursionError
```

Pre-imported modules, already present as globals (no `import` needed, but `import` of
these works too):

```
math re random itertools functools collections string hashlib json heapq bisect
operator fractions statistics array struct base64 decimal
```

Importing anything else raises `ImportError`.

**Not available:** `open`, `eval`, `exec`, `compile`, `input`, `globals`, `locals`,
`vars`, `__build_class__`, and everything else not listed above. Two consequences:

* No file, network or environment access. Your challenge must be self-contained.
* **`class` statements do not work** (they need `__build_class__`). Use functions,
  dicts and tuples instead. This is the most common surprise for authors.

`print` works and goes to the server's log — handy while developing, noise in production.

Time limits are enforced with `signal.setitimer` inside the worker; a challenge that
hangs at C level (a huge `sum(range(...))`, catastrophic regex backtracking) is killed
by the parent process, which then starts a fresh worker.

> **Honesty note.** This is a *game* sandbox: restricted builtins, wall-clock limits and
> a separate process. It is **not** a security boundary against a determined attacker.
> Organisers must read every submitted challenge before loading it into a live pool.

---

## 3. What validation checks

`validate()` (engine) and `tools/quickcheck.py` (CLI) run exactly the same checks, in
this order, stopping at the first failing group:

1. **Metadata & size** — name matches `[A-Za-z0-9_-]{1,16}` and is unique; all three
   sources present and within their character caps. Empty `description` ⇒ warning.
2. **Compilation** — each source compiles, exec's in the sandbox namespace, and defines
   the required top-level function.
3. **Behaviour**, for each of `validation_seeds` (default 20) random seeds drawn from
   `random.Random(12345)`:
   * `clue = generate(seed)` is a non-empty `str`, within `max_clue_chars` and `max_generate_ms`;
   * calling `generate(seed)` again returns the **identical** string (determinism);
   * `sol = solve(clue)` is a `str` within `max_solution_chars` and `max_solve_ms`;
   * `score(clue, sol) == 1`, within `max_score_ms`;
   * `score(clue, "") == 0`;
   * junk answers — `"0"`, `"1"`, `"x"`, `"1"*100`, the clue itself, and a shuffled
     version of the real solution — return 0 or 1 within `max_score_ms`
     (an *exception* on junk is only a warning; it counts as 0);
   * at least one junk answer must score 0, otherwise **"the scorer accepts anything"**.
4. **Warnings** (never fatal): empty description; the scorer accepts the clue itself;
   the scorer raised on `""` or junk; `solve` slower than 25% of its cap; `generate`
   slower than 50% of its cap.

The report you get back is `{ok, errors, warnings, timings, samples}` — `timings` has the
worst-case ms per function, `samples` up to three `{seed, clue, solution}` triples so you
can eyeball what players will actually see.

---

## 4. The 256-character scorer discipline

`score` is capped at **256 characters** on purpose. It forces the shape of a good
challenge: **hard to find, easy to check**.

* Everything the scorer needs must be **in the clue**. There is no hidden channel from
  `generate` to `score` — no shared state, no re-deriving the seed. If your scorer needs
  to know something, put it in the clue.
* Verify, do not re-solve. Checking "is this a palindromic prime containing 4-4-6?" fits
  in 256 chars; searching for one does not.
* Be strict about what counts, but robust about form. `s.strip()` is usually worth its
  characters; forgiving whitespace is kind to players.
* Junk in, `0` out. Raising is *tolerated* (it counts as 0 and earns a warning), but a
  scorer that returns 0 cleanly is better — it is faster and it documents the rule.
* Every answer must be checkable in ≤ 50 ms, including deliberately awful inputs like
  `"1" * 100` or a 4000-character string. Watch out for anything quadratic in
  `len(solution)`, `int(s)` on a huge digit string, or trial division on a big number.

Tricks that buy characters (all used in real challenges):

```python
def score(c,s):                      # short parameter names
 s=s.strip();n=int(s)                # one-space indent, ';' to join statements
 return int(cond1 and cond2 and ...) # bool -> int in one expression
```

`all(...)`, generator expressions, `sum(map(int, s.split()))` and slicing (`s[::-1]`)
pack a lot of checking into very little source. Keep it readable enough that an
organiser can confirm it matches your `description`.

---

## 5. Worked example: `challenges/PP.json`

Rule: *the answer is a palindromic prime whose decimal digits contain the clue*.
Clue: a 3–4 digit string. Hard to find, trivial to check — the ideal shape.

```json
{
  "name": "PP",
  "author": "orchestrator",
  "description": "Palindromic prime containing the clue digits as a substring. Clue: a random 3-4 digit string. Solution: decimal string of a palindromic prime containing it.",
  "generate": "...",
  "solve": "...",
  "score": "..."
}
```

`generate` — seeded RNG, short clue, deterministic:

```python
def generate(seed):
    r = random.Random(seed)
    n = r.choice([3, 3, 4, 4])
    return ''.join(r.choice('0123456789') for _ in range(n))
```

`solve` — a reference search, allowed to be slow (2 s cap) and long (5000 chars).
Note the top-level helper `isp`, and that no `class` is used:

```python
def isp(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    for p in range(3, int(n ** 0.5) + 1, 2):
        if n % p == 0: return False
    return True

def solve(clue):
    # build palindromes of odd length around the clue: L + clue + R such that whole is a palindrome
    for total in range(len(clue), len(clue) + 12):
        half = (total + 1) // 2
        for left in itertools.product('0123456789', repeat=half):
            s = ''.join(left)
            if s[0] == '0': continue
            pal = s + s[-2::-1] if total % 2 else s + s[::-1]
            if clue in pal and isp(int(pal)):
                return pal
    return ''
```

`score` — 135 characters, four independent conditions, no search:

```python
def score(c,s):
 s=s.strip();n=int(s)
 return int(s==s[::-1] and c in s and n>2 and n%2 and all(n%p for p in range(3,int(n**.5)+1,2)))
```

Points worth copying:

* The clue length is capped at 4 digits **because of the scorer's budget**: a 5-digit
  clue can force a 13-digit answer, whose trial division needs ~1.3 M iterations and
  blows the 50 ms limit. Choose your clue sizes by measuring the *scorer*, not the solver.
* `n % 2` and the odd-step `range(3, ..., 2)` halve the scorer's work for free.
* `int(s)` raises `ValueError` on `""` and on `"x"`. Validation reports that as a
  warning and counts it as 0 — acceptable here, but returning 0 explicitly would be
  slightly better.

Validator output for this file:

```
$ python tools/quickcheck.py challenges/PP.json
OK   PP         challenges/PP.json  gen=0.03ms score=4.15ms solve=79.52ms
   warn : score raised on empty solution (seed 1789368711): ValueError: ... (treated as 0)
   warn : score raised on junk 'x' (seed 1789368711): ValueError: ... (treated as 0)
```

---

## 6. Checklist before you submit

- [ ] `python tools/quickcheck.py mine.json -v` prints `OK` and the samples look like a
      fair puzzle (`--seeds 200` for a harder shake-out).
- [ ] `score` is well under 256 chars and well under 50 ms on junk as well as real answers.
- [ ] `generate` is seeded — no `random.random()`, no clock, no counters.
- [ ] The clue carries everything the scorer needs.
- [ ] A human could plausibly infer the rule from a handful of clue/answer/0-1 examples.
- [ ] `description` explains the rule to the organiser reviewing your code.
