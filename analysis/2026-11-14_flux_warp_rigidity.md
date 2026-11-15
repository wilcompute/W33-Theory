# Warp rigidity for two flux-sphere metric ansätze

The [unwarped spin-two bound](2026-11-14_many_sphere_magnetic.md) motivates testing whether warping creates a branch with a larger gap. In smooth, source-free \(D=d+2N\) Einstein–Maxwell theory with no bare cosmological term, two natural enlargements of that ansatz still force an unwarped round product. Here \(d>2\), \(N\ge2\), every sphere has nonzero magnetic flux, and the external reference metric is Einstein. These are rigidity statements for the metrics and fluxes specified below. General warped spin-two spectra use a weighted internal operator. [De Luca and Tomasiello](https://arxiv.org/abs/2104.12773)

## Arbitrary direct-product internal metrics with aligned flux

Let the internal metric be \(\sum_i g_i(y_i)\), with each \(g_i\) any smooth metric on its sphere. Put \(F=\sum_i f_i(y_i)\operatorname{vol}_{g_i}\), and allow an arbitrary external warp \(e^{2A(y)}g_d\). Closure is automatic. The Maxwell equation on each block reads \(\partial_i(e^{dA}f_i)=0\). Each \(f_i\) has a definite nonzero sign, since a zero on its factor would propagate over that factor and give zero total flux. Therefore \(A=\mathrm{const}-d^{-1}\sum_i\log|f_i|\). The mixed internal Ricci and stress tensors of the base product vanish, leaving \(d_iA\otimes d_jA=0\) for \(i\ne j\) from the external warping contribution. Separability then allows dependence on at most one sphere.

If the warp depended on one sphere, the Einstein equation on any other sphere would equate its Gaussian curvature to \(f_j^2/2-\sum_i f_i^2/[2(D-2)]\). Dependence on the active coordinate can only enter through its \(f_i^2\), so that flux density must be constant. Maxwell now makes the warp constant as well. All flux densities are constant and each Gaussian curvature is constant, hence positive on \(S^2\) by Gauss–Bonnet.

## Common internal conformal deformation with fixed round volume forms

Now let the metric be \(e^{2A(y)}g_d+e^{2B(y)}\bar g\), where \(\bar g\) is a product of round spheres of inverse squared radii \(K_i>0\). Both \(A\) and \(B\) may depend on every internal coordinate. Put \(F=\sum_i f_i\operatorname{vol}_{\bar g_i}\) with fixed nonzero constants \(f_i\), and set \(n=2N\). Internal Hodge scaling in Maxwell's equation gives \(d(e^{dA+(n-4)B})\wedge\bar *F=0\). Contraction with the nondegenerate two-form \(F\) is injective, so \(A=aB+\mathrm{const}\), \(a=(4-n)/d\). Absorb the additive constant in \(g_d\). For \(n=4\), \(A\) is constant and the external Einstein equation directly forces \(e^{-4B}\) constant because the magnetic energy is nonzero.

For general \(n\), the non-scalar internal Ricci terms added to \(\operatorname{Ric}(\bar g)\) reduce to \(-2\bar\nabla^2 B+q\,dB\otimes dB\), with \(q=6-n-(n-4)^2/d\). This follows by combining the conformal Ricci tensor and \(-d(\nabla^2 A+dA\otimes dA)\) in the conformally deformed internal metric. For even \(n\ge4\) and integer \(d>2\), \(q\ne0\). With \(U=e^{-qB/2}>0\) the non-scalar correction becomes \((4/q)\bar\nabla^2 U/U\). The stress tensor is block diagonal and isotropic inside each sphere. The mixed Hessians thus vanish and the Hessian within each sphere is pure trace. It follows that \(U=U_0+\sum_i u_i(y_i)\), where each \(u_i\) has mean zero and \(\bar\nabla_i^2 u_i=-K_i u_i\bar g_i\). The latter identity follows by taking the divergence of the pure-trace Hessian equation and using constant sphere curvature. [Hessian reduction in warped product geometry](https://arxiv.org/abs/1110.2455)

Subtracting the internal Einstein equations for two unit directions of the reference metric in blocks \(i,j\) removes the common scalar terms. With \(X_i=f_i^2\), it gives

\[
(K_i-K_j)U-\frac4q(K_i u_i-K_j u_j)=\frac{X_i-X_j}{2}U^{1+4/q}.
\]

Suppose \(u_i\) varies and pick \(j\ne i\). If \(X_i=X_j\), averaging requires \(K_i=K_j\) since \(U_0>0\), and then variation in \(u_i\) contradicts the equation. Otherwise the left side is affine in \(u_i\) with other coordinates fixed, so the exponent must be zero or one. It cannot be one. The equation \(q=-4\) for exponent zero has the sole allowed solution \((d,n)=(8,8)\). Indeed \(q=2\) at \(n=4\), \(q=-4/d\) at \(n=6\), and \(q<-4\) for \(n\ge10\).

At \((8,8)\), \(U=e^{2B}\) and \(A=-\tfrac14\log U\). Write \(\operatorname{Ric}(g_d)=\lambda g_d\) and let \(\bar\Delta=\bar\nabla^i\bar\nabla_i\). The external Ricci equation becomes

\[
\lambda U^{5/2}+\tfrac14\bar\Delta U=-\frac{\sum_i X_i}{2(D-2)}.
\]

Holding all but the active coordinates in sphere \(i\) fixed, \(\bar\Delta U=-2\sum_j K_j u_j\) is affine in \(u_i\). If \(u_i\) varies, differentiation twice with respect to its value on its image interval forces \(\lambda=0\). Then the nonzero slope \(-2K_i\) in the Laplacian contradicts the constant right side. Hence \(U\), \(B\), and \(A\) are constant in the exceptional dimensions too.

Under either ansatz the earlier unwarped KK bound applies. A deformation that combines general flux redistribution with a non-product internal metric, adds sources, or changes the higher-dimensional equations lies outside the two proofs.

Replay the symbolic coefficient and exceptional-dimension checks with `py -3 analysis/toe_20261114_flux_warp_rigidity.py`.
