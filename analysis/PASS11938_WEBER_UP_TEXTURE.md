# Pass 11938: the second small parameter and the Weber law for the up texture

> **Prior ownership (added after the 2026-10-17 intake).** Three statements used here were already made in Pass 11872
> (Claude track, 2026-10-09, `analysis/PASS11869_11873_SIEGEL_LEVEL3_TWO_QUTRITS.md`):
> * rank one ⟺ Ω₁₂ = 0;
> * the Schmidt spectrum (1, ε, ε²);
> * the dependence of σ₁σ₃/σ₂² on (τ₁, τ₂), with sampled values 4.4, 4.3 and 5.4.
>
> The determinant coefficient and its parity are owned by TOE38/TOE39 (Codex, 2026-10-10). This pass owns:
> * the closed-form Weber law σ₁σ₃/σ₂² = |𝔣(τ₁)𝔣(τ₂)|⁸/4, which Pass 11963 confirmed independently to 3.9·10⁻⁸;
> * the reducible polar line of the E8 Cartan;
> * the CM, cusp and data comparisons.

Producer: `analysis/w33_pass11938_weber_up_texture.py`
Certificate: `data/w33_pass11938_weber_up_texture.json`
Regression: `tests/test_w33_pass11938.py`
Track: Claude. Follows Passes 11936/11937; cites Pass 11912 (Ω₁₂ as the family Wilson line) and Passes 11869–11873
(product theta ⇔ factorised torus).

## Question

Pass 11936 left m_u/m_c = b/a fixed by the direction (0.80 on the E8-selected orbit). Pass 11937 asked whether some
direction or degeneration supplies a second small parameter.

## Results

**1. The polar line of the stabiliser state is reducible.**
* **Setting.** Let u be a tangent direction orthogonal to the stabiliser state e₁ = (1,0,0). This covers the strange
  circle (0,1,e^{iφ})/√2, with M₂ = log 2, and random (0,x,y) with M₂ between 0.38 and 0.69.
* **Result.** For every such u and every t, the level-3 theta Yukawa of Ω(1, t u) is **exactly rank one**:
  * s₂ ~ 10⁻¹⁸ wherever the Coble/Maschke inversion converges to 10⁻¹⁶;
  * s₂ ≲ √residual otherwise.
* **Reading.** The Cartan 3-plane span(Witting ray, e₁^⊥) maps into the reducible (product-torus) locus.
* **Search.** An unconstrained Nelder–Mead minimisation of m_u/m_c over CP² converges onto this line, reaching 0.001.
* **Correction to Pass 11936.** That pass described these directions as a "deeper cusp with a locked pair". The pair is
  not locked; it is zero.

**2. Geometric exponents.**
* **Spectrum.** Off the line by θ = arcsin|u₁|, near a Witting ray, the spectrum is (1, Aθt, Bθ²t):
  * exponents (0,1,2) in θ (measured 0.999 and 2.000);
  * exponents (1,1) in t.
* **Reading.** θ, the overlap of the flavour Higgs with the stabiliser state, is the second small parameter.
* **Mechanism.** θ is the off-diagonal modulus Ω₁₂ (the family Wilson line of Pass 11912).

**3. The Weber law (exact, leading order in Ω₁₂).**
* **Expansion.** Near a product torus diag(τ₁, τ₂), the heat equation gives

  Y = Σ_k (6πiΩ₁₂)^k / k! · f_k(τ₁) ⊗ f_k(τ₂), with f_k(τ)_c = Σ_n (n + c/3)^k e^{3πiτ(n+c/3)²}.

* **Orthogonality.** f₁ = (0, x, −x) is the strange state, orthogonal to the even vectors f₀ and f₂.
* **Invariant.** This gives an invariant independent of the size and phase of Ω₁₂:

  **m_u m_t / m_c² = s₁s₃/s₂² = |𝔣(τ₁) 𝔣(τ₂)|⁸ / 4**,

  where 𝔣 is the Weber function. Equivalently, the factor gives |η(τ)²/(η(τ/2)η(2τ))|⁸/√2.
* **Checks.**
  * The η-quotient was found by exact regression (residual 7·10⁻¹⁵).
  * The Weber law was checked at 10 random pairs (relative error ≤ 3·10⁻⁸).
  * 𝔣²⁴ is a root of (x−16)³ = j·x (checked to 10⁻¹⁴).
