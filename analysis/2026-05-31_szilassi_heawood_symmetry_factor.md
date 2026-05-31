# Szilassi / Heawood Symmetry Factor

Date: 2026-05-31

This separates the two symmetry layers exposed by the concrete Szilassi dual construction:

```text
1. toroidal map symmetry
2. underlying Heawood skeleton symmetry
```

The goal is to locate the exact factor

```text
336 / 42 = 8.
```

## Dual Szilassi skeleton

Starting from the concrete Csaszar face list, the dual skeleton has:

```text
14 vertices
21 edges
```

The verifier checks:

```text
cubic degree distribution
bipartition sizes 7 and 7
girth 6
```

So the skeleton is the Heawood/Szilassi incidence graph.

## Toroidal map automorphisms

The toroidal map remembers the seven hexagonal faces coming from the Csaszar vertex-stars.

The verifier computes the map automorphism group and checks:

```text
|Aut(Szilassi toroidal map)| = 42.
```

It also checks map orientation behavior:

```text
orientation-preserving automorphisms: 42
orientation-reversing automorphisms: 0
```

So the dual Szilassi map has the same chiral map behavior as the Csaszar map.

## Heawood skeleton automorphisms

The verifier separately builds the canonical Heawood graph as the incidence graph of the Fano plane.

It constructs the automorphism group as:

```text
168 Fano collineations GL(3,2)
+
168 polarity/duality maps
=
336 automorphisms.
```

So:

```text
|Aut(Heawood skeleton)| = 336.
```

## Embedding the toroidal map group

The verifier finds an explicit graph isomorphism from the dual Szilassi skeleton to the canonical Heawood graph.

Then it transports the 42 toroidal map automorphisms into the 336-element Heawood automorphism group.

It checks:

```text
transported map automorphisms form a subgroup of Aut(Heawood)
```

and the number of left cosets is exactly:

```text
8.
```

Therefore:

```text
Aut(Heawood) / Aut(Szilassi map)
```

has index 8 at the level of finite sets/cosets.

## Meaning of the factor 8

The factor

```text
8 = 336 / 42
```

is the symmetry gain obtained by forgetting the toroidal face structure.

The toroidal map remembers:

```text
which seven 6-cycles are the Szilassi hexagonal faces
```

whereas the bare Heawood skeleton remembers only:

```text
Fano point-line incidence.
```

When that face-structure constraint is removed, eight times more symmetries appear.

## Relation to previous codecs

The earlier flag-codec bridge showed:

```text
Szilassi 84 = seven face axes * twelve local side flags.
```

This theorem shows that preserving those seven face axes as a toroidal map cuts the full Heawood symmetry down from 336 to 42.

So the hierarchy is:

```text
Heawood skeleton:
    336 automorphisms

Szilassi toroidal map:
    42 automorphisms

symmetry loss/gain:
    factor 8
```

## Compressed theorem

```text
The dual Szilassi skeleton constructed from the Csaszar rotation system is a 14-vertex cubic bipartite girth-6 Heawood graph. Its full graph automorphism group has order 336, built from 168 Fano collineations and 168 dualities. The toroidal Szilassi map automorphism group preserving the seven hexagonal faces has order 42 and is entirely orientation-preserving. Transporting this map group into the canonical Heawood automorphism group gives a subgroup of index 8. Thus the factor 8 is exactly the symmetry gained by forgetting the toroidal face/rotation structure and retaining only Fano incidence.
```

## Honest boundary

This proves the symmetry-factor decomposition. The next hard step is to interpret the eight cosets explicitly: likely as the eight choices of affine/Fano chart normalization, octonion sign/cube corners, or the eight complements associated with the Fano/Heawood incidence skeleton.
