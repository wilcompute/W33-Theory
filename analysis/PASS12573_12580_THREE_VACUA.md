# Passes 12573–12580: three vacua, and what survives weak lensing and an N-body

Claude track. Continues `PASS12563_12570_STABILISED_TOWER.md`. Producer: `analysis/w33_pass12573_to_12580_three_vacua.py`. Test: `tests/test_w33_pass12573_to_12580.py`. Drivers in `analysis/toe_uv/`.

**This is not a theory of everything.** The gauge group, generations and strong CP are untouched. All dark-sector versions below give the same evidence over ΛCDM, and how large that is now depends on which weak lensing survey is right.

> **Correction (Passes 12583-12592).** The DES Y6 result below, a c′ gain of 4.0 or 2σ, compared a ΛCDM-derived S8 directly with the model. With the shear-equivalent shift the gain is 6.7, or 2.6σ on Dovekie, on a stand-in survey. The c′ gain also depends on the neutrino mass. See `PASS12583_12592_NEUTRINO_OVERLAP.md`.

## The result in brief

Three versions of the dark-dimension sector fit the data equally well and differ in their vacuum. No data set here separates them; their futures and their extra assumptions do.

| | A: relaxing radion | B: knife-edge | C: gravitino |
|---|---|---|---|
| V | Λ + Z h(x), N_f = 2 massive fermions, starts at the minimum | Z (h(x) − h_min), V_min = 0, no separate Λ | Λ − A R⁻⁴, Scherk-Schwarz twist |
| Full Planck, Pantheon+ | −8.68 | −8.57 (x₀ = 0.6) | |
| Full Planck, Dovekie | −10.86 | −10.98 (x₀ = 0.6) | −10.80 |
| Full Planck, DES-SN5YR | −17.39 | −17.35 (x₀ = 0.6) | −17.47 |
| R (μm) | 8.0 to 8.6 | 9.2 to 10.2 | 13 to 15 at ω ≥ 0.3 |
| New fields | ≥ 2 massive bulk fermions | ≥ 2 massive bulk fermions | none beyond 5D N = 1 supergravity |
| No-AdS₃ | passes | passes | passes at every ω tested |
| Future | settles at V_min > 0 | acceleration ends in 4 to 7.5 Gyr | recollapse in about 8 to 9 Gyr |
| Main conflict | TCC needs another decay channel | V_min = 0 is tuned | runaway to negative V |

Fading on the same likelihood: −8.51, −10.65, −16.95. Column C's numbers are the n = 4 fit of Pass 12562, whose potential has this form. Column B's fits use the x₀ = 0.6 row, the Planck row nearest V_min = 0 (compressed interpolation at V_min = 0 gives −8.23, −10.42, −17.06).

**The data still do not establish a Casimir origin.** The exponent is unmeasured (Pass 12567). All of R, M and the futures are conditional on that reading.

## 12573: a real N-body, which reverses the toy

`nbody_pm.py`: particle-mesh, two species, on the relaxing radion's own background from CLASS. The coupled species feels gravity plus a scalar force 2b² times gravity sourced by its own density, its mass fades with χ(a), and it has a momentum drift b χ_N p. Same seed in every run, so ratios cancel sample variance.

**Controls.**
- Linear limit (initial amplitude × 0.002): low-k species ratio 1.06 to 1.07, against 1.0614 from the linear equations and 1.0617 from CLASS; control 1.008 against 1.0074. Quadrupling the steps changes nothing.
- Control P(k) against CLASS halofit: within 22 percent from k = 0.3 to 2.9 h/Mpc at 100 Mpc/h; low k is one realisation.
- The checks caught a real bug first: the CLASS table runs backwards in a, and np.interp needs it ascending.

**Result**, 96³ particles per species, 192³ mesh, cell 0.13 Mpc/h in the 25 Mpc/h box:

