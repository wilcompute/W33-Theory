# BT1290 -- v1.0.0 Recovery Packet Release Addendum

## Purpose

BT1290 extends the v1.0.0 release instructions with explicit recovery-packet gates.

## Add to the pre-release checklist

```text
[x] Recovery packet guide and landing page present
[x] Recovery packet release manifest present
[x] Strict polar-path recovery certificate present
[x] Strict recovery certificate verifier present
[x] README points to the recovery packet
[ ] recovery-packet CI passes
```

## Recovery packet gate commands

```bash
python tools/bt1281_verify_recovery_certificate.py
python tools/bt1274_batch_score_candidates.py
python -m pytest -q tests/test_bt1269_bt1272_external_candidates.py tests/test_bt1274_bt1276_recovery_packet.py tests/test_bt1280_bt1282_recovery_docs.py tests/test_bt1288_readme_recovery_pointer.py
```

## Expected outputs

```text
certificate_verified = true
batch bands = pass 1, review 1, fail 2
strict target = diam14_polar_path
strict score = 5/5
```

## Release packet pointers

```text
docs/recovery_packet_landing.md
data/bt1287_recovery_packet_release_manifest.json
data/bt1275_strict_polar_path_recovery_certificate.json
data/bt1279_recovery_packet_index.json
```

## Release note addition

Mention that v1.0.0 includes the finite Clifford recovery packet: schema, fixtures, score tools, strict certificate, verifier, paper sections, and CI workflow.

## Boundary

A direct edit to `analysis/BT1259_v1_release_instructions.md` was blocked by the connector safety layer, so this addendum preserves the release-packet update as a separate file.
