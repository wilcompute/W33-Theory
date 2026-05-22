# 2026-05-22 - Local Octahedron Faces Are Signed Xmin

## Long shot #2

What if the recent local pencil-octahedra do not merely explain the carrier counts, but directly realize the minimal logical `X` surface?

## Result

They do.

At every W33 point `p`, the four lines through `p` form a `K4` pencil and

```text
O_p = L(K4_pencil(p))
```

is a local octahedron.

Each local octahedron has eight faces. These eight faces split into four antipodal face-pairs.

The certificate verifies:

```text
40 * 8 = 320 = |X_min^{F3}|
40 * 4 = 160 = |X_min|
```

So:

```text
signed X_min vectors      = oriented local octahedron faces
projective X_min rays     = antipodal face-pairs of local octahedra
```

## Local codec matrix

For one octahedron, take its edge-face incidence matrix:

```text
12 edges x 8 faces
```

Properties:

```text
each edge touches 2 faces
each face touches 3 edges
rank = 7
nullity = 1
```

Across 40 local octahedra:

```text
480 x 320 local edge-face codec matrix
rank = 280
nullity = 40
```

The one-dimensional local nullity is the face-sum relation of each octahedron.

## Interpretation

This closes the `X_min` side through octahedral geometry:

| object | octahedral meaning |
|---|---|
| signed `X_min` vectors | local octahedron faces |
| projective `X_min` rays | antipodal face-pairs |
| directed carrier 480 | local octahedron edges |
| local gauge/codec slots | edge-face incidence of `O_p` |

This aligns with the SM codec commit where the eight octahedron faces are read as the eight sign-orientation states / gluon-like slots, and the three axes as the local triplet structure.

## Machine certificate

Added:

- `analysis/w33_octahedron_faces_are_signed_xmin.py`
- `data/w33_octahedron_faces_are_signed_xmin.json`
