# BT1254 — BIJECTION_SOLVER_V3 pytest Suite: 9 Tests
**Date:** 2026-06-17  
**Status:** DEPLOYED ✓

## Test File
`tests/test_bijection_solver_v3.py`

## Tests Deployed

| Test | BT1248 Row | What it Verifies |
|---|---|---|
| `test_fermion_count` | Row 1 | PG(2,3) has 13 points = 12 fermions + Higgs |
| `test_gauge_boson_count` | Row 2 | K(3,3) has 9 matchings = 8 gluons + 1 photon |
| `test_color_charge_grading` | Row 3 | Ternary grades {0,1,2} non-empty and balanced |
| `test_parallel_classes` | Row 4 | 3 parallel classes × 3 matchings = 9 total |
| `test_chirality_polarity_involution` | Row 5 | Polarity map is an involution (L/R chirality) |
| `test_clifford_word_metric_diameter` | Row 6 | diam = 6 = #quark flavors (BT1247 link) |
| `test_anomaly_cancellation` | Row 7 | Charge sum = 0 mod 3 per generation |
| `test_k33_regularity` | Bonus | K(3,3) is 3-regular bipartite |
| `test_pg2_3_line_structure` | Bonus | PG(2,3) has 13 lines of size 4 |

## CI Integration
New workflow: `.github/workflows/bijection-tests.yml`  
Triggers on: push to master (touching tests or BIJECTION_SOLVER_V3.py), PRs, manual dispatch.

## Usage
```bash
pip install pytest
pytest tests/test_bijection_solver_v3.py -v
```
Expected output: **9 passed** in < 1 second (pure Python, no external dependencies).

## Significance
The SM bijection is now **machine-checkable and CI-gated**. Every merge to master automatically re-verifies the core geometric claims of the W(3,3) ↔ Standard Model correspondence.
