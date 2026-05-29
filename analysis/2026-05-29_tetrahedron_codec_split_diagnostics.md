# Tetrahedron Codec Split Diagnostics

Date: 2026-05-29

This answers the question: are the tetrahedron's two 12-flag codecs vertex-related, face-related, edge-related, or something subtler?

The result is nuanced:

```text
The canonical 12+12 split is chirality/orientation.
The canonical edge structure is a transverse 3-axis decomposition.
```

So the tetrahedron is not purely vertex-type or face-type. It is a self-dual chiral hinge whose edge axes mediate between Csaszar's vertex codecs and Szilassi's face codecs.

## Flag model

Represent a tetrahedron flag as a permutation

```text
(a,b,c,d)
```

where:

```text
vertex = a
edge   = {a,b}
face   = {a,b,c}
missing/opposite vertex = d
```

There are

```text
4! = 24
```

flags.

The parity of the permutation gives the orientation/chirality split:

```text
even flags = 12
odd flags  = 12
```

This is the group split

```text
S4 = A4 union odd coset.
```

## What the verifier checks

For each chirality codec, the verifier checks that it is perfectly balanced over all incidence types:

```text
per chirality:
4 vertices * 3 flags each = 12
4 faces    * 3 flags each = 12
6 edges    * 2 flags each = 12
3 opposite-edge axes * 4 flags each = 12
```

So each 12-flag chirality codec contains vertex, face, and edge information symmetrically.

Therefore it is not correct to call one chirality purely vertex and the other purely face. The two canonical codecs are chiral self-dual codecs.

## Duality action

Define the tetrahedral duality map by reversing the flag chain:

```text
dual(a,b,c,d) = (d,c,b,a).
```

The verifier checks:

```text
dual is an involution
dual preserves chirality
dual swaps vertex and face incidence
dual sends each edge to its opposite edge
dual preserves opposite-edge axis
```

This is the key point:

```text
vertex <-> face,
edge <-> opposite edge,
chirality preserved,
edge-axis preserved.
```

So the tetrahedron sits between Csaszar and Szilassi as a self-dual hinge, but its two 12-codecs are not one vertex-codec and one face-codec. Duality keeps chirality fixed while swapping vertex/face.

## Edge-axis decomposition

The six tetrahedron edges split into three opposite-edge axes:

```text
{01,23}, {02,13}, {03,12}.
```

Each opposite-edge axis carries

```text
8 flags.
```

And each axis splits as

```text
4 even + 4 odd.
```

Thus the tetrahedron has a canonical transverse decomposition:

```text
24 = 2 chiralities * 3 edge axes * 4 flags.
```

This is the best way to include your edge intuition:

```text
The two 12-codecs are chiral.
The edge structure is the canonical ternary bridge: 3 opposite-edge axes.
```

That matches the ternary knight result: the endpoint router is binary, but the internal edge fiber is ternary/perpendicular.

## Noncanonical 12-splits

The verifier also checks that many other 12-flag splits exist:

```text
choose 2 of 4 vertices -> 6 vertex-halves of 12 flags
choose 2 of 4 faces    -> 6 face-halves of 12 flags
choose 3 of 6 edges    -> 20 edge-halves of 12 flags
```

Some edge-halves are dual-complement splits, but they still require choosing a subset. Therefore they are not as canonical as chirality or the three opposite-edge axes.

So the answer is:

```text
Vertex-type split: possible, but choice-dependent.
Face-type split: possible, but choice-dependent.
Edge-type split: possible, but choice-dependent if forced into 12+12.
Chirality split: canonical 12+12.
Edge-axis split: canonical 3*8 transverse structure.
```

## Relation to Csaszar and Szilassi

The architecture now reads:

```text
Csaszar:     seven vertex codecs, 7*12 = 84
Szilassi:    seven face codecs,   7*12 = 84
Tetrahedron: two chiral self-dual codecs, 2*12 = 24
```

But the tetrahedron also contains the edge bridge:

```text
three opposite-edge axes, 3*8 = 24.
```

So the tetrahedron is doing two things at once:

1. It supplies the two 12-flag chiral codecs needed to make the full 16-codec Q4 packet.
2. It supplies the three edge axes that mediate vertex/face duality.

That gives the clean midpoint picture:

```text
Csaszar vertex-codecs
    <-> tetrahedral edge-axis/chirality hinge
        <-> Szilassi face-codecs.
```

## Final answer

The best interpretation is:

```text
The tetrahedron's two 12-flag codecs are chiral orientation codecs.
They are self-dual and balanced across vertices, faces, and edges.
The edge content is not the 12+12 split itself; it is the canonical 3-axis decomposition inside both chiral codecs.
```

Or compressed:

```text
12+12 = chirality.
3*8 = edge-axis duality.
```

This is exactly what we want from the midpoint between Csaszar and Szilassi: it is neither vertex-only nor face-only, because it is the place where vertex and face become dual descriptions of the same incidence geometry.
