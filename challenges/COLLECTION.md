# The collection (2026-09-05)

`challenges/*.json` is what the server loads. It holds three kinds of class:

| kind | classes | status |
|---|---|---|
| **Calibrated** by the ladder (Opus centaurs ~50 %, kid score ≥ 4 unless noted) | fennick (bookshelf), kelmar (rain over a garden), virel (next course of bricks, kid 3.7), basten (fish tank), borsel (dice lineup) | play these |
| Human-designed benchmarks | LegoZendo, LegoZendo2, Wordz | keep |
| Textbook set (v1 classes; Opus cracks nearly all blind) | AHMES … zebu (35 classes), plus OKRIN, quaich, murn | starter material; the ladder marks them `too_easy_textbook` |

Versions in flight live in `challenges/lab/` (previous versions as `<name>.vN.json`, design notes as
`NOTES_*.md`). A class is copied here when `ladder/ladder.py status` reports it `calibrated`; the copy
is the lab file at that version, byte for byte. `ladder/STARS.md` has the write-ups; `ladder/REPORT.md`
the live table. Rule-family classes (`docs/RULE_FAMILIES.md`) at Revision 3 — tavrik, tresk, wisbek,
ospren, dornic, mestrel — are in the lab awaiting their second pool each.
