# CKM Analysis Summary

This short report records the most recent pipeline runs and numeric summaries.

- H1 decomposition: regenerated (`tools/cycle_space_decompose.py`) and `data/h1_subspaces.json` is present.
- CKM overlaps: computed with `scripts/ckm_from_grams.py` → `data/ckm_from_grams.json`.
- Comparison to experimental CKM: `scripts/ckm_compare.py` → `data/ckm_comparison.json`.
  - Frobenius norm of (overlap - experimental): ~1.770523
  - Max abs diff: ~0.940155

- Unitary reconstruction sampling: `scripts/ckm_unitary_reconstruct.py` and `scripts/ckm_sample_stats.py` → `data/ckm_sample_stats.json`.
  - Sample size: 50 non-commuting pairs
  - Unitarity error mean: ~1.6649 (std ~0.0265)
  - Jarlskog mean: ~3.44e-05 (std ~1.24e-04)

- Phase reconstruction:
  - Reconstructed a candidate unitary via alternating projections (`scripts/ckm_phase_reconstruction.py`).
  - Results (`data/ckm_phase_reconstruction.json`):
    - Unitarity error: ~1.20e-15 (numerically unitary)
    - Jarlskog: ~0.04033
    - Frobenius norm |V|^2 - overlap: ~0.2815

- Scaled-phase reconstruction:
  - Reconstructed a unitary matching the fitted scaled magnitudes (`scripts/ckm_scaled_phase_reconstruction.py`).
  - Results (`data/ckm_scaled_phase_reconstruction.json`):
    - Unitarity error: ~8.43e-16
    - Jarlskog: ~1.28e-07
    - Frobenius norm |V|^2 - scaled_matrix: ~0.91593

Next suggested steps:
- Compute a normalized mapping to experimental CKM (fit column/row scalings).
- Integrate Koide/mass-fit heuristics from `tools/CKM_MATRIX.py` with the overlap statistics.
- Produce plots of Jarlskog and unitarity error distributions (notebooks or scripts).

Files produced:
- [data/ckm_from_grams.json](data/ckm_from_grams.json)
- [data/ckm_comparison.json](data/ckm_comparison.json)
- [data/ckm_sample_stats.json](data/ckm_sample_stats.json)
