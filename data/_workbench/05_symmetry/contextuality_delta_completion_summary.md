# Contextuality: delta homomorphism vs completion decoration

Inputs:
- /mnt/c/Users/wiljd/OneDrive/Documents/GitHub/Sage/data/_toe/flux_response_rankings_20260110/line_flux_response_summary.csv
- /mnt/c/Users/wiljd/OneDrive/Documents/GitHub/Sage/data/_is/incidence_autgroup_20260110/incidence_12points_15lines.csv
- /mnt/c/Users/wiljd/OneDrive/Documents/GitHub/Sage/data/_workbench/05_symmetry/D6_action_on_lines_with_completion_checks.csv

Delta-pair differences by automorphism:

|   auto_id |   delta |   pair_count |   mean_abs_diff |   median_abs_diff |   max_abs_diff |
|----------:|--------:|-------------:|----------------:|------------------:|---------------:|
|         0 |       0 |           15 |      0          |       0           |     0          |
|         1 |       0 |           15 |      0.00581021 |       0.00189579  |     0.0260587  |
|         2 |       0 |           15 |      0.00581021 |       0.00189579  |     0.0260587  |
|         9 |       0 |            9 |      0.00462335 |       0.00228975  |     0.0165889  |
|        10 |       0 |            9 |      0.00476247 |       0.000157269 |     0.0260587  |
|        11 |       0 |            9 |      0.00382652 |       0.000946193 |     0.00946978 |
|         3 |       1 |           15 |      0.00876419 |       0.00568653  |     0.0284748  |
|         4 |       1 |           15 |      0.00876419 |       0.00568653  |     0.0284748  |
|         5 |       1 |           12 |      0.00409664 |       0           |     0.0285798  |
|         6 |       1 |            8 |      0.00914781 |       0.0071509   |     0.0276336  |
|         7 |       1 |            8 |      0.00916746 |       0.0068596   |     0.0285798  |
|         8 |       1 |            8 |      0.00823228 |       0.00497614  |     0.0284748  |

Missing-sector stats (tomotope lines):

|   missing_sector |   count |        mean |      median |
|-----------------:|--------:|------------:|------------:|
|                0 |       6 | 0.0114899   | 0.00719953  |
|                1 |       3 | 0.0115104   | 0.0113717   |
|                2 |       3 | 0.00599666  | 0.00455138  |
|                3 |       3 | 0.000693093 | 0.000447663 |

Completion-class stats (tomotope lines):

| completion_class   |   count |        mean |      median |
|:-------------------|--------:|------------:|------------:|
| sec0_m2            |       6 | 0.0114899   | 0.00719953  |
| sec1_m0            |       1 | 0.0113717   | 0.0113717   |
| sec1_m1            |       1 | 0.0106319   | 0.0106319   |
| sec1_m2            |       1 | 0.0125277   | 0.0125277   |
| sec2_m0            |       1 | 0.00320069  | 0.00320069  |
| sec2_m1            |       1 | 0.0102379   | 0.0102379   |
| sec2_m2            |       1 | 0.00455138  | 0.00455138  |
| sec3_m0            |       1 | 0.000447663 | 0.000447663 |
| sec3_m1            |       1 | 0.00128891  | 0.00128891  |
| sec3_m2            |       1 | 0.000342712 | 0.000342712 |
