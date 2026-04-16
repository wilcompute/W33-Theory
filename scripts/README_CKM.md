CKM analysis scripts
--------------------

Quick helper scripts added to `scripts/`:

- `ckm_unitary_reconstruct.py` — reconstruct a 3×3 unitary from two Z3 eigenspaces and compute Jarlskog.
- `ckm_from_grams.py` — (existing) computes 3×3 overlaps from `data/h1_subspaces.json`.
- `ckm_compare.py` — compare computed overlap matrix to experimental CKM magnitudes.
- `ckm_sample_stats.py` — sample many non-commuting Z3 pairs and gather unitarity/Jarlskog stats.
- `ckm_fit_scalings.py` — fit diagonal positive scalings to map computed overlap → experimental magnitudes.
- `ckm_phase_reconstruction.py` — reconstruct unitary from raw overlap magnitudes.
- `ckm_scaled_phase_reconstruction.py` — reconstruct unitary matching the fitted scaled magnitudes.

Usage examples
--------------

Run the end-to-end pipeline:

```powershell
py -3 -X utf8 tools/cycle_space_decompose.py
py -3 -X utf8 scripts/ckm_from_grams.py
py -3 -X utf8 scripts/ckm_compare.py
py -3 -X utf8 scripts/ckm_fit_scalings.py
py -3 -X utf8 scripts/ckm_scaled_phase_reconstruction.py
```

Outputs are saved under `data/` and a short summary is in `reports/ckm_analysis.md`.
