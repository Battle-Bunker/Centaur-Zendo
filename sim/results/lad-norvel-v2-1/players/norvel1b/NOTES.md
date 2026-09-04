# norvel — notes

## The one class: `norvel`

DEMO 1 (window 0):
clue     : `xx..x..xx...x...x..xx..x..xx..xx/5`
solution :
```
   |1234|1234|1234|1234|1234|1234|1234|1234|
bd |xx..|x..x|x...|x...|x..x|x..x|..xx|..xx|
sn |..xx|..x.|.xxx|.xxx|x.xx|.xx.|xx..|xx..|
```
score 1.

Hard facts:
* The clue is 32 chars of `x`/`.` then `/5`.
* The **bd row is literally the clue**, cut into 8 groups of 4. Certain (32/32).
* Header row is three spaces then `|1234|` x8. Rows are `bd `/`sn ` + bars + trailing `|`.
* bd has 14 hits, sn has 18 hits. 14+18 = 32 = number of boxes.
* sn is the complement of bd in 28 of 32 boxes. The 4 odd ones:
  box 5 and box 17 = nobody plays; box 16 and box 19 = both play.
* No rotation / reflection / boolean combination of bd (searched all
  rotations, shifts and 8 boolean ops, and all pairs of rotations) reproduces sn.
* The clue's number 5 = the number of places where two bass hits sit side by
  side (`xx` at 0,7,19,26,30). Might be a checksum, might be a coincidence.

## Ten hypotheses, as I'd tell a 12-year-old

1. **Fill the gaps.** The snare hits exactly the boxes the bass drum leaves
   empty. (Right in 28 of 32 boxes — so close it is probably the core idea.)
2. **Fill the gaps, but you're allowed to be sloppy.** Any snare line that
   mostly fills the gaps counts; the marker only checks the bass row and the
   shape of the picture. (Would explain the 4 odd boxes: the computer that made
   the demo rolled dice.)
3. **Thirty-two hits in all.** Between them, the two drums must hit as many
   times as there are boxes — you can double up or leave a hole as long as the
   total comes to 32.
4. **Echo.** The snare plays the bass drum's pattern again, five boxes later.
5. **Anticipation.** The snare plays the bass drum's pattern five boxes early.
6. **Mirror.** The snare plays the bass line backwards (or backwards-and-
   opposite).
7. **Five snare hits, spread out evenly** over the whole 32 boxes — the number
   after the slash says how many times the snare hits.
8. **Every fifth box.** The snare hits box 1, 6, 11, 16 … (the number is a
   spacing, not a count).
9. **Backbeat.** The snare just plays the ordinary "2 and 4" a drummer always
   plays, and the number is only there to tell you how loud/fast.
10. **The number is a receipt, not an instruction.** 5 = how many times the bass
    plays two hits in a row; you only have to draw the picture, and the snare is
    whatever fills in around the bass.

## Plan
Probe round 1 by giving every challenge the same picture format but a different
snare line, cycling through the hypotheses. A 1 anywhere tells me which one is
right. Also harvest clues to see whether the number varies and whether the
pattern length is always 32.

## What I ended up believing (after 6 rounds, 4 demos)

`norvel` — clue `<pattern>/<N>`. The answer is a two-line drum grid: line 1 is
the clue pattern cut into bars of four (labels and header line are free — the
four demos used bd/sn, drum/tap, kick/snare, foot/hand), line 2 is a second
drum that fills the first drum's rests.

The graded part is line 2, and what it is graded on is (mostly) **how many
boxes are left completely silent** — boxes where neither drum plays:
* 0 or 1 silent boxes: always wrong (the exact "fills every gap" answer scores 0).
* the right count goes DOWN as N goes up: N=2 wants ~6, N=8 wants exactly 2.
* silences must be spread out and isolated; clumping them, or letting the two
  drums hit together, scores worse.
Confidence: high that the silence count is the lever (0/259 for 0 silences,
31/31 for N=8 with 2), low that it is the whole rule — the best count still
only scores 30-100% depending on N, so something positional or clue-dependent
remains.

## Round log
| round | correct/answered | what I was testing |
|---|---|---|
| 1 | 9/500 | 26 fixed hypotheses for line 2, cycled by index |
| 2 | 19/506 | 20 randomised families (density, overlaps, holes, formats) |
| 3 | 53/500 | hole count 0-8 x answer format/labels |
| 4 | 55/505 | target line-2 density 0.46-0.64 |
| 5 | 114/598 | rules for the silence count vs N |
| 6 | 208/649 | per-N silence sweep (base-1, base, base+1) |
| final | 1328/2728 | per-(N, rest-count) table |
