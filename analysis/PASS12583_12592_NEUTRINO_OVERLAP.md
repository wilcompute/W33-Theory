# Passes 12583–12592: the coupling overlaps the neutrino-mass anomaly

Claude track. Continues `PASS12573_12580_THREE_VACUA.md` and corrects one of its headline results. Producer: `analysis/w33_pass12583_to_12592_neutrino_overlap.py`. Test: `tests/test_w33_pass12583_to_12592.py`. Drivers in `analysis/toe_uv/`.

**This is not a theory of everything.** The gauge group, generations and strong CP are untouched. These passes change how much evidence the dark-sector coupling has and what it may be mixed up with. They do not measure a Casimir origin: the exponent is still unmeasured (Pass 12567).

## The result in brief

1. **The coupling c′ and the "negative neutrino mass" anomaly are partly the same signal.** The c′ gain is 4.25, 8.79, 16.23 at Σm_ν = 0.01, 0.06, 0.12 eV. Half of the gain at 0.06 eV goes away if the mass is allowed to be unphysically low. Oscillations require Σm_ν ≥ 0.059 eV, so at allowed masses the gain is at least about 8.8.
2. **The DES Y6 penalty of Pass 12574 was overstated.** A ΛCDM analysis of these models' shear returns an S8 lower by about 0.012, so the c′ gain under DES is 6.7, not 4.0. This is a Limber equivalence on a stand-in survey, not a 3x2pt likelihood.
3. **Massive hypermultiplets join the gravitino route to a minimum.** N_H ≥ 3 at twist ω = ½ fits as well as fading, on compressed CMB, has no AdS₃ at the four points tested, and is a true joint minimum in radius and twist. Its open problem is the twist mass, about H₀.
4. **Controls and nulls.** N-body convergence to 31 kpc/h: no runaway. Lyman-α: no help, no harm. Cluster gas fraction: too small to test today.

## 12583: shear-equivalent S8

An S8 prior assumes ΛCDM. `class_shear_equiv.py` builds DES-like tomographic shear by Limber for each model, with the true fading matter density in the lensing kernel, and fits it with the ΛCDM family on a Gaussian mock covariance.

| S8 equivalent − S8 true | Dovekie | DES-SN5YR |
|---|---:|---:|
| ΛCDM control | −0.0001 | −0.0001 |
| exponential | −0.0047 | −0.0064 |
| fading, c < 0 | −0.0124 | −0.0154 |
| fading, c > 0 | −0.0122 | −0.0156 |
| relaxing radion | −0.0120 | −0.0163 |
| relaxing radion with the N-body P(k) ratio | −0.0130 | −0.0173 |

The ΛCDM family absorbs the shape, with residual χ² under 0.6, so a survey would not flag the model as a bad fit at this level. **[N]**

**Not modelled:** the real n(z), intrinsic alignments, baryons, photo-z and shear nuisances. n(z) is four Gaussians. The direction is robust because growth is later in these models. The size is not established.

## 12584, 12587: DES with the shift, and a second supernova sample

Δχ² against ΛCDM. The shift in the fit is held at the Dovekie values, which are smaller than the DES-SN5YR ones and do not grow with c′.

| | Dovekie: no S8 | DES | **DES shifted** | DES-SN5YR: no S8 | DES | **DES shifted** |
|---|---:|---:|---:|---:|---:|---:|
| exponential | −2.59 | −2.89 | −3.84 | −6.71 | −7.16 | −8.12 |
| fading | −11.38 | −6.85 | **−10.56** | −17.25 | −12.09 | **−16.10** |
| relaxing radion | −11.45 | −6.62 | **−10.20** | −17.52 | −11.98 | **−15.84** |
| c′ gain | 8.79 | 3.96 | **6.71** | 10.54 | 4.93 | **7.98** |