* **Exact values.**

| factors | m_u m_t/m_c² |
|---|---|
| (i, i) | 4 |
| (i, ω) | 2^{4/3} |
| (ω, ω) | 2^{2/3} |
| (1+i, 1+i) | 1 |

* **Frames of the elliptic points.** Over all level-structure frames of the two elliptic points, |𝔣|⁸ ∈ {2, 4, 2^{4/3}}.
  At j = 1728 the cubic is (x−64)(x+8)²; at j = 0 it is (x−16)³. Hence **any product of CM elliptic-point factors gives
  m_u m_t/m_c² ≥ 1**.

**4. Confrontation with the data.** At M_Z, m_u m_t/m_c² = 0.54 (m_u = 1.23 MeV, m_c = 0.620 GeV, m_t = 168.3 GeV;
about ±20% from m_u).

| regime | m_u m_t/m_c² | status |
|---|---|---|
| CM / elliptic-point factors (includes the E8-selected square boundary curve, factor 2√2) | ≥ 1 | **excluded** |
| E8 cusp regime, small t (where the soft supertrace puts the vacuum) | ≈ 0.89/t along the e₁-perturbed strange direction | **excluded** |
| strange plane at t = O(1) | branch-dependent (φ = π, t = 0.3 / 1: 2.78 / 0.148 on one inversion branch, 3.23 / 5.28 on another; on the first branch R = 0.118, 0.80, 2.03, 7.45 at t = 2, 4, 10, 100) | reachable on some branches: a fit, not a prediction |

* **Floor in the cusp regime.** The floor over **all** directions at t = 0.005 is a search-based lower bound:
  * method: 6 Nelder–Mead runs, kept inside the one-dimensional cusp regime;
  * runs: 0.7999, 0.7999, 0.8040, 0.8100 (near M₂ ≈ 0.58, the T / log(9/5) orbit), plus 0.8778 and 0.8803 (local);
  * result: **min_u R·t = 0.7999**, so m_u m_t/m_c² ≳ 0.8/t near any Witting ray.
* **What the floor implies.** With m_c/m_t = 3.6·10⁻³, the data need t ≳ 1.5, well outside the cusp regime where
  Pass 11936 matched m_c/m_t (t ≈ 7.8·10⁻³).
* **Direction preference.** The E8 angular selector disfavours the e₁-orthogonal strange direction: C_G = 5.047, the
  largest of the special orbits (Pass 11935).

## Reading

* **Shape.** The up texture has a geometric shape: Ω₁₂, the stabiliser overlap, is the second small parameter, with
  exponents (0,1,2).
* **Coefficient.** Its O(1) coefficient is modular, a Weber function of the two elliptic factors.
* **Special values miss.** The special values the dynamics prefers (CM points, the E8 cusp regime) miss the measured
  m_u m_t/m_c² by a factor ≥ 1.8 (CM) and ≈ 190 (cusp at t ≈ 8·10⁻³, where R ≥ 103).
* **Branch caveat.** The Cartan → Ω inversion is many-valued. Small-t values reproduce across runs; values at
  t = O(1) do not, so nothing is claimed there beyond reachability.
* **Consequence.** A single-scale E8 cusp cannot give the up spectrum. The vacuum must sit at t = O(1), with a generic
  (non-CM) factor modulus, or the up sector needs a source outside the theta Yukawa (e.g. the twisted / 27 sector).

## Scope

* **Level of the claims.**
  * Exact or numerically certified: the rank-one line, the exponents and the Weber law.
  * Search-based: the cusp floor of 0.80.
  * The data comparison uses M_Z running masses. The ±20% m_u uncertainty and the running to high scales (≈ 0.64 at
    2·10¹⁶ GeV in the SM) do not change either exclusion.
* **Classical mathematics.** The heat-equation expansion and the Weber identities are classical. The new steps are:
  * the identification with m_u m_t/m_c²;
  * the E8 Cartan plane that maps to the reducible locus.
* **Rediscovery check.** Corpus searched for the result: "heat equation", "m_u m_t", "geometric texture", 2^{5/3},
  1.5874, 3.1748 (no prior statement). Pass 11912 already had Ω₁₂ as the hierarchy carrier in the Gaussian regime;
  it is cited, not re-derived.
