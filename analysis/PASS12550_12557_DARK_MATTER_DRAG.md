# Passes 12550–12557: dark matter drags the moduli

Claude track. Continues `PASS12546_12549_DARK_SECTOR_GEOMETRY.md`. Producer: `analysis/w33_pass12550_to_12557_dark_drag.py`. Test: `tests/test_w33_pass12550_to_12557.py`. Drivers in `analysis/toe_uv/`.

**This is not a theory of everything.** It sharpens one leading string-motivated reading of the DESI signal. Gauge group, generations, Λ, and strong CP stay unexplained.

## The main result

The fading dark sector (Bedroya, Obied, Vafa, Wu, arXiv:2507.03090) fits c′ ≈ 0.05, the slope of ln m_DM along the rolling field. Geometry gives |∇ln m_KK| ≥ 1/√2. Their footnote 2 reconciles the two by letting ∇m and ∇V point in different directions, so the path sees "a smaller slope for m along the direction of ∇V".

**That reconciliation does not survive matter domination.** The force on the moduli is ρ_c ∇ln m as well as ∇V, and for most of cosmic history ρ_c is the larger. Light moduli move along ∇ln m, whatever V does, so the data constrain b, the norm of ∇ln m in the light subspace, and not a projection chosen by V.

Either the modulus that sets the tower scale is heavy, or most dark matter is not on the tower. "The extra dimension is not stabilized" and "the dark matter is the tower" cannot both hold with c′ = 0.05. This assumes m_DM scales with the tower spacing, and it uses the standard moduli metric.

## 12550: CLASS with the coupling, and controls a broken build fails

`class_fading_patch.py` patches CLASS v3.3.1: background and perturbations in synchronous gauge, with θ_cdm evolved because the fifth force moves CDM off its geodesic. CLASS's Newtonian Klein-Gordon equation lacks the ψ terms, so that gauge is not used.

| Control | Result |
|---|---|
| plik-lite port vs planck-lite-py reference | exact to 1e-9 |
| H(z) ratio vs the independent solver `fading_ds.py` | within 3e-5, z = 0 to 2 |
| Einstein trace, numerical dh′/dτ vs h″ from total pressure, a > 0.1 | 2e-5 patched; **0.38 with the Klein-Gordon source sign flipped** |
| Growth at k = 0.2/Mpc vs G_eff = 1 + 2c′² ODE | 3e-5; G = 1 misses by 3 and 18 percent; **a flipped CDM force sign misses by 114 percent** |
| Planck-only ΛCDM | ω_b 0.02236, ω_c 0.1200, h 0.6734, n_s 0.9649; plik-lite χ² 586.4 |
| ACT DR6 + Planck PR4 lensing | χ² 19.9 on 19 bandpowers; 98.7 with ln A_s raised by 0.05 |

The trace test does not see the CDM force sign, which is why the growth test exists.

The controls caught three real bugs before any fit: the absolute shooting tolerance of CLASS treated V₀ ~ 1e-7 as converged, a guess that was exactly right gave a degenerate bracket, and the φφ column was converted with one power of l(l+1) too many.

**Numerical floor.** χ² jitters by about 0.1 in h. Scalar-field ΛCDM and native ΛCDM differ by 0.29 at the same parameters, a constant offset which I did not trace to its source. All fading models share the scalar-field reference; CPL is compared with native ΛCDM.

## 12551: full Planck spectra

Planck 2018 plik-lite TTTEEE, two low-l TT bins, τ prior 0.0544 ± 0.0073 (replacing low-l EE), DESI DR2, DES-Dovekie, with Levenberg-Marquardt fits: local optima, about 50 CLASS runs each. The paper used CLASS with full Planck likelihoods and ACT lensing, so this is a reproduction with a lighter likelihood, not a new analysis.

| Dovekie, Δχ² vs ΛCDM | c | c′ | Δχ² | published c, c′ |
|---|---|---|---|---|
| exponential | −0.64 | 0 | −3.8 | |
| fading, c < 0 | −0.90 | 0.053 | −10.7 | −0.92, 0.05 |
| fading, c > 0 | 0.67 | 0.053 | −8.4 | 0.69, 0.05 |
| Casimir line c = 4c′ | 0.18 | 0.046 | −3.0 | |
| CPL (vs native ΛCDM), w₀ = −0.81, wₐ = −0.69 | | | −12.3 | |

**The compressed CMB was not misleading.** Turning on c′ gains 7.0 (about 2.6σ) here and 6.4 on the compressed likelihood, on Dovekie. c′ = 0.05 ± 0.01 still does not mean 5σ, because the profile is asymmetric: −6.1, −8.0, −10.8, −4.1, +54.7 at c′ = 0.02, 0.03, 0.05, 0.07, 0.1.

**Lensing moves it up slightly.** At the best fits, without refitting, the lensing χ² falls from 22.7 (c′ = 0) to 20.0 (c′ = 0.05), and it is 61.7 at c′ = 0.1. Adding that gives a gain of 9.7, about 3.1σ. Treat this as indicative: lensing was evaluated post hoc on one sample. **This corrects the "2.3–2.8σ" of Pass 12547 for this sample.**

