# BT1003 — CI status probe

BT1003 checks the CI surface for the new R3 edgewise/fat-tower workflow.

## Workflow

```text
.github/workflows/r3-edgewise-fat-tower.yml
```

## Connector result

Checked commit:

```text
12cadf5d49b6bc66bc167e65c57ee42bc5804891
```

The GitHub connector returned:

```text
combined statuses: 0
workflow runs surfaced: 0
```

## Reading

The workflow file is committed, but the connector did not surface a run/status
for the checked commit. The next verification should use the GitHub Actions UI or
GitHub CLI with Actions read access.

## Witnesses

```text
analysis/bt1003_ci_status_probe.py
data/bt1003_ci_status_probe.json
```
