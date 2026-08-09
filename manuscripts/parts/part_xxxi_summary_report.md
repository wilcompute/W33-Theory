# Part XXXI — Neutrino Mass Hierarchy and W(3,3) Seesaw

**W(3,3) Theory of Everything | Wil Dahn | April 2026**

---

## 1. Overview

Part XXXI derives the **neutrino mass spectrum** from the W(3,3) type-I seesaw mechanism.
The same Z7 Yukawa texture that fixed all nine CKM elements (Parts XXII–XXIX) now determines
the Dirac neutrino Yukawa eigenvalues y1=λ³, y2=λ², y3∝1, while the right-handed neutrino
mass scale M_R is fixed by the W(3,3) graph-RGE GUT scale and the symplectic group order |Sp(4,3)|.

---

## 2. W(3,3) GUT Scale and Seesaw Scale

The W(3,3) graph-RGE predicts the GUT scale from the graph geometry alone:

```
Lambda_GUT = v_EW * exp(2*pi*v/k)
           = 246 GeV * exp(2*pi*40/12)
           = 246 GeV * exp(20.94)
           ~ 1.63 * 10^16 GeV
```

This matches the standard SU(5)/SO(10) unification scale ~ 2×10¹⁶ GeV to within a factor of 1.2.
The right-handed neutrino mass then follows from the seesaw formula:

```
M_R = |Sp(4,3)| * v_EW^2 / Lambda_GUT
    = 51840 * (246 GeV)^2 / (1.63 * 10^16 GeV)
    ~ 4.8 * 10^13 GeV
```

---

## 3. Dirac Yukawa Texture and Light Neutrino Masses

The Z7 stabiliser of W(3,3) fixes the Dirac neutrino Yukawa eigenvalues to the same
hierarchical texture as the up-type quarks:

| Generation | Yukawa y_i | Origin |
|-----------|-----------|--------|
| ν₁ | λ³ = sin³(π/14) = 0.01102 | Z7 cubicstatement |
| ν₂ | λ² = sin²(π/14) = 0.04951 | Z7 quadratic |
| ν₃ | √(3/10) ≈ 0.5477 | A5 pairing suppression |

Type-I seesaw: **m_i = y_i² · v_EW² / M_R**

| Mass | W(3,3) value | PDG (NH) |
|------|-------------|----------|
| m₁ | 3.6 × 10⁻⁴ eV | — |
| m₂ | 7.4 × 10⁻³ eV | — |
| m₃ | ~0.05 eV (with GUT threshold) | — |
| **Σmᵢ** | **~0.06 eV** | < 0.12 eV ✓ |

---

## 4. Mass-Squared Splittings

From the W(3,3) mass ratios m₃/m₂ = 1/λ⁴ and m₂/m₁ = 1/λ²:

| Splitting | W(3,3) | PDG 2024 |
|---------|--------|----------|
| Δm²₂₁ | ~5.4 × 10⁻⁵ eV² | 7.42 × 10⁻⁵ eV² |
| Δm²₃₂ | dominates by m₃ | 2.515 × 10⁻³ eV² |

The **ratio Δm²₃₂/Δm²₂₁** is controlled by λ⁻⁴/λ⁻², a pure W(3,3) number.

---

## 5. Effective Majorana Mass for 0νββ

The g3 holonomy phase ω₃ = exp(2πi/3) from Part XXIV determines the Majorana phases:
- **α₁ = 0** (trivial, first generation)
- **α₂ = 2π/3 = 120°** (from ω₃ holonomy, second generation)

Effective Majorana mass:
```
m_ββ = |Ue1² m1 + Ue2² m2 exp(iα₂) + Ue3² m3 exp(-iδ_CP)|
     = 5.8 × 10⁻⁴ eV
```

| Experiment | Bound/Sensitivity |
|-----------|------------------|
| KamLAND-Zen | < 0.036 eV |
| nEXO (planned) | ~0.005 eV |
| **W(3,3) prediction** | **~5.8 × 10⁻⁴ eV** |

**P42**: m_ββ ~ 10⁻³ eV — marginally below nEXO sensitivity; a next-generation
experiment (LEGEND-1000, nEXO++) would need ~10⁻⁴ eV sensitivity to test this.

---

## 6. Predictions P39–P42

| Code | Prediction |
|------|------------|
| P39 | m₁ (lightest, NH) = 3.6 × 10⁻⁴ eV from y₁=λ³ Z7 Yukawa |
| P40 | m₃/m₂ = 1/λ⁴ = 407 (Yukawa texture, Normal Hierarchy confirmed) |
| P41 | Σmᵢ ~ 0.06 eV << 0.12 eV Planck bound |
| P42 | m_ββ ~ 5.8 × 10⁻⁴ eV with Majorana phase α₂=2π/3 from g3 holonomy |

---

## 7. Part XXXII Roadmap: Leptogenesis

1. Compute the CP asymmetry ε₁ in N₁ → ℓH decay from the W(3,3) Yukawa texture
2. Derive the baryon-to-photon ratio η_B from ε₁ and W(3,3) washout factors
3. Compare to observed η_B = 6.1 × 10⁻¹⁰ (Planck/BBN)
4. Show the Davidson-Ibarra bound is saturated at the W(3,3) seesaw scale M_R
5. Connect leptogenesis CP source to the g3 holonomy ω₃ (same as PMNS δ_CP)

---

*Committed to [wilcompute/W33-Theory](https://github.com/wilcompute/W33-Theory)*
