# W33 Pass 419 — Adversarial Replication Rehearsal

Pass 419 replaces the production-facing Pass-414 v1 envelope with a chain-bound v2 contract. The v1 fixture remains useful as a software signature demonstration, but its signatures do not bind the study, device, nonce, sequence, or predecessor artifact. A valid v1 artifact can therefore be replayed into another manifest unless an external auditor adds those checks.

## Hardened v2 envelope

Every signature now binds:

- study ID and device ID;
- a 128-bit manifest nonce;
- artifact type and sequence number;
- signer role and registered public key;
- SHA-256 of the payload;
- SHA-256 of the preceding signed envelope;
- signing timestamp.

This creates one ordered custody chain rather than eight independently signed objects.

## Mandatory policy checks

The independent verifier additionally requires:

1. five distinct role keys;
2. protocol, BOM, and calibration hashes bound through the payloads;
3. raw-count and analysis payloads with no gate labels;
4. raw bytes whose SHA-256 and row count match both the manifest and frozen protocol;
5. key release strictly after blinded-analysis freeze;
6. an audit signed after unblinding;
7. nonclaim fixtures to retain `physical_experiment_completed=false` and `claim_eligible=false`.

## Attack suite

The deterministic rehearsal attempts timestamp substitution, key leakage, cross-study replay, cross-device replay, role-key collision, calibration substitution, unsigned row deletion, re-signed row deletion, predecessor reordering, nonce substitution, and claim-flag forgery. Every attack must fail for an explicit reason.

The included keys and raw counts are deterministic test fixtures. They are invalid for production and do not represent a physical experiment.
