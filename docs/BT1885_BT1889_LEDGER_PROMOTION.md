# BT1885-BT1889 — Ledger Promotion Rows

| Claim | Tier | Witness / command | Output artifact | Pass condition | Boundary |
|---|---:|---|---|---|---|
| Explicit Z40 representative schema | C/E | `analysis/bt1885_explicit_z40_representative_schema.py` | `data/PART_BT1885_EXPLICIT_Z40_REPRESENTATIVE_SCHEMA.json`; summary JSON | eight sparse Z40 rows; vectors length 40; supports lie inside BT982 vertex subset/fallback | Candidate sparse representatives only. |
| Chain A/2 operator locator | C/E | `analysis/bt1886_chain_A_over_2_operator_locator.py` | `data/PART_BT1886_CHAIN_A_OVER_2_OPERATOR_LOCATOR_summary.json` | repo search recorded; no named A/2 operator found; W33 adjacency-derived form `G40 = 2I - A_W33` selected as first candidate | Candidate metric/chain form, not proven boundary operator. |
| Vertex-subset embedding test | E/C | `analysis/bt1887_vertex_subset_embedding_test.py` | `data/PART_BT1887_VERTEX_SUBSET_EMBEDDING_TEST_results.json`; summary JSON | sparse Z40 direct `G40` evaluations agree with vertex-restricted evaluations | Metric-form consistency only, not full boundary proof. |
| Sparse Z40 phase action | E/C | `analysis/bt1888_phase_action_sparse_z40.py` | `data/PART_BT1888_PHASE_ACTION_SPARSE_Z40_results.json`; summary JSON | central-inversion phase preserves sparse-Z40 `G40` contributions | Candidate-form invariance only. |
| Final selector status paper patch | C/E | `paper/BT1889_final_selector_status_patch.tex` | `data/PART_BT1889_FINAL_SELECTOR_STATUS_PATCH_summary.json` | paper status states BT982 bridge, sparse Z40 metric-form tests, and remaining A/2 operator boundary | Insert only; no full paper/PDF build. |

## New terminal boundary

The sparse Z40 lift and central-inversion phase are consistent for the W33 adjacency-derived candidate form `G40 = 2I - A_W33`. The remaining problem is to identify or prove the actual Z40 chain A/2 boundary/operator model and verify the mapped phase action there.
