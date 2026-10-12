# Pass 11936: the radial weld — the E8 displacement is the top/charm hierarchy parameter, with Schmidt exponents (0, 1, 1)

Producer: `analysis/w33_pass11936_radial_weld.py`
Certificate: `data/w33_pass11936_radial_weld.json`
Regression: `tests/test_w33_pass11936.py`
Track: Claude.

## Inputs

* The Cartan → Siegel inversion (Coble/Maschke matching) of Passes 11879 and 11891.
* The level-3 theta two-qutrit Yukawa of Passes 11869 and 11872: θ-nulls of Ω, reshaped 3×3.
* The selected tangent direction of Pass 11935: the log(8/5) Clifford orbit.
* The essential scaling of the parallel packet 8407e70cf: log t* = −κ/(32r) − 1/2 − C_G/16, with κ = 7.211 and
  C_G = 3.693.

## Result

**Method.** Displace the vev to c = (1, t·u), invert to Ω(t) (residuals ≤ 10⁻¹³), and take the theta Yukawa's singular
values, normalised to the largest.

| direction | singular values | log-slopes |
|---|---|---|
| selected log(8/5) orbit | (1, 0.465t, 0.370t) | 1.00, 1.00 |
| generic mixed direction | (1, 0.369t, 0.259t) | 1.00, 1.00 |
| near the stabiliser | (1, 0.133t, 0.128t) — the two coefficients merge (the lock) | 1.00, 1.00 |

**How Ω moves.** Im Ω_max grows like (3/π) ln(1/t). The vev runs to a one-dimensional cusp.

**Special directions.**
* The strange direction leaves Ω fixed.
* The stabiliser direction, and some directions with no e₁ component, run into a deeper cusp. There Im Ω ≈ 20–30, and the
  pair is locked and numerically degenerate.

## Reading

**What works.** The essential scaling t ∝ exp(−κ/32r) is the **top/charm hierarchy parameter**. m_c/m_t = 0.465t matches
the data (3.6·10⁻³) at t ≈ 7.8·10⁻³, i.e. a soft-supertrace ratio **r ≈ 0.055**. A modest dimensionless input produces
the top/charm hierarchy by dimensional transmutation.

**What does not.** Near a Witting ray the degeneration is a one-dimensional cusp, with exponents (0, 1, 1). So
m_u/m_c = b/a is fixed by the direction: **0.80** on the selected orbit, against 2·10⁻³ in the data. The up/charm
hierarchy needs a second small parameter, for example a second, slower displacement towards a corner cusp. That is the
open target.
