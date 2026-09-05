# durnel1b — final score 868 (rank 1; opponent 747)

## Global structure discovered
All 7 classes are picture classes with a trailing (garrow: leading) text line "N verb".
N is the number of edits/events. Confirmed by probe: for basten/durnel/fennick,
answering the unchanged picture scores exactly when N==0 and never otherwise.
Trailing line may be kept or dropped. virel is the exception: N==0 is NOT a no-op.

## Per class
- kelmar "N lean" — SOLVED 100%. Mushrooms `(~~)`/`(~)` with `''''` stems over a ground
  row of `_ * Y`. A mushroom whose stem reaches full height pushes over the ground plant
  immediately left/right of it: `*`/`Y` -> `\` if the mushroom is on its left, `/` if on
  its right. N == number of such plants (verified 61/61 clues before ever answering).
- molvic "N swap" — SOLVED 100%. Shelves `|A B C|` separated by `+---+`; each row has a
  majority ("home") letter. A swap is a pair of cells in the SAME COLUMN in two rows where
  each holds the other row's home letter; swap them. N == number of such pairs (52/52).
- garrow "L N slices" — 26%. Loaf `##`/`::` with 2-char items; insert `|` cuts so slices
  hold ~N cells of letter L. Right-to-left greedy accumulate-to-N. Multiple answers are
  accepted; the reference answer adds extra cuts I could not derive.
- virel "N" — 20%. Prepend one new row of boxes to the wall. Answers are always
  `[-]`*k + `[]`*m summing to the wall width; 9 boxes is the most common and best guess.
  Exact k undetermined.
- basten "N nibble" / durnel "N turn" / fennick "N fall" — only the N==0 no-op solved
  (10-13% of instances). Mechanics guessed but never confirmed.

## Demos spent (3)
1. virel — the only clue with no verb at all, so no idea of the edit. Revealed
   "prepend a row" (and that its N is not a no-op count).
2. kelmar — most frequent class, "lean" gave no hint of the glyph. Revealed `*` -> `\`,
   which unlocked the whole class (100%).
3. garrow — the only class with a header line and an unknown answer shape. Revealed
   `|` cut marks. Deliberately no demo on molvic (I had already reasoned the swap rule),
   nor basten/durnel/fennick (scene-simulation classes a single example likely
   would not have pinned down).
