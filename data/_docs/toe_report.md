# TOE exploratory report

This short report highlights the notebook outputs and key figures generated from the TOE analyses.

## Figures

- **Prior vs native scatter** — `data/_docs/figures/prior_vs_native_scatter.png`

  Description: Scatter of `prior_score` vs `native_mean_abs_delta`, colored by `in_top_native` and sized by `node_commutator_score` when present. This helps evaluate whether prior/fit signals align with native sensitivity.

- **k12 entropy histogram** — `data/_docs/figures/k12_entropy_hist.png`

  Description: Distribution of `k12_entropy` across lines; useful to observe whether a subset of lines shows unusually low or high entropy, which can indicate structured projective behavior.

## Short interpretations

- The scatter plot reveals how prior signal strength and native sensitivity relate for the current dataset — use it to visually identify lines where signals disagree.
- The entropy histogram shows a spread of `k12_entropy` values; extreme tails are worth inspection for special structure.

## How to reproduce

1. `python scripts/generate_toe_key_lines.py` — writes `data/_docs/toe_key_lines.csv`.
2. `python scripts/visualize_toe_key_lines.py` — writes PNGs to `data/_docs/figures/`.
3. Open `notebooks/toe_exploration.ipynb` to interact and re-generate the figures.


---

If you want, I can expand this into a longer Markdown report that includes the mean_abs_delta by `unique_k_mod6` boxplot and short per-predictor evaluation sections. Tell me if you want that expanded and I’ll add it.
