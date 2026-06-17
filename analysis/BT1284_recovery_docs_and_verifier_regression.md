# BT1284 -- Recovery Docs and Verifier Regression

## Purpose

BT1284 protects the BT1280 through BT1283 recovery packet documentation and verification layer through pytest.

## New test file

```text
tests/test_bt1280_bt1282_recovery_docs.py
```

## Checks

The tests assert:

1. The human recovery guide exists.
2. The guide points to the schema, scorer, strict certificate, and packet index.
3. The strict recovery certificate verifier runs successfully.
4. The verifier summary is true on every check.
5. The BT1282 recovery packet paper section exists.
6. The BT1282 companion integrator exists.
7. The dedicated recovery-packet workflow exists and calls the BT1282 integrator plus the BT1281 verifier.

## Boundary

This is documentation and verifier regression protection. It does not add a public landing snippet; that follows in BT1285.
