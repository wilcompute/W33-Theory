# BT1017 — Workflow execution probe

BT1017 probes the workflow execution surface available through the connector.

## Checked commit

```text
aba0f8c8cca57632ca6a106c72e20aea2e4b3dbc
```

Connector result:

```text
combined statuses: 0
workflow runs: 0
```

## Workflows checked

```text
.github/workflows/r3-k3-long-heat.yml
.github/workflows/paper-build.yml
```

## Expected outputs after external dispatch

```text
data/bt1010_k3_64probe_heat_driver.json
data/bt1007_k3_heat_16probe_checkpoint.json
w33_paper.pdf
photonic_holonet.pdf
```

## Boundary

The connector exposes status reads but not workflow dispatch here, and no
workflow runs were surfaced for the checked commit. Actual triggering requires
Actions UI or equivalent CLI/token access.

## Witnesses

```text
analysis/bt1017_workflow_execution_probe.py
data/bt1017_workflow_execution_probe.json
```
