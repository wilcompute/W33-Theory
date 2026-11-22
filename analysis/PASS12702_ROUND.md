# Pass 12702: the E₆-SUSY + top-partner hybrid survives two loops (δ = +0.26, y′ = 0.46 ± 0.02 at 1.74 TeV) and predicts no proton decay at Hyper-K; renormalizable E₆ masses cannot make Q + U light; radiative splitting gives A's neutrinos near-resonance automatically

Claude track. Follows Pass 12701. **Not a theory of everything.** Script: `toe_pass12702_round.py`; certificate: `data/toe_pass12702_round.json`; tests: `tests/test_toe_pass12702.py`.

## (1) + (4) Hybrid at two loops, with the top partner above the LHC limit

The two-loop gauge coefficients for the vectorlike Weyl fermions come from the general formula B_ij += ½[4 S_i C₂ʲ + (20/3) C₂(G_i) S_i δ_ij]. **It reproduces the SM B_ij exactly** (fermions + Higgs + gauge; asserted in the script). The y′ term enters through d_u. Above M_SS the vectorlike superfields are scaled by 1.5, which is approximate. λ uses two-loop SM running plus the one-loop vectorlike terms.

| M_VL (Q + U) | y′ for λ = 0 at 10¹⁰ | M₁₂ | δ(α₃⁻¹), two loop | τ(p → e⁺π⁰) |
|---|---|---|---|---|
| 1.00 TeV | 0.478 | 4.6×10¹⁶ | +0.33 | ~2×10³⁷ yr |
| **1.74 TeV (LHC limit)** | **0.462** | 4.1×10¹⁶ | **+0.26** | ~1×10³⁷ yr |
| 2.5 TeV | 0.453 | 3.7×10¹⁶ | +0.21 | ~8×10³⁶ yr |
| 4 TeV | 0.442 | 3.4×10¹⁶ | +0.16 | ~5×10³⁶ yr |
| 10 TeV | 0.423 | 2.8×10¹⁶ | +0.04 | ~3×10³⁶ yr |
| *(no vectorlike pair)* | — | 9×10¹³ | −3.41 | excluded |

Width of the y′ prediction at 1.74 TeV:

| source | y′ |
|---|---|
| λ = 0 at 10⁹ / 10¹¹ GeV | 0.496 / 0.439 (−0.029 per decade) |
| M_t ∓ 0.3 GeV | 0.476 / 0.447 |
| α_s ∓ 0.0009 | 0.446 / 0.477 |

- **Unification works at two loops** with MSSM-level quality: +0.26 against +0.16 for SUSY at 1 TeV. Pass 12701's one-loop M_GUT of 1.7×10¹⁶ rises to 4×10¹⁶ at two loops.
- **The hybrid predicts y′ = 0.46 ± 0.02 at 1.74 TeV; B predicts 0.51 ± 0.02 (Pass 12689).** FCC-hh measures y′ to ±0.002 (Pass 12696). Once FCC-ee fixes M_t and α_s, the theory band shrinks to about ±0.004. The two are then separated by more than 5σ. Under the hybrid hypothesis, y′ also measures M_SS to about ±0.15 decades.
- **Proton decay:** d=6 τ(e⁺π⁰) ~ 10³⁷ yr, far beyond Hyper-K's 10-year 90% CL sensitivity of 7.8×10³⁴ yr ([Hyper-K design report](https://arxiv.org/abs/1805.04163)). d=5 K⁺ν̄ is suppressed by ~(1 TeV/M_SS)² ~ 10⁻¹⁴ relative to TeV SUSY. **A Hyper-K proton-decay signal would disfavour the hybrid.**
- Not established: the two-loop vectorlike terms in λ, the two-loop superfield coefficients above M_SS (scaled here), and thresholds.

## (2) E₆ obstruction to a light Q + U

Charges of the 27 under (Y, χ, ψ): 27 = 16₁ + 10₋₂ + 1₄, 16 = 10₋₁ + 5̄₃ + 1₋₅, 10 = 5₂ + 5̄₋₂.

