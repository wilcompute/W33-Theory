# Passes 11890–11892: the vacuum phase diagram of the E₈ twisted Higgs: every W(3,3) structure is a vacuum

Producer: `analysis/w33_pass11890_11892_vacuum_phase_diagram.py`
Certificate: `data/w33_pass11890_11892_vacuum_phase_diagram.json`
Regression: `tests/test_w33_pass11890_11892.py`
Track: Claude.

These are the three next steps of 11887–11889: the Hosotani completion, hierarchy from cusp displacement, and fermion
loops. Throughout, the setting is SU(9) + 84, the ℤ₃-twisted half of E₈. Its flat direction is the Vinberg Cartan 𝔥,
which is the genus-2 modulus together with a Weierstrass point.

## The result in one table

Each dynamical regime selects a *different* distinguished object of the W(3,3) programme:

| regime | vacuum | unbroken | W(3,3) / Siegel object |
|---|---|---|---|
| 4d bosonic loops (11884) | Witting ray | SU(3)³ (in E₈: E₆×U(1)²) | a **point** of W(3,3); a cusp |
| N = 1 SUSY | flat | — | the whole Cartan |
| SUSY, soft m² < 0 | Witting ray (max G = −18 log 3) | SU(3)³ | a **point** of W(3,3) |
| SUSY, soft m² > 0 | min G | finite (Pauli group and more) | the **C₁₀ curve y² = x⁵ − 1** with its Z₅-fixed Weierstrass point |
| 4d fermion-dominated | max F, Im Ω → large | — | a **cusp** (degeneration) |
| Hosotani: bosons, or SS adjoint gauginos (n_F = 1, 2, 4) | x = 0 | SU(9) | the untwisted point |
| Hosotani: periodic adjoint fermions, n_F = 2 | D₄ ⊕ D₄ holonomy centraliser | 16 vectors (+16 fermions) | a **tensor factorisation** (product torus) |

## 11890: Hosotani (gauge–Higgs on T²/ℤ₃)

**The setting.** Take E₈ in six dimensions on T²/ℤ₃ with the W(3,3) twist. The four-dimensional zero modes are exactly
SU(9) gauge fields plus the 84, which is the internal gauge-field component.

**Two facts make the computation possible.**
* The renormalizable flat set μ = 0 is the set of flat connections, since F_{zz̄} = [x, x†].
* The 240 eigenvalues α(x) of ad(x) form a **linear map** on 𝔥. The check error is 4·10⁻¹⁴, and the set closes under
  ω to 10⁻¹⁴, as the twist requires.

**The potential.** The untwisted one-loop potential is

  V = −Σ_α [f(α(x)) − n_F f(α(x)+s)],  f(w) = Σ_{l ∈ Λ, l≠0} cos 2π⟨l, w⟩ / |l|⁶,

on the hexagonal lattice. Massless four-dimensional vectors are counted as (1/3)#{α : α(x) ∈ Λ*}; the twist acts as a
regular order-3 Weyl element, so each orbit of three roots gives one vector. This count reproduces 80 at x = 0 and 24 at
the Witting rays.

**Results.**
* **Bosons alone, or Scherk–Schwarz adjoint gauginos** (s = 1/(1−ω), n_F = 1, 2, 4): the global minimum is at x = 0,
  and SU(9) is unbroken. The minimal gauge–Higgs completion does not reproduce the trinification selection. That
  selection needed |x| to be fixed by a tree-level Higgs potential, which gauge–Higgs unification does not supply.
* **Periodic adjoint fermions dominating** (n_F = 2): the vacuum breaks to 48 massless roots in two components of 24,
  i.e. **D₄ ⊕ D₄**, giving 16 massless vectors and 16 massless fermions.
  * The 56-dimensional holonomy centraliser equals **Fix(P) + Fix(P⊥)**, where Fix(P) is the centraliser of the
    one-qutrit Pauli group of a plane P (32-dimensional, contained in it).
  * So the vacuum is a **tensor factorisation** of the two qutrits. This is the corpus's "factorisation ↦ D₄×D₄"
    (11687), now selected dynamically.
  * In the Siegel dictionary it is a product torus.
  * Identifying the 16-dimensional four-dimensional algebra as A₂⊕A₂ (the triality-twisted fixed algebras) is inferred,
    not computed.

