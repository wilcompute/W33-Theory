# Passes 12151–12155: corrections — the candidates fail; the Fricke symmetry; leptons; running; calibrated H-momentum

Claude track. Producer: `analysis/w33_pass12151_to_12155_axis_fricke_leptons_running_hmom.py`. Drivers and frozen
outputs: `analysis/search_drivers_12151/`.

## Corrections first

**12155 corrects 12133, 12138 and 12146.** The corpus selection-rule engine (`w33_so16_selection_rules.py`, used in
Pass 11102) fixes the higher-point H-momentum rule:

- Σ R = 0 exactly for a cubic ψψφ;
- Σ R ≡ 0 (mod 3) once extra scalars are attached.

12133 and 12146 had left this rule out of their quartic ψψ⟨s₁⟩⟨s₂⟩ terms, so their lifts were only upper bounds. With
the rule imposed:

| model | light pairs, earlier quartic claim | light pairs, with H-momentum |
|---|---|---|
| A8SM_10006 | 0 | **11** |
| A8SM_16222 | 0 | **12** |
| T115 | 1 | **7** |
| S002 | 12 | **29** |

The 16 crossed models lift at most a few pairs each. **Quartic order lifts almost nothing.** The Witten-parity
statement of 12142 is unaffected.

**12153 and 12154 correct 12146–12148.** The two "best candidates" are **not viable**:

- their exotics are not lifted (above);
- the Weinberg angle fails (12154);
- their lepton sectors fail (12153).

## 12154: gauge running at k_Y = 17/3

This uses the SM spectrum with string boundary conditions k_3 = k_2 = 1.

| k_Y | sin²θ_W(M_Z), M_s solved from α_em, α_s | sin²θ_W(M_Z), heterotic M_s ≈ 2.7·10¹⁷ GeV |
|---|---|---|
| 5/3 (control) | 0.208 | 0.202 (the known non-SUSY shortfall) |
| 17/3 | 0.109, with M_s ≈ 7·10⁵ GeV (absurd) | 0.088, with α_em⁻¹(M_Z) = 342 |

The measured value needs k_Y ≈ 1.29. **The fraction-free hypercharges (k_Y ≥ 17/3) are excluded by the Weinberg
angle**, unless huge threshold corrections or light extra matter intervene. So the trade-off of 12126–12139 has a
decisive price.

## 12153: leptons of the two candidates

Trilinear, local couplings, exact H-momentum.

- **A8SM_10006:** no charged-lepton Yukawa (rank 0) and no Dirac neutrino coupling.
- **A8SM_16222:** charged-lepton rank 3, and Dirac couplings to exactly 3 singlets N. Their Majorana mass matrix is
  **zero** at trilinear and at quartic order (mod-3 H-momentum). So the neutrinos are Dirac, at the electroweak scale.

## 12152: i/√3 is the fixed point of an exact Fricke symmetry of the Witten levels

S002's lowest Witten-sector level is **exactly** invariant under T_WL → −1/(3 T_WL) on the axis:

| pair | Δ |
|---|---|
| 0.5i ↔ 0.6667i | 0.0034543236939 |
| 0.52i ↔ 0.6410i | 0.0018258998578 |

The agreement is to 13 digits. i/√3 is the fixed point, so the non-negative level is stationary there and touches zero.
That explains 12149. The full one-loop Λ is only approximately invariant:

| pair | Λ/M⁴ | Λ/M⁴ |
|---|---|---|
| 0.52i ↔ 0.641i | 117.27 | 118.72 |
| 0.55i ↔ 0.606i | 115.39 | 116.07 |

## 12151: the candidates' Wilson-line axes

| T_WL | A8SM_10006 | A8SM_16222 |
|---|---|---|
| 2i | Λ = 652 | Λ = 703 |
| 1.5i | 374 | 421 |
| i | 175 (lowest level: 40 states at +0.052) | 217 (48 states at +0.052) |
| 0.9i | tachyon-free (16 states at +0.020) | — |
| 0.8i | **tachyonic** (16 states, Δ = −0.038) | **tachyonic** (16 states, −0.038) |
| i/√3 | tachyonic (Δ = −1/6) | — |

Both roll toward small radius with Λ > 0, into a tachyon between 0.9i and 0.8i. Neither has a tachyon-free path to the
Fricke point.

## Where this leaves the programme

- **Within the A8 and e6+a2 orbifolds of this geometry:** charge quantisation forces k_Y ≥ 17/3, which the Weinberg
  angle excludes. The canonical k_Y = 5/3 brings fractional charges (11095/11097).
- **Exotics:** they are not lifted at quartic order under the calibrated rules.
- **Vacuum:** every vacuum examined has Λ > 0 and runs into a tachyon.
