# Line feature regression

Outputs:
- `data/_workbench/02_geometry/line_feature_regression.csv`

## Correlations with native mean_abs_delta
- var_q: -0.174938
- mean_q: -0.051822
- abs_mean_q: -0.110371
- unique_k_mod6: -0.039574
- unique_k_mod3: 0.068107
- canon_mean_abs_delta: 0.390912

## Sign/mean correlations
- mean_q_vs_native_mean_delta: -0.056046
- mean_q_vs_canon_mean_delta: 0.097706

## Linear regression (native_mean_abs_delta, raw)
- features: var_q, abs_mean_q, unique_k_mod6, unique_k_mod3, canon_mean_abs_delta
- R2: 0.184284
- coefficients (intercept + features):
  - intercept: 1.498858
  - var_q: -0.846567
  - abs_mean_q: -1587521876399.437256
  - unique_k_mod6: -0.161158
  - unique_k_mod3: 0.688506
  - canon_mean_abs_delta: 125.309763

## Linear regression (native_mean_abs_delta, standardized features)
- R2: 0.184284
- coefficients (intercept + z-scored features):
  - intercept: 3.058705
  - var_q: -0.138137
  - abs_mean_q: -0.202984
  - unique_k_mod6: -0.193924
  - unique_k_mod3: 0.383418
  - canon_mean_abs_delta: 0.806240
