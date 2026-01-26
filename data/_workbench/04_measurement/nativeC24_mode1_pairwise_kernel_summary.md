# Pairwise kernel fit to mode1 weights (native C24 delta stability)

Inputs:
- `data/_workbench/04_measurement/nativeC24_delta_mode_line_weights.csv`
- `data/_toe/coupling_20260110/W33_lines_to_projective_quartets.csv`
- `data/_n12/n12_58_orbit_cup_analysis.json`

- lines_used: 40

Best fit (by training R2):
- normalize_pairs: False
- ridge_alpha: 0.0
- r2: 0.871
- intercept: 0.037733
- corr_with_cup_matrix (natural order): 0.144

Top |kernel| weights (abs):
- sec0_m0 sec2_m1: -0.1711
- sec1_m1 sec3_m1: 0.1521
- sec1_m2 sec3_m1: -0.1345
- sec1_m0 sec3_m2: -0.1238
- sec1_m2 sec3_m2: 0.1163
- sec0_m0 sec2_m2: 0.0931
- sec0_m1 sec2_m2: -0.0861
- sec1_m0 sec3_m0: 0.0860
- sec0_m2 sec3_m1: 0.0831
- sec0_m2 sec2_m0: -0.0821
- sec0_m2 sec3_m2: -0.0815
- sec1_m1 sec3_m0: -0.0813
