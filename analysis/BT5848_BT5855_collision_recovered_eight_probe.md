# Passes 5848–5855 — collision-recovered matrix normalizer/code/Pauli/all-field closure

This is the clean-namespace publication of an exact eight-probe packet first staged under Pass5832–5839 after this lane had reserved that range. An unrelated parallel theorem packet subsequently landed under the same numbers, so the active publication is moved here. **The namespace changed; the finite computations did not.** The corrected runner imports the original exact routines and replays them before freezing the Pass5848–5855 certificate.

## Pass 5848 — the full degree-16 normalizer has order 1152

Let

\[
G=M_2(\mathbf F_2)_+\rtimes(GL_2(2)\times GL_2(2)),\qquad |G|=576,
\]

act on the 16 matrices by \(M\mapsto AMB^{-1}+X\). Exhausting all 20,160 elements of \(GL_4(2)\) gives a 72-element linear normalizer and trivial linear centralizer. Matrix transpose is in the normalizer but not the 36-element left/right subgroup.

The regular translation subgroup \(T\cong C_2^4\) is \(O_2(G)\), because \(G/T\cong S_3\times S_3\) has trivial 2-core. Hence \(T\) is characteristic and every \(S_{16}\)-normalizer of \(G\) lies in \(N_{S_{16}}(T)=AGL(4,2)\). Therefore

\[
\boxed{|N_{S_{16}}(G)|=1152},\qquad
\boxed{N_{S_{16}}(G)/G\cong C_2},
\]

with transpose representing the nontrivial coset.

## Pass 5849 — the Reye code’s minimum words are exactly the heavy shell

For the 12-point carrier \(P=\{(w,x):w\ne0\}\) and the 16 Reye lines \(L_M=\{(w,Mw):w\ne0\}\), exhaustive binary replay gives

\[
C_{\rm Reye}=[12,4,6],\qquad W(z)=1+12z^6+3z^8.
\]

The twelve weight-6 words are exactly the twelve heavy supports

\[
c_{\phi,\psi}(w,x)=\phi(x)+\psi(w),\qquad \phi\ne0,
\]

and the three weight-8 words are the \(\phi=0,\psi\ne0\) fiber-pair words.

This lands directly on the integral Smith data. The saturated \(R^T\) map has

\[
\operatorname{SNF}(R^T)=1^5\,2^2\,4^2,
\]

so it has four even invariant factors and 2-adic cokernel valuation 6. The saturated heavy transform instead has \(1^2\,2^5\,4^2\), seven even factors and valuation 9. The characteristic-two collapses are therefore different and must remain coefficient-ring explicit.

The local 12-coordinate code is not identified with the global q=5 binary CSS point-code family merely because both have distance 6.

## Pass 5850 — the Fourier rank 9+6 and the published two-qubit 9+6 are objectwise isometric

Saniga–Planat–Pracna’s two-qubit projective-ring construction supplies a 15-point Pauli geometry and a published \(9+6\) split. In binary Pauli coordinates \(v=(x_1,z_1,x_2,z_2)\), that split is the zero/one partition of

\[
q_{\rm SPP}(v)=x_1z_1+x_2z_2+x_2.
\]

For our nonzero dual Fourier labels

\[
Y=\begin{pmatrix}a&b\\c&d\end{pmatrix},
\qquad q_M(Y)=\det Y=ad+bc,
\]

the \(9+6\) split is rank-one versus invertible. Exhausting \(GL_4(2)\) finds exactly **72** linear isometries \(L\) satisfying

\[
q_{\rm SPP}(L(Y))=\det Y
\]

for every matrix label. One explicit choice sends the matrix-coordinate basis \((a,b,c,d)\) to

\[
(XI,\ IZ,\ IY,\ ZI).
\]

It maps the nine nonzero rank-one labels exactly onto \(C_7,\ldots,C_{15}\), the six units exactly onto \(C_1,\ldots,C_6\), and preserves all 105 polarized symplectic pairings. The rank-one 3×3 grid becomes

\[
\begin{pmatrix}
C_{10}&C_{13}&C_7\\
C_{12}&C_{15}&C_9\\
C_{11}&C_{14}&C_8
\end{pmatrix},
\]

with every row and column a commuting triple.

The scope is precise: this is an isomorphism of the **nonzero dual Fourier-label quadratic/symplectic geometry** with the two-qubit Pauli-point geometry. It is not an identification of q=5 cover points with physical qubit states or observables, and this certificate does not assert Mermin operator-product signs.

## Pass 5851 — an all-finite-field matrix Fourier/Radon theorem

Let \(R[(w,x),M]=1\) iff \(x=Mw\), with \(0\ne w\in\mathbb F_r^2\) and \(M\in M_2(\mathbb F_r)\). Additive Fourier characters of the matrix torsor split by dual matrix rank with dimensions

