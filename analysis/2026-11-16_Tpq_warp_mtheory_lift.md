# Warped M-theory lift and torus-momentum spin-two masses

The [near-resonant Type IIB branch](2026-11-16_Tpq_coupled_warp_branch.md) lifts by circle T-duality and the IIA-to-M lift to source-free warped \(\mathrm{AdS}_5\) solutions on \(S^2\times S^2\times T^2\). The Chern pair and the Page period become the three four-form periods as on the [product branch](2026-11-16_D9_iib_conifold_dual.md). The lift gives a decoupled spectral problem for external transverse traceless gravitons with torus momentum. Their lowest mass in each momentum sector increases at second order throughout the bare torus eigenvalue range \(0<\lambda_T<12\). That numerical range is also used in the repo's separate scalar instability analysis at equal flux.

## The warped fields and their periods

Use the Type IIB normalization \(L=1,\ f=4\) for the electric five-form and absorb constant dilaton and reference-circle factors into the unwarped metrics. The first and second sphere metrics are \(g_1,g_2\). The dimensionless string-frame fiber radius relative to its unwarped value is \(\rho=e^{C-5A/3}\). The remaining IIB metric is \(e^{2A}g_{\mathrm{AdS}_5}+e^{-10A/3}(e^{2D}g_1+e^{2B}g_2)\). T-duality replaces the fiber metric by its inverse, shifts the IIA dilaton by \(-\log\rho\), and generates NS three-form flux from the circle curvature. The eleven-dimensional lift is
\[
 ds_{11}^2=
 \rho^{2/3}\!\left[e^{2A}g_{\mathrm{AdS}_5}
   +e^{-10A/3}(e^{2D}g_1+e^{2B}g_2)\right]
   +\rho^{-4/3}g_{T,0}.
\]
Here \(g_{T,0}\) is the flat reference torus metric. Its constant shape comes from the IIB axiodilaton, with a constant axion accounting for the flat IIA RR one-form. The entire torus metric acquires the same local factor. [Hassan, RR T-duality rules](https://arxiv.org/abs/hep-th/9907152) · [Aspinwall, M-theory and Type IIB](https://arxiv.org/abs/hep-th/9510086)

In coordinates on the torus adapted to the reduction and duality circles, the internal \(G_4\) has a horizontal term proportional to \(e^{2D+2B+C-40A/3}\,dV_1\wedge dV_2\) and a mixed term proportional to the deformed circle curvature wedged with the torus area form. The first term is the contraction of the internal IIB five-form with the dualized circle generator. The mixed term originates in the NS three-form. The proportionality constants and orientations are fixed by the unwarped duality dictionary. The horizontal integral retains the five-form Page period, and both mixed integrals retain their Chern numbers because the connection deformation has zero integral. These forms are closed, and the eleven-dimensional equations follow locally by reduction and duality. Their globally defined curvatures and torus metric reconstruct the bosonic background with the indicated periods. A choice of spin lift or a classification of flat \(C\)-field data is a separate global question. [Topological T-duality](https://arxiv.org/abs/hep-th/0306062)

## Decoupled tensor operator

For a warped \(\mathrm{AdS}_5\) factor \(e^{2W}g_{\mathrm{AdS}_5}\), the external transverse traceless tensor profile has internal norm measure \(e^{3W}dV_6\) and gradient form \(\int e^{5W}|du|^2 dV_6\). The external matter stress is proportional to the external metric, so the tensor equation reduces to this weighted scalar operator with spin-two AdS mass. In the lift \(W=A+\frac13\log\rho\) and the factors of \(\rho\) in the internal volume cancel between the four-dimensional base and the torus. [Universal warped graviton equation](https://arxiv.org/abs/1103.2800)

Separate a torus Fourier character with bare squared momentum \(\lambda_T\) in AdS units and set \(x=\cos\theta_1\). The lowest tensor profile in that momentum sector is a positive ground state. Simplicity and the background symmetries make it constant on the second sphere and axial and even on the first. Its precise equation is
\[
 -\frac{d}{dx}\!\left[k_1(1-x^2)e^{2B+C}\frac{du}{dx}\right]
 +\lambda_T e^{2D+2B+3C-20A/3}u
 =m_{\rm tensor}^2L^2\, e^{2D+2B+C-16A/3}u .
\]
Pole conditions are regularity at \(x=\pm1\). The Rayleigh quotient is nonnegative for all warps in the ansatz. For nonzero \(\lambda_T\) the minimum of \(e^{2C-4A/3}\) times \(\lambda_T\) bounds it below, and the constant trial profile gives the weighted average of the same quantity times \(\lambda_T\) as an upper bound. The zero-momentum constant mode remains exactly massless.

## The leading change at fixed charge

Write \(A=\epsilon P_2+\epsilon^2 A_2+\cdots\) and \(C=\epsilon^2 C_2+\cdots\). At the resonance \(\langle P_2^2\rangle=1/5\), the integrated external equation gives \(\langle A_2\rangle=28/15\), and the [quadratic metric response](2026-11-16_Tpq_coupled_warp_branch.md) gives \(\langle C_2\rangle=20/9\). The first-order potential minus the first-order norm contribution is \(-4\lambda_T P_2/3\). Its average is zero, and it mixes the constant profile only with the first-sphere quadrupole at this order. The unwarped gap to that harmonic is \(32\) at resonance. At order \(\epsilon^2\), the direct contribution is \(\lambda_T\langle 2C_2-4A_2/3+8P_2^2\rangle\), and the mixing contributes \(- (4\lambda_T/3)^2\langle P_2^2\rangle/32\). Thus, at fixed bounded bare torus momentum,
\[
 m_{\rm tensor}^2L^2-\lambda_T =
 \epsilon^2\left(\frac{32}{9}\lambda_T-\frac{\lambda_T^2}{90}\right)+O(\epsilon^3).
\]
Restoring the Page period rescales the bare momentum parameter relative to the unwarped solution through \(L^4\). The [fixed-Page calculation](2026-11-16_Tpq_warp_central_charge.md) shows that this rescaling starts at cubic order, so it does not affect the displayed coefficient. The verification solves the generalized eigenproblem on the numerical warped profiles at \((7,8),(8,9),(38,43)\), checks the massless mode, and compares \(\lambda_T=1,4,12\) against the second-order formula. These values sample the allowed continuous torus shape and scale parameters. At the closest pair \((38,43)\) the numerical shifts agree with the leading prediction within \(0.12\%\).

## Consequences for the unstable scalar sector

The tensor spectrum and the scalar–Maxwell BF problem have different quadratic operators. For the unwarped solution at the limiting shape \(\eta=1/3\), the physical homogeneous shape mass has BF deficit \(\sqrt{656/9}-8>1/2\), from \(m^2L^2=4-\sqrt{64+320(\eta-1/2)^2}\). The warped backgrounds approach the product coefficients in the circle-invariant gauged fluctuation problem. The order-one deficit therefore persists for sufficiently late near-resonant bundles by continuity in that physical sector. For any isolated mode obtained from a sphere-rotation singlet at fixed torus label, the first-order diagonal warp shift vanishes because the linear deformation is a pure quadrupole. This selection rule alone cannot determine the quadratic shift of the coupled scalar–Maxwell band, particularly near crossings with nonsinglet modes. [Gubser and Mitra](https://arxiv.org/abs/hep-th/0108239)

Reproduce the [certificate](../data/toe_20261116_Tpq_warp_mtheory_lift.json) with `py -3 -B analysis/toe_20261116_Tpq_warp_mtheory_lift.py`.
