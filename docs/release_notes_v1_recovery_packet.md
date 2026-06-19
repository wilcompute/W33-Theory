# v1.0.0 Recovery Packet Release Note

This release includes the finite Clifford recovery packet as a reproducibility artifact.

## Entry points

```text
docs/recovery_packet_landing.md
data/bt1279_recovery_packet_index.json
data/bt1275_strict_polar_path_recovery_certificate.json
```

## Verification

```bash
python tools/bt1291_verify_release_packet.py
python tools/bt1281_verify_recovery_certificate.py
python tools/bt1274_batch_score_candidates.py
```

Expected results:

```text
release packet verified = true
certificate verified = true
candidate bands = pass 1, review 1, fail 2
```

## Target

```text
diam14_polar_path
order 51840
diameter 14
edge split P4/P4
labelled spread 172
strict score 5/5
```
