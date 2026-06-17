# BT1281 -- Strict Recovery Certificate Verifier

## Purpose

BT1281 adds a machine-readable verifier for the strict polar-path recovery certificate.

## Verifier

```text
tools/bt1281_verify_recovery_certificate.py
```

## Verification result

```text
data/bt1281_recovery_certificate_verification_summary.json
```

## Checks

The verifier checks:

1. Target is `diam14_polar_path`.
2. Closure order is `51840`.
3. Word diameter is `14`.
4. Edge split is `P4/P4`.
5. Labelled spread is `172`.
6. Score vector is `(1,1,1,1,1)`.
7. Validator result is pass with score `5`.
8. Batch band counts are pass `1`, review `1`, fail `2`.
9. Packet index points to the strict certificate.
10. Packet index target matches the certificate target.

## Consequence

The strict recovery certificate is now automatically checkable against the aggregate candidate scoring result and the packet index.
