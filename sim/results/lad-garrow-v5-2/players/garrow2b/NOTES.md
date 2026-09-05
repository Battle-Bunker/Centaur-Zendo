# garrow2b — Centaur Zendo notes

Global discovery (round 1, skip-only harvest of 380 clues): every class's clue ends
(garrow: begins) with "<N> <word>".  N is the number of edits the answer applies.
N == 0 therefore means "answer = the clue's picture unchanged" — free points on
~9% of every class.  (True for 6 of 7 classes; virel's number is NOT an edit count.)

| class   | rule | conf | demo | final hit |
|---------|------|------|------|-----------|
| fennick | towers of letters standing on a base row; `_` = flat lid.  For each **one-column gap** in the base, the **shorter** of the two flanking towers leans into it: everything above its base shifts one column, `_` becomes `/` (right) or `\` (left).  Equal heights → nobody leans.  A tower with a gap on **both** sides never leans.  Verified: predicted fall count == N on 106/106 clues. | certain | YES | 100% |
| molvic  | corner-shop shelves.  Find **mutual pairs**: same column c where shelf X holds Y's product and shelf Y holds X's.  Each of those two items goes home to the **leftmost `___` gap on its own shelf** (if that shelf has one); its old cell becomes `___`.  N = number of items that actually move. | certain | YES | 100% |
| virel   | rows of boxes, all the same character width.  Answer = the clue with **one new row added on top** (number line dropped).  The new row is the **maximal refinement** of one of the clue's rows: every box of width w becomes floor(w/2) boxes, all `[]` except one `[-]` if w is odd; the `[-]` is placed so the new seam falls where fewest clue rows already have a seam.  WHICH row is the source is still unsolved — the top row is never it (0/14); second-from-bottom scores best. | partial | YES | ~30% |
| durnel  | cars `<XX` / `XX>` on a road with 4 potholes `\_/` and towers of the car's letter above it.  N cars turn round.  Tried: faces-a-pothole, pothole-ahead-but-not-behind, building-height comparisons — none reproduces N. | unsolved | no | N=0 only |
| garrow  | "<letter> <N> slices" + a box of `:` with 2-char tokens.  Almost certainly "cut the box into N slices"; the cut glyph is unknown, so unguessable without a demo. | unsolved | no | N=0 only |
| norvel  | hat/snare/kick drum grid in bars of 4; "N slip".  Tested 19 count statistics, best matched only 26/95. | unsolved | no | N=0 only |
| tovel   | month calendar with letters on days; "N bump".  Tested 30 statistics, best (letters occurring >=3 times) matched 43/108. | unsolved | no | N=0 only |

Demos: molvic, fennick (round 2 — the two whose clue said least about the *rule*
and which appeared most often), virel (round 3 — the only class where the N==0
echo scored 0, i.e. the only class whose answer *shape* I could not read off the clue).
Deliberately left without a demo: durnel, garrow, norvel, tovel — each of those
clues does tell you the answer's shape (the picture, edited), so a demo would only
have bought the rule for one of four.
