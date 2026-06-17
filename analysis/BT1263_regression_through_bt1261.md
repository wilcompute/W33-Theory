# BT1263 -- Regression Through BT1261

## Purpose

BT1263 extends the named Clifford/R3/recovery regression suite through the cross-regime labelled geodesic comparison and Clifford tomography ladder section.

## New checks

The regression now asserts:

1. BT1260 channel spreads:
   - diam10_B: 0;
   - diam10_C: 0;
   - diam12: 339;
   - diam14_polar_path: 172.
2. BT1260 polar path diameter endpoint first-set histogram is `{8: 1}`.
3. BT1261 ladder section exists.
4. BT1261 section contains `Clifford tomography ladder` and `labelled geodesic tensor`.
5. The companion ladder integrator exists and knows `sec_bt1261_clifford_tomography_ladder`.

## File

- Updated test: `tests/test_bt1231_bt1233.py`

## Boundary

This protects BT1260--BT1261 and the companion integration route. The legacy integrator remains unchanged because full-file replacement of that file was blocked by the connector safety layer.
