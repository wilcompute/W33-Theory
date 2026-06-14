# BT1010 — K3_16 64-probe heat workflow

BT1010 separates the long K3_16 all-degree heat run from the cheap R3 smoke
workflow.

## Workflow

```text
.github/workflows/r3-k3-long-heat.yml
```

The workflow is manual-dispatch only and runs:

```text
python analysis/bt1010_k3_64probe_heat_driver.py --probes 64 --seed 1010
python analysis/bt1007_k3_heat_16probe_checkpoint.py
```

## Boundary

A flexible-input workflow version was blocked by the connector. The committed
workflow is therefore fixed to 64 probes and seed 1010. It records the long-run
manifest and uploads the current heat checkpoint artifacts.

## Witnesses

```text
analysis/bt1010_k3_64probe_heat_driver.py
.github/workflows/r3-k3-long-heat.yml
data/bt1010_k3_64probe_heat_driver.json
```
