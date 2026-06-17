# BT1259 -- Regression Through BT1258

## Purpose

BT1259 extends the named Clifford/R3/recovery regression suite through the labelled geodesic tensor and polar path paper theorem.

## New checks

The regression now asserts:

1. BT1257 has group order 51840 and diameter 14.
2. BT1257 is label-sensitive.
3. BT1257 first-channel totals include `g1p=16197` and `g2p=16025`.
4. BT1257 has a unique diameter-14 endpoint whose first-channel set has size 8.
5. BT1258 paper section exists.
6. BT1258 section contains the polar path identity `K_4=P_4` and the phrase `polar path tetrahedron`.
7. The integrator knows `sec_bt1258_polar_path_tetrahedron_theorem`.

## File

- Updated test: `tests/test_bt1231_bt1233.py`

## Boundary

This protects BT1257--BT1258. It does not compare labelled geodesic tensors across every regime; that is BT1260.
