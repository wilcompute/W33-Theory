# BT1294 -- Recovery Workflow Unified Verifier

## Purpose

BT1294 wires the unified release-packet verifier into the dedicated recovery-packet workflow.

## Workflow

```text
.github/workflows/recovery-packet.yml
```

## New command

```bash
python tools/bt1291_verify_release_packet.py
```

## Expanded pytest step

The workflow now runs the recovery packet tests, recovery docs tests, and README recovery pointer test.

## Consequence

The dedicated workflow now checks both the strict recovery certificate and the full release-packet gate.
