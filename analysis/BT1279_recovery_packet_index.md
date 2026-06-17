# BT1279 -- Recovery Packet Index

## Purpose

BT1279 adds one discoverable index for the finite Clifford recovery protocol.

## Index file

```text
data/bt1279_recovery_packet_index.json
```

## Indexed packet pieces

The index points to:

1. Candidate schema.
2. External candidate fixtures.
3. Single and batch scoring tools.
4. Batch scoring result.
5. Strict polar-path recovery certificate.
6. Paper sections for the ladder, score vector, and external protocol.
7. CI companion integrators.
8. Pytest regression files.

## Strict target

```text
diam14_polar_path
```

## Batch result

```text
pass = 1
review = 1
fail = 2
```

## Consequence

The external Clifford recovery protocol is now discoverable from one JSON artifact and one markdown explanation.
