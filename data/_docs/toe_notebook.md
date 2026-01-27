# Exploratory notebook & figures

- Notebook: `notebooks/toe_exploration.ipynb` — contains example analyses and a section that loads `data/_docs/toe_key_lines.csv` and saves figures to `data/_docs/figures/`.
- Figures generated:
  - `data/_docs/figures/prior_vs_native_scatter.png`
  - `data/_docs/figures/k12_entropy_hist.png`
  - (others may be present in `data/_docs/figures/`)

How to run locally:

1. Ensure Python 3.11+ is installed and `pip install --user pandas matplotlib seaborn` is available.
2. Run `python scripts/generate_toe_key_lines.py` to create `data/_docs/toe_key_lines.csv`.
3. Run `python scripts/visualize_toe_key_lines.py` to produce figures.
4. Open `notebooks/toe_exploration.ipynb` in Jupyter to interactively explore.
