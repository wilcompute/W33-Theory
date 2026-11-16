# Least-action primitive M5 probe on the warped \(T^{p,q}\) lift

The [eleven-dimensional lift](2026-11-16_Tpq_warp_mtheory_lift.md) has a closed two-form electric pressure for unfluxed M5 wraps. In the primitive torus homology class, a torus at the warp minimum has exactly the smallest effective tension and the smallest round probe-bounce action. Its exponent grows as \(N_0p^3\) on either Pell sequence, with different coefficients on the two sides. Torus-dependent radial fluctuations admit a separate momentum cutoff.

## Effective pressure and the minimal tension

Write the eleven-dimensional metric as \(e^{2W}g_{H^5}+g_6\), where \(g_{H^5}\) is unit radius and \(\rho=e^{C-5A/3}\), \(e^W=e^A\rho^{1/3}\). Continue the magnetic four-form background from Lorentzian signature with the electric pressure sign for discharge. Because \(G_4\) is internal, \(G_4\wedge G_4=0\); the dual field strength is the external volume form times the closed two-form \(\gamma=e^{5W}*_6G_4\). For a compact oriented surface \(\Sigma\), an unfluxed M5 of shape \(S^4_\chi\times\Sigma\) has effective tension \(T=T_5\int_\Sigma e^{4W}dV_\Sigma\) and pressure \(P=T_5\int_\Sigma\gamma\) in reference AdS units. The four-form pulls back to zero for this product embedding. The calculation uses the zero-three-form sector of the M5 worldvolume theory with compatible flat background data. [M5 worldvolume action](https://arxiv.org/abs/1308.2231) · [Wrapped M5 discharge in AdS5](https://arxiv.org/abs/2610.08939)

The pointwise normalized pressure form \(\gamma/(4e^{4W})\) has three skew blocks along the two sphere planes and the torus plane. The torus coefficient in a local orthonormal frame is \(e^{-4A}\). The sphere-plane coefficients, up to orientation, are \((b_i/4)e^{8A/3-2D_i+C}(1+Z_i)\) in the planes complementary to the respective mixed fluxes, where \(D_1=D,D_2=B,\ Z_1=Z,\ Z_2=0\). These follow by converting the horizontal and mixed four-form components into the warped orthonormal frame. The comass of a two-form with these three blocks is the largest absolute block coefficient. The sphere coefficients have magnitude at most \(\sqrt8/4<1\) on the unwarped products and remain below one sufficiently close to resonance. Pointwise, the largest available pressure-to-tension ratio on the near-resonant warped branch is attained on the torus plane.

A sharper bound holds at fixed charge. Let \(dV_{T,0}\) be the pullback of the unwarped torus area form. Its comass in \(g_6\) is \(\rho^{4/3}\), so
\[
 \int_\Sigma e^{4W}dV_\Sigma
 \ \ge\ e^{4A_{\min}}\left|\int_\Sigma dV_{T,0}\right|.
\]
For \([\Sigma]=[T^2]\) the integral on the right is the reference torus area. A torus at the warp minimum attains it. By closedness the pressure \(P\) is the same on every representative of this class. Evaluating on the torus using the duality lift gives \(P=4T_5{\cal A}_{T,0}\), whereas its tension at base position \(y\) is \(T_5{\cal A}_{T,0}e^{4A(y)}\). Thus \(\alpha=4T/P=e^{4A_{\min}}\) for the minimizing surface. Charge sectors with a sphere component are outside this fixed-homology action comparison.

## The action and scale along quantized sequences

Let \(\Omega_4=8\pi^2/3\). The Euclidean round probe action in unit reference AdS is
\[
 I(\chi)=\Omega_4 T\left[\sinh^4\chi-\frac4\alpha\int_0^\chi\sinh^4 r\,dr\right].
\]
Its stationary radius is \(\tanh\chi=\alpha\), which exists for \(0<\alpha<1\). The envelope derivative of the stationary action with respect to \(T\) at fixed \(P\) is the positive sphere area. Therefore the surface that attains the tension bound also gives the least action among the round unfluxed probes of this primitive torus charge. At the minimum the stationary action is
\[
 B=\Omega_4 T\left[1+\frac1{2(1-\alpha^2)}-\frac{3}{2\alpha}\operatorname{arctanh}\alpha\right],
 \qquad B\sim \frac{\Omega_4 T}{4(1-\alpha)}.
\]
A torus at the minimum is stationary under both external and internal shape variations. The external radius satisfies the pressure condition and the internal first variation vanishes because the effective torus tension is minimized and the closed pressure form has no \(dy\wedge dT\) component.

The [unwarped flux dictionary](2026-11-16_D9_iib_conifold_dual.md) and the [fixed-Page rescaling](2026-11-16_Tpq_warp_central_charge.md) give \(\Omega_4 T=(4\pi^3/3)N_0\alpha/I_P\) for one torus wrapping, where \(I_P\) is the dimensionless IIB Page integral. One can also obtain this normalization directly from \(T_5=1/[(2\pi)^5\ell_p^6]\) and the unwarped M-theory area and radius formulas. Near the quadrupole resonance \(p I_P\to 9\sqrt6\pi^3/40\). For the [Pell sequences](2026-11-16_Tpq_warp_resonance.md), let \(D_{\rm Pell}=25q^2-32p^2\), with fixed values \(-7\) and \(17\). The warp coefficient satisfies \(p^2\epsilon\to5D_{\rm Pell}/1024\). For negative coefficient the minimum is at a pole to leading order, and for positive coefficient it is at the equator, where \(P_2=-1/2\). It follows that
\[
 \lim\frac{B}{N_0p^3}
 =\begin{cases}
  2048/(27\sqrt6\,|D_{\rm Pell}|),&D_{\rm Pell}<0,\\
  4096/(27\sqrt6\,D_{\rm Pell}),&D_{\rm Pell}>0 .
 \end{cases}
\]
The large-charge comparison keeps \(p,q\) primitive and at fixed torus shape. One may take \(N_0\) of order \(p^\nu\) with \(2<\nu<3\). Then \(L/\ell_p\) and the torus radii in Planck units grow as \(p^{\nu/3}\) and \(p^{1/2-\nu/6}\), respectively, while the fractional one-unit charge jump is smaller than the order-\(p^{-2}\) probe detuning. These scaling inequalities identify a regime in which to test backreaction. They do not control the fully backreacted action or the other vacuum instabilities.

## Radial shape modes that carry torus momentum

Keep the torus at the minimizing base point and allow the external normal displacement to vary on \(S^4_\chi\times T^2\). At fixed base point the induced metric is a product with external sphere radius \(a=e^W\sinh\chi\) and internal metric \(\rho^{-4/3}g_{T,0}\). The DBI quadratic form has the two Laplacians. The pressure term gives the same local \(-4/a^2\) Jacobi potential as for a round D3, since varying the external radial graph at fixed torus coordinates changes the enclosed volume independently at each torus point. The normal eigenvalues up to the common positive tension are
\[
 \frac{\ell(\ell+3)-4}{a^2}+\rho^{4/3}\lambda_T .
\]
Here \(\lambda_T\) is the squared momentum in the reference torus metric of the same solution. Extra radial negative modes can occur only at \(\ell=0\), for nonzero torus labels with
\[
 \lambda_T<
 4(1-\alpha^2)\alpha^{-2}e^{-2C+4A/3}.
\]
The right-hand side is order \(p^{-2}\) along the primitive Pell families. At fixed torus shape in the scaling window above, the smallest nonzero \(\lambda_T\) grows as \(N_0/p\). The radial normal sector then has exactly one negative mode, carried by the constant mode on both factors. Internal normal and chiral worldvolume fluctuations remain separate. This radial cutoff is also distinct from the bulk coupled scalar–Maxwell spectrum.

The [verifier](toe_20261116_Tpq_M5_probe_action.py) checks the warped pressure coefficients and the exact hyperbolic action and evaluates numerical probes from the existing background solver. Its [JSON output](../data/toe_20261116_Tpq_M5_probe_action.json) records the radius, exponent per unit horizontal flux, and radial momentum cutoff.
