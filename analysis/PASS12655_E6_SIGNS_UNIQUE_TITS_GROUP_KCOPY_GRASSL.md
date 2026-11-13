# Pass 12655: the E6 sign pattern on the 45 triads is unique (one class in 2²⁴); its monomial symmetry group is a non-split 2⁶·W(E6); the k-copy hierarchy fails; our qubit minima confirm the Grassl–Kantor value

Claude track. Follows Pass 12654. **Not a theory of everything.**

## 1. The E6 signs are unique up to coordinate sign changes (`w33_e6_cubic_sign_uniqueness.py`)

For a sign pattern s ∈ {±1}⁴⁵ on the 45 tritangent triads of the 27 lines, put N_s = Σ s_t x_i x_j x_k and x# = ∇N_s. The adjoint (Jordan/Springer) identity **(x#)# = N(x)·x**, written coefficient by coefficient, has 2,295 non-trivial equations:
- 1,215 = 27·45 monomials receive exactly one term (a product of three signs must equal a fourth);
- 1,080 receive exactly two terms (two products must cancel);
- none receive more.

So the identity is an **affine linear system over F₂** in log s, with no non-linear equations.
- Its rank is 24, so the solution space has dimension 45 − 24 = **21**.
- The diagonal sign changes ε_iε_jε_k span exactly 21 dimensions.
- Hence **the solutions form a single orbit of coordinate sign changes: of the 2²⁴ sign classes, exactly one satisfies the adjoint identity.**

Controls:
- the repository's signs satisfy the system;
- the all-plus pattern does not (its stabiliser has dimension 6, Pass 12653);
- a random coboundary shift of the repository signs has a 78-dimensional stabiliser;
- a single sign flip violates the system and drops the stabiliser to dimension 30.

**Scope.** This is uniqueness among sign patterns satisfying the adjoint identity in the coordinate (Euclidean) identification of the 27 with its dual. The uniqueness of the E6 cubic is classical; what is recorded here is the explicit F₂-linear form and the count "1 of 2²⁴".

## 2. Monomial symmetry: a non-split 2⁶·W(E6) of order 3,317,760 (`w33_e6_cubic_integral_structure.py`, `w33_e6_cubic_weyl_splitting.py`)

- **Diagonal sign symmetries:** 2⁶ (the F₂-rank of the triad incidence matrix is 21 of 27). This is the 2-torsion of a maximal torus.
- **Every one of the 51,840 automorphisms of the triad hypergraph lifts** to a signed permutation preserving N. So the monomial group is M = 2⁶·W(E6), |M| = **3,317,760**.
- All 891 involutions of W(E6) (classes with 15, 7 and 3 fixed lines: 36 + 270 + 585) have lifts of order 2.
- **The extension does not split.** For an E6 Coxeter system of six reflections, each reflection has 32 involutive lifts. An exhaustive search over lifts finds **no** choice satisfying all the Coxeter relations (adjacent pairs: 64 compatible of 1,024; commuting pairs: 256).
- So W(E6) is **not** a subgroup of the signed permutations preserving the cubic. M has the shape of the Tits group (extended Weyl group) of E6, the integer points of the torus normaliser in E6(6)(ℤ). The identification with the Tits group is by order and non-splitting only; no isomorphism was constructed.
- Literature: Adams–He, *Lifting of elements of Weyl groups* (arXiv:1608.00510) study exactly this extension; the E6 statement was not read in the primary source.

**Reading.** The repository's signs are not decoration. They carry the 2-cocycle of the Tits extension, and W(3,3)'s group W(E6) ≅ Sp(4,3)·2 acts on the signed cubic only through this non-split cover.

## 3. Charge ranks (same script)

