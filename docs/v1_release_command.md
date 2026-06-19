# v1.0.0 Release Command

Before publishing `v1.0.0`, run one command from the repository root:

```bash
bash tools/bt1299_run_v1_release_gates.sh
```

Expected final line:

```text
BT1299 v1 release gates passed
```

This command checks:

```text
strict recovery certificate
external candidate batch scores
unified release packet
release readiness badge
paper-build handshake
release pytest subset
```

Single source of truth:

```text
data/bt1303_v1_release_source_of_truth_index.json
```

Readiness badge:

```text
data/bt1295_v1_release_readiness_badge.json
```

Paper-build handshake:

```text
python tools/bt1300_verify_paper_build_handshake.py
```

Recovery release note:

```text
docs/release_notes_v1_recovery_packet.md
```