## 11891: Higgs displacement from the trinification point is the cusp coordinate

Move the Cartan vev off a Witting ray by δ and invert to the torus, as in 11879; inversion residuals are ≤ 10⁻¹⁵. The
largest reduced Im Ω grows by a constant step per halving of δ. The local slope d(Im Ω)/d ln(1/δ) is:

| δ step | 0.0125→0.00625 | →0.003125 | →0.0015625 | →0.00078125 |
|---|---|---|---|---|
| slope | 0.95277 | 0.95338 | 0.95376 | 0.95402 |

It increases monotonically toward **3/π = 0.95493**; geometric extrapolation gives 0.9546.

**What follows.** Im Ω = (3/π + o(1)) ln(1/δ). The leading level-3 theta suppression |e^{πiΩ/3}|, which comes from the
v² = 1/9 terms, is then ∝ δ. **The family-hierarchy parameter of the theta texture is linear in the Higgs displacement
from the trinification point.**

This joins two earlier results:
* the radiative vacuum, which sits exactly on the cusp (11884);
* the (1, ε, ε²) theta hierarchy (11872/11876).

Small corrections that displace the vacuum by δ give ε ∝ δ. A natural source is the dimension-12 holomorphic operator,
with δ ∼ (v/Λ)⁸·(couplings).

## 11892: fermion loops

* **N = 1 SUSY** (chiral 84 plus gauginos): along the D-flat direction, the heavy scalar spectrum is proportional to the
  vector spectrum (11884). With the SUSY normalisation every massive vector multiplet is degenerate, so V₁‑loop ≡ 0. The
  modulus stays exactly flat perturbatively.
* **Soft scalar mass m².** To first order the one-loop shift is a positive multiple of m²G, where G = Σ eᵢ log eᵢ and
  Σ eᵢ is fixed.
  * **m² < 0** selects max G = −18 log 3, attained exactly at the Witting rays: trinification again.
  * **m² > 0** selects min G = −21.8539226. Inverting to the torus gives the **C₁₀ curve y² = x⁵ − 1** (distance
    3·10⁻⁷ after an Sp(4,ℤ) shear). On the exact C₁₀ torus, the six odd-theta Cartan points give G = −21.7976 (five of
    them) and −21.8539226 (one), so the vacuum is the Weierstrass point fixed by the Z₅ automorphism (x = ∞).
  * The C₁₀ point is CP-conserving (11874).
* **Fermion-dominated, non-SUSY:** this selects the maximum of F. It has 4 massless vectors, and its torus runs to
  large Im Ω, i.e. toward a cusp.

## What this changes

1. **The W(3,3) structures are vacua, not just labels.** Each distinguished object becomes the vacuum of an ordinary
   field-theory regime:
   * points of W(3,3) (trinification, E₆);
   * tensor factorisations (D₄×D₄);
   * the most symmetric pointed Jacobian (C₁₀, Gottschling's order-10 point);
   * cusps.
2. **The hierarchy mechanism is quantitative.** ε ∝ δ, with δ the displacement from the trinification point.
3. **Which regime is ours** is still undecided by internal data. It is set by the matter content and the SUSY-breaking
   pattern. That is now the precise open question, replacing "why q = 3".

## Not established

* The Hosotani analysis uses the untwisted contribution only; fixed-point (twisted) contributions are not included.
* The fermion content is adjoint copies only.
* The A₂⊕A₂ identification is inferred.
* The C₁₀ result is first order in soft m².
* None of this is connected to measured quantities.

## Prior art

* Hosotani (1983, 1989).
* Gauge–Higgs unification on T²/ℤ_N (e.g. Haba–Hosotani–Kawamura–Yamashita; Scrucca–Serone–Silvestrini).
* Scherk–Schwarz.
* Gottschling (1961).
* Bruin–Filatov (Weierstrass points).
* Corpus: 11687 (factorisation ↦ D₄×D₄), 11874 (C₁₀ point, CP), 11872/11876 (hierarchy), 11879–11889.
* TOE44 (parallel track): the CP rephasing firewall.
