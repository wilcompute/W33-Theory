# BT1277 -- Recovery Packet Regression

## Purpose

BT1277 protects the BT1274--BT1276 recovery-packet layer through pytest.

## New test file

```text
tests/test_bt1274_bt1276_recovery_packet.py
```

## Checks

The tests assert:

1. Batch scoring sees four external candidates.
2. Batch scoring band counts are pass 1, review 1, fail 2.
3. Exact polar path passes.
4. Diameter-12 candidate reviews.
5. Sparse full-closure candidate fails.
6. Not-full-order candidate scores 0.
7. Strict certificate has target `diam14_polar_path`, closure order `51840`, word diameter `14`, edge split `P4/P4`, labelled spread `172`, score vector `(1,1,1,1,1)`, and validator band `pass`.
8. External protocol paper section exists and contains the protocol keywords.

## Boundary

This is pytest protection. CI already runs `python -m pytest -q`, so these checks are included in the normal test path.
