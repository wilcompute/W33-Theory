# BT1020 — Workflow runbook summary

BT1020 adds the external execution protocol for workflows that the connector can
commit but cannot dispatch.

## Runbook

```text
docs/BT1020_workflow_runbook.md
```

## Trigger order

```text
k3-middle-rank-smoke.yml
r3-k3-long-heat.yml
paper-build.yml
```

## Expected artifacts

```text
k3-middle-rank-smoke-data
k3-heat-long-run-data
paper-build-pdfs
```

## Boundary

The runbook does not claim these workflows have run. It records the exact Actions
UI or equivalent CLI/token execution protocol, expected outputs, and first triage
checks.

## Witnesses

```text
docs/BT1020_workflow_runbook.md
data/bt1020_workflow_runbook.json
```
