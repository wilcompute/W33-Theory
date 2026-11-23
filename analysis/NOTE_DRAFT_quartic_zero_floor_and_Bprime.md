# A model-independent floor on the top-partner Yukawa from a vanishing Higgs quartic, and a dark-dimension completion with B-mesogenesis

*Draft note, Claude track (Passes 12707–12731). Not peer reviewed. Numbers are reproducible from the scripts cited in each section.*

## Summary
1. **The floor.** Take the Standard Model plus one TeV vectorlike quark family (Q + T) with a Yukawa y′ to the Higgs. If new physics sets λ = 0 at some intermediate scale μ, the y′ that achieves this never falls below **0.40** for μ = 10⁷–10¹³ GeV (95% range 0.35–0.47, including top-mass scheme, α_s and threshold uncertainties). A measured **y′ < 0.35 excludes every such completion,** and **y′ < 0.40** does so at FCC-era precision. The literature we found bounds vectorlike-quark Yukawas only from above (perturbativity, Landau poles).
2. **B′.** A completion built from the dark dimension, with:
   - a radius of 0.009–0.2 μm, after the 2026 exclusion of KK-graviton dark matter;
   - a 1.74 TeV top partner with y′ ≈ 0.50 that sets λ = 0 at the 5D Planck scale;
   - B-mesogenesis at the forced 6–17 MeV reheating temperature for the baryon asymmetry;
   - a two-component dark sector.

   It fits DESI DR2 with static-radius coupled quintessence and is testable at Belle II and FCC-hh. We found no prior paper combining these ingredients.

## 1. The y′ floor
**Setup:**
- Two-loop SM running with Buttazzo et al. NNLO matching.
- Two-loop vectorlike-quark terms (PyR@TE).
- The full one-loop threshold at M_VL = 1.74 TeV: λ_SM = λ_VL(1 + 2N_c y′²/48π²) − (5/6)N_c y′⁴/16π².

**The needed y′ at M_t = 172.80 GeV:**

| μ (GeV) | 10⁷ | 10⁸ | 10⁹ | 10¹⁰ | 10¹¹ | 10¹² | 10¹³ |
|---|---|---|---|---|---|---|---|
| y′ | 0.608 | 0.544 | 0.495 | 0.458 | 0.433 | 0.418 | 0.413 |

- **The curve flattens above 10¹⁰ GeV,** so every completion with a quartic zero at an intermediate scale and one vectorlike family predicts y′ ≈ 0.41–0.50.
- **Uncertainty budget:** Monte Carlo over M_t (172.80 ± 0.26 ⊕ a 0.5 GeV scheme term), α_s (0.1180 ± 0.0009) and the threshold field-renormalisation term (±50%). The floor's 95% range is **0.351–0.469** (median 0.400). At FCC-ee precision (σ_Mt = 0.04, σ_αs = 0.0002) it tightens to **0.402–0.423**.
- **Scripts:** `explore_pass12723_attractor.py`, `explore_pass12724_round.py`, `explore_pass12725_round.py`.

## 2. Completion B′
**Dark dimension.**
- Near-threshold KK-graviton decays are d-wave suppressed (Langhoff 2026; Lee–Randall–Riojas 2026; the Γ ∝ p⁵ scaling reproduced independently in `toe_pass12708_round.py`). KK-graviton dark matter is therefore excluded, and MeV-photon limits require R ≲ 0.2 μm.
- With R = λΛ^{−1/4} and λ = 10⁻⁴–2.3×10⁻³, the 5D Planck scale is M₅ ≈ 1–3×10⁹ GeV.

**Top partner.**
- λ(M₅) = 0 fixes **y′ = 0.488–0.505** at M_t = 172.80 (≈ +0.005 from the B-mesogenesis mediator's gauge charges).
- FCC-hh separates B′ from E₆-type completions (y′ ≈ 0.46 and falling with M_VL) at 3–15σ.
- A coloured mesogenesis mediator must have a Higgs portal |λ_HY| ≲ 0.04, or the prediction is lost.

**Cosmology.**
- **Reheating:** the dark dimension forces T_RH ≈ 6–17 MeV, inside the 5–60 MeV range of Dark_CP B-mesogenesis. The required A_CP·BR ≈ 0.5–1.4×10⁻⁷.
- **The dark baryon's share:** mesogenesis supplies at most 86% of the dark matter (m_ψ < m_B − m_p).
- **Dark energy:** a second, cold component (≥ 14–20%) coupled to quintessence with β ≈ 0.3 reproduces DESI DR2's apparent phantom crossing (χ² = 3.0 against 6.3 for ΛCDM) at a static radius, with σ8 unchanged (ratio 0.995).
- **Newton's constant:** a radion-driven DESI evolution would vary G 38× faster than lunar laser ranging allows. The radius must be static.

**Tests:**
- **Belle II inclusive B → baryon + missing energy** (26–61% of B′ at 10 ab⁻¹, 62–89% at 50 ab⁻¹).
- **HL-LHC vectorlike quarks** at ≥ 1.74 TeV.
- **FCC-hh y′.**
- **N_eff** changes by only ≈ −0.06, so B′ does not explain the low-N_eff hint.

## 3. Caveats
- **Inputs:** the KK-graviton exclusion rests on 2026 preprints. Belle II reach uses an assumed tag efficiency and background.
- **Approximations:** the dark-energy fits use a Gaussian CPL likelihood with an assumed w₀–w_a correlation of −0.9.
- **Scope:** the y′ floor assumes λ = 0 as the boundary condition. With N degenerate vectorlike families the floor scales as about 0.40·N^(−1/4) (0.34 for N = 2, 0.30 for N = 3). With Yukawas to both chiralities it applies to (y′⁴ + y″⁴)^{1/4}. The general falsifier is (Σ y⁴)^{1/4} < 0.35, summed over families and chiralities.

## Related work
- Redi–Strumia (1208.6013), axion–Higgs unification.
- Ibáñez–Valenzuela (1301.5167), high-scale SUSY with tan β ≈ 1.
- Unwin (2609.28740), SUSY at the vanishing quartic.
- Hall–Harigaya (1803.08119), Higgs parity.
- Montero–Vafa–Valenzuela (2205.12293), the dark dimension.
- Elor–Escudero–Nelson (1810.00880) and Elor (2509.18246), B-mesogenesis.
- Langhoff (2610.01825); Lee–Randall–Riojas (2609.36234).
