# BT1256 -- Regression Through BT1255

## Purpose

BT1256 extends the named Clifford/R3/recovery regression suite through BT1254 and BT1255.

## New checks

The regression now asserts:

1. BT1254 has eight labelled channels.
2. BT1254 records fixed-label orientation flips as explicit channel permutations.
3. BT1254 keeps the unlabelled Cayley sphere invariant.
4. BT1255 classifies the full-order zero-edge graphs as:
   - diam10_A: `K2+2I`;
   - diam10_B: `2K2`;
   - diam10_C: `empty_4I`;
   - diam12: `P3+I`;
   - diam14: `P4`.
5. BT1255 classifies the diameter-14 nonzero graph as `P4`.

## File

- Updated test: `tests/test_bt1231_bt1233.py`

## Boundary

This is regression protection for BT1254--BT1255. It does not add a new labelled-geodesic tensor or paper theorem.
