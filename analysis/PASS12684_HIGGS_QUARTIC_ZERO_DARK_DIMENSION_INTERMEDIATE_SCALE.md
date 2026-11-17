# Pass 12684: the Higgs quartic zero is not at the dark dimension's species scale; the top mass picks the intermediate scale √(v M_Pl) (not significant alone)

Claude track. Research-driven pass, outside W(3,3). **Not a theory of everything.** Script: `toe_pass12684_higgs_criticality_dark_dimension.py`; certificate: `data/toe_pass12684_higgs_criticality_dark_dimension.json`.

## Question

Two scales sit suspiciously close together, and Montero–Vafa–Valenzuela ([arXiv:2205.12293](https://arxiv.org/abs/2205.12293)) remarked on this qualitatively:
- the dark dimension's species scale, M̂ ~ Λ^{1/12} M_Pl^{2/3} ~ 10⁹–10¹⁰ GeV, i.e. the 5D Planck scale of one micron-sized extra dimension;
- the scale where the SM Higgs quartic λ runs to zero, ~10¹⁰–10¹¹ GeV.

Take the identification λ(M₅) = 0 seriously, e.g. as a high-scale-SUSY threshold with tan β = 1 at the species scale, the boundary condition of Ibáñez–Valenzuela. Then:
- the dark-energy density fixes R, hence M₅ and the top mass;
- with the 2025 B−L dark-dimension neutrino model (m_ν ~ y²⟨H⟩²/M₅, [arXiv:2512.09052](https://arxiv.org/abs/2512.09052)), it also ties m_t to the neutrino scale.

Is the identification quantitatively true?

## Method

- **Running.** MSbar NNLO initial conditions at μ = M_t from Buttazzo et al. ([arXiv:1307.3536](https://arxiv.org/abs/1307.3536)), then two-loop RGEs for (g_Y, g₂, g₃, y_t, λ).
- **Validation.** The run reproduces their three-loop fit for λ(M_Pl), including its slopes in m_t, α_s and M_h, with a uniform offset of −0.0010. That offset is equivalent to +0.155 GeV in the required m_t and is applied to every quoted required top mass.
- **Dark-dimension conventions.** M₅³ = M̄_Pl²/(2πR), m_KK = 1/R, Λ^{1/4} = 2.25 meV. The O(1) convention factors 1/(2π)…1 are carried as a band in R.
- **Inputs.** M_h = 125.20, α_s = 0.1180 ± 0.0009. Measured M_t = 172.57 ± 0.29 GeV (direct average), or 172.4 ± 0.7 (pole mass from cross sections).

## Result 1: λ(M₅) = 0 with a micron dark dimension is excluded

| R | M₅ | M_t required (α_s = 0.1180) |
|---|---|---|
| 1 μm | 5.7×10⁸ GeV | **174.38** (±0.31 from α_s) |
| 30 μm | 1.8×10⁸ GeV | **175.07** |

Against 172.57 ± 0.43 (direct average, with the α_s spread added in quadrature) the identification fails by 4–6σ. Against the cross-section pole mass it fails by 2.5–3.5σ. Conversely, for the measured M_t the zero lies at μ₀ ≈ 3–5×10¹⁰ GeV. That would put R at about 10⁻⁶ μm (m_KK ~ 100 keV), not a micron.

> **The precise version of the coincidence is false.** The surviving statement is the weaker one: for M_t < 174.3 GeV the instability scale lies **above** the dark dimension's cutoff. Within that EFT the electroweak vacuum is then stable, with about 1.5 decades to spare at the measured top mass.

## Result 2: which "natural" boundary scale the top mass prefers

| boundary condition λ(μ*) = 0 at | μ* (GeV) | M_t required | vs 172.57 ± 0.43 |
|---|---|---|---|
| √(v M_Pl) (M_Pl = 1.22×10¹⁹) | 5.5×10¹⁰ | **172.57** | 0.0σ |
| √(M_Z M_Pl) | 3.3×10¹⁰ | 172.71 | 0.3σ |
| √(v M̄_Pl) (reduced) | 2.5×10¹⁰ | 172.80 | 0.5σ |
| √(m_t M̄_Pl) | 2.1×10¹⁰ | 172.86 | 0.7σ |
| M_GUT²/M_Pl (string SUSY-breaking scale, Ibáñez–Valenzuela talk) | 3.3×10¹³ | 171.42 | 2.7σ |
| M_Pl (asymptotic safety / multiple-point criticality) | 1.2×10¹⁹ | 170.98 | 3.7σ |
| dark dimension M₅ (R = 1–30 μm) | 1.8–5.7×10⁸ | 174.4–175.1 | 4.2–5.8σ |

The measured top mass sits **between** the two classic predictions: the Planck-scale boundary (AS/MPP, ~171.0) and the dark dimension (~174.5). It singles out the intermediate scale ~2–6×10¹⁰ GeV. That is the geometric-mean scale √(M_EW M_Pl) of the intermediate-scale string scenario (Burgess–Ibáñez–Quevedo) and of split/high-scale SUSY with tan β ≈ 1.

**Look-elsewhere control.** A boundary scale drawn log-uniformly from [10⁸, 10¹⁹] GeV requires an M_t within 1σ of the measurement **12%** of the time. So the √(v M_Pl) match is not evidence on its own: it is a ~1.5σ-equivalent coincidence. The informative content is the **exclusions**: the AS/MPP Planck boundary at 3.7σ, the flux-SUSY scale M_GUT²/M_Pl at 2.7σ, and the dark-dimension identification at 4σ or more. All three are stated against the direct average, and all weaken under the pole-mass ambiguity (~0.5 GeV).

## Caveats

- Running is two-loop plus a uniform three-loop offset; the residual is ≈ ±0.1 GeV in the required M_t.
- The direct-average top mass is a Monte-Carlo mass; its relation to the pole mass is uncertain by about 0.3–0.5 GeV.
- The threshold correction at the boundary (λ(μ*) = δλ ≠ 0, e.g. tan β ≠ 1 or stop mixing) shifts μ* and is not included.
- Prior art: the qualitative proximity of the instability scale to the intermediate / species scale is known (MVV 2022; Ibáñez–Valenzuela 2013; the vanishing-quartic scale in [arXiv:2609.28740](https://arxiv.org/abs/2609.28740) and 1307.2513). What is new here is the quantitative test with current inputs, the exclusion of λ(M₅) = 0 for the dark dimension, and the look-elsewhere number.

## Falsifiers ahead

An FCC-ee threshold scan (δm_t ≈ 50 MeV, with the pole-mass ambiguity resolved) together with a lattice α_s at ±0.0003 would fix μ₀ to about ±0.15 decades. That separates the variants √(v M_Pl), √(v M̄_Pl) and √(m_t M̄_Pl), which span 0.43 decades. It would test the AS/MPP Planck boundary at more than 10σ.
