# BT1280 -- Recovery Packet Guide

## Purpose

BT1280 adds a human-facing guide for using the finite Clifford recovery packet.

## Guide file

```text
docs/recovery_packet_guide.md
```

## Covered workflow

The guide explains:

1. How to create a schema-shaped candidate JSON.
2. How to score one candidate with `tools/bt1272_score_candidate.py`.
3. How to batch-score all bundled fixtures with `tools/bt1274_batch_score_candidates.py`.
4. How to inspect the strict polar-path recovery certificate.
5. Which paper sections explain the ladder, score vector, and external-candidate protocol.
6. Where to find the one-stop packet index.

## Boundary

This is documentation only. Machine verification is added in BT1281.
