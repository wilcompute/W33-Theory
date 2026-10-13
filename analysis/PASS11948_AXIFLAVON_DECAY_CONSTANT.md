# Pass 11948: the axiflavon decay constant is fixed by the up-quark masses — f_a ≈ 4–5·10¹⁵ GeV, m_a ≈ 1.1–1.5 neV

> **Withdrawn as a strong-CP solution by Pass 11949.** The theta Yukawa breaks the Froggatt–Nielsen U(1) explicitly
> at second harmonic (top modulation 2–5·10⁻⁶); the top loop exceeds the axion quality bound by 10¹⁶–10¹⁷ and fixes θ̄ = O(1).
> The rephasing structure and the f_a formula stand only as statements about the modulus.

Producer: `analysis/w33_pass11948_axiflavon_decay_constant.py`
Certificate: `data/w33_pass11948_axiflavon_decay_constant.json`
Regression: `tests/test_w33_pass11948.py`
Track: Claude. Quantifies the axiflavon reading of Pass 11947.

## 1. Normalisation

**The Kähler metric.** With the Siegel complex-structure Kähler potential K = −log det Im Ω,

K_{Ω₁₂Ω̄₁₂} = 1/(2·Im τ₁·Im τ₂)

at the product locus. A finite-difference check agrees to 10⁻³.

**The decay constant.** Write Ω₁₂ = r·e^{iφ}. The canonical field is a = M_P·r·φ/√(Im τ₁·Im τ₂). Since θ̄ = 3φ,

**f_a = M_P·|Ω₁₂| / (3·√(Im τ₁·Im τ₂))**.

This is invariant under the rescaling Ω → Ω/6 between toy and physical units.

## 2. Fixed by the up-quark masses

**Reduction.** Near the product locus, m_c/m_t = κ(τ)·|Ω₁₂|. So

f_a = M_P·(m_c/m_t) / (3·κ·Im τ).

**Along the Weber curve.** Along the whole Weber level curve |𝔣(τ)|⁸ = 2√(m_u m_t/m_c²) (22 points), the weight-zero
combination κ·Im τ stays between 0.584 and 0.591, a 1.3% spread. So f_a is fixed by two up-sector mass ratios alone:

| input m_c/m_t | f_a (GeV) |
|---|---|
| M_Z scale (0.00368) | 5.06–5.12·10¹⁵ (both quark fits: 5.12·10¹⁵) |
| GUT scale (≈ 0.0027) | ≈ 3.7·10¹⁵ |

## 3. Phenomenology (standard formulae)

* **Mass.** m_a = 5.69 μeV·(10¹² GeV/f_a) = **1.1–1.5 neV**, i.e. a frequency of **270–370 kHz**.
* **Photon coupling.** The anomaly sits in the up sector only, so E/N = 2·N_c·Q_u² = 8/3 and
  g_aγγ = α/(2πf_a)·(E/N − 1.92) ≈ **1.7–2.3·10⁻¹⁹ GeV⁻¹**.
* **Dark matter.** For the axion to be all of dark matter through misalignment, the initial angle must be about 0.007.
  This requires pre-inflationary Peccei–Quinn breaking, where the domain-wall number 3 is harmless.
* **Experimental window.** The 1–100 neV window is the GUT-scale Peccei–Quinn target of ABRACADABRA, DMRadio-GUT and
  CASPEr-Electric. The predicted mass sits at its lower edge.

## Scope

**Conditional on:**
* the axiflavon reading of Pass 11947 (a dynamical, flux-flat arg Ω₁₂);
* K = −log det Im Ω. Other Kähler contributions, such as brane and Kähler-moduli mixing, rescale f_a by O(1).

**Not addressed:**
* the axion quality problem;
* the O(10⁻³) shift of J under θ̄ relaxation.

**Prior art.**
* The axiflavon/flaxion mechanism: Calibbi et al. 2016; Ema et al. 2016.
* GUT-scale axions in the 1–100 neV window: e.g. arXiv:1807.09769 and 2301.00809.
* The new step: f_a follows from the up-quark mass ratios through the theta geometry.
