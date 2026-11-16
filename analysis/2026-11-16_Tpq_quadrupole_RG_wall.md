# Matched quadrupole domain wall near the Type IIB warp resonance

The [coupled \(T^{p,q}\) branch](2026-11-16_Tpq_coupled_warp_branch.md) and its [fixed-Page anomaly](2026-11-16_Tpq_warp_central_charge.md) supply two independent physical matching conditions for the leading five-dimensional axial scalar description. Together they fix its kinetic normalization in the quadrupole coordinate and give a slow planar AdS domain wall. The wall is exact in the explicit matched five-dimensional model below. A ten-dimensional interpolation would require solving the radial dependence of the Kaluza–Klein tower and its constraint fields.

## Normalize the light mode by two observables

Use the unwarped AdS radius for units. Let \(x\) denote the coefficient of \(P_2\) in the warp \(A\), \(t=32-\lambda_{2,0}\), and \(c_2=256/3\). The ten-dimensional static projected equation begins with \(F(x)=t x-c_2 x^2\), and the physical unwarped mass is
\[
 m^2 L^2=\lambda+16-8\sqrt{\lambda+4}=-t/3+O(t^2).
\]
In a smooth local five-dimensional Einstein-frame description of this light scalar with constant leading kinetic coefficient \(K\), matching the static equation and mass fixes \(V'(x)/K=-F(x)/3\) to quadratic order in the small detuning and amplitude. The proportionality at the degenerate point is determined by the unwarped derivative, so changes in a smooth matching factor affect only higher orders. This uses the isolated light mode in the axial pure-five-form sector and integrates out the other fields there in a derivative expansion. [Metric and five-form mass spectrum, Eq. (18)](https://arxiv.org/abs/hep-th/0108239)

The potential difference between \(x=0\) and \(x=t/c_2+O(t^2)\) is \(-K t^3/(18c_2^2)+O(t^4)\). In the same five-dimensional Einstein frame, \(a\propto(-V)^{-3/2}\) at a stationary point, so the anomaly shift near \(V=-12\) is \(\delta a/a=\delta V/8\). Matching the independent ten-dimensional result \(-t^3/65536\) at fixed Page charge yields \(K=16\) at resonance. Thus the canonical linear coordinate in this matching is \(\phi=4x\). This determines the leading coefficient, without a claim to have derived derivative interactions of the complete ten-dimensional fluctuation action. [Holographic Weyl anomaly](https://arxiv.org/abs/hep-th/9806087)

Within the same leading matching, multiplying the earlier static spin-two slopes by \(-1/3\) gives physical mass predictions \(m_{\mathrm{axial}}^2 L^2=t/3+O(t^2)\) and \(m_{\mathrm{biaxial}}^2 L^2=-t+O(t^2)\) at the warped point, with the biaxial pair degenerate. The two neutral static variations correspond to rotating the internal solution. The matching fixes the small masses of this multiplet and leaves the vector mixing and the known independent below-BF shape mode outside its scope.

## Explicit wall in the matched action

For the action \(R-(K/2)(\partial x)^2-V\), let the planar metric be \(dr^2+e^{2B(r)}dx_{1,3}^2\) and choose the model
\[
 W(x)=6+K\left(\frac{t x^2}{24}-\frac{c_2 x^3}{36}\right),
 \qquad V=\frac{W_x^2}{2K}-\frac{W^2}{3}.
\]
This reproduces the matched quadratic force in \((t,x)\), with subleading terms beyond the matching fixed by this model choice. The first-order equations \(B'=W/6,\ x'=-W_x/K\) obey all planar Einstein–scalar equations. In canonical coordinates \(W=6+t\phi^2/24-16\phi^3/27\). [Freedman, Gubser, Pilch and Warner, holographic domain walls](https://arxiv.org/abs/hep-th/9904017)

In terms of \(u=c_2 x/t\), the exact model profile is
\[
 u(r)=\frac{1}{1+\exp[t(r-r_0)/12]},\qquad
 B'(r)=1+\frac{K t^3}{432c_2^2}(3u^2-2u^3).
\]
Increasing \(r\) points toward the ultraviolet. For \(t>0\) the wall runs from an unwarped UV to a warped IR, and for \(t<0\) the UV and IR exchange roles. The holographic \(a\)-function is proportional to \(B'^{-3}\) and increases with \(r\), since \(B''=-Kx'^2/6\). The exact model endpoint ratio \(a_{\rm warp}/a_{\rm FR}=(1+t^3/196608)^{-3}\) reproduces the physical cubic term. At leading order the 10–90 percent width in log energy is \(24\log(9)/|t|\), growing as \(p^2\) along each primitive Pell family. This makes the small anomaly shift and the large separation in radial scale consequences of the same detuning.

The leading spin-two flow is \(Q'=-(tQ-2c_2(Q^2)_0)/12\), where \(Q=x\,\operatorname{diag}(-1/2,-1/2,1)\) is the axial orbit. Linearizing along the wall gives axial, rotational, and biaxial transfer factors proportional to \(u(1-u)\), \(u\), and \(u/(1-u)^3\), respectively. The axial solution is the translation of the wall. On the \(t>0\) side the warped IR is repulsive in the biaxial sector of this leading flow, so reaching it requires axial symmetry or tuning of the corresponding perturbations. These transfer factors solve the leading first-order flow and are not boundary Green functions of the ten-dimensional background.

The model uses a fixed Page sector and matches both endpoint observables at their controlled orders. Existence of the planar wall in this five-dimensional model leaves open whether a regular ten-dimensional wall with these endpoints exists, and whether solutions that reach them are stable in other sectors.

Reproduce the [certificate](../data/toe_20261116_Tpq_quadrupole_RG_wall.json) with `py -3 -B analysis/toe_20261116_Tpq_quadrupole_RG_wall.py`.
