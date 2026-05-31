# Szilassi Dual from Csaszar Rotation

Date: 2026-05-31

This performs the concrete dual construction promised after the Csaszar rotation verifier.

The previous verifier derived the orientable rotation system of the concrete Csaszar map from its 14 triangular faces and showed:

```text
7 vertices * 6 neighbors * 2 local sides = 84 concrete Csaszar flags.
```

This theorem constructs the dual map directly.

## Dual construction

The duality rule is:

```text
Csaszar vertices         -> Szilassi hexagonal faces
Csaszar triangular faces -> Szilassi vertices
Csaszar edges            -> Szilassi edges
```

Since Csaszar has

```text
V=7, E=21, F=14,
```

the dual has

```text
V_dual=14, E_dual=21, F_dual=7.
```

The verifier checks this exactly, with genus 1.

## Seven dual hexagons

At each Csaszar vertex, the oriented rotation system gives a 6-cycle of incident triangular faces.

Those six primal faces become the six dual vertices around one Szilassi face.

So each Csaszar vertex-star becomes one Szilassi hexagon.

The verifier checks:

```text
7 dual faces
all 7 are hexagons
```

## Szilassi / Heawood skeleton

The dual skeleton has:

```text
14 vertices
21 edges
```

The verifier checks:

```text
cubic degree distribution
bipartite
shortest cycle length/girth = 6
```

So the dual skeleton has the expected Heawood/Szilassi incidence pattern.

## Dual 84 flags

A Szilassi face-side flag is represented by:

```text
(face axis, boundary dual vertex, side in {next,prev}, adjacent boundary dual vertex)
```

Each hexagonal face has:

```text
6 boundary edges * 2 sides = 12 flags.
```

Globally:

```text
7 faces * 12 flags = 84.
```

The verifier checks:

```text
84 Szilassi face flags
12 flags at every face axis
6 boundary positions per face
```

## Concrete duality with Csaszar flags

The verifier also constructs a concrete incidence-level map from Csaszar vertex-side flags to Szilassi face-side flags.

The local two-state side/orientation codec survives the duality:

```text
Csaszar side around a vertex
    ->
Szilassi next/prev side around the dual hexagonal face.
```

So the concrete toroidal duality matches the earlier abstract Fano polarity picture:

```text
Csaszar vertex axes <-> Szilassi face axes.
```

## Relation to Fano polarity

Earlier, the abstract Fano-polarity labeling said:

```text
Csaszar:
    polar Fano points as vertex axes

Szilassi:
    Fano lines as face axes
```

This concrete dual construction shows the same vertex-face swap at the toroidal map level.

## Compressed theorem

```text
Dualizing the oriented Csaszar triangular map gives a Szilassi-type map with 14 vertices, 21 edges, and 7 hexagonal faces. The seven hexagons are the vertex-stars of the Csaszar rotation system. Its skeleton is cubic, bipartite, and girth 6, matching the Heawood/Szilassi incidence pattern. Its flags decompose as 7 hexagonal face axes times 12 local side flags, and the Csaszar vertex-side flags map concretely to Szilassi face-side flags under duality.
```

## Honest boundary

This proves the concrete dual flag-codec construction. The next hard step is to compare the automorphism/chirality behavior of the dual Szilassi map with the Csaszar map: does the dual also have only orientation-preserving map automorphisms, and how does this sit inside the larger Heawood graph automorphism group of order 336?
