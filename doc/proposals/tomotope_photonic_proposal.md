# Tomotope → Photonic Experimental Signatures

**Project:** Tomotope/Finite Geometry ↔ Photonic Signatures

**Lead:** wilcompute (W33-Theory)
**Branch:** photonic/threshold-sweeps

## Abstract

This proposal aims to establish a reproducible pipeline connecting finite incidence geometries (tomotopes, Reye/finite configurations, Veldkamp structures) to experimentally-accessible photonic network signatures. We will map finite geometries to interferometer coupling designs, simulate Gaussian Boson Sampling (GBS) outputs, and quantify topological and distributional signatures (persistent homology H0/H1, Wasserstein distances, Jensen–Shannon divergence). The goal is to identify robust, statistically significant signatures that distinguish geometry-derived designs from null ensembles and to propose feasible small-scale photonic experiments to test finite-geometry TOE hypotheses.

---

## Hypothesis

Certain finite incidence geometries impose constraints on mode connectivity and symmetry that produce measurable differences in photonic output distributions. These differences manifest as (1) distinct persistent-homology summaries (H0/H1 features and Wasserstein distances) and (2) statistically significant JS divergence from null or randomly connected interferometers across loss/squeezing regimes.

---

## Methods

1. Geometry → Interferometer mapping
   - Represent finite incidence structures as adjacency/incidence matrices.
   - Convert adjacency to unitary proposals using spectral embedding + orthonormalization (e.g., via Householder reflections or beamsplitter parameterization), ensuring preservation of key automorphism symmetries when possible.
   - Produce small interferometer designs (6–8 modes) derived from candidate finite geometries.

2. Simulation pipeline
   - Use existing scripts (`scripts/quantum_photonics/run_gbs.py`, `run_gbs_tda_grid.py`, `run_gbs_tda_followup.py`) to sample outputs across eta and squeezing sweeps.
   - Compute distributional metrics (JS divergence vs theoretical threshold probabilities) and TDA metrics (ripser persistence diagrams for threshold patterns, Wasserstein distances between diagrams).
   - Implement bootstrap and permutation tests to estimate significance and control for chance correlations.

3. Robustness and noise modeling
   - Model loss, detector inefficiency, and dark counts; evaluate how signatures degrade with noise.
   - Test encoding variants (threshold vs exact photon-number patterning).

4. Experimental design guidance
   - Identify the minimal interferometer setting (modes ≤ 8) with robust signatures under realistic parameter regimes.
   - Provide parameter ranges (squeezing, loss budget) and measurement counts (shots) for feasible lab measurements.

---

## Statistical tests and success criteria

- Bootstrap JS CIs and permutation tests for Wasserstein distances to show separation between geometry-derived designs and nulls (p < 0.05).
- Minimum practical success: consistent detection of a signature (e.g., H1 count or JS > baseline) for at least one geometry across plausible noise levels.

---

## Deliverables & Timeline (8 weeks)

- Week 1–2: Mapping code, initial interferometer prototypes, small simulations (deliver: `notebooks/quantum_photonics/tomotope_mapping.ipynb`).
- Week 3–4: Full simulation grid (eta/squeezing), TDA analysis, bootstrap work (deliver: `bundles/v23_toe_finish/v23/gbs_threshold_tda_tomotope_grid.json` + plots).
- Week 5–6: Robustness analysis and candidate experimental designs (deliver: design document, parameter table, suggested hardware specs).
- Week 7–8: Write-up, PR with reproducible notebooks and results, suggested experimental protocol for collaborators.

---

## Resources & compute

- Use existing venv dependencies (Strawberry Fields, TheWalrus, ripser/persim).
- Adaptive-shot strategies for heavy hafnian sampling; keep initial search to modes ≤ 8 to remain tractable.
- Recommend at least one workstation with 16+ CPU cores and 32+ GB RAM for heavy sampling runs; cloud GPUs are not essential for current simulations (classical hafnian cost remains CPU-bound).

---

## Risks & mitigations

- Risk: Non-unique signatures across geometries.
  - Mitigation: Cross-validate using multiple metrics (JS, Wasserstein, Betti counts) and permutation tests.
- Risk: Sampling cost for high shots.
  - Mitigation: Use adaptive shots, importance sampling, and restrict initial experiments to low-mode prototypes.

---

## Next steps

1. Add the proposal to `doc/proposals/` and push to `photonic/threshold-sweeps` (this file).
2. Implement `notebooks/quantum_photonics/tomotope_mapping.ipynb` with mapping examples and a small simulation for one geometry.
3. Run grid and follow-up high‑precision runs against top candidate geometries.

---

*If you want, I can expand any section into a funding‑style one‑pager or generate a runnable checklist to start Week 1 work.*
