# A mixed Z4 R-anomaly beyond universal E6 inflow

The [eight-hypermultiplet orbifold vacuum](2026-11-17_E6_two_corner_vacuum.md) uses $Z_4^R$ to retain one Higgs doublet pair and forbid the direct holomorphic dimension-five proton-decay contact. Its six-dimensional Green–Schwarz gauge and gravitational factorization test does not test this discrete symmetry on four-dimensional gauge backgrounds. On the common bulk Cartan there is an allowed background with zero normalized $E_6$ instanton number and a mixed $Z_4^R$ phase of minus one. Consequently a universal shift coupled only to the inherited bulk $E_6$ instanton class cannot cancel this anomaly. The fixed-point gauge subgroups supply additional characteristic classes that match it algebraically.

## Local index and an independent zero-mode check

Let $F/(2\pi)=h x+k y$ on spin $S^2\times S^2$, with $x,y$ the integral generators and $\int xy=1,\ x^2=y^2=0$. Take $h,k$ in the common compact $E_6$ Cartan cocharacter lattice. These fluxes extend over the internal orbifold with all toral twists commuting. This is a background test of the gauge theory before imposing nonzero Higgs profiles. The four-dimensional integrated gravitational Pontryagin number is zero.

For a fermion of $R$ charge $r$ and Cartan weight $q$, the exponent of its $Z_4^R$ phase is $r q(h)q(k)$ modulo four. The four-dimensional chirals of a hypermultiplet have fermion charges $-1,+1$, with opposite inversion parities. The gaugino and chiral adjoint carry $+1,-1$. The localized mixed gauge coefficient at a $T^2/\mathbb Z_2$ fixed point is one quarter of the parity-weighted trace, in the orbifold regulator convention:

$$
\mathcal A_f(h,k)=\frac14\left[\operatorname{tr}_{78}\big(P_f h k\big)
-E_f\operatorname{tr}_{27}\big(P_f h k\big)\right],\qquad
(E_{00},E_{10},E_{01},E_{11})=(0,-4,4,0).
$$

Each fundamental and dual hypermultiplet has the same contribution to the quadratic trace. The localized matter with superfield charge one has zero fermionic $R$ charge, and the neutral localized singlets have no mixed gauge index. The verifier constructs a saturated integral Cartan basis directly from the 45 cubic monomials, computes the 72 adjoint roots and parity signs from the cubic derivations, and independently checks that the sum of the local bilinears agrees with counting the actual projected zero modes. See [von Gersdorff and Quirós on orbifold-localized traces](https://arxiv.org/abs/hep-th/0305024) and [Lee et al. on the discrete MSSM anomaly convention](https://arxiv.org/abs/1009.0905).

## A global obstruction on an explicit allowed bundle

Choose $h=\operatorname{diag}(1,0,-1)$ in the left trinification $SU(3)$ and $k=\operatorname{diag}(1,0,-1)$ in the right trinification $SU(3)$. These commute and have integral charges in the faithful $27$. They have $\operatorname{tr}_{27}(hk)=0$. Write

$$
J(h,k)=\operatorname{tr}_{27}(hk)/6.
$$

This is the normalized $E_6$ instanton number on the flux background. The exact corner anomaly exponents are $(0,0,2,0)$ modulo four. The global phase is $-1$ even though $J=0$. This obstruction uses one globally defined background, so it is independent of how the local anomalies are redistributed between corners by counterterms. A universal Green–Schwarz inflow proportional to $J$ cannot remove it. The ordinary universal gravitational term also vanishes on this background.

## What simple-factor instantons miss

The local Lie algebras at $00,10,11$ have global form $(SU(6)\times SU(2))/\mathbb Z_2$. With instanton numbers $I_6,I_2$ normalized on the simply connected covering factors, the coefficients are $(0,-4)$, $(2,-10)$ and $(0,-4)$. In each pair the two entries agree modulo four. On the quotient, flux along

$$
h_6=\tfrac12\operatorname{diag}(1,1,1,-1,-1,-1),\qquad
h_2=\tfrac12\operatorname{diag}(1,-1)
$$

is allowed, since the two endpoint center elements are identified. Put $h_6,h_2$ on both spheres. Then $I_6=3/2,\ I_2=1/2$ and $J=I_6+I_2=2$. Every one of the three corner coefficients gives phase $-1$ on its corresponding local quotient background. The other corner contributions cancel that sign when these examples are extended with identical flux on both spheres across the orbifold. The orthogonal-flux example in the preceding section gives a separate nonzero integrated phase. These examples distinguish the failure of an inherited *local* class from the integrated anomaly.

## Quantized nonuniversal terms that match the tested anomaly

At an $SU(6)\times SU(2)$ corner define $C_f=4 I_2$, an integral first Pontryagin number up to sign for the three-dimensional adjoint bundle of the weak factor. At $01$ the group is $(\operatorname{Spin}(10)\times U(1)_\psi)/\mathbb Z_4$. The $1_4$ in the $27$ defines a genuine charge-four line bundle $L_4$ there. Use $C_{01}=\frac12\int c_1(L_4)^2$, an integer on spin four-manifolds. Its bilinear on the common flux lattice is the square of the character on the even neutral coordinate 8. The exact local forms are

| Fixed point | Local mixed gauge exponent before reduction mod four |
| --- | --- |
| $00$ | $-C_{00}$ |
| $10$ | $2J-3C_{10}$ |
| $01$ | $4J-10C_{01}$ |
| $11$ | $-C_{11}$ |

The verifier tests the $4^5$ coefficient vectors modulo four for $J$ and the four indicated local classes on the full common Cartan flux lattice. Within this set, every successful integrated match uses all four nonuniversal classes. One representative coefficient vector is $(2,3,1,2,3)$ in order $(J,C_{00},C_{10},C_{01},C_{11})$. Integer coefficients allow a periodic axion coupling at the level of these characteristic classes, with sign chosen opposite to the fermion phase. This gives a target for localized inflow. It leaves open the origin of the axion shift and localized interactions, the discrete gravitational and global anomaly conditions beyond the tested gauge backgrounds, and whether the required couplings descend from the 6D tensor multiplet or require a twisted sector.

Reproduce with `python analysis/toe_20261117_E6_fixed_point_R_anomaly.py`. The matching output is `data/toe_20261117_E6_fixed_point_R_anomaly.json`.
