# BT1273 -- External Candidate Pytest Regression

## Purpose

BT1273 protects the BT1269, BT1271, and BT1272 external-candidate pipeline through pytest.

## New test file

```text
tests/test_bt1269_bt1272_external_candidates.py
```

## Checks

The pytest file checks:

1. BT1269 schema required fields.
2. BT1269 edge-split required fields.
3. Exact polar path fixture scores pass with score 5.
4. Diameter-12 fixture scores review with score 2.
5. Sparse full-closure fixture scores fail with score 1.
6. Not-full-order fixture scores fail with score 0.

## Boundary

This is pytest-based CI protection rather than another append to the large named regression file. CI already runs `python -m pytest -q`, so the new tests are included in the standard test pass.
