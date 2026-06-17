# BT1247 -- Promote Structural Invariants into BT1242

## Purpose

BT1247 merges the BT1245 structural explanation back into the BT1242 classifier output.

## Change

`analysis/bt1242_four_transvection_regime_classifier.py` now emits:

- global order counts;
- global order-and-diameter counts;
- full-order structural summaries;
- local pair/triple closure patterns;
- diagnostic rules for diameter 10, 12, and 14 regimes.

## Full-order structural summary

```text
diam10: 22680 sets, 3 patterns
diam12: 25920 sets, 1 pattern
diam14: 12960 sets, 1 pattern
```

## Key rule

The BT1228 / BT1233 regime is the diameter-14 full-order regime with pair orders `9^3 24^3` and triple orders `72^2 648^2`.

## Boundary

This is an integration/refactor artifact. It preserves the BT1242 counts and promotes the BT1245 explanation into the primary classifier output.
