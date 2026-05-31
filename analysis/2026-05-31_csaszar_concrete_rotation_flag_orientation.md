# Concrete Csaszar Rotation Flag Orientation

Date: 2026-05-31

This moves beyond the abstract Fano incidence labeling and tests a concrete Csaszar map orientation.

The repo already contains McCooey Csaszar-1 coordinates and the 14 triangular faces in the toroidal deep-dive file.  The face list is enough to derive the combinatorial rotation system of the orientable map.

## Input

The verifier uses the 14 triangular faces:

```text
(0,1,2), (0,2,5), (0,5,4), (0,4,6), (0,6,3), (0,3,1),
(1,3,4), (1,4,5), (1,5,6), (1,6,2),
(2,6,4), (2,4,3), (2,3,5), (5,3,6)
```

These are the Csaszar faces from the concrete realization data already in the repo.

## Map counts

The verifier checks:

```text
V = 7
E = 21
F = 14
Euler characteristic = 0
genus = 1
```

Each edge is incident to exactly two faces.

So this is the expected toroidal triangular map of `K7`.

## Coherent face orientation

The verifier orients the faces so that every shared edge is traversed in opposite directions by its two incident faces.

This gives an orientable rotation system.

At each vertex, the induced local neighbor rotation is a 6-cycle.

So every vertex sees all six other vertices in a cyclic order.

## Concrete 84 flags

A concrete local flag is represented as:

```text
(vertex axis v, adjacent neighbor w, side in {next, prev}, other neighbor completing the face on that side)
```

For each vertex:

```text
6 adjacent neighbors * 2 sides = 12 flags.
```

Globally:

```text
7 vertices * 12 flags = 84.
```

The verifier checks:

```text
84 concrete flags
12 flags at every vertex
6 adjacent neighbors at every vertex
2 sides/orientations for every ordered vertex-neighbor pair
```

This gives the concrete Csaszar realization of the same local two-state side/orientation codec used in the Fano-polarity model.

## Automorphism / chirality test

The verifier computes the vertex-permutation automorphism group preserving the triangular face set.

It checks:

```text
|Aut(Csaszar map)| = 42.
```

Then it tests whether those automorphisms preserve or reverse the chosen orientable face system.

Result:

```text
orientation-preserving automorphisms: 42
orientation-reversing automorphisms: 0
```

So the concrete Csaszar map is chiral at the combinatorial map level.

## Relation to the Fano orientation label

Earlier, the abstract Fano-polarity model had a local orientation label

```text
p -> q
```

on the two affine points of `M\L`.

In the concrete Csaszar rotation system, that finite two-state orientation corresponds to choosing one of the two sides of an incident edge around a vertex:

```text
next side
prev side
```

So the bridge is:

```text
Fano p->q local orientation
    ~=
Csaszar side-of-edge choice in the vertex rotation system.
```

## Correct chirality statement

The abstract Fano model alone only gives a two-state side/orientation codec.

The concrete Csaszar map adds an orientable embedding structure, and with that extra structure the automorphism result is:

```text
Csaszar is chiral: all 42 map automorphisms preserve orientation; none reverse it.
```

## Compressed theorem

```text
Using the concrete Csaszar face list, one can orient the 14 triangular faces coherently on the torus. The induced rotation at each of the 7 vertices is a 6-cycle, yielding 7*6*2=84 concrete side flags. The vertex-permutation automorphism group preserving the face set has order 42 and is entirely orientation-preserving, with zero orientation-reversing automorphisms. Thus the Fano two-state orientation label realizes concretely as the two local sides of an incident edge in the chiral Csaszar rotation system.
```

## Honest boundary

This proves the concrete Csaszar side/orientation model. The next hard step is to perform the dual construction for Szilassi: derive its seven hexagonal face cycles, build the dual rotation/face-side flags, and verify that Fano polarity maps the Csaszar concrete orientation data to the Szilassi face-codec data.
