# Pass 12627: shear prefers fading over CPL out of sample; the MCMC confirms fading's held-BAO gain; but any particle carrier of the coupling is radiatively unnatural (Chat's audit, accepted)

Claude track. Producer: `analysis/w33_pass12627_mcmc_shear_radiative.py`. Test: `tests/test_w33_pass12627.py`. Scripts in `analysis/toe_uv/`: `mcmc_holdout.py`, `des_joint_cpl.py`, `shear_ppd.py`. The sign grid (`sign_grid.py`) and the c > 0 joint refit (`des_joint_cpos.py`) are still running and go to an addendum.

**Not a theory of everything.**

## 1. MCMC: fading on DES-SN5YR with BAO held out

emcee, 20 walkers × 60 steps, burn-in 20, one threaded CLASS process. τ_int ≈ 6 steps, so about 130 effective samples.

- **Held-BAO elpd: −10.97, against ΛCDM's −12.34, a gain of +1.4.** The Fisher draws gave −13.13 untruncated and −9.84 truncated, so the MCMC sits between them, closer to the truncated value.
- Trained without BAO, c′ = 0.018 ± 0.015 (1.2σ from zero) and c = 0.10 ± 0.73 (the two modes).
- **The walkers stay 55/45 in the two signs, but emcee does not move between separated modes,** so that split mostly reflects the 50/50 start. Mode weights come from the grid, still to come.

## 2. Does CPL's shear penalty survive a joint refit?

Joint fit of plik-lite + τ + DESI + Dovekie SN + lensing + fσ8 + DES Y3 shear:

| | total χ² | shear (des + nuisance priors) |
|---|---:|---:|
| ΛCDM | 2466.92 | 202.77 |
| fading c < 0 | 2456.22 | 203.34 |
| CPL (new, w₀ = −0.82, wₐ = −0.64) | 2457.91 | **206.56** |

**Yes.** CPL's shear is 3.2 worse than fading's after refitting, against 3.0 at fixed background. CPL wins elsewhere, so the totals differ by only 1.7.

## 3. Shear held out: who predicts DES Y3?

Train on everything except shear, draw 20 truncated Fisher samples per model, refit the ten DES nuisances for each draw, and score the shear:

| elpd_shear | ΛCDM | fading c > 0 | fading c < 0 | CPL |
|---|---:|---:|---:|---:|
| DES Y3 | **−101.38** | −101.43 | −101.80 | −103.50 |

- **Fading predicts held-out shear better than CPL by 1.7 (c < 0) to 2.1 (c > 0).** ΛCDM predicts it best, narrowly.
- Frozen statement S1 (fading beats CPL on shear) therefore points the right way on DES Y3: at fixed background, in a joint refit, and out of sample. DES Y3 is not the future data S1 is scored against.
- Adding shear-held to the Dovekie out-of-sample totals of Pass 12626 gives fading +5.3 and CPL +3.4 over ΛCDM. On Dovekie, shear reverses the CPL/fading tie.

## 4. Chat's audit (3869fe29c, 4b97ce7d1, c7079f950): accepted, and it closes the particle carrier

Chat's track read Pass 12628 in full and found:
- **(a) Radiative instability.** A 16 keV Majorana mass m ∝ e^(−bφ) puts a one-loop curvature of 3.76×10²³ H₀² into φ's potential (at μ = m). Present-day subtraction does not protect the history. The method is Chat's, already owned (`toe_20261103_dark_radiative_stability.py`), with general background in Garny, hep-ph/0606120. **This was missing from my corridor.**
- **(b) The parent scalar's quartic is non-perturbative.** With m_S² = λ_S v_S² (canonical w = v_S/√2), λ_S ≈ 10 at (16 keV, 3 TeV) and about 370 at 10 TeV, and the boundary scales as λ_S ≈ 5.3 (M_N/16 keV)¹⁵.
- **(c) Lyman-α from mean or rms momentum is only a proxy.** Chat's counterexamples have equal mean and second moment but different free-streaming kernels. A transfer function is needed. My 15.8–17.4 keV edge is a proxy, not a bound.
- **(d) The upper edge is not general.** Momentum-resolved kinetics with inverse Higgs decays give the right abundance at 16, 30 and 100 keV in its declared model, but scalar self-collisions are then large at 16 and 30 keV.
- **(e) A producer gap.** `sterile_hh.json` held two fields that `sterile_hh.py` did not produce, because they came from an inline snippet. **Fixed in this pass:** the producer now writes them.

**General form of (a) (`axion`-independent).** One field-dependent mass m adds V″ ≈ b² m⁴/(4π² M_P²). Keeping that below H₀² requires

