# BT1027 — K3 level-2 third boundary runner

BT1027 adds the manual execution path for the K3 level-2 third boundary map.

## Target

```text
map         = third_boundary
shape       = [152960, 184320]
nnz         = 737280
target rank = 110593
```

## Runner

```text
analysis/bt1027_k3_third_boundary_runner.py
```

Default mode writes a manifest. Full execution is reserved for checkout or CI:

```text
python analysis/bt1027_k3_third_boundary_runner.py --execute --block-size 512
```

## Manual workflow

```text
.github/workflows/k3-d3.yml
```

## Boundary

The full all-row result is not claimed here. The workflow records the manifest;
full execution still requires a checkout/CI run with sufficient wall-clock budget.

## Witnesses

```text
data/bt1027_k3_third_boundary_runner.json
```
