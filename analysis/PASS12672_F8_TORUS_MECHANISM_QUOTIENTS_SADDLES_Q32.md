# Pass 12672: why cos(2π/9) — the F₈ minimum is a three-qubit problem cycled by the norm-one torus of F₆₄; exact quotient bounds; a second critical level; code-space lower bounds; q = 32

Claude track. Follows Pass 12671 (exact witness, 3d06c2738). **Not a theory of everything.**

## 1. Mechanism: nine three-qubit stabiliser bases, one orbit of the order-9 torus (`w33_f8_effective_three_qubit.py`)

On the 8-dimensional code space of T = ⟨−iP(12,53), P(53,33), P(1,6)⟩ (Pass 12671), the objective is an effective three-qubit problem.
- Each of the nine MUBs has exactly 7 covered Paulis in T^⊥.
- They map to the 7 points of a Lagrangian L_t of T^⊥/T ≅ F₂⁶ (the symplectic space W(5,2)).
- Hence **c₈ = min over ψ ∈ C⁸ of 8·Σ_t Σ_k p_{t,k}(ψ)² − 9**, over nine three-qubit stabiliser bases. They are **not** mutually unbiased.

The coset weights (the number of covered Paulis per effective Pauli) are 0 (27 points), 1 (18), 2 (9) and 3 (9). The weight-0 set is not a quadric (tested).

The nine Lagrangians are **circulant**. Along the cycle 0-4-3-7-2-8-1-5-6:
- neighbours at step 1 meet in a line;
- step 2 meet in a point;
- steps 3 and 4 meet trivially.

**There is exactly one symplectic map σ with σ(L_i) = L_{i+1}.** It has order 9, neither σ nor σ³ has fixed points, and **σ⁶ + σ³ + 1 = 0**. Since Φ₉ is irreducible over F₂, F₂⁶ = F₂[σ]/Φ₉ ≅ F₆₄, and σ is multiplication by an element of order 9: a generator of the norm-one torus of F₆₄. σ preserves the weights.

> **The cos(2π/9) mechanism.** The nine effective bases form one orbit of the order-9 torus of F₆₄ acting on the effective three-qubit phase space. The minimising state is not torus-invariant: Pass 12671 found it isolated, and §1 of that note showed the order-9 *linear* symmetries of the full problem are broken. But the effective configuration is Z₉-circulant, and the value lies in the real subfield Q(cos 2π/9) of Q(ζ₉).

This turns Pass 12669's remark ("9 = q + 1 = order of the norm-one torus; no mechanism derived") into a computed structure. A derivation of the value from the circulant structure (e.g. a Fourier diagonalisation over Z₉) is not done.

### 1b. The minimiser is a Clifford eigenstate of the torus (`w33_f8_clifford_eigenstates.py`)

The exact witness's squared-expectation table on the effective space is invariant under every power of σ.
- σ has 64 Clifford lifts V on C⁸, unitaries with V E_a V† ∝ E_{σ(a)}. **Exactly one fixes the witness, which spans a one-dimensional eigenspace of it.**
- Normalise each lift so that V⁹ = I. Its spectrum is all nine 9th roots of unity but one. Measuring j from the absent root, the eigenvector ψ_j of ζ₉ʲ has, for **all 64 lifts (512 eigenvectors)** with maximum deviation 2.3×10⁻¹⁴:

  **64F(ψ_j) = (47 − 32 cos(4πj/9))/9 for j = ±1, ±2, ±4**, and **64F(ψ_j) = 37/3 for j = ±3**.

- The three primitive pairs give the three roots of the cyclic cubic: j = ±4 gives c₈, j = ±1 gives 4.6048 and j = ±2 gives 8.5634. They are cycled by ζ ↦ ζ², the Galois group of Q(cos 2π/9). The non-primitive pair gives the rational 37/3, the same value as the j = 0 order-9 eigenspace in Pass 12671 §1.
- So the minimiser is a "magic state" in the sense of being an eigenvector of a non-Pauli Clifford. This parallels Howard's result that Clifford-eigenstate magic states optimise Pauli entropic uncertainty (arXiv:1501.05319); here the Clifford acts on an emergent code space.

### 1c. Exact: the cubic is the Galois orbit of a critical point (`w33_f8_galois_conjugate_witnesses.py`)

- Let τ: γ ↦ γ² − 2 generate Gal(Q(γ)/Q), extended to K = Q(γ, √3, i) fixing √3 and i. It commutes with complex conjugation.
- Hermiticity, tr = 1, ρ² = ρ and criticality are polynomial identities over Q. Criticality means [G(ρ), ρ] = 0, with G(ρ) = Σ_t U_tᵀ diag(2p_t) U_t.
- So τ maps pure critical states to pure critical states. **Checked in exact arithmetic:**
  - ρ (the Pass 12671 witness) is an exact critical point;
  - τ(ρ) and τ²(ρ) are exact pure critical states with 64F = (79 − 16γ²)/9 = 4.6048… and (15 + 16γ + 16γ²)/9 = 8.5634….

