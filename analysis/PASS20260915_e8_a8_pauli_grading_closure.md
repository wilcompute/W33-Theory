# Pass 2026-09-15 — classification closes the E8 A8 sector as the two-qutrit Pauli grading

## Theorem

Let `g=c^10` be the canonical fixed-point-free order-three element used by Pass 1021, and let

\[
V=E_8/(1-g)E_8\cong \mathbb F_3^4.
\]

For the order-three Lie-algebra lift whose fixed algebra is the Kac `A8` class, the fixed algebra

\[
\mathfrak a=\mathfrak e_8^g\cong\mathfrak{sl}_9(\mathbb C)
\]

carries a fine `V`-grading

\[
\mathfrak a=\bigoplus_{0\ne v\in V}\mathfrak a_v,
\qquad \dim\mathfrak a_v=1,
\qquad \mathfrak a_0=0,
\]

and this grading is equivalent, up to a symplectic relabeling of `V` and rescaling of the one-dimensional homogeneous generators, to the standard tensor-product two-qutrit Pauli grading of `sl(9,C)`.

Equivalently: the 80 E8 oriented-A2 orbit degrees are not merely in bijection with the 80 nonidentity two-qutrit Paulis. They are the homogeneous degrees of the same fine Lie grading, up to graded equivalence.

## Proof chain

### 1. The 80 one-dimensional pieces

Holotrade `68df33f` and its W33 ledger import identify the relevant order-three `E8` class as the unique class with 80-dimensional fixed algebra, hence type `A8 = sl9`. The twist fixes no Cartan direction and permutes the 240 roots in 80 free three-cycles. Each root three-cycle therefore contributes one fixed line and there is no fixed Cartan summand.

The exact weld `data/w33_e8_twisted_fibration_weld.json` identifies those 80 cycles with all nonzero vectors of

\[
V=E_8/(1-g)E_8\cong\mathbb F_3^4.
\]

The oriented-A2 refinement identifies each degree with the triangle `{r,gr,g^2r}`.

### 2. It is a V-grading

The support certificate `data/w33_e8_a8_pauli_support_bridge.json` checks all 3160 unordered pairs of distinct nonzero degrees. If the induced symplectic form satisfies `Omega(v,w)=0`, no root sum occurs. If `Omega(v,w)` is nonzero, exactly three root sums occur and all three lie in the unique root orbit labeled `v+w`.

Thus the fixed lines satisfy

\[
[\mathfrak a_v,\mathfrak a_w]\subseteq\mathfrak a_{v+w}.
\]

When `w=-v`, the only possible root brackets land in the Cartan; because the fixed Cartan is zero, the bracket of the fixed lines is zero, agreeing with the missing degree-zero component. Hence the decomposition is a genuine `V`-grading.

All 80 nonzero homogeneous components are one-dimensional, so the grading is fine.

### 3. Type II is impossible

For `sl(n)` with `n>=3`, Bahturin and Kochetov classify abelian group gradings into Type I and Type II. Their Type II grading has a distinguished element of order 2; quotienting by it gives a Type I grading. See arXiv:0908.0906, especially the discussion of Type I/II and Theorem 4.9.

Here the grading group is

\[
V\cong\mathbb Z_3^4,
\]

which has no element of order 2. Therefore this grading cannot be Type II. It is Type I.

Bahturin--Kochetov then imply that the `V`-grading on `sl9` is induced from a unique `V`-grading on the associative algebra

\[
M_9(\mathbb C).
\]

### 4. Restoring the identity gives 81 one-dimensional components

For every nonzero `v`, the matrix component restricts to the one-dimensional Lie component `a_v`. At degree zero, the Lie component is zero, so the matrix degree-zero component is exactly the scalar identity line. Therefore the induced grading of `M9` has

\[
81=9^2
\]

one-dimensional homogeneous components.

Bahturin--Kochetov show that a matrix grading with all homogeneous components of dimension at most one is a graded division algebra. Its support `T` has order `9^2=81`, and its graded-isomorphism class is determined by a nondegenerate alternating bicharacter

\[
\beta:T\times T\to\mathbb C^\times.
\]

For `T=Z_3^4`, a standard realization is a tensor product of two order-three Weyl/Pauli matrix algebras.

### 5. The bicharacter is the W33 symplectic form up to the only harmless equivalences

The exact root-support certificate shows that the zero set of the matrix commutator bicharacter is exactly the zero set of the W33/twisted-register symplectic form `Omega`: the same 1000 unordered nonparallel orthogonal pairs commute, while the 2160 remaining pairs do not.

Nondegenerate alternating forms on the four-dimensional vector space over `F3` are all symplectically equivalent. Replacing `Omega` by its nonzero scalar multiple merely exchanges the two primitive cube-root phases. Hence the induced matrix division grading is, up to symplectic relabeling, exactly the tensor two-qutrit Pauli grading.

Restricting back to traceless matrices gives the asserted graded equivalence on `sl9`.

## External literature boundary

The classification ingredients are published mathematics, not new claims of this repository:

- Y. Bahturin and M. Kochetov, *Classification of group gradings on simple Lie algebras of types A, B, C and D*, Journal of Algebra 324 (2010), 2971--2989, arXiv:0908.0906. Their matrix-algebra discussion shows one-dimensional matrix gradings are division gradings classified by a nondegenerate alternating bicharacter; their Type-A classification identifies Type-I Lie gradings as restrictions of matrix gradings.
- E. Pelantova, M. Svobodova and S. Tremblay, *Fine grading of sl(p^2,C) generated by tensor product of generalized Pauli matrices and its symmetries*, J. Math. Phys. 47 (2006), arXiv:quant-ph/0510106. They give the tensor-Pauli fine grading and its normalizer quotient `Sp(4,F_p) x C2`.
- The `A8=sl9` fixed algebra of the relevant order-three `E8` class is classical Kac theory; the repo's Holotrade certificate independently enumerates the fixed dimensions and identifies the unique 80-dimensional case.

## What is new here

The new corpus contribution is the chain that makes those classical results meet the exact W33/E8 quotient:

\[
E_8\text{ root three-cycles}
\;=\;
V\setminus\{0\}
\;=\;
\text{homogeneous degrees of the fine two-qutrit Pauli grading of }\mathfrak{sl}_9,
\]

with W33's symplectic form controlling exactly which homogeneous brackets vanish.

This closes the algebraic-structure gap stated historically in `tools/HONEST_ASSESSMENT.py`, **up to graded equivalence**. What remains noncanonical is a preferred phase/normalization of each one-dimensional generator, not the Lie algebra or its grading class.

## Scope

This is a mathematical identification of a finite Lie grading. It does not by itself establish the Standard Model, a continuum limit, coupling constants, masses, or experimental predictions.
