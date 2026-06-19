# BT1291 -- Unified Release Packet Verifier

## Purpose

BT1291 adds one verifier for the v1.0.0 release packet.

## Files

```text
tools/bt1291_verify_release_packet.py
data/bt1291_release_packet_verification_summary.json
```

## Gate coverage

The verifier checks the release metadata, paper-build workflow, release instructions, recovery addendum, README packet pointer, recovery workflow, packet index, strict certificate, certificate-verification summary, and release manifest.

## Result

```text
verified = true
```

## Consequence

The release-prep layer and recovery-packet layer now have one machine-readable gate.
