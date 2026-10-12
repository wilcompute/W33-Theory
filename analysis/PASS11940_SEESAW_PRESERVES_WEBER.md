# Pass 11940: the Weber invariant is seesaw-invariant

Producer: `analysis/w33_pass11940_seesaw_preserves_weber.py`
Certificate: `data/w33_pass11940_seesaw_preserves_weber.json`
Regression: `tests/test_w33_pass11940.py`
Track: Claude. Corrects and completes Pass 11939.

## Correction to Pass 11939

**What 11939 cannot mean.** Its relation m₁m₃/m₂² = m_u m_t/m_c² was phrased as "one swap-symmetric home". A shared
**Ω** cannot be meant.

**Why.** If the Weinberg coefficient and the up coupling were theta nulls of the same Ω, they would be proportional.
The whole spectra would then coincide: m₂/m₃ = m_c/m_t = 3.6·10⁻³, against the measured 0.173, a factor of 48.

**What the relation actually needs.**
* a **shared τ**, the complex structure of the two elliptic factors, which fixes the Weber invariant;
* a **channel-specific Ω₁₂**, the hierarchy parameter.

11939 named no mechanism for this.

## The mechanism: the type-I seesaw

**Setting.** m_ν = Y_D M⁻¹ Y_D. Both the Dirac coupling Y_D and the Majorana coupling M are theta nulls of
swap-symmetric homes with the **same τ**, each with its own Ω₁₂ (ε_D, ε_M).

**Why it works.** The heat-equation coefficients x^k/k! of Pass 11938 compose: x_ν = x_D²/x_M. Hence:
* **R_ν = m₁m₃/m₂² = R(τ) = |𝔣(τ)|¹⁶/4**, the same Weber invariant. Measured: relative error ≤ 2.6·10⁻⁴ for
  ε_M ≤ 10⁻², and 2.6·10⁻² at ε_M = 0.1, i.e. an O(ε_M) correction.
* **ε_ν = ε_D²/ε_M**: m₂/m₃ agrees with κε_D²/ε_M to 10⁻⁴ (κ = 0.6675 at the home τ = 1 + 0.874i of Pass 11939).

**Reading.** The complex structure is universal; the hierarchy parameters are channel-specific. That is what the
11939 relation needs. The assumption of 11939 therefore becomes: **the Dirac and Majorana couplings are theta nulls
with the same τ as the up coupling.**

## Right-handed spectrum (with Y_D = Y_u)

**Setting.** SO(10)- or Pati–Salam-type Dirac unification.

**Spectrum.** M_i = m_{u,i}²/m_{ν,i} gives

| | M₁ | M₂ | M₃ |
|---|---|---|---|
| GeV (M_Z-scale inputs; running moves these by O(1) factors) | 1.9·10⁶ | 4.4·10¹⁰ | 5.7·10¹⁴ |

**The same invariant again.** M₁M₃/M₂² = R(τ) = 0.538: one Weber invariant governs all three matrices.

**Leptogenesis.**
* **N₁ fails.** M₁ is far below the Davidson–Ibarra bound (~10⁹ GeV), so N₁ thermal leptogenesis fails.
* **The relevant literature.** This is the SO(10)-inspired structure. Its N₂-dominated leptogenesis (arXiv:1012.2343)
  allows, for normal ordering, m₁ ≈ 1–5 meV or 30–100 meV. The supersymmetric version (arXiv:1512.06739) allows
  10–30 meV.
* **Where we land.** Our m₁ = 0.80 meV (0.67–0.97) sits **just below** the lower non-SUSY window.
* **Status.** This is recorded as a tension, not a success. It could move with running, with the up-mass error, or
  with a Dirac–charged-lepton misalignment; that is not computed here.

## Scope

**Exact or numerical (to the stated precision).**
* The seesaw composition of the heat-equation coefficients.
* The preservation of R.
* ε_ν = ε_D²/ε_M.

**Assumed.**
* Shared τ across the Dirac, Majorana and up couplings.
* Swap-symmetric homes.
* Leading order in Ω₁₂.
* Y_D = Y_u, used for the right-handed spectrum only.

**Classical part.** Seesaw relations of the form M_i = m_D²/m_ν in a common basis are classical. The new step is that
the theta-null structure supplies the common basis and the common invariant.
