# Finite-amplitude M5 stripe and the capped local flux saddle

The [nonuniform wrapped M5 stripe](2026-11-16_Tpq_M5_nonuniform_probe.md) has an exact first integral. It continues from the round-cylinder threshold to a shrinking neck and a smooth capped saddle. Quadrature finds no crossing of stripe and round actions at the sampled amplitudes. A different comparison reveals a crossing: the capped saddle can have lower action than the round one while the round torus-momentum sector still has its single constant negative mode. The cap is localized along one torus cycle and changes the topology of the probe worldvolume.

## First integral and two ways to close the worldvolume

Use a rectangular worldvolume torus, and let \(z\) be proper distance along the modulated circle in local AdS units. Keep the transverse circle wrapped and the base position at the polar or equatorial warp minimum. The first variation in that base position vanishes for these radial graphs because the first derivatives of the AdS warp and torus radius vanish there and the torus pressure coefficient is constant. Up to a common positive factor, the action per transverse circle is
\[
 J=\int dz\,\big[S(r)\sqrt{1+r_z^2}-cV(r)\big],\quad
 S(r)=\sinh^4r,\quad V(r)=\int_0^r S(v)\,dv,\quad c=4/\alpha.
\]
It is the constant-pressure area–volume problem for a rotational hypersurface in \(H^5\times\mathbb R\) before taking the circle quotient. [Rotational CMC spheres in hyperbolic products](https://arxiv.org/abs/2301.11038) · [M5 probe action](https://arxiv.org/abs/1308.2231)

Set \(U=S-cV\). The nonzero maximum \(U_0\) lies at \(r_0=\operatorname{arctanh}\alpha\) because \(U'=4S(\coth r-1/\alpha)\). Translation in \(z\) gives \(E=S/\sqrt{1+r_z^2}-cV\). For every \(0<E<U_0\), the two turning points \(r_\pm\) solve \(U(r_\pm)=E\); the profile has a strictly positive neck and defines a periodic smooth graph. Its period \(P\) and full-period action are
\[
 \begin{aligned}
 P(E)&=2\int_{r_-}^{r_+}\frac{E+cV}{\sqrt{S^2-(E+cV)^2}}\,dr,\\
 J(E)&=E P(E)+2\int_{r_-}^{r_+}\sqrt{S^2-(E+cV)^2}\,dr .
 \end{aligned}
\]
At the round endpoint \(P_0=\pi\sinh r_0\) by the [radial cutoff](2026-11-16_Tpq_M5_probe_index.md). The second integral vanishes at \(E=U_0\) and has derivative \(-P(E)\). Thus \(J'(E)=E P'(E)\) and the stripe action excess against a round probe on the same period is exactly
\[
 J(E)-P(E)U_0=\int_E^{U_0}[P(\xi)-P(E)]\,d\xi .
\]
This identity would imply strict positive excess everywhere if global period monotonicity were proved. The verifier tests the sign and derivative identity by quadrature; it does not certify continuous monotonicity.

The \(E=0\) limit has \(r_-=0\) and a finite bulge. At the neck \(dz/dr\sim cr/5\), so \(z-z_{\rm tip}\) is a smooth function of the squared radial distance and the \(S^4\) caps off. Reflecting at the bulge gives the smooth \(S^5\) in the cover. At period \(P_{\rm cap}=P(0)\), a periodic chain has neighboring caps touching. For a longitudinal circle of length \(L_\parallel>P_{\rm cap}\), a single cap fits without touching its images. Its lifted worldvolume is \(S^5\times S^1\), and its action is the length-independent \(J(0)\) times the common transverse factor. The round probe action on that circle is \(L_\parallel U_0\), so the crossing is exactly at \(L_\parallel=J(0)/U_0\) if that period exceeds \(P_{\rm cap}\). The capped brane sweeps an interval of the longitudinal circle and sources a local flux domain in \(H^5\times S^1\). The round brane wraps both cycles and implements the homogeneous torus discharge channel. A lower cap action is a comparison of two probe saddles at the same background, rather than a smaller exponent for homogeneous one-unit discharge.

## Checks and the geometric negative mode

The quadrature uses the cosine variable between the turning radii and the stable factorization \(S^2-(E+cV)^2=(U-E)(S+E+cV)\). It checks 13 energies for each of seven control values of \(\alpha\), and also uses the three actual tension ratios from the [warped M5 probes](2026-11-16_Tpq_M5_probe_action.md). Every sampled stripe has positive excess. In the small-\(\alpha\) limit the hyperbolic integrals reduce to the Euclidean rotational sphere, with \(r_0\sim\alpha,\ r_+\sim5\alpha/4,\ U_0\sim\alpha^4/5\). The limits are \(P_{\rm cap}/P_0\to5/(2\pi)\) and \(J(0)/(U_0P_0)\to15625/16384\). The quadratures recover the approach to these limits and find both ratios approach one numerically as \(\alpha\) approaches one.

| Warped Chern pair | Minimum length for one cap, divided by \(P_0\) | Action crossing length divided by \(P_0\) |
| --- | ---: | ---: |
| \((7,8)\) | \(0.974159677\) | \(0.998043432\) |
| \((8,9)\) | \(0.971816151\) | \(0.997732830\) |
| \((38,43)\) | \(0.996624309\) | \(0.999953545\) |

The geometric normal of the capped hypersurface in \(H^5\times\mathbb R\) has exactly one unconstrained negative mode. The Jacobi field for translations along the line has one interior node on the meridian, so Sturm oscillation in the rotation-invariant sector gives one negative eigenvalue below it. In the \(\ell=1\) angular sector the hyperbolic Killing fields have a nodeless radial coefficient and give zero ground eigenvalue. Higher angular sectors increase the angular-gradient potential. For a transverse spectator circle the normal operator adds its nonnegative Fourier eigenvalues, so a sufficiently short spectator produces no more negative modes in this block. For example at the cap the four equal angular curvatures are \(k_\theta=cV\coth r/S\). Differentiating \(S\tanh r/4\) shows \(V\le S\tanh r/4\), hence \(0\le k_\theta\le c/4\); the meridian curvature \(c-4k_\theta\) is nonnegative. This bounds \(|{\rm II}|^2\le c^2\), while ambient Ricci in the normal direction is nonpositive. A spectator circumference below \(2\pi/c\) therefore suffices. The statement concerns the geometric normal block. Internal displacements, the chiral determinant, and coupled bulk fluctuations of the capped saddle require separate checks. [CMC sphere stability](https://arxiv.org/abs/2301.11038)

There is a scale issue in applying the comparison. Near the Pell limit the longitudinal threshold in local AdS units is of order \(p\). If the two mixed fluxes are primitive, the unwarped torus area in AdS units is of order \(p/N_0\). Stretching a primitive rectangular torus to the threshold then shrinks the transverse circumference to order \(N_0^{-1}\) in AdS units, below the eleven-dimensional Planck scale at large \(N_0\). A common divisor \(J_{\rm flux}\) of the two mixed periods preserves their ratio and the dimensionless warp while increasing the torus area by \(J_{\rm flux}\). Taking \(J_{\rm flux}\) of order \(N_0\) with a chosen constant prefactor lets the transverse length remain of order the AdS radius and the longitudinal length be of order \(p\) times that radius. All lengths can then be large in Planck units with suitable rectangular shape. This does not establish control of the dynamical backreaction at a localized cap.

Reproduce the [JSON result](../data/toe_20261116_Tpq_M5_finite_stripe.json) with `py -3 -B analysis/toe_20261116_Tpq_M5_finite_stripe.py`.
