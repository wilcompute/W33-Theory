# Pass 12703: a light Q + U needs the SU(5) 75 inside the E₆ 650; two-loop top-partner terms move y′ by only +0.002; B and the hybrid overlap in y′ unless M_SS ≳ 3×10⁹ GeV; radiative-only leptogenesis for A falls short by ×3.4 with the SM τ Yukawa

Claude track. Follows Pass 12702. **Not a theory of everything.** Script: `toe_pass12703_round.py`; certificate: `data/toe_pass12703_round.json`; tests: `tests/test_toe_pass12703.py`.

**Two corrections to Pass 12702**, both found here:
- **(a)** The claim that B and the hybrid are separated by more than 5σ holds only for M_SS ≳ 3×10⁹ GeV. At lower M_SS they overlap (item 4).
- **(b)** The claim that radiative splitting makes A's leptogenesis work with a technically natural small phase fails with the SM τ Yukawa: η_B is at most 1.8×10⁻¹⁰ (item 3).

## (1) Which part of the 650 can make Q + U light while e^c stays heavy

Q, u^c and e^c fill the SU(5) 10 inside the SO(10) 16 of the 27. Their masses come from 10̄ ⊗ 10 = 1 + 24 + 75. Each of these contains exactly one SM singlet. Computed exactly (sympy, Hilbert–Schmidt projection on End(10) with multiplicities 6, 3, 1):

| SU(5) piece | acts on (Q, u^c, e^c) as |
|---|---|
| 1 | (1, 1, 1) |
| 24 (hypercharge) | (1/6, −2/3, 1) |
| **75** | **(1, −1, −3)** |

- **With the 75:** m(Q) = m(u^c) = 0 is solved by a = 4m₀, b = −5m₀/3, and then **m(e^c) = 10 m₀**, which is heavy.
- **Without the 75** (b = 0): the masses are affine in Y, which is Pass 12702's obstruction.
- **Where the 75 lives:** 16̄ ⊗ 16 = 1 + 45 + 210, and the only SU(5) 75 sits in the **210**. Under SO(10)×U(1) the 650 is 1 + 45 + 54 + 210 + 16 + 16̄ + 144 + 144̄ + 10 + 10̄. The 210 occurs in the 650 and not in the 78.
- **Counting check:** the 650 holds 11 SM singlets and 1 + 78 hold 6, giving **17**. That is exactly the 17 mass parameters of 27̄·27 counted in Pass 12702.

