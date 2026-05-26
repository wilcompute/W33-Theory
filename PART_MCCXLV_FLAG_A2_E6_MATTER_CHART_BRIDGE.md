# Part MCCXLV: Flag A2/E6 Matter Chart Bridge

## Claim Boundary

MCCXLV is a finite spectral-combinatorial theorem. It refines the
`w33_e8_spectral_bridge.py` result

```text
240 = 6 + 72 + 81 + 81
```

from a count into an explicit packet decomposition. It does not claim the final
rank-8 E8 projection. In fact, it proves that the naive A2-triplet-sum quotient
does not produce that projection.

## Flag Anchor

Choose any W(3,3) point-line flag `(p0, L0)`. There are 160 such flags. For
each one, the 240 local corners split as:

```text
6 same-point A2-root corners
+ 24 adjacent-point triples
+ 27 positive matter triples
+ 27 negative matter triples.
```

Equivalently:

```text
240 = 6 + 24*3 + 27*3 + 27*3.
```

The six same-point corners are the A2 root packet at `p0`. The 72 adjacent
corners are the E6-root sector, grouped as two triples over each of the 12
points adjacent to `p0`. The 162 nonadjacent corners split into two 81-corner
matter sectors using the chosen line `L0`.

## The 81-Sector Is the Missing Coordinate Chart

For a nonadjacent point `q`, the common-bridge theorem gives a one-hot Gram
signature against the six A2-root corners at `p0`. The chosen line `L0` divides
the six A2 slots into two triples:

```text
base corner contains L0     -> plus matter sector,
base corner avoids L0       -> minus matter sector.
```

Thus each nonadjacent point contributes three corners to each matter sector.
Since the nonneighbors of `p0` form an affine 27-point cloud,

```text
81 = 27*3 = 3^3 * 3 = 3^4.
```

This is the exact ternary matter chart: an affine 3-space with one qutrit fiber.

## Exact Lambda=-2 Chart Certificate

Let `A3` be the k=3 adjacency matrix on the 240 local corners. The theorem uses
the rational eigenspace

```text
(A3 + 2I)x = 0.
```

Over `GF(7)`, the verifier computes:

```text
rank(A3 + 2I) = 159,
nullity        = 81.
```

Adding zero-coordinate constraints on either 81-sector gives full rank:

```text
rank([A3 + 2I ; plus-sector zero constraints])  = 240,
rank([A3 + 2I ; minus-sector zero constraints]) = 240.
```

So an exact `lambda=-2` eigenvector is determined by its coordinates on either
81-sector. This proves that each matter sector is a full coordinate chart for
the 81-dimensional `lambda=-2` component.

## Twisted Ternary Hypercube

Each 81-sector has the same vertex and edge budget as the ternary Hamming graph
`H(4,3)`:

```text
vertices = 81,
degree   = 8,
edges    = 324.
```

But it is not the ordinary Hamming network. The spectra differ from the exact
Hamming spectrum

```text
H(4,3): {-4:16, -1:32, 2:24, 5:8, 8:1}.
```

So the W33 matter sector is a twisted ternary hypercube: the count and local
budget match `3^4`, while the adjacency is curved by the W33 symplectic
connection.

## Boundary: The 8D Bridge Is Not the Naive Quotient

The natural next guess is to sum each A2 triple and hope the 24D golden tight
frame collapses to rank 8. The verifier checks this directly:

```text
rank(triplet sums in the 24D golden frame) = 24.
```

So the triplet-sum quotient preserves the 24D frame. The remaining target is
sharper: the E8 rank-8 projection must come from an additional triality
identification, not from simply adding the A2 fibers.

## Artifacts

- Analysis: `analysis/w33_flag_a2_e6_matter_chart_bridge.py`
- Tests: `tests/test_w33_flag_a2_e6_matter_chart_bridge.py`
- Result: `PART_MCCXLV_FLAG_A2_E6_MATTER_CHART_BRIDGE_results.json`
