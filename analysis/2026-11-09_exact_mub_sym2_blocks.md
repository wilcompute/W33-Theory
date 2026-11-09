# Nine identical 5D cyclotomic blocks for two-qutrit MUB certificates

**Date:** 2026-11-09. **Code:** analysis/w33_exact_mub_sym2_blocks_20261109.py. **Result:** data/w33_exact_mub_sym2_blocks_20261109.json. **Regression:** tests/test_w33_exact_mub_sym2_blocks_20261109.py. Everything is verified using signed integer pairs in Z[omega] with omega²+omega+1=0; no floating-point eigenvalues and no external Python packages.

## Ancestry: not a duplicated priority claim

Pass 12636 enumerated the 432 five-base, 135 eight-base and 36 ten-base maximal partial spreads of W(3,3). Pass 12638 showed positive numerical Hermitian-SOS lower bounds. **During this independent check, Pass 12639 was pushed by a parallel research track** and already proved the same strong-unextendibility bounds *exactly*, using cyclotomic certificates on representative pentads and group transitivity. Therefore the new theorem here is **the ninefold 5-dimensional decomposition and exhaustive 603-case independent integer replay**, not the first proof of strong unextendibility.

## Construction and exact reduction

Let L be a two-qutrit Pauli context, with nine simultaneous eigenvectors B_L, and let W(u) be the standard symmetrically phased Weyl operators. The same-outcome two-copy projection is

\[
D_L=\sum_{e\in B_L}|e,e\rangle\langle e,e|
=\frac19\sum_{u\in L}W(u)\otimes W(-u).
\]

The second factor is W(-u), not W(u); this ensures that each D_L is a Hermitian orthogonal projector. Define the quartic incompatibility witness for k selected contexts S by

\[
F_S(v)=\sum_{L\in S}\sum_{e\in B_L}
\bigl(|\langle e|v\rangle|^2-\|v\|^2/9\bigr)^2
=\langle v\otimes v,H_S(v\otimes v)\rangle,
\qquad H_S=\sum_{L\in S}D_L-\frac{k}{9}I.
\]

Every Weyl tensor W(u) ⊗ W(-u) preserves the **center-of-mass address** s=z+w in F3². For each fixed s there are exactly five unordered pairs {z,w}: one diagonal pair and four off-diagonal pairs. Thus Sym²(C⁹), dimension 45, splits into nine 5-dimensional sectors. Simultaneous translations of z and w commute with every D_L and transitively permute the sectors because 2 is invertible in F3. **All nine blocks are unitarily equivalent**, so exactly one 5×5 cyclotomic matrix suffices.

Set R_L=9 D_L restricted to the s=0 sector and R_S=sum R_L. The code uses an unnormalized symmetric-pair basis, which is similar to the orthonormal Hermitian representation and preserves its spectrum. It proves R_L²=9R_L and tr(R_L)=9 for every context; tr(R_L R_M)=9 for each of the 540 disjoint context pairs; and tr(R_L R_M R_N)=27 for all 4320 pentad triples.

## Exhaustive polynomial identities: every maximal configuration

| Bases | Number of configurations | Exact integer-matrix identity | Eigenvalues of R_S in 5D | Spectrum of H_S on Sym²(C⁹) |
|---:|---:|---|---|---|
| 5 | 432 | R_S² − 27 R_S + 126 I = 0; tr=45 | 6 (×4), 21 (×1) | 1/9 (×36), 16/9 (×9) |
| 8 | 135 | R_S² − 36 R_S + 288 I = 0; tr=72 | 12 (×4), 24 (×1) | 4/9 (×36), 16/9 (×9) |
| 10 | 36 | R_S = 18 I | 18 (×5) | 8/9 (×45) |

All equations are checked **entrywise in Z[omega]** against 603 independently enumerated maximal cliques of the disjointness graph; eigenvalues follow from the distinct integer roots, trace, and Hermiticity. Thus for *every* nonzero v in C⁹,

\[
\boxed{F_S(v)\ge\frac19\|v\|^4\quad(k=5),\qquad
F_S(v)\ge\frac49\|v\|^4\quad(k=8).}
\]

This provides an exact, all-vector Hermitian sum-of-squares re-verification of **strong**, not merely Pauli-class weak, unextendibility.

**Control and limitation.** Four contexts contribute at most four rank-one operators in any 5D sector, so the Gram operator has a negative eigenvalue -4/9 and cannot prove positivity. Removing any one context from a pentad also leaves an available fifth MUB context, giving 2160 explicit subset-extension checks. Negative eigenvalues on Sym² need not themselves correspond to an unbiased pure state; the extension observation is separate. The SOS lower bound 1/9 is **not** the exact minimum of the pure-state quartic (earlier numerical optimization found approximately 0.14711). No physical Hamiltonian, mass, photon circuit, or TOE is derived.

Prior art: Pass 12639 (analysis/PASS12639_EXACT_STRONG_UNEXTENDIBILITY.md); A. Szántó, *Complementary decompositions and unextendible mutually unbiased bases*, Linear Algebra Appl. 496 (2016), 392–406, doi:10.1016/j.laa.2016.02.010.
