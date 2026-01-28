# Sage.zip continuation — effective low-dimensional TOE model (2026-01-11)

This checkpoint is computed **only from Sage/data/** inside Sage.zip.

## 1) Sanity check: we can exactly reproduce nativeC24 full-grid stabilities
Using:
- H_transport from `data/_toe/projector_recon_20260110/N12_58_orbit0_H_transport_59x24_sparse_*.npz`
- H_coin from `data/_toe/projector_recon_20260110/N12_58_sector_coin_C24_K4_by_k_sparse_*.npz`
- defect7 potential on nodes {0,10,12,20,26,27,45}
- flux toggle = replace `e* -> e` on the 4 delta4 edges in `N12_58_orbit0_edges_with_2T_connection_*.csv`
- W(3,3) point rays in C^4 from `data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv`
- embedding to C^24 via u_- = (1,1,1,-1,-1,-1)/sqrt(6) along Z6 (per README)
- measurement p_point(t)=Σ_node |<phi_point,psi_node(t)>|^2, line score uses max over the 4 points per line
- stability = mean(max)/std(max) over times t=0..2 step 0.25

At (λ,μ)=(0.50,1.25), stabilities match the stored CSV to numerical precision (~1e-11).

## 2) State-space structure at a representative keypoint (λ,μ)=(0.50,1.25)
Let d(t)=psi_flux(t)-psi_noflux(t). SVD over the 9 sampled times yields singular values:
[1.648e+00, 1.265e+00, 7.530e-01, 3.628e-01, 1.223e-01, 2.846e-02,
 4.572e-03, 4.242e-04, 3.237e-20]

Key fact: **every right singular vector lies in the deck-odd subspace**, i.e. it is an eigenvector of the deck swap Z (pos->pos+3) with eigenvalue -1.
Numerically: deck_minus_mass = 1.0 to machine precision for the top modes.

Interpretation: the flux toggle injects dynamics only in the **central Z2 (e*) channel**; the deck-even channel is exactly unaffected.

The leading difference modes localize on the nontrivial holonomy cycles:
- modes 1–2 are dominated by cycles 3/4 (the long cycles passing through nodes 12,27,26,45)
- modes 3–5 lean toward cycles 1/2 (the 0–20 defect channel)

See `keypoint_lam0p5_mu1p25_difference_modes_summary.csv`.

## 3) Line-space (measurement-space) compression across the entire 51-point grid
Let D be the 51×40 matrix of delta_stability over the full grid.
SVD energy shares:
- mode1: 0.7642
- mode2: 0.1255
- mode3: 0.0920

So **the top 3 modes capture ~0.9817** of the full grid response.

Mode1’s heaviest weights are (line8,line3) negative versus (line14,line36,line7,line1,...) positive — exactly the observed winner competition.
See `delta_mode1_topweights.csv`.

The grid coefficients (c1,c2,c3) are smooth in (λ,μ); c2 and c3 are near-linear in λ for each μ.
See `grid_delta_mode_coefficients_c1_c2_c3.csv`.

## 4) Immediate next step suggested by this checkpoint
Because the response lives in:
- a **strict deck-odd state-space channel**, and
- an **~3-dimensional line-space field theory**,

the next high-leverage computation is to:
1) fit a compact parametric form for (c1,c2,c3)(λ,μ) (e.g., low-degree polynomial or rational),
2) interpret c1 as “flux amplitude” and (c2,c3) as “coin–defect interference” terms,
3) then map the line modes (v1,v2,v3) back to projective quartets/orbits to extract a closed-form symmetry explanation for which measurements are flux-favored vs flux-suppressed.
