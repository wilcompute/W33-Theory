# Native C24 full-grid summary

Sources:
- `data/_toe/native_fullgrid_20260110/nativeC24_fullgrid_winners_flux_vs_noflux.csv`
- `data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv`

## Winner flips
- winner_changed_count: 51 / 51

## Flux winners by mu (line_id: count)

- mu=0.75 line=36: 17
- mu=1.25 line=14: 11
- mu=1.25 line=36: 6
- mu=1.75 line=14: 9
- mu=1.75 line=36: 5
- mu=1.75 line=7: 3

## No-flux winners by mu (line_id: count)

- mu=0.75 line=3: 13
- mu=0.75 line=8: 4
- mu=1.25 line=3: 13
- mu=1.25 line=8: 4
- mu=1.75 line=11: 12
- mu=1.75 line=3: 5

## Top 10 lines by mean_abs_delta (native)

- line 8: mean_abs_delta=8.49327497788095, unique_k_mod6=4, var_q_class=low(1/9)
- line 3: mean_abs_delta=7.517186487724674, unique_k_mod6=5, var_q_class=low(1/9)
- line 14: mean_abs_delta=7.486776248626127, unique_k_mod6=3, var_q_class=low(1/9)
- line 36: mean_abs_delta=7.097558018762999, unique_k_mod6=6, var_q_class=mid(1/3)
- line 7: mean_abs_delta=6.823915242613725, unique_k_mod6=4, var_q_class=low(1/9)
- line 1: mean_abs_delta=6.423742771015123, unique_k_mod6=6, var_q_class=mid(1/3)
- line 11: mean_abs_delta=5.680064573809641, unique_k_mod6=3, var_q_class=low(1/9)
- line 12: mean_abs_delta=5.674183043183397, unique_k_mod6=4, var_q_class=low(1/9)
- line 21: mean_abs_delta=5.066053204772975, unique_k_mod6=4, var_q_class=mid(1/3)
- line 38: mean_abs_delta=4.268223125365549, unique_k_mod6=6, var_q_class=low(1/9)

## Mean mean_abs_delta by unique k mod 6 (native)

- k_mod6_unique=1: mean_abs_delta=0.847794 (n=1)
- k_mod6_unique=2: mean_abs_delta=1.95586 (n=1)
- k_mod6_unique=3: mean_abs_delta=3.990311 (n=4)
- k_mod6_unique=4: mean_abs_delta=3.439398 (n=15)
- k_mod6_unique=5: mean_abs_delta=2.678224 (n=8)
- k_mod6_unique=6: mean_abs_delta=2.778778 (n=11)

## Mean mean_abs_delta by Q12 variance class (native)

- var_q_class=high(1): mean_abs_delta=0.847794 (n=1)
- var_q_class=low(1/9): mean_abs_delta=3.221803 (n=27)
- var_q_class=mid(1/3): mean_abs_delta=2.875977 (n=12)

## Overlap with canonical top10 (sector-reduced)

- overlap_count: 4
- overlap_lines: 8, 3, 14, 7
