# Nonlinear continuation through the capped M5 spectator fold

The [sixth-order action](2026-11-16_Tpq_M5_cap_sixth_order.md) predicts a fold and an equal-action transition on the negative-quartic side of the spectator bifurcation. This calculation solves the full unfluxed normal-graph equation numerically across that region. It uses the graph amplitude to continue through the fold while the spectator circumference turns. The tension ratios here are controls near the quartic zero, below the values of the three near-resonant warped examples already constructed. [Normal-graph CMC constructions](https://projecteuclid.org/journals/journal-of-differential-geometry/volume-64/issue-3/From-Constant-mean-Curvature-Hypersurfaces-to-the-Gradient-Theory-of/10.4310/jdg/1090426999.full)

## Solver and action check

Use the [exact tubular action](2026-11-16_Tpq_M5_cap_spectator_branch.md), with \(K=(2\pi/\ell_\perp)^2\) in local AdS units. The meridian basis diagonalizes the reference cap's Jacobi quadratic form. A cosine basis fixes the spectator phase, and both halves of the meridian are related by reflection. Prescribe the coefficient \(a\) of \(\psi(s)\cos\theta\), where \(\langle\psi^2\rangle_s=1\). Solve the full weak variational equation for all other coefficients and for \(K\) together. The second-order deformation gives the starting guess. The numerical solve evaluates the hyperbolic tube factors and the square root directly; the sixth-order coefficients select the region to investigate. The action is an independent quadrature of the normal-graph area and swept volume. Its integrand subtracts the uniform action before integration, since the competition occurs at a much smaller scale than the absolute cap action.

Along any stationary profile, the derivative of the normalized action excess with respect to \(K\) is the explicit derivative at fixed graph:
\[
 \frac{d\Delta I}{dK}
 =\left\langle
 \frac{{\cal J}(f)f_\theta^2}
 {2\sqrt{1+f_s^2/(1+mf)^2+Kf_\theta^2}}\right\rangle.
\]
It is positive for a nontrivial modulation. Hence an amplitude parametrization turns the action and \(K\) at the same fold, and the equal-action crossing can be found directly without subtracting two independent extrapolations of the action.

The magnitude curvature has the opposite sign from the slope of \(K(a)\) near the fold. If \(F(a,K)\) is the projected stationarity equation with the other coefficients solved, then \(F_a=-F_K K'(a)\) at a solution and \(F_K=a/2+O(a^3)>0\) for \(a>0\) sufficiently small. The turning point exchanges the sign of this direction while the cap's original negative geometric mode stays in the complement.

## Numerical coexistence and shift

| Tension ratio \(\alpha\) | Fold \(K-K_c\) | Fold amplitude | Equal-action \(K-K_c\) | Equal-action amplitude |
| ---: | ---: | ---: | ---: | ---: |
| \(0.9174768990\) | \(8.72257\times10^{-8}\) | \(0.0428595\) | \(6.53422\times10^{-8}\) | \(0.0525224\) |
| \(0.9172768990\) | \(7.88723\times10^{-7}\) | \(0.0743754\) | \(5.89444\times10^{-7}\) | \(0.0912500\) |

The fold and crossing detunings are about \(2.4\)–\(2.6\%\) above their sixth-order predictions at the closer control, and \(7.3\)–\(7.7\%\) above at the farther control. The two spectral truncations agree on the amplitudes and detunings within \(0.6\%\). For the closer control, at a shared detuning of \(5.8808\times10^{-8}\), the two nonzero solutions have amplitudes \(0.0280705\) and \(0.0537337\), with opposite action excesses \(+5.2554\times10^{-12}\) and \(-4.5726\times10^{-12}\). The uniform cap also exists at that circumference. The second control gives the same action ordering on the two modulated branches. The fine solves for these comparisons have projected variational residuals below \(4\times10^{-14}\).

## Scope

This comparison is local to the cap and keeps the \(S^5\times S^1\) topology. It does not address detachment from the spectator circle, the gravitational shift of the transition, or whether the restricted tension and circumference values can be obtained in a different flux family. The spectral calculation checks the projected stationary equations and convergence with the truncation. It is not a validated numerical existence proof.

Reproduce the [certificate](../data/toe_20261116_Tpq_M5_cap_nonlinear_fold.json) with `py -3 -B analysis/toe_20261116_Tpq_M5_cap_nonlinear_fold.py`.
