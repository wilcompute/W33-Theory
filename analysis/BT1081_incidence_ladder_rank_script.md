# BT1081 — Incidence ladder rank script

BT1081 builds the W33 boundary/spectral-projector harness and computes projected ranks for nearest-sector ladder blocks.

## Constructed complex

```text
points    = 40
edges     = 240
triangles = 160
```

The 1-Laplacian spectrum is recovered as

```text
0^81, 4^120, 10^24, 16^15.
```

## Operators tested

Four C1 operators are tested between nearest eigensectors `(0,4)`, `(4,10)`, `(10,16)`:

```text
line-edge adjacency
triangle-edge adjacency
d0 d0^T
d2 d2^T
```

## Projected ranks

| operator | 0->4 | 4->10 | 10->16 |
| --- | ---: | ---: | ---: |
| line-edge adjacency | 31 | 24 | 15 |
| triangle-edge adjacency | 38 | 22 | 15 |
| d0 d0^T | 0 | 0 | 0 |
| d2 d2^T | 0 | 0 | 0 |

## Reading

The Laplacian pieces `d0 d0^T` and `d2 d2^T` commute with `Delta_1`, so they give no off-sector ladder. The nonzero W33-native ladders come from edge-adjacency operators on C1.

The line-edge adjacency is the stronger candidate for the nearest-sector ladder because it achieves full target ranks on the last two steps:

```text
4->10  rank 24
10->16 rank 15
```

and a nonzero first step:

```text
0->4 rank 31.
```

## Witnesses

```text
analysis/bt1081_incidence_ladder_rank_script.py
data/bt1081_incidence_ladder_rank_script.json
```
