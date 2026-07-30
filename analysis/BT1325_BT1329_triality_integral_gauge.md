# Passes 1325–1329 — Triality Globalization, Integral Forms, and Cycle Nonselection

Status: **EXACT / machine-checkable**

## Pass 1325 — three-carrier triality globalization

Let `X` be one 432-dimensional coset carrier and `Y` the 480-dimensional directed-edge carrier.  The three conjugate coset carriers form

\[
X^{(3)}=X\otimes \mathbb C^3_{\rm perm},
\qquad
\mathbb C^3_{\rm perm}\cong\mathbf1\oplus\mathbf2
\]

under the commuting triality group `S3`.  If `H=End_G(X)` is the literal 26-dimensional Hecke algebra, then

\[
End_G(X^{(3)})\cong H\otimes M_3(\mathbb C),
\qquad \dim=234.
\]

The triality-fixed algebra is

\[
End_{G\times S_3}(X^{(3)})
\cong H\otimes(\mathbb C\oplus\mathbb C)
\cong H\oplus H,
\qquad \dim=52.
\]

Thus the globalization is a matrix amplification, not a literal wreath-product identification.

On the common support of `X^(3) ⊕ Y`, the unsymmetrized linking algebra is

\[
3M_4(\mathbb C)\oplus M_{10}(\mathbb C),
\qquad \dim=148.
\]

After imposing triality equivariance it becomes

\[
3\bigl(M_2(\mathbb C)\oplus\mathbb C\bigr)
\oplus M_4(\mathbb C)\oplus M_3(\mathbb C),
\qquad \boxed{\dim=40}.
\]

The full transport space has dimension 18 and decomposes as six copies of the permutation representation; its triality-invariant diagonal has dimension 6.

## Pass 1326 — integral and modular forms

For the six primitive orbital channel vectors, the coefficient matrix has

\[
\det C=3456=2^7 3^3
\]

and Smith form

\[
\boxed{\operatorname{SNF}(C)=\operatorname{diag}(1,1,1,12,12,24)}.
\]

It reduces from rank 6 to rank 3 in characteristics 2 and 3, while retaining rank 6 in characteristic 5.

Each of the 26 rational Hecke matrix units was independently cleared to a primitive integral column.  Their exact Smith diagonal is

\[
\boxed{
1^5,\;2^7,\;4,\;12^4,\;24^3,\;48,\;144,\;288,\;864,\;4320,\;34560
}.
\]

Equivalently, in ordered form:

```text
1,1,1,1,1,2,2,2,2,2,2,2,4,12,12,12,12,24,24,24,
48,144,288,864,4320,34560
```

The determinant is

\[
2^{57}3^{21}5^2.
\]

The primitive Hecke lattice has modular ranks

\[
\operatorname{rank}_{\mathbb F_2}=5,
\quad
\operatorname{rank}_{\mathbb F_3}=13,
\quad
\operatorname{rank}_{\mathbb F_5}=24,
\]

and full rank 26 at every other prime.  Thus the exact bad-prime set is

\[
\boxed{\{2,3,5\}}.
\]

## Pass 1327 — species-20 gauge geometry

The real commutant of the threefold species-20 isotypic component of the **432 carrier** is `M3(R)`.  The setwise normalizer of the three primitive diagonal idempotents is the monomial group.  Its orthogonal part is

\[
C_2^3\rtimes S_3=W(B_3),\qquad |W(B_3)|=48,
\]

with orientation-preserving subgroup of order 24, isomorphic to `S4`.  Modulo signs/phases, the actual copy-permutation quotient is `S3`.

Across the three triality carriers, the nine species-20 axes form a 3-by-3 gauge grid.  Coherent internal/triality permutations give `S3 × S3` of order 36; independent internal gauges give

\[
S_3\wr S_3=S_3^3\rtimes S_3,
\qquad |S_3\wr S_3|=1296.
\]

For the primitive integral normalization the three singular-scale ratios are `(2,3,2)`, whose elementary invariants are

\[
(e_1,e_2,e_3)=(7,16,12)
\]

and whose stabilizer is `C2`.  After partial-isometry normalization the Gram matrix is `I3`, restoring full `S3`; therefore the `2:3:2` asymmetry is an integral-coordinate effect, not dynamical copy selection.

This also corrects Pass 1305: that script did not execute AtlasRep and reversed the literal module multiplicities.  Multiplicity three occurs on the 432 carrier; the 480 carrier contains one species-20 copy.

## Pass 1328 — primitive-cycle transport obstruction

On the aligned six-channel Hom basis, right Hashimoto action is

\[
\operatorname{diag}(11,-1,-1,-1,-1,-1).
\]

Consequently the length-7 and length-8 powers act on the species-20 transport block as

\[
B^7|_{\mathbf{20}}=-I_3,
\qquad
B^8|_{\mathbf{20}}=+I_3.
\]

More generally, every `W(E6)`-averaged primitive-cycle operator is equivariant.  Because the directed-edge carrier contains species 20 with multiplicity one, Schur's lemma forces every such operator to be scalar on that copy.  Hence

\[
T_i C_n=\lambda_nT_i,
\qquad i=0,1,2,
\]

and no invariant length-7 or length-8 cycle operator can distinguish the three 432-side species-20 copies.  A single non-averaged cycle can select coordinates only by breaking the symmetry.

## Pass 1329 — independent reconstruction and scope corrections

The full result is checked twice:

1. a SymPy exact-matrix engine;
2. a standard-library-only engine using Bareiss determinant elimination and local Smith reduction over `Z/p^N Z`.

Both return the same 26-unit determinant and Smith diagonal.  A standalone GAP certificate containing both integer matrices is also checked in CI when GAP is available.

Two parallel claims are scope-corrected:

- Pass 1298 computes the tensor square of the rank-3 W33 scheme; it is not the literal 26-dimensional `W(E6)/S5` Hecke algebra.
- Pass 1305 is a generic `M3` coordinate calculation, not an AtlasRep execution, and assigns the multiplicity-three block to the wrong carrier.
