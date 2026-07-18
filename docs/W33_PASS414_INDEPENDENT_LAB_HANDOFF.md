# W33 Pass 414 — Independent Laboratory Handoff

## Purpose

This packet lets an external laboratory run the Pass-409 four-gate Choi-visibility falsifier without receiving the gate-label key before the blinded analysis is frozen. It adds cryptographic custody and independent audit requirements to the existing Pass-397 `seal -> analyze -> unblind` contract.

## Roles

Five roles are deliberately separated:

1. **Protocol owner** — freezes the protocol and success/failure rule.
2. **Acquisition laboratory** — accepts the BOM, calibrates the apparatus, and acquires blinded counts.
3. **Blind-key custodian** — creates and holds the gate-code mapping until blinded analysis completion.
4. **Blinded analyst** — receives counts and calibration but not the key.
5. **Independent auditor** — verifies signatures, hashes, timestamps, role separation, and the final claim boundary.

A production organization may assign several people from one institution, but the acquisition signer, key custodian, blinded analyst, and auditor must use distinct signing keys and must satisfy the prohibited-role overlaps in the manifest.

## Artifact chain

The following eight artifacts are mandatory and hash-linked:

1. frozen protocol;
2. accepted bill of materials;
3. calibration certificate;
4. blinded raw counts;
5. blinded analysis;
6. blind key;
7. unblinded result;
8. independent audit.

Each artifact receives an Ed25519 envelope over its SHA-256 digest, artifact type, signer role, and signing timestamp. The packet verifies signatures against the public keys frozen in the handoff manifest.

## Timing law

The required ordering is

```text
protocol freeze
  < BOM acceptance and calibration
  < acquisition start <= acquisition completion
  < blinded analysis completion
  < key reveal
  < independent audit completion.
```

Any violation invalidates claim eligibility. The key must not be copied into raw-count, calibration, or blinded-analysis storage before the analysis hash is frozen.

## Production procedure

1. Copy `data/w33_pass414_empty_handoff_manifest.json` and populate the study ID, device ID, organizations, contacts, and public keys.
2. Validate the manifest against `schemas/w33_pass414_independent_lab_handoff_v1.schema.json`.
3. Freeze and sign the Pass-409 protocol and BOM before acquisition.
4. Complete source, mode-overlap, loss, dark-count, phase-linearity, tritter-balance, timing, and detector acceptance tests. Sign the calibration certificate.
5. Acquire four-phase counts under blind gate codes with no gate labels in the raw file. Sign the raw-byte hash immediately after acquisition.
6. Run Pass 397 `seal` and `analyze` without access to the blind key. Sign the blinded-analysis hash.
7. The key custodian releases and signs the key only after the blinded-analysis timestamp.
8. Run Pass 397 `unblind` **without** `--test-mode`.
9. The independent auditor re-hashes every artifact, verifies each Ed25519 signature and timestamp, checks role separation, and signs the audit report.

## Acceptance tests

At minimum, the external laboratory must record:

- heralded-source identity and count stability;
- 27-mode identity and routing map;
- mode-overlap and non-dark fractions;
- phase response at `0, pi/2, pi, 3pi/2` and at the non-Clifford offsets `+/-2pi/9` if Pass 411 is included;
- tritter transfer matrix and imbalance;
- coupler insertion loss and crosstalk;
- delay-register timing and jitter;
- detector efficiency, dark rate, dead time, and timestamp synchronization;
- raw shot conservation for every row;
- exact software commit and schema versions.

## Claim boundary

The deterministic fixture in `data/w33_pass414_nonclaim_custody_fixture.json` exists only to test signatures and role ordering. Its private keys are derived from public labels and are permanently invalid for production. Passing the fixture establishes software-contract integrity only. It is not evidence that a photonic experiment occurred or that the architecture works physically.
