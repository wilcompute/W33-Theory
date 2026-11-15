# Canonical bolt distance and the nodal contribution to the D9 potential

The [nodal core EFT](2026-11-14_cubic_flux_bubble_eft.md) gives the leading local action term of the Eguchi–Hanson region as \(192\pi^2\Omega/(7a^2)\), where \(a\) is the bolt radius and \(\Omega=\beta+104\alpha^2/7\) for the two operators specified there. To compare derivatives of this term to the AdS scale, the bolt parameter must be normalized by its metric deformation. This calculates the norm in the complete Ricci-flat inner space and uses the compact Einstein-frame volume to normalize its contribution to the five-dimensional kinetic term. [Eguchi–Hanson Einstein deformations](https://arxiv.org/abs/2105.13193) · [Kähler–Einstein nodal gluing](https://arxiv.org/abs/1211.5344)

## An explicit transverse traceless size mode

Use \(F_r=1-a^4/r^4\), with metric coefficients \(F_r^{-1},r^2/4,r^2/4,r^2F_r/4\) along \(dr,\sigma_1,\sigma_2,\sigma_3\). At fixed \(r^4-a^4\) the size variation is \(h=\partial_a g+\mathcal L_{a^3r^{-3}\partial_r}g\). This chart follows the bolt, and the vector field decays at infinity. In the orthonormal frame the components are

\[
h=\frac{2a^3}{r^4}\operatorname{diag}(-1,1,1,-1).
\]

The equal radial and collapsing-circle coefficients give a regular tensor at the bolt. Its trace vanishes. For a diagonal invariant tensor, only the radial divergence can be nonzero. In proper radial distance \(\rho\), this divergence is \(\partial_\rho h_{00}+\sum_i (\partial_\rho\log w_i)(h_{00}-h_{ii})\), with \(w_i\) the orbit metric radii. The fiber term vanishes and the two horizontal terms cancel the derivative of \(h_{00}\). This is an exact representative of the radial Ricci-flat deformation. For a complex smoothing at fixed Kähler period, use the hyperkähler-rotated description of the same inner metric. The radial norm is unchanged by that rotation. [ALE hyperkähler period description](https://academic.oup.com/qjmath/article/76/1/337/7990706)

The integrated square norm with orbit-integrated volume \(\pi^2r^3dr\) is

\[
\int_{r\ge a}|h|^2=4\pi^2a^2,\qquad
\frac{\int_{a\le r\le b}|h|^2}{\int_{r\ge a}|h|^2}=1-(a/b)^4.
\]

The five-dimensional Einstein kinetic term from a transverse traceless variation is \(-\int |h|^2(\partial a)^2/(4\operatorname{Vol} M)\), after factoring out the coefficient of \(R_5\). With \(\operatorname{Vol}M=6\pi^2R^4\), the radial coordinate with kinetic term \(-\tfrac12(\partial\varphi)^2\) in this inner calculation is \(\varphi=a^2/(2\sqrt3 R^2)\). It gives a finite radial distance to \(a=0\) for the core contribution. In terms of the transverse smoothing parameter \(t\), \(a/R\) scales as \(|t|^{1/4}\), so this distance scales as \(|t|^{1/2}\). The norm calculation describes the localized component and does not bound the differentiated bulk gluing correction or the full compact moduli metric.

## Potential derivatives in the normalized coordinate

With the convention \(R_5-\tfrac12(\partial\varphi)^2-V\), the prior inner action contribution and \(L^2=10R^2\) give

\[
L^2 V_{\rm core}=-\frac{320\Omega}{7R^2a^2}
=-\frac{160\Omega}{7\sqrt3 R^4\varphi},\qquad
\frac{d^2(L^2 V_{\rm core})}{d\varphi^2}
=-\frac{7680\Omega R^2}{7a^6}.
\]

For \(|\Omega|\) of order \(\ell^4\) with cutoff length \(\ell\), pick \(a=\ell^{2/3}R^{1/3}\). In the large-flux limit \(R/\ell\to\infty\), the local higher-derivative expansion parameter is \((\ell/R)^{2/3}\), the core potential in AdS units is of order \((\ell/R)^{8/3}\), and its second derivative in the core-normalized field stays finite in AdS units. Thus a small contribution to the potential can have appreciable curvature in field space while remaining below the local cutoff. The core term is monotone for \(\Omega\ne0\). Its second derivative becomes a physical scalar mass only after finding a stationary point of the matched compact potential and using the full kinetic metric, so it cannot by itself be compared with an AdS stability bound.

Replay the tensor norm, cutoff fraction, and scale checks with `py -3 analysis/toe_20261114_cubic_flux_bolt_distance.py`.
