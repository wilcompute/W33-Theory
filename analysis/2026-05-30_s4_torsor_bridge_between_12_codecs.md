# S4 Torsor Bridge Between the Two 12-Codecs

Date: 2026-05-30

This continues the comparison between the two native 12-codecs.

Previous theorem:

```text
line-pair 12-codec = Borel/basis codec in GL(2,3)
tetrahedral 12-codec = A4 alternating/chiral codec
```

They both have 12 elements, but they are not isomorphic as groups.

This theorem identifies the correct bridge.

## Two regular torsors

The tetrahedral chiral codec is

```text
A4
```

and acts simply transitively on the oriented tetrahedral flags.

The line-basis codec is the Borel subgroup

```text
B < GL(2,3)
```

fixing the anchor point on `PG(1,3)`. It acts simply transitively on signed anchored line-bases.

So both are 12-element regular torsors, but for different groups:

```text
A4 torsor: chiral/even tetrahedral flags
Borel torsor: signed anchored line bases
```

## Shared ambient S4 geometry

The bridge is the common ambient four-point geometry:

```text
PGL(2,3) ~= S4.
```

The verifier checks:

```text
|PGL(2,3)| = 24
```

by its faithful action on the four points of `PG(1,3)`.

Inside this `S4`, let

```text
H = S3
```

be the stabilizer of the anchor point.

Then:

```text
|A4| = 12
|H| = 6
|A4 ∩ H| = 3
```

and the verifier checks the factorization

```text
S4 = A4 H.
```

Because the intersection has size 3, every element of `S4` has exactly 3 decompositions

```text
s = a h,
```

with

```text
a in A4, h in H.
```

## Borel projective image

The Borel line-basis codec has order 12 in `GL(2,3)`.

Projectivizing by the central sign sends it to

```text
H = S3 < S4.
```

The verifier checks:

```text
Borel order = 12
projective image order = 6
kernel over projective image has size 2
```

Thus:

```text
Borel -> S3 point stabilizer
```

while

```text
A4 -> chiral/even tetrahedral subgroup.
```

## Correct bridge

The bridge between the two 12-codecs is not a group isomorphism.

It is a torsor/incidence bridge through the ambient `S4`:

```text
A4 --inside--> S4 <--inside/projective image-- S3 <--double cover-- Borel
```

with

```text
S4 = A4 S3,
A4 ∩ S3 = C3.
```

So the correspondence has a natural 3-fold overlap coming from the common cyclic subgroup.

## Interpretation

The recurring 12 splits into two native forms:

```text
A4-type 12:
    tetrahedral chirality / even rotations / oriented flags

Borel-type 12:
    signed anchored bases on PG(1,3) / line-pair symplectic codec
```

They are related because both live over the same four-point `S4` geometry, but they preserve different structures:

```text
A4 preserves chirality.
Borel preserves a chosen anchor point and signed basis data.
```

## Compressed theorem

```text
The two 12-codecs are non-isomorphic regular torsors. The tetrahedral codec is the A4 torsor of oriented chiral flags. The line-pair codec is the Borel torsor of signed anchored line-bases. They meet through PGL(2,3)=S4: the Borel projectivizes to an S3 point stabilizer H, while A4 is the even subgroup, and S4=A4H with A4∩H=C3. Thus the bridge is a 3-fold S4 incidence correspondence, not a canonical group identification.
```

## Honest boundary

This proves the group-theoretic bridge. The next hard step is to see whether the C3 overlap corresponds geometrically to the three non-anchor points on the input line, the three cyclic rotations of a Fano line, or the three orientations inside the local qutrit triangle.
