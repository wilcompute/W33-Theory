# Symplectic Projection Fiber Lines

Date: 2026-05-30

This adds the symplectic form to the projection tower

```text
PG(5,3) -> PG(3,3)=W33.
```

The previous projection theorem showed:

```text
364 = 40*9 + 4.
```

So the three-qutrit projective Pauli space projects to W33 with:

```text
40 affine fibers of size 9
plus a kernel PG(1,3) of size 4.
```

This theorem verifies the internal symplectic geometry of those 9-point fibers.

## Fiber geometry

Each fiber over a W33 anchor is an affine F3^2 plane with 9 points.

With the 3-qutrit symplectic form, the internal commuting graph of one fiber has:

```text
9 vertices
12 edges
degree distribution: one vertex of degree 8, eight vertices of degree 2
```

So each fiber is:

```text
four qutrit affine lines through a central zero point.
```

Equivalently:

```text
four triangles sharing one central point.
```

This is exactly the local pattern the live index keeps suggesting: four qutrit memory/measurement directions, each a 3-point line.

## Kernel directions

The kernel is

```text
PG(1,3)
```

with four projective points.

These four kernel points are the four directions of each affine F3^2 fiber.

The verifier checks:

```text
4 kernel directions
each direction line has 3 fiber points
the eight nonzero fiber points are partitioned by those four directions
the zero point lies on all four direction lines
```

Across all 40 fibers, each kernel direction selects

```text
40 * 3 = 120
```

fiber points.

So the kernel is not leftover noise. It is the line-at-infinity / direction selector for the affine 9-fibers.

## Cross-fiber commutation

For two W33 base anchors, there are two cases.

If the base anchors commute / are adjacent in W33:

```text
there are 33 commuting pairs between their two 9-point fibers.
```

If the base anchors do not commute:

```text
there are 24 commuting pairs between their two 9-point fibers.
```

The verifier checks this uniformly across all base pairs:

```text
240 base-commuting pairs -> 33 fiber-commuting pairs each
540 base-noncommuting pairs -> 24 fiber-commuting pairs each
```

The difference is exactly:

```text
33 - 24 = 9.
```

So adjacency in the W33 base appears as one extra affine fiber plane worth of commuting lifts.

## Interpretation

The projection

```text
PG(5,3) -> W33
```

is not merely a count identity. It has the local symplectic structure:

```text
fiber = affine F3^2 plane
kernel = PG(1,3) directions at infinity
fiber lines = four qutrit measurement triangles
base adjacency = +9 extra commuting fiber lifts
```

This makes the earlier identities concrete:

```text
364 = 40*9 + 4
36 = 4*9
```

The 9 is the affine fiber size, and the 4 is the kernel/projective direction count.

## Compressed theorem

```text
Under PG(5,3)->PG(3,3), each W33 anchor has a 9-point affine fiber F3^2. The kernel PG(1,3) consists of four direction points, and each direction selects one 3-point affine line in every fiber. Internally each fiber is four qutrit triangles sharing a central point. Between two fibers, W33-adjacent base anchors have 33 commuting lifts while nonadjacent anchors have 24; the adjacency excess is exactly 9, one affine fiber's worth.
```

## Honest boundary

This proves the symplectic fiber-line structure for the n=3 to n=2 projection. The next test is to identify the 9 fiber labels with the nine affine measurement-frame labels from the 36-spread audit, i.e. prove that the four kernel directions times nine affine fiber labels reproduce the 36 spread choices relative to an anchor.
