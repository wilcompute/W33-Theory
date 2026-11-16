# Arbitrary-shape D3 probe obstruction and the warped threshold

The [round smeared calculation](2026-11-16_D3_spherical_discharge.md) excludes finite-radius classical discharge in a backreacted truncation. Its scope leaves open localized branes and nonspherical embeddings. In a fixed Type IIB Freund–Rubin background \(H^5_L\times Y\), a separate first-variation argument excludes every smooth compact D3 probe with nonconstant external projection at charge-normalized tension. The worldvolume can bend into \(Y\) and carry real Abelian gauge flux. This tests localization and shape in the probe limit. It applies to the [\(T^{p,q}\) dual](2026-11-16_D9_iib_conifold_dual.md) with all the circle topologies and spin lifts considered there.

For comparison, the probe isoperimetric inequality concerns the value of area minus flux volume. A positive value alone is compatible with a positive-action stationary bounce. The variation below supplies a strict sign for an admissible deformation at each externally extended compact probe. The warped criterion is the finite-radius counterpart, within this class of backgrounds, of testing the brane-jet force at each internal position. [Seiberg and Witten](https://arxiv.org/abs/hep-th/9903224) · [Ferrari and Rovai](https://arxiv.org/abs/1411.1887) · [Bena, Pilch and Warner](https://arxiv.org/abs/2003.02851)

## First variation with internal tilt and Abelian flux

Use Einstein-frame metric \(e^{2A(y)}g_{H^5_L}+g_Y\) with compact \(Y\), smooth warp \(A\), constant axiodilaton, vanishing three-form field strengths, and the usual real electric coefficient of the analytically continued D3 Wess–Zumino term. Write the external five-form as \(f\,dV_{H^5_L}\) with \(f>0\), measured with the unwarped metric. The five-form has a purely internal component as well. The Bianchi identity gives constant \(f\) in this source-free background. Take the orientation for discharge and write \(q>0\) for its charge. Use the leading-derivative action \(T\int \sqrt{\det(h+\mathcal F)}-q\int C_4\), with induced metric \(h\) and the real, dilaton-rescaled gauge-invariant two-form \(\mathcal F\). Hold the worldvolume gauge field fixed under the deformation. The external variation of the pullback of the background two-forms is gauge-trivial because the three-form field strengths vanish. Any constant axion coupling is topological under this variation. [D-brane effective action](https://arxiv.org/abs/hep-th/9812095) · [Wess–Zumino terms](https://arxiv.org/abs/hep-th/9604119)

Choose any hyperbolic center and let \(r\) be the unwarped distance to it. The vector \(X=\sinh(r/L)\partial_r\) is smooth at the center and has \(\mathcal L_X g_{H^5_L}=2\cosh(r/L)g_{H^5_L}/L\). Flow the embedding by \(X\), keeping its internal position fixed. Since the worldvolume is compact, \(X\) can be cut off away from its image. In a tangent \(h\)-orthonormal frame let \(P\) be the external Gram matrix computed with the warped metric, \(F\) the skew matrix of \(\mathcal F\), \(w=\sqrt{\det(1+F)}\), and \(M=(1-F^2)^{-1}\). Thus \(0\le P\le 1\), and \(P=0\) means the external projection has zero differential. The symmetric inverse of \(1+F\) is \(M\). The DBI density varies by
\[
\frac{T}{L}\cosh(r/L)\,w\,\operatorname{tr}(MP)\,dV_h .
\]
The flux density can reduce this by at most \(q f e^{-4A}\sinh(r/L)\sqrt{\det P}\,dV_h\). This bound is the norm of the projected tangent four-vector times the radial contraction of the external volume form. The purely internal five-form has zero contraction with \(X\). The factor \(e^{-4A}\) converts the four projected tangents to the unwarped metric. The Wess–Zumino variation uses the field strength directly, so the argument also applies with patchwise potentials.

The determinant identity \(\det(1-F^2)=w^4\) and arithmetic–geometric mean applied to \(M^{1/2}PM^{1/2}\) give
\[
w\,\operatorname{tr}(MP)\ge 4\sqrt{\det P}.
\]
The trace is strictly positive whenever \(P\ne0\), including at deficient rank where the projected flux contribution vanishes. Consequently, if \(T\ge q f L e^{-4A(y)}/4\) everywhere, the full variation is bounded below by
\[
\delta_X I\ge
\frac{T}{L}\int_\Sigma e^{-r/L}w\,\operatorname{tr}(MP)\,dV_h.
\]
This is strictly positive for a nonconstant external projection on any connected component. In the unwarped repo solution \(A=0,\ f=4/L\), the physical tension is \(T=q\). The argument excludes round or nonspherical smooth compact probe saddles at that tension, and also excludes evasion by real worldvolume flux of arbitrary pointwise amplitude within the DBI approximation. Branes whose projection is a point lie outside the externally extended channel.

## A sharp probe threshold and its spectrum

If \(T<q f L e^{-4A_{\min}}/4\), pick a global minimum \(y_*\) of \(A\). Set \(A_*=A(y_*)\) and \(\alpha_*=4T e^{4A_*}/(q f L)<1\). An unfluxed geodesic sphere in the external space at constant \(y_*\) is stationary at
\[
\tanh(r_s/L)=\alpha_* .
\]
Indeed the DBI tension in unwarped external units is \(T e^{4A_*}\) and the electric pressure is \(qf\). The linear internal variation vanishes at \(y_*\), and pulling back the internal five-form in that variation gives zero. Neither the gauge field nor mixed embedding variations change the stationarity conditions at \(F=0\). These facts give necessity and sufficiency for the **existence of a smooth compact externally extended probe saddle** under the stated conditions for the warped metric and flux. They make no assertion that such warp data solve Type IIB by themselves.

The proper sphere radius is \(a=e^{A_*}L\sinh(r_s/L)\). With \(L_*=e^{A_*}L\), the radial normal Hessian is the constant-mean-curvature Jacobi form with potential \(-|{\rm II}|^2-\operatorname{Ric}(n,n)=-4/a^2\), since \(|{\rm II}|^2=4\coth^2(r_s/L)/L_*^2\) and \(\operatorname{Ric}(n,n)=-4/L_*^2\) in the \(H^5\) slice. The eigenvalues with respect to the proper sphere measure are \(T[\ell(\ell+3)-4]/a^2\). The \(\ell=0\) mode is negative, the five \(\ell=1\) modes move the center, and all \(\ell\ge2\) modes are positive. The internal scalar quadratic form is \(T\int_\Sigma (|\nabla\delta y|^2+4\nabla^2 A(\delta y,\delta y))\,dV_h\), nonnegative at the minimum, with no quadratic mixing with the radial mode. The external electric term has no internal derivative and the purely internal \(C_4\) term starts at fourth order in an expansion about a constant internal map. The Maxwell quadratic form from DBI is nonnegative. The sphere therefore has exactly one negative direction in this bosonic probe action. Its radius law \(1-\alpha_*\sim L_*^2/(2a^2)\) has the same leading coefficient as the repo's smeared spherical branch. The [backreacted radial index](2026-11-16_D3_radial_negative_mode.md) and this full probe index refer to different variational problems.

## The pure-five-form Einstein equation forces threshold crossing under warping

For a source-free two-derivative Type IIB solution in this class, the external Ricci equation in an orthonormal frame reads
\[
-\frac{4e^{-2A}}{L^2}-\Delta_Y A-5|\nabla A|^2=-\frac{f^2}{4}e^{-10A}.
\]
Here the flux coefficient comes from contracting the Lorentzian electric five-form in the Einstein equation before continuing the probe problem to Euclidean signature. On compact \(Y\) without boundary, integrate the equivalent equation for \(e^{5A}\). [Warped Type IIB field equations](https://arxiv.org/abs/hep-th/0510125)
\[
\left(\frac{fL}{4}\right)^2 =
\frac{\int_Y e^{3A}\,dV_Y}{\int_Y e^{-5A}\,dV_Y}
=\frac{\int_Y e^{8A} e^{-5A}\,dV_Y}{\int_Y e^{-5A}\,dV_Y}.
\]
For nonconstant \(A\) the right-hand side is strictly between its minimum and maximum values of \(e^{8A}\). Thus \(e^{4A_{\min}}< fL/4\) and physical D3 tension \(T=q\) satisfies the strict sphere criterion at the minimum. If \(A\) is constant, the relation gives threshold equality and the first-variation obstruction applies. This links the external Einstein equation to the probe threshold without having to classify the internal metrics. Source terms, higher derivatives, or additional field strengths change the integral argument.

### The equal-flux conifold has a gap against small warps

Normalize \(fL/4=1\) by a constant shift of \(A\) and a rescaling of the reference \(H^5_L\) metric. Then \(u=e^{5A}\) satisfies \(L^2\Delta_Y u=20(u^{-1}-u^{3/5})\). A first-order warp about \(u=1\) requires a scalar eigenvalue \(32\) of \(-L^2\Delta_Y\). Metric changes leave the first-order equation unchanged because every Laplacian annihilates a constant.

On equal-flux \(T^{1,1}\) the scalar eigenvalues are \(6[j(j+1)+k(k+1)-m^2/8]\), with \(m\) the integer fiber charge and \(j,k\) each in \(|m|/2+\mathbb Z_{\ge0}\). The formula also follows by combining the [repo's monopole connection-Laplacian calculation](toe_20261116_D9_charged_monopole_harmonics.py) on each sphere with the vertical eigenvalue \(9m^2/4\). All eigenvalues are integer multiples of \(3/4\), which excludes \(32\). The exact distance to the spectrum is \(4\): spins above 2 give eigenvalues at least \(105/2\), and the finite set with spins at most 2 has \(36\) as the nearest level, attained by the neutral \((j,k)=(2,0)\) mode. Every fiber quotient retains that mode and can only remove scalar levels. [Ceresole, Dall'Agata and D'Auria](https://arxiv.org/abs/hep-th/9907216)

There is also a local nonlinear implication. The operator \(L^2\Delta_Y+32\) has an \(L^2\) inverse bounded by the reciprocal of its spectral gap. For metrics sufficiently close to any fixed equal-flux quotient metric after rescaling into AdS units, the gap remains positive by continuity of eigenvalues. The remainder in its equation for \(u-1\) is pointwise \(O((u-1)^2)\), so a nonzero solution cannot have arbitrarily small sup norm in that neighborhood. This excludes nearby smooth pure-five-form warped vacua on the same quotient, independently of the internal Einstein equation. A calculation of possible large warps or changes in other fields remains separate.

The strict variation approaches zero relative to the local DBI strain as the probe goes far out in AdS. Thus this fixed-background proof provides no uniform gap for brane self-backreaction or string corrections near the planar limit. It also leaves the perturbative \(T^{p,q}\) and winding instabilities in place.

Reproduce the symbolic Born–Infeld and sphere checks and the numerical rank-by-rank tilted flux controls with `py -3 -B analysis/toe_20261116_D3_arbitrary_shape_probe.py`. The [JSON certificate](../data/toe_20261116_D3_arbitrary_shape_probe.json) records the first seven spherical harmonic levels and the matrix bounds over 1,280 sampled configurations. The analytic trace inequality covers the full stated domain.
