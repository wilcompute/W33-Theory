# BT1250 -- Regression Through BT1249

## Purpose

BT1250 extends the named Clifford/R3/recovery regression suite through the stabilizer and paper-section layer.

## New checks

The regression now asserts:

1. BT1242 structural summary fields are present and correct.
2. BT1248 stabilizer orders by diameter are exact:
   - diameter 10: stabilizers 4, 8, 16;
   - diameter 12: stabilizer 2;
   - diameter 14: stabilizer 4.
3. BT1249 paper section files exist.
4. The integrator knows both BT1236 and BT1249 section input paths.

## File

- Updated test: `tests/test_bt1231_bt1233.py`

## Boundary

This protects the current witness stack. It does not add new mathematical classification beyond BT1248/BT1249.
