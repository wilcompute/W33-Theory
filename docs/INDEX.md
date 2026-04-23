# W33 Documentation Index

Navigator for the repository's paper sections, reproducibility paths, and formal proof tracks.

> Live status note: the current public-facing source of truth is [docs/index.html](./index.html), especially `#current-synthesis`, `#verified`, and `#open`, together with [docs/march_2026_frontier_note.md](./march_2026_frontier_note.md). Older summaries in this repo should be treated as preserved snapshots unless they explicitly say they are the live view.


## Primary Entry Points

| Audience | Start Here | Why |
|---|---|---|
| First-time reader (1-page) | [docs/LAYPERSON_ONE_PAGE_MAP.md](./LAYPERSON_ONE_PAGE_MAP.md) | Fast orientation with immediate run path |
| First-time reader | [docs/LAYPERSON_TEXTBOOK_GUIDE.md](./LAYPERSON_TEXTBOOK_GUIDE.md) | Full beginner textbook path with zero assumed physics background |
| Beginner practice | [docs/LAYPERSON_WORKBOOK.md](./LAYPERSON_WORKBOOK.md) | Step-by-step learning tasks with evidence collection |
| Beginner claim audit | [docs/LAYPERSON_EVIDENCE_AUDIT_TEMPLATE.md](./LAYPERSON_EVIDENCE_AUDIT_TEMPLATE.md) | Reproducibility-first template for scoring claim strength |
| Beginner concept navigation | [docs/LAYPERSON_CONCEPT_MAP.md](./LAYPERSON_CONCEPT_MAP.md) | Visual/structural map from objects to evidence paths |
| First-time reader (short) | [README.md](../README.md) | Short repo overview with a live-status note pointing back to the audited entrypoints |
| Live repo audit | [docs/repo_frontier_audit.html](./repo_frontier_audit.html) | Current repo-wide map: active folders, exactness tiers, and citation corrections |
| Local determinant-support boundary | [`scripts/w33_local_albert_shadow_audit.py`](../scripts/w33_local_albert_shadow_audit.py) | Consolidated executable local `H27/E6` cubic audit: `45 = 9 + 36`, five-tritangent incidence, and the cocycle-gauge boundary |
| Exact finite ladder | [`scripts/w33_qutrit_ladder_audit.py`](../scripts/w33_qutrit_ladder_audit.py) | Consolidated executable `1q -> 2q -> 3q -> 6q` ladder with the exact kernel/non-kernel boundary |
| Exact `q=3` master lock | [`scripts/w33_q3_master_lock_audit.py`](../scripts/w33_q3_master_lock_audit.py) | Consolidated executable `q=3` overdetermination audit across the local kernel, corrected spectral/Ihara layer, and continuum coefficient seed |
| Exact normalization bridge | [`scripts/w33_normalization_bridge_audit.py`](../scripts/w33_normalization_bridge_audit.py) | Consolidated executable bridge between the per-vertex `W(3,q)` adjacency moments and the April 2026 `q^4-1` lift normalization, proving that the apparent `M_2` uniqueness gap is exactly the zero-mode occupancy factor |
| Exact continuum coefficient seed | [`scripts/w33_toroidal_continuum_seed_audit.py`](../scripts/w33_toroidal_continuum_seed_audit.py) | Consolidated executable toroidal/decimal audit for the exact `8 / 56 / 320 / 2240 / 12480` packet behind the current continuum surface |
| W33-E8 boundary | [`scripts/w33_e8_correspondence_boundary_audit.py`](../scripts/w33_e8_correspondence_boundary_audit.py) | Conservative split between exact finite `W33 <-> E8` content and promoted phenomenology on the old correspondence theorem surface |
| Neutrino preset robustness | [`scripts/w33_neutrino_preset_audit.py`](../scripts/w33_neutrino_preset_audit.py) | Cross-preset audit showing that the `1/mu` branch remains the minimum-sum neutrino solution under both the legacy NuFIT 5.3 baseline and the current official NuFIT 6.0 fits |
| Electron-seed packet boundary | [`scripts/w33_electron_seed_packet_audit.py`](../scripts/w33_electron_seed_packet_audit.py) | Conservative audit showing that the residual charged-fermion wall has collapsed to the exact packet `98 x 17 x 208 = lambda*Phi6^2*(mu^2+1)*mu^2*Phi3`, with the last gap being physical identification of that packet |
| Flavor frontier boundary | [`scripts/w33_flavor_frontier_audit.py`](../scripts/w33_flavor_frontier_audit.py) | Conservative audit separating the exact `q=3` arithmetic selectors from the promoted `§83–§91` CKM/PMNS/running-alpha layer, and benchmarking the new formulas against the repo's stronger exact flavor bridges and current PDG/NuFIT data |
| Exact flavor spine | [`scripts/w33_exact_flavor_spine_bridge.py`](../scripts/w33_exact_flavor_spine_bridge.py) | Canonical exact flavor statement: local action-backbone generator `tan(theta_C)=3/13`, global CKM observable `lambda=9/40=q^2/v`, exact Levi Wolfenstein closure, and exact incidence-geometry PMNS packet `4/13, 7/13, 2/91` |
| Standard Model TQC boundary | [`scripts/w33_standard_model_tqc_boundary_audit.py`](../scripts/w33_standard_model_tqc_boundary_audit.py) | Conservative computational reading of the exact Standard Model spine: exact qutrit Clifford/stabilizer backbone, exact tetra-qutrit control/transport primitive, and an honest boundary before any full braiding-universal topological quantum computer claim |
| Standard Model magic packet | [`scripts/w33_standard_model_magic_packet_audit.py`](../scripts/w33_standard_model_magic_packet_audit.py) | Sharper universality scaffold: exact qutrit Clifford processor, exact tetrahedral control/transport bus, exact qutrit generation memory, and a minimal two-slot quartic magic candidate |
| Full manuscript reader | [docs/README_LIVING_PAPER_2026_02_11.md](./README_LIVING_PAPER_2026_02_11.md) | Preserved long-form narrative and theorem flow |
| Contributor | [CONTRIBUTING.md](../CONTRIBUTING.md) | Local workflow, tests, and contribution standards |
| Formalization contributor | [docs/index.html#hard-computation](./index.html#hard-computation) | Live proof-entry map; formal Lean path is not yet wired as a stable public entry point |

## Outreach & announcements

- Release announcement: [docs/outreach/pillar-45-qec.md](./outreach/pillar-45-qec.md) — Pillar‑45 (GF(3) QEC + MLUT) release and DOI

## Core Research Tracks

| Track | Key Docs | Main Scripts | Tests |
|---|---|---|---|
| W33 to E8 correspondence | `docs/NOVEL_CONNECTIONS_2026_02_10.md` | `scripts/w33_e8_correspondence_theorem.py`, `scripts/w33_homology.py`, `scripts/w33_hodge.py` | `tests/test_e8_embedding.py`, `tests/test_w33_hodge.py` |
| Heisenberg/qutrit structure | `reports/auto_ingest/W33_Heisenberg_action_bundle_20260209_v1_analysis_report.md` | `scripts/w33_heisenberg_qutrit.py` | `tests/test_heisenberg_qutrit_structure.py` |
| E6/F3 trilinear and reduced-orbit theorems | `docs/REDUCED_ORBIT_THEOREM_2026_02_10.md`, `docs/REDUCED_ORBIT_FORMAL_PROOF_2026_02_11.md` | `tools/build_e6_f3_trilinear_map.py`, `tools/analyze_e6_f3_trilinear_symmetry_breaking.py`, `tools/check_min_cert_orbit_involution_rule.py`, `tools/prove_z22_no_global_stabilizer.py` | `tests/test_e6_f3_trilinear.py`, `tests/test_check_min_cert_orbit_involution_rule_smoke.py`, `tests/test_prove_z22_no_global_stabilizer_smoke.py` |
| Orbit-stabilizer bridge on exact min-cert reps | `docs/ORBIT_STABILIZER_BRIDGE_2026_02_11.md` | `tools/analyze_orbit_stabilizer_bridge.py` | `tests/test_analyze_orbit_stabilizer_bridge_smoke.py` |
| GL(2,3) involution group/graph bridge | `docs/GL2_F3_INVOLUTION_CONJUGACY_2026_02_11.md` | `tools/analyze_gl2_f3_involution_conjugacy.py` | `tests/test_analyze_gl2_f3_involution_conjugacy_smoke.py` |
| AGL(2,3) det=2 involution class and D12 centralizer | `docs/AGL23_DET2_INVOLUTION_CLASS_2026_02_11.md` | `tools/analyze_agl23_det2_involution_class.py` | `tests/test_analyze_agl23_det2_involution_class_smoke.py` |
| W33 neighbor action realizes AGL(2,3) (51840 -> 432 with Z3 kernel) | `docs/W33_NEIGHBOR_ACTION_AGL23_2026_02_11.md` | `tools/analyze_w33_neighbor_action_agl23.py` | `tests/test_analyze_w33_neighbor_action_agl23_smoke.py` |
| Reduced-orbit stabilizer census (55 reduced Hessian reps) | `docs/REDUCED_REP_STABILIZER_CENSUS_2026_02_11.md` | `tools/analyze_reduced_rep_stabilizer_census.py` | `tests/test_analyze_reduced_rep_stabilizer_census_smoke.py` |
| Reduced-orbit stabilizer outliers (non-identity z-map cases) | `docs/REDUCED_REP_STABILIZER_OUTLIERS_2026_02_11.md` | `tools/analyze_reduced_rep_stabilizer_outliers.py` | `tests/test_analyze_reduced_rep_stabilizer_outliers_smoke.py` |
| s12 universalization and pattern analysis | `docs/S12_UNIVERSALIZATION_2026_02_11.md`, `docs/S12_JACOBI_FAILURE_PATTERN_2026_02_11.md`, `docs/S12_SL27_Z3_BRIDGE_2026_02_11.md` | `tools/universalize_s12_algebra.py`, `tools/analyze_s12_jacobi_failure_pattern.py`, `tools/analyze_s12_sl27_z3_bridge.py` | `tests/test_universalize_s12_algebra_smoke.py`, `tests/test_analyze_s12_jacobi_failure_pattern_smoke.py`, `tests/test_analyze_s12_sl27_z3_bridge_smoke.py` |
| Vogel scans, arithmetic checks, and resonance bridge | `docs/VOGEL_UNIVERSAL_RESEARCH_2026_02_11.md`, `docs/VOGEL_RATIONAL_DIMENSION_THEOREM_2026_02_11.md`, `docs/VOGEL_RATIONAL_HIT_CROSSWALK_2026_02_11.md`, `docs/VOGEL_INTEGER_M_LOCUS_2026_02_11.md`, `docs/VOGEL_RESONANCE_BRIDGE_2026_02_11.md` | `tools/vogel_universal_snapshot.py`, `tools/vogel_rational_dimension_theorem.py`, `tools/vogel_rational_hit_crosswalk.py`, `tools/vogel_integer_m_locus.py`, `tools/analyze_vogel_resonance_bridge.py` | `tests/test_vogel_universal_snapshot_smoke.py`, `tests/test_vogel_rational_dimension_theorem_smoke.py`, `tests/test_vogel_rational_hit_crosswalk_smoke.py`, `tests/test_vogel_integer_m_locus_smoke.py`, `tests/test_analyze_vogel_resonance_bridge_smoke.py` |

## High-Signal Status and Standards

- Canonical naming and counts: [STANDARDIZATION.md](../STANDARDIZATION.md)
- Current status and open gaps: [docs/index.html#current-synthesis](./index.html#current-synthesis), [docs/repo_frontier_audit.html](./repo_frontier_audit.html), [docs/march_2026_frontier_note.md](./march_2026_frontier_note.md), [docs/STATUS_AND_GAPS.md](./STATUS_AND_GAPS.md) (conservative baseline)
- Online-source separation log: [docs/README_EXTENSION_ONLINE_FINDINGS_2026_02_10.md](./README_EXTENSION_ONLINE_FINDINGS_2026_02_10.md)
- CI workflows: [`.github/workflows/`](../.github/workflows/)

## Common Commands

```bash
python scripts/w33_e8_correspondence_theorem.py
python scripts/w33_heisenberg_qutrit.py
python tools/prove_z22_no_global_stabilizer.py
python tools/vogel_universal_snapshot.py
python tools/analyze_vogel_resonance_bridge.py
python tools/analyze_gl2_f3_involution_conjugacy.py
python tools/analyze_agl23_det2_involution_class.py
python tools/analyze_w33_neighbor_action_agl23.py
python tools/analyze_orbit_stabilizer_bridge.py
python tools/analyze_reduced_rep_stabilizer_census.py
python tools/analyze_reduced_rep_stabilizer_outliers.py
python -m pytest -q
```

## Notes

- "Verified" claims are computational theorems within this repository's model and code paths.
- GitHub browser branding assets are in [docs/assets/](./assets/), including [docs/assets/w33-social-preview.png](./assets/w33-social-preview.png).
