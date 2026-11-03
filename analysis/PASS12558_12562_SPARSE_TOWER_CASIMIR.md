# Passes 12558–12562: the sparse tower, its Casimir energy, and what the data do not say

Claude track. Continues `PASS12550_12557_DARK_MATTER_DRAG.md`. Producers: `analysis/w33_pass12558_to_12559_sparse_tower.py`, `analysis/w33_pass12560_to_12562_casimir_tower.py`. Tests: `tests/test_w33_pass12558_to_12559.py`, `tests/test_w33_pass12560_to_12562.py`. Drivers in `analysis/toe_uv/`.

**This is not a theory of everything.** Gauge group, generations, Λ and strong CP stay unexplained. Λ is put in by hand below, and that is the cosmological constant problem, untouched.

## The result in brief

A dark sector can be written with nothing but a constant Λ, the Casimir energy of the dark dimension, and about 7 percent of the dark matter on the KK tower:

V(χ) = Λ + Z exp(−4bχ), m_tower ∝ exp(−bχ) on a fraction f of the dark matter.

With the same number of extra parameters as the fading fit, on full Planck spectra with both fluids evolved, it fits as well or slightly better: Δχ² = −10.8 against −10.7 on Dovekie, −17.5 against −16.9 on DES-SN5YR. The negative sign, which massless bosons give, is preferred by 3.2 and 5.4.

**The data do not establish that this term is Casimir.** Freeing the exponent gives a flat curve, so the fit measures a local slope, and ε is largely c relabelled. Everything that follows from "it is Casimir" (R ≈ 13 μm, recollapse) is conditional on that assumption. No detection is claimed, and the preference over ΛCDM is the same 2.5 to 3σ-level preference as before.

## 12558: full Planck on every sample

Planck plik-lite + τ prior + DESI DR2, with CLASS patched as in Pass 12550. Δχ² against scalar-field ΛCDM; CPL against native ΛCDM.

| | DESI + CMB | Pantheon+ | Dovekie | DES-SN5YR |
|---|---|---|---|---|
| fading, c < 0 | −5.4 | −8.5 | −10.7 | −16.9 |
| fading, c > 0 | −3.8 | −6.8 | −8.4 | −13.8 |
| CPL | −9.5 | −8.9 | −12.3 | −19.6 |
| c′ gain over c′ = 0 | 5.4 | 6.1 | 6.9 | 8.4 |
| same, σ | 2.3 | 2.5 | 2.6 | 2.9 |
| Casimir line c = 4c′, cost | 0.03 | 3.5 | 5.4 | 10.9 |
| S8, ΛCDM → fading | 0.804 → 0.835 | 0.806 → 0.832 | 0.807 → 0.833 | 0.809 → 0.837 |

Both branches match Table I of arXiv:2507.03090 within 0.1 in c and 0.01 in c′ on every sample.

**Two corrections to my own numbers.**

- **The exact symmetry φ → −φ at c′ = 0** makes the two exponential fits equal, so their difference measures my optimiser's scatter: up to 1.8. The better branch is now the reference.
- **Lensing.** With that reference, the post hoc lensing-included c′ gain is 6.5, 7.4, 8.0, 8.7 across samples: 2.6 to 3.0σ. The "9.7, about 3.1σ" of Pass 12551 was the top of the range, and the parallel track cited it (`aae4f41f5`). Their later finding that 99.98 percent of the squared lensing response is absorbed by A_s and n_s (`f3593b2ae`) means even this may shrink under a proper refit. I did not refit.

**The Casimir tension comes from supernovae.** On DESI + CMB alone the line costs 0.03; c is set by supernovae while c′ is not.

## 12559: joining the drag to the loops

The parallel track's `aae4f41f5` shows a 4D particle with c′ ≈ 0.05 needs m ≲ 0.017 eV if its Coleman-Weinberg curvature is not to exceed H₀², and it says that a regulated KK tower is out of scope. Reproduced here to 1e-10, as a control.

**The tower.** Direct mode sum with the local bulk term subtracted gives V = −3ζ(5)/(4π²ℓ⁴) per real massless degree of freedom, to 1e-12, with m_KK = 2π/ℓ: no m_n⁴ survives, whatever level the dark matter occupies. Without the subtraction the integral grows without limit, which is the control. This textbook result is the point: the tower's loops are finite because of 5D locality.

**The clash.** V ~ m_KK⁴ has curvature 16b²V along ∇ln m. If |V| ≤ ρ_DE, then μ ≤ 4b√(3Ω_DE) H₀, which is 4.1 to 7.0 H₀: exactly the Hubble mass the drag excludes, and short of μ ≥ 1e5 H₀ by 1.4e4 to 2.5e4.

| route | drag (b5b4db003) | loops (aae4f41f5, here) |
|---|---|---|
| all DM on tower, free modulus | excluded | natural |
| all DM on tower, heavy modulus | passes at μ ≳ 1e5 H₀ | tower supplies 4 to 7 H₀; extra sector, about 0.6 to 1.9 eV, tuned by 5e9 to 5e11 |
| all DM a 4D particle, b large, heavy modulus | passes | m ≲ 1.5 to 4.7 eV at μ = 1e5 to 1e6 H₀ (Dirac) |
| **sparse tower, f b = c′, free modulus** | **passes** | **natural** |