\[
N_0=1,\qquad N_1=(r-1)(r+1)^2,\qquad N_2=r(r-1)^2(r+1)=|GL_2(r)|.
\]

The incidence map has the exact decomposition

\[
\boxed{\operatorname{im}R^T=\mathbf1\oplus\mathcal F_{\rm rank\,1}},
\qquad
\boxed{\ker R=\mathcal F_{\rm rank\,2}},
\]

hence

\[
\boxed{\operatorname{rank}R=1+(r-1)(r+1)^2}.
\]

The nonzero squared singular values are \(r^2(r^2-1)\) on the constant mode and \(r^2(r-1)\) on rank one. The line–hyperplane disjointness relation is

\[
D[M,(\phi,\psi)]=1\iff \psi=-\phi M.
\]

At \(r=2\), every rank-one label has a unique nonzero factorization \(Y=\phi^Tw^T\). For \(r>2\), each has \(r-1\) factorizations, giving an extra point-side kernel of dimension

\[
(r-2)(r-1)(r+1)^2.
\]

Complete Fourier character-sum replays at \(r=2,3,5,7\) match the formulas exactly; prime powers follow using a nontrivial additive character composed with the field trace.

## Pass 5852 — publication closure

The publication contract names `docs/index.html` as the public index. The four preceding matrix cards existed as sources but were not registered in the local public-section contract. Pass5852 registers Passes 5776–5855 and adds a resilient materializer that treats `docs/index.html` and root `index.html` independently, rejects duplicate IDs, and removes the stale collision card if an already-queued legacy workflow ever writes it.

The shared manuscript frontier is corrected to include this Pass5848–5855 insert and exclude the contaminated Pass5832–5839 matrix insert, while preserving the independently landed Pass5840–5847 matrix/doily addendum.

## Pass 5853 — outside-box probe 1: determinant is a self-dual bent chirp

For

\[
f(Y)=(-1)^{\det Y}
\]

on additive \(M_2(\mathbb F_2)\), the Walsh transform obeys the exact pointwise identity

\[
\boxed{\widehat f(Z)=4f(Z)}.
\]

Thus determinant is a self-dual bent quadratic. The Walsh values are \(+4\) ten times and \(-4\) six times, packaging the \(10=(1+9)\) singular versus 6-unit split into one Fourier eigenfunction.

## Pass 5854 — outside-box probe 2: the order-1152 symmetry is the unit-difference rook graph

On the 16 matrices, define

\[
M\sim N\iff M-N\text{ is invertible}.
\]

Exact enumeration gives

\[
\operatorname{SRG}(16,6,2,2).
\]

There are eight \(K_4\)'s and exactly two partitions into four disjoint \(K_4\)'s, yielding intrinsic row/column coordinates. Therefore the graph is the \(4\times4\) rook/lattice graph \(L_2(4)\), not the Shrikhande graph. Its full automorphism group is

\[
\boxed{S_4\wr C_2},\qquad |\operatorname{Aut}|=1152,
\]

and the resulting 1,152 permutations are exactly the affine normalizer from Pass5848. This resolves the repo’s earlier unexplained \(S_4\wr C_2\) appearance: its source is the six unit-difference directions, not the Delsarte graph of the Reye two-weight code.

## Pass 5855 — outside-box probe 3: the Reye code is a projective-line puncture of simplex

Take the binary simplex \([15,4,8]\) code on the 15 nonzero points of \(PG(3,2)\). In coordinates \((w,x)\in\mathbb F_2^2\oplus\mathbb F_2^2\), delete the projective line

\[
\ell_0=\{(0,x):x\ne0\}.
\]

Restricting all simplex words to the remaining 12 points gives exactly the Reye kernel:

\[
\boxed{C_{\rm Reye}=\operatorname{puncture}_{\ell_0}(\mathrm{Simplex}[15,4,8])}.
\]

For \(\phi\ne0\), the deleted line contains exactly two ones, so simplex weight 8 drops to 6; these are the twelve heavy words. For \(\phi=0,\psi\ne0\), the deleted line is zero and the three words remain weight 8. This proves \(1+12z^6+3z^8\) conceptually.

## Reproduction

```bash
python3 analysis/w33_pass5848_5855_collision_recovered_eight_probe.py
python3 -m pytest -q tests/test_w33_pass5848_5855_collision_recovered_eight_probe.py
```

External prior art used for the two-qubit comparison: M. Saniga, M. Planat, P. Pracna, *Projective Ring Line Encompassing Two-Qubits*, arXiv:quant-ph/0611063.

## Boundary

All promoted results are finite algebra, coding theory, integral Smith theory, Fourier analysis, graph theory, or publication plumbing. The two-qubit bridge lives on nonzero dual Fourier labels; it does not supply a q=5 physical-state embedding, dynamics, particle assignment, mass/coupling law, continuum limit, or experimental prediction.
