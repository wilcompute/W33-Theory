# BT1302--BT1305 -- Release Closure

## Purpose

This pass closes the v1.0.0 release-gate layer.

## New workflow wiring

```text
.github/workflows/recovery-packet.yml
```

The workflow now runs the paper-build handshake and the one-command v1 release gate runner.

## New source of truth

```text
data/bt1303_v1_release_source_of_truth_index.json
```

This index links the readiness badge, gate matrix, runner, paper handshake, release note, recovery packet, and paper-build workflow.

## Human command doc

```text
docs/v1_release_command.md
```

The command is:

```bash
bash tools/bt1299_run_v1_release_gates.sh
```

Expected final line:

```text
BT1299 v1 release gates passed
```

## Regression

```text
tests/test_bt1302_bt1304_release_closure.py
```

The tests protect the workflow wiring, source-of-truth index, and release command doc.
