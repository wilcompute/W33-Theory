# Part DCCCXIV - Phenomenology Claim-Ledger Audit

**Verifier:** `verify_dcccxiv_phenomenology_claim_ledger_audit.py`
**Tests:** `tests/test_dcccxiv_phenomenology_claim_ledger_audit.py`
**Data:** `data/dcccxiv_phenomenology_claim_ledger_audit.json`

---

## 1. Why This Part Exists

The May 17 GitHub burst added Parts DCCLXXXIV-DCCCXIII as a broad
phenomenology layer: neutrino masses, CKM/PMNS, Higgs/top/W/g-2, dark matter,
inflation, lensing, and baryogenesis.

Those files are useful as a frontier ledger, but they are not all the same
kind of claim. Some are marked proven, some are predictions, some are partial,
and some explicitly record tensions. DCCCXIV makes that distinction executable.

---

## 2. What The Audit Checks

The audit verifies:

- the 784..813 result ledger is contiguous and has 30 result JSON files,
- every result JSON has a matching theorem note,
- status strings are classified instead of treated as uniformly proven,
- DCCXCVIII master verification is stale because it only verifies through 797,
- internal sigma/status mismatches are surfaced.

The current concrete mismatch is DCCCII: the result text says the top-mass
claim is within `1 sigma`, while the same JSON carries `residual_sigma = 3.3`
and `pole_residual_sigma = 16.3`.

---

## 3. Architecture Read

This does not reject the phenomenology burst. It upgrades it into a ledger with
explicit proof status:

```text
claimed_proven / prediction / partial / tension / mixed
```

The live finite-geometry core remains separate from broad low-energy
phenomenology until each item has verifier coverage and stable regime labels.

---

## 4. Boundary

This is a claim-hygiene theorem. It checks internal result-JSON consistency and
public status labeling. It does not validate the physical derivations,
external experimental inputs, or correctness of the phenomenological model.
