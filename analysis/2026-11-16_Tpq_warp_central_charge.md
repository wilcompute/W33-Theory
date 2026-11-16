# Fixing the Page charge distinguishes the two sides of the warped \(T^{p,q}\) branch

The [coupled Type IIB solution](2026-11-16_Tpq_coupled_warp_branch.md) gives unwarped and warped backgrounds on the same circle bundle at the same five-form Page period. Their holographic Weyl anomalies first differ at cubic order in detuning. Allowing all five quadrupole harmonics also gives a local classification in the antipodally even circle-bundle ansatz. Every sufficiently small nonzero solution there is axial up to rotation. Its static quadrupole equation has both positive and negative directions after quotienting the rotations.

## Fixed Page charge and the cubic term

Use dimensionless internal metric \(g_Y=e^{-10A/3}h\) and put back the common length \(L\) in the ten-dimensional metric. The coefficient of the five-dimensional Einstein term is proportional to \(L^8 I_g\) when the reference AdS metric has unit radius, where \(I_g=\int e^{-16A/3}dV_h\). The Page period is proportional to \(4L^4 I_P\) with \(I_P=\int e^{-40A/3}dV_h\). These use the graviton weight \(e^{3A}\) and the magnetic five-form density \(e^{-5A}\), respectively, before the internal conformal change. At fixed Page period and fixed ten-dimensional Newton constant, \(a=c\propto I_g/I_P^2\) at the two-derivative order. Integrating the scalar equation for \(A\) gives \(I_g=I_P=I\) on any smooth solution in the sector. The exact central-charge ratio is therefore \(a_{\rm warp}/a_{\rm FR}=I_{\rm FR}/I_{\rm warp}\). [Henningson and Skenderis](https://arxiv.org/abs/hep-th/9806087) · [Warped AdS reduction and central charge](https://arxiv.org/abs/0906.4109)

Use the auxiliary Riemannian Einstein–scalar action \(S=\int [R(h)-(G/2)|dA|^2-V(A)]dV_h\) from the coupled equations, with \(G=80/3\). Its on-shell value is \(S=(2/3)\int V\,dV_h=8I\) by the Einstein trace and equality of the two integrals. This identity compares the physical normalization integrals without interpreting \(S\) as a Lorentzian effective potential. Put \(t=32-\lambda_{2,0}\), \(c_2=256/3\), and \(A=\epsilon P_2+O(\epsilon^2)\) at the same integer fluxes. The metric \(h\) first changes at order \(\epsilon^2\) and is stationary at the reference solution. The orthogonal scalar corrections can enter the action only at quartic order because the quadratic scalar operator is diagonal in harmonics. Using \(\int P_2^2/\operatorname{Vol}(Y)=1/5\) gives
\[
 \frac{S_{\rm warp}-S_{\rm FR}}{\operatorname{Vol}(Y_{\rm FR})}
  = \frac{G}{5}\left(\frac{t\epsilon^2}{2}-\frac{c_2\epsilon^3}{3}\right)+O(\epsilon^4).
\]
Along the branch \(\epsilon=t/c_2+O(t^2)\). Dividing by \(8\) to convert to the normalization integral and taking its reciprocal gives
\[
 \boxed{\ \frac{a_{\rm warp}-a_{\rm FR}}{a_{\rm FR}} =
    \frac{(\lambda_{2,0}-32)^3}{65536}+O((\lambda_{2,0}-32)^4)\ }.
\]
For \(\lambda_{2,0}<32\) the warped branch has the smaller central charge, and for \(\lambda_{2,0}>32\) the unwarped branch does. Along both Pell sequences the fractional separation scales as \(p^{-6}\). On the \(\lambda_{2,0}<32\) side the unwarped near-marginal operator is relevant, so the central-charge ordering is compatible with an RG trajectory from the unwarped point to the warped one in that sector. The ordering alone does not construct a domain wall. [Unwarped five-form and trace spectrum](https://arxiv.org/abs/hep-th/0108239)

| Chern pair | Numerical relative anomaly shift | Numerical / leading cubic |
| --- | ---: | ---: |
| \((7,8)\) | \(-2.75918\times10^{-7}\) | \(0.981954\) |
| \((8,9)\) | \(+5.44628\times10^{-8}\) | \(1.011235\) |
| \((38,43)\) | \(-1.79761\times10^{-12}\) | \(0.999708\) |

The verifier integrates both weights from the existing Legendre solver, with the exponential shift evaluated before integration to control cancellation. It computes the ratio at fixed Page period from the two separate integrals.

## Remove the axial restriction within the even ansatz

Keep the same connection-metric ansatz and allow \(A,D,B,C\) to be arbitrary antipodally even functions of the first sphere. The linearized metric operator depends only on the spherical harmonic eigenvalue, so the earlier invertibility proof still applies at every \(m\). The scalar kernel at resonance is now the entire real spin-two representation. Parametrize it as \(Y_Q(\widehat n)=\widehat n^{\mathsf T}Q\widehat n\) for traceless symmetric \(Q\). Solving the complementary equations by the equivariant implicit function theorem leaves a smooth \(SO(3)\)-equivariant map
\[
 F(Q,t)=tQ-2c_2(Q^2)_0+O(\|Q\|^3+|t|\|Q\|^2).
\]
Here the subscript removes the trace. The unique quadratic equivariant term is fixed by the axial result \(Q=\epsilon\operatorname{diag}(-1/2,-1/2,1)\), which gives \(F=(t-c_2\epsilon)Q\) at this order. The trace-free Einstein residual still vanishes by the weighted divergence argument on \(S^2\), which does not use axial symmetry.

For diagonal \(Q\) with eigenvalues \(r_i\), rotations that flip pairs of signs force \(F\) to be diagonal, with entries \(F_i\). Permutation covariance makes \(D_{ij}=(F_i-F_j)/(r_i-r_j)\) smooth, including at equality, by factoring an antisymmetric difference. Likewise \(D_{12}-D_{23}\) is divisible by \(r_1-r_3\) and its quotient is \(-2c_2+O(|t|+\|Q\|)\). If \(Q\) has three distinct eigenvalues and is a root, both divided differences vanish, contradicting the nonzero quotient. Thus every nearby nontrivial solution has a repeated eigenvalue. Its remaining fields inherit its axial symmetry by uniqueness of the complementary solutions. This proves local uniqueness up to rotation in the stated ansatz.

Linearizing the static projected equation on the nonzero branch gives \(-t+O(t^2)\) in the axial direction and \(3t+O(t^2)\) in each of the two biaxial directions. The other two directions are exactly neutral for the equation, since they move along the orbit of a rotated solution. The non-rotational derivatives have opposite signs on either side of resonance. These are derivatives of the static equation in the chosen variables, rather than a computation of the full ten-dimensional Lorentzian fluctuation operator. The known unwarped below-BF mode lies in another sector.

Reproduce the [JSON result](../data/toe_20261116_Tpq_warp_central_charge.json) with `py -3 -B analysis/toe_20261116_Tpq_warp_central_charge.py`.
