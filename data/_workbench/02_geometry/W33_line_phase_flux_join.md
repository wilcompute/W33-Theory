# W33 phase + flux sensitivity join

Sources:
- `data/_workbench/02_geometry/W33_line_phase_map.csv`
- `data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv`

Outputs:
- `data/_workbench/02_geometry/W33_line_phase_flux_join.csv`

## Distribution: unique k mod 6 (all lines)

- 1: 1
- 2: 1
- 3: 4
- 4: 15
- 5: 8
- 6: 11

## Distribution: unique k mod 6 (top 10 by mean_abs_delta)

- 2: 1
- 3: 2
- 4: 3
- 5: 2
- 6: 2

## Distribution: Q12 variance class (all lines)

- high(1): 1
- low(1/9): 27
- mid(1/3): 12

## Top 10 lines by mean_abs_delta

- line 8: mean_abs_delta=0.028922, unique_k_mod6=4, var_q_class=low(1/9), cards=3♡ 4♠ 8♣ 10♣
- line 19: mean_abs_delta=0.023528, unique_k_mod6=4, var_q_class=low(1/9), cards=10♠ 10♡ 10♢ 10♣
- line 39: mean_abs_delta=0.019453, unique_k_mod6=5, var_q_class=low(1/9), cards=2♠ 3♡ 6♣ 7♣
- line 35: mean_abs_delta=0.015444, unique_k_mod6=6, var_q_class=mid(1/3), cards=1♣ 2♣ 5♢ 8♣
- line 26: mean_abs_delta=0.012539, unique_k_mod6=3, var_q_class=low(1/9), cards=2♠ 2♡ 2♢ 2♣
- line 3: mean_abs_delta=0.012528, unique_k_mod6=5, var_q_class=low(1/9), cards=3♢ 4♣ 8♠ 10♡
- line 18: mean_abs_delta=0.011372, unique_k_mod6=6, var_q_class=mid(1/3), cards=1♡ 2♠ 5♠ 8♠
- line 7: mean_abs_delta=0.011269, unique_k_mod6=4, var_q_class=low(1/9), cards=6♠ 6♡ 6♢ 6♣
- line 14: mean_abs_delta=0.01094, unique_k_mod6=3, var_q_class=low(1/9), cards=2♢ 4♣ 5♣ 6♠
- line 15: mean_abs_delta=0.010632, unique_k_mod6=2, var_q_class=low(1/9), cards=8♠ 8♡ 8♢ 8♣
