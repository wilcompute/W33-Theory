# Passes 11818–11822 — why the W(3,3) Z6-I Standard Models fail and Z6-II need not: the corrected R rule, the alternating SU(9) cubic, the ℤ₉ centre, and hidden confinement

Producer: `analysis/w33_pass11818_11821_su9_flavour_and_corrected_textures.py`
Inputs: `data/w33_pass11810_probe_fields.json.gz` (33 core Z6-I models), `data/w33_pass11819_z6ii_probe_fields.json.gz` (9 Z6-II A8 Standard Models + Codex benchmark)
Certificate: `data/w33_pass11818_11821_su9_flavour_and_corrected_textures.json`
Lean: `formal/W33/Pass11822SU9Flavour.lean`
Regression: `tests/test_w33_pass11818_11822.py`

## 11818 — the corrected R rule, and what survives

**The rule.** Cabo Bizet, Kobayashi, Mayorga Peña, Parameswaran, Schmitz and Zavala (arXiv:1301.2322, eqs. 3.53–3.54) give the Z6-I rule:
* plane 3 carries its own R charge;
* the two G2 planes carry **one combined, γ-corrected** charge, Σ_α [R¹ + R² + 6γ]_α ≡ 2 (mod 6);
* in orbifolder's sign convention the targets are −1 (mod 3) and −2 (mod 6).

This is weaker than the per-plane rule of Pass 11810, so that pass's higher-order claims are re-derived here.

**What survives.**

* **Tree level is exact and rule-independent.** Untwisted cubics are the 10D super-Yang–Mills term ε_ijk Tr Φⁱ[Φʲ, Φᵏ]. So the up Yukawa is g·ε on the two degenerate planes and m_t = m_c, in all 33 models.
* **The lock.** Splitting top from charm needs a nonempty monomial that is neutral under every rule.
  * With hidden-neutral singlets **no such monomial exists in 10 models** (the same 10, flagship included): the degeneracy is exact to all orders.
  * With hidden composites the first neutral monomial has degree 3 (15 models), 6 (3), 7 (2) or 9 (4).
* **Down quarks and leptons.**
  * With hidden-neutral condensates they are zero to all orders by U(1) gauge invariance alone in 22/33 (rule-free).
  * With hidden composites they first appear at degree 12 (20 models), 15 (2) or 4 (2).

## 11819 — the Z6-II A8 class does not have the disease

**Rule.** Z6-II on G2 × SU(3) × SO(4) (same reference):
* plane 1: R¹ + 6γ ≡ −1 (mod 6);
* plane 2: R² ≡ −1 (mod 3);
* plane 3: R³ ≡ −1 (mod 2).

**Results** for the 9 Z6-II A8 Standard Models with the SM in SU(9), and for the Codex benchmark:
* **Up quarks.** The matrices are **hierarchical**: 0–4 cubic entries, with the rest at singlet degree 1–7. The benchmark has exactly **one** cubic entry, a single heavy top.
* **Down quarks.** Entries exist with ordinary hidden-neutral singlets (9–45 per model).

> **Why.** Z6-I has two planes with the same twist (⅙, ⅙). By the alternating-cubic theorem (11821b) these planes form a degenerate family pair. The Z6-II twists (⅙, ⅓, −½) are all different, so no plane pair is degenerate.

## 11820 — hidden confinement cannot rescue Z6-I

**Hidden gauge couplings.** The one-loop N = 1 coefficients b = 3C₂(G) − Σ T(R), with α_GUT = 1/24.5, give for the flagship:
* hidden **SU(5)**: b = 8, so **Λ/M_s ≈ 4.4 × 10⁻⁹**;
* the two hidden SU(2)s: not asymptotically free (b = −8, −11).

**Consequence for down masses.** Two sources are possible, and neither works:
* **From confinement:** composites at degree ≥ 12 give masses below ~10⁻⁵⁰ m_t.
* **From perturbative hidden-charged vevs:** m_b/m_t = 1/40 at degree 12 needs ⟨φ⟩/M_s ≈ **0.74**, which is outside perturbative control.

The Z6-I W(3,3) class therefore has **no realistic bottom or tau**. Together with m_t = m_c, it is **phenomenologically excluded**. This is consistent with Holotrade's exclusion of the class (b81ef8c) and sharper in mechanism.

## 11821 — SU(9) flavour unification: the theorems behind both

**(a) Three copies of minimal SU(9) flavour unification.** The W(3,3) T⁶/ℤ₃ vacuum 3(84) + 27(9̄) (Pass 11714) is three copies of the minimal anomaly-free three-generation SU(9) content **84 + 9 × 9̄**. This content is due to Frampton; see Chen et al. [arXiv:2108.08690](https://arxiv.org/abs/2108.08690) and [arXiv:2307.07921](https://arxiv.org/abs/2307.07921). Per copy:
* net tens = 4 − 1 = 3;
* net 5̄s = 9 − 6 = 3.

This is the "3 = 4 − 1" level count of Pass 11713.

**(b) THEOREM: the cubic is alternating.** T(x, y, z) = ε(x ∧ y ∧ z) on Λ³C⁹ is **alternating**: swapping two blocks of three indices gives the sign (−1)⁹. It was checked with the actual two-qutrit bracket. Consequences:
* **Families = copies.** The Yukawa matrix is M_ij = Σ_k ε_ijk h_k. It is antisymmetric, with singular values **(|h|, |h|, 0)**: a degenerate pair and a massless family.
* **Families = levels** (one copy). The renormalizable cubic vanishes, as Chen et al. note.

> **The two-qutrit SU(9) never gives a renormalizable, non-degenerate top Yukawa by itself.** The compactification geometry must split the copies. Z6-II does; Z6-I cannot.

**(c) THEOREM: the ℤ₉ centre.** Invariants need 3·n(84) − n(9̄) ≡ 0 (mod 9). So:
* 84 · 9̄ · 9̄ is **not** invariant;
* the minimal down-type operator is the **quartic** 84 · 9̄³, itself alternating in the three 9̄ copies.

> **The bottom Yukawa is structurally one field beyond the top's:** the top is the nine-level determinant 84³, while the bottom needs 84 · 9̄³.

## 11822 — Lean

`formal/W33/Pass11822SU9Flavour.lean` type-checks against the repository's Mathlib, with no `sorry`. It proves:
* the alternating-family Yukawa `skew h` satisfies `skewᵀ = −skew`, `skew · h = 0`, `det = 0` and `skew · skewᵀ = |h|² I − h hᵀ`, i.e. a degenerate pair plus a massless family;
* the ℤ₉-centre rule;
* the per-copy family counts.

## What this means for the TOE

The chain W(3,3) → two-qutrit E₈ → SU(9) flavour unification is consistent. Its two textbook obstacles are now exact theorems:
* the alternating top cubic;
* the ℤ₉ suppression of the bottom.

The viable branch has to break the copy symmetry geometrically: **Z6-II-type geometries with all twists distinct**, with families coming from planes whose twists differ.

**The Z6-I W(3,3) class is excluded** by its Yukawa sector.

## Scope

* **Necessary selection rules only.** No CFT amplitudes and no F/D-flat vacua.
* The confinement estimate uses one-loop running with α_GUT = 1/24.5.
* Classical background (cited, not claimed): SU(9) flavour unification (Frampton; Chen et al.), the R rule (Cabo Bizet et al.), and the 10D super-Yang–Mills untwisted Yukawas.

Passes 11823–11825 are released unused.
