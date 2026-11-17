# Pass 12683: degree 8 is not tight on orbit A (2.4463) nor globally at q = 4 (0.965 vs 1); the other track's E6 -> SU(5) -> SM vacuum on two-qutrit frames: the VEV pair is a skew frame pair and the SU(5) 5 is its five tensor factorisations

Claude track. Follows Pass 12682 (addendum D). **Not a theory of everything.**

## 1. Solver: Clarabel with static regularisation

The symmetry-reduced SOS pipeline (`w33_f8_symmetric_sos8.py`) now has a Clarabel option (`SOLVER=clarabel`). Clarabel's PSD triangle is the upper triangle in column-major order, while SCS's is the lower one, so the rows of each cone are permuted.

- **T code space (control).** Clarabel solves in 2.8 s and gives **2.4985085993**, against c₈ = 2.4985086467. The fresh-point identity error is **5.5×10⁻¹⁴**, compared with 2×10⁻⁸ for SCS.
- **The 16-dimensional SDPs.** With the default static regularisation (10⁻⁸), Clarabel stops at iteration 1 with a NumericalError. The cause is not structural: there are no empty columns and no untouched cone diagonals. The sampled equality block has condition number 6×10⁴. A regularisation of 3×10⁻⁷ to 3×10⁻⁶ fixes it, and this is now the default.
- **Re-solving without the setup.** `DUMP=<prefix>` saves the SDP, and `w33_f8_sdp_dump_solve.py` re-solves it in about 30 s instead of 20 minutes. It also reports the equality residual and the smallest cone eigenvalue of the returned point.

## 2. Orbit A, degree 8: 2.4463, about 0.052 below c₈

| static reg. | status | bound | max equality residual | min cone eigenvalue |
|---|---|---|---|---|
| 3×10⁻⁷ | Solved | **2.4462862** | 1.2×10⁻⁹ | +3.0×10⁻⁷ |
| 1×10⁻⁶ | Solved | 2.4456421 | 1.1×10⁻⁸ | +3.7×10⁻⁷ |
| 3×10⁻⁶ | Solved | 2.4442152 | 3.0×10⁻⁸ | +2.8×10⁻⁷ |

Every returned point is feasible (all cone eigenvalues positive, equalities met to 10⁻⁸), so each value is a numerical lower bound. Regularisation biases the optimum downward, so the best value, 2.44629, is the closest to it. The unconverged SCS value of Pass 12682 D (≈ 2.4463) agrees.

> **Result (numerical).** On the orbit-A code space the degree-8 SOS value is ≈ 2.4463, below c₈ = 2.4985 by about 0.052. **Degree 8 is not tight on orbit A**, unlike the T code space, where it equals c₈ (Passes 12674, 12678). Orbit A carries half of the generic global minimisers as a positive-dimensional family, and degree 8 does not certify that family's level. Certifying c₈ there needs degree ≥ 10 or a face/symmetry argument. For comparison, degree 6 on orbit A gives 2.0818.

Caveat: these bounds rest on the sampled identity (rank 151, saturated). Pass 12682 D checked it at fresh points to 5.6×10⁻⁶. They are not rational certificates.

## 3. Global degree 8 at q = 4: 0.965, not 1

The **whole** F₄-regulus problem (five MUBs of C¹⁶; not a code space) is a weighted four-qubit model. It has 75 covered Paulis, each of weight 1 (`w33_f4_global_model.py`). Its Pauli-symmetry group in Sp(8,2) has order **14,400**, found by symplectic backtracking. The subgroups fixing 1, 2 or 3 of the five bases have orders 1,440, 360 and 120. The true minimum is c₄ = 1: 40 of 40 random starts reach 1.000000, and Pass 12672 records it as the stabiliser value.

With the order-360 subgroup, the symmetric SDP has 6,797 variables, 305 invariant identities (rank saturated at 400 samples), 195 cones (largest 88) and 2.0×10⁷ nonzeros. Clarabel (static regularisation 10⁻⁶) solved it in 7,039 s:

  **global degree-8 bound at q = 4: 0.96492** (fresh-point identity error 2.2×10⁻⁷)

| q = 4, global | bound |
|---|---|
| degree 6 (Pass 12660/12673) | 0.7225 |
| **degree 8 (this pass)** | **0.9649** |
| true minimum | 1 |

The regularisation bias measured on orbit A is about 0.002, far below the 0.035 gap.

> **Result (numerical).** Even for five MUBs in C¹⁶, degree-8 SOS is not globally tight. It closes 87% of the degree-6 gap but stops 3.5% short of the stabiliser value. So for nine MUBs in C⁶⁴ a global degree-8 certificate of c₈ is very unlikely: degree 6 there reached only 30% (0.760 of 2.4985). The global proof of c₈ needs degree ≥ 10, an extra multiplier, or a non-SOS argument.

**Pipeline speed-up (exact).** On a right coset H_w g, b_w(U_hU_gψ) = R_h b_w(U_gψ), and Y_w is H_w-invariant. So the group average needs only one g per coset, i.e. per distinct label g⁻¹·w. This costs the orbit size instead of |G| per block. Re-validated on T: 2.4985085381, identity error 2.3×10⁻¹³. The pipeline also takes a general degree (`HALF`). Degree 10 on T is redundant, since degree 8 is already tight there. Degree 10 on orbit A has blocks of about 430 and is too large for this machine without more symmetry.

