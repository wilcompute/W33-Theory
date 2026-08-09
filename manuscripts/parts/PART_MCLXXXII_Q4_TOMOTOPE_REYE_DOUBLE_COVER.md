# Part MCLXXXII: Q4 Antipodal Tomotope-Reye Double Cover

## Claim Boundary

MCLXXXII is a finite incidence-cover theorem. It proves that the Q4
plaquette-router incidence from MCLXXXI descends under the antipodal Q4
translation to the Reye configuration that the tomotope paper identifies as the
tomotope edge-triangle medial layer.

It is not a continuum field equation and does not claim that Q4 replaces the
tomotope. The result is a precise two-sheet combinatorial bridge.

## Statement

MCLXXXI gave the Q4 face-edge incidence packet:

```text
24 square faces,
32 edges,
24 faces * 4 edges = 32 edges * 3 faces = 96 incidences.
```

Act on Q4 by bitwise complement:

```text
(b0,b1,b2,b3) -> (1-b0,1-b1,1-b2,1-b3).
```

This antipodal translation has no fixed square face and no fixed edge. Therefore
the quotient has

```text
24 / 2 = 12 face-orbits,
32 / 2 = 16 edge-orbits,
96 / 2 = 48 incidences.
```

The quotient incidence graph is isomorphic to Reye's configuration:

```text
12_4, 16_3.
```

## Reye Model

The verifier uses the classical cube model:

```text
12 points = 8 cube vertices + cube center + 3 infinity points,
16 lines = 12 cube edges + 4 body diagonals.
```

Every point lies on four lines and every line lies on three points:

```text
12 * 4 = 16 * 3 = 48.
```

The antipodal Q4 quotient has exactly the same bipartite incidence graph.

## Tomotope Lock

The tomotope edge-triangle medial layer has the same Reye parameters:

```text
tomotope edges      = 12,
tomotope triangles  = 16,
edge-triangle incidences = 12 * 4 = 16 * 3 = 48.
```

Thus the MCLXXXI Q4 packet is a two-sheet lift of the tomotope/Reye medial
layer:

```text
Q4 face-edge incidences = 2 * tomotope medial incidences = 2 * 48 = 96.
```

The same 96 is the tomotope automorphism order, and the full tomotope flag
count is the remaining rank-0 vertex choice:

```text
|Aut(T)| = 96,
Flags(T) = 192 = 2 * 96.
```

## Reading

The previous Q4 result did not merely share the number `24` with the tomotope
family. Its incidence graph is a connected antipodal double cover of the
tomotope/Reye medial layer. In the self-entangled qutrit reading:

```text
Q4 plaquette lift      = two-sheet router cover,
tomotope/Reye medial   = quotient incidence skeleton,
96 lifted incidences   = tomotope automorphism order,
192 flags              = lifted incidence packet with vertex-side choice.
```

This explains why the Q4 plaquette result points directly at the tomotope.

## Source Alignment

- NetworkX hypercube graph documentation: Qn nodes are bit tuples and edges
  differ in exactly one bit.
  https://networkx.org/documentation/stable/reference/generated/networkx.generators.lattice.hypercube_graph.html
- MathWorld Hypercube: the tesseract has 16 vertices, 32 edges, 24 square
  faces, and 8 cubic cells.
  https://mathworld.wolfram.com/Hypercube.html
- Monson et al., *The Tomotope*: the tomotope is an abstract uniform 4-polytope;
  its medial layer `I1,2` has Reye parameters `(12_4, 16_3)`.
  https://bmonson.ext.unb.ca/fields/tom.pdf

## Artifacts

- Analysis: `analysis/w33_q4_tomotope_reye_double_cover.py`
- Tests: `tests/test_w33_q4_tomotope_reye_double_cover.py`
- Result: `PART_MCLXXXII_Q4_TOMOTOPE_REYE_DOUBLE_COVER_results.json`
