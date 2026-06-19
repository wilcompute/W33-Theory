# BT1293 -- Release Packet Regression

## Purpose

BT1293 adds pytest protection for the BT1290--BT1292 release-packet layer and the BT1294 workflow wiring.

## New test file

```text
tests/test_bt1290_bt1292_release_packet.py
```

## Checks

The tests assert:

1. BT1290 release addendum exists and contains the recovery-packet release gates.
2. BT1291 unified release verifier runs and returns `verified=true`.
3. All BT1291 checks are true.
4. BT1292 release note block exists and contains the unified verifier command plus strict target summary.
5. The recovery-packet workflow runs the BT1291 unified verifier and includes the README recovery pointer regression.

## Boundary

This protects the release-packet layer. The final readiness badge is added in BT1295.