**Correction to Pass 12574.** "DES Y6 cuts the c′ gain to 2σ" came mostly from reading a ΛCDM number as if it applied to these models. The better estimate is 2.6σ on Dovekie and 2.8σ on DES-SN5YR as local Δχ². Fading is still 1.6σ high against DES after the shift, S8 χ² 2.48. **[N, conditional on the stand-in survey]**

## 12585: N-body convergence

Coupled share in the densest tenth of peaks at the one-cell scale, all at 192³ cells:

| Box (Mpc/h) | Cell (kpc/h) | b = 1/√2 | b = √(3/2) |
|---:|---:|---:|---:|
| 100 | 521 | 1.18 | |
| 25 | 130 | 1.21; seed 77: 1.24 | 1.37 |
| 6 | 31 | 1.20 | 1.31 |

The control stays near 1 and peak counts move by under 1.5 percent. No runaway to 31 kpc/h. **[N]** The 6 Mpc/h box lacks large-scale modes, and no baryons are included.

## 12586: Lyman-α

Goldstein et al's compressed eBOSS point, Δ²_L = 0.310 ± 0.020, n_L = −2.340 ± 0.006, in the fit:

| | Δχ² | Lyα χ² | Δ²_L | n_L |
|---|---:|---:|---:|---:|
| ΛCDM | 0 | 18.67 | 0.341 | −2.3144 |
| exponential | −2.85 | 18.24 | 0.341 | −2.3147 |
| fading | −11.41 | 18.68 | 0.357 | −2.3141 |
| relaxing radion | −10.03 | 20.32 | 0.362 | −2.3130 |

The slope tension is an existing ΛCDM one (Rogers and Poulin 2311.16377), and the coupling leaves the slope alone. **My hope that it would help is not supported.** **[N]** The prediction uses linear P(k) at z = 3 and takes the compression as valid for this model.

## 12588–12590: gravitino route with hypermultiplets

Gravity contributes −8S(ω, 0) and each hyper +4S(ω, x). N_H ≥ 3 makes V_C positive at small x, which gives a minimum, as in the massive-hypermultiplet stabilisation of hep-th/0209178, here applied to the dark dimension. Compressed CMB only, ω = ½, Dovekie; DES-SN5YR in the last column:

| N_H | x_i/x_min | Δχ² | x₀ | R (μm) | M (meV) | V_min / ρ_crit | Turnaround | Δχ², DES-SN5YR |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1.0 | −10.27 | 0.458 | 11.05 | 8.2 | +0.48 | none | −16.78 |
| 3 | 1.35 | −10.42 | 0.618 | 13.07 | 9.3 | −0.06 | 54 Gyr | −17.10 |
| 3 | 3.0 | −10.54 | 1.373 | 14.88 | 18.2 | −14.9 | 9.6 Gyr | −17.33 |
| 8 | 1.0 | −10.37 | 0.906 | 13.42 | 13.3 | +0.44 | none | −16.99 |

Fading on the same likelihood: −10.19 and −16.46. The whole grid sits at R of 10–15 μm, and it does not discriminate: all differences are under 1.

**No-AdS₃ [N].** All four rows tested pass with massless m₁, on a further circle, with the lightest Dirac neutrino in normal ordering bounded at 10.3, 10.7, 10.9 meV on Dovekie and 9.9 meV on DES-SN5YR. So **Σm_ν is 0.059 to 0.076 eV**, conditional on the conjecture, Dirac masses and this spectrum. Inverted ordering is not in this code path and was not tested here. Scope: a bounded scan of four points, cut from 24 for run time.

**Joint vacuum [N].** ω is a modulus unless fixed discretely, and I had set it by hand. For every N_H, ω = ½ at x_min has both Hessian eigenvalues positive and is the only local minimum on the (x, ω) grid. Control: gravity alone gives ω = ½ at every radius. At small radius ω = 0 wins for N_H ≥ 4, where V = 0 and supersymmetry returns at this order, so the vacuum has a basin, not a global attractor.

