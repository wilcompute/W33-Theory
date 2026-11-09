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

## Addendum 1: independent check of the patch, and the corrected fixed-background shear

**Matched-fluid check (`hf_matched_fluid.py`).** Halofit depends only on Ω_m(z), Ω_v(z), w(z), f_ν and the linear P. For each scalar-field best fit I fit (w0, wa) to the field's own w(a) over z < 3. I then run the same parameters through CLASS's untouched fluid path and compare the nonlinear boost at k = 0.3, 1 and 3 h/Mpc, z = 0.01 and 1:

| largest deviation from the matched fluid | exponential (uncoupled) | fading c < 0 | fading c > 0 |
|---|---:|---:|---:|
| patched build | **0.04%** | 3.9% | 4.4% |
| original build | 57% | 57% | 58% |

The uncoupled model agrees to 0.04%, so the patch reproduces the fluid path's halofit inputs. The roughly 4% residual for the coupled models is plausibly the coupling, which changes Ω_m(z) and linear growth so they are not the same physics as the fluid. That attribution is not separately tested. Halofit is in any case uncalibrated for coupled dark matter, a caveat that applied before the fix too.

The patched scalar-field path matches plain Λ to 2×10⁻⁶. This is the numerical Ω_scf-tuning precision; the original build was off by 0.58.

**Corrected fixed-background shear** (Dovekie full-data cosmologies, nuisances refitted; `sign_des*.json`, originals in `*_orig.json`). The table shows χ²_shear relative to ΛCDM:

| | fading c < 0 | fading c > 0 | CPL | **CPL − fading c < 0** |
|---|---:|---:|---:|---:|
| DES Y3, original build | +1.19 | +0.31 | +4.29 | +3.10 |
| DES Y3, **patched** | +1.94 | +1.00 | +1.29 | **−0.64** |
| KiDS-Legacy, original build | +1.73 | +0.34 | +6.41 | +4.68 |
| KiDS-Legacy, **patched** | +2.49 | +1.06 | +2.21 | **−0.28** |

CPL's raw χ² is unchanged; it is a control. **CPL's apparent shear penalty was entirely the bug.** With correct nonlinear power, the evolving-dark-energy models all sit 1–2.5 behind ΛCDM on shear, and shear does not separate CPL from fading: |Δχ²| < 0.7.

The hybrid split is now small: CPL − fading = −0.60 (DES) and −0.32 (KiDS), made of power −1.3/−1.6 and geometry +1.6/+1.9. The earlier "55–60% power, high-z" mechanism is withdrawn.

**Frozen statements.**
- **S1** ("fading beats CPL on shear") is **not supported by current data**: the difference is within 0.7, slightly favouring CPL. Its formal target, the next release, still stands.
- **S8**, as frozen (Δχ²(CPL − fading) > 0, carried by high z), **would be falsified if current data counted**. They don't formally, but I now expect it to fail.
- **S7's** sign clause goes the same way.
- The frozen files stay unedited as the record.

The held-out shear rerun (`q19`) and the patched refit of the training fits (`q20`) are running.

## Addendum 2: a second nonlinear model (HMcode) agrees

Stock CLASS **refuses** to run HMcode with a scalar field ("Cannot use scalar field scf with HMcode (not yet coded)"). Halofit has no such guard and returns wrong answers without warning, which is the bug above.

`class_hmcode_scf_patch.py` supplies the missing treatment and lifts the guard (`~/cosmo/class_fading_hm`). It applies the same Ω correction, sets Ω_w = Ω_φ, and takes w0, wa from the field's w at a = 1 and 1/2. Results (`hmcode_check.py`, `hmcode_check.json`):

| HMcode P_nl/P_lin, z = 0.01 | k = 0.1 h/Mpc | k = 1 | k = 3 |
|---|---:|---:|---:|
| ΛCDM, plain Λ = w = −1 fluid | 1.017 | 5.585 | 18.817 |
| ΛCDM, scalar field, patched | 1.028 | 5.601 | 18.825 |
| fading c < 0 best fit, patched | 1.022 | 5.641 | 18.903 |
| CPL best fit | 1.013 | 5.537 | 18.601 |

