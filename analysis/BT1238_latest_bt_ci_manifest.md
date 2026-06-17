# BT1238 -- Latest BT CI Manifest

## Purpose

BT1238 wires the BT1231--BT1233 regression stack into the repository CI path as a named checkpoint.

## CI change

The workflow now runs:

```bash
python tests/test_bt1231_bt1233.py
```

before the general pytest sweep.

## Protected artifacts

This named step protects:

1. BT1231 exact minimal projective-transvection count;
2. BT1232 fail-closed R3 evidence gate;
3. BT1233 exact word-metric fingerprint.

## Why this matters

The general pytest command should already discover the file, but an explicit CI step makes the Clifford/R3 witness lane visible in workflow logs and prevents it from being buried inside the larger test suite.

## Boundary

This is a CI wiring artifact. It does not run CI inside this chat session; it updates the GitHub Actions workflow so the repository executes the step on push / pull request.
