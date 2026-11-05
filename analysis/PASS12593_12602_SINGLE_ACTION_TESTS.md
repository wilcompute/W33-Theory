# Passes 12593–12602: testing single-action candidates, and what failed

Claude track. Continues `PASS12583_12592_NEUTRINO_OVERLAP.md`. Producer: `analysis/w33_pass12593_to_12602_single_action_tests.py`. Test: `tests/test_w33_pass12593_to_12602.py`. Drivers in `analysis/toe_uv/`.

**This is not a theory of everything, and nothing here gets close to one.** Every complete candidate tested fails at least one major gate. The round gives one real out-of-sample success for the dark-sector coupling, a real shear likelihood, several sharp no-gos, and four retractions.

## The result in brief

1. **A rolling dark dimension and a Standard Model on an E8 wall are mutually exclusive** (12593). The heterotic route and the fading-radius route cannot both hold, unless the rolling field is not the radius.
2. **Real DES Y3 shear leaves the coupling's gain nearly intact** (12596): c′ gain 7.7, shear χ² moving by under 1. This replaces the stand-in survey of Pass 12583.
3. **The coupling predicts held-out supernovae** (12597): the fit with lowest training χ², which never saw SN, is 5.25 better than ΛCDM on them; the exponential is not, and CPL is 15 to 17 worse. Across both held-out probes fading beats CPL by 7.4 to 22.6. This is the first out-of-sample success in this programme, but not a blind one.
4. **Evidence is still weak** (12597): Laplace ln B is 0.44 for fading and 1.26 for the radion under stated flat priors.
5. **One action with one scale fails** (12601): D3-branes at C³/ℤ₃ with the SUSY-breaking loop closed miss sin²θ_W by 8.4 percent, and neutrinos by a factor of thousands.
6. **Everpresent Λ fails on DESI in both forms tested** (12602).
7. **Random Yukawa chains tie Froggatt-Nielsen and do not beat it** (12599).

## Retractions in this round

| What I said | What is true |
|---|---|
| Holdout: fading predicts SN at 1629.99 from the first run | That run started at the optimum fitted to the held data and did not move. It leaked. Withdrawn; the neutral rerun is below |
| Forward chain gets CKM ordering right | Numpy returns singular values heaviest first and I did not reverse them, so θ₁₂ and θ₂₃ were swapped. The corrected forward chain has the ordering backwards |
| Strong CP solved at no likelihood cost by SL(3) hops | A tautology: dividing a hop by det^(1/3) rescales Y by a scalar, so masses and angles cannot change. The physics is whether a symmetry enforces it, and that is not built |
| v²/M_s ≈ 0.04 eV at M_s ~ 10¹² GeV | Arithmetic slip. It is about 37 eV |

Also recorded as failed predictions: the (d−1) = 3 ≡ 0 obstruction to Fierz-Pauli in characteristic 3 does not occur (12600); the lepton ratio 0.53 ≈ ½ is not evidence, because the spread at the needed chain length is 0.28 to 1.07 (12599).

## 12593: the wall against the rolling radius

**[E]** `hw_wall_radius.py`. On an 11D interval, M_Pl²/M₁₁² ∝ Vρ and α_wall ∝ 1/V, with two moduli. Solar-system tests need Vρ fixed and the α clock needs V fixed, and together those fix ρ.

| Branch | β | d ln α/dφ | Violation |
|---|---:|---:|---|
| V fixed | 1/√6 = 0.408 | 0 | 163 times Cassini |
| Vρ fixed | 0 | 0.926 | about 9×10⁶ times the clock |
| best mix | | | still 163 |

Assumption: brane scales track M₁₁. Consequence: with an E8-wall Standard Model the radius must be stabilised, with a radion heavier than about 5 meV, which needs a stabiliser near 2.7 TeV (12598), far above the Casimir scale. The electroweak vacuum energy alone gives a 2.7 cm range, too light by about 670 in mass.

Control: D3-like branes have g_s as a third modulus and leave room. `dd_brane_classes.py` extends this to all Dp: with the dilaton free b² = 5/6 for every p, and with it fixed b² = n/(n+1), where n counts small transverse dimensions. So b = 1/√2 is a D7 wrapping the other four. This restates the formula of Pass 12548 for brane classes; it does not predict b. Bubble of nothing: log₁₀ B ≈ 59.5, safe.

## 12594: E8 × anti-E8

Fabinger and Hořava (hep-th/0002073) have the chirality-flipped wall. Each wall keeps its own N = 1 and all supersymmetry breaks non-locally, so **ω = ½ has a discrete origin**, closing the open problem of Pass 12590. Their attractive force and negative cosmological constant are the route C of Pass 12577 in M-theory.

