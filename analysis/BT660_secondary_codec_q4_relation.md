# BT660 — Secondary Codec Q4 Relation Theorem

BT657 proved the raw Levi-flag complement is not Q4.  It is

```text
4K4 = K4 + K4 + K4 + K4.
```

So the Q4/K4,4 layer must be rebuilt as a **secondary codec relation**, not as Levi flag adjacency.

## Product labeling

The 16 complement flags split as four complete W33 line-fiber cells, each with four local flags.  Label this set abstractly as

```text
C16 = A x B,
|A|=4,
|B|=4,
A ~= F2^2,
B ~= F2^2.
```

Here:

- `A` labels the four K4 line-fiber cells;
- `B` labels the four flags inside each K4 cell.

The raw Levi adjacency is

```text
(a,b) ~raw (a,b') for b != b'.
```

Thus raw adjacency is exactly four K4 components.

## Secondary codec relation

Choose a two-generator square basis in `A` and a two-generator square basis in `B`:

```text
SA = {alpha1, alpha2},
SB = {beta1, beta2},
```

where each pair spans F2^2.  Define the secondary codec adjacency by

```text
(a,b) ~codec (a+alpha,b) for alpha in SA,
(a,b) ~codec (a,b+beta) for beta in SB.
```

This graph is the Cartesian product

```text
C4 square on A  □  C4 square on B,
```

hence

```text
C16_codec ~= Q4.
```

It has

```text
16 vertices,
32 edges,
regular degree 4,
connected = true.
```

## Antipodal quotient

With the usual antipodal map

```text
(a,b) -> (a+alpha1+alpha2, b+beta1+beta2),
```

the quotient has eight axes.  Since Q4 is bipartite and the antipodal map preserves parity in dimension four, the quotient graph is

```text
Q4/{pm} ~= K4,4.
```

This recovers the tomotope/Fano codec chain safely:

```text
raw Levi complement: 4K4
secondary codec lift: Q4
antipodal codec quotient: K4,4.
```

## Non-uniqueness / gauge count

A K4 cell has three possible omitted perfect matchings, equivalently three square structures on four points.  Therefore the product codec has

```text
3 x 3 = 9
```

basis-gauge choices before additional Fano/tomotope labels are imposed.

So the codec relation is not canonical from Levi adjacency alone.  It becomes canonical only after choosing a Fano/tomotope boundary chart.

## Boundary

The theorem does **not** say the 16 complement flags induce Q4 in the Levi flag graph.  It says Q4 is the minimal secondary product-codec relation compatible with the verified 4K4 complement decomposition.
