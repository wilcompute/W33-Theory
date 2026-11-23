# Pass 12726: A is rescued by pre-inflation misalignment at θᵢ = 0.992π; mesogenesis can supply at most 86% of B′'s dark matter, so the coupled component lies outside it; O(1) brane kinetic terms can repair the SO(10) orbifold; the first layer, not attention vs MLP, is where ternary hurts, and code compounds the damage; the summary page now loads its numbers from a status file

Claude track. **Not a theory of everything.**
- Scripts:
  - `explore_pass12726_round.py`;
  - `explore_pass12726_layers.py` (≈60 min);
  - `build_toe_status.py`, which writes `analysis/toe_status.json`.
- Tests: `tests/test_toe_pass12726.py`, 5 tests passing.
- Page: [Quartic Zero Decision Map](https://claude.ai/artifact/P7DdJZNBnjeSPJgFZ4Wnoc), version 3, which fetches `status.json`.

## (1) Rescuing completion A
- **Abundance formula:** pre-inflation misalignment gives Ω_a h² = 0.12 (f_a/9×10¹¹)^1.165 θᵢ² F(θᵢ), with the anharmonic factor F = [ln(e/(1 − θ²/π²))]^{7/6}.

| f_a (GeV) | θᵢ needed for all of the dark matter | tuning 1 − θ/π |
|---|---|---|
| 3.7×10⁹ (−1σ) | none below π | — |
| **2.5×10¹⁰ (central, = μ₀)** | **3.117 = 0.992π** | **0.8%** |
| 1.7×10¹¹ (+1σ) | 2.04 = 0.65π | none needed |

- **With pre-inflation PQ breaking and θᵢ ≈ 0.992π, the axion at f_a = μ₀ is all of the dark matter** (m_a ≈ 230 μeV), at about 1% tuning.
- **The cost is low-scale inflation.** Isocurvature bounds tighten near π, and PQ breaking must happen before inflation (H_I/2π < f_a, T_RH < f_a).
- **A survives** as "f_a = μ₀ plus near-π misalignment", and it is testable by haloscopes at 50–1000 μeV.

## (2) B′'s second dark-matter component
- **Mesogenesis's ceiling:** in mesogenesis ψ → φ_B + ξ, so the stable dark states come one pair per baryon, with m_φ + m_ξ < m_ψ < 4.34 GeV. **The mesogenesis sector can supply at most 86% of the dark matter.**
- **Where the coupled component sits:** the quintessence-coupled ≥ 20% (Pass 12725) must lie outside the mesogenesis sector. Candidates include an axion-like or dark scalar field with a fifth force to quintessence.
- **Status:** B′'s dark sector has three parts: mesogenesis states (uncoupled), a coupled 20% component, and quintessence.

## (3) Repairing the SO(10) orbifold with brane kinetic terms
**Setup:** terms on the Pati–Salam brane shift δ₃ = a₄, δ₂ = a_L and δ₁ = 0.6a_R + 0.4a₄. The predicted α₃⁻¹ then moves by 1.29a₄ + 0.43a_R − 1.71a_L.

**Requirement:** cancelling the −1.46 shift at M_sR = 10 (Pass 12725) takes a₄ = 1.14, or a_L = −0.85, or a_R = 3.41 (in α⁻¹ units).

**Natural size:** α_G⁻¹/(πM_sR) = 0.74, so the repair needs **O(1.2–1.5) coefficients on SU(4) or SU(2)_L**.

**Status:** this is plausible but not automatic. The hybrid's orbifold doublet–triplet route stays open with one O(1) brane parameter.

## (4) Where ternary hurts: post-hoc ternarisation of an fp32 model (2 layers, d = 64, 3000 steps)

| corpus | fp32 | attention only | MLP only | layer 0 only | layer 1 only | all |
|---|---|---|---|---|---|---|
| prose | 2.660 | 3.976 | 3.977 | **4.424** | 3.296 | 4.693 |
| code | 2.187 | 4.002 | 4.018 | **4.381** | 3.112 | **5.283** |

- **Attention and MLP are equally sensitive on both corpora.**
- **The first layer is far more sensitive than the second,** the same pattern as Pass 12714's mixed-precision result.
- **Code compounds the damage:** quantising everything costs +3.1 bits/char on code against +2.0 on prose. This explains why ternary training closed the gap on prose but not on code (Pass 12725).
- **Practical rule:** keep the first layer at higher precision and ternarise the rest.

## (5) A data-driven summary page
`analysis/build_toe_status.py` collects the headline numbers from the pass certificates into `toe_status.json`:
- M_t, μ₀ and P(stable);
- the y′ floor today and at FCC;
- the falsifier;
- A's m_a, dark-matter share and θᵢ;
- B′'s χ² and σ8;
- Belle II coverage.

The page fetches it and fills tagged values, with inline fallbacks. **To update the page:** run the script and republish with the new file.

## Status
- **A:** rescued by near-π misalignment (1% tuning, low-scale inflation).
- **B′:** a three-part dark sector (mesogenesis ≤ 86%, plus a coupled component and quintessence).
- **Hybrid:** the orbifold is repairable with O(1) brane terms. Doublet–triplet splitting is now an open but plausible route.
- **Ternary:** first-layer precision matters most, and code is more fragile than prose.
