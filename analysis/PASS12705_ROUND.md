# Pass 12705: in real E₆, a 650 alone never leaves only Q + U light but 650 + 78 does; the SO(10) analogue leaves a massless octet + triplet that spoils unification unless lifted to ≳ 10¹⁶ GeV; minimal-flavour-violating tree splittings make A's leptogenesis work in 7–9% of parameter space; the dark-graviton bound gives B y′ = 0.522–0.530

Claude track. Follows Pass 12704. **Not a theory of everything.** Script: `toe_pass12705_round.py` (≈4 min); certificate: `data/toe_pass12705_round.json`; tests: `tests/test_toe_pass12705.py`.

**Correction to Pass 12704.** The dark-graviton bound is eq. (4.14) of 2307.11048, verified verbatim from the PDF: ℓ₅^eff > (2/γ)(δ/0.5)(λ/0.1)^{2/3} × 10 μm. At natural parameters that means **ℓ₅^eff ≥ 10 μm**. (ℓ₅ itself, eq. 4.13, is ≥ 20 μm.) Pass 12704's "eqs. (42)–(43), ≳ 20 μm" came from a summary.

## (1) Real E₆: is there a vacuum where only Q + U are light?

**Construction:**
- e₆ is computed directly as the derivation algebra of the cubic norm N = det A + det B + det C − tr(ABC) on 27 = (3,3̄,1) + (1,3,3̄) + (3̄,1,3). **It has dimension 78**, and it contains the SU(3)³ actions.
- The hypercharge was found by search: six combinations of SU(3)_L × SU(3)_R Cartans reproduce the 27's Y content, and three of them put Q in the (3,3̄,1) block. Those three are equivalent under SU(3)_R Weyl reflections.
- The SM-invariant 27̄·27 mass operators number **17 = 1 + 5 (78) + 11 (650)**. This is computed, and agrees with the counting of Passes 12702–12703.
- The superpotential is the most general renormalizable one in these fields:
  - **650:** both cubic invariants (tr X³ and the dd̄XXX contraction; they are independent, as Babu–Bajc–Susič note);
  - **78:** tr A²; tr A³ = 0, as E₆ requires;
  - **couplings:** 78·78·650 and 650·650·78 (both non-zero).
- F-flat vacua were found by Newton iteration from 300 random starts on the SM-singlet slice. Symmetric criticality guarantees they are vacua of the full theory. Hermitian VEVs make the D-terms vanish.

