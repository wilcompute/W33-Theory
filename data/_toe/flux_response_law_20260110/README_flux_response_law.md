# TOE flux-response law (canonical W33 projector coupling)

This folder contains an explicit, re-derived response model linking **central Z₂ holonomy (e\*)** to line-level stability shifts ΔS.

## Predictors computed per (λ, μ)

- **Defect mass**: mean_t Σ_{node in defect7} Σ_k |ψ[node,k](t)|²

- **Central coherence**: mean_t | Σ_node Σ_sector Σ_{z=0..2} ψ[s,z](t) · conj(ψ[s,z+3](t)) |

- Deltas are (flux − no-flux), where no-flux replaces e\*→e on the four delta4 edges.


## Response model per W33 line

For each line ℓ, I fit the linear model over the 51 grid points:

ΔS_ℓ ≈ c0 + c1·ΔC + c2·C_flux + c3·D_flux + c4·μ + c5·λ

where ΔC is the coherence difference (flux−noflux), C_flux is flux coherence mean, and D_flux is defect mass mean.


## Top flux-sensitive lines (by mean |ΔS|)

- **Line 8** (other; cards: 3♡ 4♠ 8♣ 10♣; quartet: `sec0_m2 sec1_m0 sec2_m0 sec3_m2`)
  - mean|ΔS|=0.02892, max|ΔS|=0.03961, R²=0.413
  - coeffs: c1(ΔC)=7.919, c2(C_flux)=-3.791, c3(D_flux)=-0.400

- **Line 19** (rank_spread; cards: 10♠ 10♡ 10♢ 10♣; quartet: `sec0_m1 sec1_m2 sec2_m2 sec3_m2`)
  - mean|ΔS|=0.02353, max|ΔS|=0.04238, R²=0.832
  - coeffs: c1(ΔC)=-51.034, c2(C_flux)=34.508, c3(D_flux)=2.872

- **Line 39** (other; cards: 2♠ 3♡ 6♣ 7♣; quartet: `sec0_m2 sec1_m2 sec2_m2 sec3_m1`)
  - mean|ΔS|=0.01945, max|ΔS|=0.02768, R²=0.581
  - coeffs: c1(ΔC)=8.340, c2(C_flux)=-4.785, c3(D_flux)=-0.438

- **Line 35** (other; cards: 1♣ 2♣ 5♢ 8♣; quartet: `sec0_m1 sec1_m2 sec2_m0 sec3_m1`)
  - mean|ΔS|=0.01544, max|ΔS|=0.02179, R²=0.829
  - coeffs: c1(ΔC)=-7.062, c2(C_flux)=5.411, c3(D_flux)=0.049

- **Line 26** (rank_spread; cards: 2♠ 2♡ 2♢ 2♣; quartet: `sec0_m1 sec1_m1 sec2_m2 sec3_m0`)
  - mean|ΔS|=0.01254, max|ΔS|=0.01790, R²=0.736
  - coeffs: c1(ΔC)=-2.955, c2(C_flux)=2.262, c3(D_flux)=-0.129


## Files

- `grid_flux_noflux_defectmass_coherence.csv`: predictors per (λ,μ)
- `response_law_regression_coeffs_all40.csv`: coefficients for all 40 lines
- `top15_flux_sensitive_lines_with_response_law.csv`: ranked top-15 with quartets + fitted coefficients
- `linewise_correlations.csv`: quick correlation diagnostics
