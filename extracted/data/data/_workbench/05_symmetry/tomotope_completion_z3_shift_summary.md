# Tomotope completion vs Z3-shifted flux predictions

Inputs:
- `data/_is/star_algebra_20260110/tomotope_15_rainbow_lines_phase_function_model.csv`
- `data/_workbench/05_symmetry/transport_projective_z3_w33_line_shifted_quartets.csv`
- `data/_toe/flux_response_rankings_20260110/line_flux_response_summary.csv`

- tomotope lines: 15

By missing_sector (mean over lines):
- missing_sector=0: n=6, sum1_mean_abs_delta=0.011490 if sum1 else na, sum2_pred_mean_abs_delta=0.006527, sum0_pred_mean_abs_delta=0.009573
- missing_sector=1: n=3, sum1_mean_abs_delta=0.011510 if sum1 else na, sum2_pred_mean_abs_delta=0.013509, sum0_pred_mean_abs_delta=0.005355
- missing_sector=2: n=3, sum1_mean_abs_delta=0.005997 if sum1 else na, sum2_pred_mean_abs_delta=0.007396, sum0_pred_mean_abs_delta=0.005667
- missing_sector=3: n=3, sum1_mean_abs_delta=0.000693 if sum1 else na, sum2_pred_mean_abs_delta=0.011717, sum0_pred_mean_abs_delta=0.006814
