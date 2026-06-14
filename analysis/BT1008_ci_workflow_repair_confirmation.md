# BT1008 — CI workflow repair and confirmation

BT1008 updates the R3 edgewise/fat-tower workflow to track the latest artifacts.

## Workflow

```text
.github/workflows/r3-edgewise-fat-tower.yml
```

## Repair applied

The workflow now runs these additional smoke scripts:

```text
analysis/bt1003_ci_status_probe.py
analysis/bt1006_k3_level2_endpoint_ranks.py
analysis/bt1007_k3_heat_16probe_checkpoint.py
```

and uploads these additional artifacts:

```text
data/bt1003_ci_status_probe.json
data/bt1006_k3_level2_endpoint_ranks.json
data/bt1007_k3_heat_16probe_checkpoint.json
```

## Boundary

The GitHub connector still did not surface a workflow run/status. A TeX
package-install step was not patched through the connector; the workflow retains
BT999 behavior and builds PDFs only when `latexmk` is available.

## Witnesses

```text
.github/workflows/r3-edgewise-fat-tower.yml
data/bt1008_ci_workflow_repair_confirmation.json
```
