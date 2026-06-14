# BT1020 — Paper and heat workflow runbook

This runbook records the exact external workflow steps needed because the current
connector can read commit statuses but does not expose workflow dispatch.

## Workflows

```text
.github/workflows/r3-k3-long-heat.yml
.github/workflows/paper-build.yml
.github/workflows/k3-middle-rank-smoke.yml
```

## Trigger order

1. Trigger `k3-middle-rank-smoke.yml` first.
2. Trigger `r3-k3-long-heat.yml` after the smoke workflow passes.
3. Trigger `paper-build.yml` after paper integrator changes land.

## Expected artifacts

```text
k3-middle-rank-smoke-data
k3-heat-long-run-data
paper-build-pdfs
```

Expected files:

```text
data/bt1015_k3_middle_stream_contracts.json
data/bt1016_k3_middle_rank_smoke_test.json
data/bt1018_k3_degree2_row_shard.json
data/bt1010_k3_64probe_heat_driver.json
data/bt1007_k3_heat_16probe_checkpoint.json
w33_paper.pdf
photonic_holonet.pdf
```

## Failure triage

- If Python import fails, check working directory and package path assumptions.
- If the rank smoke job fails, inspect the row weight and rank fields first.
- If heat workflow fails by time, reduce probes or move to a larger runner.
- If paper build fails, inspect the LaTeX log before changing source text.
- If no run appears, verify Actions are enabled for the repository and workflow
  dispatch is allowed.

## Boundary

This runbook does not claim the workflows have run. It is the external execution
protocol for Actions UI or equivalent CLI/token access.
