# Index Read Correction and Local Shell Repair

Date: 2026-05-30

This note records the correction after reading the live `docs/index.html` page directly instead of relying only on search hits.

The page contains more than theorem titles. It gives the working local dictionary:

```text
W(3,3) = SRG(40,12,2,4)
local shell = 13 + 27
13 = anchor + four qutrit triangles
27 = affine Heisenberg shell
36 = 4 * 9 spread/MUB frame split
```

The important discipline point is that the raw local 27-node non-neighbor shell and the later Witting/Schlaefli packet shell should not be conflated.

## q=3 selector

The page emphasizes the coincidence/equality

```text
q^5 - q = edge count of GQ(q,q)
```

For a generalized quadrangle of order `(q,q)`, the point count and collinearity degree are

```text
points = (q+1)(q^2+1)
degree = q(q+1)
```

so the point-graph edge count is

```text
q(q+1)^2(q^2+1)/2.
```

The equality

```text
q^5 - q = q(q+1)^2(q^2+1)/2
```

reduces, for q>0, to

```text
2(q-1)=q+1,
```

hence

```text
q=3.
```

At q=3:

```text
q^5-q = 240
GQ edge count = 240
points = 40
degree = 12
```

So q=3 is selected by the equality between the Frobenius-style count and the W(3,3) point-graph edge count.

## Local shell stats

The pushed verifier `analysis/w33_local_27_shell_stats.py` checks the actual local induced subgraphs in the symplectic W(3,3) graph.

For any anchor:

```text
1 anchor + 12 neighbors + 27 non-neighbors = 40.
```

The 12-neighbor shell is exactly four triangles:

```text
12 = 4 * 3.
```

The raw 27-node non-neighbor induced graph has:

```text
27 vertices
8-regular internal degree
108 internal edges
```

So the raw 27 shell is not itself the complement Schlaefli graph, which would be 10-regular. The Schlaefli/Witting bridge remains meaningful, but it runs through the balanced packet / Heisenberg chart layer, not through the raw second-subconstituent adjacency alone.

## Why this matters

The live index is doing two things at once:

1. It describes the exact local W(3,3) shell:

```text
13 + 27 = PG(2,3) tangent screen + AG(3,3) affine bulk.
```

2. It describes a later packet construction in which 27 balanced packets recover an `F3^2 x F3` Heisenberg chart and a Witting/Schlaefli-style shell.

Those are connected, but they should not be collapsed into the same raw graph.

## Correct local dictionary

```text
anchor:
    1 distinguished projective point

neighbor shell:
    12 = 4 qutrit triangles = four isotropic lines through the anchor, excluding the anchor itself

tangent screen:
    13 = anchor + 12 neighbors = PG(2,3)

affine bulk:
    27 = AG(3,3), organized as nine size-3 fibers in a chosen affine direction

spread layer:
    36 = 4 anchor-line sectors * 9 affine measurement frames
```

## Next target

The next hard test is to connect the raw 27-node affine bulk graph to the balanced 27-packet Heisenberg chart by an explicit quotient or transform, rather than assuming the raw second subconstituent already is the final packet graph.