**[E]** Mode sums in units of S: gravity 8, vector 4, hyper −4, so the coefficient is 4(n_H − n_V − 2) = 4(h²¹ − h¹¹) = −2χ. The n_H − n_V − 2 count is standard (hep-ph/0105021 as I recall it, not re-read). I found nothing in the two papers I read connecting it to the dark dimension, and did not search further, so no novelty is claimed.

**Failure of the tempting link.** Witten's critical length is about 10⁻¹⁹ of a 10 μm interval, so G-flux must vanish exactly. That removes the standard embedding, which is what ties generations to |χ|/2. The Casimir coefficient remains −2χ; the link to generations does not. The negative sign the fits prefer needs χ > 0 and so h¹¹ > h²¹, which also adds massless moduli, so massless boson counts are tabulated in `hw_wall_radius.json`.

## 12595, 12601: D3-branes at C³/ℤ₃

Aldazabal, Ibáñez, Quevedo, Uranga (hep-th/0005067). ℤ₃ gives three generations and sin²θ_W = 3/14 at M_s. Control: I reproduce their M_s = 8.3×10¹¹ GeV against 9×10¹¹, and sin²θ_W = 0.2315, and their SM spectrum's wrong-sign 0.204.

**With a dark dimension:** a 10 μm interval caps M_s near 1.2×10⁸ GeV, about 7000 times too low, and their M_s needs R ≈ 3×10⁻¹¹ μm. Unifying at the cap needs extra running of 13.5 and 4.5 units.

**Closing the loop without a dark dimension.** Their result assumes SUSY at 1 TeV. Setting M_SUSY = κ M_s²/M_P:

| κ | M_s (GeV) | M_SUSY (GeV) | sin²θ_W | pull |
|---:|---:|---:|---:|---:|
| 1 | 1.2×10¹¹ | 5900 | 0.2118 | −8.4% |
| 1/16π² | 4.3×10¹¹ | 480 | 0.2281 | −1.3% |
| 0.01 | 3.8×10¹¹ | 600 | 0.2266 | −2.0% |

So sequestering, natural for D3-branes, rescues most of it at one loop but needs M_SUSY near 500 GeV, in conflict with collider limits for coloured states unless spectra are compressed; I did not model this. Extra doublets (ΔB_L = 1, ΔB₁′ = 2 to 3) also restore 0.2315 to 0.2318, at M_SUSY of 300 to 640 GeV.

Other gates at M_s = 1.2×10¹¹ GeV: v²/M_s is 5070 times atmospheric, needing a Yukawa near 0.01; axion misalignment needs θ = 3.25, out of range; volume modulus 0.3 MeV by LVS scaling, a moduli problem; Higgs at 125 GeV has no tree-level tan β solution at M_SUSY = 5.9 TeV (cos²2β would exceed 1 until M_SUSY is near 10 TeV, tan β = 16 there and 3 at 100 TeV, at one loop), so it needs stop thresholds I did not compute; dark energy is 10⁻⁶² of M_SUSY⁴. **Fails.**

## 12596: real DES Y3 shear

`class_des_fit.py`. ξ± with the published covariance and source n(z), shear calibration, photo-z shifts, NLA alignments. Scale cuts are mine: ξ₊ θ > 10′, ξ₋ θ > 60′, 200 data points. The nuisance priors are from memory of Amon and Secco et al and not re-read.

**Control [N].** Shear alone: S8 = 0.789 and χ² = 200.9 on 200 points. Published: 0.759 to 0.776, ± about 0.025. This is a best-fit value against posterior means, so it passes within about 1σ, not tightly.

| Δχ² vs ΛCDM | default cuts | tighter (20′, 100′) |
|---|---:|---:|
| exponential | −2.97 | −2.97 |
| fading | −10.71 | −10.35 |
| radion | −10.65 | not run |
| c′ gain | **7.74** | **7.39** |

Shear χ² is 201.48 for ΛCDM and 201.83 for fading, while S8 rises from 0.810 to 0.827. So the shear data absorb that S8. **The DES tension of Pass 12574 does not appear in the shear likelihood.** Caveats: Y3, not Y6, whose S8 is what Pass 12574 used; 3×2pt is not done, since galaxy clustering and galaxy-galaxy lensing need bias modelling; TATT and baryons are not modelled, and η drifts to 1.1, wider than a typical prior; Halofit on a coupled model, where N-body says under 3 percent at these scales.

## 12597: out of sample, and evidence

`class_holdout.py`. Starts come from the ΛCDM fit trained on the same reduced data. Dovekie.

**SN held out.** ΛCDM: train 628.93, predicts SN at 1635.23.

