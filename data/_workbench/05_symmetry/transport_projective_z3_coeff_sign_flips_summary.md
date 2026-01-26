# Transport Z3 coefficient sign flips (ridge predictions)

Inputs:
- `data/_workbench/05_symmetry/transport_projective_z3_w33_line_shifted_quartets.csv`
- `data/_workbench/05_symmetry/quartet_ridge_response_coeffs_all81.csv`
- `data/_toe/flux_response_rankings_20260110/line_flux_response_summary.csv`

Flip counts by coefficient (sum1 -> sum2 / sum1 -> sum0):
- delta: sum2_flips=12, sum0_flips=13
- flux_coh: sum2_flips=15, sum0_flips=13
- def_mass: sum2_flips=14, sum0_flips=14
- mu: sum2_flips=12, sum0_flips=16
- lambda: sum2_flips=15, sum0_flips=15

Lines with flips (line ids):
- delta sum2: [2, 3, 6, 14, 17, 18, 20, 21, 22, 23, 28, 39]
- delta sum0: [2, 6, 7, 8, 13, 14, 15, 17, 18, 23, 30, 36, 39]
- flux_coh sum2: [2, 3, 6, 11, 14, 16, 17, 18, 20, 21, 22, 26, 28, 30, 39]
- flux_coh sum0: [2, 3, 6, 7, 8, 13, 14, 15, 16, 17, 26, 30, 36]
- def_mass sum2: [2, 6, 7, 8, 13, 14, 15, 17, 18, 21, 22, 23, 30, 39]
- def_mass sum0: [2, 3, 6, 7, 11, 13, 14, 17, 18, 20, 23, 28, 36, 39]
- mu sum2: [2, 6, 7, 8, 13, 14, 15, 17, 18, 23, 30, 39]
- mu sum0: [2, 3, 4, 6, 7, 11, 13, 14, 15, 17, 18, 20, 23, 28, 36, 39]
- lambda sum2: [2, 4, 6, 8, 15, 16, 17, 21, 22, 23, 26, 28, 32, 35, 39]
- lambda sum0: [4, 6, 7, 8, 13, 15, 16, 17, 20, 23, 26, 32, 35, 36, 39]

Top flux lines and node0 winners:
- line 8 (rank 1): flips=delta:sum0, flux_coh:sum0, def_mass:sum2, mu:sum2, lambda:sum2, lambda:sum0
- line 19 (rank 2): flips=none
- line 39 (rank 3): flips=delta:sum2, delta:sum0, flux_coh:sum2, def_mass:sum2, def_mass:sum0, mu:sum2, mu:sum0, lambda:sum2, lambda:sum0
- line 35 (rank 4): flips=lambda:sum2, lambda:sum0
- line 26 (rank 5): flips=flux_coh:sum2, flux_coh:sum0, lambda:sum2, lambda:sum0
- line 3 (rank 6): flips=delta:sum2, flux_coh:sum2, flux_coh:sum0, def_mass:sum0, mu:sum0
- line 18 (rank 7): flips=delta:sum2, delta:sum0, flux_coh:sum2, def_mass:sum2, def_mass:sum0, mu:sum2, mu:sum0
- line 7 (rank 8): flips=delta:sum0, flux_coh:sum0, def_mass:sum2, def_mass:sum0, mu:sum2, mu:sum0, lambda:sum0
- line 22 (rank 26): flips=delta:sum2, flux_coh:sum2, def_mass:sum2, lambda:sum2
- line 17 (rank 36): flips=delta:sum2, delta:sum0, flux_coh:sum2, flux_coh:sum0, def_mass:sum2, def_mass:sum0, mu:sum2, mu:sum0, lambda:sum2, lambda:sum0
