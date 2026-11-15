# Pass 12673: exact torus eigenvalue formula; certified code-space lower bound 2.49; torus code spaces at q = 32; a global symmetry-reduced degree-6 SOS

Claude track. Follows Pass 12672. **Not a theory of everything.**

## 1. Exact: the torus eigenvalue formula (`w33_f8_torus_eigen_exact.py`)

On the code space, c(ρ) = Σ_t Σ_{a∈L_t∖0} tr(ρE_a)² depends only on the nine effective Lagrangians as point sets. It is evaluated in a standard three-qubit Pauli model reached by a symplectic basis change; signs are irrelevant for squares.

The lift of σ is built exactly over Q(ζ₇₂), normalised so that U⁹ = I, and the eigenprojectors are P_j = (1/9)Σ_k ζ₉^{−jk} Uᵏ. **In exact arithmetic**, for every lift checked (16 in a first run, 3 in the recorded run):
- one projector is zero (index j₀) and the other eight have rank one;
- with r = j − j₀, **c(P_j) = (47 − 16(ζ₉^{2r} + ζ₉^{−2r}))/9 = (47 − 32cos(4πr/9))/9** for r = ±1, ±2, ±4, and **37/3** for r = ±3.

**All 64 lifts follow.** H_d V H_d† ∝ V·H_{(σ⁻¹+1)d}, and σ⁻¹ + 1 is invertible over F₂ because σ has no fixed points (checked). So every lift V·H_c is Pauli-conjugate to V. Pauli conjugation preserves c and shifts the spectrum by a common phase, which leaves r unchanged.

> **Theorem (exact).** The 512 eigenstates of the Clifford lifts of the order-9 torus on the code space carry exactly the values (47 − 32cos(4πr/9))/9 (r = ±1, ±2, ±4) and 37/3 (r = ±3). The minimum c₈ is r = ±4.

This upgrades Pass 12672 §1b from numerical (2.3×10⁻¹⁴) to exact.

## 2. Certified: 64F ≥ 2.49 on the code space (`w33_f8_codespace_sos6_certify.py`)

Basis: the 8 projector columns B₀, with entries in {0, ±1/8, ±i/8}, so every coefficient is a Gaussian rational. Certificate:

  (tᴴGt)·(64Σ|w_j·t|⁴ − (9 + C)(tᴴGt)²) = m₃ᴴX₃m₃ + m₁ᴴX₁m₁,

with charge blocks of size 120 and 288.

Method:
1. SCS solves at fixed C, maximising the minimum Gram eigenvalue.
2. Round to denominator 2⁴⁰.
3. Exact orthogonal projection onto the 14,400 coefficient constraints. Each Gram entry feeds one coefficient, so the projection is closed-form and preserves Hermiticity.
4. Exact PSD proof on the real embedding: Y − δI = LLᵀ + E with a dyadic L and an integer-exact residual E, where ‖E‖_F < δ.

| C | SCS margin | ‖E‖²_F/δ² (blocks 3, 1) | certified |
|---|---|---|---|
| 49/20 = 2.45 | 1.09×10⁻⁴ | 3×10⁻²³, 8×10⁻²⁰ | yes |
| 62/25 = 2.48 | 3.89×10⁻⁵ | 1×10⁻²², 1×10⁻¹⁸ | yes |
| **249/100 = 2.49** | 1.56×10⁻⁵ | 2×10⁻²², 7×10⁻¹⁸ | **yes** |

> **Theorem (exact certificate).** On the 8-dimensional code space of T, 64F ≥ 249/100. With the Pass 12671 witness, the code-space minimum lies in [2.49, (47 − 32cos 2π/9)/9 = 2.498508…].

This is not a global bound. The degree-6 value at this level is 2.4967 (Pass 12672), so degree 6 can never reach c₈ here.

## 3. Torus code spaces at q = 32 (`w33_regulus_torus_invariant_codespaces.py`, `w33_regulus_torus_clifford_eigenspaces.py`)

**Structure at q = 8.** S = (g, g) with g of order 9 has order 9 on F₂¹². Its fixed space is 6-dimensional, and all 63 of its non-zero vectors are uncovered (det acts there like the norm of F₆₄). The complement is the Φ₉ block. T lies in the fixed space. Searching isotropic uncovered 3-subspaces of the fixed space reproduces c₈ (120 of 480 code-space/sign choices; the others give 3 or 7).

