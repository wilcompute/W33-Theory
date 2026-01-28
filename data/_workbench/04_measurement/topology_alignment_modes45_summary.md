# Topology alignment (modes 4–5)

Inputs:
- /mnt/c/Users/wiljd/OneDrive/Documents/GitHub/Sage/data/_toe/native_fullgrid_20260110/nativeC24_fullgrid_line_stabilities_flux_noflux.csv
- /mnt/c/Users/wiljd/OneDrive/Documents/GitHub/Sage/data/_toe/coupling_20260110/W33_lines_to_projective_quartets.csv
- /mnt/c/Users/wiljd/OneDrive/Documents/GitHub/Sage/data/_n12/n12_58_orbit_cup_analysis.json

|   mode_k |   pairwise_r2 |   best_corr_J |   best_corr_U | perm_J                    | perm_U                    |
|---------:|--------------:|--------------:|--------------:|:--------------------------|:--------------------------|
|        4 |      0.884157 |     -0.583667 |     -0.601038 | 5 6 10 0 8 11 3 2 4 1 9 7 | 11 1 5 3 7 8 4 2 0 9 6 10 |
|        5 |      0.927212 |      0.537763 |      0.514415 | 2 6 9 0 11 1 10 7 3 8 4 5 | 2 0 4 3 7 1 5 8 6 9 11 10 |

Baselines:

|   mode_k |   baseline_max_abs_corr_J |   baseline_max_abs_corr_U |
|---------:|--------------------------:|--------------------------:|
|        4 |                 -0.459112 |                 -0.457292 |
|        5 |                 -0.400679 |                  0.441231 |