| Start (c, c′) | Train χ² | Held SN χ² |
|---|---:|---:|
| fading (−0.9, 0.05) | **622.79** | **1629.98** |
| fading (−0.5, 0.08) | 622.98 | 1631.25 |
| fading (0.5, 0.02) | 624.30 | 1633.63 |
| fading (−0.3, 0.01) | 625.83 | 1634.51 |
| exponential, three starts | 628.94 to 659.9 | 1635.22 to 1635.80 |
| CPL, three starts, all converging to w₀ ≈ −0.60, wₐ ≈ −1.2 | 619.93 to 620.30 | 1649.92 to 1652.57 |

**[N]** Better training fits predict SN better, and the exponential has nothing to offer: c falls to about 0. So the SN gain is predicted by the CMB + BAO + lensing + fσ8 preference for the coupling. Limits: the data were not blind; the start (−0.9, 0.05) was chosen knowing roughly where the full optimum is, though the fit itself did not see SN; the landscape has several local minima.

**BAO held out.** ΛCDM: train 2244.87, BAO 36.81. Fading: 2243.90 → 31.28; 2243.91 → 16.02; 2244.45 → 18.93. Training cannot select among these, so this prediction is not unique. A 2245.66 start gave 60.11 and is an unconverged point. Exponential, three starts: 2243.74 to 2243.77 → 32.86 to 33.34. CPL, three starts: 2239.91 to 2240.03 → 15.25 to 16.26, converged.

**Cross-validation total [N]**, held SN + held BAO, taking the lowest-training fit for each model:

| Model | Total | Note |
|---|---:|---|
| ΛCDM | 1672.04 | |
| exponential | 1668.52 | |
| CPL | 1668.64 | good on BAO, 17 worse than ΛCDM on SN |
| fading | 1661.26 | 1646.00 with the BAO fit at nearly equal training χ² (Δ = 0.01) |

So fading wins by 7.4 to 22.6 over CPL and 10.8 to 26.0 over ΛCDM, reversing the in-sample order, where CPL is ahead by 1.2 (`665622ee1`). CPL trained without SN lands at w₀ ≈ −0.6, wₐ ≈ −1.2, far from where SN want it, which is the known DESI + CMB versus SN strain. Limits: point estimates, not posterior predictive; both models have broad posteriors; Dovekie only; not blinded; two folds. The radion was not rerun in neutral form and is expected to follow fading, as it does everywhere else.

**Evidence.** Laplace ln B over ΛCDM: exponential −1.25, fading +0.44, radion +1.26, with flat priors c ∈ 6 wide, c′ ∈ 0.2 wide. The Fisher gives c′ = 0.052 ± 0.008, whereas Δχ² implies about ± 0.017, so the posterior is not Gaussian and the volume is underestimated, by about a factor of 2 per c′ direction. Either way this is weak on any scale, not a detection. The radion's priors on prod and Zn are arbitrary.

## 12598: frozen predictions

`class_prereg_dovekie.json`, sha256 of the model block `186786a84e7f5598110bfdae5e9dc5f5f00da9f41219141500eca6820bde3e90`. Fixed under this commit, before any data newer than those used. Bands come from 24 Fisher draws, with the c, c′ block inflated by 2.

| Observable | ΛCDM | fading | Separation |
|---|---:|---:|---:|
| γ(z = 1.1), ln f / ln Ω_m | 0.5473 | 0.5365 ± 0.0054 | 2.0σ |
| D_H/r_d(0.51) | 22.57 ± 0.05 | 22.34 ± 0.15 | 1.4σ |
| D_H/r_d(0.706) | 20.07 ± 0.03 | 19.89 ± 0.12 | 1.4σ |
| C_L^κκ(1000) ×10⁸ | 1.03 ± 0.016 | 1.075 ± 0.03 | 1.3σ |
| S8 | 0.812 ± 0.007 | 0.831 ± 0.012 | 1.3σ |

Separation is model spread, not a survey's σ. Cross-check: m_DM(rec)/m_DM(today) = 1.014, against 1.0149 from parallel `f98ea2929`.

## 12599: random chains for flavour

Mechanism is prior art: von Gersdorff, arXiv:1705.05430, including shared-chain CKM with N_q ≈ 6 to 8 and short lepton chains, which my scan re-finds. **Not** in that paper by text search: Lyapunov or Oseledets language, the exact exponent ratio, strong CP. Real-determinant strong CP in general is Feruglio et al, arXiv:2406.01689.

**[E]** Exponent ratio r = ln(m₃/m₂)/ln(m₂/m₁): ½ for Ginibre (ψ(3), ψ(2), ψ(1)), 2 for inverse, 1 for any hop symmetric under inversion. Corrected on 1.0 after a precision artefact at span 38 e-folds, which exceeds double precision.

