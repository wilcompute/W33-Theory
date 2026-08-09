# Part MCCXLVII: Toroidal Dual Symmetry Groups

## Claim Boundary

MCCXLVII is a symmetry stratification theorem for the Csaszar/Szilassi dual
toroidal pair. It separates three layers that should not be conflated:

```text
geometric realization symmetry,
abstract toroidal-map automorphism group,
bare graph automorphism group.
```

## Source Alignment

The repo-local realization file records seven coordinate models:

```text
5 Csaszar realizations,
2 Szilassi realizations,
all with Symmetry: 2-fold Cyclic (C2).
```

External references align with the same boundary:

- Csaszar: genus-one toroidal polyhedron with `V=7`, `E=21`, `F=14`, skeleton
  `K7`, and dual Szilassi.
- Szilassi: genus-one toroidal polyhedron with `V=14`, `E=21`, `F=7`, Heawood
  graph skeleton, and a 180-degree rotation axis.
- Regular map database: the dual Heawood map has `V/F/E=7/14/21`, Schläfli
  type `{3,6}`, skeleton `K7`, and full symmetry group `C7 semidirect C6` of
  order `42`.
- The bare Heawood graph has automorphism group `PGL_2(7)` of order `336`.

## Geometric Layer: C2

The verifier checks the coordinate involution in the repo face lists:

```text
Csaszar:  (0 1)(2 3)(4 5), fixing 6,
Szilassi: (0 1)(2 3)(4 5)(6 7)(8 9)(10 11)(12 13).
```

Both preserve their listed faces. Thus the concrete coordinate realizations
retain a `C2` Euclidean symmetry.

## Abstract Map Layer: 42

The Csaszar face set has:

```text
|Aut(map)| = 42.
```

The element-order profile is:

```text
1: 1,
2: 7,
3: 14,
6: 14,
7: 6.
```

This is the Frobenius group:

```text
C7 semidirect C6 = AGL(1,7).
```

The orientation profile is:

```text
orientation-preserving = 42,
orientation-reversing  = 0.
```

So the map is chiral: it has two flag orbits, since each map has

```text
flags = 4E = 84 = 2*42.
```

The Szilassi map is the dual map. Its listed seven hexagonal faces are
isomorphic to the dual of the Csaszar face structure, and therefore have the
same abstract map automorphism group of order `42`.

## Bare Graph Layer: 336

If the Szilassi hexagonal faces are forgotten, its skeleton is the Heawood
graph. The bare graph has:

```text
|Aut(Heawood graph)| = 336 = 8*42.
```

So the toroidal face embedding cuts the bare graph symmetry by a factor of
`8`. This is the key distinction: `336` belongs to the graph, while `42` belongs
to the toroidal map.

## W33 Bridge

The dual toroidal pair contributes:

```text
84 + 84 = 168 = 4*42 = |Aut(Fano)|.
```

The pointed split from the existing toroidal flag packet remains:

```text
84 = 72 + 12
```

for either the Csaszar vertex shell or the Szilassi face shell. Adding the
tetrahedral ground-state flag count gives:

```text
168 + 24 = 192,
```

which is exactly the tomotope flag carrier.

## Artifacts

- Analysis: `analysis/w33_toroidal_dual_symmetry_groups.py`
- Tests: `tests/test_w33_toroidal_dual_symmetry_groups.py`
- Result: `PART_MCCXLVII_TOROIDAL_DUAL_SYMMETRY_GROUPS_results.json`