The patched scalar-field ΛCDM residual is 0.3% at k = 1 and 1.1% at k = 0.1. This is from HMcode's approximate growth with fitted (w0, wa); it is not chased further.

**The fading/CPL boost ratio at k = 1, z ≈ 0 is +1.9% in HMcode and +0.6% in patched halofit.** Both nonlinear models put fading and CPL within about 2% in nonlinear power, consistent with the corrected shear result that the shear data do not separate them.

## Addendum 3: reproduced on stock CLASS and reported upstream (lesgourg/class_public#682)

Stock CLASS v3.3.1 (commit 5668031) with a thawing exponential scalar field (λ = 1, w = −0.848 today, Ω_scf = 0.686) gives the following P_nl/P_lin at z = 0:

| | k = 1 h/Mpc | k = 3 |
|---|---:|---:|
| scalar field | 4.21 | 8.58 |
| matched w0 = −0.85 fluid | 5.71 | 19.58 |
| Λ | 5.87 | 19.45 |

Halofit reads Ω_m = 2.75 and Ω_v = 0, while the true Ω_m is 0.313.

The input files and the issue text are in `analysis/toe_uv/class_issue_682/`. The documented explanatory.ini scalar field is a tracker with w ≈ 0 today, behaving like matter, so it does not show the problem; that is why a thawing potential is used. Posted as https://github.com/lesgourg/class_public/issues/682 from the wilcompute account.

## Addendum 4: scale-cut robustness, S9 frozen, and an audit of every other halofit consumer

**Conservative cuts** (ξ₊ > 30′, ξ₋ > 120′; `sign_des*_cut30.json`, patched builds). χ²_shear relative to ΛCDM:

| | fading c < 0 | fading c > 0 | CPL | CPL − fading |
|---|---:|---:|---:|---:|
| DES Y3 | +1.35 | +0.45 | +1.17 | −0.18 |
| KiDS-Legacy | +0.13 | −0.24 | +0.40 | +0.27 |

The no-split result holds and tightens: |CPL − fading| ≤ 0.27, and every model is within 1.4 of ΛCDM. The baryon-feedback check was conditional on a shift above 0.5, so it was not needed.

**Frozen S9** (`prereg_noshear.json`, sha f40c2645). The next shear releases will not separate CPL from fading (|Δχ²| < 2 per survey), and every evolving model will stay within 4 of ΛCDM. S9 supersedes S8 and the sign clauses of S1 and S7.

**Audit of every script that reads `pk_nl`.**
- `class_des_fit.py`: corrected above.
- `class_shear_equiv.py` (Pass 12583, the shear-equivalent S8): both the mocks and the ΛCDM family it fits went through the scalar-field path. Rerun with patched builds, including a patched `class_massive_hf` for the relaxing radion: **pending** (`class_shear_dovekie_hf.json`).
- `nbody_ic.py` and `nbody_pm.py` (Pass 12573): the coupled/control power ratio, the N-body result itself, never used halofit and stands. The **control-vs-halofit check** used the faulty scalar-field halofit. Against the patched halofit (`nbody_halofit_recheck.py`), the 100 Mpc/h control reaches 0.54–0.94 of the nonlinear power at k = 0.3–2.9 h/Mpc, so the largest deviation is 59%, not the "within 22 percent" stated in Pass 12573. The particle-mesh run under-resolves small-scale power, as expected at that resolution. The earlier agreement came from comparing against a wrong reference.
- Pass 12593 §(DES shear χ², ΛCDM 201.48 against fading 201.83) used the unpatched likelihood. The patched fixed-background values are ΛCDM +0 and fading +1.94 (DES), so the shear data still absorb fading's higher S8, at a cost of about 2 rather than 0.35.
- Everything else (BAO, SN, CMB, fσ8 from linear σ8, S8 priors) uses linear quantities. CMB lensing moved by less than 1 (`hf_impact.json`).
