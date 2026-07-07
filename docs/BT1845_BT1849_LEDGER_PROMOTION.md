# BT1845-BT1849 — Ledger Promotion Rows

| Claim | Tier | Witness / command | Output artifact | Pass condition | Boundary |
|---|---:|---|---|---|---|
| Transported tetracode S4 stabilizer action | E/C | `analysis/bt959_selected_minimizer_stabilizer_orbit.py`; `analysis/bt1845_tetracode_stabilizer_action_audit.py` | `data/bt959_selected_minimizer_stabilizer_orbit.json`; `data/PART_BT1845_TETRACODE_STABILIZER_ACTION_AUDIT_summary.json` | orbit size 24, stabilizer size 1, support-60 intersection singleton at minimizer 2 | Closes transported S4 quotient only; local A2/Weyl/glue refinement open. |
| Winner-2 canonical E8 selector basis | E | `analysis/bt1846_winner2_canonical_basis_export.py` | `data/PART_BT1846_WINNER2_CANONICAL_BASIS_EXPORT_summary.json` | canonical selector pairs `(3,68),(4,42),(38,65),(90,144)` labelled across four striations | Canonical runtime selector basis; not a full local quotient claim. |
| Shot protocol compression | P/S | `analysis/bt1847_shot_protocol_compression.py` | `data/PART_BT1847_SHOT_PROTOCOL_COMPRESSION_summary.json`; generated CSV | 1440 rows compress to 360 bundles, preserving four striations and 144000 nominal shots | Scheduling compression only; no measured data. |
| E8-labelled compiled trace runner | E/S | `analysis/bt1848_e8_labelled_trace_runner.py` | `data/PART_BT1848_E8_LABELLED_TRACE_RUNNER_summary.json`; generated JSONL | 1023-row trace gains compiled phase and canonical E8 selector labels | Runner spec; large labelled JSONL generated in repo environment. |
| Tetracode selector paper insert | C/E | `paper/BT1849_tetracode_selector_upgrade_insert.tex` | paper insert | states BT954/BT956 metric agreement and BT959 transported S4 rigidity | Insert, not full rebuilt PDF. |

Promotion rule: the selector is now metric-canonical and transported-S4-rigid. The only remaining quotient boundary is the local A2/Weyl/glue stabilizer refinement.
