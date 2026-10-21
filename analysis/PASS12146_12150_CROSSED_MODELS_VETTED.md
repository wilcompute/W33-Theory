# Passes 12146–12150: two vetted candidate models, flavour, Witten parity, S002's minimum at 1/√3, the βθ congruence

Claude track. Producer: `analysis/w33_pass12146_to_12150_crossed_models_vetted.py`. Drivers and frozen outputs:
`analysis/search_drivers_12146/`.

## Headline

**A8SM_10006 and A8SM_16222** (from the 104 A8 models of Pass 11095), under a fraction-free hypercharge with k_Y = 17/3, are:

- fraction-free, with three generations;
- a single heavy top **and** bottom, with |V_tb| = 1;
- free of Witten-protected exotics;
- free of light vector-like exotics up to quartic order;
- Λ > 0;
- tachyon-free down to Im T_WL = 1.5.

These are the best-vetted candidates so far. Caveats: quartic lifts are upper bounds (H-momentum is not imposed at
quartic order); charm and lighter masses come at next order; the vacuum is not stabilised (Λ > 0, dilaton tadpole).

## 12146: vetting the 16 crossed models of 12145

**Vacuum and tachyons.**

- One-loop Λ/M⁴ (11106 engine, T_WL = 2i, T\* = ρ) lies in [643.7, 703.0]: all positive.
- 12 of 16 are tachyon-free down to Im T_WL = 1.5 (11107 enumerator).
- Four are tachyonic at 1.5: A8SM_1295 and 17724 (Δ = −0.0028), 5110 and 6052 (Δ = −0.067).

**Exotics to quartic order** (12133 method). A8SM_10006 (11 → 0) and A8SM_16222 (15 → 0) keep no light vector-like
pair. The other 14 keep between 3 and 15.

## 12147: flavour

- In the 12 models with a single heavy top **and** bottom, the two heavy directions coincide in the light-Q space:
  **|V_tb| = 1**.
- Adding quartic Q·u·H·⟨s⟩ terms (an upper bound) raises the up-type rank from 1 to 3 in all 16. So charm and up arise
  one order higher: m_c/m_t ~ ⟨s⟩/M.

## 12148: Witten parity

- In all 16 models every SM-singlet scalar has mm = 0, so mass terms cannot cross Witten-parity sectors.
- 10 models therefore carry exactly protected vector-like pairs, some of them colour triplets.
- Six carry none: 10006, 16222, 17724, 4168, 438 and 6052.

## 12149: S002's minimum is the point where 56 states become massless

**Potential** (T\* = ρ):

| Im T_WL | 0.52 | 0.55 | 0.58 | 0.6 |
|---|---|---|---|---|
| Λ/M⁴ | 117.27 | 115.39 | **115.14** | 115.77 |

**Lowest Witten-sector level** (a 56-state multiplet):

| Im T_WL | 0.7 | 0.62 | 0.58 | 0.56 | 0.55 | 0.54 | 0.5 | 0.4 |
|---|---|---|---|---|---|---|---|---|
| Δ_min | 0.0062 | 0.00085 | 3.5·10⁻⁶ | 0.00016 | 0.00039 | 0.00075 | 0.0035 | 0.023 |

At **Im T_WL = 1/√3 exactly, Δ = −4·10⁻¹⁶: the 56 states are massless.**

The potential minimum sits at this point. That matches the familiar stationarity of string potentials where extra states
become massless. 1/√3 is 1/3 of the critical radius √3 that 11107 found for A8 models; that relation is observed, not
yet explained.

**Instability.** Off the axis these states turn tachyonic: the B-field direction (CP-odd, 12141) is unstable.

## 12150: the βθ obstruction as a lattice congruence

**The congruence.** A colour-singlet βθ state at fixed point f has Q = v·π + v·U_f, with U_f = V0 + V1 + Σ c_i W_i. So
it is integral iff v·U_f ∈ Z. On all 1080 k_Y = 5/3 candidates (A8 + S002 + T115) this congruence reproduces the direct
test exactly.

**The finite check.** No admissible root has v·(V0 + V1) and every v·W_i integral: 0 of 1080.

- In 982 candidates the obstruction is v·(V0 + V1), with residues 1/6, 1/3, 1/2, 2/3, 5/6.
- In the other 98 it is a Wilson-line residue of 1/3 or 2/3.

The 1104/1104 failure of 12143 therefore reduces to one lattice congruence and a finite check over roots.
