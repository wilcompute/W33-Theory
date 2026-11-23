# Pass 12712: binary beats ternary 2.5× in on-chip energy, but PAM3 is the link optimum in a narrow band (which is why GDDR7 uses it); the exact RS spectrum puts the B′/hybrid degeneracy at kL = 6.5; Belle II at 10⁻⁷ tests all of B′; ternary training lands between binary and 2-bit with 44% zeros

Claude track. Follows Passes 12710–12711. **Not a theory of everything.**
- Script: `explore_pass12712_round.py` (≈15 s).
- Certificate: `data/explore_pass12712_round.json`.
- Tests: `tests/test_toe_pass12712.py`, 4 tests passing.

## (1) Energy per bit: on chip vs links

**On chip.**
- Every level gap needs the same transistor on/off ratio: V_gap = n(kT/q)ln10 × decades ≈ 0.39 V (n = 1.3, 5 decades).
- The swing is therefore (r − 1)V_gap, and the energy per bit ∝ (r − 1)²/log₂r.

| r | swing | thermal floor (1 fF, error rate 10⁻¹⁵) | energy/bit vs binary |
|---|---|---|---|
| 2 | 0.39 V | 32 mV | 1.00 |
| 3 | 0.77 V | 65 mV | **2.52** |
| 4 | 1.16 V | 98 mV | 4.50 |

**Binary wins on-chip logic by 2.5×** whenever the supply voltage can be scaled. Thermal noise is not the binding constraint; the subthreshold slope is.

**Links.**
- Bandwidth, not energy, is scarce in a link.
- The margin is −20log₁₀(r − 1) − α·D/(2b_r), with b = 1 (NRZ), 1.5 (PAM3, 3 bits per 2 symbols) and 2 (PAM4).
- Result: NRZ is best below 36/α Gb/s, **PAM3 in 36–42/α**, PAM4 above.
- At α ≈ 1 dB/GHz (illustrative) PAM3's window is 36–42 Gb/s per pin. **GDDR7 (32–48 Gb/s per pin), USB4 v2 and Thunderbolt 5 ship PAM3.**
- So ternary signalling is in mass production today, and this simple margin model reproduces why: it is optimal in a narrow band of loss × data rate.

## (2) Light Q+U without tuning: a candidate mechanism
- The generalised missing-partner mechanism ([arXiv:2308.11705](https://ar5iv.labs.arxiv.org/html/2308.11705)) splits the colour components of vectorlike SU(5) 10-plets from the electroweak ones without fine-tuning.
- Q + U are exactly the coloured part of a 10. If it embeds in E₆, it removes the (M_VL/M_GUT)² ~ 10⁻²⁷ penalty of Pass 12710, and the hybrid becomes the best-supported completion (Bayes factor 0.1–0.75).
- The embedding is open.

## (3) The exact RS graviton spectrum (replaces the interpolation of Pass 12710)
- **Spectrum:** the first mode is the root of J₁(x e^{−kL})Y₁(x) − Y₁(x e^{−kL})J₁(x) = 0, with m₁ = x₁ k e^{−kL}.
- **Inputs:** the spacing is held at m₁ = 1 eV, and M_Pl² = (M₅³/k)(1 − e^{−2kL}).

| kL | x₁ | M₅ (GeV) | y′ (SM on UV brane) |
|---|---|---|---|
| 0 (flat) | — | 9.8×10⁸ | 0.5050 |
| 1 | 5.143 | 1.5×10⁹ | 0.4973 |
| 3 | 3.860 | 3.1×10⁹ | 0.4859 |
| 5 | 3.832 | 6.1×10⁹ | 0.4763 |
| 7 | 3.832 | 1.2×10¹⁰ | 0.4677 |
| 10 | 3.832 | 3.2×10¹⁰ | 0.4565 |

**The warped B′ meets the hybrid's y′ = 0.470 at kL = 6.46** (the interpolation gave ~7). If FCC measures y′ ≈ 0.47, that alone cannot tell the hybrid from a warped B′. Belle II can.

## (4) B′ forecast (Monte Carlo over its surviving parameter space)
**Priors:**
- log λ ∈ [−4, log₁₀ 2.3×10⁻³];
- T_RH log-uniform within its window;
- m_Φ ∈ [11, 100] GeV, log prior;
- |A_CP^dark| ∈ [0.1, 1], log prior.

**Results:**
- **Required BR:** median 1.0×10⁻⁶, 90% range 2.1×10⁻⁷ – 4.9×10⁻⁶.
- **Fraction testable:** 50% at a reach of 10⁻⁶ and **100% at 10⁻⁷**. Belle II's projected reach (~10⁻⁷) **covers all of B′**, modulo the exclusive-to-inclusive fraction of B → ψ + baryon modes.
- **y′ (flat dimension, with the mediator's gauge shift):** 0.493–0.509. FCC separates this from the hybrid at ≥ 3σ across all of flat B′, and at ≥ 5σ across half of it.

## (5) Ternary training (quantisation-aware, numpy)
**Task:** a teacher MLP (32-64-10, tanh) is learned by a student (32-128-10, ReLU), with 6000 training and 3000 test samples, 60 epochs, a straight-through estimator and 3 seeds. The task is deliberately hard; full-precision accuracy is 0.56.

| weights | test accuracy | bits/weight | zero weights | multiplications |
|---|---|---|---|---|
| fp32 | 0.562 ± 0.002 | 32 | 0% | yes |
| binary (sign·α) | 0.523 ± 0.011 | 1 | 0% | none |
| **ternary (TWN, 0.7 mean\|w\|)** | **0.538 ± 0.005** | 1.58 | **44%** | **none** |
| 2-bit | 0.552 ± 0.003 | 2 | 0% | yes |

- **Accuracy:** ternary recovers about 40% of the gap between binary and full precision, sitting between binary and 2-bit.
- **Compute:** it keeps binary's multiplication-free arithmetic and skips 44% of the additions as well, consistent with the single-layer estimate of Pass 12711 (46%).

## Status
- **B′:** fully testable by Belle II at 10⁻⁷, and by FCC if the dimension is flat. A warped dimension degenerates with the hybrid at kL ≈ 6.5.
- **Hybrid:** hinges on embedding the generalised missing-partner mechanism in E₆.
- **Ternary:** it wins in links (PAM3) and in neural-network weights. It loses in on-chip logic.
