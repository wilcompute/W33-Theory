# BT1287 -- Recovery Packet Release Manifest

## Purpose

BT1287 makes the recovery packet release-aware after the latest release-prep commit.

## Context

The most recent inspected commit was:

```text
6319e97866726d11db4670466c9574538477045c
```

It fixed the paper-build path under `paper/`, deployed `.zenodo.json`, added compile stubs, and prepared v1.0.0 release instructions.

## Manifest

```text
data/bt1287_recovery_packet_release_manifest.json
```

## Manifest contents

The manifest lists:

1. Release target `v1.0.0`.
2. Strict target `diam14_polar_path`.
3. Strict certificate and verifier summary.
4. Packet index and schema.
5. Human docs.
6. Scoring and verification tools.
7. Tests.
8. Dedicated recovery-packet workflow.
9. Expected outputs: certificate verified, batch bands pass 1 / review 1 / fail 2, strict score 5.

## Consequence

The recovery packet is now positioned as a release artifact rather than an isolated research note.
