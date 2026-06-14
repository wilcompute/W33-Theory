# BT1024 — Real shards in K3 middle-rank smoke workflow

BT1024 updates the K3 middle-rank smoke workflow to include bounded real-incidence
shards.

## Workflow

```text
.github/workflows/k3-middle-rank-smoke.yml
```

## New real-incidence smoke commands

```text
python analysis/bt1021_k3_real_degree2_incidence_shard.py --start 0 --count 8
python analysis/bt1022_k3_real_degree3_incidence_shard.py --start 0 --count 8
```

The windows are intentionally tiny until checkout/Actions timing is known.

## New artifacts

```text
data/bt1021_k3_real_degree2_incidence_shard.json
data/bt1022_k3_real_degree3_incidence_shard.json
```

## Boundary

The workflow was updated. Runtime success is not claimed until an Actions run is
surfaced and inspected.

## Witnesses

```text
data/bt1024_real_shards_smoke_workflow.json
```
