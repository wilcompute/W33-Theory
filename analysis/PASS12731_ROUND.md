# Pass 12731: at two loops the hybrid's orbifold window is ΛR ≳ 10 (matching protection); the freeze-in higgsino does not fit the hybrid; E₆'s internal Z₃ symmetries cannot protect it; A's escape needs a SUSY flat direction; a draft note on the y′ floor and B′

Claude track. **Not a theory of everything.**
- Script: `explore_pass12731_round.py`.
- Note: `NOTE_DRAFT_quartic_zero_floor_and_Bprime.md`.
- Tests: `tests/test_toe_pass12731.py`, 3 tests passing.
- Page: [Quartic Zero Decision Map](https://claude.ai/artifact/P7DdJZNBnjeSPJgFZ4Wnoc), version 9.

## (1) The hybrid's orbifold window at two loops
- **Method:** the localised orbifold running is put inside the Pass 12703 two-loop unification, above M_c = 1/R, with b_extra = β^H = (−3/5, 1, 3). M_c = M₁₂/(ΛR) is iterated to self-consistency.

| ΛR | M_c (GeV) | M₁₂ (GeV) | δ (two loops) |
|---|---|---|---|
| (none) | — | 4.1×10¹⁶ | +0.259 |
| 3 | 2.0×10¹⁶ | 6.0×10¹⁶ | +0.183 |
| 7 | 1.2×10¹⁶ | 8.2×10¹⁶ | +0.124 |
| **10** | 9.3×10¹⁵ | 9.3×10¹⁶ | **+0.100** |
| 14 | 7.5×10¹⁵ | 1.05×10¹⁷ | +0.077 |
| 20 | 6.0×10¹⁵ | 1.2×10¹⁷ | +0.052 |
| 40 | 3.8×10¹⁵ | 1.5×10¹⁷ | +0.005 |

- **The window shifts:** with the running inside the evolution, the unification scale rises and the cancellation is gentler than the one-loop shift of Pass 12730.
- **Result:** **|δ| ≤ 0.1 for ΛR ≳ 10, overlapping the M_*R ≥ 9.8 protection bound everywhere.** M₁₂ ≈ 1×10¹⁷ GeV also lengthens the proton lifetime.

## (2) A freeze-in higgsino in the hybrid (retracts Pass 12730's dark-matter entry)
- **Requirement:** a Dirac-like higgsino with an unsuppressed Z coupling must have m_χ ≳ 8×10¹⁰ GeV (Unwin 2026).
- **Why it stays Dirac-like:** with gauginos near M_SS = 8.45×10⁹ GeV, the neutral splitting is m_Z²/M ≈ 1 keV, far below the ~100 keV that would make scattering inelastic.
- **Consequence:** the higgsino would need μ ≈ 10·M_SS and would not be the lightest superpartner. **The hybrid's dark matter falls back to a gaugino LSP produced by freeze-in (T_RH < M_SS), or an axion.**

## (3) Ternary structures inside E₆ cannot protect the hybrid
- **Why:** E₆'s Z₃ centre and trinification's cyclic Z₃ (a Weyl-group element) are both elements of E₆. Every E₆-invariant operator, H̄Σ²H included, is automatically invariant under them.
- **Consequence:** the protecting symmetry must lie outside E₆, such as the anomaly-free Z₁₀ of Pass 12718.

## (4) A resonance-free PQ field for A
- **Scale:** the field must fall from f_I ≈ 1.8×10¹⁷ GeV to f_a ≈ 2.5×10¹⁰ GeV, a factor of 7×10⁶.
- **What fails:** a quartic radial potential restores PQ through conformal preheating.
- **What works:** only a quadratic-dominated SUSY flat direction (W = λX(PQ − f_a²) with soft masses), with resonance parameter q ≲ 1 and a saxion decaying before BBN, avoids it (cf. Harigaya–Ibe–Kawasaki–Yanagida).
- **Consequence:** A's untuned escape exists, but only inside a supersymmetric PQ sector.

## (5) Draft note
`NOTE_DRAFT_quartic_zero_floor_and_Bprime.md` writes up the two results with no prior art found:
- the model-independent y′ floor (0.40; falsifier y′ < 0.35 now, < 0.40 at FCC);
- the B′ completion: dark dimension, top partner and B-mesogenesis, with tests, caveats and related work.

## Status
- **Hybrid:** Q + U pseudo-Goldstones, plus orbifold doublet–triplet splitting with protection at ΛR ≳ 10 (two loops), plus M₁₂ ≈ 10¹⁷. Dark matter is a gaugino (freeze-in) or an axion, not a higgsino.
- **A:** viable only with a SUSY flat-direction PQ sector (escape) or two tunings.
- **B′:** unchanged, and written up.
