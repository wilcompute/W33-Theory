# BT1022 — Real K3 level-2 degree-3 incidence shard

BT1022 adds the bounded real-incidence shard for the third boundary map.

## Contract

```text
map         = degree_3
rows        = 152960
cols        = 184320
nnz         = 737280
target rank = 110593
```

## Implementation

Rows are triangles, columns are tetrahedra, and each tetrahedron contributes to
its four triangle rows. The script reuses the accepted BT998 edgewise subdivision
helpers, feeds them the K3_16 facets, builds level-2 face sets, and emits bounded
real triangle-tetrahedron incidence rows.

## Boundary

The shard is real incidence, but bounded. It does not claim the full degree-3
rank. Full rank execution remains the checkout/CI layer.

## Witnesses

```text
analysis/bt1022_k3_real_degree3_incidence_shard.py
data/bt1022_k3_real_degree3_incidence_shard.json
```
