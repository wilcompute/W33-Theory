# BT1265 -- Regression Through BT1264

## Purpose

BT1265 extends the named Clifford/R3/recovery regression suite through the tomography score vector.

## New checks

The regression now asserts:

1. BT1264 winner is `diam14_polar_path`.
2. Ranked regime order is:

```text
diam14_polar_path, diam12, diam10_A, diam10_B, diam10_C
```

3. The polar path regime scores `5/5`.
4. The diameter-12 regime scores `2/5`.
5. The diameter-10_B regime scores `1/5`.

## File

- Updated test: `tests/test_bt1231_bt1233.py`

## Boundary

This protects BT1264. It does not add a generic candidate validator; that is BT1266.
