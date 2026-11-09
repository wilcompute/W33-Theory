**Summary.** With a scalar field (`Omega_scf`) as dark energy, halofit computes its fitting-formula inputs from `index_bg_Omega_m` and `index_bg_Omega_r`. `background.c` fills those with the field split into a "matter" part (ρ − 3p) and a "radiation" part (3p); see `background.c` around line 486, "not very meaningful for oscillatory models", and the earlier discussion in #506. For a slowly rolling field (p ≈ −ρ), halofit therefore sees Ω_m ≈ Ω_m,true + 4Ω_φ and Ω_v = 1 − Ω_m − Ω_r ≈ 0. The resulting nonlinear power is badly wrong, and no warning is given. HMcode refuses scf explicitly ("not yet coded"); halofit runs.

**Reproduction (stock v3.3.1, commit 5668031).** Three runs share h = 0.674, ω_b = 0.0224, ω_cdm = 0.120, `output=mPk`, `non_linear=halofit`, `z_pk=0`:
1. Λ.
2. A w0 = −0.85 fluid.
3. A thawing exponential scalar field: `Omega_scf=-1`, `scf_parameters=1.0,0.0,0.0,0.0,16.0,0.0`, `attractor_ic_scf=no`, `scf_tuning_index=2`, `YHe=0.245`. Its w today is −0.848 and Ω_scf = 0.686.

| P_nl/P_lin at z = 0 | k = 0.1 h/Mpc | k = 1 | k = 3 |
|---|---:|---:|---:|
| Λ | 1.012 | 5.868 | 19.45 |
| fluid, w0 = −0.85 | 1.012 | 5.706 | 19.58 |
| **scalar field, w = −0.85** | **1.047** | **4.209** | **8.58** |

At z = 0 halofit reads Ω_m = 2.75 and Ω_v = 0, while the true Ω_m = 0.313. The linear P(k) is not affected.

In a modified build, the same ΛCDM run as a scalar field with constant potential gives 4.22 / 8.30 at k = 1 / 3 h/Mpc, against 5.91 / 19.93 for Λ. The halofit, fourier and background lines involved are unmodified stock code.

**Suggested fix (halofit only; background and perturbations unchanged).** At both places where halofit sets `Omega_m` and `Omega_v`, when `has_scf`:
- subtract the field's matter part (ρ_scf − 3p_scf)/ρ_crit from Ω_m, and its 3p_scf/ρ_crit from Ω_r;
- set Ω_v = 1 − Ω_m − Ω_r;
- use w = p_DE/ρ_DE, summed over scf, Λ and the fluid (the same instantaneous-w treatment as for a CPL fluid);
- use the corrected Ω0_m in f_ν.

With this, ΛCDM run as a scalar field matches Λ to 2×10⁻⁶ (the Ω_scf shooting precision). For an uncoupled exponential field, the nonlinear boost agrees to 0.04% with a CPL fluid fitted to the field's w(a). A patch script is here: https://github.com/wilcompute/W33-Theory/blob/master/analysis/toe_uv/class_halofit_scf_patch.py. An analogous HMcode treatment is in `class_hmcode_scf_patch.py` in the same directory.

A cheaper alternative would be a `class_test` refusing scf with halofit, as HMcode already does.