**Check against the literature:** the unbroken dimensions found include 46 (SO(10)×U(1)), 38 (SU(6)×SU(2)), 24 (SU(3)³) and 22 (SU(3)×G₂). These are the regular and special cases of [Babu–Bajc–Susič](https://arxiv.org/abs/2305.16398).

| system (3 parameter sets each) | vacua | Q + U only light (all other blocks heavy, relative 10⁻³) |
|---|---|---|
| 650 alone | 11, 12, 16 | **0, 0, 0**, although vacua with unbroken dimension 13–14 (SM×U(1)ⁿ) exist |
| 650 + 78 | 30, 17, 37 | **11, 5, 15**, with unbroken dimension 13 or 14 (one at 16) |

- With a single 27̄·27·650 coupling, the condition m(Q) = m(u^c) is one extra equation at an isolated vacuum, so it generically fails.
- The 78 coupling supplies the second parameter, at the cost of **two tuned couplings** (M and η₇₈).
- **This answers question 4 of the cross-track request:** the hybrid needs a 650 **and** a 78 with a VEV outside the ψ direction. The other track's ψ-only adjoint is not enough.

## (2) SO(10) 45 + 210: full mass matrix and the leftover massless states

- **Full-space check:** for the Pass 12704 vacua, the gradient over all 255 fields vanishes (|dW|/|v| = 10⁻¹⁵), so symmetric criticality holds. The Hessian agrees with finite differences to 2×10⁻¹².
- **Result:** **every vacuum where Q + U alone are light has extra massless chiral states beyond the 32 Goldstones.** The quantum numbers come from the Cartan weights on the zero-mode space with the Goldstones projected out:
  - **ω ≠ 0** (four vacua): **exactly (8,1,0) + (1,3,0)**, which is 11 states;
  - **ω = 0:** (3,2,−5/6) + (3,2,1/6) + conjugates, 24 states (36 with 8 + 3 + 1).
- Vacua of higher symmetry have no extras, apart from the p, B-only family, which has 30.

The light octet and triplet do not spoil the light Q + U themselves, but they change unification. In the hybrid (M_VL = 1.74 TeV, M_SS = 10¹⁰ GeV, two loop; chiral superfields above M_SS, Weyl below):

| octet + triplet mass | M₁₂ | δ(α₃⁻¹) |
|---|---|---|
| decoupled (reference) | 4.1×10¹⁶ | +0.26 |
| 10¹⁵ GeV | 1.9×10¹⁸ | +1.35 |
| 10¹²–10¹⁴ GeV | α₁ and α₂ do not meet below 10¹⁹ | — |

- Lifting the pair with Planck-suppressed operators gives M_GUT²/M_Pl ~ 10¹³–10¹⁴ GeV, which is too light.
- **The minimal 45 + 210 route therefore needs additional fields, for example a 54, to give the octet and triplet a GUT-scale mass.** For the 650 + 78 vacua of item 1, the full 650 + 78 mass matrix (650×650) is not computed here. Whether they carry the same leftovers is open and is the next check.
- This is reminiscent of the octet-triplet unification of Bachas–Fabre–Yanagida, which uses such states at ~10¹³ GeV to push unification toward the string scale.

## (3) A's heavy neutrinos with minimal-flavour-violating tree splittings

In lepton MFV, the only spurions are h and Y_e ([Cirigliano–Isidori–Porretti](https://arxiv.org/abs/hep-ph/0607068); [Branco et al.](https://arxiv.org/abs/hep-ph/0609067)). So the N mass at the high scale is M₀[1 + c₁ Re(h†h) + c₂ Re(h†Y_eY_e†h)] with O(1) coefficients, on top of the radiative running. The c₂ term misaligns at order y_τ²|h|² ~ 10⁻¹², without the loop factor ln/16π².

| case (2000 points, Λ = M_GUT) | η_B max | fraction ≥ 6.1×10⁻¹⁰ |
|---|---|---|
| control: y_τ = 0 | 2×10⁻¹⁴ | 0 |
| c₂ = 0, c₁ ∈ [−3, 3] (works only where c₁ cancels the radiative splitting) | 5×10⁻⁸ | 1.7% |
| \|c₂\| ∈ [0.3, 3] | 7×10⁻⁷ | **9.0%** |
| \|c₂\| ∈ [0.1, 1] | 1×10⁻⁷ | **7.0%** |

- **With MFV, A's leptogenesis works without any extra symmetry, for O(1) tree coefficients.** The radiative-only case gave 0%.
- The mechanism is the one in the MFV leptogenesis literature cited above. It is applied here to A's Vissani-natural window.

## (4) Dark-graviton band, verified

Eq. (4.14) (verbatim) gives 30 μm > ℓ₅^eff > (2/γ)(δ/0.5)(λ/0.1)^{2/3} × 10 μm. At the paper's natural values (γ ~ 2, δ ~ 0.5, λ ~ 0.1), **ℓ₅^eff = 10–30 μm, so y′_B = 0.522–0.530**. Over the O(1) range of 1–30 μm, y′_B = 0.508–0.530.

Against the hybrid at M_SS = 10¹⁰ GeV (y′ = 0.464), the natural-parameter gap is 0.058. At FCC precision (σ(y′) ≈ 0.005) that is about 11σ.

## (5) Cross-track summary

`CROSS_TRACK_SUMMARY_12684_12698.md` now has an addendum for Passes 12702–12705, covering three corrections and the answer to question 4.

## Status

- **A:** natural, with MFV tree splittings (7–9%), an explicit 10⁻¹²–10⁻⁵ splitting, or the τ on the PQ doublet.
- **B:** y′ = 0.522–0.530 at natural dark-graviton parameters.
- **Hybrid:** needs a 650 + 78 (non-ψ) with two tunings, and its leftover light states must be checked. In SO(10) they are an octet + triplet that has to be lifted to ≳ 10¹⁶ GeV.