**The open problem.** The twist's mass is about 3.4 H₀ at κ = 1, and κ is a stand-in for a Kähler metric I did not derive. If so, the twist has only recently begun to move, so ω = ½ today needs a discrete origin such as an S¹/(Z₂×Z₂′) boundary condition, or a lucky start. **[I]** The hyper mass M ≈ 1/R is also an input, and hypers need not share the tower's production: no brane coupling is assumed.

## 12591: gas fraction

Baryons do not fade, so f_b(z) is a direct clock on the dark matter mass. Relative to z = 0.1, with the ΛCDM best fit as reference. Control: ΛCDM returns 1.

| z = 1.1 | f_b | Distance factor D_A^(−3/2) | Apparent |
|---|---:|---:|---:|
| fading | +0.62% | +1.63% | +2.26% |
| relaxing radion | +0.50% | +1.77% | +2.28% |

f_b is *higher* at high z, opposite to the naive word "fading": at these low redshifts in the c < 0 fit, the field has turned around and dark matter gains mass toward today. Mantz et al 2111.09343 report about 3 percent intrinsic scatter in distance per cluster, so this looks marginal now. I did not fit their data. **[N for the signal, I for the assessment]**

## 12592: neutrino mass

Massive neutrinos add late matter and suppress lensing, and DESI + CMB prefer the opposite, an effective mass below zero. One massive state, plik-lite + τ prior + DESI + ACT/Planck lensing + fσ8 + Dovekie:

| Σm_ν (eV) | ΛCDM χ² | exponential | fading | relaxing radion | c′ gain | c′ |
|---:|---:|---:|---:|---:|---:|---:|
| 0.01 | 2260.07 | 2256.10 | 2251.85 | 2251.82 | **4.25** | 0.047 |
| 0.06 | 2263.97 | 2261.37 | 2252.59 | 2252.52 | **8.79** | 0.052 |
| 0.12 | 2271.59 | 2270.30 | 2254.07 | 2253.91 | **16.23** | 0.061 |
| 0.25 | 2296.85 | | 2257.77 | | | 0.076 |

**Control [N].** The 0.06 rows return the earlier fits within 0.01. A parabola gives ΛCDM −0.073 ± 0.052 eV, 2.59σ from 0.06. Pulido-Hernández and Cervantes-Cota 2603.13208 report 2.59σ on Planck, ACT, DESI and these supernovae. Their likelihood differs, so agreement to the digit is partly chance. Elbers et al 2503.14744 give −0.101 for DESI + CMB without supernovae. I did not run that case.

**Result [N].** The pull toward low mass is weaker by a factor of 5.2, 5.2, 6.2 at 0.06, 0.12, 0.25 eV. DES-SN5YR agrees, 3.7 over 0.01 to 0.12. A parabola for fading gives −0.20 ± 0.16 eV, 1.6σ from 0.06, but this profile is close to linear, so that vertex is poorly determined and the slope is the safer statement.

**Where it comes from.** Going from 0.01 to 0.25 eV, ΛCDM BAO goes 12.0 → 22.2 and the τ prior 0.7 → 10.6. In fading, BAO stays at 9.1 and τ reaches 1.2. Suspected mechanism, not tested: the fifth force raises lensing and growth while neutrinos lower them, S8 falling from 0.837 to 0.814. **[I]**

**With the shifted DES prior:**

| Σm_ν (eV) | ΛCDM | fading |
|---:|---:|---:|
| 0.01 | 2265.39 | |
| 0.06 | 2266.77 | 2256.21 |
| 0.12 | 2272.28 | 2256.33 |
| 0.25 | | 2258.34 |

Fading is flat to 0.12 eV, where the gain over ΛCDM is 15.95. So the mass and the S8 pressure pull the same way here. The fixed shift is conservative at higher c′.

