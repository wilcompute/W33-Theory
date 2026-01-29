PR Draft: photonic/threshold-sweeps

Title: Add GBS threshold-sweep scripts, notebook updates, and initial outputs

Summary:
- Adds multiple threshold-sweep scripts for GBS threshold detector analysis (quick, minimal, extended, adaptive, high-precision).
- Adds notebook `notebooks/quantum_photonics/gbs_benchmark_full.ipynb` with integrated result display cells.
- Adds initial run outputs (JSON, PNG, PDF) under `bundles/v23_toe_finish/v23/` for reproducible figures and diagnostics.
- Adds tests for quantum photonics utilities and documentation files `docs/QUANTUM_PHOTONICS_README.md` and `docs/QUANTUM_PHOTONICS_NEXT_STEPS.md`.

Notes:
- Attempted to push branch `photonic/threshold-sweeps` but Git push failed due to SSH permission issue (git@github.com: Permission denied (publickey)).
- To finalize the PR, either configure SSH keys or push via HTTPS and then open a PR on GitHub. Suggested commands:
  - git push -u origin photonic/threshold-sweeps
  - gh pr create --title "Add GBS threshold-sweep scripts" --body "See PR_DRAFT_photonic_threshold_sweeps.md" --base main

Related work & TDA methods (added):
- We add an optional Topological Data Analysis (TDA) pathway to the notebook to capture multi-scale geometric signatures in GBS sample spaces. Key references:
  - Nicolau, Levine & Carlsson, *Science* 2011 (Mapper in genomics)
  - Rabadan & Blumberg, *Topological Data Analysis for Genomics and Evolution* (overview)
  - Emmett et al., *Parametric inference using persistence diagrams* (population genetics case study, arXiv:1406.4582)
  - Lesnick, Rabadán & Rosenbloom (topological approaches to reticulate evolution, arXiv:1804.01398)
  - Benjamin et al., *Multiscale topology for spatial transcriptomics* (arXiv:2212.06505)
- Tooling: `ripser`, `persim`/`ripser.py`, `giotto-tda` are recommended and added to `requirements.txt` as optional dependencies for running the TDA prototype.
- Reproducibility note: A short TDA prototype cell computes persistence diagrams and Betti curves from the GBS photon-count point clouds and compares Wasserstein/bottleneck distances to Jensen–Shannon divergence across (modes, η). See `notebooks/quantum_photonics/gbs_benchmark_full.ipynb` for usage and examples.

Files of interest (partial list):
- scripts/quantum_photonics/run_gbs_threshold_sweep_quick.py
- scripts/quantum_photonics/run_gbs_threshold_sweep_minimal.py
- scripts/quantum_photonics/run_gbs_threshold_sweep_ext.py
- scripts/quantum_photonics/run_gbs_threshold_sweep_highshots.py
- scripts/quantum_photonics/run_gbs_threshold_sweep_highprec_adaptive.py
- notebooks/quantum_photonics/gbs_benchmark_full.ipynb
- bundles/v23_toe_finish/v23/gbs_threshold_js_vs_eta.png
- bundles/v23_toe_finish/v23/gbs_threshold_sweep_quick.json
- bundles/v23_toe_finish/v23/gbs_threshold_summary_adaptive.pdf

Recommended next steps for reviewer:
1. Pull branch and run the notebooks to verify outputs: `git checkout photonic/threshold-sweeps && jupyter nbconvert --to notebook --execute notebooks/quantum_photonics/gbs_benchmark_full.ipynb`.
2. Run high-precision scripts locally if resources permit (see `run_gbs_threshold_sweep_highshots.py`).
3. Check `bundles/v23_toe_finish/v23/` for produced JSON/PNG/PDF artifacts and review `docs/QUANTUM_PHOTONICS_README.md`.

TDA prototype (new):
- A small TDA prototype script `scripts/quantum_photonics/run_gbs_tda_proto.py` computes persistence diagrams for small-sample GBS runs and writes `bundles/v23_toe_finish/v23/gbs_threshold_tda_runtime.json`.
- To run locally: ensure TDA packages are available (e.g., `pip install ripser persim giotto-tda`) and run `python scripts/quantum_photonics/run_gbs_tda_proto.py`.
- The notebook `notebooks/quantum_photonics/gbs_benchmark_full.ipynb` contains a TDA section that demonstrates Betti curves and a Wasserstein vs JS comparison for small-sample runs.

If you want, I can try to push again if you enable SSH or provide instructions to use HTTPS.
