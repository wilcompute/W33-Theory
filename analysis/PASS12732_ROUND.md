# Pass 12732: the orbifold hybrid's KK X,Y bosons put proton decay at 10³³–10³⁴ yr (below Super-K) unless matter sits on the SM brane; bino freeze-in at T_RH ≈ M/24 gives the hybrid's dark matter; the y′ floor scales as N^(−1/4) with families; A's SUSY escape needs a saxion heavier than ~10⁶–10⁸ GeV; an end-to-end evidence update

Claude track. **Not a theory of everything.**
- Script: `explore_pass12732_round.py`.
- Tests: `tests/test_toe_pass12732.py`, 4 tests passing.
- Page: [Quartic Zero Decision Map](https://claude.ai/artifact/P7DdJZNBnjeSPJgFZ4Wnoc), version 10.
- The draft note's scope section has been updated.

## (2) Proton decay in the orbifold hybrid (corrects earlier passes)
- **Setup:** in an orbifold GUT the X,Y gauge bosons are KK modes at (2n+1)/R. With matter on the GUT-symmetric brane:
  - τ(p → e⁺π⁰) ≈ 1.6×10³⁴ yr × (M_c/10¹⁶)⁴ × (α_G⁻¹/25)² / (π²/8);
  - M_c comes from the two-loop window of Pass 12731.

| ΛR | M_c (GeV) | τ (yr), ×/÷10 hadronic | vs Super-K 2.4×10³⁴ |
|---|---|---|---|
| 3 | 2.0×10¹⁶ | 1.8×10³⁵ | allowed |
| 7 | 1.2×10¹⁶ | 2.1×10³⁴ | borderline |
| **10** | 9.3×10¹⁵ | **8×10³³** | below |
| 20 | 6.0×10¹⁵ | 1.4×10³³ | below |
| 40 | 3.8×10¹⁵ | 2×10³² | excluded |

- **The tension:** with matter on the GUT brane, proton stability wants ΛR ≲ 7, while unification (two loops) and Goldstone protection want ΛR ≳ 10.
- **The resolution: matter on the SM brane,** where the X,Y wavefunctions vanish, so there is no tree-level dimension-6 decay. Alternatively, Hall–Nomura-type bulk matter can be used.
- **This corrects the hybrid's earlier "no proton decay at Hyper-K".** That figure (Passes 12702, 12717) used M_X = M₁₂ ≈ 4×10¹⁶ GeV, which does not hold in the orbifold version.
- **The prediction now depends on where the matter sits:**
  - on the GUT brane: decay at the current limit, already in tension;
  - on the SM brane: no dimension-6 signal.

## (1) Bino-like freeze-in dark matter for the hybrid
- **Model:** Boltzmann-suppressed pair production with ⟨σv⟩ = 4πα²/M² (α = 0.01) and g* = 228.75.
- **Result:** Ω h² = 0.12 requires **M/T_RH ≈ 24.3**, nearly independent of mass. For M = 10⁹, 8.45×10⁹ and 3×10¹⁰ GeV, T_RH = 4×10⁷, 3.5×10⁸ and 1.2×10⁹ GeV.
- **Consistency:** T_RH sits below M_SS and far below M_c. **This replaces the retracted higgsino (Pass 12731).**

## (3) Refereeing the y′ floor (draft note updated)
- **Families:** with N degenerate vectorlike families of equal y′, the y′⁴ terms add, so the floor is ≈ 0.40·N^(−1/4) = **0.40, 0.34, 0.30** for N = 1, 2, 3.
- **Chiralities:** with Yukawas to both chiralities, the floor applies to (y′⁴ + y″⁴)^{1/4}.
- **General statement of the falsifier:** **(Σ y⁴)^{1/4} < 0.35**, summed over families and chiralities.

## (4) Saxion cosmology for A's SUSY PQ escape
- **Inputs:** an oscillation from f_I = 1.8×10¹⁷ GeV gives ρ_s/s ≈ (T_RH/8)(f_I/M_Pl)². The saxion width is Γ ≈ m_s³/(32π f_a²).

| m_s | T_RH = 10⁸ | T_RH = 10¹⁰ |
|---|---|---|
| 10⁴ GeV | dominates (dilution ×15) | dominates (×1500) |
| 10⁶ GeV | no domination | marginal (×1.5) |
| 10⁸ GeV | no domination | no domination |

- **A's escape needs a heavy saxion,** m_s ≳ 10⁶–10⁸ GeV. Otherwise saxion domination dilutes the axion and moves the required θᵢ.

## (5) End-to-end evidence (Bayes factor vs SM, SM m_t prior width 15 / 5 / 2 GeV)

| completion | evidence | notes |
|---|---|---|
| hybrid (pseudo-Goldstone Q + U, orbifold) | **0.375 / 0.125 / 0.050** | ×0.5 for proton-decay tension |
| A, SUSY PQ escape | 0.44 / 0.15 / 0.06 | divide by 8 for trials: 0.055 / 0.019 / 0.0075 |
| B′ | 0.044 / 0.015 / 0.006 | — |
| A, tuned (θᵢ plus hilltop) | 0.026 / 0.009 / 0.003 | divide by 8: 0.003 / 0.001 / 0.0004 |

- **Ranking after trials:** hybrid > A (escape) ≈ B′ > A (tuned).
- **None is preferred over the SM.** These are heuristic factor estimates, not full integrals.

## Status
- **Hybrid:** leads on evidence. It needs matter on the SM brane (proton decay) and bino freeze-in dark matter (T_RH ≈ 3.5×10⁸ GeV). Its unification and protection window is ΛR ≳ 10.
- **A:** escape via a SUSY PQ sector with a heavy saxion.
- **B′:** unchanged.
- **Universal falsifier:** (Σ y⁴)^{1/4} < 0.35.
