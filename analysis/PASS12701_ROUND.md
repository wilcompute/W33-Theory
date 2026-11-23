# Pass 12701: A can stay natural with quasi-degenerate neutrinos at 10⁷ GeV; split SUSY moves the ceiling to 5×10⁷ GeV; a TeV vectorlike top partner with y′ ≈ 0.48 lets high-scale SUSY at 10¹⁰ GeV unify and keep the quartic zero

Claude track. Follows Pass 12700. **Not a theory of everything.** Script: `toe_pass12701_round.py`; certificate: `data/toe_pass12701_round.json`; tests: `tests/test_toe_pass12701.py`.

**Correction to Pass 12700.** Two-loop running shifts the MSSM unification mismatch by **+0.8** (−0.62 → +0.16, computed in item 4), not −0.8. The 12700 note, script string and certificate note are corrected; its conclusions are unchanged.

## (1) Leptogenesis for completion A under the Vissani bound

Formulas used:
- Required asymmetry: ε = η_B/(0.96×10⁻² κ), with κ from the Buchmüller–Di Bari–Plümacher fit;
- hierarchical maximum: Davidson–Ibarra ε_DI = 3 M m_atm/(16π v²);
- needed enhancement R = ε/ε_DI, with a degeneracy of order ΔM/M ~ 1/R (order of magnitude).

| M_N | Vissani Δ | R (m̃ = m_sol, κ = 0.043) | R (m̃ = m_atm, κ = 0.005) | ΔM/M |
|---|---|---|---|---|
| **1.24×10⁷ GeV** | **10** | 1.2×10³ | 9.9×10³ | **10⁻⁴–10⁻³** |
| 10⁸ GeV | 5×10³ | 150 | 1.2×10³ | ~10⁻³ |
| 5×10⁸ GeV | 7×10⁵ | 30 | 250 | ~10⁻² |
| 10⁹ GeV | 5×10⁶ | 15 | 120 | ~10⁻² |

