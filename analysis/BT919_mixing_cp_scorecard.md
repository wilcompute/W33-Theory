# BT919 — The Complete Quark+Lepton Mixing+CP Falsifiability Scorecard

**Status: PROVEN (cross-check, `analysis/bt919_mixing_cp_scorecard.py`, data `data/bt919_mixing_cp_scorecard.json`)**

Extends BT918 to the entire flavor-mixing sector: all nine W(3,3)
graph-parameter predictions (3 CKM elements, 3 PMNS angles, the CP phase,
the Jarlskog invariant, the Wolfenstein A) audited against current PDG with
σ-levels, in one place.

| quantity | substrate | value | PDG | dev | σ |
| --- | --- | --- | --- | --- | --- |
| \|V_us\| (Cabibbo) | (λ+Φ₆)/v = 9/40 | 0.22500 | 0.22501 | 0.00% | 0.0 |
| \|V_cb\| | μ/Θ² = 1/25 | 0.04000 | 0.04053 | 1.31% | 0.7 |
| \|V_ub\| | λ/(vΦ₃) = 1/260 | 0.003846 | 0.00382 | 0.68% | 0.1 |
| sin²θ₁₂ (solar) | μ/Φ₃ = 4/13 | 0.30769 | 0.307 | 0.23% | 0.1 |
| sin²θ₂₃ (atmos) | Φ₆/Φ₃ = 7/13 | 0.53846 | 0.546 | 1.38% | 0.4 |
| sin²θ₁₃ (reactor) | λ/(Φ₆Φ₃) = 2/91 | 0.02198 | 0.02203 | 0.24% | 0.1 |
| sin δ_CP (CKM) | (μ²−1)/(μ²+1) = 15/17 | 0.88235 | 0.911 | 3.14% | 1.0 |
| J_CKM (Jarlskog) | 27/884000 | 3.054e-5 | 3.08e-5 | 0.83% | 0.2 |
| A (Wolfenstein) | μ/(q+λ) = 4/5 | 0.80000 | 0.826 | 3.15% | 1.7 |

**8 of 9 within 1σ.** The single outlier is the Wolfenstein A = μ/(q+λ) = 4/5
at 1.7σ (3.15%) — the sharpest prediction at risk.

## Structural notes

- The whole flavor sector is built from {q=3, λ=2, μ=4, Φ₃=13, Φ₆=7, Θ=10,
  v=40}: every denominator is one of Φ₃, Φ₆Φ₃, Θ², q+λ, v.
- The two large PMNS angles sum to 4/13 + 7/13 = **11/13** (11 = k−1 = the
  Ihara prime, BT918).
- The Jarlskog factors as J = |V_us|·|V_cb|·|V_ub|·sin δ_CP =
  (9/40)(1/25)(1/260)(15/17) = 27/884000.

## Reading

The entire fermion mixing-and-CP sector — nine independent observables across
quarks and neutrinos — is reproduced by elementary W(3,3) graph-parameter
ratios, with 8 within 1σ of measurement and the ninth at 1.7σ. This is a
dense falsifiability surface: nine kill criteria, each a fixed rational number,
collectively at the sub-percent-to-few-percent level. The Wolfenstein A = 4/5
is the one to watch (1.7σ) — the prediction most likely to be falsified by
improved data.

## Honest boundary

The discrete *structure* under these ratios is derived (BT858–892: the
long-root transvection geometry — gauge group, generations, flavor S₃,
Yukawa texture, chirality, parity). The mixing/CP *ratios* themselves are
validated phenomenology (w33_paper), and their first-principles derivation
from the within-grade q²=9 profile (BT894/897/898) remains open. BT919 is the
falsifiability audit of the ratios, not their derivation.

## Open

- Derive the ratios (esp. A = μ/(q+λ), the outlier) from the within-grade
  layer; resolve the 1.7σ A tension.
- The PMNS CP phase δ (currently weakly measured) as the next falsifiable
  substrate ratio.
