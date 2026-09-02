# quaich — solved

Clue: string over {-, |, /}, even length 12–18, uniformly random.

Answer: rearrange the clue's characters (always an exact anagram).
Every character is matched with one of a **different** kind. With
a=#'-', b=#'|', c=#'/', the pair multiplicities are forced:

    p = (a+b-c)/2   pairs (-,|)
    q = a - p       pairs (/,-)
    r = b - p       pairs (/,|)

The answer writes each pair-class as a "block" x^k y^k, in a fixed
block order, with a fixed leading character per block:

    r>0 and q>0 :  /^r |^r   -^p |^p   /^q -^q
    r == 0      :  -^q /^q   -^p |^p
    q == 0      :  |^p -^p   |^r /^r

Extra constraint discovered empirically: **the first block may not be
longer than the last block.** If it would be, split the first block into
unit blocks ("/|"*r, "-/"*q, "|-"*p respectively). Any other split of the
middle block is also accepted, so the checker validates a family, not one
exact string.

Final: 3539/3539.
