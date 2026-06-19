# BT1286 -- Recovery Landing Regression

## Purpose

BT1286 extends the recovery docs regression to protect the landing page and release manifest.

## Change

Updated:

```text
tests/test_bt1280_bt1282_recovery_docs.py
```

## Added checks

The test file now protects:

1. `docs/recovery_packet_landing.md`.
2. The landing links to the guide and packet index.
3. The landing states expected verified and batch-score outputs.
4. `data/bt1287_recovery_packet_release_manifest.json`.
5. The release manifest targets `v1.0.0` and points to the strict certificate.

## Boundary

A later README pointer was protected with a separate pytest file in BT1288 because full-file replacement of this test file was blocked by the connector safety layer on the second edit.
