# BT1239 -- BT1236 Integration Sanity Checker

## Purpose

BT1239 adds a static checker for the BT1236 paper insert and its integrator.

## Checks

The checker verifies:

1. the BT1236 source insert exists;
2. the integrator exists;
3. the source insert contains the key Clifford and word-metric formulas;
4. the preprint input line appears zero or one times, never more;
5. if the generated paper section exists, it exactly matches the source insert.

## Current status

```text
ready_to_integrate
```

The source insert and integrator are present, the key formulas are present, and the preprint has no duplicate input line. The generated paper section appears after running:

```bash
python tools/integrate_bt1236_insert.py
```

## Boundary

This checker does not mutate the paper. It detects missing source, missing integrator, duplicate input, and section/source drift.

## Files

- Code: `analysis/bt1239_bt1236_integration_sanity.py`
- Result: `data/bt1239_bt1236_integration_sanity_summary.json`
