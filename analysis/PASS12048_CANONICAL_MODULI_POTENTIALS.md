# Pass 12048: canonical moduli potentials point away from the flavour hierarchy

* **Producer:** `analysis/w33_pass12048_canonical_moduli_potentials.py` (4/4 checks, about 2 s)
* **Certificate:** `data/w33_pass12048_canonical_moduli_potentials.json`
* **Regression:** `tests/test_w33_pass12048.py`
* **Track:** Claude. Reservation `9d0303849`.

## Question

Passes 12004–12047 show that every flavour extension of the theta architecture is a fit, because nothing fixes the
moduli. Do the canonical, parameter-free modular-invariant potentials fix them, and in the right place?

The potentials are N = 1 supergravity, V = e^K(K^{ij̄}D_iW D_jW̄ − 3|W|²):
* **Genus 1:** K = −3 log(2 Im τ), W = η⁻⁶. This is the gaugino-condensation classic (FILQ 1990, CFILQ 1991).
* **Genus 2:** K = −3 log det(2 Im Ω), W = χ₁₀^(−3/10). This is the unique power that makes e^K|W|² Sp(4,ℤ)-invariant.
  * χ₁₀ is evaluated as the product of the ten even theta constants squared.
  * Derivatives are branch-free: d ln W = −0.3 dχ₁₀/χ₁₀.

## Results

**1. Genus 1.** The minimum is at τ = 1.2346i, reproducing the classic 1.23i. Its SL(2,ℤ) images on the CP line
Re τ = 1 give m_u m_t/m_c²:
* 2.37, at +45σ;
* 0.366, at −11σ.

The data are 0.534 ± 3.3%. The fitted up modulus is 1.1435i in the fundamental domain.

**2. Genus 2, near the product locus.** The up hierarchy (1, ε, ε²) lives near Ω₁₂ = ε → 0 (Pass 11872).
* **Control.** χ₁₀ → π² ε² Δ(τ₁)Δ(τ₂), checked to 10⁻⁵. This is an exact control of the evaluation.
* **Behaviour.** The ε F-term dominates, giving **V ∝ |ε|^(−16/5) → +∞** (measured log slope 3.200).
* **Consequence.** The canonical potential *repels* the hierarchy locus. At the fitted ε_u = 0.0055 it is large,
  positive and steep.

**3. Genus 2, minimum on the symmetric CP-locus home.**
* **Location.** Im ε / Im τ = 1/2 (to 2·10⁻⁶), Im τ = 1.2721, V = −83.39. An equivalent image sits at 1.0482.
* **Geometry.** Im Ω is proportional to the **A₂ (Eisenstein) lattice Gram matrix**, a point with enhanced stabiliser.
  The canonical potential selects the A₂-symmetric abelian surface, the lattice native to the qutrit structure.
* **But no hierarchy.** There m₂/m₁ = 0.18–0.31, against m_c/m_t = 0.0037.

## Reading

**What the canonical potentials do.** They stabilise the moduli at symmetric points: 1.23i in genus 1, the A₂ point in
genus 2. They push away from the near-product region that the flavour hierarchy needs.

**What this sharpens.** The "free moduli" problem of 12004–12047 becomes concrete: the natural potentials point the
wrong way. The hierarchy needs a non-canonical stabilisation, for example:
* matter or threshold factors (H(j)-type);
* fluxes;
* a sector that makes the product locus attractive, such as states becoming light there.

**Observation, not claimed as more.** The genus-2 minimum is the A₂ point, consistent with the qutrit/Eisenstein
structure of the substrate.

## Scope

* **Potentials.** Two canonical potentials, with no dilaton dynamics and no H-factors.
* **Genus-2 minimum.** Located only on the symmetric CP-locus slice.

## What is not new

* The genus-1 minimum (FILQ; CFILQ).
* χ₁₀ as the genus-2 analogue of Δ, and its product-locus factorisation (classical).
* Siegel modular flavour (Ding–Feruglio–Liu, arXiv:2010.07952).
* Hierarchies near fixed points (Novichkov–Penedo–Petcov; Feruglio et al.).
* Codex 11950 uses χ₁₀ differently, as a gauge-kinetic divisor.