## 4. Parallel work: the other track's E₆ → SU(5) → SM candidate (6a4a37517), replicated

The other track computed the full Lie stabiliser of the E₆ cubic I₃ = det A + det B + det C − Tr(ABC) by exact elimination and reported this chain:
- 78 derivations;
- two singlet 27+27̄ VEV pairs (A = e₃e₃ᵀ, e₃e₂ᵀ) leave 24 generators (A₄ = su(5));
- an adjoint VEV along Y = (Y_L, Y_R, Y_C) = (diag(1,1,−2), diag(4,−2,−2), 0) leaves 12 generators, su(3) ⊕ su(2) ⊕ u(1).

**Independent replication** (`w33_pass12683_e6_su5_sm_replication.py`) uses different code: its own I₃ gradient, 1,600 random sample points and SVD ranks, with no exact elimination. It gives **78 / 24 / 12**. The Y spectrum on the 27, with multiplicities {−6: 1, −3: 2, −2: 6, −1: 6, 0: 2, 2: 3, 3: 4, 4: 3}, reproduces their content under Y_SM = −Y/6: e^c, H_u, 2d^c, Q, 2N, D, 2L, u^c. **PASS.**

Their note itself says the branching is established E₆ group theory. Two singlet VEVs give SO(10) ∩ SO(10)′ = SU(5), and an adjoint breaks that to the SM, in the Georgi–Glashow way. What is new there is the automated full-stabiliser certificate.

**One addition that bears on their next problem 2** (a SUSY superpotential for 2×(27+27̄) + 78):
- **E₆ has no cubic Casimir.** The invariant degrees are 2, 5, 6, 8, 9, 12; numerically Tr X³ / |X|³ = 4×10⁻¹⁷ for a random X in e₆ on the 27. So the renormalisable self-superpotential of the 78 is only ½m TrΦ².
- **Y annihilates both VEVs** (Y v₁ = Y v₂ = 0, ⟨vᵢ|Y|vⱼ⟩ = 0). Take renormalisable W = ½m TrΦ² + μ H̄H + λ H̄ΦH + κH³ + κ̄H̄³. At their vacuum the Y-component of F_Φ is m·v_Y, and F_H̄ = μ·v: the cubic terms vanish there because rank-≤1 matrices have zero adjugate, and ΦH = 0.
- **Consequence.** F-flatness forces m = 0, and forces μ to vanish on the VEV directions. Every breaking scale is then a flat direction that renormalisable W cannot fix. This is not a no-go: non-renormalisable terms, larger representations such as 351′ or 650, or SUSY breaking can lift it. But "precise vacuum scales" cannot come from the renormalisable superpotential of this field content. It is the same pattern as this track's D-flat-or-empty-superpotential lesson (Gordan alternative, Pass 10960 line), and the known reason E₆ SUSY GUTs use 351′/650 or higher-dimension operators.

**Update after 6442db4d6 / 17e3dc053.** The other track independently found the same degree-5 obstruction: quadratic + quintic invariants cannot stabilise Y on its 16-dimensional centraliser. They lift it with Tr Φ⁶ (coefficients (−283, 3, 1) in Σ c_d TrΦ^d/d) plus a Gram "lock" term, getting a Higgs-sector minimum that is isolated modulo gauge at tree level, from chosen non-renormalisable operators. That is the non-renormalisable route anticipated above. Their vacuum is the one used in section 5.

## 5. The vacuum's incidence shadow on two-qutrit frames (`w33_pass12683_su5_vacuum_skew_frames.py`)

**Dictionary used** (Claude track, 5419c27; GQ(2,4) factors as in `gq24_lives_inside_w33_as_its_octet_factors.py`):
- The 40 Pauli classes of C³⊗C³ are the points of W(3,3).
- A tensor factorisation is an octet L ∪ L^⊥ (45 of them).
- A complete factorisation frame is 5 factorisations whose octets partition the 40 classes; there are 27 frames.
- Two frames share one factorisation or none. That gives the Schläfli graph, i.e. the 27 lines of the cubic surface: lines meet exactly when their frames share a factorisation.

**Part A (their basis).** Two of the 27 weights of I₃ meet exactly when they lie in a common cubic monomial. Their two SU(5)-breaking VEVs e₇ = A₃₂, e₈ = A₃₃ share a row of A, so no monomial contains both: **the VEV pair is a skew pair of lines.** Classifying the other 25 weights by incidence with the pair, and reading off their hypercharges:

| incidence with (F₁, F₂) | size | content (Y_SM) | SU(5) |
|---|---|---|---|
| F₁, F₂ themselves | 1 + 1 | N, N (the VEVs) | 1 + 1 |
| meets both (common transversals) | 5 | **D (3,1)₋₁/₃ ×3, H_u (1,2)₁/₂ ×2** | **5** |
| meets F₁ only | 5 | d^c ×3, L ×2 | 5̄ |
| meets F₂ only | 5 | d^c ×3, L ×2 | 5̄ |
| skew to both | 10 | Q ×6, u^c ×3, e^c | 10 |

