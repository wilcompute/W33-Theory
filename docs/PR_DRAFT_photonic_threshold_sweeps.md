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

If you want, I can try to push again if you enable SSH or provide instructions to use HTTPS.
