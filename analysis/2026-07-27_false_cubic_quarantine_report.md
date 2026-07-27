# Step 1 — False-Cubic Quarantine: Dependency Scanner and Pre-Commit Guard

**Date:** 2026-07-27  
**Grounds:** Shifted-Adjacency Three-Mode Theorem (commit `9fb912f6`)  
**Corrected spectrum:** `spec(D) = 11¹ ⊕ 1²⁴ ⊕ (−5)¹⁵`

## What must be quarantined

The following identifiers originate exclusively from the false polynomial
`p_old(t) = (t+1)((t+1)²−36)` and carry no independent derivation:

| Identifier | False value | Why invalid |
|---|---|---|
| Eigenvalue set | `{−7, −1, 5}` | `p_old` annihilates none of the true eigenspaces |
| Multiplicities | `{16, 10, 6}` | Sum = 32 ≠ 40 = dim(point carrier) |
| 32-dimensional packet | implicit | No 32-dim eigenspace of D exists |
| `Z(−1) = 0` | claimed zero | `det(I − (−1)D) = (1+11)(1+1)²⁴(1−5)¹⁵ ≠ 0` |
| Taylor coefficients | `8, −248, …` | Derived from false generating function |
| Old minimal polynomial | `t³+3t²−33t−35` | `p_old(D)` has rank 40; annihilates nothing |

## Scanner

The script `analysis/w33_false_cubic_quarantine_scanner.py` performs a
repository-wide regex scan of all `.py`, `.tex`, `.md`, `.json`, `.txt` files
and classifies each hit:

- **COPY_INVALIDATED** — verbatim copy with no independent derivation; must be
  annotated or superseded.
- **DERIVED_MANUAL_REVIEW** — file contains its own derivation chain; needs
  human verification that the derivation is independent of `p_old`.
- **POSSIBLY_AWARE_NEEDS_REVIEW** — file references both old and new spectra;
  needs reconciliation comment.
- **SUPERSEDED_BY_ERRATUM** — the erratum or audit files themselves; excluded.

Output: `data/QUARANTINE_2026_07_27_false_cubic_scan.json`

## Pre-commit guard specification

Add the following rule to `.pre-commit-config.yaml` (or create it):

```yaml
- repo: local
  hooks:
    - id: w33-false-cubic-guard
      name: Block reintroduction of false W(3,3) cubic eigendata
      language: python
      entry: python analysis/w33_false_cubic_quarantine_scanner.py
      types: [python, tex, markdown, json]
      pass_filenames: false
      stages: [commit]
      # Fail if any COPY_INVALIDATED hits appear in staged files
```

For a stricter guard, the scanner can be adapted to exit with code 1 on any
`COPY_INVALIDATED` classification in modified files.

## Positive replacement rule

Every location that previously used `{−7, −1, 5}` for spectral computation
must be replaced by `{11, 1, −5}` with multiplicities `{1, 24, 15}` and the
rational projectors:

```
P_11 = (D − I)(D + 5I) / 160
P_1  = −(D − 11I)(D + 5I) / 60
P_-5 = (D − 11I)(D − I) / 96
```

Every polynomial propagator on the point carrier reduces uniquely to a
quadratic in D via `D³ = 7D² + 49D − 55I`.

## Status

- [x] Corrected spectrum proven and committed (`9fb912f6`)
- [x] Scanner script committed (`w33_false_cubic_quarantine_scanner.py`)
- [ ] Scanner run across full working tree — run locally and commit JSON
- [ ] Pre-commit hook installed
- [ ] All COPY_INVALIDATED hits annotated or superseded
