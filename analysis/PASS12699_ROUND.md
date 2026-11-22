# Pass 12699: neither completion explains the Belle II Kνν̄ or 95 GeV hints; A's DFSZ-type potential is consistent; B's soft-lepton tag survives realistic cuts; DFSZ-reach haloscopes cover A's axion; an E₆-SUSY threshold at the quartic zero needs tan β ≈ 1.1–1.5 and M_SS < 5×10¹⁰ GeV

Claude track. Follows Pass 12698. **Not a theory of everything.** Script: `toe_pass12699_round.py`; certificate: `data/toe_pass12699_round.json`.

## (1) Anomaly scout

| hint | needed | A | B |
|---|---|---|---|
| Belle II B⁺ → K⁺νν̄: 2.3(7)×10⁻⁵ vs SM 0.50×10⁻⁵ (excess 1.8×10⁻⁵) | B → K a with f_a/C_bs ≈ 2×10⁸ GeV, excluded for a QCD axion (SN1987A f_a ≳ 10⁸ GeV with O(1) couplings) | predicts 10⁻¹³: **no** | no light invisible state: **no** |
| ~95 GeV scalar (CMS γγ, LEP bb̄) | a light singlet or second doublet | second doublet decouples at ≥ 10⁵ GeV: **no** | no light scalar: **no** |

Neither completion explains either hint. If either becomes significant, both completions need additions.

## (2) Completion A's DFSZ-type potential

Fields H₁, H₂, σ with the PQ term −κH₁H₂σ². An explicit parameter point:
- λ₁ = 0.13, λ₂ = 0.5, λ_σ = 4×10⁻¹⁰;
- portals λ₁₂ = 0.1, λ₁σ = 10⁻¹², λ₂σ = 10⁻⁶;
- κ = 2×10⁻¹³.

The quartic form on the radial octant has minimum 1×10⁻¹⁰ > 0, so it is **bounded below**. With f_a = 10¹¹ GeV the second doublet sits at m_H₂ ≈ 10⁸ GeV and its induced VEV is v₂ ≈ 5×10⁻⁵ GeV: negligible, so the light Higgs is SM-like. The tiny portals (λ₁σ ~ 10⁻¹²) are the standard DFSZ/SMASH price of a light Higgs. This shows that a consistent point exists; it is not a scan of the full parameter space.

## (3) Toy Monte Carlo of B's soft leptons (14 TeV, M = 1.65 TeV)

Setup: pair kinematics drawn from the CT18NNLO-weighted threshold distribution (⟨β*⟩ = 0.52); B → T ℓν with a Michel spectrum (endpoint 22 GeV) in the B frame, boosted to the lab.

| cut (with \|η\| < 2.5) | acceptance |
|---|---|
| p_T > 5 GeV | 0.89 |
| p_T > 7 GeV | 0.82 |
| p_T > 10 GeV | 0.67 |
| p_T > 15 GeV | 0.43 |

The median lepton p_T is 13.5 GeV. The soft-lepton tag (34% of pairs, Pass 12694) therefore keeps ≈ 80% efficiency at standard soft-lepton thresholds. A full simulation (MadGraph + Delphes) is not available in this environment; this toy fixes the kinematics but not backgrounds.

## (4) Haloscope forecast for A

| axion | E/N | g/g_KSVZ | scan time vs KSVZ | vs DFSZ |
|---|---|---|---|---|
| KSVZ | 0 | 1 | 1 | 0.02 |
| **A, b only** | 2/3 | 0.65 | 5.5 | **0.13** |
| A, b + τ opposite | −4/3 | 1.69 | 0.12 | ≈ 0 |
| DFSZ benchmark | 8/3 | 0.39 | 44 | 1 |

MADMAX and ALPHA aim for DFSZ sensitivity over roughly 40–400 μeV and 40–200 μeV. Reaching it would cover A's b-only axion in the lattice window ~8× faster than DFSZ. **Completion A is fully testable by the planned haloscopes.**

## (5) Bridge to the other track's SUSY E₆ construction

The other track's E₆ → SU(5) → SM vacuum (6442db4d6, 17e3dc053) is supersymmetric. If SUSY is broken at M_SS with the tree-level MSSM matching λ(M_SS) = (g² + g′²)/8 · cos²2β, the measured m_t (172.57) requires:

| M_SS | λ_SM(M_SS) | cos²2β | tan β |
|---|---|---|---|
| 10⁹ GeV | +0.0083 | 0.136 | 1.47 |
| 10¹⁰ GeV | +0.0031 | 0.051 | 1.26 |
| 10^10.5 GeV | +0.0009 | 0.015 | 1.13 |
| ≥ 10¹¹ GeV | < 0 | — | **no solution** |

> **Bridge result.** A SUSY E₆ model with SUSY broken at the intermediate scale must break it **below μ₀ ≈ 5×10¹⁰ GeV**, with **tan β ≈ 1.1–1.5**. tan β → 1 makes the SUSY threshold coincide with the quartic zero (the Ibáñez–Valenzuela case). Threshold corrections from stop mixing are not included; they shift tan β by O(0.1). This is a concrete, checkable constraint on the other track's vacuum. See `REQUEST_E6_INTERMEDIATE_SCALE_SUSY.md`.
