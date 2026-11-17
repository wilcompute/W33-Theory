# Spectator-circle bifurcation of the capped M5 probe

The [cap's first spectator zero modes](2026-11-16_Tpq_M5_cap_geometric_threshold.md) generate a local new branch. Its normal displacement depends on the spectator coordinate as well as the original meridian. On the three near-resonant warped backgrounds, the reduced quartic is positive. Consequently the modulated cap exists on the long-spectator side and has less action than the uniform cap. Small-curvature-radius controls have the opposite quartic sign. The local modulation leaves the worldvolume topology \(S^5\times S^1\), with the spectator still wrapped. A cap that also closes along this cycle would require a finite deformation. [Rotational CMC caps](https://arxiv.org/abs/2301.11038) · [Normal-graph CMC bifurcation methods](https://projecteuclid.org/journals/journal-of-differential-geometry/volume-64/issue-3/From-Constant-mean-Curvature-Hypersurfaces-to-the-Gradient-Theory-of/10.4310/jdg/1090426999.full)

## Exact normal-graph action

At a fixed transverse warp minimum the purely geometric probe equations reduce to a constant-pressure area–volume problem in \(H^5\times\mathbb R_z\times S^1\), in local AdS units. The warp and torus metric have vanishing first transverse derivatives at a polar or equatorial wrapping location, so such graphs have zero first variation in the internal base. The pullback of \(G_4\) remains zero, and the unfluxed three-form is admissible. Fix a longitudinal circumference strictly larger than the cap width so that the graphs remain embedded for small amplitudes. [M5 action](https://arxiv.org/abs/1308.2231)

Use arclength \(s\) on the capped meridian and an angle \(\theta\) of period \(2\pi\) on the spectator, with \(K=(2\pi/\ell_\perp)^2\). Let \(f(s,\theta)\) be an outward normal graph, \(v=z_s\), \(h=v\coth r\), and \(m=c-4h\), where \(c=4/\alpha\). A normal geodesic in the meridian plane changes \((r,z)\) by \((v,-r_s)f\). The angular and meridian tubular metric lengths are multiplied by \(\cosh(vf)+(h/v)\sinh(vf)\) and \(1+mf\). The expression for the angular factor has a regular limit at the tip. Set
\[
 {\cal J}(f)=(1+mf)\big[\cosh(vf)+(h/v)\sinh(vf)\big]^4 .
\]
After dividing by the common positive tension and reference area, the exact action difference is the average with measure \(S(s)\,ds\,d\theta\) of
\[
 {\cal J}(f)\sqrt{1+\frac{f_s^2}{(1+mf)^2}+Kf_\theta^2}
       -1-c\int_0^f{\cal J}(t)\,dt .
\]
This uses the volume swept by the normal graph. Its second variation has the undistorted cap Jacobi potential \(Q\) and additive spectator eigenvalues \(n^2K\).

## Branch and sign test

Write \(K_c=-\lambda_0\) and normalize the geometric ground function \(\psi\) to \(\langle\psi^2\rangle_s=1\) in the weighted meridian average. Keeping the mode even across the bulge removes the longitudinal translation. Keeping the spectator profile even fixes its phase, and imposing external \(SO(5)\) invariance excludes the external translations. In this subspace the sole kernel at \(K=K_c\) is \(\psi(s)\cos\theta\). Its eigenvalue derivative with respect to \(K\) is one. Invert the complementary elliptic operator and then divide the one-dimensional equation by the kernel amplitude. This gives the local bifurcation when the quartic below is nonzero. Spectator half-period translation reverses the amplitude and makes the reduced action even. By symmetry, stationarity in this subspace gives stationarity for the full geometric probe.

Write \({\cal J}(f)=1+cf+j_2 f^2+j_3 f^3+j_4 f^4+\cdots\). The direct quartic comes from the normal-graph action at \(f=a\psi\cos\theta\). The cubic variational source has only a constant and second spectator harmonic. If \(b_0,b_2\) denote the weak-form sources of these harmonics and \(H_0,H_2\) their quadratic forms including the Fourier averaging factors, the corrected quartic is
\[
 b={\cal Q}_{4,\mathrm{direct}}-\frac12
       \big[b_0^{\mathsf T}H_0^{-1}b_0+b_2^{\mathsf T}H_2^{-1}b_2\big].
\]
The constant harmonic includes the cap's negative mode. Omitting that response changes the coefficient. The code checks the tube coefficient identity \(j_2-c^2/2=-Q/2\), evaluates the two linear inverses, and repeats the calculation with larger meridian basis and quadrature.

For \(\sigma=K-K_c\), the reduced action is \(\sigma a^2/4+ b a^4+O(a^6+|\sigma|a^4)\). It gives
\[
 a^2=-\sigma/(8b)+O(\sigma^2),\qquad
 I_{\rm modulated}-I_{\rm uniform}=-\sigma^2/(64b)+O(|\sigma|^3)
\]
in the normalized units. For positive \(b\), the branch lies at \(\sigma<0\), or \(\ell_\perp>\ell_\perp^\star\), and its magnitude direction becomes positive while its phase remains a translation. The original negative cap direction survives in the complement. On the tested warped backgrounds the remaining internal and chiral sectors retain their gaps for sufficiently small modulation, after keeping their exact symmetry zero modes. Thus the nearby modulated physical probe has index one while the uniform cap on that side has index three. For negative \(b\) the branch instead lies on the short side, has higher action, and adds a negative magnitude direction. [Uniform-cap internal and chiral blocks](2026-11-16_Tpq_M5_cap_probe_index.md)

| Warped Chern pair | Reduced quartic \(b\) |
| --- | ---: |
| \((7,8)\) | \(4.9075630\times10^{-4}\) |
| \((8,9)\) | \(5.7541187\times10^{-4}\) |
| \((38,43)\) | \(9.6921649\times10^{-6}\) |

In the Euclidean small-cap limit the corresponding coefficient is exactly \(-35/(48R_{\rm cap}^4)\). The numerical controls locate a sign change at \(\alpha\simeq0.917576899\), stable across the two resolutions. They do not exclude other roots or resolve the sixth-order problem at the sign change. The positive coefficients in the table classify a local probe branch. They give no conclusion about finite-amplitude closure, front interactions, or gravitational backreaction.

Reproduce the [certificate](../data/toe_20261116_Tpq_M5_cap_spectator_branch.json) with `py -3 -B analysis/toe_20261116_Tpq_M5_cap_spectator_branch.py`.
