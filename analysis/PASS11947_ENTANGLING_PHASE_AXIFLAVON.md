# Pass 11947: the phase of the up-sector entangling modulus is an anomalous Froggatt–Nielsen rephasing — an axiflavon candidate

> **Withdrawn as a strong-CP solution by Pass 11949.** The theta Yukawa breaks the Froggatt–Nielsen U(1) explicitly
> at second harmonic (top modulation 2–5·10⁻⁶); the top loop exceeds the axion quality bound by 10¹⁶–10¹⁷ and fixes θ̄ = O(1).
> The rephasing structure and the f_a formula stand only as statements about the modulus.

Producer: `analysis/w33_pass11947_entangling_phase_axiflavon.py`
Certificate: `data/w33_pass11947_entangling_phase_axiflavon.json`
Regression: `tests/test_w33_pass11947.py`
Track: Claude. First strong-CP statement in the theta-null flavour chain (Passes 11938–11946).

## 1. Exact structure

**The texture.** Near a product home the up Yukawa is

Y_u = Σ_k c_k f_k f_kᵀ, with c_k = (6πiε)^k / k!   (Pass 11938).

**The determinant.** By Cauchy–Binet,

det Y_u = Σ_{k₁<k₂<k₃} c_{k₁} c_{k₂} c_{k₃} det[f_{k₁} f_{k₂} f_{k₃}]².

**Parity selects the terms.** The odd vectors span one dimension (Passes 11941/11944), so only triples with exactly one odd
k survive.
* The leading triple is (0,1,2).
* The next ones, (0,2,3) and (0,1,4), are suppressed by |ε|².

**Result.**

**arg det Y_u = 3·arg ε_u + const(τ) + O(|ε_u|²).**

Measured: the deviation from 3φ scales as |ε|^2.00 (1.3·10⁻⁶ at ε = 10⁻³, 1.1·10⁻³ at 3·10⁻²).

**Reading.**
* The heat-kernel texture *is* a Froggatt–Nielsen texture, with charges (0,1,2) on both chiralities.
* arg ε is the FN U(1) rotation.
* Its QCD anomaly coefficient is 0 + 1 + 2 = 3.

## 2. In the quark fits

The fits are those of Pass 11942, which reproduce all eight quark observables.

| rotation | θ̄ = arg det(Y_uY_d) | masses, \|V\|, J |
|---|---|---|
| arg ε_u → arg ε_u + φ | shifts by 3φ (to 10⁻⁴ rad) | change ≤ 3·10⁻³ relative (largest for J) |
| arg ε_d → arg ε_d + φ | shifts | change 9–30% |

The down rotation is not an anomalous rephasing: the down Wilson lines (Pass 11941) make it physical.

## 3. Reading

**The fitted vacua have a strong-CP problem.** They have θ̄ = O(1): 0.19 and −1.41 rad at the two fits. Taken alone, the
framework has a strong-CP problem.

**But arg Ω₁₂ is a candidate solution.** The up-sector Ω₁₂ is precisely the modulus that, per Pass 11913, stays flat
under fluxes within the tadpole bound. If its phase is a dynamical field:
* the QCD potential relaxes θ̄ to zero;
* it does so along a direction that leaves the CKM untouched to 3·10⁻³.

**Mechanism.** The entangling modulus is then the flavon and its phase the QCD axion. This is the axiflavon/flaxion
mechanism (Calibbi–Goertz–Redigolo–Ziegler–Zupan 2016; Ema–Hamaguchi–Moroi–Nakayama 2016), with the FN charges supplied
geometrically by the theta heat kernel rather than chosen.

## Open

* **Decay constant.** It needs the Kähler normalisation of Ω₁₂ in physical units.
* **Quality.** Every other potential for arg Ω₁₂ must be below about 10⁻¹⁰ of the QCD one. This is the standard axion
  quality problem; Pass 11913's flatness is necessary, not sufficient.
* **Domain-wall number.** It is 3.
* **The residual.** The O(10⁻³) shift of J along the axion direction means that relaxing θ̄ moves J slightly. A
  consistent fit must impose θ̄ = 0 and refit; this has not been done.
