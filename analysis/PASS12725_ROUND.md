# Pass 12725: a partially coupled dark sector fits DESI without boosting σ8 (the 20% second component carries the coupling); the SO(10) orbifold overshoots unification at M_sR ≥ 10; FCC tightens the falsifier to y′ < 0.40; the new top mass breaks completion A's axion–dark-matter link; on code the ternary gap widens with width; a shareable summary page

Claude track. **Not a theory of everything.**
- Scripts:
  - `explore_pass12725_round.py`;
  - `explore_pass12725_codelm{32,64}.py`;
  - an inline computation saved as `data/explore_pass12725_axion_shift.json`.
- Tests: `tests/test_toe_pass12725.py`, 5 tests passing.
- Summary page: [Quartic Zero Decision Map](https://claude.ai/artifact/P7DdJZNBnjeSPJgFZ4Wnoc), private until shared.

## (2) B′ dark sector: couple only the second component
**Setup:** a fraction f of the dark matter couples to quintessence (m ∝ e^{βφ}) and the rest does not. Background, apparent CPL against DESI DR2 + CMB + Pantheon+, and linear growth with separate coupled and uncoupled components.

| f | β | λ | w₀ | w_a | min w | χ² (ΛCDM 6.33) | σ8 / σ8(ΛCDM) |
|---|---|---|---|---|---|---|---|
| 1.0 | 0.1 | 0.9 | −0.908 | −0.258 | −1.068 | 1.81 | 1.016 |
| 0.5 | 0.2 | 0.9 | −0.901 | −0.273 | −1.080 | 1.81 | 1.013 |
| **0.2** | **0.3** | **0.9** | **−0.881** | **−0.289** | **−1.095** | **3.02** | **0.995** |
| **0.5** | **0.1** | **0.9** | — | — | — | **3.34** | **0.993** |

- **Coupling only 20% of the dark matter (β = 0.3) keeps DESI's phantom mimicry (χ² 3.0) without raising σ8.**
- **The pieces fit together.** Pass 12724 required at least 20% of B′'s dark matter to be a second component. **The minimal consistent B′ dark sector** is therefore an uncoupled dark baryon (≤ 80%) plus a second component (≥ 20%) coupled to quintessence with β ≈ 0.3.

## (1) SO(10) orbifold KK thresholds
**Parity classes of the 45** under Pati–Salam (one brane) and SU(5)×U(1) (the other), computed with the so(10) machinery:

| class | content | mass levels |
|---|---|---|
| (++) | SU(3)×SU(2)×U(1)×U(1)_X | 2n/R |
| (+−) | (3,1)_{±2/3} + (1,1)_{±1} | (2n+1)/R |
| (−+) | X,Y (3,2)_{±5/6} | (2n+1)/R |
| (−−) | (3,2)_{±1/6} | (2n+2)/R |

- **Note:** the numerical classification mislabelled (++), so its b = (0, −4, −6) is set analytically.
- **Shift of the predicted α₃⁻¹:** −0.87 at M_sR = 5, −1.27 at 8, **−1.46 at 10**, −1.88 at 15, −3.07 at 30, −7.93 at 100.
- **In SO(10) the KK thresholds at M_sR ≥ 10 overshoot the hybrid's +0.26 mismatch by more than 1.** The SU(5) estimate of Pass 12724 (−0.12 at 10) was too optimistic, because the extra Pati–Salam-only and (3,2)_{1/6} towers dominate.
- **Consequence:** geometric protection (M_sR ≥ 9.8) and SO(10) orbifold doublet–triplet splitting are **in tension**. Escapes are brane-localised kinetic terms, additional bulk matter, or a smaller protection requirement (a quality bound below dimension 11).

## (4) The y′ floor at FCC-era precision
**Inputs:** σ(M_t) = 0.04 GeV with no scheme ambiguity, σ(α_s) = 0.0002, threshold ±10%.

**Floor:** median 0.412, 95% range **0.402–0.423** (today: 0.351–0.469).

**At FCC the falsifier tightens to y′ < 0.40.**

## (exploration) The new top mass and completion A's axion
- **What A assumes:** f_a ≈ μ₀ (the quartic zero), with a post-inflation axion.

| M_t | f_a = μ₀ (GeV) | m_a | axion share of the dark matter |
|---|---|---|---|
| 172.57 | 5.4×10¹⁰ | 105 μeV | 47% |
| **172.80** | **2.5×10¹⁰** | **229 μeV** | **19%** |

- **What full dark matter needs:** f_a = 1.04×10¹¹ GeV, i.e. **M_t = 172.38**. That is 1.6σ below 172.80 (experimental) or 0.8σ (with the scheme uncertainty).
- **The predicted mass band:** 34–1550 μeV at 1σ. ALPHA Phase I (40–80 μeV, axion search 2027–28) covers only the low tail.
- **Status:** **A's coincidence between λ = 0 at f_a and the axion being the dark matter now needs the top mass to fall by about 0.4 GeV.**

## (3) Ternary scaling on a code corpus (200,000 characters of this repo's Python, vocabulary 95)

| width | fp32 | ternary (curriculum) | gap | zero weights |
|---|---|---|---|---|
| 32 | 2.968 | 3.510 | 0.542 | 47% |
| 64 | **2.389** | 3.096 | **0.707** | 46% |

- **On code the gap widens from width 32 to 64.** Full precision benefits far more from width (−0.58 bits/char) than ternary does (−0.41).
- **The width^−0.59 closing seen on prose (Passes 12723–12724) does not generalise at these sizes.** It is domain-dependent.

## (exploration, web) Novelty and status checks
- **The y′ floor:** published vacuum-stability analyses with vectorlike quarks (PRD 107 036018; arXiv:1812.11303; 2512.24215) put *upper* bounds on vectorlike Yukawas. No lower bound from requiring λ to vanish at an intermediate scale was found, so **the floor appears new**.
- **No 2026 ATLAS/CMS vectorlike-quark excess** was found near 1.5–2 TeV.
- **Proton decay:** Super-K p → e⁺π⁰ > 2.4×10³⁴ yr (2020). Hyper-K starts in 2027.
- **Dark energy:** DESI's final five-year cosmology is expected in 2027. DES final BAO+SN gives 3.2σ.

## Status
- **A:** strained by M_t = 172.80. The axion is only 19% of the dark matter unless M_t ≈ 172.4.
- **B′:** the most coherent it has been. A static radius, an uncoupled dark baryon, and a coupled second component fit DESI (χ² 3.0) with no σ8 penalty.
- **Hybrid:** doublet–triplet splitting remains open, and the SO(10) orbifold route overshoots unification.
- **Falsifier:** y′ < 0.35 today, y′ < 0.40 at FCC.
- **Ternary:** the language-model gap closes with width on prose but not on code.