- Q, u^c and e^c are the only states in the 27 with their SM quantum numbers, so no mixing reaches them. Their masses from 27̄·27·(1 + 78) are m + c_Y Y + c_χ χ + c_ψ ψ.
- In the SU(5) 10 they share χ = −1 and ψ = 1. The rows (1, Y, χ, ψ) have **rank 2**: the mass is affine in Y.
- **Setting m(Q) = m(u^c) = 0 forces m(e^c) = 0** (verified symbolically with sympy). A light Q + U then comes with a light e^c, i.e. a complete 10 + 10̄, which does not repair unification.
- A 27 + 27̄ pair has **17** SM-invariant mass parameters. The diagonal ones are Q, u^c, e^c, D, H_u; the 2×2 blocks are (d^c, D̄), (L, H_d) and (ν^c, S). A singlet plus the 78 supplies at most **6** (Y, χ, ψ and the singlets in the 16 and 16̄).
- **The hybrid therefore needs a 650 (27̄ ⊗ 27 = 1 + 78 + 650) or non-renormalizable operators.**

**Applied to the other track's F/D-flat branch (7af60ca6b, `data/toe_20261122_round6_e6_FD_branch.json`).** The adjoint vacuum value lies along U(1)_ψ at a = −m/(4λ). It gives 16 → 3m/4 and 10 → 3m/2 and leaves the singlet massless. These are complete SO(10) multiplets, so the branch has no unification repair. For the hybrid, the branch needs a 650 or higher-dimension terms; this is added to the cross-track request.

## (3) Leptogenesis for A: radiative resonance

Suppose the heavy neutrinos are exactly degenerate at a scale Λ (from a flavour symmetry acting on N) and are split only by Yukawa running. Then ΔM ≈ M·2h²/(16π²)·ln(Λ/M) and Γ = h²M/(8π), so **ΔM/Γ ≈ ln(Λ/M)/π, independent of the Yukawa size** (up to an O(1) factor from the flavour structure).

| Λ | ΔM/Γ | ε / sin φ | sin φ needed |
|---|---|---|---|
| f_a = 10¹¹ GeV | 2.9 | 0.17 | 10⁻⁵–7×10⁻⁵ |
| M_GUT | 6.7 | 0.07 | 2×10⁻⁵–2×10⁻⁴ |
| M_Pl | 8.3 | 0.06 | 2×10⁻⁵–2×10⁻⁴ |

- At M_N = 1.24×10⁷ GeV (Vissani Δ = 10), the seesaw Yukawa gives y² ≈ 2×10⁻⁸. Then Γ/M ≈ 8×10⁻¹⁰ and ΔM/M ≈ 2×10⁻⁹.
- The resonance is reached automatically. The asymmetry is set by a small CP phase, sin φ ~ 10⁻⁵–10⁻⁴, which is technically natural.
- This is radiative resonant leptogenesis ([González Felipe–Joaquim–Nobre, hep-ph/0311029](https://arxiv.org/abs/hep-ph/0311029); [Branco et al., hep-ph/0507092](https://arxiv.org/abs/hep-ph/0507092)), applied here to A's Vissani window. It is not new as a mechanism.
- **The degeneracy must not come from approximate lepton number.** In the pseudo-Dirac case the light-mass suppression forces y² up by M/ΔM, and the Vissani tuning grows to ~10⁵.
- Not established: the O(1) flavour factor, and the flavour-coherence corrections near ΔM ~ Γ (Garny et al.), which are a factor of ~2.

## Status of the scenarios

- **A** (axion): natural if its heavy neutrinos are degenerate by a flavour symmetry at ~10⁷ GeV with radiative splitting.
- **B** (dark dimension): y′ = 0.51.
- **Hybrid** (E₆ SUSY at 10¹⁰ + top partner): y′ = 0.46, no proton decay, and it needs a 650-type E₆ mass.

All three remain conditional. The hybrid and B share their LHC signature and differ by 0.05 in y′.
