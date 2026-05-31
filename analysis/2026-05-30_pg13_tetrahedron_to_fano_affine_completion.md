# PG(1,3) / Tetrahedron to Fano Affine Completion

Date: 2026-05-30

This lifts the single `C3` qutrit triangle to the full seven-point Fano plane.

Previous theorem:

```text
C3 = A4 ∩ S3
```

is the cyclic orientation of the three non-anchor points of `PG(1,3)`. After labeling those three points by the nonzero vectors of `F2^2`, the same `C3` is the orientation-preserving automorphism group of a Fano-line triple.

This theorem explains where that Fano line sits inside the full Fano plane.

## Main construction

Identify the four points of

```text
PG(1,3)
```

or the four vertices of a tetrahedron with the affine plane

```text
AG(2,2) = F2^2.
```

So the four tetrahedral points are:

```text
(0,0), (1,0), (0,1), (1,1).
```

The three nonzero vectors

```text
(1,0), (0,1), (1,1)
```

are the three directions of this affine plane.

Completing the affine plane by adding its three directions at infinity gives

```text
PG(2,2),
```

the Fano plane.

Thus:

```text
Fano plane = AG(2,2) affine tetrahedron + line at infinity.
```

## Anchor-local triangle

Fix an affine anchor point `p`.

The other three affine points `q` determine three direction vectors:

```text
q - p.
```

Over `F2`, subtraction is the same as addition, so:

```text
q - p = q + p.
```

The verifier checks that for every anchor `p`, the three non-anchor points give exactly the three nonzero directions of `F2^2`.

Therefore:

```text
local non-anchor triangle at p = line-at-infinity direction triple.
```

So the local `C3` qutrit triangle selects the oriented line at infinity in the Fano completion.

## Full Fano plane check

The verifier builds the full Fano plane from:

```text
4 affine points + 3 infinity directions.
```

It checks:

```text
7 points
7 lines
3 points per line
3 lines through each point
each pair lies on exactly one line
```

The seven lines are:

```text
1 line at infinity
6 affine lines
```

The six affine lines split into:

```text
3 parallel classes of 2 lines.
```

Each parallel class meets at one of the three infinity directions.

## Orientation

Choose the cyclic direction order:

```text
(1,0) -> (0,1) -> (1,1) -> (1,0).
```

This is the `C3` orientation.

It orients the Fano line at infinity and supplies the local wedge orientation of the triple.

The Fano sum law on the line at infinity is:

```text
(1,0) + (0,1) = (1,1)
(0,1) + (1,1) = (1,0)
(1,1) + (1,0) = (0,1)
```

So the local non-anchor qutrit triangle has become the oriented Fano-line law.

## Correct bridge

The correct bridge is:

```text
PG(1,3) / tetrahedron:
    four-point projective/tetrahedral object

AG(2,2):
    affine chart with four points

Fano plane PG(2,2):
    AG(2,2) plus line at infinity

C3 overlap:
    cyclic orientation of the line at infinity
```

So the four-point tetrahedral geometry does not equal the seven-point Fano plane. It is an affine chart inside the Fano plane.

The missing three points are the directions at infinity.

## Compressed theorem

```text
The four points of PG(1,3)/tetrahedral geometry can be modeled as AG(2,2). For any chosen anchor, the three remaining points translate to the three nonzero directions of F2^2. Adding those three directions as points at infinity completes AG(2,2) to the Fano plane PG(2,2). The C3 overlap orients this line at infinity, and the local non-anchor qutrit triangle becomes the oriented Fano-line triple u+v=w.
```

## Honest boundary

This proves the affine completion bridge. The next hard step is to connect this affine Fano chart to the global Fano wedge-dot codec on seven Csaszar/Szilassi axes and determine whether changing the anchor corresponds to changing affine charts in the same Fano plane.
