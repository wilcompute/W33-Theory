# A coupled Type IIB warp branch near the \(T^{p,q}\) quadrupole resonance

The [quantized resonance calculation](2026-11-16_Tpq_warp_resonance.md) excludes an exact infinitesimal warp about every integer-flux \(T^{p,q}\). Its scalar equation had a small finite-amplitude branch near irrational resonance, but with the internal metric frozen that branch failed the internal Einstein equation. Allowing the metric and five-form to respond gives a genuine local branch of the classical Type IIB field equations. It exists on the integer Chern bundles sufficiently close to the resonance and can preserve the Page period. The warped branch has the classical D3 probe discharge channel proved in the [arbitrary-shape calculation](2026-11-16_D3_arbitrary_shape_probe.md).

## Remove the linear metric source

Use \(e^{2A}g_{\mathrm{AdS}_5}+g_Y\), a constant axiodilaton, zero three-forms, and the self-dual five-form with electric coefficient \(f\) in the unwarped AdS volume form. The internal five-form is \(f e^{-5A}\,dV_{g_Y}\). Set \(L=1,\ f=4\) by the reference normalization and use
\[
g_Y=e^{-10A/3}h.
\]
In the external equation the Laplacian conformal term cancels the \(5|\nabla A|^2\) term. In the internal equation the conformal Ricci Hessian cancels the term \(-5\nabla^2 A\) from the external metric warp. The remaining system is
\[
 \Delta_h A=V'(A)/G,\qquad
 \operatorname{Ric}(h)=\frac G2\,dA\otimes dA +\frac{V(A)}{3}h,\qquad
 G=\frac{80}{3},\qquad V=20e^{-16A/3}-8e^{-40A/3}.
\]
These are the five-dimensional Riemannian Einstein–scalar equations with \(V(0)=12,\ V'(0)=0,\ V''(0)/G=-32\). Thus the correction to \(h\) begins at \(A^2\) whenever the metric operator is invertible in the chosen gauge and symmetry. The physical internal metric \(g_Y\) already changes at first order. [Type IIB warped equations](https://arxiv.org/abs/hep-th/0510125) · [Warped flux branches in a different compactification](https://arxiv.org/abs/1404.5979)

## Solve the metric equations on the circle bundle

Take the fields on the first sphere to be smooth, axisymmetric and even in \(x=\cos\theta_1\). With \(g_i\) the unperturbed sphere metrics, use \(h=e^{2D}g_1+e^{2B}g_2+e^{2C}\vartheta^2\), with the reference circle length absorbed into \(\vartheta\). Let \(d\vartheta=b_1(1+Z)dV_1+b_2dV_2\), with the oriented area forms of \(g_i\). At shape \(\eta\), use \(b_1^2=8\eta,\ b_2^2=8(1-\eta)\), and \(k_i\) as in the earlier spectrum calculation. The mixed horizontal-vertical Einstein equation is the connection equation \(d(e^{3C}*_B d\vartheta)=0\), where \(*_B\) uses the four-dimensional base. Keeping the first Chern integral fixed solves it exactly with
\[
 1+Z=\frac{e^{2D-2B-3C}}{\langle e^{2D-2B-3C}\rangle_1}.
\]
The correction two-form has zero integral and therefore changes the connection on the same circle bundle. The second Chern integral is fixed directly. [Ricci tensor of connection metrics](https://doi.org/10.1016/S0393-0440(03)00156-6)

Use the first-sphere trace, second-sphere component, and fiber component as the three metric equations. At resonance \(\eta=1/3\), linearizing them in \((D,B,C)\) gives the constant-mode determinant \(4096/9\). For positive harmonics of the first sphere, \(\lambda_\ell=k_1\ell(\ell+1)\), the matrix is
\[
\begin{pmatrix}
\lambda_\ell-2k_1 & \lambda_\ell+2b_1^2 & \lambda_\ell/2+2b_1^2\\
0 & \lambda_\ell-2k_2+2b_2^2 & -b_2^2\\
0 & -2(b_1^2+b_2^2) & \lambda_\ell-2b_1^2+b_2^2
\end{pmatrix}.
\]
Its determinant is \((\lambda_\ell-32/3)^2(\lambda_\ell+8)\). Only \(\ell=1\) can be singular, and that harmonic is odd. The triangular principal Laplacian symbol is invertible. These facts give the bounded elliptic inverse on even axisymmetric fields, for example between Hölder spaces with two derivatives of difference. The implicit function theorem solves these three metric equations for \((D,B,C)\) as smooth functions of \(A\) and the nearby shape, with \((D,B,C)=O(A^2)\).

After the scalar and these metric equations hold, the remaining Einstein residual is trace-free and confined to the first sphere. The contracted Bianchi identity gives zero divergence in \(h\), since the scalar equation supplies the stress conservation. For this horizontal tensor the divergence reduces to the first-sphere divergence with density \(e^{2B+C}\). Multiplying by that positive density gives a divergence-free trace-free tensor of the first-sphere metric. Such tensors are holomorphic quadratic differentials on \(S^2\), so the residual vanishes. The executable check also verifies this traceless equation directly at second order.

## Finite amplitude for nearby integer fluxes

In the even axisymmetric scalar sector at resonance the kernel is simple, spanned by \(P_2(x)\). All other scalar harmonics can be solved by the elliptic implicit function theorem. Write \(A=\epsilon P_2+O(\epsilon^2)\) with the remainder orthogonal to \(P_2\). Since the metric response in \(h\) starts at order \(\epsilon^2\), its effect on the scalar equation starts at third order. The scalar source has coefficient \(896/3\) at order \(A^2\), and \(\langle P_2^3\rangle/\langle P_2^2\rangle=2/7\). The remaining scalar equation is
\[
 0=(32-6k_1)\epsilon-\frac{256}{3}\epsilon^2+O(\epsilon^3).
\]
After dividing by \(\epsilon\), the derivative in \(\epsilon\) is nonzero at resonance. A local nonconstant solution therefore has
\[
 \epsilon=\frac3{256}(32-\lambda_{2,0})+O((32-\lambda_{2,0})^2).
\]
The irrational shape is used as the center of a common set of differential equations on the first sphere. Their coefficients depend smoothly on \(\eta\) and do not require a global circle bundle at the irrational parameter. At each nearby integer pair the connection above reconstructs a smooth metric on its own global bundle. The scale \(L\) is then fixed by the five-form Page period, which is proportional to \(4 L^4\int_Y e^{-5A}dV_{g_Y/L^2}\); this positive factor permits the same prescribed period as on the unwarped solution. Both primitive Pell sequences therefore produce small but nonzero warps on sufficiently late members, without taking an infinitesimal zero mode at any fixed integer pair.

For \((p,q)=(7,8)\) and \((8,9)\), the numerical quadrupole coefficients are \(0.00305721\) and \(-0.00179759\). They agree with the leading branch formula within \(1.3\%\). Moving from six to eight even Legendre harmonics changes each amplitude by less than \(2\times10^{-9}\). The sampled residuals of both the retained equations and the independently evaluated traceless equation at eight harmonics are below \(7\times10^{-15}\).

In this normalization the warped solution has \(A_{\min}<0\) and hence local probe ratio \(\alpha_* = e^{4A_{\min}}<1\). The prior probe theorem gives a round localized D3 at that minimum, with index one in the probe action. Along either primitive sequence \(A_{\min}\) is negative of order \(p^{-2}\), so the sphere radius in local AdS units grows as \(p\). The coupled branch is a classical solution and the discharge saddle is a probe. Its backreacted bounce and the warped background's own dynamical spectrum remain to be computed.

Reproduce the determinant, projected coefficient, quadratic metric response, and numerical examples at integer Chern pairs with `py -3 -B analysis/toe_20261116_Tpq_coupled_warp_branch.py`. The [JSON certificate](../data/toe_20261116_Tpq_coupled_warp_branch.json) includes the metric coefficients and harmonic truncation checks.
