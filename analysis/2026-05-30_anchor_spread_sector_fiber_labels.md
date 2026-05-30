# Anchor Spread-Sector Fiber Labels

Date: 2026-05-30

This executes the next test after the symplectic projection fiber theorem.

The existing spread audit proves:

```text
W(3,3) has 36 symplectic spreads.
Fix an anchor p.
The four isotropic lines through p split the 36 spreads into four sectors of size 9.
Each spread is one memory line through p plus 9 affine measurement lines.
```

The new test asks whether those nine spreads in a fixed sector are actually the same kind of nine-label affine object as the 9-point fiber in

```text
PG(5,3) -> PG(3,3).
```

## Setup

Fix an anchor point p.

The local shell splits as:

```text
p^perp = PG(2,3), size 13
AG(3,3) affine complement, size 27
```

The four isotropic lines through p are the four memory-line sectors.

Choose one anchor line L through p. Then:

```text
36 spreads / 4 anchor lines = 9 spreads in the L-sector.
```

The allowed affine directions for that sector are the nine points of

```text
p^perp \ L.
```

So there are:

```text
13 - 4 = 9
```

allowed directions.

## New checked bijection

For a fixed sector L and a fixed allowed affine direction d, look at the nine affine lines of direction d in the 27-point affine bulk.

The verifier checks:

```text
spread -> the affine line of direction d contained in that spread
```

is a bijection from:

```text
9 spreads in the L-sector
```

to:

```text
9 parallel affine lines of direction d.
```

It checks this for every one of the four sectors and every one of the nine directions in that sector.

So:

```text
4 sectors * 9 directions
```

all pass the same 9-label bijection test.

## Meaning

This proves that the nine spreads in a fixed anchor-line sector are coordinatized by the nine labels of an affine quotient:

```text
AG(3,3) / direction ≅ F3^2.
```

That is exactly the same abstract nine-label object as the projection fiber in

```text
PG(5,3) -> W33.
```

Therefore the previous count

```text
36 = 4 * 9
```

now has a direct geometric interpretation:

```text
4 = choice of memory line through the anchor
9 = choice of affine F3^2 fiber label / parallel affine line in a chosen direction
```

## Relation to PG(5,3) projection

The previous projection theorem showed:

```text
364 = 40*9 + 4.
```

The new spread-sector theorem shows that the 9 appearing there is not merely a fiber size. It is the exact label set that classifies the nine spreads inside a fixed anchor-line sector.

So the local dictionary is:

```text
PG(5,3) projection fiber:
    9 points of an affine F3^2 plane

Spread sector at anchor:
    9 spreads, equivalently 9 parallel affine lines in any allowed direction
```

These are now verified as the same finite affine label type.

## Compressed theorem

```text
Fix an anchor p and an anchor line L through p. The nine spreads containing L are in canonical bijection with the nine parallel affine lines of any chosen allowed direction d in p^perp\L. Thus each sector is an affine F3^2 label set. Consequently 36=4*9 means four memory-line sectors times nine affine fiber labels, matching the 9-fibers in the projection PG(5,3)->PG(3,3).
```

## Honest boundary

This proves the sector/fiber label bijection at the incidence level. The next hard test is to build a canonical coordinate map between the PG(5,3) fiber coordinates and the spread-sector affine-line labels, not just prove that both are 9-element affine planes.
