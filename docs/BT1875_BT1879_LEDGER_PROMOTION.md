# BT1875-BT1879 — Ledger Promotion Rows

| Claim | Tier | Witness / command | Output artifact | Pass condition | Boundary |
|---|---:|---|---|---|---|
| Integral E8 representative template | C/E | `analysis/bt1875_integral_e8_representative_template.py` | `data/PART_BT1875_INTEGRAL_E8_REPRESENTATIVE_TEMPLATE.json`; summary JSON | 8 rows = 4 selector pairs x 2 phase bits; required BT1870 fields present; BT982 basis source linked | Template only; integral vectors and chain-boundary compatibility pending. |
| Representative existence search | E/C | `analysis/bt1876_representative_existence_search.py`; `analysis/bt982_explicit_integral_e8_basis.py` | `data/PART_BT1876_REPRESENTATIVE_EXISTENCE_SEARCH_summary.json`; `data/bt982_explicit_integral_e8_basis.json` | BT982 found as primary basis candidate; final basis B and Cartan Gram checks recorded | Does not map BT982 basis columns onto BT1875 rows yet. |
| Corrected summaries regenerated | E/C | `analysis/bt1877_regenerate_corrected_summaries_audit.py` | `data/PART_BT1877_REGENERATE_CORRECTED_SUMMARIES_AUDIT_summary.json` | BT1860/BT1861/BT1864 summaries, ledger, and execution summary corrected to central inversion in O(A2) | Deep archives may retain historical wording. |
| BT1873 apply/check path | C/E | `analysis/bt1878_apply_bt1873_patch_plan.py` | `data/PART_BT1878_APPLY_BT1873_PATCH_PLAN_summary.json` | apply=True patch command and static TeX check command recorded | Plan only; no full paper rewrite/PDF build in connector pass. |
| Final selector dashboard | E/C | `docs/BT1879_FINAL_SELECTOR_CERTIFICATE_DASHBOARD.md` | `data/PART_BT1879_FINAL_SELECTOR_CERTIFICATE_DASHBOARD_summary.json` | human-readable table mirrors BT1874 certificate and BT1876 basis bridge | Dashboard only; final integral representative lift remains open. |

## New practical bridge

BT982 is now the explicit basis source. The next concrete move is to map `final_integral_basis_B` from BT982 onto the BT1875 support-pair/phase rows, then test chain-boundary compatibility.