**But the known 650 vacua do not do it.** A single renormalizable 650 has minima preserving SU(3)³, SU(6)×SU(2), SO(10)×U(1), F₄ and SU(3)×G₂ ([Babu–Bajc–Susič, 2305.16398](https://arxiv.org/abs/2305.16398); model building in [2403.20278](https://arxiv.org/abs/2403.20278)). The 75 direction preserves only the SM group. A light Q + U alone therefore needs a VEV misaligned from the regular single-650 vacua, from more fields or more superpotential structure. This is open.

What the regular vacua would leave light instead, at 1.74 TeV with the hybrid at M_SS = 10¹⁰ GeV (two-loop unification code of Pass 12702):

| vacuum (light block) | M₁₂ | δ(α₃⁻¹) |
|---|---|---|
| 75 direction: Q + U | 4.1×10¹⁶ | **+0.26** |
| SU(3)³ quark blocks: Q + U + 2D | 6.6×10¹⁴ | −9.9 |
| SU(3)³ lepton block: 2L + E | 2.9×10¹³ | +1.9 |
| SU(6)×SU(2) (15, 1): complete 10 + 5 | 1.5×10¹⁴ | −3.5 |

Only the Q + U pattern unifies.

**Tuning.** A TeV Q + U out of 27 + 27̄ masses near M_SS requires a cancellation of about 10⁻⁷. That is technically natural (chiral symmetry), but it is a doublet–triplet-type tuning.

## (2) Two-loop top-partner terms (PyR@TE 3)

The full two-loop RGEs for SM + (Q_VL, T_VL, y′ H Q T) were generated with [PyR@TE 3](https://arxiv.org/abs/2007.12700).

- **Control:** the same tool with the vectorlike fields removed reproduces every two-loop coefficient of `beta_sm` in Pass 12685.
- **Structure:** in β_λ the y′ terms are an exact copy of the top terms, with no yt–y′ cross terms. β_yt does get cross terms (−27/4 yt y′²yt², −27/4 yt y′⁴, 20 g₃² yt y′², …). The vectorlike gauge content also changes the pure-gauge two-loop terms (for example g₃⁴ yt: −108 → −284/3).

| target | y′, one-loop VL | y′, two-loop VL |
|---|---|---|
| hybrid: λ(10¹⁰) = 0, M_VL = 1.74 TeV | 0.462 | **0.464** |
| B: R = 0.1 μm (M₅ = 1.2×10⁹) | 0.494 | 0.495 |
| B: R = 1 μm | 0.507 | 0.508 |
| B: R = 38.6 μm | 0.531 | 0.532 |

The effect is +0.001 to +0.002 everywhere, below the ±0.016 inputs from M_t and α_s. The one-loop vectorlike treatment of Passes 12685–12702 was adequate.

## (3) An explicit O(2) model for A's degenerate N: radiative-only leptogenesis falls short

The model:
- two N with an O(2)-symmetric Majorana mass M₀·𝟙 at Λ;
- Casas–Ibarra Yukawas (normal ordering, m₁ = 0);
- one-loop running of M with the τ Yukawa term in h;
- flavoured Pilaftsis–Underwood asymmetries, with both the M_iΓ_j regulator and the "difference" regulator;
- per-flavour BDP efficiency at M₀ = 1.24×10⁷ GeV (Vissani Δ = 10).

Checks:
- Re z (an O(2) rotation of the degenerate N) drops out to 10⁻⁶.
- Control: y_τ = 0 (aligned running) gives η = 7.5×10⁻¹⁶. **With exact degeneracy, the mass basis diagonalizes Re(h†h), so the total and the flavoured asymmetries both vanish at leading order.** The τ Yukawa misalignment is the only source, as in [González Felipe–Joaquim–Nobre](https://arxiv.org/abs/hep-ph/0311029).

| Λ | median ΔM/Γ | η_B max (4000 points) | fraction ≥ 6.1×10⁻¹⁰ |
|---|---|---|---|
| f_a = 10¹¹ | 1.7 | 1.75×10⁻¹⁰ | 0 |
| M_GUT | 4.2 | 1.80×10⁻¹⁰ | 0 |
| M_Pl | 5.1 | 1.81×10⁻¹⁰ | 0 |

- The maximum is unchanged for |Im z| < 4 and for M₀ = 3×10⁶ GeV.
- η_B scales as y_τ²: ×3 gives 17% of points, ×10 gives 87%. **Radiative-only O(2) leptogenesis needs y_τ ≥ 1.83× its SM value.** That would mean a τ on a tan β-enhanced doublet: in A, a lepton-charged DFSZ variant with tan β ≳ 2. The other option is an explicit tree-level splitting, and then the degeneracy is no longer automatic.
- **This corrects Pass 12702 item 3:** the effective phase is not free; it is fixed at order y_τ² ln(Λ/M)/16π².
- Not established: flavour-coupling (A-matrix) and spectator corrections (O(1)), coherent-oscillation effects near ΔM ~ Γ, and thermal masses.

## (4) B versus the hybrid: y′ measures the scale of the quartic zero

- **B's band:** short-range gravity limits Yukawa-strength deviations to λ < 38.6 μm ([Eöt-Wash, Lee et al. 2020](https://arxiv.org/abs/2002.11761)). This caps B's radius. Over R = 0.1–38.6 μm, M₅ runs from 1.2×10⁹ down to 1.7×10⁸, and **y′_B ∈ [0.495, 0.532]** at two loops.
- **Torsion balances can't reach B:** gravitational-strength deviations at R ~ 1 μm lie far below the reach of current tests at that range.

The hybrid's y′ and unification as a function of M_SS (two loop, M_VL = 1.74 TeV):

| M_SS | y′ | δ | M₁₂ |
|---|---|---|---|
| 10⁸ | 0.542 | +1.91 | 5×10¹⁷ |
| 3×10⁸ | 0.519 | +1.51 | 2.7×10¹⁷ |
| 10⁹ | 0.497 | +1.08 | 1.4×10¹⁷ |
| 3×10⁹ | 0.480 | +0.68 | 7.7×10¹⁶ |
| 10¹⁰ | 0.464 | +0.26 | 4.1×10¹⁶ |
| 3×10¹⁰ | 0.452 | −0.13 | 2.3×10¹⁶ |

- **For M_SS = 3×10⁸ to 10⁹ GeV the hybrid sits inside B's band.** There it unifies worse (δ ≈ +1 to +1.5, against +0.16 for TeV SUSY).
- With MSSM-quality unification (|δ| ≲ 0.7, so M_SS ≳ 3×10⁹), y′_hyb ≤ 0.480 against y′_B ≥ 0.495. The gap is 0.015. With FCC-hh (±0.002) and an FCC-ee-reduced theory band (±0.004) that is about a 3σ separation, not more than 5σ.
- **The robust discriminators are elsewhere:** B's KK-graviton dark matter and the species scale, against the hybrid's 650 sector and its unification.

## (5) Review of the other track's a790aef

- Their H27-invariant mediator vacuum re-runs cleanly: full Hessian rank 14, no residual singlet moduli. Our run restores their certificate afterwards.
- The model contains only SO(10)-singlet u, v, one adjoint Cartan along U(1)_ψ, and E₆-neutral mediators. The 27 masses still come from 27̄·27·(1 + 78) along ψ, so the light states remain complete SO(10) multiplets.
- **It has no 650 and no 75 component, so question 4 of `REQUEST_E6_INTERMEDIATE_SCALE_SUSY.md` stays open.** It is now sharpened to: does their vacuum admit a misaligned SU(5)-75 VEV inside a 210 ⊂ 650?
- Their 9D H27 code and Hasse layers do not bear on this representation question.

## Status

- **A** needs either y_τ ≥ 1.8× SM (τ on an enhanced doublet) or an explicit tree-level N splitting.
- **B:** y′ ∈ [0.495, 0.532].
- **Hybrid:** needs a misaligned 75 direction of the 650, which is beyond the known single-650 vacua, and M_SS ≳ 3×10⁹ GeV for both good unification and separation from B.

All three remain conditional.
