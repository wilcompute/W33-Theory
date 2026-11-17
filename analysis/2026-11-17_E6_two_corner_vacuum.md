# A two-frame supersymmetric vacuum on the E6 orbifold

The [four-hypermultiplet spectrum](2026-11-17_E6_two_protected_corners.md) supplies $H_2=e_8$ but leaves $H_1=e_7$ as an external frame insertion. Two more conjugate pairs of bulk hypermultiplets give an explicit vacuum with both frames. In the zero-mode theory, the exact mass calculation leaves one physical Higgs doublet pair and lifts all other chiral fields in the Higgs and gauge sector. The matter coupling needed to lift the family exotics also produces an independent colored-scalar proton-decay amplitude.

## Dynamical frames and their superpotential

Keep the two protected corners and the second Wilson line of the earlier solution. Use four pairs of bulk hypermultiplets in $27+\overline{27}$. In each pair, call the two $R=0$ chirals $H,\bar H$ and their respective $R=2$ partners $H^c,\bar H^c$. The partner has opposite inversion sign and the same translation signs. The fields $A,B$ supply the two frames. $K$ carries the Yukawa source, and $L$ supplies a second doublet of each hypercharge before the boundary masses.

| Pair | Intrinsic signs $(\eta,\eta_x,\eta_y)$ | $R=0$ coordinates | $R=2$ partner coordinates |
| --- | --- | --- | --- |
| $A,\bar A$ | $(+,+,-)$ | 7, 12, 13, 14 | 0, 3 |
| $B,\bar B$ | $(+,-,+)$ | 8, 15, 16, 17 | 18, 19, 21, 22, 24, 25 |
| $K,\bar K$ | $(-,+,-)$ | 0, 3 | 7, 12, 13, 14 |
| $L,\bar L$ | $(-,+,-)$ | 0, 3 | 7, 12, 13, 14 |

Write the cubic polarizations as $d$ and $d^*$, the canonical pairing as a dot, and set the two VEV magnitudes and nonzero coupling coefficients to one in the verifier. Powers of the effective theory cutoff are implicit. The localized superpotential at the first protected fixed point has these terms and their indicated conjugate-representation terms. The bars on chiral field names denote independent chiral fields in dual representations.

- Pair $L$ with $A^c$ and $\bar L$ with $\bar A^c$ using direct invariant bilinears.
- Couple $K^c$ to $d^*(\bar A,d(A,A))$ and $L^c$ to $d^*(\bar A,d(B,B))$. Include the dual terms for $\bar K^c,\bar L^c$. These terms give the two triplet mass matrices.
- Impose the two norm constraints with $(K^c\cdot A)(A\cdot\bar A-1)$ and $(\bar K^c\cdot\bar A)(B\cdot\bar B-1)$. Pair the remaining neutral partners using two localized $R=0$ singlets $s,t$ with $s(L^c\cdot A)+t(\bar L^c\cdot\bar A)$.
- Include the bulk gauge superpotential with $H^c\Sigma H-\bar H^c\Sigma^T\bar H$ for each pair. Its zero-mode contribution follows from the 12 chiral-adjoint generators of the signed orbifold.

These localized terms are restrictions of $E_6$-invariant contractions and have superpotential charge two. At the vacuum, only $A,\bar A$ along coordinate 7 and $B,\bar B$ along coordinate 8 are nonzero. The same-row rank-one vectors have $d(A,A)=d(B,B)=0$ and the fixed norms are satisfied. The first derivatives of the boundary superpotential therefore vanish also before projecting onto the zero modes. Constant profiles respect both translations. The bulk moment maps cancel pointwise between an aligned field and its dual, with vanishing gauge connection and chiral adjoint. The two frame charges have rank two on the 14 vector zero modes, leaving the 12 Standard Model generators.

The exact holomorphic mass block has 32 rows of $R=2$ chiral components and 38 columns of $R=0$ chiral components. Its rank is 32, including rank four on the uneaten neutral mass block. Two of the six null directions are gauge-orbit directions, and the remaining four components form the doublets $K_{0,3}$ and $\bar K_{0,3}$. All nonzero ranks persist in an open neighborhood of the chosen couplings. The light doublets can rotate into $L,\bar L$ under allowed boundary masses, with nonzero overlap with the original sourced doublets near the displayed point.

This establishes the classical flat profiles and the zero-mode mass calculation for a chosen brane superpotential. A regulated codimension-two brane theory, the Kaluza–Klein mass corrections, realistic flavor fits, and the localized discrete and gravitational anomaly conditions remain to be matched. For comparison with an independent four-dimensional construction, see [Bajc and Susič](https://arxiv.org/abs/1311.0775).

The shape of the gauge breaking here is imposed by the toral boundary actions. The frame sector then uses mixed fundamental invariants to break the two remaining Cartans. This is compatible with the parallel obstruction to an independent quartic shape term in the single E6 adjoint. [Parallel adjoint calculation](https://github.com/wilcompute/W33-Theory/commit/e01f774b5)

## A scalar exchange that survives the original vertex selection

With the local family coupling $W_X=\lambda\,d(X,X,A)$, the $A$ VEV lifts the family exotics through the same rank-ten Hessian used in the earlier matter calculation. Its heavy scalar at coordinate 12 also couples to the light $QL$ slots $(1,18)$ and the light $U^cD^c$ slots $(10,17)$, each with tensor coefficient $-1$. The scalar propagator between a vertex and its conjugate generates a dimension-six operator with $|\Delta B|=1$. In the displayed zero-mode normalization the triplet mass block is $2I_3$. With canonical kinetic terms and unit $\lambda$, the coefficient magnitude in this tensor convention is $1/4$. This is a tree matching coefficient in the chosen units. Flavor rotations, physical mass scales, running, contact terms, and the normal-derivative gauge exchange are separate inputs.

An explicit deformation of the family coupling cancels this particular linear triplet source while preserving the same matter Hessian. Replace the vector $A$ only in $W_X$ by

$$
A-\frac{1}{2v_1^2}d^*(\bar A,d(A,A)).
$$

The cubic correction vanishes at the vacuum. Its linearization on the fluctuation of $A$ is the projector $I-h_1^2$ in the unit convention, where $h_1=d(e_7,\cdot)$ in dual coordinates. The verifier checks that it fixes the frame and annihilates the three triplet directions at 12, 13, and 14. The variation with respect to $\bar A$ vanishes at the frame. This is a change of an independent brane coupling with kinetic terms held fixed. The coefficient relation is a tuning and wider protection requires a symmetry or matching calculation.

## The eight-hypermultiplet anomaly lattice

With eight charged fundamentals on the covering space and one tensor multiplet, the same trace equations give $a\cdot b=-4$, $b^2=+2$ and 106 neutral hypers in the gravitational count. In the even unimodular plane $U$, the vectors are $a=(-2,-2)$ and $b=(1,1)$. On $\mathbb F_2$, this switches from the negative section of the four-hyper candidate to the positive section class $s+2f$. The split $IV^*$ data on this section have leading degrees $10,16$ for $f_3,g_4$. The square root of $g_4$ has degree eight, as expected for eight fundamental matter points in a generic split tuning. This identifies compatible bulk divisor and anomaly data. The pullback of the two Wilson lines, all fixed-point degrees of freedom, and their inflow still need a common ultraviolet construction. [Six-dimensional anomaly lattices](https://arxiv.org/abs/1008.1062) · [Split E6 tuning](https://doi.org/10.1007/s00220-023-04860-0)

Reproduce with `python analysis/toe_20261117_E6_two_corner_vacuum.py`. Its output is saved in `data/toe_20261117_E6_two_corner_vacuum.json`.
