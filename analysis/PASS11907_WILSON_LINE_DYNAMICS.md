# Pass 11907: dynamics of the relative Wilson line

Producer: `analysis/w33_pass11907_wilson_line_dynamics.py`
Certificate: `data/w33_pass11907_wilson_line_dynamics.json`
Regression: `tests/test_w33_pass11907.py` (about 2.5 min)
Track: Claude.

## Input

Pass 11906 established the exact magnetized texture for a localised Higgs:
|Y_c(ζ)| = C e^{−(3π/2)(Im ζ)²/Im τ} |θ[c/3,0](3ζ, 6τ)|.
* The Gaussian prefactor was fitted to the direct overlaps at seven points (ln f linear in (Im ζ)²/Im τ, slope
  −3π/2, to 10⁻⁹).
* With it, F_p = Σ_c |Y_c|^p is invariant under ζ → ζ + 1/3, ζ → ζ + 2τ/3 and ζ → −ζ (10⁻¹⁶).
* Units: C = 1, so the top coupling at ν = 0 is about 1. The meaningful coefficient below is therefore r y_t².

## 1. The minimal potential selects degenerate textures

V = ±F₂ is the two-loop vacuum energy with the light Higgs. For each of τ = 1.3i, 0.1+1.3i, 0.3+0.9i and 2i:

| | location | spectrum |
|---|---|---|
| global maximum | ζ ≡ 0 | (1, ε, ε), so m_c = m_u |
| global minimum | the theta-zero point ζ = 1/6 + τ/3 | (0, 1, 1), i.e. a massless state with the other two equal |

Either sign therefore selects a degenerate texture. This is the dynamical version of Pass 11905.

## 2. Competing quadratic and quartic terms select a hierarchy

Take V = −F₂ + r F₄ at Im τ = 4.209.
* **The symmetric point destabilises.** ν = 0 loses stability exactly at **r = 1/2**, where the Hessian changes sign.
* **Generic vacua.** For every r > 1/2 tested (0.6, 0.8, 1, 2, 5, 8), the global minimum sits at a **non-symmetric**
  ν(r). It increases monotonically from 0 towards 1/3, and the spectrum is non-degenerate and hierarchical.
* **The observed up ratios.** The vacuum gives m_c/m_t = 3.6·10⁻³ and m_u/m_c = 1.7·10⁻³ at **r* = 0.890**, an O(1)
  coefficient. No hierarchy is put in by hand: Im τ fixes the product m_u m_c/m_t², and r selects the split.
* **The opposite sign.** +F₂ − r F₄ keeps degenerate minima.

## Reading

Two earlier results said the hierarchy cannot come for free:
* it is not selected by symmetry (11905);
* the minimal light-Higgs potential selects degenerate textures.

This pass shows what does select it. A **generic competition between the quadratic and quartic Yukawa terms** with
r y_t² > 1/2 places the Wilson line at a non-symmetric point. The observed up hierarchy is such a vacuum, with
r y_t² ≈ 0.89 and Im τ ≈ 4.2. So the magnetized two-qutrit home has a natural dynamical mechanism for the up
hierarchy.

## Not established

* **Coefficients.** The coefficients are not derived: loop factors, supersymmetry breaking, and the other sectors'
  contributions. So this is a mechanism with an O(1) parameter, not a prediction.
* **Scope.** Down and lepton sectors, the CKM, and the Higgs-mode alignment (TOE48 front 2) are not included.

## Prior art

* Corpus: 11904–11906.
* TOE46 and TOE48 (parallel track: equal-background lock; Higgs-mode potential).
* Cremades–Ibáñez–Marchesano.
* Moduli-dependent Yukawa potentials, generally.
