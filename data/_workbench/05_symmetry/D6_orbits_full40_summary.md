# D6 orbits vs flux (all 40 W33 lines)

Inputs:
- data/_toe/coupling_20260110/W33_lines_to_projective_quartets.csv
- data/_is/incidence_autgroup_20260110/automorphism_group_order12_point_maps.csv
- data/_toe/flux_response_rankings_20260110/line_flux_response_summary.csv
- data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv
- data/_toe/flux_response_law_20260110/response_law_regression_coeffs_all40.csv

Orbits found: 8
- Duplicate quartets: 4 quartet(s) map to multiple line_ids.
  - sec0_m0 sec0_m1 sec0_m2 -> [9, 24, 31]
  - sec1_m0 sec1_m1 sec1_m2 -> [27, 29, 33]
  - sec2_m0 sec2_m1 sec2_m2 -> [12, 25, 38]
  - sec3_m0 sec3_m1 sec3_m2 -> [0, 34, 37]

Orbit summaries:
- orbit 0: size_lines=3, size_quartets=1, rank_range=32..35, mean_abs_delta=[0.001350, 0.001584, 0.001987], line_types={'monochrome12': 3}, var_q_classes={'low(1/9)': 2, 'mid(1/3)': 1}, stabilizer_auto_ids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
- orbit 1: size_lines=12, size_quartets=12, rank_range=2..33, mean_abs_delta=[0.001609, 0.006051, 0.023528], line_types={'other': 8, 'rank_spread': 4}, var_q_classes={'mid(1/3)': 4, 'low(1/9)': 8}, stabilizer_auto_ids=[0]
- orbit 2: size_lines=6, size_quartets=6, rank_range=6..27, mean_abs_delta=[0.003201, 0.010435, 0.012528], line_types={'other': 4, 'rank_spread': 2}, var_q_classes={'low(1/9)': 4, 'mid(1/3)': 2}, stabilizer_auto_ids=[0, 5]
- orbit 3: size_lines=6, size_quartets=6, rank_range=1..40, mean_abs_delta=[0.000343, 0.002076, 0.028922], line_types={'rank_spread': 2, 'other': 4}, var_q_classes={'low(1/9)': 3, 'high(1)': 1, 'mid(1/3)': 2}, stabilizer_auto_ids=[0, 9]
- orbit 4: size_lines=3, size_quartets=1, rank_range=13..39, mean_abs_delta=[0.000371, 0.005802, 0.010320], line_types={'monochrome12': 3}, var_q_classes={'low(1/9)': 2, 'mid(1/3)': 1}, stabilizer_auto_ids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
- orbit 5: size_lines=1, size_quartets=1, rank_range=37..37, mean_abs_delta=[0.000868, 0.000868, 0.000868], line_types={'rank_spread': 1}, var_q_classes={'low(1/9)': 1}, stabilizer_auto_ids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
- orbit 6: size_lines=6, size_quartets=2, rank_range=11..31, mean_abs_delta=[0.002344, 0.004392, 0.010587], line_types={'monochrome12': 6}, var_q_classes={'low(1/9)': 4, 'mid(1/3)': 2}, stabilizer_auto_ids=[0, 1, 2, 6, 7, 8]
- orbit 7: size_lines=3, size_quartets=3, rank_range=9..26, mean_abs_delta=[0.003302, 0.003459, 0.010940], line_types={'other': 2, 'rank_spread': 1}, var_q_classes={'low(1/9)': 3}, stabilizer_auto_ids=[0, 5, 6, 11]

Top 5 most flux-sensitive lines (mean_abs_delta):
- line 8 orbit 3: mean_abs_delta=0.028922, rank=1, type=other, quartet=sec0_m2 sec1_m0 sec2_m0 sec3_m2
- line 19 orbit 1: mean_abs_delta=0.023528, rank=2, type=rank_spread, quartet=sec0_m1 sec1_m2 sec2_m2 sec3_m2
- line 39 orbit 3: mean_abs_delta=0.019453, rank=3, type=other, quartet=sec0_m2 sec1_m2 sec2_m2 sec3_m1
- line 35 orbit 1: mean_abs_delta=0.015444, rank=4, type=other, quartet=sec0_m1 sec1_m2 sec2_m0 sec3_m1
- line 26 orbit 1: mean_abs_delta=0.012539, rank=5, type=rank_spread, quartet=sec0_m1 sec1_m1 sec2_m2 sec3_m0

Bottom 5 least flux-sensitive lines (mean_abs_delta):
- line 20 orbit 3: mean_abs_delta=0.000343, rank=40, type=other, quartet=sec0_m2 sec1_m1 sec2_m2 sec3_m2
- line 31 orbit 4: mean_abs_delta=0.000371, rank=39, type=monochrome12, quartet=sec0_m0 sec0_m1 sec0_m2
- line 28 orbit 3: mean_abs_delta=0.000448, rank=38, type=other, quartet=sec0_m2 sec1_m2 sec2_m0 sec3_m0
- line 10 orbit 5: mean_abs_delta=0.000868, rank=37, type=rank_spread, quartet=sec0_m0 sec0_m1 sec0_m2 sec1_m0 sec1_m1 sec1_m2 sec2_m0 sec2_m1 sec2_m2 sec3_m0 sec3_m1 sec3_m2
- line 17 orbit 3: mean_abs_delta=0.001289, rank=36, type=rank_spread, quartet=sec0_m2 sec1_m0 sec2_m1 sec3_m1
