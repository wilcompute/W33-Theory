# Unextendible mutually unbiased bases of two qutrits: the complete Pauli-class picture

*Standalone note. Computations in `analysis/w33_pentad_umub.py`, `w33_size8_splits.py`, `w33_pentad_strong_umub.py` and `w33_split_triality.py`. Context: Passes 12634–12637 of this repository.*

## Setting

Two qutrits live in Hilbert space C⁹. A maximal commuting set of 8 two-qutrit Pauli operators X^a Z^b ⊗ X^c Z^d has a common eigenbasis, a stabiliser basis. The 40 such classes are the lines of the symplectic generalised quadrangle W(3,3). Two stabiliser bases are mutually unbiased (|⟨a|b⟩|² = 1/9) exactly when their classes share no operator, i.e. when the lines are disjoint; we checked this on all 780 pairs.

A set of Pauli-class MUBs is *weakly unextendible* if no further Pauli-class basis is unbiased to all of them (a maximal partial spread). It is *strongly unextendible* if no vector at all is unbiased to all of them (Mandayam, Bandyopadhyay, Grassl and Wootters, arXiv:1302.3709).

## Results

**1. The complete spectrum (exhaustive enumeration).** Weakly unextendible Pauli-class MUB sets in dimension 9 have exactly three sizes:

| number of bases | how many sets | structure |
|---:|---:|---|
| 10 (complete sets) | 36 | the spreads of W(3,3) |
| 8 | 135 | three per tensor factorisation (result 2) |
| 5 | 432 | two orbits of 216 under the Clifford group (result 4) |

There are no sets of size 7 or 9. Thas (arXiv:1407.2778) constructs sizes ℓ² − ℓ + 1 or ℓ² − ℓ + 2 for prime ℓ; at ℓ = 3 only the 8 occurs. A size-5 maximal partial spread of W₃(3) appears in arXiv:2105.05833.

**2. The size-8 sets are the entangled bases of a factorisation.** C⁹ has 45 tensor factorisations C³ ⊗ C³. For each one:
- 16 stabiliser bases are product bases;
- 24 are maximally entangled (flat Schmidt spectrum);
- **the 24 entangled bases split into exactly three weakly unextendible sets of 8 MUBs.**

These 3 × 45 = 135 sets are all the size-8 sets.

**3. Strong unextendibility (numerical).** Minimise Σ_e (|⟨e|v⟩|² − 1/9)² over unit vectors v ∈ C⁹, from many random starts:

| set | minimum |
|---|---:|
| 4 bases from a complete set (control; extendible) | ~10⁻¹⁷ |
| any 4 bases of a size-5 set | ~10⁻¹⁸ |
| **a size-5 set** | **0.14711** (3 sets × 200 starts, identical) |
| **a size-8 set** | **0.4444** (3 sets × 80 starts, identical) |

**No vector is unbiased to all bases of a size-5 or size-8 set, while every 4 of the 5 can be extended.**
- The size-5 sets appear to be **strongly unextendible MUB sets of 5 bases in dimension 9**.
- Szántó (arXiv:1502.05245) constructs strongly unextendible sets in dimension p², p ≡ 3 (mod 4), which for p = 3 have 8 bases. Our size-8 result agrees with that.
- I did not find a 5-basis strongly unextendible set in dimension 9 in the literature I could reach.
- **Theorem (exact; Pass 12639).** For every size-5 set, Σ_e(|⟨e|v⟩|² − |v|²/9)² ≥ |v|⁴/9 for all v ∈ C⁹. The certificate operator on Sym²(C⁹) satisfies Π(X − Π/9)(X − 16Π/9) = 0 exactly over Q(ω), and the Clifford group with its antiunitary coset carries one pentad to all 432. So **every size-5 set is strongly unextendible**. Size-8 sets satisfy F ≥ 4|v|⁴/9 exactly (tight), and their 16/9 eigenspace is the Λ²⊗Λ² of their own factorisation. The two-qubit size-3 sets are proved too (bound 1/4, tight); the three-qubit size-5 sets resist the Hermitian relaxation at degrees 4 and 6.

**4. Symmetry and chirality.**
- The 432 size-5 sets form one orbit under the extended Clifford group PGSp(4,3) and two orbits of 216 under PSp(4,3). The extended group adds the antiunitary coset.
- **Triality.** For each factorisation, the symmetries permuting its three entangled 8-MUB classes form S3. The even permutations come from unitary Clifford elements; the transpositions come only from the antiunitary coset (all 45 factorisations).

## Where this comes from

These sets are not arbitrary. Through the isomorphism W(E6) ≅ PGSp(4,3), they are pieces of the geometry of cubic surfaces:
- the 36 complete sets are the positive roots of E6;
- the 135 size-8 sets are the orthogonal root frames;
- the 432 size-5 sets are the 432 real regions of the moduli space of marked cubic surfaces. Each region is a positive geometry, the "E6 pezzotope" of Early, Geiger, Panizzut, Sturmfels and Yun (arXiv:2306.13604).

The 216 pairs of opposite chirality are related by a single Weyl reflection.
