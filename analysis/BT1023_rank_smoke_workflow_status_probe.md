# BT1023 — Rank smoke workflow status probe

BT1023 checks whether the K3 middle-rank smoke workflow surfaces through the
connector after the new workflow commit.

## Workflow

```text
.github/workflows/k3-middle-rank-smoke.yml
```

## Checked commit

```text
69e18e352e1204f448d777d34666471a40e60bd0
```

Connector result:

```text
combined statuses = 0
workflow runs = 0
```

## Reading

The workflow is committed, but the connector surfaced no run for the checked
commit. The two new shard scripts should be added to the workflow after a
checkout timing pass.

## Witnesses

```text
analysis/bt1023_rank_smoke_workflow_status_probe.py
data/bt1023_rank_smoke_workflow_status_probe.json
```
