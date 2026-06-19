# BT1296 -- Readiness Badge Verifier

## Purpose

BT1296 adds an executable verifier for the BT1295 v1 release-readiness badge.

## Files

```text
tools/bt1296_verify_release_readiness_badge.py
tests/test_bt1295_bt1296_readiness_badge.py
```

## Checks

The verifier checks that the badge is ready, targets v1.0.0, targets `diam14_polar_path`, has strict score 5, has bundled band counts pass 1 / review 1 / fail 2, and agrees with the BT1291 release summary.

## Boundary

A direct edit to BT1291 was blocked by the connector safety layer, so BT1296 is a safe companion verifier.
