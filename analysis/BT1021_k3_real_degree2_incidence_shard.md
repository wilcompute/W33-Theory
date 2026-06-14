# BT1021 — Real K3 level-2 degree-2 incidence shard

BT1021 replaces the deterministic BT1018 shard with a bounded real-incidence
shard.

## Contract

```text
map         = degree_2
rows        = 45120
cols        = 152960
nnz         = 458880
target rank = 42345
```

## Implementation

The script reuses the accepted BT998 edgewise subdivision helpers, feeds them the
K3_16 facets, builds the actual level-2 K3 face sets, and emits bounded real
edge-triangle incidence rows.

## Boundary

The shard is real incidence, but bounded. It does not claim the full degree-2
rank. Full rank execution remains the checkout/CI layer.

## Witnesses

```text
analysis/bt1021_k3_real_degree2_incidence_shard.py
data/bt1021_k3_real_degree2_incidence_shard.json
```