So **27 → 1 + 1 + 5 + 5̄ + 5̄ + 10 is exactly the incidence partition of the 27 lines relative to a skew pair.**

**Part B (two qutrits).** A graph isomorphism carries (e₇, e₈) to a skew pair of frames (F₁, F₂), which share no factorisation, and carries Y to the frames:
- The **five common transversal frames** are mutually skew. The map "transversal ↦ the factorisation it shares with F₁" is a **bijection onto F₁'s five tensor factorisations**, and likewise onto F₂'s.
- So the SU(5) fundamental **5 is the set of the five tensor factorisations of the VEV frame.** Of these, **3 carry the colour triplet D and 2 carry the weak doublet H_u.**

**Part C (symmetry).** The unitary Cliffords mod Paulis, PSp(4,3) of order 25,920, act faithfully on the 27 frames. The stabiliser of the ordered VEV-frame pair has **order 60 and acts on the five transversals as A₅**, the even half of W(A₄) = S₅. The odd half, which includes every single Weyl reflection, is realised only by antiunitaries, matching the chirality-torsor result (e92a047). The doublet–triplet choice (which 2 of the 5 factorisations are "weak") is one orbit of 10 under this group, with stabiliser of order 6 = (S₃ × S₂) ∩ A₅.

> **Scope (read this).** This is an exact incidence/Weyl-level dictionary, not a derivation of gauge fields from W(3,3); see the PASS7376–7384 caution. The SU(5) Lie algebra, the vacuum dynamics and the hypercharge values come from the other track's E₆ construction. What W(3,3) supplies:
> - **(i)** the 27 as two-qutrit factorisation frames;
> - **(ii)** the breaking pattern E₆ ⊃ SU(5) as "fix an ordered pair of frames sharing no factorisation". Skew-pair stabilisers 216/240 are already in the other track's 2026-11-13 ExFT note, there in "five-axis section" language;
> - **(iii)** the SU(5) multiplets as incidence classes, and the 5 as the five tensor factorisations of a frame;
> - **(iv)** the doublet–triplet split as a non-canonical choice of 2 of those 5 factorisations. The frame geometry does **not** select it (orbit of 10). This matches the other track's finding that their triplet filter is a tuned coefficient relation that hypercharge alone cannot protect (0e967f8ef).
>
> The classes themselves are classical cubic-surface geometry (Schläfli; the 5 transversals of a skew pair). The new content is the identification with the explicit vacuum and with two-qutrit factorisations.

## Addendum A: the doublet–triplet split is a choice of measurement context (`w33_pass12683_doublet_triplet_contexts.py`)

Section 5 left the doublet–triplet choice (which 2 of the VEV frame's 5 factorisations are "weak") unselected: one orbit of 10. We scanned natural W(3,3) objects for those whose stabiliser inside the unitary pair-stabiliser (A₅) splits the five transversals:

| object | number | stabiliser | orbits on the 5 transversals |
|---|---|---|---|
| point (Pauli class) | 40 | 3 | 1 + 1 + 3 |
| factorisation | 20 / 15 / 10 | 3 / 4 / 12 | 1+1+3 / 1+4 / 1+4 |
| isotropic line (measurement context) | 30 | 2 | 1 + 2 + 2 |
| **isotropic line (measurement context)** | **10** | **6** | **2 + 3** |

**Exactly 10 of the 40 measurement contexts induce a 2 + 3 split, and they correspond one-to-one to the 10 doublet choices.** A context here is 4 mutually commuting two-qutrit Pauli classes, i.e. a joint eigenbasis of 9 states. Each of these 10 contexts:
- meets the octets of the two **weak** factorisations in 2 points each (one local Pauli per qutrit), and the three **colour** octets in none;
- does this in **both** VEV frames F₁ and F₂.

Checked with matrices, for all 10 contexts and all 9 eigenvectors:

> **In the two weak factorisations the context's eigenbasis is a product basis (Tr ρ_A² = 1). In the three colour factorisations it is maximally entangled (Tr ρ_A² = 1/3).**

So in this dictionary, the SU(5) → SM step (the adjoint VEV along Y) corresponds to choosing a measurement context compatible with the two VEV frames:
- **weak** = the 2 tensor factorisations in which that measurement is separable;
- **colour** = the 3 in which it is maximally entangled.

> **Scope.** This is still a choice: an orbit of 10, so W(3,3) does not *select* the split. It also remains a Weyl/incidence-level correspondence, not a derivation of SU(3)×SU(2) dynamics. What it adds is a physical name for the other track's free adjoint direction: a maximal commuting set of two-qutrit observables. It also turns "why 3 + 2?" into a statement about entanglement: a context compatible with two skew frames is separable in exactly 2 of a frame's 5 tensor factorisations. It does not explain the other track's triplet filter. An open question this raises: does an independently motivated context, for example the clock context of P12052 or the computational-basis context, land in this special orbit of 10?
