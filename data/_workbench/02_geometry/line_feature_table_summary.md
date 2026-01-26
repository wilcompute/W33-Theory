# Line feature table summary

Sources:
- `data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv`
- `data/_workbench/02_geometry/W33_line_phase_map.csv`
- `data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv`
- `data/_toe/native_fullgrid_20260110/nativeC24_fullgrid_winners_flux_vs_noflux.csv`

Outputs:
- `data/_workbench/02_geometry/line_feature_table.csv`

## Correlation
- Pearson (native vs canonical mean_abs_delta): 0.390912

## Top-10 overlap (native vs canonical)
- overlap_count: 4
- overlap_lines: 8, 3, 14, 7

## Largest rank deltas (|native_rank - canon_rank|)

- line 18: canon_rank=7, native_rank=36, delta=29
- line 26: canon_rank=5, native_rank=31, delta=26
- line 36: canon_rank=29, native_rank=4, delta=-25
- line 35: canon_rank=4, native_rank=29, delta=25
- line 39: canon_rank=3, native_rank=28, delta=25
- line 10: canon_rank=37, native_rank=14, delta=-23
- line 37: canon_rank=35, native_rank=12, delta=-23
- line 24: canon_rank=13, native_rank=32, delta=19
- line 15: canon_rank=10, native_rank=27, delta=17
- line 11: canon_rank=21, native_rank=7, delta=-14
