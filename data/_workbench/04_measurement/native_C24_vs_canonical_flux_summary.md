# Native C24 vs canonical flux ranking comparison

Inputs:
- `data/_toe/flux_response_rankings_20260110/line_flux_response_summary.csv`
- `data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv`

- lines compared: 40
- spearman_rank_correlation: 0.330

Top 10 overlap:
- canonical_top: [8, 19, 39, 35, 26, 3, 18, 7, 14, 15]
- native_top: [8, 3, 14, 36, 7, 1, 11, 12, 21, 38]
- overlap: [3, 7, 8, 14] (n=4)

Largest rank gaps (top 10):
- line 18: canonical_rank=7, native_rank=36, diff=29
- line 35: canonical_rank=4, native_rank=32, diff=28
- line 26: canonical_rank=5, native_rank=31, diff=26
- line 36: canonical_rank=30, native_rank=4, diff=26
- line 39: canonical_rank=3, native_rank=28, diff=25
- line 10: canonical_rank=37, native_rank=14, diff=23
- line 37: canonical_rank=35, native_rank=12, diff=23
- line 15: canonical_rank=10, native_rank=27, diff=17
- line 24: canonical_rank=13, native_rank=30, diff=17
- line 11: canonical_rank=22, native_rank=7, diff=15