The Casimir line costs 5.4 against free c > 0 (2.3σ), and 6.0 on the compressed likelihood.

## 12552: the exact fixed point

With coupled dust and a massless field, χ_N = 2b is an exact attractor, with w_eff = 2b²/3 and ρ_c ∝ a^(−3−2b²). This is Amendola's φMDE (2000); only the application is at issue here.

| dark matter mass | b² | w_eff in the "matter era" | ρ_c |
|---|---|---|---|
| m_KK, all moduli free | 3/2 | **1** | a⁻⁶ |
| m_KK, fixed volume, n = 1 | 1/2 | **1/3** | a⁻⁴ |
| m_KK, fixed volume, n = 2, 3, 6 | 2/3, 3/4, 6/7 | 4/9, 1/2, 4/7 | a^(−13/3), a^(−9/2), a^(−33/7) |
| M_D, one extra dimension | 1/6 | 1/9 | a^(−10/3) |
| fitted c′ = 0.05 | 1/400 | 1/600 | a^(−3.005) |

At b² = 3/2 the matter era does not exist: KK matter with free moduli dilutes like kination. The fixed-volume branch, which survived Pass 12548's Cassini test, gives a radiation-like expansion for n = 1.

## 12553: two-field fits

Compressed CMB, background only, χ along ∇ln m, φ orthogonal, V = V₀ exp(−cφ − aχ). The control, with V and m along one field, returns the single-field χ² within 1e-5.

| b | Pantheon+ | DES-Dovekie | DES-SN5YR |
|---|---|---|---|
| 0.02 | −4.2 | −5.5 | −11.0 |
| 0.05 | −8.3 | −10.1 | −16.3 |
| 0.1 | +34 | +32 | +22 |
| 0.2 | +678 | +862 | +929 |
| 1/√6 | +2703 | +2309 | +2253 |
| 1/√2 | +5990 | +6312 | +3545 |
| √(3/2) | +8267 | +8616 | +8013 |

Values at large b are the best found by a local optimiser, with some scatter (b = 1 lies below b = 1/√2 on two samples). The exclusion does not depend on their exact size.

At b = 0.05 the fit reaches the single-field gain with V well away from the χ axis (c ≈ 0.6, a ≈ −0.6). **V's direction is not what the data pick; b is.**

## 12554: what is left

**1. Stabilise the modulus.** A valley χ = εφ gives c′ = bε, with ε ≈ 0.07 for b = 1/√2, if χ has mass μ. `dm_drag_mod.py` integrates the kick. The full fits fail to shoot above μ ~ 100 H₀; those failures are not counted as exclusions, and the full fits are not used for this estimate.

| μ/H₀ | range 1/μ | ρ_χ/ρ_c, b = 1/√2 | b = √(3/2) |
|---|---|---|---|
| 1e4 | 440 kpc | 4.3 | 4.9 |
| 1e5 | 44 kpc | 0.97 | 1.4 |
| 1e6 | 4.4 kpc | 0.33 | 0.64 |
| 1e7 | 0.44 kpc | 0.11 | 0.28 |
| 1e8 | 0.044 kpc | 0.036 | 0.10 |

Within its range χ mediates a dark-matter force 2b² = 1 to 3 times gravity. The paper's own bound is c′ ≲ 0.2 (2c′² ≲ 0.08), and the Sagittarius stream limit of about 10 percent (Kesden and Kamionkowski) is disputed (Keselman et al). Taken at face value, these need a range well below tens of kpc: **μ ≳ 1e5 to 1e6 H₀, roughly 1e-28 to 1e-27 eV.**

That is not "Hubble mass", and it is the stabilisation the scenario says it does not assume. [I] The modulus then also holds a substantial fraction of the dark matter as oscillations. [I] With Planckian field range, a stabiliser with that μ has scale √(μM_Pl) of about 0.6 to 1.9 eV, tuned against Λ by a factor of about 5e9 to 5e11. The bound on range is my reading of disputed work, and no halo simulation was run.

**2. Couple only a fraction f.** The drag is then χ_N = 2bfΩ_c and only f·b acts as c′. With f·b = 0.05, so f = 7 percent at b = 1/√2 and 4 percent at √(3/2): Δχ² = −7.6 to −9.2 (b = 1/√2) on Pantheon+ and Dovekie, −15.1 on DES-SN5YR, within 2.2 of the single-field gain. f = 0.3 costs over +170. Then at least 93 percent of dark matter is not on the tower, which gives up the "dark gravitons" identification for the bulk. It also leaves a small component with a force of order gravity, whose small-scale consequences I did not study.

**3. A steep wall** V_w = M exp(λχ), which stops the drag. |Δ ln m| from recombination to today is 0.283 at λ = 50 and 0.075 at λ = 200, so about 15/λ, and the fit reaches +754 to +770 and +81 to +87. Extrapolating, c′ = 0.05 needs λ ≈ 1000. That is a potential 1000 times steeper than any slope in the scenario; its other consequences are not examined here.