| | L = 100, b = 1/√2 | L = 25, b = 1/√2 | L = 25, b = √(3/2) |
|---|---|---|---|
| coupled mass share | 5.4% | 5.4% | 3.1% |
| share in densest 10% of peaks, 1 cell, relative | 1.18 | 1.21 | 1.37 |
| same, control | 1.01 | 1.01 | 1.01 |
| P_total ratio, largest | +2.1% | +2.9% | +2.9% |
| peak count, control → coupled | 963 → 962 | 616 → 614 | 615 → 617 |

**No runaway.** Peak counts do not change, total power moves by under 3 percent, and the coupled share rises by a modest factor. **I retract the sign of the toy in Pass 12563**, which said the coupled species is expelled by 12 to 25 percent: it used a constant positive χ̇, whereas the true field reverses late. The N-body has it concentrated.

Nonlinear evolution also lowers the low-k species ratio from the linear 1.06 to about 1.02, which real phase mixing should do, and I had not expected.

**Limits.** PM force, so nothing below about 0.13 Mpc/h: this says nothing about cusps, dwarfs or subhalos, where a stronger force on the coupled species matters most. No baryons. One seed. A tree or AMR run remains needed. A P(k) change of 2 to 3 percent at k > 5 h/Mpc may matter for Lyman-α, which I did not test.

## 12574: weak lensing and RSD in the fit

Planck plik-lite + DESI + Dovekie + ACT/Planck lensing + fσ8 from six redshifts, refit, with an S8 prior on or off. These priors assume ΛCDM and are summaries, so this tests size, not a final verdict; fσ8 is diagonal, and its BOSS values are from memory.

| Δχ² vs ΛCDM | no S8 prior | KiDS-Legacy | **DES Y6** |
|---|---|---|---|
| exponential | −2.59 | −2.67 | −2.89 |
| fading | −11.38 | −10.33 | **−6.85** |
| relaxing radion | −11.45 | −10.40 | **−6.62** |
| c′ gain (σ) | 8.8 (3.0) | 7.7 (2.8) | **4.0 (2.0)** |
| S8: ΛCDM → fading | 0.812 → 0.831 | 0.812 → 0.828 | 0.806 → 0.816 |

**This is the sharpest pressure on the whole programme, and it depends on the survey.** With DES Y6 (0.789 ± 0.012) the coupling falls to 2σ, with S8 pulled to 0.816, still 2.2σ from DES. With KiDS-Legacy (0.81) nothing changes much. Any genuine dark-sector signal requires S8 ≈ 0.82 to 0.83, so a settled DES-like S8 would largely remove the case for it. A proper 3x2pt likelihood for these models is the needed next step: the species do not trace each other, and the prior assumes they do.

fσ8 adds about 1 in the coupling's favour: χ² ≈ 6 on 6 points for every model, so it does not discriminate. ΛCDM itself is 1.4σ from DES here, so part of the tension is not new.

## 12575: V_min = 0, the knife-edge

V(χ) = Z (h(x) − h_min). No-AdS₄ wants V_min ≥ 0, the strong dS conjecture wants V_min ≤ 0, and this is the only point satisfying both. It is a slice of the x₀ family, so no new fit is needed: compressed, Δχ² = −8.23, −10.42, −17.06, with x₀ = 0.65, 0.63, 0.59.

R = 9.2 to 10.2 μm and M ≈ 12.7 meV. Dark energy today is the radion's height above zero, with slope |V′/V| = 1.1 to 1.6, the order the dS conjecture asks for. **Acceleration ends 4 to 7.5 Gyr from now**, from the row nearest V_min = 0.

**What it does not do.** Why V_min is exactly zero is the cosmological constant problem restated, in terms of bulk and brane counterterms. It removes Λ as a free number only by assuming that zero. Rows nearest zero have |V_min| up to 0.06, and a turnaround at 56 or 84 Gyr on the negative side shows the slice is sharp in that outcome only.

## 12576: V_min > 0 cannot decay along the radion

V → +∞ at small x and V → Λ > V_min at large x, so version A's minimum is global along the radion. TCC limits its life to (1/H) ln(M_Pl/H), about 2,800 to 3,100 Gyr, with ln(M_Pl/H) = 139. So A needs an unidentified decay channel, or it violates TCC.

