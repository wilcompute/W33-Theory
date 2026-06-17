# BT1253 -- Regression Through BT1252

## Purpose

BT1253 extends the named Clifford/R3/recovery regression suite through the ordered/oriented invariance and polar-path tetrahedron layers.

## New checks

The regression now asserts:

1. BT1251 has exactly \(4!2^4=384\) labelled/oriented variants.
2. BT1251 leaves the unlabelled symmetric Cayley sphere and ball checkpoints invariant.
3. BT1252 has polar zero-edge graph \(P_4\).
4. BT1252 has nonpolar edge graph \(P_4\).
5. BT1252 records the balanced pair/triple closure laws \(9^3 24^3\) and \(72^2 648^2\).

## File

- Updated test: `tests/test_bt1231_bt1233.py`

## Boundary

This protects BT1251--BT1252. It does not add new regime geometry beyond those artifacts.