**m ≲ (4π² H₀² M_P²/b²)^(1/4) = 0.020 eV** (b = 0.053; reproduces Chat's 3.76×10²³ at 16 keV).

The same holds for every heavier field whose mass moves with φ, such as the parent's radial mode. So without a protecting symmetry, **no particle dark matter heavier than about 0.02 eV can carry the fading coupling naturally.** The coupling is then as fine-tuned as the cosmological constant itself.

This general statement is old: Doran and Jaeckel 2002 on loop corrections to quintessence; Garny 2006. **No novelty is claimed.** It supersedes the "sterile neutrino survives" conclusion of Passes 12626 and 12628. The frozen S5 corridor is now conditional on an unbuilt protecting mechanism, and on the proxy Lyman-α edge.

## 5. Where this leaves the line of work

- **The data side stands.** Evolving dark energy beats ΛCDM out of sample. Shear now separates fading from CPL, by 1.7–3.2 depending on method. BAO cannot fix the sign of c.
- **The particle side is closed as a naturalness problem.** A fading coupling to any particle dark matter is radiatively unnatural unless protected, for example by supersymmetry with splittings below 10⁻²⁰ eV (Chat's estimate). The interesting physics question becomes whether any symmetry can protect it, not which particle carries it.

## Sources

Chat's track: `analysis/2026-11-06_sterile_parent_and_changed_work_audit.md`, `..._inverse_higgs_production_and_sterile_spectra.md`, `..._scalar_self_reactions_and_threshold_cancellation.md`. Literature: hep-ph/0606120 (Garny); astro-ph/0203018 (Doran and Jaeckel, as recalled); arXiv:1609.01289; 0911.1120.

## Addendum (2026-11-08): the sign grid failed by design; naturalness literature; the one natural home

**`sign_grid.py` is withdrawn as an evidence estimator.** With the base cosmology held at each mode's best fit, χ² changes by tens per grid step in c′ (for example 2298 → 2329 → 3010 at c = −0.9), because nothing compensates the shift in today's dark-matter density. The fixed-base conditional width is far below the marginal σ(c′) = 0.035. Its 15×15 grid cannot resolve the posterior, and its minima (2261–2263) sit 18 above the refitted optimum (2243.75). This was my design error. The partial `sign_grid.json` is kept as a record. The valid estimates are:
- the Pass 12625 Laplace weight on Dovekie, P(c > 0) = 0.26 (both modes well inside the prior);
- the profile likelihood in c (`c_profile.py`, running: all other parameters refitted at 11 fixed values of c).

**Literature on natural couplings (abstracts read, full texts not):**
- "The Impossible Triangle" (arXiv:2607.10859): energy-transfer portals (trilinear, quartic, Yukawa) between dark matter and dark energy at the sizes needed for S8 require tuning of 10⁵²–10⁸⁷, even with SUSY. Derivative couplings saturate at about 4% S8 suppression.
- arXiv:2603.07879: a pseudo-Goldstone dark energy is radiatively stable only if the renormalisable portals are forbidden, which leaves derivative (pure momentum-exchange) couplings with no background energy transfer.
- arXiv:2512.11639: pure momentum exchange breaks down at w = −1 unless energy is also transferred, which matters for CPL's crossing.
- Tsedrik and Bose (arXiv:2512.17684): dark scattering plus CPL against DES Y3 3×2pt + DESI DR2 + DES-SN5YR + Planck gives an interaction **consistent with zero**. So "CPL + momentum exchange removes CPL's shear penalty" is already tested and null. Our CPL shear penalty (1.7–3.2) is a 1–2σ effect consistent with that.

**The one natural home for a fading coupling: axion monodromy (D'Amico, Hamill and Kaloper, arXiv:1605.00996).** Take a dark-matter axion a (decay constant f) mixed with a dark-energy axion φ (decay constant F) through Λ⁴ cos(a/f + φ/F).
- The dark-matter mass varies as m² ∝ cos θ, so **b = (M_P / 2F) tan θ**. Our fitted b ≈ 0.05 needs **F ≈ 10 M_P / tan θ**, which is super-Planckian, hence monodromy.
- φ enters only through a phase protected by shift symmetry, so the 0.02 eV cap does not bite: the φ-dependence is the axion potential itself, not an extra loop term.
- The dark matter is then an axion lighter than 0.02 eV and heavier than about 2×10⁻²⁰ eV (Lyman-α on wave dark matter, recalled from memory). Averaged over oscillations, it behaves as the fading model's mass-varying, number-conserving dark matter.
- **Distinctive prediction:** the coupling runs, b ∝ tan θ(φ), whereas every fit here assumed a constant b. A fit with b(φ) = b₀ tan(θ₀ + φ/F)/tan θ₀ would test this.
- The mechanism is D'Amico, Hamill and Kaloper's, so no novelty is claimed. The mapping onto the fitted b is the framing added here.

**Scorecard** (`scorecard.py`) now has a shear-held column. Dovekie out-of-sample plus shear gives fading +5.3 and CPL +3.4 over ΛCDM.

**How much the coupling runs in that completion (`monodromy_running.py`).** I fix F by c′(φ₀) = c′_fit and use each fit's field excursion since recombination (Δφ = 0.26–0.85 M_P).

| θ₀ today | F | c′ change since recombination, c < 0 | c > 0 |
|---|---:|---:|---:|
| 0.30 | ≈ 3 M_P | +47 to +49% | breaks down (θ crosses 0) |
| π/4 | ≈ 9 M_P | +6% | +18 to +21% |
| 1.20 | ≈ 23–24 M_P | +3% | +10 to +11% |
| 1.45 | ≈ 73–78 M_P | +3% | +8 to +10% |

- For F ≳ 9 M_P, the constant-c′ fits approximate the natural completion to ≲ 6% (c < 0) or ≲ 21% (c > 0).
- For F ≈ 3 M_P, they do not.
- The completion predicts that c′ grows toward today. A fit with this one-parameter running (F) is the next CLASS patch (`class_fading_patch.py` would need c′ → tan(θ₀ + φ/F)/(2F), including the dc′/dφ terms in the perturbation equations).