**q = 32.** The structure is the same. S = (g, g) with g of order 33 has order 33 on F₂²⁰, its fixed space is 10-dimensional, and all 1,023 non-zero vectors are uncovered (a copy of F₁₀₂₄ with det acting as a norm). The greedy search found 3,000 isotropic uncovered 5-subspaces in it. On the 32-dimensional code spaces of 3 of them (× 32 sign choices; stopped by the time limit), the best value is **exactly 11, the stabiliser value**, with nothing below it.

**Unequal-trace torus pairs at q = 32.** Two pairs: (20, 28) gives 15.044 (33 eigenspaces, dimensions 29–32), and (20, 23) gives 13.597 (dimensions 20–33). Both are above 11.

> **q = 32 conclusion.** Every torus construction tried (equal-trace eigenspaces 12.4896, unequal-trace 13.6 and 15.0, fixed-space code spaces 11) stays at or above the stabiliser value 11. The q = 8 phenomenon, a non-stabiliser optimum on a torus-fixed code space, does not recur at q = 32 in these searches. This is evidence, not a proof, that c₃₂ = 11.

## 4. A global degree-6 SOS by symmetry reduction (`w33_f8_global_sos6.py`)

The problem is f_c = |ψ|²(Σ_{P∈Ccov}|⟨ψ|P|ψ⟩|² − c|ψ|⁴) over all of C⁶⁴. Two symmetries reduce it:
- **Heisenberg group.** Monomials split by Z-character, and X-shifts relate the character blocks. One block of each charge suffices: B₁ = {ψ_xψ_y ψ̄_{x⊕y}} (2,080) and B₃ = {ψ_xψ_yψ_{x⊕y}} (715).
- **Singer cycle Z₆₃ ⊂ GL(2,8).** It preserves F by index permutations. The block monomials form 34 + 13 orbits, the Fourier blocks have size at most 34 complex (68 real), and there are 8,131 coefficient classes under shifts ⋊ Z₆₃.

In that first formulation (`w33_f8_global_sos6.py`) the SDP has 156,406 variables and nnz(A) = 3.6×10⁷. SCS's sparse factorisation alone took 1,240 s, and the run did not finish.

**Second formulation (`w33_f8_global_sos6_v2.py`).**
- The symmetry group is enlarged to Γ = ΓL(1,64) (order 378): the Singer cycle, the F₈-linear x ↦ x⁸ and the coordinatewise Frobenius, all checked numerically to preserve F.
- The variables are values of the invariant Gram matrix on Γ-orbits of monomial **pairs** (11,560 for B₁, 1,416 for B₃). Each feeds exactly one of the 1,416 coefficient classes.
- PSD is imposed on one Z₆₃-Fourier block per orbit of characters.
- The result is 12,977 variables, 2,832 equalities, 26 PSD blocks (at most 68 real) and nnz = 3.4×10⁶, solved by SCS in 979 s.

| run | expected | SDP value |
|---|---|---|
| control: all 4,095 Paulis (the polynomial vanishes identically at 63) | 63 | **63.0000000000** |
| control: q = 4 (F₄ regulus, five MUBs of C¹⁶), same code | 16 × 0.0452 (Pass 12660, independent Pauli-reduced degree-6 SOS) = 0.723 | **0.7224946** (0.045156 in F) |
| **q = 8, the nine F₈-regulus MUBs** | ? | **0.7603388** |

> **Result (numerical SDP, validated by two known-answer controls).** The best global degree-6 SOS bound is 64F ≥ 0.760, about 30% of c₈. It is weaker than the existing 2.0818 bound (other track, PPT dual). On the code space the same degree gives 2.4967. At q = 4 degree 6 reaches 72% of the true value.
>
> So degree-6 SOS is far from tight globally at q = 8, and it is not the route to a global proof. The positivity of F away from the code space needs more than degree 6. The two-copy PPT relaxation also fails (≤ 0; other track, 056c4fc9f); the PPT-dual construction behind 2.0818 is the stronger tool.

**Ceiling (as predicted).** Any global degree-6 certificate restricts to one on the code space, so the global degree-6 bound is at most 2.4967 < c₈; the computed value 0.760 is far below even that. Proving c₈ needs degree 8 or more (or more copies). The other track's two-copy PPT counter-certificate (056c4fc9f) shows the symmetric two-copy relaxation gives at most 0.

## Prior art and ownership

- The code space, torus mechanism and witness are Passes 12671–12672 (Claude track).
- The exact rational witness and the two-copy PPT obstruction are the other track's (3c373c924, 056c4fc9f). The PPT-dual bound 2.0818 is common code.
- The certification method follows Pass 12660's validated type-B bound, here with an exact LDLᵀ residual instead of diagonal dominance.
