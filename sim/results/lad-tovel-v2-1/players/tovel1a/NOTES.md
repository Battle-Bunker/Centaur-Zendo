# tovel — hypothesis log (team tovel1a)

Clue format `A/B/C/D/E`:
  A in {28..31}  days in the month
  B in {0..6}    weekday of day 1 (Mon=0)
  C in A..Z      the "marked" letter
  D in {2..6}    controls how long the C run must be
  E in {1..26}   the day the C run starts.  (B+E-1)%7 is ALWAYS 0,1 or 2.

Answer = the month drawn as a calendar, each day tagged with a letter.
Cell = "%2d%s" (day right-aligned in 2, then the letter), cells joined by one
space, seven per row, leading blanks for B, each line rstripped, header row
first.  Header text is NOT checked (the two demos used different headers).

The grader is a PREDICATE, not string equality: many letterings score 1.
Confirmed necessary: day E carries C; C occupies a contiguous run starting at
day E whose length is fixed by D; other days may be anything (D other letters
cycling works).

Run length that scores (block starts at day E):
  D=2 -> 4 days   D=3 -> 9   D=4 -> 10   D=5 -> 11   D=6 -> 16
Equivalently "cover W(D) Mon-Fri days from day E":
  W = {2:4, 3:7, 4:8, 5:9, 6:12}.
Verified 100% for D=3,4,6 at every weekday of E.
STILL UNSOLVED: D=2 and D=5 when day E falls on a Wednesday ((B+E-1)%7==2).
Both the fixed-length and the fixed-weekday-count blocks fail there; the
correct block for that corner is something else.

Round history: 0/498, 5/480, 65/502, 54/504, 30/468, 173/492, FINAL 2613/2954.
