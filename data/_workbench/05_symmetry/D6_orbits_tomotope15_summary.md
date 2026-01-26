# D6 orbits vs flux (tomotope 15)

Inputs:
- data/_is/star_algebra_20260110/tomotope_15_rainbow_lines_phase_function_model.csv
- data/_is/incidence_autgroup_20260110/automorphism_group_order12_point_maps.csv
- data/_toe/flux_response_rankings_20260110/line_flux_response_summary.csv
- data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv
- data/_toe/flux_response_law_20260110/response_law_regression_coeffs_all40.csv

Orbit summaries (tomotope-local IDs):
- orbit 0 (full40_orbits=[2]): size=6, rank_range=6..27, mean_abs_delta_mean=0.008754, median=0.010435, missing_sector={1: 3, 2: 3}, var_q_class={'low(1/9)': 4, 'mid(1/3)': 2}
- orbit 1 (full40_orbits=[3]): size=6, rank_range=1..40, mean_abs_delta_mean=0.008886, median=0.002076, missing_sector={0: 3, 3: 3}, var_q_class={'low(1/9)': 3, 'high(1)': 1, 'mid(1/3)': 2}
- orbit 2 (full40_orbits=[7]): size=3, rank_range=9..26, mean_abs_delta_mean=0.005900, median=0.003459, missing_sector={0: 3}, var_q_class={'low(1/9)': 3}

Missing-sector split (mean_abs_delta):
- orbit 0, missing_sector 1: size=3, mean_abs_delta_mean=0.011510, median=0.011372, rank_range=6..10
- orbit 0, missing_sector 2: size=3, mean_abs_delta_mean=0.005997, median=0.004551, rank_range=14..27
- orbit 1, missing_sector 0: size=3, mean_abs_delta_mean=0.017080, median=0.019453, rank_range=1..29
- orbit 1, missing_sector 3: size=3, mean_abs_delta_mean=0.000693, median=0.000448, rank_range=36..40
- orbit 2, missing_sector 0: size=3, mean_abs_delta_mean=0.005900, median=0.003459, rank_range=9..26
