# BT1002 — CI build integration

BT1002 adds a GitHub Actions workflow for the corrected R3 edgewise/fat-tower
stack.

## Workflow

```text
.github/workflows/r3-edgewise-fat-tower.yml
```

## Triggers

```text
push to master
pull_request to master
workflow_dispatch
```

## Smoke scripts

```text
analysis/bt991_local_4simplex_edgewise_template.py
analysis/bt993_edgewise_density_recurrences.py
analysis/bt1000_k3_level2_feasibility_gate.py
analysis/bt1001_full_heat_supertrace_estimator_stack.py
```

## Paper verification

The workflow runs:

```text
bash tools/bt999_apply_integrators_and_verify.sh
```

That applies the BT990/BT996 paper integrators, verifies markers, writes
`data/bt999_integrator_marker_check.json`, and runs `latexmk` when available.

## Artifacts

The workflow uploads the R3 JSON outputs and any generated PDFs.

## Reading

This makes the R3 edgewise/fat-tower stack reproducible in CI: local template,
density recurrence, feasibility gate, estimator manifest, paper marker checks,
and optional PDF artifacts are now wired together.
