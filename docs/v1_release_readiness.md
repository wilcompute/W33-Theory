# v1.0.0 Release Readiness

Status:

```text
ready = true
badge = v1-release-ready
```

Release target:

```text
v1.0.0
```

Strict recovery target:

```text
diam14_polar_path
```

Primary machine badge:

```text
data/bt1295_v1_release_readiness_badge.json
```

Unified verifier:

```bash
python tools/bt1291_verify_release_packet.py
```

Expected outputs:

```text
release packet verified = true
certificate verified = true
candidate bands = pass 1, review 1, fail 2
strict score = 5/5
```

Human entrypoints:

```text
README.md
docs/recovery_packet_landing.md
docs/recovery_packet_guide.md
docs/release_notes_v1_recovery_packet.md
```

Machine entrypoints:

```text
data/bt1279_recovery_packet_index.json
data/bt1287_recovery_packet_release_manifest.json
data/bt1291_release_packet_verification_summary.json
tools/bt1291_verify_release_packet.py
```
