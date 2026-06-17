# BT1246 -- BT1236 Runtime Paper Inclusion

## Purpose

BT1246 makes the BT1236 paper inclusion deterministic in CI/checkouts without risking a full-file manual rewrite of `paper/w33_preprint.tex` through the connector.

## CI step

The workflow now runs:

```bash
python tools/integrate_bt1236_insert.py
python analysis/bt1239_bt1236_integration_sanity.py
```

before the Clifford/R3/recovery regression suite.

## Why this route

The GitHub connector supports full-file replacement for existing files, not patch-style editing. The main preprint is a multi-hundred-line file, and the connector output truncates long file bodies. Reconstructing it manually would risk corrupting the manuscript.

The safe route is to keep the section materialized and run the already-pushed idempotent integrator in CI/checkouts. That produces the input insertion deterministically without duplicating it.

## Boundary

This is runtime/check-out integration. The committed `paper/w33_preprint.tex` still lacks the input line until the integrator is run or the file is safely patched in a normal checkout.
