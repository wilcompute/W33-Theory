# Pass 11949: the axiflavon fails the quality test — correction to Passes 11947/11948

Producer: `analysis/w33_pass11949_axiflavon_quality_fails.py`
Certificate: `data/w33_pass11949_axiflavon_quality_fails.json`
Regression: `tests/test_w33_pass11949.py`
Track: Claude. Tests the strong-CP reading of Pass 11947 and withdraws it.

## 1. Explicit breaking

**The residual.** Pass 11947 showed that arg det Y_u = 3·arg ε_u + O(|ε|²), and that quark observables move by at most
3·10⁻³ under arg ε_u → arg ε_u + φ. That residual is fatal.

**Why it exists.** The even vectors f₀ and f₂ are not orthogonal, so the holomorphic ε² term breaks the Froggatt–Nielsen
U(1) explicitly.

**Measured.** Over a full turn of φ the top Yukawa is modulated as a pure second harmonic, cos(2φ + α):
* relative amplitude **5.2·10⁻⁶** (fit A) and **2.0·10⁻⁶** (fit B);
* the fourth harmonic is below 10⁻⁹.

## 2. Size

| | potential |
|---|---|
| top-quark Coleman–Weinberg term, (3/16π²)·4m_t⁴·δ | 3.5·10² GeV⁴ (A), 1.3·10² GeV⁴ (B) |
| same, with TeV-scale supersymmetry cutting off the ultraviolet | about 1 GeV⁴ |
| QCD axion potential, χ ≈ (75 MeV)⁴ | 3·10⁻⁵ GeV⁴ |
| quality bound, about 10⁻¹⁰·χ | 3·10⁻¹⁵ GeV⁴ |

The breaking exceeds the quality bound by **10¹⁶–10¹⁷** (10¹⁴–10¹⁵ with supersymmetry).

## 3. Where it lands

The top loop fixes arg Ω₁₂ at its own extrema:

| | minima of m_t | maxima of m_t |
|---|---|---|
| θ̄, fit A | −3.11, 0.04 | 1.61, −1.53 |
| θ̄, fit B | −1.80, 1.34 | −0.23, 2.91 |

None is anywhere near 10⁻¹⁰.

**Conclusion.** arg Ω₁₂ is **not** a viable QCD axion.

**What is withdrawn.**
* The strong-CP reading of Pass 11947.
* The axion prediction of Pass 11948 (f_a ≈ 4–5·10¹⁵ GeV, m_a ≈ 1.1–1.5 neV), as a solution to strong CP.

**What stands.**
* The rephasing structure (arg det Y_u = 3·arg ε + O(|ε|²)).
* The f_a formula, as a statement about the modulus.

The strong-CP problem of the theta-null flavour chain is therefore **open again**.

## 4. Observation (two fits, not derived)

At every extremum of m_t(φ), arg det Y_u = ±π/4 or ±3π/4 to about 1% (0.776 and −2.366, against 0.785 and −2.356).

## What would rescue it

* **A symmetry.** An exact symmetry that forbids the ε² admixture into the leading Yukawa, for example f₀ ⊥ f₂ at a
  special τ. None is known here.
* **Another mechanism.** A strong-CP mechanism that does not rely on this phase, such as a separate axion or a
  Nelson–Barr structure.

## Lesson

An approximate rephasing that leaves observables fixed to 10⁻³ is not an axion candidate. Quality needs the explicit
breaking to be below about 10⁻¹⁷ of the Yukawa, so this should have been tested before Pass 11948 quantified f_a.
