# C3 Fano Triangle Orientation

Date: 2026-05-30

This continues the C3 overlap theorem.

Previous theorem:

```text
C3 = A4 ∩ S3
```

inside

```text
S4 = PGL(2,3)
```

is the cyclic rotation of the three non-anchor points on `PG(1,3)`.

This theorem connects that local qutrit triangle to the Fano-line triple law.

## Important warning

This is not an identification of fields:

```text
F3 != F2.
```

The bridge is instead an identification of the same three-point oriented incidence object:

```text
three non-anchor points of PG(1,3)
```

with

```text
three nonzero vectors of F2^2.
```

## Fano line model

The three nonzero vectors of `F2^2` are:

```text
u = (1,0)
v = (0,1)
w = (1,1).
```

They satisfy the Fano-line triple law:

```text
u + v = w
v + w = u
w + u = v
```

and equivalently

```text
u + v + w = 0.
```

The full automorphism group of this three-point Fano line is

```text
GL(2,2) ~= S3.
```

The orientation-preserving subgroup is

```text
A3 = C3.
```

## Verified bridge

The verifier checks:

```text
C3 from A4∩S3 has order 3
its restricted action on the three non-anchor points is A3
GL(2,2) acts as S3 on the three nonzero F2^2 vectors
A3 inside GL(2,2) equals the C3 overlap after labeling
all GL(2,2) permutations preserve the Fano sum law
C3 preserves both the Fano sum law and cyclic orientation
```

Therefore the C3 overlap is exactly the orientation-preserving automorphism group of a Fano-line triple.

## Orientation interpretation

Choosing one of the two nontrivial C3 cycles gives an oriented triple:

```text
u -> v -> w -> u.
```

This cyclic order is the wedge orientation.

Odd permutations in `S3` reverse orientation and correspond to the dot/dual flip.

So the local dictionary is:

```text
C3:
    wedge/cyclic orientation of the Fano-line triple

S3:
    full line symmetry, including orientation-reversing dot/dual flips
```

## Connection back to the qutrit triangle

The three non-anchor points on `PG(1,3)` form a qutrit triangle.

The overlap

```text
A4 ∩ S3 = C3
```

rotates them cyclically.

After choosing a labeling by the nonzero vectors of `F2^2`, that same C3 is the cyclic orientation of the Fano-line law

```text
{u,v} -> u+v.
```

Thus the qutrit triangle and Fano line share the same oriented three-point codec, even though their fields differ.

## Compressed theorem

```text
The C3 overlap between tetrahedral chirality A4 and anchored line stabilizer S3 is the cyclic orientation of the three non-anchor points of PG(1,3). After labeling those three points as the nonzero vectors u,v,w of F2^2, the same C3 is the orientation-preserving automorphism group of the Fano-line law u+v=w, v+w=u, w+u=v. Hence the local qutrit triangle and Fano wedge/dot triple share the same oriented three-point incidence codec, while S3 supplies the orientation-reversing dual flips.
```

## Honest boundary

This proves the oriented three-point bridge. The next hard step is to lift this from a single Fano line to the full seven-point Fano plane and see how the four-point `PG(1,3)`/tetrahedral geometry selects one local line inside the global Fano wedge-dot codec.
