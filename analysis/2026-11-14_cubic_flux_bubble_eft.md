# Eguchi–Hanson core coefficients and a controlled nodal scaling

The [cubic-surface EFT calculation](2026-11-14_cubic_flux_eft.md) found a constant four-derivative potential at first order, and a varying curvature-cubed insertion. A constant first-order potential can coexist with a nonuniform metric response. Here the inner model of one smoothed node is \(\mathbb R^{1,4}\times\) Eguchi–Hanson, with external curvature and magnetic stress suppressed relative to the core Riemann tensor by \((a/R)^2\). Here \(a\) denotes the physical bolt scale and \(R=\kappa^{-1/2}\) the bulk Kähler–Einstein curvature scale. This computes the bolt contribution in that inner limit. A matched compact solution would also fix the global response and the effective action outside the core. [Nodal gluing](https://arxiv.org/abs/1211.5344)

Use the Lorentzian action density \(R_D+\alpha\mathcal G+\beta\operatorname{tr}\mathcal R_D^3\), where \(\mathcal G\) is the Gauss–Bonnet combination, \(\mathcal R_D\) is the sectional-curvature operator on two-forms, \([\alpha]=\mathrm{length}^2\), and \([\beta]=\mathrm{length}^4\). The signs below refer to its action after internal integration.

## The direct curvature cube

In the Eguchi–Hanson metric let \(F_r=1-a^4/r^4\) and use proper radial distance with \(dr/d\rho=\sqrt{F_r}\). The three orbit metric radii are \(r/2,r/2,r\sqrt{F_r}/2\). Writing any of these as \(w(\rho)\), the corresponding sectional curvature with one radial direction is \(-w''/w\). One Weyl half vanishes on this Ricci-flat metric, so the nonzero curvature-operator eigenvalues are twice these three sectional curvatures: \((-4,-4,8)a^4/r^6\). Radial volume, after integrating over \(S^3/\mathbb Z_2\), is \(\pi^2 r^3dr\). Therefore

\[
K=R_{abcd}R^{abcd}=384a^8/r^{12},\qquad
\int K=48\pi^2,\qquad
\int\operatorname{tr}\mathcal R^3=\frac{192\pi^2}{7a^2}.
\]

The first integral is independent of the bolt scale, while the second is enhanced as the bolt shrinks. [Eguchi–Hanson geometry and higher-curvature variants](https://arxiv.org/abs/2207.04014)

## Gauss–Bonnet response at second order

On this product the Gauss–Bonnet equation tensor is zero on the internal four-dimensional block by the four-dimensional variational identity. On the flat external block it is \(-K g_{\mu\nu}/2\). Tracing and reversing the nine-dimensional Einstein equation at order \(\alpha\) gives \(R_{\mu\nu}=\alpha K g_{\mu\nu}/7\) and \(R_{ij}=-5\alpha K g_{ij}/14\). Use an external log warp \(A\) and common internal log scale \(B=-5A/2\) at this order. This cancels the Hessian terms in the internal Ricci variation and leaves \(\Delta A=-\alpha K/7\). The solution regular at \(r=a\) and decaying at infinity is

\[
A(r)=\frac{\alpha}{7}\left(\frac{24}{r^2}+\frac{8a^4}{r^6}\right),\qquad
\Delta A=r^{-3}\partial_r(r^3F_r\partial_r A).
\]

The same response follows by expanding the Einstein kinetic action in \(A,B\). On \(B=-5A/2\) its quadratic integrand is \(-35|\nabla A|^2/2\), while the linear Gauss–Bonnet insertion is \(5\alpha K A\). The terms from integration by parts at the bolt and at infinity vanish for the quadratic action with a regular, decaying response. Substituting the solution gives the second-order action correction \((5\alpha/2)\int K A=19968\pi^2\alpha^2/(49a^2)\). The two specified contributions to the local action therefore combine as

\[
\frac{192\pi^2}{7a^2}\left(\beta+\frac{104}{7}\alpha^2\right).
\]

The tuned zero in this formula is for these two operators and the leading Ricci-flat inner approximation. Other operators and global matching may contribute to the compact reduction. In particular, a first-order curvature-cubed calculation alone cannot fix even the leading core effect if Gauss–Bonnet is present.

## A parametric window below the local cutoff

Let the cutoff length be \(\ell\), with fixed-size Wilson coefficients \(\alpha\sim\ell^2\), \(\beta\sim\ell^4\). The aligned flux integer fixes \(R\propto |q|\) at fixed electric coupling. There is a window \(\ell\ll a\ll R\) by taking large flux and a smoothing whose dimensionless bubble scale is small. The normalized nodal smoothing has \(a/R\) of order \(|t|^{1/4}\) for a transverse local parameter \(t\), up to a fixed normalization of the gluing scale. For example \(a=\sqrt{\ell R}\) takes \(|t|\) of order \((\ell/R)^2\). The local derivative expansion parameter \(\ell^2/a^2=\ell/R\) tends to zero. The six-derivative core contribution divided by internal volume and expressed in AdS curvature units has size \(\ell^4/(R^2 a^2)=(\ell/R)^3\), larger than the smooth-bulk size \((\ell/R)^4\) by \(R/\ell\) when the leading coefficient is nonzero. Its absolute size still tends to zero. This is a controlled enhancement in the inner computation, with the sign of a physical potential or its stationary points requiring the compact effective action.

Replay the inner curvature, radial response, and action checks with `py -3 analysis/toe_20261114_cubic_flux_bubble_eft.py`.
