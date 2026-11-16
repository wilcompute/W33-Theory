# Pass 12677: torus levels are uniform algebraic numbers at q = 4, 8, 16, 32; the type-C code space is an E₈/2E₈ structure; the qutrit side of the E₆(a₁) bridge

Claude track. Follows Pass 12676. **Not a theory of everything.**

## 1. Uniform arithmetic of the torus levels (`w33_q32_torus_level_eigenspace_newton.py` with REG_K, `w33_q32_torus_level_identify.py`)

For each q the equal-trace torus-Clifford eigenspace minimum τ_q was refined to 45 digits:
- the eigenspace is computed exactly (W = ±1/√q² entries after removing a global phase) by iterative refinement;
- Newton in mpmath then runs inside the eigenspace (final gradients ~10⁻⁵²);
- the value is identified by pslq in Q(cos 2π/(q+1)), and checked by forming the Galois-conjugate polynomial.

| q | τ_q | (q+1)·τ_q in powers of g = 2cos(2π/(q+1)) | degree | conjugate polynomial integral to | τ_q smallest conjugate | stabiliser min | τ_q vs it |
|---|---|---|---|---|---|---|---|
| 4 | 1.21114561800016824287… | 11 − 8g, i.e. τ = (15 − 4√5)/5 | 2 | 3×10⁻⁴⁹ | yes | 1 | above |
| 8 | 2.49850864668807809705… = c₈ | 47 − 16g | 3 | exact (Pass 12669–12671) | yes | 3 | **below** |
| 16 | 5.59643098750834375751… | 271 + 112g + 160g² − 432g³ − 112g⁴ + 224g⁵ + 16g⁶ − 32g⁷ | 8 | 9×10⁻³¹ | yes | 1 | above |
| 32 | 12.48962076764063949717… | 1183 + 32g + 416g² + 960g³ − 1568g⁴ − 896g⁵ + 864g⁶ + 288g⁷ − 128g⁸ − 32g⁹ | 10 | 6×10⁻³⁰ | yes | 11 | above |

> **Observed law (q = 4, 8, 16, 32).** The torus level τ_q is (q+1)⁻¹ times an algebraic integer of full degree φ(q+1)/2 in Q(cos 2π/(q+1)), and it is the smallest of its Galois conjugates. Only at q = 8, where q + 1 = 3², does it fall below the stabiliser minimum (Pass 12675 conjecture).

The mean of the conjugates, Tr/(deg·(q+1)), is exact because the polynomials are integral: 3, 47/9, 15, 4891/165. For even k it equals **q − 1** exactly; for odd k it does not. This is recorded as an observation, without a mechanism.

## 2. The type-C code space is an E₈/2E₈ structure (`w33_f8_typeC_quadric.py`)

The global order-9 symmetry (m ↦ g·m·hᵀ, ord g = ord h = 9) normalises T. It therefore fixes T's unique type-A subgroup and its unique type-C subgroup, and maps the five type-B subgroups among themselves; the type-B representative tested is fixed. On each 8-dimensional effective phase space S′^⊥/S′ it acts with orbits 9 × 28 + 1 × 3, and it preserves four quadratic forms: three elliptic and **one hyperbolic** (135 singular + 120 nonsingular points, the E₈/2E₈ type; W(E₈)/{±1} = O⁺(8,2)).

| type | covered cosets relative to the invariant hyperbolic form |
|---|---|
| **C** | **all 90 covered cosets (weights 1, 2, 3: 54 + 27 + 9) are singular; all 120 nonsingular points (the 120 root classes of E₈) have weight 0** |
| A | mixed (weight 1: 36 nonsingular, 27 singular; weight 2: 18 + 18) |
| B | mixed (weight 1: 36 + 63; weight 2: 18 nonsingular) |

> **Type C carries a clean E₈/2E₈ structure.** No covered Pauli coset lies on an E₈ root class; all lie in the 135-point norm-4 shell. Type C is also the 16-dimensional code space with the strongest degree-6 bound (2.4967, equal to the T code-space value; Pass 12675), while A and B have 2.0818 and 2.4729. The cleanest geometry coincides with the tightest relaxation.

So the chain of code spaces around the minimum reads T (8-dim, E₆/2E₆, Pass 12675) ⊂ C (16-dim, E₈/2E₈). The corpus's "240 = 240" question (E8 roots vs W(3,3) edges) was closed negatively in Pass 1020; nothing here reopens it.

## 3. The qutrit side (`w33_qutrit_E6a1_eigenstates.py`)

- **PSp(4,3) has exactly 5,760 elements of order 9**, the size of the E₆(a₁) class of W(E₆) (centraliser of order 9). This is consistent with the order-9 class corresponding under W(E₆)⁺ ≅ PSp(4,3).
- **The eigenstates of two-qutrit Clifford lifts** of one such element (all 81 Pauli corrections, 513 one-dimensional eigenspaces) have stabiliser fidelity **(2 + 2cos 2π/9)/9 = 0.3924543** (324 states), 4/9 (162) or 1 (27). So Q(cos 2π/9) arises on the two-qutrit side from Clifford eigenstates of the E₆(a₁) element, not only from the qutrit T gate.
- **Comparison with Pass 11253** (exact Clifford+T time-reversal fidelity levels): no cubic level matches. The only coincidence is 4/9 = (2/3)² with the one rational 11253 level, which is too small and too common to count. **The two-way bridge is at the level of the class and the field, not of the specific numbers.**

## 4. The degree-8 certificate: both sides

- At C = 2.498509 (3.5×10⁻⁷ above c₈) the SCS margin is −3.6×10⁻⁷ and certification fails, as it must.
- Below c₈ the margin equals the gap (Pass 12674); the face has 383 = 3 × 128 − 1 complex dimensions (Pass 12676).
- Exact facial reduction at c₈, which needs the 128 eigenstates' monomial vectors in the effective Fourier blocks, is still identified but not done.
