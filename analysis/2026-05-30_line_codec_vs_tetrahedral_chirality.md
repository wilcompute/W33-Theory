# Line Codec vs Tetrahedral Chirality

Date: 2026-05-30

This compares the new 12-codec from anchored line-pair transport with the earlier tetrahedral chiral 12-codec.

The key question was:

```text
Are these two 12-codecs canonically the same, or only count-equivalent?
```

The answer is:

```text
They are count-equivalent but not naturally the same group.
```

## Line-pair 12-codec

The line-pair theorem identified the 12 states over

```text
([a], L_in, L_out)
```

as choices of a signed input-line basis `(a,b)` with `[a]` fixed.

On the projective input line

```text
PG(1,3),
```

choose coordinates so the anchor is `[e0]`.

The 12 signed basis choices are exactly matrices of the form

```text
[ alpha   x  ]
[   0   delta ]
```

where

```text
alpha, delta in F3^*, x in F3.
```

This is the Borel point-stabilizer in

```text
GL(2,3).
```

It has order

```text
2 * 2 * 3 = 12.
```

The verifier checks:

```text
|B| = 12
center size = 2
B has elements of order 6
```

Its projective image has order 6 and is the point stabilizer

```text
S3 < PGL(2,3) ~= S4.
```

So the line-pair 12-codec is a Borel/basis codec.

## Tetrahedral chiral 12-codec

The tetrahedral chiral codec is

```text
A4,
```

the even permutations / rotational symmetries of the tetrahedron.

The verifier checks:

```text
|A4| = 12
center is trivial
A4 has no elements of order 6
```

So the tetrahedral 12-codec is an alternating/chiral codec.

## Not isomorphic

The line-codec group and tetrahedral chiral group both have order 12, but they are not isomorphic.

Reason:

```text
Borel codec:
    center size 2
    has elements of order 6

A4 codec:
    center size 1
    no elements of order 6
```

Therefore:

```text
line-pair 12-codec != tetrahedral chiral 12-codec
```

as native groups.

## Ambient bridge through S4

They are still related through the same ambient four-point geometry.

The verifier checks:

```text
PGL(2,3) acts faithfully on the four points of PG(1,3)
```

and therefore

```text
PGL(2,3) ~= S4.
```

Inside this ambient `S4`:

```text
line codec -> preimage in GL(2,3) of an S3 point stabilizer
```

while

```text
tetrahedral codec -> A4 even/chiral subgroup.
```

So the correct relationship is:

```text
same ambient S4 geometry,
different native 12-substructures.
```

## Interpretation

This is a useful correction. The recurring 12 is real, but it appears in at least two forms:

```text
Borel/basis 12:
    signed basis choices on a projective line with first point fixed

Alternating/chiral 12:
    even tetrahedral flags / A4 rotations
```

They can be bijected as 12-element sets, but not canonically identified as groups without extra structure.

## Compressed theorem

```text
The line-pair 12-codec is the Borel point-stabilizer in GL(2,3), order 12, structure C2 x S3, projectivizing to an S3 point stabilizer in PGL(2,3)=S4. The tetrahedral chiral 12-codec is A4, the even subgroup of S4. Since the Borel codec has center of size 2 and elements of order 6, while A4 has trivial center and no elements of order 6, the two 12-codecs are not isomorphic as groups. They are count-equivalent and meet inside the same ambient four-point S4 geometry.
```

## Honest boundary

This proves they are not canonically the same group. The next hard step is to locate the correct bridge between them: likely a torsor-level transform inside `PGL(2,3)=S4`, or a polarity that sends point-stabilizer/Borel data to alternating/chiral data only after forgetting group multiplication.
