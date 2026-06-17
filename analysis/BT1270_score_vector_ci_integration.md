# BT1270 -- Score Vector CI Integration

## Purpose

BT1270 adds a safe companion integrator for the BT1267 score-vector paper section and wires it into CI.

## New helper

```text
tools/integrate_bt1267_score_vector_insert.py
```

The helper copies the BT1267 analysis-side TeX source into the paper sections directory and inserts the BT1267 section line into the preprint when run.

## CI update

The CI paper-materialization step now runs the existing Clifford integrator, the BT1261 ladder companion integrator, the BT1267 score-vector companion integrator, and then the existing BT1239 integration sanity check.

## Boundary

This follows the same safe companion-integrator route used for BT1261, avoiding the connector block encountered when replacing the legacy integrator directly.
