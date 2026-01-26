# Native C24 W(3,3) projector full-grid scan (parity u_- embedding)

Grid:
- lambda: 0.4..0.56 step 0.01 (n=17)
- mu: [0.75, 1.25, 1.75]
- times: 0..2 step 0.25 (n=9)

Dynamics:
H = H_transport + lambda*H_coin + mu*V_defect7
Flux toggle: e* -> e on the 4 delta4 edges (0-20,10-12,26-27,27-45)

Measurement:
- 40 canonical W(3,3) C^4 rays (12th-root phases)
- Embedded into C^24 using u_- = (1,1,1,-1,-1,-1)/sqrt(6) along Z6.
- For each W33 line (basis of 4 points), score = stability(mean/max outcome over time).

Outputs:
- nativeC24_fullgrid_line_stabilities_flux_noflux.csv (2040 rows = 51 grid points * 40 lines)
- nativeC24_fullgrid_winners_flux_vs_noflux.csv (51 rows)
- nativeC24_line_flux_response_ranking_summary.csv (40 lines ranked by mean_abs_delta)
