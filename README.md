# THEORY OF EVERYTHING — Executive README

This repository contains the W33 ↔ E8 research codebase, reproducible artifacts,
and the computational verification used in the companion writeups (Pillars,
manuscripts, and notebooks).

The canonical project summary is maintained in `COMPLETE_SUMMARY.md` (now used
as the repository README for the GitHub landing page).

---

Quick links (run locally):

- Run core verification smoke tests:
  `python -m pytest tests/test_e8_embedding.py -q`
- Reproduce mass‑synthesis pipeline:
  `python scripts/w33_mass_synthesis.py`
- Reproduce CKM/PMNS predictions + CP phase:
  `python scripts/w33_ckm_predictor.py`
- Reproduce spectral action checks:
  `python -m pytest tests/test_e8_embedding.py::TestSpectralAction -q`

---

See `COMPLETE_SUMMARY.md` for the human‑readable Theory summary and predictions.
The top‑level `README.md` now forwards readers there and highlights runnable
scripts and test commands for reproducibility.

If you want a different landing page (e.g. `W33_THEORY_DEFINITIVE_SUMMARY.md` or
GitHub Pages under `docs/`), tell me which file to use and I will update that
instead.
| Reproduce the `AGL(2,3)` det-`2` involution class | `docs/AGL23_DET2_INVOLUTION_CLASS_2026_02_11.md` | `python tools/analyze_agl23_det2_involution_class.py` | `python -m pytest tests/test_analyze_agl23_det2_involution_class_smoke.py -q` |
| Reproduce the W33 neighbor action realizing `AGL(2,3)` | `docs/W33_NEIGHBOR_ACTION_AGL23_2026_02_11.md` | `python tools/analyze_w33_neighbor_action_agl23.py` | `python -m pytest tests/test_analyze_w33_neighbor_action_agl23_smoke.py -q` |
| Reproduce the orbit-stabilizer bridge | `docs/ORBIT_STABILIZER_BRIDGE_2026_02_11.md` | `python tools/analyze_orbit_stabilizer_bridge.py` | `python -m pytest tests/test_analyze_orbit_stabilizer_bridge_smoke.py -q` |
| Reproduce reduced-orbit stabilizer census | `docs/REDUCED_REP_STABILIZER_CENSUS_2026_02_11.md` | `python tools/analyze_reduced_rep_stabilizer_census.py` | `python -m pytest tests/test_analyze_reduced_rep_stabilizer_census_smoke.py -q` |
| Inspect reduced-orbit stabilizer outliers (non-identity `z`) | `docs/REDUCED_REP_STABILIZER_OUTLIERS_2026_02_11.md` | `python tools/analyze_reduced_rep_stabilizer_outliers.py` | `python -m pytest tests/test_analyze_reduced_rep_stabilizer_outliers_smoke.py -q` |
| Inspect formalization progress in Lean 4 | `proofs/lean/README.md` | `cd proofs/lean && lake build` | CI: `.github/workflows/lean4.yml` |

## Quick Setup

```bash
python -m venv .venv
# PowerShell
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements-dev.txt
```

Run the short confidence check:

```bash
python scripts/w33_e8_correspondence_theorem.py
python -m pytest tests/test_e8_embedding.py tests/test_heisenberg_qutrit_structure.py -q
```

Run full regression:

```bash
python -m pytest -q
```

## Repository Layout

```text
.github/workflows/   CI, smoke checks, Sage and Lean pipelines
scripts/             Core reproducibility scripts tied to claims
tools/               Extended theorem tooling and artifact builders
tests/               Pytest suite and smoke checks
proofs/lean/         Lean 4 formalization skeleton and CI target
docs/                Paper sections, theorem notes, and status documents
artifacts/           Machine-generated outputs used by writeups
```

## Manuscript and Historical Material

The previous long-form root manuscript has been preserved at:

- `docs/README_LIVING_PAPER_2026_02_11.md`

Additional high-signal documents:

- `docs/NOVEL_CONNECTIONS_2026_02_10.md`
- `docs/REDUCED_ORBIT_THEOREM_2026_02_10.md`
- `docs/REDUCED_ORBIT_FORMAL_PROOF_2026_02_11.md`
- `docs/NONTRIVIAL_UNSAT_CORE_GEOMETRY_2026_02_11.md`
- `docs/NONTRIVIAL_CORE_RULEBOOK_2026_02_11.md`
- `docs/CORE_RULEBOOK_MIN_CERT_LINK_2026_02_11.md`
- `docs/CORE_MOTIF_ORBIT_POLARIZATION_2026_02_11.md`
- `docs/CORE_MOTIF_ENRICHMENT_STATS_2026_02_11.md`
- `docs/CORE_MOTIF_ANCHOR_CHANNELS_2026_02_11.md`
- `docs/GLOBAL_SIGN_RIGIDITY_DUAL_PROFILE_2026_02_11.md`
- `docs/MINIMAL_GLOBAL_IDENTITY_CERTIFICATES_2026_02_11.md`
- `docs/README_EXTENSION_ONLINE_FINDINGS_2026_02_10.md` (raw web-source log)
- `docs/S12_UNIVERSALIZATION_2026_02_11.md`
- `docs/S12_JACOBI_FAILURE_PATTERN_2026_02_11.md`
- `docs/S12_SL27_Z3_BRIDGE_2026_02_11.md`
- `docs/VOGEL_UNIVERSAL_RESEARCH_2026_02_11.md`
- `docs/VOGEL_RESONANCE_BRIDGE_2026_02_11.md`
- `docs/GL2_F3_INVOLUTION_CONJUGACY_2026_02_11.md`
- `docs/AGL23_DET2_INVOLUTION_CLASS_2026_02_11.md`
- `docs/W33_NEIGHBOR_ACTION_AGL23_2026_02_11.md`
- `docs/ORBIT_STABILIZER_BRIDGE_2026_02_11.md`
- `docs/REDUCED_REP_STABILIZER_CENSUS_2026_02_11.md`
- `docs/REDUCED_REP_STABILIZER_OUTLIERS_2026_02_11.md`

## Contribution Notes

- Use `CONTRIBUTING.md` for local workflow and pre-commit guidance.
- Keep claims executable: each theorem update should include script path, test path, and artifact path.
- Prefer adding new result documents under `docs/` and generated outputs under `artifacts/`.

## GitHub Repository Metadata

- About text and topics are tracked in `.github/settings.yml`.
- Social preview image asset: `docs/assets/w33-social-preview.png`.
- Upload path in GitHub UI: `Settings -> General -> Social preview -> Upload an image`.
