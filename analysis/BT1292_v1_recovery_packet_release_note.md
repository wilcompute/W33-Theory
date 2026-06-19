# BT1292 -- v1 Recovery Packet Release Note

## Purpose

BT1292 adds a compact ready-to-paste release note block for v1.0.0.

## File

```text
docs/release_notes_v1_recovery_packet.md
```

## Contents

The note names the recovery packet entry points, verification commands, expected outputs, and strict target summary.

## Expected outputs

```text
release packet verified = true
certificate verified = true
candidate bands = pass 1, review 1, fail 2
```

## Consequence

The release can now advertise the finite Clifford recovery packet with a concise reproducibility block.
