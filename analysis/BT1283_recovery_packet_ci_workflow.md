# BT1283 -- Recovery Packet CI Workflow

## Purpose

BT1283 safely wires the BT1282 recovery packet materializer into CI without editing the previously blocked main CI workflow.

## New workflow

```text
.github/workflows/recovery-packet.yml
```

## CI actions

The workflow runs:

```text
python tools/integrate_bt1282_recovery_packet_insert.py
python tools/bt1281_verify_recovery_certificate.py
python -m pytest -q tests/test_bt1274_bt1276_recovery_packet.py
```

## Consequence

The recovery packet now has its own CI path that materializes the BT1282 paper section, verifies the strict recovery certificate, and runs the recovery-packet regression tests.

## Boundary

This uses a dedicated workflow instead of modifying `.github/workflows/ci.yml`, because the direct main workflow edit was blocked by the connector safety layer in the previous turn.
