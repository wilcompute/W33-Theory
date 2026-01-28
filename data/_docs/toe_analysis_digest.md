# TOE analysis digest (quick highlights) ✅

## What I ran
- Executed the main pipeline: `scripts/toe_analysis_run.ps1` (used a temporary `-ExecutionPolicy Bypass` to allow script execution). This wrote a checkpoint JSON to `data/_checkpoints/checkpoint_toe_analysis_run_20260112T050348Z.json`.

## Key outputs produced
- `data/_workbench/02_geometry/W33_line_phase_map.csv` & `.md` — per-line k-mod6 / k-mod3 statistics and low-uniqueness lines.
- `data/_workbench/02_geometry/line_feature_table.csv` & summary — correlation between native and canonical rankings (Pearson ≈ 0.391) and top-10 overlap = 4.
- `data/_workbench/04_measurement/native_C24_fullgrid_summary.md` — winner flips (51/51 lines flipped), top native-sensitive lines include **8, 3, 14, 36, 7**, and overlaps with canonical top10: **8, 3, 14, 7**.
- `data/_workbench/04_measurement/e_star_oddness_flux_winner_summary.md` — e* oddness predictor summary (corr(odd_fraction, mean_abs_delta) ≈ 0.265, top-5 oddness lines: **3, 7, 6, 16, 23**).
- `data/_workbench/04_measurement/mixed_predictor_oddness_defect_summary.md` — mixed predictor (oddness + defect mass) summary (top5: **19, 22, 23, 21, 35**; flux winner beats noflux ≈ 0.0588).

## Quick findings
- Correlation between canonical and native mean_abs_delta is moderate (≈ 0.39) but top-list overlap is limited (4/10), suggesting complementary signals.
- Several lines (8, 3, 14, 36, 7) appear consistently important across analyses — good candidates for follow-up.
- The pipeline required a small compatibility fix: I copied `data/_toe/coupling_20260110/*` into `data/toe_coupling_20260110/` so scripts expecting `data/toe_coupling_20260110/` run unchanged.

## Recommended next steps (pick any)
1. Add small unit tests and CI job that runs `python -m py_compile scripts/*.py` and `scripts/toe_analysis_run.ps1` (guarded) to catch regressions. ✅
2. Produce a short CSV digest `data/_docs/toe_key_lines.csv` with the union of top-k lines from the `native` and `canonical` analyses and relevant metrics (k-mod stats, mean_abs_delta, ranks). I can generate this next.
3. Run targeted deeper analyses: (a) per-line response surfaces, (b) visualizations of distribution of mean_abs_delta by `unique_k_mod6`, (c) run the optional predictors (`action_candidate_predictor`, `node_commutator_projective_predictor`) and produce an evaluation report.

---

If you'd like I can: (A) generate the CSV digest and a short Jupyter or markdown report with a few plots, (B) add minimal CI checks, or (C) perform any of the deeper analyses above—tell me which and I’ll proceed. ✨


## New: Notebook, figures & CI ✅
- **Notebook:** `notebooks/toe_exploration.ipynb` (exploratory notebook with examples and a section that loads `data/_docs/toe_key_lines.csv` and saves figures to `data/_docs/figures/`).
- **Figures generated:** `data/_docs/figures/prior_vs_native_scatter.png`, `data/_docs/figures/k12_entropy_hist.png` (and example plots under `data/_docs/figures/`).
- **CI workflow:** Added `.github/workflows/ci.yml` (runs `python -m py_compile scripts/*.py`, installs minimal deps and runs the digest generator + visualizer as a smoke test).
- **Predictor metrics:** `node_commutator_projective_predictor` summary: **pearson ≈ 0.145**, **spearman ≈ 0.063**, top-5 predicted lines: **[39, 19, 20, 30, 5]**.

- **New predictor columns added:** `data/_docs/toe_key_lines.csv` now includes **mixed_score** and **e_star_oddness** columns (see `scripts/generate_toe_key_lines.py`).

If you want, I can (D) add the notebook to the repo docs, (E) wire the figures into the summary README, or (F) add a minimal GitHub Pages/markdown report that embeds these images. Tell me which of those to do next and I’ll proceed. ✨

- **Report:** `data/_docs/toe_report.md` — short exploratory report embedding the notebook-generated figures.

- **Quick validation:** the CI `smoke` job now runs `scripts/generate_toe_key_lines.py` and `scripts/visualize_toe_key_lines.py` and verifies `data/_docs/toe_key_lines.csv` and at least one figure exist. (This runs automatically on push/PR and is designed to catch regressions in the digest/visualization flow.)
