# LegoZendo

Clue = LETTER (A-Z) + N where N in {0,2,3,...,12}.  (N=1 NEVER appears -> big hint)
Answer = ASCII grid.  Bricks: 2 rows tall, width = 3*studs.  Background = any
non-letter char ('.', '~', '#' all accepted; no background at all also accepted).

## RULE (confidence high)
N == number of studs in the LARGEST connected same-colour region of the clue's
letter.  Size-1 regions read as 0 (hence no N=1 clues).

Evidence:
- demo Y3: Y region = 3 studs (3-wide + 6-wide, touching)  -> 3
- demo X4: X regions = {2+2=4}, {1}  -> 4
- demo J7: J regions = {3+4=7}, {1}  -> 7
- probe v7 (J7 shape all one letter, 11 studs, all connected) hit ONLY N=11
- probe v8 (Y3 shape all one letter, 5 studs) hit ONLY N=5, letter must equal clue letter
- N=0 hits: grids where clue letter absent, OR present as a lone 1-stud brick