| | lnZ over its grid | best ln L |
|---|---:|---:|
| quarks: chains, by hop type | −11.2 to −12.3 | −8.75 to −9.2 |
| quarks: FN, 3 percent of grid | −10.6 | −5.49 |
| all flavour: chains, 2 integers | −18.0 to −18.6 | −15.6 to −16.2 |
| all flavour: FN 10-5̄, four charges + ε | −18.88 | −13.53 |

No single hop type has both CKM ordering and quark mass ratios: forward gets θ₁₂ < θ₂₃, inverse pushes r to 2, symmetric gives equal angles. Differences in lnZ are under 1, and that is no decision. Two integers do comparably to four charges plus ε, a modest Occam point. Conditioned on all flavour data: normal ordering 98 to 99 percent, Σm_ν ≈ 0.064 eV (68 percent 0.058 to 0.075), m₁ ≈ 1.5 meV. I did not run the same conditional for FN, so these do not discriminate.

## 12600: light cones and gravitons on F_q⁴

Extends the null-history clock of parallel `986795826` and `b47886dac`, whose formula I verified at q = 3, 5, 7, 11, 13.

**[E]** Clock order with N = q^(d−1): 1, q, q, q², q², q³ for d = 2 to 7. N generalises their q² and is my choice, so this is a curiosity and not dimension selection. SRG(81,20,1,6) at (1,3) is prior art, Pass 11831. Signature: for q ≡ 3 mod 4, (1,3) has Witt index 1 and (2,2) has 2, as in real space; for q ≡ 1 mod 4 all signatures have index 2. Euclidean still has null vectors, so the match is partial.

**[E]** Linearised Einstein over GF(p), `finite_graviton.py`, q = 3, 5, 7, 11, 13: exhaustive at q = 3, about 500 samples otherwise, with no Bianchi or gauge failures. Null momenta always give 2 polarisations and massive shells 5.

Helicity: rotations on k^⊥/k have order q + 1 for q ≡ 3 mod 4 and half that in Ω, the finite Lorentz group proper. Helicities ±2 coincide when 4 ≡ 0 mod the order. So at q = 3 they coincide in both, and in Ω a graviton's helicity equals a scalar's. Separation needs q ≥ 7 in SO(2), q ≥ 11 in Ω. Prior art: helicity mod 2 in Pass 11834 and no helicity on the spinor in Pass 11864. The spin-2 corollary and the table are the additions, and the search behind that was limited to those passes and a few neighbours.

## 12602: everpresent Λ

Sorkin's 1987 argument is the one framework that gave the size of Λ in advance. `everpresent_lambda.py`: H₀ emerges per history, with ω_b, ω_m fixed, distances only. Best-fit ΛCDM on the same terms: χ² = 1658.39.

**Light-cone volume, V = ∫a³(4π/3)χ³dt.** Unit-free, so the size is predicted. Zero of 320,000 histories in the h window at α ≤ 1, with early fraction 35 percent at α = 1. At α = 3, 0.7 percent survive and the best is +3640. This is Barrow's objection, gr-qc/0612128, in numbers.

**Comoving volume, V = ∫a³dt.** α = 0.3: early fraction 0.4 percent and 8 percent of histories in the window. But the comoving unit is absorbed in α, so **the size is no longer predicted**. Best of 19,224 histories at α = 0.2 is +46, and ln⟨e^(−χ²/2)⟩ is −37 relative to best-fit ΛCDM. The histories are too jagged for w ≈ −1 at low z. The mean is dominated by rare histories, so −37 is a sample value. Since none as good as ΛCDM appeared among 19,224 in-window draws, the probability of one is below about 10⁻⁴ per in-window history, or about 2×10⁻⁶ per history, a bound of about −13 before any Occam cost for ΛCDM, which is about −5 for a flat Λ prior. I did not implement Zwane et al's exact prescription, so their fit is not refuted directly. No DESI DR2 test of it turned up in one search.

## Parallel commits read

`f98ea2929` through `cc26c15a4`: all non-Claude commits of 3 to 5 November. Dark-sector cross-checks: `665622ee1` CPL better than fading by 1.2, and no holdout run, which this round supplies. `f3593b2ae`: 99.98 percent of c′'s lensing response absorbed by amplitude and tilt, consistent with shear being blind here. `5d6fd1ea5`: exact isometry cannot protect mass and rolling potential; 12593 sharpens the same area.

## Sources

arXiv:hep-th/0002073, 0907.1602, hep-th/0005067, hep-th/0011289, 1705.05430, 2406.01689, 1703.06265, gr-qc/0612128, 2307.13743. DES Y3 public 2pt file at desdr-server.ncsa.illinois.edu.
