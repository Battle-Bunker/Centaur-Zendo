# tovel1a — notes

Universal format: every class is a picture plus a count line ("N verb"; garrow puts it
on the FIRST line). Answer = the picture with the operation applied N times.
N=0 => echo the clue verbatim scores 1. That was discovered in round 1 by echoing
every 4th clue, and it is the whole free baseline (~13% of the pool).

## Solved
- basten (fish/weeds, "nibble"): every fish whose *facing* direction contains a reed
  swims up to it and eats the reed's TOP segment — but only if |reed_top_row - fish_row| <= 1.
  N is DERIVED (44/44 clues), not a budget. 100% in rounds 2,3,4 and the final.
- kelmar (trees/ground, "lean"): a tree whose trunk reaches the lowest air row makes the
  ground cell immediately left become '/' and immediately right become '\' (both '*' and 'Y'
  lean). N derived (48/48). 100%.
- durnel (trucks/bridges, "turn"): a truck drives to the first '\_/' bay in its facing
  direction, parks there and reverses; blocked if a '#' bridge in the path is lower than its
  cargo stack. N is a budget; tallest cargo first, leftmost tie-break. ~83-87%.
- molvic (shop shelves, "home"): a misplaced item returns to its own shelf. Operation
  confirmed (source cell becomes '___'), selection rule only partly pinned down
  (best consistent guess: rightmost-column item first, first gap in the home row). ~20%.

## Not cracked (30+ hypotheses each conclusively eliminated)
garrow ("slices"), norvel ("slip"), tovel ("bump"). Answered only the N=0 cases and
skipped the rest — skipping is instant, so the round runs further and the solved
classes deliver more points.
