# Pass 12632: a CLASS halofit bug invalidates every scalar-field shear prediction since Pass 12629 (correction notice; corrected numbers to follow)

Claude track. **This is a correction, and a retraction pending reruns.**

## The bug

Public CLASS (`source/background.c`, around line 486) splits a scalar field into a "matter" part ρ − 3p and a "radiation" part 3p, with the comment "not very meaningful for oscillatory models". Halofit (`external/Halofit/halofit.c`) reads Ω_m and Ω_r from those totals and sets Ω_v = 1 − Ω_m − Ω_r. For a slowly rolling dark-energy field (p ≈ −ρ), halofit therefore sees:
- Ω_m ≈ Ω_m,true + 4Ω_φ ≈ 3;
- Ω_r ≈ −2;
- Ω_v ≈ 0, that is, no dark energy.

It also computes f_ν from the inflated Ω0_m. The linear power is unaffected.

**Who is affected.** Every model run through our scalar-field path: ΛCDM (run as c = c′ = 0), fading c < 0 and c > 0, the exponential model, monodromy, and KLT. **CPL and plain Λ go through the fluid or Λ path and are correct.** So in every shear comparison since Pass 12629, CPL was the only model with correct nonlinear power.

## Controls (`analysis/toe_uv/halofit_check.py`)

The same ΛCDM parameters were run through three paths. The table shows P_nl/P_lin at z = 0.01 (`halofit_check_orig.json`, `halofit_check_hf.json`).

| | k = 0.1 h/Mpc | k = 1 | k = 3 |
|---|---:|---:|---:|
| plain Ω_Λ | 1.014 | 5.911 | 19.926 |
| w = −1 fluid (CPL path) | 1.014 | 5.911 | 19.926 |
| **scalar field, original build** | **1.053** | **4.222** | **8.304** |
| scalar field, patched build | 1.014 | 5.911 | 19.926 |

The linear P(k) of the scalar-field and Λ runs agrees to four digits at all k. Only the nonlinear spectrum differs: the ratio of nonlinear spectra is 0.71 at k = 1 and 0.42 at k = 3. The anomaly first appeared in `growth_ratio.py`, which on the original build gave CPL's nonlinear power at +134% over fading's at k = 3, z ≈ 0, even though CPL's linear σ8 was 1.7% lower (`growth_ratio_orig.json`).

## The fix (`analysis/toe_uv/class_halofit_scf_patch.py`)

The patch changes halofit only. At each call it removes the scalar field's matter and radiation parts and sets Ω_v = 1 − Ω_m − Ω_r. It uses w = p_DE/ρ_DE, summed over the scalar field, Λ and any fluid, which is the same instantaneous-w treatment CLASS gives a CPL fluid. f_ν uses the corrected Ω0_m. The patched builds are `~/cosmo/class_{fading,klt,klt2}_hf`. `class_cmb.py` now takes `CLASSBIN` and `MONOBIN` from the environment.

## Impact on the training fits is small (`hf_impact.py`; same parameters, no refit)

The halofit fix enters the expansion-plus-CMB fits only through the CMB lensing terms (lensed C_ℓ and ACT lensing). Δχ² (patched − original):

| ΛCDM | fading c < 0 | fading c > 0 | exponential | KLT | CPL (control) | plain Λ (control) |
|---:|---:|---:|---:|---:|---:|---:|
| +0.80 | +0.09 | +0.29 | +0.97 | +0.27 | 0.00 | 0.00 |

The patched ΛCDM moves to within 0.3 of the plain-Λ value, and refitting closes the rest. **The expansion-data results (Passes 12620–12628, out-of-sample BAO and SN) shift by less than 1 in χ², and against ΛCDM rather than for it.** They stand, pending a refit.

## What is withdrawn until rerun

- **Every shear result for the scalar-field models:**
  - the fixed-background shear χ² (`sign_des*.json`);
  - the held-out shear elpd (Passes 12629–12631);
  - the "CPL predicts held-out shear worst" result;
  - the combined totals (fading +4.72, CPL +0.32);
  - the block decomposition;
  - the power/geometry hybrid split.
- **Frozen statements S1, S7 and S8.** Their stated content is unchanged, but the evidence we cited for them is withdrawn.
- **Anything derived from those numbers on the other track**, including the S8 hybrid Shapley certificate (46e2945e2), which uses the original-build hybrid values.

The reruns with the patched builds are running (`/mnt/c/tmp/q18.sh`). This notice will be followed by the corrected tables, whichever way they come out.
