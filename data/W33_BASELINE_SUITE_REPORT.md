# W33 Baseline Audit Suite Report

Generated: 2026-01-13T23:26:17Z

This summarizes hit-rates for low-complexity expression search against a few physics targets.
It is intended as a *multiple-comparisons sanity check*: if a target has many close hits in a broad grammar, then post-hoc ‘beautiful’ formulas are less evidential.

## Mode: strict

Config:

- base_count: 17
- unary_ops: sqrt, inv
- binary_ops: +, -, *, /
- max_depth: 4
- max_pool: 250000
- num_exprs_scored: 250000

Best matches (per target):

| target | best % error | complexity | expr | value |
|---|---:|---:|---|---:|
| alpha | 0.077917% | 5 | ((7 / 40) / 24) | 0.00729166666666667 |
| higgs_over_z | 0.001091% | 7 | ((5280 / 6048) / (7 / 11)) | 1.3718820861678 |
| omega_lambda | 0.001613% | 5 | ((40 + 22) / 90) | 0.688888888888889 |
| cabibbo_deg | 0.002435% | 7 | ((240 / 6048) + (2 + 11)) | 13.0396825396825 |

Hit rates by tolerance (hits within tolerance / expressions scored):

| target | ≤0.1% | ≤0.5% | ≤1.0% | ≤5.0% | ≤10.0% |
|---|---:|---:|---:|---:|---:|
| alpha | 1/250000 (4e-06) | 19/250000 (7.6e-05) | 44/250000 (0.000176) | 354/250000 (0.001416) | 639/250000 (0.002556) |
| higgs_over_z | 9/250000 (3.6e-05) | 42/250000 (0.000168) | 85/250000 (0.00034) | 486/250000 (0.001944) | 899/250000 (0.003596) |
| omega_lambda | 3/250000 (1.2e-05) | 31/250000 (0.000124) | 65/250000 (0.00026) | 341/250000 (0.001364) | 668/250000 (0.002672) |
| cabibbo_deg | 16/250000 (6.4e-05) | 68/250000 (0.000272) | 130/250000 (0.00052) | 668/250000 (0.002672) | 1154/250000 (0.004616) |

Approx. (naïve) probability of ≥1 hit at ≤0.1% among the 4 targets:

- ~0.000115996 (treating per-target events as independent)

## Mode: medium

Config:

- base_count: 20
- unary_ops: sqrt, inv
- binary_ops: +, -, *, /
- max_depth: 4
- max_pool: 250000
- num_exprs_scored: 250000

Best matches (per target):

| target | best % error | complexity | expr | value |
|---|---:|---:|---|---:|
| alpha | 0.025252% | 8 | ((40 / 6048) * (3 / e)) | 0.00729919526133814 |
| higgs_over_z | 0.005020% | 6 | ((11 + e) / 10) | 1.3718281828459 |
| omega_lambda | 0.001613% | 5 | ((40 + 22) / 90) | 0.688888888888889 |
| cabibbo_deg | 0.004388% | 7 | (sqrt(24) + (5 + pi)) | 13.0405721391561 |

Hit rates by tolerance (hits within tolerance / expressions scored):

| target | ≤0.1% | ≤0.5% | ≤1.0% | ≤5.0% | ≤10.0% |
|---|---:|---:|---:|---:|---:|
| alpha | 8/250000 (3.2e-05) | 52/250000 (0.000208) | 92/250000 (0.000368) | 612/250000 (0.002448) | 1043/250000 (0.004172) |
| higgs_over_z | 20/250000 (8e-05) | 76/250000 (0.000304) | 152/250000 (0.000608) | 817/250000 (0.003268) | 1610/250000 (0.00644) |
| omega_lambda | 9/250000 (3.6e-05) | 61/250000 (0.000244) | 124/250000 (0.000496) | 624/250000 (0.002496) | 1217/250000 (0.004868) |
| cabibbo_deg | 33/250000 (0.000132) | 146/250000 (0.000584) | 290/250000 (0.00116) | 1489/250000 (0.005956) | 2702/250000 (0.010808) |

Approx. (naïve) probability of ≥1 hit at ≤0.1% among the 4 targets:

- ~0.000279974 (treating per-target events as independent)

## Notes

- ‘strict’ uses only arithmetic + sqrt + inverse; no π/e/φ, no log/exp.
- ‘medium’ adds π/e/φ but still no log/exp.
- ‘full’ (log/exp) is intentionally gated because it tends to make very tight fits easy.

To run full mode and regenerate the JSON:

```powershell
$env:W33_RUN_FULL='1'
python claude_workspace\w33_baseline_audit_suite.py
```
