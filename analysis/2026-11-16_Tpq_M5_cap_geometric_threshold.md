# Geometric spectator threshold of the capped M5

The [capped M5 probe](2026-11-16_Tpq_M5_cap_probe_index.md) has one geometric negative eigenvalue on its \(S^5\) factor, denoted \(\lambda_0<0\) in local AdS units. Computing it yields the sharp spectral criterion for the spectator circle. The earlier \(4\pi/c\) bound is a sufficient bound using the maximum pointwise curvature. The actual threshold is much longer in the near-planar regime. For \((p,q)=(38,43)\) it is about \(239.32\) local AdS units. [Rotational CMC sphere and stability](https://arxiv.org/abs/2301.11038)

## Scalar Jacobi problem and exact mode-count criterion

Use the [capped meridian](2026-11-16_Tpq_M5_finite_stripe.md), with arclength \(s\), hyperbolic radius \(r(s)\), and longitudinal velocity \(v=dz/ds=cV(r)/\sinh^4r\). Set \(S=\sinh^4r\). The four angular principal curvatures are \(h=v\coth r\), and the meridian curvature is \(c-4h\). The hyperbolic component of the unit normal has squared norm \(v^2\), so the geometric potential \(|{\rm II}|^2+\operatorname{Ric}(n,n)\) is
\[
 Q(r)=(c-4h)^2+4h^2-4v^2=(c-4h)^2+4h^2\operatorname{sech}^2r .
\]
The ground lies in the rotation-invariant sector of
\[
 L_0=-S^{-1}\partial_s(S\partial_s)-Q.
\]
It is even about the bulge, so the eigenproblem uses a regular tip and a Neumann condition at the bulge on one half of the cap. The longitudinal translation field has one node on the full meridian. The external translation fields are nodeless in the radial factor of the first angular sector. As in the earlier normal index calculation, these facts show that \(\lambda_0\) is the only negative level before adding the spectator circle.

A Fourier integer \(n\) on a spectator circumference \(\ell_\perp\) adds \((2\pi n/\ell_\perp)^2\) to each geometric eigenvalue. The internal and chiral blocks stay nonnegative on the stated near-resonant backgrounds by the weighted factorization. The bosonic probe index is therefore exactly
\[
 1+2\,\#\{\, n\in\mathbb Z_{>0}:\ (2\pi n/\ell_\perp)^2<-\lambda_0\,\}.
\]
At equality the pair of threshold modes is neutral. The sharp spectral threshold is \(\ell_\perp^\star=2\pi/\sqrt{-\lambda_0}\). The numerical values below resolve \(\lambda_0\), rather than using the earlier pointwise curvature sufficient condition.

## Numerical values

The solver integrates the Jacobi Rayleigh form on the half cap after \(r=r_+\sin\theta\), with separate Gauss quadrature and Legendre resolutions and a local turning-point Taylor expansion to avoid subtracting nearly equal speeds at the bulge. The basis is regular and even at the tip in \(r\), and the vanishing \(dr/ds\) enforces reflection at the bulge. The code also evaluates the differential residual separately from the generalized matrix eigenpair. These are convergence and residual checks, not interval-certified error bounds.

| Chern pair | \(\lambda_0\sinh^2 r_0\) | \(\ell_\perp^\star\) in local AdS units | \(\ell_\perp^\star/P_0\) |
| --- | ---: | ---: | ---: |
| \((7,8)\) | \(-3.0053471\) | \(32.78432\) | \(1.15367\) |
| \((8,9)\) | \(-3.0062545\) | \(30.10470\) | \(1.15350\) |
| \((38,43)\) | \(-3.0001132\) | \(239.31866\) | \(1.15468\) |

Here \(r_0=\operatorname{arctanh}\alpha\) is the round-probe radius and \(P_0=\pi\sinh r_0\) its longitudinal instability period. In each tested background, a square torus near the [cap–round action crossing](2026-11-16_Tpq_M5_finite_stripe.md) has spectator circumference below the cap's first extra negative mode. A second-direction localization could still arise away from a linear instability of this cap.

## Near-planar limiting operator

Let \(u=1/\sinh^2 r_0\) and \(y=u\sinh^2 r\). At fixed \(0<y<2\) as \(u\to0\), the first integral gives
\[
 1-v^2=u(2/y-1)+o(u),\qquad Q/u\to4/y .
\]
The coordinate \(\sigma=\sqrt{u}\,s\) consequently gives \(y=2\sin^2\sigma\) on the limiting half cap, \(0<\sigma<\pi/2\). The measure is proportional to \(\sin^4\sigma\,d\sigma\). The bulk limiting operator is
\[
 -\partial_\sigma^2-4\cot\sigma\,\partial_\sigma-2\csc^2\sigma .
\]
Conjugating by \(\sin^2\sigma\) gives the constant-coefficient operator \(-\partial_\sigma^2-4\). The finite-form-energy choice at the tip becomes Dirichlet after conjugation, since the other indicial behavior of the original eigenfunction is \(\sigma^{-2}\) and has divergent gradient energy. Reflection imposes Neumann at the bulge. The lowest eigenvalue of this limiting problem is \(-3\) with unconjugated profile \(\csc\sigma\). The odd-reflection translation gives zero, as in the exact cap. This derivation identifies the limiting spectral problem and is consistent with the numerical convergence toward \(\lambda_0/u=-3\) and \(\ell_\perp^\star/P_0=2/\sqrt3\); it does not bound boundary-layer errors for arbitrarily small \(u\). The opposite, small-\(\alpha\) limit gives the Euclidean \(S^5\) of radius \(5r_0/4\), for which \(\lambda_0\sinh^2r_0\to-16/5\). The controls cover both regimes.

Reproduce the [numerical threshold certificate](../data/toe_20261116_Tpq_M5_cap_geometric_threshold.json) with `py -3 -B analysis/toe_20261116_Tpq_M5_cap_geometric_threshold.py`. These thresholds concern the classical probe operator. Bulk backreaction and the nonlinear branch beyond the spectator threshold remain open.
