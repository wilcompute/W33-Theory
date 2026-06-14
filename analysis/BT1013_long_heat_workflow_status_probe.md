# BT1013 — K3 long-heat workflow status probe

BT1013 checks the status surface for the long K3 heat workflow.

## Workflow

```text
.github/workflows/r3-k3-long-heat.yml
```

## Connector result

Checked commit:

```text
62d59c00459abcd916bf84a5ea4111046558f733
```

The connector surfaced:

```text
combined statuses: 0
workflow runs: 0
```

## Reading

The workflow is committed and separated from smoke tests, but no run/status is
surfaced by the connector for the checked commit. Triggering and final artifact
inspection require manual dispatch in the Actions UI or equivalent Actions access.

## Expected artifacts

```text
data/bt1010_k3_64probe_heat_driver.json
data/bt1007_k3_heat_16probe_checkpoint.json
```

## Witnesses

```text
analysis/bt1013_long_heat_workflow_status_probe.py
data/bt1013_long_heat_workflow_status_probe.json
```