## 12577: Scherk-Schwarz gravitini

The natural origin for fermions at M ~ 1/R. Spectrum on an interval: 4 massless bosons (graviton 2, radion, axion), 8 at n/R; fermions 4 at |n + ω|/R. This spectrum is my assignment, level-matched at ω = 0, not derived from an orbifold calculation here, and arXiv:2301.07719 discusses the embedding for the dark dimension.

| ω | N_eff | R (μm) | gravitino (meV) | m₁ bound (meV) |
|---|---|---|---|---|
| 0.5 | 15.5 | 14.8 | 6.7 | 11.2 |
| 0.3 | 10.6 | 13.4 | 4.4 | 11.5 |
| 0.1 | 1.70 | 8.5 | 2.3 | 12.9 |
| 0.02 | 0.073 | 3.9 | 1.0 | 14.1 |

**No AdS₃ at any ω tested**, because bosons and fermions cancel on short circles, with no new matter added. V_C is negative for every ω, which is the sign the fit prefers. The two extra massless bosons sit at the limit Pass 12539 allows; the radion's Hubble-scale mass and any axion mass were ignored, which is conservative.

**The price.** V_C is exactly R⁻⁴, so there is no minimum, and it runs to negative V at small R. Recollapse from Pass 12562 returns on this route, conditional on the form of V holding at smaller R. Whether SUSY breaking at about 5 meV in the bulk is consistent with the brane is not addressed.

## 12578: the coupled fraction from brane production

Using eq. (3.14) of arXiv:2209.09249: ρ̇ ∝ T⁸ R/M_P², so f ∝ R Tᵢ³. **Control: all dark matter at R = 1 μm needs Tᵢ = 3.97 GeV, against their 4 GeV.** (One symbol in the rate was garbled in the PDF extraction, and I assumed π², which that agreement supports.)

At R = 8.5 μm, f = 0.08 needs Tᵢ = 0.84 GeV, while their natural scale Tᵢ ~ 1 GeV gives f = 0.14. **So a fraction near 0.1 is what a micron-scale dimension and that scale give, when the 4 GeV of all dark matter is not assumed.** It is not a prediction, since f ∝ Tᵢ³ and "1 GeV" is an order-of-magnitude estimate, but the fraction is no longer arbitrary. The rest of the dark matter stays unidentified.

## 12579: the volume modulus

Brane matter couples to it at about gravitational strength, so its range must lie below short-range limits: μ ≥ 6.6 meV for 30 μm, a stabiliser scale √(μ M_Pl) ≈ 4 TeV. That is a scale estimate, not a construction, and it is well below M_D, so it is not implausible. The model has this scale and meV-scale physics side by side, unexplained.

## Standing

| Label | Claim |
|---|---|
| [E] | Massive and twisted Casimir sums; V_min = 0 slice |
| [N] | N-body results in the stated range; all fits, as local optima |
| [N] | c′ gain 8.8, 7.7, 4.0 under no S8, KiDS, DES priors on Dovekie |
| [I] | Coupling of each vacuum to conjectures; gravitino spectrum; volume modulus scale |
| [C] | R, M, x₀ and each future: conditional on Casimir origin and on the conjectures |

**Retractions.** The toy's expulsion (Pass 12563). "Lensing and RSD add little": DES Y6 does not.

**Prior art.** Scherk-Schwarz in the dark dimension is arXiv:2301.07719's. Production is arXiv:2209.09249's. Recollapse is Luu, Qiu and Tye's. Novelty of the combination is not claimed; the search was narrow.

**Gaps.** No 3x2pt likelihood. No small-scale N-body. No Lyman-α. Gravitino spectrum not derived. One sample for the growth fits.

## Sources

arXiv:2209.09249, 2301.07719, 2512.20570, 2507.03090, 2601.14559 (DES Y6), 2503.19442 (KiDS-Legacy), 2007.08993 (eBOSS), 2506.24011. Parallel track: `f3593b2ae`, `b2f605041`.
