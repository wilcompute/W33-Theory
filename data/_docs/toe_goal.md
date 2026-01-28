# TOE Project Goal & Success Criteria

## Objective
Predict and explain per-line sensitivity (`native_mean_abs_delta`) and identify robust predictor signals that generalize beyond the current dataset and are reproducible.

## Scope
- Primary target: `native_mean_abs_delta` (per-line scalar)
- Candidate predictors: `prior_score`, `fit_score`, `node_commutator_score`, `mixed_score`, `e_star_oddness`, and other derived features in `data/_workbench/*`
- Deliverables: reproducible scripts that generate `data/_docs/toe_key_lines.csv`, figures (`data/_docs/figures/*`), predictor evaluations (`data/_docs/predictor_evaluation.csv`/`.md`), and modeling results (`data/_docs/modeling_results.csv`/`.md`)

## Quantitative success criteria (initial proposal)
- Statistical evidence: a predictor is considered *statistically supported* if permutation-based p-value < 0.05 after Benjamini–Hochberg FDR correction across tested predictors.
- Effect-size threshold: absolute Pearson or Spearman correlation >= 0.20 is considered a practically meaningful signal (tunable).
- Predictive baseline: a predictive model should show cross-validated R^2 at least 0.05 greater than a permuted-feature null-model (or CV R^2 > 0.10 as an absolute baseline).
- Stability: predictor importance or rank should be stable across bootstrap resamples (median Spearman rank correlation among resamples > 0.6).
- Robustness: results should persist under reasonable preprocessing choices (e.g., winsorization, small feature subsetting).

> These thresholds are conservative starting points and should be reviewed; they are intentionally modest given small sample sizes and domain uncertainty.

## Reproducibility checklist
- Use deterministic seeds for permutations and bootstraps and record them in outputs.
- Provide a pinned environment (`requirements.txt` or `environment.yml`) and `ENV.md` describing optional Sage/PySymmetry setup.
- Add a small deterministic fixture dataset and an end-to-end smoke test in CI that reproduces the basic pipeline.
- Place generated artifacts under `data/_docs/` and write short `*.md` digests explaining how they were produced.

## Evaluation steps (run order)
1. `python scripts/generate_toe_key_lines.py` → produces `data/_docs/toe_key_lines.csv`
2. `python scripts/visualize_toe_key_lines.py` → writes `data/_docs/figures/` PNGs and a small summary CSV
3. `python scripts/eval_predictors.py` (or `eval_predictors_expanded.py`) → permutation tests, FDR, bootstrap CIs → produces `predictor_evaluation.csv`/`.md`
4. `python scripts/modeling/run_models.py` → cross-validated models + permuted nulls → `modeling_results.csv` and notebook summaries
5. Collate figures and write `data/_docs/toe_final_report.md`

## Commands (developer quick-run)
- Run the minimal end-to-end (fast):
  - python scripts/generate_toe_key_lines.py
  - python scripts/visualize_toe_key_lines.py
  - python scripts/eval_predictors.py --permutations 200 --seed 1

- Full reproducible run (after env pinned & optional Sage available):
  - python -m pip install -r requirements.txt  # or micromamba env
  - python scripts/eval_predictors.py --permutations 2000 --seed 42
  - python scripts/modeling/run_models.py --cv 5 --seed 42

## Acceptance criteria for Task 1
- `data/_docs/toe_goal.md` exists in the repo and is reviewed/approved.
- Metrics and reproducibility checklist are clear enough to guide Task 2 (fixtures) and Task 3 (expanded evaluation).

---

**Next step:** create a small deterministic fixture dataset under `data/_workbench/00_meta/fixtures/` and add the CI smoke/fixture loader. (Task 2)
