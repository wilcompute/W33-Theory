# BT1018 — K3 level-2 degree-2 bounded row shard

BT1018 adds the first bounded row-shard module under the BT1015/BT1016 stream
contract.

## Map contract

```text
map          = degree_2
shape        = [45120, 152960]
global nnz   = 458880
target rank  = 42345
row weight   = 3
```

## Default shard

```text
start       = 0
count       = 256
row weights = [3, 3]
window rank = 256
```

## Reading

The shard verifies the block API that the full K3 level-2 iterator needs:
`start`, `count`, `cols`, and `row_weight`. It does not yet claim real incidence
rows for the full complex; the deterministic columns are a bounded API and
reducer test. The next layer is to replace the deterministic columns with real
face incidences in checkout or CI.

## Witnesses

```text
analysis/bt1018_k3_degree2_row_shard.py
data/bt1018_k3_degree2_row_shard.json
```