- **A can keep Δ ≈ 10 with a quasi-degenerate pair at 1.2×10⁷ GeV split by ΔM/M ~ 10⁻⁴–10⁻³.** That is six orders milder than TeV resonant leptogenesis (~10⁻¹⁰; [Hambye–March-Russell–West](https://arxiv.org/abs/hep-ph/0403183), [Pilaftsis–Underwood](https://arxiv.org/abs/hep-ph/0309342)).
- A symmetry still has to explain the splitting; this is an extra assumption, not a prediction.
- Minimal axiogenesis is not an option at KSVZ/DFSZ f_a ([2108.09299](https://arxiv.org/abs/2108.09299)).

## (2) Split SUSY: gauginos and higgsinos at 1 TeV, scalars at M_SS

The one-loop split-SUSY RGEs (Giudice–Romanino, [hep-ph/0406088](https://arxiv.org/abs/hep-ph/0406088), appendix eqs. 56–60 and 68; λ_ours = λ_GR/2) are added on top of the two-loop SM running. The SM limit was checked term by term. Matching at M_SS: λ = (g² + g′²)/8 · cos²2β, g̃_u = g sin β, etc., solved by shooting.

| M_SS | λ(M_SS) | tan β |
|---|---|---|
| 10⁵ GeV | +0.041 | 2.89 |
| 10⁶ GeV | +0.023 | 1.96 |
| 10⁷ GeV | +0.009 | 1.46 |
| ≥ 10⁸ GeV | < 0 | — |

**Split-SUSY ceiling: M_SS < 5×10⁷ GeV**, against 5.4×10¹⁰ GeV for high-scale SUSY. This agrees with the published split bound of ~10⁸ GeV ([1809.07774](https://arxiv.org/abs/1809.07774)). Light gauginos and higgsinos drive λ negative faster. So the split variant, the one that unifies, loses the coincidence of the SUSY scale with the quartic zero.

## (3) Repairing high-scale-SUSY unification with incomplete E₆ pieces

The scan covers one or two piece types, multiplicity 1–3, at masses M_X = 10³–10⁹ GeV:
- vectorlike pairs from the 27: Q, U, D, L, E, X;
- Weyl adjoint pieces from the 78: an (8,1,0) octet and a (1,3,0) triplet.

They are non-SUSY fermions below 10¹⁰ GeV and full superfields above. Of 197 combinations with M_GUT > 3×10¹⁵ GeV, the best reach **δ = −0.68 at one loop**, the same as the MSSM at 1 TeV (−0.62). With the +0.8 two-loop shift, they unify as well as the MSSM. The best three, each at 1 TeV:

| pieces at 1 TeV | M_GUT | α_G⁻¹ | d=6 τ_p |
|---|---|---|---|
| **Q + U vectorlike (incomplete 10 + 10̄)** | 1.7×10¹⁶ | 24.6 | ~4×10³⁵ yr |
| 3 × (L + L̄) + octet | 1.7×10¹⁶ | 24.6 | ~4×10³⁵ yr |
| 2 × (D + D̄) + triplet | 1.7×10¹⁶ | 28.6 | ~6×10³⁵ yr |

**The other track's light states cannot repair unification.** The 64 unlifted spinor directions and the 16/10 split of fd9c87e47 are complete SU(5) multiplets (16 = 10 + 5̄ + 1, 10 = 5 + 5̄), which shift all b_i equally.

**(3b) The leading repair has B's top-partner content.** A vectorlike Q + U at 1 TeV keeps λ > 0 all the way to M_Pl for y′ ≤ 0.4: its gauge contributions remove the quartic zero. The zero returns at 10¹⁰ GeV for **y′ = 0.478**; y′ = 0.51 puts it at 8×10⁸ GeV. Note this one-loop vectorlike treatment is the same as in Pass 12685.

> **Combined scenario (new combination, conditional).** E₆ SUSY broken at M_SS ≈ 10¹⁰ GeV with tan β ≈ 1, plus a TeV vectorlike top partner with y′ ≈ 0.46–0.50. In this scenario:
> - the quartic zero sits at M_SS;
> - the couplings unify at 1.7×10¹⁶ GeV with MSSM-level quality;
> - the d=6 proton lifetime is ~4×10³⁵ yr (beyond Hyper-K's 20-year reach of ~10³⁵);
> - the LHC/FCC top-partner signature is the same as B's (compressed T–B–T′ triplet).
>
> It is distinct from B: B's species scale of ~10⁹ GeV forbids running to 10¹⁰. The other track's E₆ vacuum would have to leave Q + U light; whether its messenger filter can do that is the question for them. Not established: two-loop running with the vectorlike pair, thresholds, and the origin of the Q + U lightness.

## (4) Two-loop unification and proton lifetime

The two-loop coefficients B_ij and d_u are from hep-ph/0406088 eqs. 40–45, with the top Yukawa included. The proton lifetime uses τ(p → e⁺π⁰) ≈ 4.7×10³⁴ yr (M_X/10¹⁶)⁴ (α_G⁻¹/25)², with α_H = 0.0144 GeV³ and A_R = 2.5. This is uncertain by a factor of ~3.

| spectrum | M₁₂ | δ(α₃⁻¹) two loop | τ_p |
|---|---|---|---|
| SM | 1.1×10¹³ GeV | −4.92 | 2×10²³ yr |
| MSSM at 1 TeV | 1.4×10¹⁶ GeV | +0.16 | 2×10³⁵ yr |
| high-scale SUSY 10¹⁰ | 9.1×10¹³ GeV | −3.40 | 7×10²⁶ yr (excluded if unified) |
| split (1 TeV / 10¹⁰) | 1.2×10¹⁶ GeV | −0.58 | 1.5×10³⁵ yr |

The Super-K limit is 2.4×10³⁴ yr. All the spectra that unify predict τ_p of 10³⁵–10³⁶ yr, at or beyond Hyper-K's reach.

## (5) Cross-track summary

`CROSS_TRACK_SUMMARY_12684_12698.md` now has an addendum for Passes 12699–12701.

**Correction (Pass 12704).** An explicit scan with flavoured Pilaftsis–Underwood asymmetries gives a degeneracy window of 10⁻¹² ≲ ΔM/M ≲ 10⁻⁵ for A at 1.24×10⁷ GeV (more than 5% of points reach η_B). At 10⁻⁴ only 0.2% of points work, so the 10⁻⁴–10⁻³ estimated in item 1 was optimistic.
