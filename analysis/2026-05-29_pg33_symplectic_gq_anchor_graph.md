# PG(3,3) Symplectic GQ / W33 Anchor Graph Theorem

Date: 2026-05-29

This is the exact next step after the PG(3,3) phase-space spread bridge.

The previous theorem showed:

```text
81 = |F3^4|
40 = |PG(3,3)_points|
```

so the 40 W33 anchors are the projectivized nonzero directions of the global four-mode qutrit phase space.

The new theorem adds the missing relation: W33 is not merely the point set of PG(3,3). It is the symplectic generalized quadrangle W(3,3) inside PG(3,3).

## Symplectic form

Work in F3^4 with the standard alternating form

```text
<x,y> = x0*y2 + x1*y3 - x2*y0 - x3*y1 mod 3.
```

Every projective point is isotropic because the form is alternating. But only some projective lines are totally isotropic.

Those totally isotropic lines are the lines of the generalized quadrangle W(3,3).

## Verified incidence geometry

The verifier constructs PG(3,3), all projective lines, and all totally isotropic lines.

It checks:

```text
F3^4 phase states = 81
PG(3,3) points = 40
all PG(3,3) lines = 130
totally isotropic lines = 40
points per isotropic line = 4
isotropic lines per point = 4
polar plane size per point = 13
```

So the W33 incidence geometry is:

```text
40 points, 40 lines, 4 points/line, 4 lines/point.
```

This is exactly the generalized quadrangle W(3,3).

## W33 collinearity graph

Define two points to be adjacent if they lie on a common totally isotropic line.

The verifier checks that the resulting collinearity graph has:

```text
vertices = 40
degree = 12
edges = 240
```

and strongly regular parameters:

```text
(40,12,2,4).
```

That means:

```text
each adjacent pair has 2 common neighbors
each non-adjacent pair has 4 common neighbors
```

The spectrum is:

```text
12^1 + 2^24 + (-4)^15.
```

So the W33 graph itself is exactly recovered as the collinearity graph of the symplectic GQ.

## Spread-router bridge survives

The verifier also constructs a spread of totally isotropic lines:

```text
10 disjoint isotropic lines partition the 40 points.
```

Each line has 4 points. Therefore:

```text
40 = 10 * 4.
```

The X-ray count remains:

```text
160 = 10 * 16 = 40 * 4.
```

So the spread bridge is now symplectic, not merely projective:

```text
E1 = 10 spread lines
chi = 4 points per isotropic line
Q4 = 16 router states per spread line
```

## Factorization

The global factorization remains:

```text
51840 = 40 * 16 * 81.
```

But the terms now have their sharpest meanings:

```text
40 = points of symplectic W(3,3) inside PG(3,3)
16 = Q4 router / Cl4 / D8 / codec state count
81 = F3^4 qutrit phase-state count
```

So:

```text
|W(E6)| = symplectic PG(3,3) anchors * Q4 router states * F3^4 phase states.
```

## Relation to earlier codec stack

The structure now aligns as:

```text
F3^4:
    global qutrit phase space, 81 states

PG(3,3):
    projectivized anchor space, 40 points

W(3,3):
    symplectic generalized quadrangle incidence inside PG(3,3)

W33 graph:
    collinearity graph, 40 vertices, 240 edges, degree 12

Q4:
    router/codec layer attached to symplectic spread lines
```

This upgrades the previous picture from projective-count matching to actual symplectic incidence geometry.

## Compressed theorem

```text
The four qutrit modes form F3^4. Projectivizing nonzero vectors gives the 40 points of PG(3,3). Imposing the standard alternating symplectic form selects 40 totally isotropic lines, each with 4 points and 4 lines through each point. The collinearity graph of this incidence geometry has 40 vertices, degree 12, 240 edges, strongly regular parameters (40,12,2,4), and spectrum 12^1 + 2^24 + (-4)^15. This is W(3,3). Therefore the W33 anchor graph is the symplectic collinearity graph of the global qutrit phase space.
```

## Honest boundary

This proves the W33 anchor graph from PG(3,3) symplectic incidence. The next valid test is to attach the Q4 router to an isotropic line spread and check whether the 10 spread lines times 16 Q4 states produce the 160 minimal X-rays with the correct 3-adic overlap distribution.
