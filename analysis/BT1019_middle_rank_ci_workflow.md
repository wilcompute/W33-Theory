# BT1019 — K3 middle rank CI smoke workflow

BT1019 adds a cheap CI smoke workflow before any full K3 level-2 middle rank job
is attempted.

## Workflow

```text
.github/workflows/k3-middle-rank-smoke.yml
```

## Scripts

```text
analysis/bt1015_f2_bitset_rank_core.py
analysis/bt1015_k3_middle_stream_contracts.py
analysis/bt1016_k3_middle_rank_smoke_test.py
analysis/bt1018_k3_degree2_row_shard.py --start 0 --count 256
```

## Artifacts

```text
data/bt1015_k3_middle_stream_contracts.json
data/bt1016_k3_middle_rank_smoke_test.json
data/bt1018_k3_degree2_row_shard.json
```

## Reading

The middle rank stack now has a CI smoke layer that verifies the reducer,
contracts, deterministic row-window test, and bounded degree-2 shard before the
full execution is attempted.
