# 2026-05-22 - Root-Line Orthogonality Decomposition

## Breakthrough

The full 120-root-line orthogonality graph decomposes into two geometrically meaningful pieces:

```text
root-line orthogonality = collinear block graph + noncollinear transport graph
```

## Collinear block graph

If two W33 points are collinear, their two point-triads have all 9 cross-pairs orthogonal.

Across all 240 collinear point-pairs this contributes

```text
240 * 9 = 2160
```

root-line orthogonality edges.

This is the graph made from K3,3 blocks between collinear point-triads.

It is 36-regular on 120 vertices.

## Noncollinear transport graph

If two W33 points are noncollinear, their two point-triads have exactly 3 orthogonal cross-pairs, a perfect matching.

Across all 540 noncollinear point-pairs this contributes

```text
540 * 3 = 1620
```

root-line orthogonality edges.

This graph is 27-regular on 120 vertices and connected.

Its spectrum is

```text
27^1 + 3^75 + (-3)^24 + (-9)^20
```

This is the 3-cover transport graph carrying the Z3 holonomy from the previous pass.

## Total root-line graph

The root-line orthogonality graph has

```text
3780 edges
```

and the decomposition checks exactly:

```text
3780 = 2160 + 1620
```

or

```text
E_rootline = C_collinear + T_noncollinear.
```

## Meaning

The root-line graph separates into:

| layer | W33 relation | local form | edge count |
|---|---|---:|---:|
| collinear block | adjacent points | K3,3 between triads | 2160 |
| noncollinear transport | nonadjacent points | perfect matching between triads | 1620 |

The noncollinear transport graph is the layer where cyclic phase holonomy lives.

## New code

- `analysis/w33_rootline_orthogonality_decomposition.py`

When run, it writes:

- `data/w33_rootline_orthogonality_decomposition.json`
