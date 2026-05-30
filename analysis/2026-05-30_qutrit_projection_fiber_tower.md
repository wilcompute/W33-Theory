# Qutrit Projection Fiber Tower

Date: 2026-05-30

This executes the next hard test from the qutrit Pauli hierarchy recursion.

The projective n-qutrit Pauli space over q=3 is

```text
PG(2n-1,3)
```

with point count

```text
N_n = (3^(2n)-1)/2.
```

The previous theorem proved the recursion

```text
N_n = 9 N_(n-1) + 4.
```

This theorem proves a geometric projection law over the W33 base.

## Projection to W33

For n>=2, project

```text
PG(2n-1,3) -> PG(3,3)
```

by forgetting the last

```text
2(n-2)
```

coordinates.

The base

```text
PG(3,3)
```

has 40 points, which are the W33 anchors.

The projection is undefined on the projective kernel where the first four coordinates vanish.

## Fiber law

For n>=3:

```text
N_n = 40 * 3^(2n-4) + N_(n-2).
```

Here:

```text
40 = W33 anchors
3^(2n-4) = affine fiber size over each W33 anchor
N_(n-2) = projective kernel
```

So the higher qutrit projective geometries are W33-indexed affine fiber towers plus a lower-level projective kernel.

## Verified cases

### n=3

```text
PG(5,3): 364 points
```

Projection to W33 gives:

```text
40 base points
fiber size 9 over every base point
kernel size 4
```

Therefore:

```text
364 = 40*9 + 4.
```

Interpretation:

```text
three-qutrit projective Pauli geometry = W33 anchors with affine 9-fibers plus a one-qutrit kernel PG(1,3).
```

### n=4

```text
PG(7,3): 3280 points
```

Projection to W33 gives:

```text
40 base points
fiber size 81 over every base point
kernel size 40
```

Therefore:

```text
3280 = 40*81 + 40.
```

Interpretation:

```text
four-qutrit projective Pauli geometry = W33 anchors with affine 81-fibers plus a W33 kernel PG(3,3).
```

### n=5

```text
PG(9,3): 29524 points
```

Projection to W33 gives:

```text
40 base points
fiber size 729 over every base point
kernel size 364
```

Therefore:

```text
29524 = 40*729 + 364.
```

## Why this matters

This turns the hierarchy from a count recursion into geometry.

The W33 object is the stable base:

```text
PG(3,3) = W33 anchor space.
```

Higher qutrit spaces project onto W33 with uniform affine fibers:

```text
9, 81, 729, ...
```

The leftover kernel is not noise. It is the lower qutrit projective hierarchy:

```text
N_(n-2).
```

Thus the tower has a two-step recursive structure:

```text
higher qutrit space = W33-indexed affine 9-adic fibers + lower qutrit kernel.
```

## Relation to spread frames

For n=3:

```text
364 = 40*9 + 4.
```

The 9-fiber is the affine measurement-frame component that appeared in

```text
36 = 4*9.
```

So the spread-frame layer is literally the affine fiber over each W33 anchor, paired with the four anchor-line sectors.

For n=4:

```text
3280 = 40*81 + 40.
```

The 81-fiber is the full four-mode qutrit phase space over each W33 anchor, with a W33 kernel.

This connects the hierarchy back to the global factorization:

```text
51840 = 40 * 16 * 81.
```

The 81 is not arbitrary: it is exactly the n=4 projection fiber size over each W33 anchor.

## Compressed theorem

```text
Projecting PG(2n-1,3) to the first four coordinates gives a map to PG(3,3)=W33. Off the kernel, every W33 anchor has uniform fiber size 3^(2n-4), and the kernel is PG(2n-5,3) with N_(n-2) points. Hence N_n = 40*3^(2n-4)+N_(n-2). In particular, 364=40*9+4 and 3280=40*81+40.
```

## Honest boundary

This proves the projective fiber law. The next hard step is to add the symplectic form: determine which fibers preserve isotropic/commuting structure and whether the n=3 fiber over each W33 anchor carries the expected 9 affine measurement-frame labels from the spread audit.
