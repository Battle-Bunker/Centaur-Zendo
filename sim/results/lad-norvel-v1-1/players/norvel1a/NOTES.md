# norvel — notes

Only ONE class: `norvel`. Clue = `<pattern>/<N>`, pattern is x/. of length 16/20/24/28
(always multiple of 4), N in 2..5. Pattern always starts with 'x'.

Answer format (exact, from demos):
```
drum |xx..|..xx|x...|x..x|x..x|...x|
clap |x.xx|xx..|xxxx|.xx.|xxx.|.xx.|
 tap |.xx.|x.x.|.xxx|.xxx|.xx.|xxx.|
```
labels right-aligned to width 4, space, then bars of 4 slots separated/bounded by '|',
lines joined by '\n', no trailing newline.

## Facts from 2 demos
- drum line == clue pattern EXACTLY (both demos).
- per-beat count of playing voices: min 1, max 2 in BOTH demos (N=2 and N=3).
  => every beat has >=1 voice; never all 3 at once.
- max consecutive rests: drum 4 / 5 (exceeds N, it's given), clap & tap == N exactly
  in both demos (2 with N=2, 3 with N=3).  => hypothesis: added voices must have
  gap <= N.
- every voice has >=1 hit in every bar (both demos).
- densities: demo1 10/16/15 of 24; demo2 9/19/19 of 28.

## Round 1 (546 presented, 0 correct)
Tested 10 degenerate candidates incl. clap=comp/tap=comp, alternating x.x./.x.x,
all-x, all-dots, 1/2/4 voices, swapped drum. ALL 0.
So: coverage+max2+distinct is NOT sufficient (the alternating candidate satisfied
those and still failed) -> gap<=N or another rule is real.

## Round 2 (441, 30 correct = 6.8%) and Round 3 (564, 10 = 1.8%)
CONFIRMED (round 3 structural sweep):
- exactly 3 voice lines (2 voices 0/71, 4 voices 0/71)
- first line's pattern must equal the clue pattern (random first line 0/70)
- instrument NAMES are irrelevant: demo 3 used `foot/hand/voice` (label width =
  longest name), demo 1&2 used `drum/clap/tap`; both score the same for me.
- every beat must have >=1 instrument (all 43 correct answers; violating = 0)
- at most 2 instruments per beat matters a lot: r3 cover-only 2.8% vs cover+cap2 8.7%
  (2 correct answers did contain a triple, both with N>=3, so cap may be min(N,3)
   or triples are just rare/tolerated)
RULED OUT as hard rules (each violated by at least one *correct* answer):
- per-voice max gap <= N (a correct answer had a voice resting 13 beats)
- per-voice hits per bar >= 1; per-voice density; no-triple with N>=3
- any forbidden local chord bigram/trigram (mined: none)
- any single scalar necessary condition separating correct from wrong (~120 tried)
Difficulty depends on the clue: hit rate by (N, drum max gap): (2,3)=24%, (2,4)=17%,
(2,5)=7.5%, (4,3)=5%, (5,3)=5.5%, (3,4)=0%, (4,5)=0%, (5,4)=0%.
Reference-solver style (3 demos): at drum-rest beats BOTH other voices play ~78% of
the time; at drum-hit beats one other voice doubles ~50% of the time; max 2 always.

## Rounds 4-6 (parameter search inside cover+cap2)
Sampler: at a drum-REST beat both other voices play with prob p_both, else exactly
one (50/50); at a drum-HIT beat one other voice doubles with prob p_dbl, else the
drum plays alone.  Structurally guarantees cover + max 2.
 (p_both,p_dbl)  hit rate
 (0.50,0.50)  7.7%   (0.78,0.80)  7.7%   (0.30,0.30) 11%
 (0.95,0.50) 19.8%   (0.78,0.50) 20.7%
 (0.78,0.10) 26.1%   (0.78,0.20) 30.7% (n=329)  <-- best
 n2-targeting / N-adaptive variants: 18.5%
 alternate-single 29.4%; clap-only doubling 20.3%; 80%-clap single 22.9%
 => the two added voices must be treated SYMMETRICALLY; doubling drum hits is bad.
FINAL: 780 / 2941 = 26.5%
