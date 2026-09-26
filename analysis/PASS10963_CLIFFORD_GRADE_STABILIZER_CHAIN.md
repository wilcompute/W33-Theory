# Pass 10963 — Clifford-grade stabilizers recover the tetrahedral S4 -> S3 chain

Producer: `analysis/w33_pass10963_clifford_grade_stabilizer_chain.py`

Exact generator certificate: `analysis/w33_pass10963_exact_stabilizer_generators.py`

Independent GAP cross-check: `analysis/w33_pass10963_group_structure.g`

Certificates:

- `data/w33_pass10963_clifford_grade_stabilizer_chain.json`
- `data/w33_pass10963_exact_stabilizer_generators.json`

Pass 10961 supplied two operator packets on the doubled Albert carrier:

- \(V_{10}=\mathrm{span}\{\Gamma_1,\ldots,\Gamma_{10}\}\);
- \(P_{19}=V_{10}+\mathrm{span}\{\Gamma_{10}\Gamma_i:1\le i\le9\}\).
## 1. Exact stabilizers

Let

\[
g=\begin{pmatrix}0&1\\1&1\end{pmatrix},\qquad
b=\begin{pmatrix}1&0\\1&-1\end{pmatrix}
\]

over \(\mathbf F_3\). Direct multiplication gives

\[
g^8=b^2=1,\qquad bgb=g^3.
\]

Therefore

\[
\langle g,b\rangle\cong QD_{16}=SD_{16}.
\]

The index-two subgroup \(\langle g^2,b\rangle\) obeys the dihedral relation and is \(D_8\).
The independent exact \(\mathbb Q(i,\sqrt2)\) transport check proves that \(b\) preserves all 10 generators of \(V_{10}\) and all 19 generators of \(P_{19}\). Pass 10961 already proves that \(g^2\) preserves \(V_{10}\), while \(g\) preserves \(P_{19}\) but not \(V_{10}\). An order-three element outside \(\langle g,b\rangle\) preserves none of the packet generators.

GAP independently finds only one proper intermediate subgroup above this \(D_8\), namely the same \(QD_{16}\). Hence

\[
\operatorname{Stab}(V_{10})=D_8,
\qquad
\operatorname{Stab}(P_{19})=QD_{16}.
\]

Moreover,

\[
N_{GL(2,3)}(\langle g\rangle)=QD_{16},
\]

so the 19D packet stabilizer is exactly the normalizer of the clock \(C_8\).
## 2. Cores and quotient actions

The core of the vector-packet stabilizer is the center:

\[
\operatorname{core}_{G}(D_8)=\{\pm I\}\cong C_2.
\]

Thus

\[
GL(2,3)/\{\pm I\}\cong PGL(2,3)\cong S_4.
\]

The core of the 19D stabilizer is quaternionic:

\[
\operatorname{core}_{G}(QD_{16})\cong Q_8,
\]

with order census \(1^1\,2^1\,4^6\). Therefore

\[
GL(2,3)/Q_8\cong S_3.
\]

The two packet orbits consequently have sizes \(48/8=6\) and \(48/16=3\).
## 3. The packets are the six edges and three perfect matchings of a tetrahedron

The projective line \(PG(1,3)\) has four points. The exact \(GL(2,3)\) action on those four points has kernel \(\{\pm I\}\) and image \(S_4\).

The producer constructs an equivariant bijection

\[
\{6\ V_{10}\text{ packets}\}
\longleftrightarrow
\{6\text{ edges of }K_4\}.
\]

The three \(P_{19}\) packets are equivariantly identified with the three perfect matchings of \(K_4\), equivalently the three pairs of opposite tetrahedron edges.

Because \(D_8<QD_{16}\) with index two, each 19D packet contains exactly two vector packets, and those two packets are one opposite-edge pair.
## 4. Literal intersections and coupling ranks

The full numerical replay from exact committed matrices uses tolerance \(10^{-8}\).

For the six 10D packets:

- 12 adjacent-edge pairs have literal intersection dimension 0;
- 3 opposite-edge pairs have literal intersection dimension 1;
- the adjacent pairs have Hilbert–Schmidt cross-Gram rank 9;
- the opposite pairs have cross-Gram rank 1.

So adjacent packets are transverse but strongly coupled, while each opposite-edge pair shares one distinguished line.

For the three 19D packets:

\[
\dim(P_i\cap P_j)=8\qquad(i\ne j),
\]

and every pair has cross-Gram rank 9.
A further surprise is that the two complete packet orbits generate the same operator space:

\[
\operatorname{span}_{g\in G}(gV_{10}g^{-1})
=
\operatorname{span}_{g\in G}(gP_{19}g^{-1}),
\]

and the common dimension is

\[
33.
\]

Thus the six edge packets and the three perfect-matching packets are two different covers of one 33-dimensional \(GL(2,3)\)-stable Clifford-grade hull.

## 5. Clock meaning

Pass 10961 showed that odd ticks leave grade 1 and enter the mixed-bivector sector, whereas even ticks return to the Clifford-vector normalizer. Pass 10963 identifies the finite group behind that ladder:

\[
D_8=\operatorname{Stab}(V_{10})
<
QD_{16}=N(C_8)=\operatorname{Stab}(P_{19})
<
GL(2,3).
\]

The minimal packet closed under one clock tick is therefore the 19D packet, and its stabilizer is precisely the semidihedral clock normalizer.
## 6. Triality boundary

The quotient \(GL(2,3)/Q_8\cong S_3\) acts on the three 19D packets. That has the same permutation degree as \(D_4\) triality.

However, Pass 10955 showed that on the fixed \(D_4\) minuscule sets \(V,S_+,S_-\), the current signed-permutation realization sees only the determinant transposition \(S_+\leftrightarrow S_-\); it does not realize a triality 3-cycle.

So the packet \(S_3\) is an exact new three-object action, but not yet an identified \(D_4\) triality action. Constructing or obstructing an intertwiner between those two \(S_3\) structures is the next clean test.

## Boundary

The stabilizers, normalizer, cores, quotient groups, and tetrahedral coset dictionary are exact finite-group results. The packet intersection/cross-Gram dimensions are numerical replays of exact committed matrices with a large separation from the \(10^{-8}\) threshold.

No physical gauge group, spacetime tetrahedron, or Standard-Model triality is inferred.