**4. Dark matter is not on the tower**, or its mass is sequestered from the moving moduli to about 5 percent. That is a different model, and the paper's link between DM and the dark dimension goes with it.

## 12555: β fitted directly

(c, c′, β) with baryon mass ∝ exp(−βφ), observed redshift corrected, SN M ∝ G^(−3/2) on or off. Control: β = 0 returns `fading_ds.py` exactly.

Cosmology alone is weak: |β| = 0.03 costs under 0.5 on all samples, and |β| = 0.1 costs about 1 to 10, the largest values being local fits that fell to c ≈ 0. **The solar system decides.** With Cassini and LLR the joint fit gives β ≈ 0.0007 and ξ ≈ 0.03 on all samples, consistent with zero, which is what Pass 12548's bound said. This pass confirms the bound rather than improving it.

## 12556: is crossing w = −1 needed?

The premium P = χ²(best w ≥ −1) − χ²(best free w), on 13 bins. Under a w ≥ −1 truth it is a mixture, not χ²(13), so p comes from mocks. Solved by bound-constrained sequential least squares. Nine random starts agree within 1e-5, and agree with Pass 12546's differential evolution within 0.1, which also gives Pantheon+ its global ceiling of −5.2.

| | Pantheon+ | Dovekie | DES-SN5YR |
|---|---|---|---|
| ceiling / free | −5.2 / −18.3 | −8.0 / −19.1 | −14.8 / −24.6 |
| premium | 13.1 | 11.1 | 9.8 |
| **p(premium), linear (20,000) / nonlinear (200)** | 0.10 / 0.065 | 0.21 / 0.175 | 0.27 / 0.21 |
| p(ΛCDM → ceiling gain) | 0.13 | 0.038 | 0.0017 |
| p(ΛCDM → free gain) | 0.11 | 0.074 | 0.012 |

**Crossing w = −1 is not required** on any sample. It replaces my rough p ≈ 0.27 of Pass 12546. The evidence against ΛCDM from a w ≥ −1 history depends strongly on the sample, reaching 3σ only on DES-SN5YR, and it sits at z < 0.07 (Pass 12546). A 13-bin test has less power than CPL's two parameters, so these p values do not contradict CPL's larger significance. Background only, compressed CMB. Truth was fixed at the ceiling's best fit, not marginalised.

## 12557: clocks and neutrinos

At the fitted roll (|φ_N| ≈ 0.43 to 0.54 today), Lange et al (2021) give |d ln α/dφ| ≲ 1e-7 and |d ln μ/dφ| ≲ 3e-6. MICROSCOPE bounds a product, κ_univ κ_α ≲ 1.5e-12, with an electromagnetic mass-fraction difference of 2.4e-3 that I estimated. The rolling field must be sequestered from the Standard Model to one part in 1e7; the brane localisation the paper invokes has to deliver that, loops included. I did not compute the loops.

**A clean zero, with its scale control.** Bulk Dirac neutrinos give m_ν ∝ L^(−1/2), so at most a 2.5 percent shift from recombination to today. Resolving 0.02 eV out of 0.06 eV needs 12 times more. The rolling radius does not connect to the neutrino window of Passes 12534–12539 at any measurable level.

## Standing

| Label | Claim |
|---|---|
| [E] | w_eff = 2b²/3 fixed point; b² values from the moduli metric |
| [N] | All fits, profiles and p values above, on the stated likelihoods |
| [I] | "Either heavy modulus or sparse coupling": needs m_DM ∝ tower spacing, a locally flat moduli metric, and no other force competing with ρ_c ∇ln m at z ≫ 1 (a wall is one such force) |
| [C] | Range requirement μ ≳ 1e5 to 1e6 H₀: rests on a disputed stream bound, with no halo simulation |

**Novelty is not claimed.** φMDE and radion sourcing by KK matter are old. In the three dark-dimension papers I read and a few web searches I did not find this argument applied to the fading dark sector, but that search is narrow. Someone should search harder before citing it as new.

**Gaps.** plik-lite instead of the full Planck likelihoods. Lensing post hoc. Two-field results use the compressed CMB and background only, though Dovekie's single-field agreement suggests that is adequate near b = 0.05, and at large b the failure is in the background itself. No nonlinear structure. Clock and MICROSCOPE bounds quoted from their abstracts.

## Sources

arXiv:2507.03090 (Bedroya et al), 2503.14738 (DESI DR2), 1907.12875 (Planck likelihoods), 1909.05869 (planck-lite-py), 2307.01100 (radion in the dark dimension), 2209.15487 (MICROSCOPE), 2010.06620 (Lange et al), 0903.4458 (Kesden, stream force bound), DOI 10.1103/PhysRevLett.97.131303 (Kesden and Kamionkowski; DOI from memory), ACT DR6 lensing likelihood `act_dr6_lenslike` 1.2.1.
