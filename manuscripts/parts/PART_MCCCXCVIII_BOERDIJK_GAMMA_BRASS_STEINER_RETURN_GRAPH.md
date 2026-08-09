# Part MCCCXCVIII: Boerdijk/Gamma-Brass Steiner Return Graph

## Claim Boundary

MCCCXCVIII is a finite incidence theorem on the W33-derived `E6` Steiner shell,
plus a static source-count dictionary from the 2004 gamma-brass/Boerdijk-Coxeter
paper and the regular `600`-cell.

It proves a new internal return graph:

```text
240 Steiner trihedra -> 40 components x 6 trihedra
component adjacency by 9 shared tritangents -> srg(40,12,2,4)
```

It does not assert that the component graph has been canonically identified
with the original W33 point graph.

## External Source Counts

The online paper trail identifies the user hint as gamma-brass, not `Y`-brass:

- E. A. Lord and S. Ranganathan, "The gamma-brass structure and the
  Boerdijk-Coxeter helix", Journal of Non-Crystalline Solids 334-335 (2004),
  121-125, doi `10.1016/j.jnoncrysol.2003.11.069`.

The static counts used here are:

```text
gamma-brass cluster atoms = 26
3x3x3 bcc-derived sites = 52 = 2 x 26
augmented cluster atoms = 38
augmented tetrahedral packing = 81 tetrahedra
local helix coordination = 12
initial tetrahedron shared by = 4 icosahedra
```

The regular `600`-cell source-count layer is:

```text
vertices = 120
edges = 720
triangular faces = 1200
tetrahedral cells = 600
Boerdijk-Coxeter rings = 20
tetrahedra per ring = 30
```

## W33 Dictionary

The gamma-brass counts land directly on the W33 substrate:

```text
26 = 3^3 - 1
52 = 2(3^3 - 1)
38 = 40 - 2
81 = 3^4
12 = k
4 = mu
```

The `600`-cell counts land on the new Steiner shell:

```text
120 = Steiner trihedral pairs
720 = 240 trihedra x 3 tritangents
720 = 45 tritangents x 16 trihedra
720 = 120 trihedral pairs x 6 contained tritangents
600 = 20 Boerdijk-Coxeter rings x 30 tetrahedra
30 = 5 x 3!
40 = 2 chiralities x 20 Boerdijk-Coxeter rings
```

## Internal Construction

Start with the `240` individual Steiner trihedra from MCCCXCVII.  Each trihedron
has a `9`-weight cover.

Build the disjoint-cover graph:

```text
vertices = 240 trihedra
edge = two trihedra have disjoint 9-weight covers
```

The graph has:

```text
degree = 4
edges = 480
connected components = 40
component size = 6
```

Inside each component:

```text
3 disjoint 9-weight covers partition all 27 E6 weights;
each cover carries its 2 partner trihedra;
the 6 trihedra use 18 distinct tritangents;
each of the 27 weights appears exactly twice.
```

## Return Graph

For each six-trihedron component, collect its `18` tritangents.  On the `40`
components, define:

```text
C_i adjacent C_j  <=>  |T_i cap T_j| = 9
```

The verifier obtains:

```text
vertices = 40
degree = 12
edges = 240
adjacent common-neighbor count = 2
nonadjacent common-neighbor count = 4
```

So the return graph has exactly:

```text
srg(40,12,2,4)
```

The complementary relation is:

```text
|T_i cap T_j| = 6 -> srg(40,27,18,18)
```

## Reading

The `240` Steiner trihedra do not remain only an `E8`-count shell.  They fold
back to a `40`-component quotient, with `6 = 3!` trihedra per component.  That
quotient carries the W33 strongly regular parameter set.

This is the cleanest bridge found from the Boerdijk-Coxeter hint:

```text
gamma-brass 81 tetrahedra -> W33 q^4
600-cell 120 vertices -> 120 Steiner pairs
600-cell 720 edges -> trihedron-tritangent incidence
20 Boerdijk-Coxeter rings with two chiralities -> 40 return components
40 return components with degree 12 -> srg(40,12,2,4)
```

So the Steiner shell now has an internal return map back to W33-scale
incidence, while preserving the boundary that no canonical graph isomorphism is
being claimed.

## Artifacts

- Analysis: `analysis/w33_boerdijk_gamma_brass_steiner_return_graph.py`
- Tests: `tests/test_w33_boerdijk_gamma_brass_steiner_return_graph.py`
- Result: `PART_MCCCXCVIII_BOERDIJK_GAMMA_BRASS_STEINER_RETURN_GRAPH_results.json`
