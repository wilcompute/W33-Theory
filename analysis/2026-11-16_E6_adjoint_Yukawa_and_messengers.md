# Adjoint Yukawa separation and heavy-field matching for the \(E_6\) candidate

The [isolated Higgs-sector construction](2026-11-16_E6_isolated_SM_Higgs_vacuum.md) leaves one light doublet pair and one chiral \(\mathbf{10}+\overline{\mathbf5}\) per chosen matter \(\mathbf{27}\). Its basic down-type operator gives the usual \(SU(5)\) relation between down and charged-lepton Yukawas. Keeping the exact light-field projection, adjoint insertions lift that relation. Within the specified cubic-contraction family, two insertions are necessary for independent symmetric matrices and three are necessary for independent antisymmetric matrices. A separate heavy-field construction produces the chosen Higgs-stabilization operators at tree level. These are effective model-building results with chosen couplings. [Renormalizable \(E_6\) benchmark](https://arxiv.org/abs/1504.00904) · [\(E_6\) adjoint tensor products](https://arxiv.org/abs/hep-ph/0101349) · [GUT Yukawa Clebsch factors](https://arxiv.org/abs/0902.4644)

## Exact light-matter Clebsch factors

Let \(d\) denote the polarization of the cubic on the \(\mathbf{27}\), with dual form \(d^*\). The down doublet enters the cubic via \(D=d^*(\bar K,\bar H_1)\). The two matter slots of \(d(X_i,X_j,D)\) are ordered with the \(\mathbf{10}\) component first, so the aligned charged-lepton matrix has the \(e^c\) family index first and the \(L\) index second. One transposes this matrix in the convention with \(L\) first. The verifier constructs the original rank-ten matter mass from the cubic and selects the light coordinates before evaluating any insertion.

At \(\Phi=Y\), the integer weights on the two slots are \((x,y)=(-1,-2)\) for \(Q,d^c\), and \((-6,3)\) for \(e^c,L\). Every one of the six colored and two charged-lepton vertices has its respective pair. Strip the known component signs of the common cubic contractions. The product insertion \(d(\Phi X_i,\Phi X_j,D)\) is symmetric under family exchange and multiplies these vertices by \(xy\). The antisymmetric one-insertion term is the difference between inserting \(\Phi\) in the first or second matter slot. It gives \(x-y\), and the difference between the \((2,1)\) and \((1,2)\) insertions gives \(xy(x-y)\). Up-type \(Q,u^c\) has weights \((-1,4)\), so its single antisymmetric insertion gives \(-5\).

Consequently the independent symmetric and antisymmetric flavor inputs have the maps
\[
 \begin{pmatrix}S_d\\ S_e\end{pmatrix}
 =\begin{pmatrix}1&2\\1&-18\end{pmatrix}
   \begin{pmatrix}S_0\\S_2\end{pmatrix},\qquad
 \begin{pmatrix}A_d\\ A_e\end{pmatrix}
 =\begin{pmatrix}1&2\\-9&162\end{pmatrix}
   \begin{pmatrix}A_1\\A_3\end{pmatrix}.
\]
Their determinants are \(-20\) and \(180\), respectively. The normalization can absorb operator scales into the family tensors. The symmetric part of an up Yukawa comes from the original cubic and the antisymmetric part from the single insertion. Thus the map in this effective operator family spans all 27 complex entries of the three charged-fermion matrices for three chosen families. This proves freedom to fit them at tree level and removes the earlier tensor relation. It gives no flavor prediction, mass hierarchy or CKM fit by itself.

There is also a lower-order obstruction in this family. Both down-type weight pairs have \(x+y=-3\). Symmetric polynomials through degree one therefore evaluate in one common direction. Antisymmetric polynomials through degree two are \(x-y\) times a symmetric polynomial of degree at most one, again giving a single common direction. Insertions on the fixed neutral \(\bar H_1\) or on either fixed light Higgs weight supply no new direction within the same contraction. Other invariant contractions are outside this minimality statement.

## A renormalizable tree realization of these Yukawas

Introduce vectorlike \(\mathbf{27}+\overline{\mathbf{27}}\) messengers \(F_i,\bar F_i,G_i,\bar G_i,U,\bar U\). Their bilinear and cubic terms can be chosen as
\[
 \sum_i\bar F_i(MF_i-\Phi X_i)+\bar G_i(MG_i-\Phi F_i)
       +\bar U(MU-d^*(\bar K,\bar H_1)).
\]
The barred-field equations give \(F_i=\Phi X_i/M,\ G_i=\Phi^2X_i/M^2,\ U=D/M\) exactly in the tree superpotential. The cubic contractions \(d(X_i,X_j,U)\), \(d(F_i,X_j,U)\), \(d(F_i,F_j,U)\), and \(d(G_i,F_j,U)\) produce the four down terms above. Antisymmetric family matrices in the appropriate mixed terms implement their slot differences. The up terms use \(K\) in place of \(U\) with zero or one insertion. For diagonal family-universal messenger masses, the charged legs acquire positive family-universal kinetic factors at the fixed vacuum. They rescale each species' coupling and preserve the rank statements. The spectrum and running through the heavy thresholds have not been fitted.

## A separate tree realization of the Higgs stabilizer

Work in common mass units and let \(R,S,\bar R,\bar S\) be four independent chiral multiplets in \(\operatorname{End}(\mathbf{27})\) transforming by conjugation. This is a reducible \(E_6\) representation, with its full field content retained here. Take the trace-polynomial superpotential
\[
 \operatorname{Tr}\big[\bar R(R-\Phi^2)+\bar S(S-\Phi R)
           -\tfrac{283}{2}\Phi^2+\tfrac35 RS+\tfrac16 S^2\big]
       +\sum_a\bar H_a R H_a
       +\operatorname{tr}_2[L(G-\mathbf1)-\tfrac12 L^2].
\]
The entries of \(L\) are four independent gauge singlets and \(G_{ab}=\bar H_a H_b\). Every term is at most cubic in the enlarged elementary fields. The \(\bar R,\bar S,L\) equations give \(R=\Phi^2,\ S=\Phi^3,\ L=G-\mathbf1\). Eliminating the heavy fields reproduces the quadratic, fifth- and sixth-degree adjoint terms, the Higgs lock, and the squared Gram term exactly. The multiplier-to-field constraint map is triangular and invertible, so the full heavy Hessian is invertible as well. The heavy block contributes \(4\cdot729+4=2920\) to the rank, with the earlier reduced Higgs Hessian as its Schur complement. At the specified vacuum the heavy fields are diagonal Hermitian functions of \(Y\) and of the projector onto \(\ker Y\). Each endomorphism moment map vanishes and the original D-flatness is preserved. The expanded sector has the same gauge orbit and no new local Higgs flat directions.

This is an explicit tree-level realization, using a large messenger sector and the same chosen symmetry-breaking coefficients. It does not give a natural relation among those coefficients or imply ultraviolet completeness. In particular, perturbative running with this much charged matter is a separate constraint. The light doublet mass still uses the tuned relation in the [Higgs-sector model](2026-11-16_E6_isolated_SM_Higgs_vacuum.md), and none of the extra operators is derived from W33.

The [Yukawa map](../data/toe_20261116_E6_adjoint_Yukawa_maps.json) and [Higgs elimination](../data/toe_20261116_E6_Higgs_messenger_matching.json) certificates come from the adjacent Python producers.
