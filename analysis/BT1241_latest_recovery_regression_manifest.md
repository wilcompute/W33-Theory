# BT1241 -- Latest Recovery Regression Manifest

## Purpose

BT1241 extends the named Clifford/R3 CI checkpoint through BT1240.

## Changes

The regression file now asserts the BT1240 synthetic recovery harness:

- exact case passes with order 51840 and diameter 14;
- dropped-generator case fails and collapses to order 648;
- swapped-generator case fails despite full order 51840 because its word metric changes;
- identity replacement fails the local order-three law.

The CI step is now named:

```text
Run latest BT Clifford/R3/recovery regressions
```

and still runs:

```bash
python tests/test_bt1231_bt1233.py
```

## Boundary

This is regression wiring. It does not prove new Clifford structure; it protects the already-pushed BT1231--BT1240 witness layer from silent drift.
