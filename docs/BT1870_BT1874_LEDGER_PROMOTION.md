# BT1870-BT1874 — Ledger Promotion Rows

| Claim | Tier | Witness / command | Output artifact | Pass condition | Boundary |
|---|---:|---|---|---|---|
| Physical E8 representative model boundary | C/E | `analysis/bt1870_physical_e8_representative_model.py` | `data/PART_BT1870_PHYSICAL_E8_REPRESENTATIVE_MODEL_summary.json` | model fields specify support pair, integral E8 vectors, A2 coordinates, phase bit, Gram/metric data, and chain-boundary compatibility | Specification only; no integral vectors constructed. |
| Central-inversion phase transport test | E/C | `analysis/bt1871_central_inversion_phase_transport_test.py` | `data/PART_BT1871_CENTRAL_INVERSION_PHASE_TRANSPORT_TEST_summary.json` | phase bits 0 and 1 fix the winner-2 H support selector; winner 2 remains the support-metric result | No vector-level phase transport claimed. |
| Central-inversion wording audit | E/C | `analysis/bt1872_central_inversion_wording_audit.py` | `data/PART_BT1872_CENTRAL_INVERSION_WORDING_AUDIT_summary.json` | active path says central inversion in O(A2), outside plain W(A2) | Some generated/archive summaries may contain historical wording until regenerated. |
| BT1869 holonet merge patch | C/E | `analysis/bt1873_holonet_machine_bt1869_merge_patch.py` | `data/PART_BT1873_HOLONET_MACHINE_BT1869_MERGE_PATCH_summary.json` | anchor, canonical selector, 48 split, O(A2)/W(A2) phase class, final boundary present | Patch witness only; not full paper rewrite/PDF build. |
| Final selector quotient certificate | E/C | `analysis/bt1874_final_selector_quotient_certificate.py` | `data/PART_BT1874_FINAL_SELECTOR_QUOTIENT_CERTIFICATE.json`; summary JSON | canonical selector, quotient stages, phase bit, closed support shadow, exactly one open E8 representative-lift boundary | Certificate does not solve final integral representative lift. |

## Current terminal state

Everything visible on the mod-2 H support shadow is closed. The remaining problem is the concrete integral E8 representative phase lift for the central-inversion class, with chain-boundary compatibility.
