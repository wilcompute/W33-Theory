# Analytic magnetic energies that preserve the D9 static shape cancellation

The [quartic calculation](2026-11-14_d9_quartic_flux.md) showed that generic corrections spoil the static shape cancellation for an equal-angular-degree KK mass source. In the same Einstein-frame product ansatz with fixed magnetic charges and Einstein curvature, an entire nonlinear family preserves the cancellation. Let \(X,Y\) be the two squared orthonormal magnetic flux densities and \(T=X+Y\). Within magnetic energies analytic near \(X=Y=0\) with Maxwell leading term and no constant term, the restricted energies that preserve the stationary radius ratio for a finite interval of static source strengths across the weak-field charge branch are exactly

\[
W(X,Y)=T\,f(T^3XY),\qquad f(0)=1/2.
\]

The first allowed nonlinear term is \(\gamma T^4XY\), with twelve field strengths. The subsequent possible terms are separated by ten field strengths. This classifies the magnetic energy sampled by the two-block flux ansatz. It leaves derivative operators, curvature corrections, and covariant invariants that vanish on this ansatz undetermined. A finite interval of sources is used in the classification, so an accidental zero at a single source or charge ratio does not impose the same condition.

## Force equation and necessity

Write \(u\) for the common log-radius displacement and \(v\) for its half difference, as in the [quadratic Maxwell calculation](2026-11-14_d9_radion_response.md). At fixed \(v\), the curvature force has a constant shape-to-volume ratio \(3\delta/7\), where \(\delta\) is the difference of the two inverse squared radii divided by their sum. The source rescales the whole curvature term by \(k=1-Jn/2\) with common angular eigenvalue \(n=\ell(\ell+1)\). A stationary branch with constant \(v\) has varying \(u\), since the curvature has nonzero volume force and its coefficient varies with \(J\). Along such a ray in \(X,Y\), the analytic magnetic force must have the curvature force ratio on an open interval. Analyticity continues that identity to the weak-field limit in the connected weak-field domain. Its Maxwell term gives \(r=(5/7)\delta\), where \(r=(X-Y)/T\). This is the Maxwell stationary shape relation. Across the charge branch, \(r\) ranges over an open interval.

For a homogeneous term \(W_p=T^p h_p(r)\) the volume derivative of \(e^{-8u/3}W_p\) is \(-(4p+8/3)e^{-8u/3}W_p\). The shape derivative contributes the operator \(-4[X\partial_X-Y\partial_Y]\) on \(W_p\). Matching their ratio to \(3r/5\) at every common scale separates the Taylor degrees and gives

\[
(1-r^2)h_p'(r)=-\frac{2(p-1)}5 r h_p(r),\qquad h_p(r)=c_p(1-r^2)^{(p-1)/5}.
\]

A nonzero Taylor polynomial in \(X,Y\) requires the exponent to be a nonnegative integer \(m\). Thus \(p=5m+1\), and using \(1-r^2=4XY/T^2\) gives the stated family. Conversely every member has the required force ratio along the Maxwell shape ray. The remaining volume stationarity equation has a local solution near the Maxwell branch by its positive volume Hessian. For example with \(W=T/2+\gamma T^4XY\), in units with the unperturbed sum of inverse squared radii one, set \(R=e^{-2u}\), and denote \(P_0=(X+Y)^4XY\) at the unperturbed Maxwell vacuum. The exact source equation on the stationary shape ray is \(k=R+(20/7)\gamma P_0 R^{11}\). For \(\gamma\ge0\) it has a unique positive solution for every positive \(k\) in this polynomial model.

## Born–Infeld control

The Abelian determinant energy on two orthogonal magnetic blocks is \([\sqrt{(1+sX)(1+sY)}-1]/s\). Its first correction is \(-s(X-Y)^2/8\). Substituting into the earlier fixed-flux response gives \(\partial_J v/(ns)=4\delta(245-100\delta^2)/[120(21-5\delta^2)]+O(s)\) in the same units. It has the sign of \(\delta\) at leading order and is nonzero at every strictly asymmetric point. This uses the determinant gauge action as a control for the Einstein product ansatz. [Born–Infeld determinant action](https://arxiv.org/abs/hep-th/9908105)

The symbolic verifier independently builds the polynomial force matrices through degree 18 and checks the exact finite-source equation and the Born–Infeld expansion. Replay with `py -3 analysis/toe_20261114_d9_protected_magnetic.py`.
