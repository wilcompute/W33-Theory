# Homogeneous radion response to a D9 KK mass source

Consider the repo's unwarped nine-dimensional Einstein–Maxwell branch on \(\mathrm{AdS}_5\times S^2(R_a)\times S^2(R_b)\) with fixed magnetic fluxes. Write \(A=R_a^{-2}\), \(B=R_b^{-2}\), \(\delta=(A-B)/(A+B)\), and shift the two log-radii by \(\beta_a=u+v,\ \beta_b=u-v\). The log-radius fields have kinetic metric \(G=\mathrm{diag}(56/3,8)\) in the convention \(-G_{ij}\partial\phi^i\partial\phi^j/2\). The background fields obey \(f_i^2=2A_i+2(A+B)/5\), and \(L^2=20/(A+B)\). [Repo background and radion masses](2026-11-14_nextfive_flux_cursor_frame_optical_results.md) · [General Einstein–Maxwell product fluctuations](https://arxiv.org/abs/1310.6360)

In five-dimensional Einstein frame the common Weyl factor in the homogeneous potential and the internal derivative contribution to the spin-two squared mass is \(e^{-8u/3}\). The potential is this factor times \(\sum_i[-2 A_i e^{-2\beta_i}+(f_i^2/2)e^{-4\beta_i}]\). The internal derivative mass is the factor times \(\sum_i n_i A_i e^{-2\beta_i}\), where \(n_i=\ell_i(\ell_i+1)\). For a massive mode define \(z=(n_a A-n_b B)/(n_a A+n_b B)\). Its log squared-mass gradient is \(g=(-14/3,-2z)^T\). Direct differentiation gives

```text
L² Hess(V) = [[1120/3, 160 δ], [160 δ, 288]] = K.
```

The dimensionless static susceptibility for this source is

\[
g^T K^{-1}g=\frac{7}{120}\left(1+\frac{5(z-\delta)^2}{21-5\delta^2}\right).
\]

For positive radii \(|\delta|<1\). Among the massive harmonics the lower bound \(7/120\) is attained exactly at \(\ell_a=\ell_b\). There \(K^{-1}g=(-1/80,0)^T\), so the two radii shift together despite the volume–shape mixing at unequal flux. The result also has a finite-source counterpart. Add the specified static term \(J m_{\rm KK}^2(u,v)\) to the potential. For common \(n_a=n_b=n\) it rescales the internal curvature term by \(1-Jn/2\). At \(v=0\), \(\partial_v(V+Jm^2)=(3\delta/7)\partial_u(V+Jm^2)\). The stationary branch through the background is exactly

\[
v=0,\qquad e^{2u}=\frac{1}{1-Jn/2}\quad (Jn<2).
\]

For a nonuniform Euclidean source, set \(x\) to the eigenvalue of the positive external scalar Laplacian in units \(L^{-2}\). The shape component of \(-(K+xG)^{-1}g\) for equal angular degrees is

\[
\frac{\delta x}{4[(x+20)(x+36)-(1200/7)\delta^2]}.
\]

The zero-static-shape response therefore coexists with shape exchange for unequal flux at nonzero momentum. This calculation uses a specified source for the internal derivative term. Matching a physical spin-two amplitude requires the other metric and Maxwell vertices and a choice of external AdS observables. The same diagonal harmonic sequence has \(m_{11}^2L^2=40\), \(m_{22}^2L^2=120\), so magnetic charge tuning provides no parametric separation between those two exchange scales. [Previous mixed-harmonic overlap check](2026-11-14_kk_cutoff.md) · [Scope of the flat-space spin-two scalar bound](https://arxiv.org/abs/2608.05273)

Replay with `py -3 analysis/toe_20261114_d9_radion_response.py`.
