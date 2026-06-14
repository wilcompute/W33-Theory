# BT1025 — K3 level-2 degree-2 full rank runner

BT1025 adds the manual full-rank execution path for the real K3 level-2 degree-2
middle map.

## Target

```text
map         = degree_2
shape       = [45120, 152960]
nnz         = 458880
target rank = 42345
```

## Runner

```text
analysis/bt1025_k3_degree2_full_rank_runner.py
```

Default mode writes a manifest. Full execution requires:

```text
python analysis/bt1025_k3_degree2_full_rank_runner.py --run-full --block-size 512
```

## Manual workflow

```text
.github/workflows/k3-degree2-full-rank.yml
```

## Boundary

The full rank job is not claimed here. It is wired as a manual workflow/check\-out
execution path because it is too long for cheap smoke CI.

## Witnesses

```text
data/bt1025_k3_degree2_full_rank_runner.json
```
