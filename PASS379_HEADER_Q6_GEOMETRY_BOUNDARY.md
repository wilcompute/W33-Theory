# Pass 379 — the header clock is not a Q6 geometry operation

Pass 377 built an exact binary-control object: the BT828 one-axis toggle
events reach a 48-flag header plane, and incrementing its depth acts by
`f ↦ f + 64 (mod 192)`. Pass 378 then ruled out a factorization through the
live LOAD/FLIP/LATCH scheduler flag.

Pass 379 asks the next precise computing question: after applying BT1371's
pinned 192-row flag-to-Q6-edge table, does this header permutation preserve
Q6 edge geometry? It does not.

## Exact object tested

BT1371 assigns every tomotope flag a distinct edge of the six-cube Q6. The GAP
witness reads that live table directly, checks all 192 rows are distinct
single-bit Q6 edges, and transports the arithmetic header permutation through
it. Two Q6 edges are adjacent exactly when they share an endpoint. Since every
cube automorphism preserves this line-graph adjacency, a failure rules out a
cube-edge geometric interpretation of this particular header permutation
through this particular address table.

The full 192-flag bus still has the free arithmetic C3 action
`f ↦ f + 64 (mod 192)`, with `192 = 64 × 3`; the Pass-377 image is its
invariant 48-flag subclock, `48 = 16 × 3`.

## GAP result

The Q6 line graph has exactly `64 × binomial(6,2) = 960` adjacent unordered
edge pairs. Under the transported header shift, only 146 remain adjacent; 814
adjacent pairs are lost, balanced by 814 nonadjacent pairs that become
adjacent. The first deterministic witness is:

`{0, 8} ↦ {64, 72}`.

Flags 0 and 8 label `000000–000001` and `000001–001001`, which share the
vertex `000001`. Shifted flags 64 and 72 label `011111–111111` and
`010101–010111`, which share no endpoint.

The computed Q6-direction transition matrix is:

~~~
5  4  4  5   6   8
4  5  5  4   8   6
3  2  6  3   8  10
2  3  3  6  10   8
5 13  7  7   0   0
13 5  7  7   0   0
~~~

It is not a direction permutation: the header depth step mixes the pinned
table's Q6 direction classes.

## Correct computational reading

The header C3 remains a valid finite control-address clock. It can select,
advance, and verify header state. It is not, through the present BT1371 address
table, a Q6 geometric transition, a Q6 state traversal, or a physical
oscillation. This is a stronger typed-ABI boundary, not a failure of the
header control layer.

The theorem does not rule out an explicitly constructed different
flag-to-edge intertwiner. It says that no such intertwiner is supplied by the
current pinned table, and that the arithmetic clock alone must not be
presented as one.

## Reproduction

~~~
gap -q analysis/w33_pass379_header_q6_geometry_boundary.g
python3 -m pytest tests/test_pass379_gap_header_q6_geometry_boundary.py -q
~~~

The certificate is GAP-owned:

- witness: `analysis/w33_pass379_header_q6_geometry_boundary.g`
- output: `data/w33_pass379_header_q6_geometry_boundary.json`
- focused regression: `tests/test_pass379_gap_header_q6_geometry_boundary.py`

Search signature: `192/64x3/960/geometry-boundary`.
