# Static shape preservation and the spin-two gap on products of flux spheres

Take the Einstein action with an algebraic Abelian gauge energy on an unwarped product of \(N\ge2\) two-spheres and a maximally symmetric external space of dimension \(d>2\), with no bare cosmological term. Each sphere carries fixed magnetic charge. Let \(A_i=R_i^{-2}\) and let \(X_i\) be the squared orthonormal magnetic fields. Write \(S=\sum_i A_i\), \(T=\sum_i X_i\), and \(H=d-2+N\). Normalize the magnetic energy to have leading term \(T/2\). The many-sphere Einstein–Maxwell compactification itself is established. This calculation extends the repo's [D9 finite-source classification](2026-11-14_d9_protected_magnetic.md) to all \(d,N\) in this setting. [Brown and Dahlen](https://arxiv.org/abs/1310.6360) · [Brown, Dahlen and Masoumi](https://arxiv.org/abs/1401.7321)

## Analytic magnetic terms that preserve every radius ratio

The equal-angular-eigenvalue KK source multiplies the curvature term by \(k=1-Jn/2\), with \(n=\ell(\ell+1)\). For log-radii displaced by \(u+v_i\), where \(\sum_i v_i=0\), the Einstein-frame factor is \(e^{-cu}\) with \(c=4N/(d-2)\). At fixed shape the curvature varies as \(-2S e^{-(c+2)u}\), and a homogeneous magnetic term \(W_p\) of degree \(p\) in the \(X_i\) varies as \(e^{-(c+4p)u}\). These powers agree with the earlier [radial reduction](2026-11-14_general_flux_curvature_radius_classifier.md).

Stationarity with all radius ratios fixed over an open interval of \(J\) forces the curvature and magnetic gradients to have the same shape-to-volume ratios at every common scale in that interval. The Maxwell term fixes the ratios by analytic continuation to weak field. Each remaining Taylor degree must obey the same ratios because its common scaling power is different. With \(r_i=X_i/T\), this gives the pairwise equations

\[
(X_i\partial_i-X_j\partial_j)W_p=a(r_i-r_j)W_p,
\qquad a=\frac{4p+c}{4+c}.
\]

The Maxwell branch samples an open set of positive normalized fields: given any positive \(A_i\) use \(X_i=2A_i+2S/H\) and choose charges proportional to \(\sqrt{X_i}/A_i\). Continuous charge ratios give the open set directly, and ratios of quantized charges can approximate them at weak field by common scaling. Euler homogeneity now fixes the individual equations as \(X_i\partial_i W_p=[a r_i+(p-a)/N]W_p\). Dividing by \(T^a(\prod_i X_i)^{(p-a)/N}\) yields zero derivatives of the quotient on the positive cone. Thus the nonzero polynomial solution is proportional to that monomial. The power \((p-a)/N=(p-1)/H\) must be a nonnegative integer, by the order of vanishing when one \(X_i\) tends to zero. The full analytic magnetic family on this ansatz is therefore

\[
W=T f\!\left(T^{d-2}\prod_{i=1}^{N}X_i\right),\qquad f(0)=\tfrac12.
\]

Conversely this family aligns all the forces on the Maxwell shape ray. The positive Maxwell volume Hessian supplies a nearby stationary point for weak fields and sources in a neighborhood of zero. The first nonlinear term is \(F^{2(d+N-1)}\), giving \(F^{10}\) at \((d,N)=(4,2)\) and \(F^{12}\) at either \((4,3)\) or \((5,2)\).

The [two-polarization cone obstruction](2026-11-14_d9_protected_photon_cones.md) applies with the other \(N-2\) blocks held fixed. The restricted energy depends on the active pair through its sum and product. The first nonlinear term has a strictly positive second derivative polynomial in one squared block field and a strictly positive derivative with respect to the pair product, each multiplied by the same leading coefficient. At sufficiently weak generic fields the two tested squared speeds shift in opposite directions. Extra fixed magnetic planes therefore leave the obstruction intact for the algebraic action.

## A bound on the first spin-two KK mass at every Maxwell charge ratio

Stationarity of \(e^{-4\sum_i\beta_i/(d-2)}\sum_i(-2A_i e^{-2\beta_i}+X_i e^{-4\beta_i}/2)\) fixes \(X_i=2A_i+2S/H\) and the vacuum potential \(V_* = -(d-2)S/H\). The homogeneous log-radius Hessian is the sum of \(\mathrm{diag}[8(X_i-A_i)]\) and the positive semidefinite rank-one term \(-16V_*\mathbf 1\mathbf 1^T/(d-2)^2\). In particular every positive-radius Maxwell vacuum is a strict local minimum in these radius directions.

In the convention \(X_i=Q_i^2 A_i^2\), any nonzero fixed charges \(Q_i\) give a unique such radius solution. Put \(C=2S/H\). The positive root of \(Q_i^2 A_i^2=2A_i+C\) obeys \(A_i/C=[\sqrt{1+Q_i^2 C}-1]^{-1}\). The equation \(\sum_i A_i/C=H/2\) then has exactly one solution because its left-hand side decreases strictly from infinity to zero for \(C>0\). An overall charge rescaling \(Q_i\mapsto tQ_i\) sends \(C\mapsto C/t^2\) and leaves the radius ratios and the dimensionless gap invariant.

The Einstein-frame external AdS radius satisfies \(L^2=(d-1)H/S\). For the external transverse-traceless tower the first positive mass squared is \(2\min_i A_i\), obtained by exciting angular degree one on a single sphere. Consequently

\[
m_{\rm first}^2 L^2=\frac{2(d-1)(d-2+N)\min_i A_i}{\sum_i A_i}
\ \le\ \frac{2(d-1)(d-2+N)}{N}\ \le\ d(d-1).
\]

The first inequality is saturated at equal radii. At fixed external dimension, varying charges or adding spheres cannot generate parametric separation of the first spin-two mass from the AdS scale on this Maxwell branch. The bound concerns the Maxwell background and the spin-two tower. The nonlinear selection rule concerns static mass-source response within the fixed product ansatz.

Replay with `py -3 analysis/toe_20261114_many_sphere_magnetic.py`.
