# BT1288 -- README Recovery Packet Pointer

## Purpose

BT1288 adds a root-level pointer from `README.md` to the recovery packet.

## README additions

The README now contains a `Recovery Packet` section pointing to:

```text
docs/recovery_packet_landing.md
data/bt1279_recovery_packet_index.json
data/bt1275_strict_polar_path_recovery_certificate.json
```

## Regression

A dedicated pytest protects those README references:

```text
tests/test_bt1288_readme_recovery_pointer.py
```

## Boundary

The README update was intentionally small and near the top of the file so future readers can find the packet before diving into the rest of the repository.