**Two fluids on full Planck.** Coupled fraction in `cdm`, the rest in CLASS's `idm` fluid with interactions off. f = 1 through this route returns the direct fit within 0.1.

| f b = 0.05 | Dovekie | DES-SN5YR |
|---|---|---|
| single-field fit | −10.65 | −16.95 |
| b = 1/√2, f = 7.1% | −10.21 | −16.40 |
| b = √(3/2), f = 4.1% | −9.64 | −15.66 |
| b = 1/√2, f = 30% | +396 | +424 |

The product f b is what the data fix: 0.03 and 0.07 are worse than 0.05. S8 falls by 0.008 to 0.011 against the fully coupled fit, a possible discriminator. The coupled fluid leads the uncoupled one by 5 percent today at k = 0.2/Mpc, down from 9 percent at a = 0.02. I expected the lead to grow; the field's late reversal is the suspected cause, not verified.

**The motion is large.** At b = 1/√2 with V off the χ axis, m_KK falls by Δln m = −0.31 from recombination to today. The neutrino null of Pass 12557 used the fully coupled 1 percent, and it does not transfer to this route.

## 12560: what produces c′

Dropping each DESI bin, refitting (compressed CMB, background).

| dropped | gain, no SN | c′ | gain, Dovekie | c′ | held-out χ², ΛCDM → fading, no SN |
|---|---|---|---|---|---|
| none | 5.3 | 0.051 | 6.4 | 0.050 | |
| 0.295 | 5.3 | 0.051 | 6.2 | 0.050 | 0.01 → 0.01 |
| 0.510 | 5.2 | 0.051 | 7.1 | 0.052 | 3.7 → 4.2 |
| **0.706** | **2.6** | **0.043** | **4.0** | **0.045** | **6.8 → 4.3** |
| 0.934 | 6.4 | 0.057 | 6.0 | 0.051 | 1.7 → 3.9 |
| 1.321 | 5.4 | 0.052 | 6.2 | 0.050 | 0.6 → 0.7 |
| 1.484 | 5.6 | 0.052 | 6.6 | 0.051 | 0.5 → 0.8 |
| 2.330 | 5.4 | 0.051 | 6.4 | 0.050 | 0.03 → 0.12 |

**c′ survives losing any one bin, but about half of its no-SN gain rests on z = 0.706.** Held out, fading predicts that bin better than ΛCDM; it predicts z = 0.934 worse. A mixed holdout, not a success. A systematic in one DESI redshift bin would matter here.

## 12561: losing mass is not the signal

Λ + decaying cold dark matter into dark radiation, with the same parameter count: −1.9 on Dovekie, −1.0 on DES-SN5YR, against −10.2 and −16.5. Control: Γ = 0 returns ΛCDM. Best fits sit near the edge of my Γ range, and warm decay products are not modelled, so this excludes only this form. It does say that fading's gain is not just "dark matter lost 1.3 percent of its energy".

## 12562: Λ + Casimir + sparse tower

Compressed CMB, background; `casimir_fast.py` agrees with the general solver to 6e-7, after that same control caught a wrong start time and an unclosed budget in my first version.

| b = 1/√2 | Pantheon+ | Dovekie | DES-SN5YR |
|---|---|---|---|
| fading, c < 0 | −8.4 | −10.2 | −16.5 |
| **negative Casimir** | **−8.2** | **−10.6** | **−17.4** |
| positive Casimir | −7.6 | −8.8 | −13.8 |
| no Casimir | −2.8 | −2.5 | −2.0 |
| ε = V_C/ρ_crit | −0.29 | −0.32 | −0.41 |
| f | 8.0% | 8.3% | 8.5% |
| Δln m_KK, recombination to today | −0.18 | −0.18 | −0.16 |
| w_φ today | −0.88 | −0.85 | −0.78 |

Results barely change for b from 1/√2 to √(3/2). **Full Planck, two fluids:** negative −10.80 (ε = −0.30), positive −7.63 on Dovekie; negative −17.47 (ε = −0.40), positive −12.03 on DES-SN5YR. Compressed and full ε agree, and the sign preference widens from 1.7 and 3.5 to 3.2 and 5.4. Post hoc lensing χ² is 20.2 and 20.6, against 20.2 and 20.4 for fading, so lensing does not separate them; S8 is 0.833 and 0.839. At b = 1 on DES-SN5YR the fit reaches −17.73.

**Why this form is natural to try.** The fit's better c < 0 branch has V rising as the tower mass falls, which is exactly what −|A| m_KK⁴ does, and massless bosons give the minus sign. The drag pushes χ up early; the Casimir slope pushes it back late, giving the reversal the c < 0 fits show.

**Why c/c′ is not 4.** c_eff/c′ = 4(|ε|/V_today)/f, an identity, checked numerically. With f = 1 and all dark energy Casimir it gives 4; with f ≈ 8 percent and a sub-dominant Casimir term, the fit's ratio is 22 to 32. This resolves Pass 12548's "13 to 15, not 4" in form, though the instantaneous c_eff here (−1.3 to −1.9) is larger than the constant fitted c (−0.85 to −1.04), so the match is rough.