> The three roots of 243c³ − 3807c² + 17577c − 23941 are all exact critical values of F, realised by Galois-conjugate pure states. c₈ is the smallest. That the minimum is cubic-irrational, rather than of higher degree, is explained by the witness's field.

**Not inherited from GL(2,8).** The normaliser of S in GL(2,8) has order 56 and contains no element of order 9. σ is a symmetry of the code-space problem that is not induced by the linear symmetry group used in Pass 12671 §1. Whether it lifts to another element of the full Clifford symmetry group of the regulus set is not checked.

## 2. Exact bounds for both five-qubit quotient 9-sets (`w33_f8_quotient_exact_corollary.py`)

The other track showed that the two shortening Paulis (12,51) (determinant 1, spectral type 27) and (57,34) (determinant 3, type 17) lie in Pass 12660's stabiliser S, and replayed the quotient objective on its rational witness (`toe_20261114_regulus_quotient_witness.py`, 3228ba7bf). Running their replay, in their determinant/trace-pairing convention, on the exact expectations of the Pass 12671 witness, in exact arithmetic over Q(γ, √3):
- the parent value from *their* covered set (det = 0, 567 labels) is exactly 47/9 − 16γ/9, an independent cross-check of the convention;
- for both shortening Paulis the witness is stabilised exactly, all anticommuting covered expectations vanish, there are 279 quotient representatives, and the quotient objective equals the parent value exactly.

> Both five-qubit quotient 9-sets have **exact** upper bound (dimension-scaled) (47 − 32cos(2π/9))/9, i.e. min F ≤ (47 − 32cos(2π/9))/288. This supersedes their rational bound 2.49850865922; the lower bounds are unchanged (the parent minimum, by the quotient lemma).

## 3. A second critical level, identified (`w33_f8_saddle_levels.py`)

The rank-3 code-space minima at q = 8 take the values 2.4985 (c₈), 2.74109, 3 and 7. A random-group control (`w33_q32_codespace_search.py` at q = 8) also finds 2.81234.
- Every code-space critical point is a critical point of F on C⁶⁴ (symmetric criticality). This is checked directly: the full 64-dimensional gradient norms are at most 5×10⁻⁹.
- Newton's method in mpmath refines 2.74109 to 35 digits: **c = 2.7410899853553475002632635110618726**. It satisfies **13c³ − 265c² + 1447c − 2243 = 0**.
- The discriminant is 2¹⁴·37³, which is not a square. So the Galois group is S₃, with resolvent Q(√37), unlike the cyclic cubic of c₈.
- The Hessian null space on the code space has dimension 4, a one-parameter family.
- The weaker levels 2.757 ≈ 7 − 3√2 (Pass 12669), 2.6848 and 2.81234 are not refined here.

## 4. Lower bounds on the code space (`w33_f8_codespace_sos.py`, `w33_f8_codespace_quillen.py`, `w33_f8_codespace_sos6.py`)

These bound the minimum *on the code space* only. Even an exact match would not bound the global minimum.

| method | size | bound | c₈ |
|---|---|---|---|
| degree-4 real SOS (16 real variables) | Gram 136 | 1.000 | 2.4985 |
| Hermitian Quillen hierarchy, k = 0…6 | up to 6,435 monomials | −9, −3.67, −3.67, −0.91, −0.28, 0.367, **0.391** | 2.4985 |
| degree-6 phase-block SOS (charge blocks 120 + 288) | SCS | running; reported in an addendum | 2.4985 |

The k = 0 value −9 is the code-space analogue of the other track's global two-copy relaxation, which also gives −9 (9b576804d). The Quillen hierarchy converges, as it must (Catlin–D'Angelo), but slowly. The plain SOS hierarchies on this problem are far from tight at low degree, consistent with the degree-6 global bound 0.0452 at q = 4 (Pass 12660). A matching lower bound remains open.

Solver note: an interior-point solver on the 576×576 real PSD block needs a dense (576·577/2)² scaling matrix (220 GB). The first-order SCS was used instead.

## 5. q = 32: Pauli code spaces against the stabiliser value 11 (`w33_q32_codespace_search.py`)

Control: on random states, d·F from the CZ model equals the sum over the 33·1023 covered Paulis (det = 0), at q = 32 and at q = 8. The method also reproduces c₈ at q = 8 from random rank-3 uncovered groups.

The 40-minute random search over rank 4–7 groups is running; its result will be reported in an addendum.

## Prior art and ownership

- The order-4 stabiliser is Pass 12660. The exact witness is Pass 12671.
- The quotient types, the shortening labels and the replay code are the other track's (3228ba7bf). Their rational witness bound is superseded only as an upper bound; their construction stands.
- Quillen (1968) and Catlin–D'Angelo (1996) are used for the Hermitian Positivstellensatz.
- Literature search: stabiliser states are known to be the worst case for Pauli/MUB uncertainty tasks, with magic states better (Howard, arXiv:1501.05319; Andersson et al., arXiv:1412.8181). No source found treats regulus subsets or this torus structure.
