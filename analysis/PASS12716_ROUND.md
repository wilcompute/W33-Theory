# Pass 12716: a gauged-SO(10) "Goldstones instead of fine tuning" construction leaves exactly Q + U (18 multiplets); only a Z₁₀ with (H̄H)⁵ protects it to dimension 11; a Planck-suppressed quartic spoils unification unless its cutoff is ~10¹⁷; FCC odds reach ~45:1 either way; ternary crossbars and ternary Hamming codes do not beat binary per operation or per SNR

Claude track. **Not a theory of everything.**
- Script: `explore_pass12716_round.py` (≈1 min).
- Certificate: `data/explore_pass12716_round.json`.
- Tests: `tests/test_toe_pass12716.py`, 5 tests passing.

## (0) Gauged-SO(10) Goldstones instead of fine tuning (computed)
- **Setup:** two sectors with no cross-couplings in W:
  - Σ (a 45, VEV along B−L), whose broken generators give 30 Goldstones;
  - H + H̄ (16 + 16̄, VEV → SU(5)), whose broken generators give 21: 10 + 10̄ + 1.
- **Symmetry:** the two sectors have an accidental SO(10)_Σ × SO(10)_H, of which the diagonal SO(10) is gauged.
- **Eaten:** gauged SO(10) → SM, 33 generators.
- **Uneaten:** 30 + 21 − 33 = **18 = (3,2)_{±1/6} + (3̄,1)_{∓2/3}**, which is exactly vectorlike Q + U.
- **This is a complete, gauge-consistent version of the Pass 12714–12715 mechanism**, and it sits inside the E₆ hybrid (E₆ ⊃ SO(10)).

## (1) Can a discrete symmetry protect the accidental symmetry?
**Search space:**
- Z_N with N ≤ 30, both non-R and R.
- Σ-sector templates {Σ², Σ⁴} and {XΣ², Σ⁴, X³}.
- H-sector templates Y·(H̄H)ⁿ (Y has no VEV).
- Violating operators H̄ΣᵏH(H̄H)^c X^a and products of two such cores.

| H sector | best minimal violating dimension, non-R (N) | R (N) |
|---|---|---|
| Y·H̄H (n = 1) | 4 (2) | 4 (2) |
| n = 2 | 5 (2) | 5 (2) |
| n = 3 | 8 (6) | 4 (2) |
| n = 4 | 9 (4) | 5 (2) |
| **n = 5** | **12 (Z₁₀)** | 4 (2) |

Both Σ templates give the same results.

- **Theorem (n = 1):** when H̄H appears linearly, H̄Σ²H carries the charge of the allowed Σ² term, so violation at dimension 4–5 is unavoidable. Higher powers push it to about 2n + dim(Σ-monomial).
- **Result:** **only a non-R Z₁₀ with an H-sector driven by (H̄H)⁵ meets the quality requirement** (dimension ≥ 11). The construction is possible but contrived. Alternatives are gauged U(1)′s or geometric separation of the sectors, for example on different branes, which is natural in an extra dimension.

## (2) Unification with the pseudo-Goldstone spectrum
- The 45's LR-adjoint remnants (8,1) + (1,3) sit at 2m, with m = λa²/M.
- Pass 12705's two-loop machinery, with the hybrid reference δ = +0.26:

| λ | cutoff M | octet + triplet mass | M₁₂ | δ |
|---|---|---|---|---|
| 1 | M_Pl | 1.4×10¹⁵ | 1.4×10¹⁸ | +1.25 |
| 4 | M_Pl | 5.5×10¹⁵ | 3.1×10¹⁷ | +0.84 |
| 4π | M_Pl | 1.7×10¹⁶ | 9.6×10¹⁶ | +0.50 |
| 1 | 10¹⁷ | 3.4×10¹⁶ | 4.9×10¹⁶ | +0.31 |
| ≥ 4 | 10¹⁷ | ≥ 10¹⁷ | 4.1×10¹⁶ | +0.26 |

- **A Planck-suppressed quartic spoils unification**, as the octet and triplet are too light; this is the same issue as Pass 12705.
- **The quartic needs a cutoff of about 10¹⁷ GeV** (a heavy 54 or another renormalisable completion), or strong coupling λ ~ 4π.

## (3) Ternary compute-in-memory crossbars
- **Model:** E_w = E_cell + E_ADC/rows.
  - ADC Walden figure of merit 10–50 fJ per conversion step, capped at 8 bits.
  - Binary: one device.
  - Ternary: two differential devices; a zero draws no current.
- **Results:**
  - Binary: 0.011–0.052 pJ per weight-op.
  - Ternary: 0.011–0.10 pJ, equal to binary only when the ADC saturates its 8-bit cap (256 rows).
- **In analog crossbars ternary is not cheaper per operation**; it needs a wider ADC range and twice the devices.
- **Correction to Pass 12715's framing:** its 0.073 pJ/bit threshold applies to digital weight-stationary arithmetic, not analog crossbars. In a crossbar, ternary's case rests on accuracy per operation (Pass 12712), not energy.

## (4) FCC posterior odds (hypothetical measurements at M_VL = 3 TeV)

| truth | y′_obs | σ_meas | BF hybrid vs generic VLQ | BF B′ vs generic | posterior odds (hybrid : B′ : generic) |
|---|---|---|---|---|---|
| hybrid | 0.453 | 0.005 | **46** | ≈ 0 | 35 : 0 : 1 |
| hybrid | 0.453 | 0.002 | 51 | ≈ 0 | 39 : 0 : 1 |
| B′ | 0.490 | 0.005 | ≈ 0 | **43** | 0 : 1.9 : 1 |
| B′ | 0.490 | 0.002 | ≈ 0 | 46 | 0 : 2.0 : 1 |

- **A 3 TeV partner with a measured y′ decides between the hybrid and B′ completely**, with Bayes factors of about 45.
- **The hybrid would then be strongly favoured overall (35–39 : 1).** B′, which starts with a small prior (0.044), would reach only about 2 : 1 against a generic vectorlike quark.

## (5) Ternary vs binary Hamming codes (equal cell noise and swing)

| SNR | binary (127,120): info/cell, block failure | ternary (121,116): info/cell, block failure |
|---|---|---|
| 8 | 0.945, 8×10⁻⁶ | 1.519, 0.88 |
| 10 | 0.945, 7×10⁻¹⁰ | 1.519, 0.26 |
| 14 | 0.945, 7×10⁻¹⁵ | 1.519, 7×10⁻⁴ |

- **Ternary cells store 61% more information but need about 6 dB more SNR for the same reliability.** This is the same trade-off as channel capacity (Pass 12711): favourable only when SNR is plentiful and density is precious, as in multi-level flash.

## Status
- **Hybrid:** has a complete gauged-SO(10) construction for light Q + U. It needs:
  - a Z₁₀ with (H̄H)⁵, or sector separation, to solve the quality problem;
  - a quartic cutoff of about 10¹⁷ to protect unification.
- **FCC at 3 TeV would settle hybrid vs B′ decisively.**
- **Ternary:** its wins are confirmed in signalling (PAM3) and in digital weight-stationary inference. It loses in analog crossbars per operation and in ECC per SNR.
