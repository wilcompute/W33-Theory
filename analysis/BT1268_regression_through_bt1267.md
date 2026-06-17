# BT1268 -- Regression Through BT1267

## Purpose

BT1268 extends the named Clifford/R3/recovery regression suite through the operational validator and score-vector paper section.

## New checks

The regression now asserts:

1. BT1266 validator bands:
   - `exact_polar_path`: pass;
   - `wrong_full_order_diam12`: review;
   - `closure_only`: fail;
   - `not_full_order`: score 0.
2. BT1267 paper section exists.
3. BT1267 section contains `Tomography score vector`, `S=(C,D,P,E,L)`, and `5/5`.

## File

- Updated test: `tests/test_bt1231_bt1233.py`

## Boundary

This protects BT1266--BT1267. External candidate schema validation is added separately in BT1269.