**What this means, both ways.**
- Reading against the coupling: c′ is not independent of the neutrino anomaly, so the two cannot be counted as separate evidence. If the anomaly goes away for a mundane reason, such as τ or a CMB systematic, part of the c′ gain could go with it. The 4.25 at Σm_ν = 0.01 eV is the part that does not overlap in this test, and it is about 2σ.
- Reading for it: c′ gives a route to the anomaly with allowed positive masses. Inverted ordering at about 0.10 eV is no longer pressed by cosmology here.
- **Joint statement, conditional:** no-AdS₃ on this spectrum wants 0.059–0.076 eV, and ΛCDM sits about 2.6σ from that range by the parabola, where fading is flat within 1 in χ². That is a better fit, not a proof that the coupling is needed.

**Kill list.** JUNO finding inverted ordering excludes this no-AdS₃ route, not fading. Σm_ν ≥ 0.1 eV from a laboratory would exclude the route as well. A future lab mass above 0.25 eV presses fading too.

**Prior art, no novelty claimed.** Li et al 2606.05005 already find that interacting dark sectors shift the neutrino bound, by model, and 2603.13208 treats curvature and w₀wₐ. What I have not found is this c′-gain-versus-mass table for this coupling, but my search was limited. The corpus has no earlier cosmological test of this: `git grep` for gas fraction, effective neutrino mass and negative neutrino mass gave one leptogenesis file, which I did not open.

**Limits.** Six Gauss-Newton iterations per point, no posterior, and no marginalisation. CLASS cannot use a negative mass, so all sub-zero numbers are extrapolations. One massive state stands in for three. The c′ gain at fixed mass is a local Δχ², with no look-elsewhere correction.

## Parallel commits read

`7749ee259`, `36e52b0a4`, `c278d0c40`, `6ef47cdb5`, `7dde67be4`, `6816ebb73`, `2f3791d0d`, `1ccd113da`: W33 subdivision, C3 frames, cycle constraints, E6 vectorlike CP, flux Ramsey, tomotope and Reye, Peres contextuality, 25 inscribed 24-cells and PG(3,4), temporal Choi, two-E8 glues, A5 intertwiners, Euclidean and Lorentzian simplices. None touches the dark sector. `7749ee259` states it does not import this cosmology, and that is correct: nothing in these passes supports W33 physics or the reverse.

**One cross-boundary note.** `36e52b0a4` corrects the KO argument of `analysis/w33_spacetime_dimension_from_KO.py` to dim M ≡ 4 mod 8, not exactly 4. A 5D bulk fails that congruence as it stands, 5 + 6 ≠ 2 mod 8. This need not be a contradiction if the finite triple lives only on the 4D brane and the bulk carries gravity and neutral hypers with no finite part, which is the layout used here. **[I]** So the two tracks are compatible only with that layout, and no map between them is built.

## Claim labels

| | |
|---|---|
| [E] | V(ω = 0) = 0 and the symmetry ω → 1 − ω |
| [N] | shifts of 12583; tables of 12584–12592 |
| [I] | fifth-force mechanism for the neutrino relief; discrete origin of ω; brane-only KO layout; gas-fraction assessment |
| [C] | R, M, m₁ and Σm_ν windows: conditional on the Casimir reading, the conjecture and the spectrum |

## Sources

arXiv:2503.14744, 2603.13208, 2606.05005, 2303.00746, 2311.16377, 2111.09343, 2601.14559, 2503.19442, 2507.03090, 2301.07719, hep-th/0209178, hep-th/0310190, hep-th/0504002, hep-ph/0402143.


> **Correction (Pass 12632, 2026-11-08).** The shear-equivalent S8 shifts in Pass 12583 used CLASS halofit, which mishandles scalar-field dark energy. Patched, the shifts are smaller by 30-46%: fading c<0 -0.0083, not -0.0124; relaxing radion -0.0082, not -0.0120. The "c' gain under DES 6.7, not 4.0" lies in between (about 5.8 if the gain is linear in the S8 shift; not refitted). See `analysis/PASS12632_HALOFIT_SCF_BUG.md`, addendum 5.