For integer vectors with entries in {0, ±1} and support ≤ 3 (rank 1: x# = 0; rank 2: N = 0, x# ≠ 0; rank 3: N ≠ 0):

| support | pattern | rank | N | count |
|---|---|---|---|---|
| 1 | — | 1 | 0 | 54 |
| 2 | skew pair | 1 | 0 | 864 |
| 2 | meeting pair | 2 | 0 | 540 |
| 3 | pairwise skew | 1 | 0 | 5,760 |
| 3 | 1 or 2 meeting pairs | 2 | 0 | 17,280 |
| 3 | a triad | 3 | ±1 | 180 + 180 |

- Rank 1 ⇔ the support is pairwise skew, independent of signs.
- The unit-norm vectors of support 3 are exactly the 45 triads.
- In the 5D N = 8 dictionary (Ferrara–Günaydin, hep-th/9708025) these are ½-, ¼- and ⅛-BPS charge vectors. The 45 triads are the minimal "entropy-carrying" charge configurations, and the other track's 72 + 216 coordinate sections are the maximal coordinate subspaces of rank-1 vectors (cocliques of the meeting graph).
- This is a dictionary, not a derivation of black-hole physics.

## 4. The k-copy symmetric-extension hierarchy fails in practice (`w33_kcopy_symmetric_bound.py`)

B_k = λ_max of Q₁₂ on Sym^k(C^d) bounds Σ_U from above (B₂ is the swap bound).

| set | truth | B₂ | B₃ | B₄ | B₅ |
|---|---|---|---|---|---|
| three-qubit five-set | 6 | 12 | 8.3148 | 8.3148 | 7.4275 |
| four-qubit type A | 14.162 | 20 | 20 | | |
| four-qubit type B | 14 | 20 | 17.333 | | |
| five-qubit 9-set | 30 | 40 | 39.041 | | |

Purity controls are exact. Convergence is far too slow: at five qubits the third level removes less than one unit of a gap of 10. **Negative**: this is the fifth relaxation that cannot certify 1/32, after ϑ, swap, the self-dual LP and conditioning.

## 5. Literature: our minima confirm the Grassl–Kantor value (Kantor, arXiv:1601.04194, read in full text)

- Kantor's Table 1 (Theorems 5.2, 6.2): maximal symplectic partial spreads of size **q^k + 1 in dimensions 4k and 4k − 2**, q even. For q = 2 this gives 5 (dims 6, 8), 9 (dims 10, 12), 17 (dims 14, 16). This is the repository's 2^⌈n/2⌉ + 1.
- **Grassl's conjecture** (n even): the smallest size is q^{n/2} + 1. Kantor: false when 2n = 8 for q = 2^{2e+1} > 2 (Suzuki–Tits ovoids), "plausible … if 2n > 8".
- **What the repository adds for q = 2:**
  - the value is the exact **minimum** in dimension 6 (5; Pass 12643);
  - in dimension 8 (5; Pass 12648), so Grassl's conjecture **holds** for Sp(8,2);
  - in dimension 10 (9; Pass 12654, exhaustive, one implementation, cross-check pending).
- Dimension 12 (six qubits): 9 is attained (Grassl; Pass 12651), and minimality is open.
- The elementary covering bound gives only size ≥ 4 for every n = 3…6 (`w33_rank_code_covering_bound.py`), so it cannot help.

## Open

- An explicit isomorphism M ≅ Tits group of E6, and the cocycle in W(3,3) terms.
- Six qubits: is 9 minimal? Exhaustive search is out of reach as built.
- The exact 1/32 and 1/16 (type B).
- Θ(W(3,3)) ∈ [√58, 10]: symmetric-code search in progress (addendum).

## Addendum A: the M-theory and IIB sections, and T² ↔ S¹, in the 27 lines (`w33_sections_levi_overlap.py`)

The other track found 72 six-coordinate and 216 five-coordinate maximal null sections (`toe_20261113_albert_six_coordinate_sections.py`); these are the maximal cocliques of the 27-line meeting graph. Two predictions were made before computing, and both hold.

**Levi types.**
- Each family is a single W(E6)-orbit.
- Stabiliser orders are **720 = |W(A₅)|** for sixers and **240 = |W(A₄ × A₁)|** for fivers.
- These are the Weyl groups of GL(6) and GL(5) × SL(2), the Levi subgroups of the M-theory and type IIB solutions of the E6(6) section constraint (Hohm–Samtleben, arXiv:1312.0614).
- So the 72 sixers correspond to the 72 roots of E6, and the 216 fivers to the 216 A₄ × A₁ subsystems.

**Overlaps.**
- A sixer and a fiver share 0, 1, 2 or **4** coordinates, never 3 or 5.
- Each sixer shares 4 coordinates with exactly **15 = C(6,4)** fivers: every 4-subset of a sixer lies in exactly one fiver.
- Each fiver shares 4 coordinates with exactly **5** sixers: every 4-subset of a fiver lies in exactly one sixer.

**Reading.** This is the combinatorial form of "M-theory on T² ↔ IIB on S¹". Choosing a T⁴ inside the M-theory T⁶ (15 ways) determines a unique IIB section, and choosing a T⁴ inside the IIB T⁵ (5 ways) determines a unique M-theory lift.

**Scope.** These are counts on coordinate sections of the repository's cubic, matching the known exceptional-field-theory structure. No field theory is constructed.

**Ownership.** The four-coordinate overlap statement was committed first by the other track (a4593c961, `2026-11-13_e6_tits_coordinates.md`); this addendum was computed independently and agrees. Cite theirs.
