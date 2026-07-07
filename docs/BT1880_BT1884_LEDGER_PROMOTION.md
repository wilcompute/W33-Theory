# BT1880-BT1884 — Ledger Promotion Rows

| Claim | Tier | Witness / command | Output artifact | Pass condition | Boundary |
|---|---:|---|---|---|---|
| BT982-to-BT1875 mapper | E/C | `analysis/bt1880_bt982_to_bt1875_mapper.py` | `data/PART_BT1880_BT982_TO_BT1875_MAPPED_TEMPLATE.json`; summary JSON | eight mapped rows; BT982 basis columns cover 0..7; chain boundary remains pending | Candidate vector population only. |
| Chain-boundary compatibility tester | C/E | `analysis/bt1881_chain_boundary_compatibility_tester.py` | `data/PART_BT1881_CHAIN_BOUNDARY_COMPATIBILITY_TEST_results.json`; summary JSON | mapped vectors are integral 8-coordinate BT982 vectors; boundary not falsely passed | Explicit Z^40 chain A/2 model still required. |
| Central-inversion vector action | E/C | `analysis/bt1882_central_inversion_vector_action.py` | `data/PART_BT1882_CENTRAL_INVERSION_VECTOR_ACTION_results.json`; summary JSON | phase-1 simultaneous vector negation preserves slot Gram contributions | Vertex-E8 Gram test only, not Z^40 chain-boundary proof. |
| Final certificate upgrade | E/C | `analysis/bt1874_final_selector_quotient_certificate.py` | `data/PART_BT1874_FINAL_SELECTOR_QUOTIENT_CERTIFICATE.json`; summary JSON | BT982 basis, BT1880 mapping, BT1882 Gram action recorded; only Z^40 chain boundary open | Certificate upgrade only. |
| Paper patch apply/check bundle | C/E | `analysis/bt1884_paper_patch_apply_check_bundle.py` | `data/PART_BT1884_PAPER_PATCH_APPLY_CHECK_BUNDLE_results.json`; summary JSON | apply command, static TeX check, and certificate refresh command recorded | Command bundle only; no connector-side PDF build. |

## New terminal boundary

The integral vertex-E8 basis exists via BT982, is mapped into selector-pair/phase rows by BT1880, and the central-inversion phase preserves vertex-E8 Gram contributions by BT1882. The only remaining explicit mathematical boundary is the Z^40 chain A/2 representative/boundary model.
