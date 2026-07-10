# Levi Duality-Defect and Characteristic-Two Incidence-Dirac Theorem

## Result

Let \(M\) be the \(40\times40\) point-line incidence matrix of the symplectic generalized quadrangle \(W(3,3)\), and set

\[
\mathcal D=\begin{pmatrix}0&M\\M^{T}&0\end{pmatrix},\qquad
\Gamma=\begin{pmatrix}I_{40}&0\\0&-I_{40}\end{pmatrix}.
\]

The new verifier proves four linked statements.

### 1. Spectral supersymmetry without geometric self-duality

Over characteristic zero,

\[
\Gamma\mathcal D+\mathcal D\Gamma=0,
\]

and

\[
\mathcal D^{2}=
\begin{pmatrix}
A_{W}+4I&0\\
0&A_{Q}+4I
\end{pmatrix},
\]

where \(A_W\) is the point-collinearity graph of \(W(3,3)\), while \(A_Q\) is the line-intersection graph, equivalently the point graph of the dual parabolic quadrangle \(Q(4,3)\).

Both halves have Gram spectrum

\[
16^{1}\oplus6^{24}\oplus0^{15},
\]

so

\[
\operatorname{spec}(\mathcal D)=
(-4)^{1}\oplus(-\sqrt6)^{24}\oplus0^{30}
\oplus(\sqrt6)^{24}\oplus4^{1}.
\]

There are \(15\) zero modes on each grade, hence Witten index zero.  But the two halves are not isomorphic:

\[
\alpha(W(3,3))=7,
\qquad
\alpha(Q(4,3))=10.
\]

Therefore the Levi carrier is **spectrally paired but geometrically non-swappable**.  Equal point and line counts do not imply a point-line duality.  A grading-reversing permutation automorphism would induce an isomorphism between the two halved graphs, so none exists.

This sharpens the architecture language: address and route are dual roles, but their type bit is intrinsic.  A physical mirror operation that exchanges them is extra middleware, not an internal automorphism of the \(q=3\) incidence geometry.

### 2. The odd-characteristic parity law

For the classical family \(W(3,q)\),

\[
MM^{T}=(q+1)I+A_W,
\qquad
M^{T}M=(q+1)I+A_Q.
\]

When \(q\) is odd, \(q+1\), \(q(q+1)\), \(q-1\), and \(q+1\) are all even.  Reducing the generalized-quadrangle strongly-regular relation modulo two therefore gives

\[
A_W^{2}=A_Q^{2}=0.
\]

Consequently

\[
\boxed{\mathcal D^{4}=0\quad\text{over }\mathbb F_2}
\]

for every odd \(q\).  This is the algebraic shadow of the same parity boundary at which \(W(3,q)\) ceases to be self-dual: the dual is \(Q(4,q)\), and the two are isomorphic exactly for even \(q\).

### 3. The exact \(q=3\) nilpotent packet

At \(q=3\), the nilpotency index is exactly four, not smaller.  The verifier obtains

\[
\operatorname{rank}_{2}(\mathcal D,\mathcal D^{2},\mathcal D^{3},\mathcal D^{4})
=(50,26,2,0),
\]

and hence

\[
\dim\ker(\mathcal D,\mathcal D^{2},\mathcal D^{3},\mathcal D^{4})
=(30,54,78,80).
\]

The Jordan type is

\[
\boxed{J_4^{\oplus2}\oplus J_3^{\oplus22}\oplus J_1^{\oplus6}}.
\]

The packet is exact substrate arithmetic:

\[
(50,26,2,0)=(5\Phi_4,2\Phi_3,\lambda,0),
\]

\[
(30,54,78,80)=(h(E_8),2q^3,\dim E_6,2v),
\]

and

\[
(2,22,6)=(\lambda,2(k-1),2q)
\]

for the nonzero Jordan-block multiplicities \((J_4,J_3,J_1)\).

These labels are exact arithmetic readings of the filtration.  They are not, by themselves, a continuum-physics derivation.

### 4. The missing explanation for the \(8+20=28\) W/Q glue split

In characteristic two the two Hamiltonian halves are themselves differentials:

\[
A_W=MM^{T},\qquad A_Q=M^{T}M,
\qquad A_W^2=A_Q^2=0.
\]

Their ranks and homologies are

\[
\operatorname{rank}_2 A_W=16,
\qquad
\dim H(A_W)=40-2(16)=8,
\]

\[
\operatorname{rank}_2 A_Q=10,
\qquad
\dim H(A_Q)=40-2(10)=20.
\]

Thus

\[
\boxed{8+20=28}.
\]

Earlier repo passes found exactly these two dimensions as the Construction-A discriminant-form ranks: \(O_8^+(2)=E_8/2E_8\) on the W side and \(O_{20}^+(2)\) on the Q side.  The present theorem explains their common origin: they are the two chiral homologies of one Levi incidence Dirac operator after characteristic-two collapse.

Moreover, \(M^T\) and \(M\) induce zero maps on these homologies.  The two sectors are coupled at chain level but remain separated after quotienting by boundaries.  This is an exact algebraic model of a type-protected address/route split.

## Why this was not already in the repository

The existing W/Q frontier established:

- cospectrality and local indistinguishability;
- the ovoid separator \(7\) versus \(10\);
- different critical groups;
- different binary code and lattice-glue ranks \(8\) versus \(20\).

The missing object was the common \(80\)-dimensional incidence operator that unifies all four facts.  The new result does not merely add another separator.  It explains why the same pair is isospectral over characteristic zero, why it is non-swappable geometrically, and why it separates into \(8\)- and \(20\)-dimensional homologies over characteristic two.

## Files

- `analysis/w33_levi_duality_defect.py` — self-contained verifier.
- `data/PART_2026_07_10_LEVI_DUALITY_DEFECT_results.json` — generated certificate.
- `tests/test_w33_levi_duality_defect.py` — regression tests.

## External geometry boundary

The classical finite-geometry fact used here is that the generalized quadrangle from \(Q(4,q)\) is the dual of \(W(3,q)\), and they are self-dual/isomorphic exactly when \(q\) is even.  For \(q=3\), the equal \(40+40\) cardinalities are therefore a balanced bipartition, not a duality automorphism.
