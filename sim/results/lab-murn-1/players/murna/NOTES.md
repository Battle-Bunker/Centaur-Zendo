# murn — solved

Clue: `<row>|<n>`, row over {'.','o','#'}.
Answer: newline-separated grid, all rows len(row).

Constraints (verified: 21 TP / 0 FP / 0 FN over 1464 scored samples):
1. last row == clue row
2. total '#' across the whole grid == n
3. for adjacent rows a (above) / b (below), at each i, with
   d = #dots among b[i-1],b[i],b[i+1] (off-end counts as '.'):
       a[i]=='#' requires d==1 ; a[i]=='o' requires d==2 ; a[i]=='.' free.

Solver: build upward from the clue, spend the '#' budget on d==1 cells,
fill d==2 cells with free 'o' to keep density (capacity) for the level above;
6 periodic masks as fallbacks. 819/819 clues solvable, 0.017 ms each.