**The test it fails to pass: the exponent.** V_C ∝ exp(−nbχ), n free.

| n | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 12 |
|---|---|---|---|---|---|---|---|---|
| Pantheon+ | −8.26 | −8.24 | −8.22 | −8.20 | −8.17 | −8.14 | −8.09 | −7.94 |
| Dovekie | −10.30 | −10.39 | −10.47 | −10.55 | −10.62 | −10.68 | −10.80 | −10.85 |
| DES-SN5YR | −16.85 | −17.03 | −17.20 | −17.35 | −17.48 | −17.60 | −17.80 | −18.06 |

**Flat, and 4 is not a minimum.** n|ε| changes far less than ε, so the data see a local slope. "Slope fixed by geometry" is true of the model and earns no evidential credit from these data. I had called this a possible measurement of the Casimir law; it is not one.

**Conditional on it being Casimir, with n = 4:**

- **Radius.** |V_C| = N (3ζ(5)/64π⁶)/R⁴ gives, for the 5 graviton degrees of freedom, R = 12.7 to 13.8 μm, and 12 to 15 μm across the Δχ² ≤ 4 range of ε. R ∝ (N/|ε|)^(1/4), so the agreement between samples is mostly that weak power and is weak evidence. N = 1 to 20 moves it by about 1.5 either way; an interval instead of a circle halves N. The gravitational-strength limit stops at λ = 38.6 μm (Lee et al. 2020), and levitated spheres reach a strength of about 1e6 near 10 μm (arXiv:2412.13167), so a gravity-strength force at 13 μm is untested. **That is the falsifiable statement. Reaching it needs a large improvement in short-range experiments.**
- **Future.** χ_N < 0 today: the field has turned back towards smaller radius, where V_C is unbounded below. V crosses zero 4.6 to 6.2 Gyr from now and expansion stops 7.6 to 9.1 Gyr from now (b = 1/√2). The positive branch and the Z = 0 control never turn around. This extrapolates the potential outside the fitted range and depends on n. Recollapse from negative vacuum energy with DESI is prior art: Luu, Qiu and Tye, JCAP 2025, arXiv:2506.24011, expansion stopping near 25 Gyr; mine is near 21 to 23 Gyr of cosmic age, from a different model.

**Conflict.** My own Pass 12539 found that a graviton tower alone gives AdS₃, so under no-AdS₃ a dark dimension needs bulk fermions. Massless periodic bulk neutrinos would flip the net sign and are excluded at R ≈ 13 μm by oscillations (R ≲ 1 μm, arXiv:1101.0003). So the negative branch, with its R, conflicts with the same swampland programme the scenario rests on. [I] A possible way out, not computed: massive bulk fermions with mR ≳ 1 are exponentially suppressed on the dark circle but still act on short circles, where no-AdS₃ bites. The positive branch has no such conflict, at a cost of 3.2 to 5.4. Pass 12534's Dirac neutrino window assumed bulk neutrinos, and it is lost at this R.

**Fixed volume.** Cassini excludes a pure radion if brane matter tracks M_D, so the usable range is the fixed-volume b from 1/√2 to 1, which requires the volume modulus heavy. That stabilisation is assumed. So is the fraction: nothing here says why f ≈ 8 percent or what the other 92 percent is. Primordial black holes are discussed in dark-dimension work; I have not tested that.

## Standing

| Label | Claim |
|---|---|
| [E] | Casimir sum; c_eff/c′ identity |
| [N] | All fits, on the stated likelihoods; local optima, scatter up to 1.8 |
| [N] | Flat exponent: the data do not measure n |
| [I] | The identification of the c < 0 branch with a negative Casimir term: consistent, not demonstrated |
| [C] | R ≈ 13 μm and recollapse: conditional on n = 4 and Casimir origin |

**Prior art.** The Casimir radion potential with a DM coupling and a phantom-looking crossing near z ≈ 0.4 is Katayama et al., arXiv:2603.19819, who build a positive potential from extra bulk fields and compare with DESI BAO, with no likelihood fit and c_DM free. Mantry and Furuuchi, arXiv:2610.35124, relate R to dark energy through a 5D quintessence potential. Amendola 2000 owns the fixed point. **What I did not find in these or in my searches:** constant Λ + negative Casimir as the fitted model, the sparse tower, or a joint fit giving ε. That search covered a handful of papers and queries, so novelty is not claimed.

**Gaps.** plik-lite. Lensing post hoc, and possibly absorbed under a refit. No nonlinear structure for a 7 percent component with a force of order gravity on itself: this is the most obvious way for the sparse tower to die. Massive bulk fermions not computed. Λ unexplained.

## Sources

arXiv:2507.03090, 2603.19819, 2610.35124, 2506.24011, 2307.11048, 2002.11761, 2412.13167, 1101.0003, hep-ph/0201128. Parallel track: `aae4f41f5`, `f3593b2ae`, `5d6fd1ea5`.
