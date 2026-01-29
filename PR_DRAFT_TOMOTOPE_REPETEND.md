Title: Tomotope ↔ Repetend Analysis — numerics, TDA, and enrichment tests

Summary
-------
This PR adds an exploratory numeric analysis linking decimal repetend patterns (denominators up to 10k) with Tomotope-related invariants and residue classes. It includes:

- A full repetend scan script and outputs (`scripts/number_theory/run_repetend_scan.py`, `data/repetend_scan/`) which computes repetend lengths, full repetend flags, and saves CSV/JSON and plots.
- Enrichment analyses (`scripts/number_theory/repetend_enrichment_sweep.py`) testing properties (full_repetend, eq6, div6, div12, div24, div192) against residues mod12/mod24; CSVs and heatmaps saved in `data/repetend_scan/`.
- Multivariate logistic regression script integrated in the notebook that fits models of properties on `mod12` indicators and saves coefficient CSVs and JSON model summaries.
- A notebook `notebooks/number_theory/repetend_tomotope_analysis.ipynb` which reproduces the main figures and model outputs and provides short conclusions.

Key findings (short)
-------------------
- Residue classes mod12 are non-uniform with respect to full repetends and divisibility-by-12 (residues 4 and 8 show enrichment in univariate tests).  
- Logistic regression (mod12 categorical control) identifies which residues contribute most to the association; model summaries and coefficient CSVs are saved for inspection.

Files to review
---------------
- `data/repetend_scan/repetend_scan_10000.csv`  
- `data/repetend_scan/repetend_summary_10000.json`  
- `data/repetend_scan/repetend_hist_10000.png`  
- `data/repetend_scan/enrichment_pval_heatmap_mod12_10000.png`  
- `data/repetend_scan/fraction_div12_by_mod12_10000.png`  
- `data/repetend_scan/logistic_models_10000.json`  
- `notebooks/number_theory/repetend_tomotope_analysis.ipynb`

Suggested PR description
------------------------
This PR adds a reproducible numeric pipeline exploring patterns in decimal repetends and their statistical associations with residue classes; integrates Tomotope generator summary as contextual metadata; adds notebook and figures for review. The work is exploratory; the statistical associations are hypothesis-generating rather than conclusive. Please review the notebook and the saved CSVs and advise which results you want included in the main paper or follow-up analyses.

Next steps I can do autonomously (pick up to 3):
- Expand logistic models to include mod24 interactions and totient-based covariates.  
- Run the same analyses for denominators up to 100k (compute-intensive; will run overnight).  
- Prepare PR-ready figures and a concise one‑page supplement explaining methods and findings.

If you want, I can open a draft PR for you and attach the key figures and JSON outputs.