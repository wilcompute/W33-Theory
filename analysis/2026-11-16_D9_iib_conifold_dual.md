# Type IIB circle dual of the eleven-dimensional two-sphere flux family

The [eleven-dimensional sibling of the D9 flux model](2026-11-16_D9_mtheory_uplift.md) has internal space \(S^2_1\times S^2_2\times T^2\), horizontal four-form period \(N_0\), and mixed periods \(N_1,N_2\). It has a Type IIB description as the \(T^{p,q}\) Einstein family. This identifies the previously calculated homogeneous instability, accounts for the additional torus-momentum band that lies outside Type IIB supergravity, and gives a classical backreacted planar realization of the marginal torus-wrapped M5 channel. The nine-dimensional Einstein–Maxwell action remains a separate model. [M-theory on a torus and Type IIB on a circle](https://arxiv.org/abs/hep-th/9510086) · [The \(T^{p,q}\) stability analysis](https://arxiv.org/abs/hep-th/0108239)

## Quantized flux becomes circle topology

Reduce on the first M-theory circle. The two mixed \(G_4\) periods become NS three-form periods with a leg on the remaining IIA circle. T-dualize that circle. Fiber integration of the NS flux gives the first Chern class of the new IIB circle,
\[
 c_1(Y)=N_1[\sigma_1]+N_2[\sigma_2],\qquad
 \int_{S_i^2}\sigma_i=1 .
\]
The horizontal eleven-dimensional four-form becomes the IIA RR four-form, then the IIB self-dual five-form with Page period \(N_0\) on \(Y\). We take the duality without additional flat RR or NS backgrounds that would change the Page-charge conventions. The IIB axiodilaton is constant and is the M torus's complex modulus. The relevant metric and five-form solve the two-derivative equations. The use of circle duality on the invariant fields is separate from the identification of nonzero momentum states. [Bouwknegt, Evslin and Mathai, topology and flux under T-duality](https://arxiv.org/abs/hep-th/0306062) · [Duff, Lü and Pope, Hopf-circle duality in AdS](https://arxiv.org/abs/hep-th/9803061)

In Type IIB Einstein frame put \(s=R_f/L\), where \(R_f\) is the physical radius of the fiber coordinate of period \(2\pi\). The metric can be written
\[
 ds_Y^2=r_1^2 d\Omega_1^2+r_2^2 d\Omega_2^2+
         R_f^2\left(d\psi+\tfrac12\sum_i N_i\cos\theta_i\,d\varphi_i\right)^2 ,
\]
with orientations chosen for the displayed Chern numbers. In a local orthonormal frame the connection curvature has magnitudes \(L|b_i|=s|N_i| k_i/2\), \(k_i=L^2/r_i^2\). The transverse Ricci curvatures are \(k_i-(Lb_i)^2/2\); the fiber Ricci curvature is \(\sum_i(Lb_i)^2/2\). With \(k_1=4(1+\eta), k_2=4(2-\eta)\), choose \(s=2\sqrt{8\eta}/(|N_1|k_1)\) when \(N_1\ne0\). The M flux-ratio equation then gives \((Lb_1)^2=8\eta\), \((Lb_2)^2=8(1-\eta)\), and all three IIB Ricci curvatures are 4. Either endpoint can be computed using the nonzero mixed period. This is the IIB Freund–Rubin system with five-form density \(4/L\).

The homotopy sequence of the bundle gives \(\pi_1(Y)=\mathbb Z_g\), \(g=\gcd(|N_1|,|N_2|)\), since the boundary map sends \((a,b)\in\pi_2(S^2\times S^2)\) to \(aN_1+bN_2\). Its generator is the fiber. On the M side, normalize both torus coordinates to period one. A translation by \((a,b)\) shifts flat three-form periods by \(\pm N_i a,\pm N_i b\), as follows by integrating \(G_4\) over the swept chains of \(S_i^2\times S^1\). The translations preserving the fixed differential C-field therefore form \(\mathbb Z_g\times\mathbb Z_g\). Equivalently, the two torus vectors gauge shifts with two Smith factors \(g,g\). This matches the two geometric winding labels of the IIB NS and RR strings on the fiber. It pertains to this flux and axion gauging; a full charge classification with dynamical brane endpoints may involve additional identifications. [Integral circle topology of \(T^{p,q}\)](https://arxiv.org/abs/hep-th/0108239)

## The radius actions agree, including the BF mode

In the IIB metric use logarithmic radius shifts \(\gamma_1,\gamma_2,\gamma_f\) for the two spheres and the fiber. Put \(d=(2,2,1)^{\mathsf T}\) and \(B=d\cdot\gamma\). The Einstein kinetic matrix is \(2\operatorname{diag}(d)+(2/3)dd^{\mathsf T}\). At fixed Chern numbers and five-form period, the scalar potential in AdS units is
\[
 V_{\mathrm{IIB}}=e^{-2B/3}\left[
 -2k_1e^{-2\gamma_1}-2k_2e^{-2\gamma_2}
 +\tfrac12(Lb_1)^2e^{2\gamma_f-4\gamma_1}
 +\tfrac12(Lb_2)^2e^{2\gamma_f-4\gamma_2}
 +8e^{-2B}\right].
\]
The curvature of the circle connection contributes the two positive geometric terms, and the last term is the fixed internal five-form energy including the self-duality prescription. The M radius variables \(\beta_1,\beta_2,\beta_T\), at fixed torus complex structure, map to
\[
 (\gamma_1,\gamma_2,\gamma_f)
   =(\beta_1+\tfrac12\beta_T,\ \beta_2+\tfrac12\beta_T,\ -\tfrac32\beta_T).
\]
The IIB kinetic metric pulls back to \(4I+(8/3)\mathbf1\mathbf1^{\mathsf T}\), and each of the five potential terms pulls back to its M counterpart. This identifies the full homogeneous three-radius action in the two-derivative truncation, including the mass \(32/L^2\) of the IIB breathing mode.

For Gubser and Mitra's parameter \(\Lambda=4/k_1=1/(1+\eta)\), the splitting squared of the two traceless singlet metric masses is \(16(49-60/\Lambda+20/\Lambda^2)=64+320(\eta-\tfrac12)^2\), where the splitting is measured from the common value \(4\). The M radion below the BF bound at unequal flux is exactly the IIB \(T^{p,q}\) instability. At equal flux its log-radius eigenvector expands one sphere and contracts the other at fixed fiber radius, as in the Type IIB analysis. On the unquotiented supersymmetric conifold branch this is the \(\Delta=2\) mode associated with the baryonic current multiplet. That interpretation is available in the supersymmetric IIB description and does not rely on isolated higher-curvature terms in eleven dimensions. [Gubser and Mitra, spectrum and operator map](https://arxiv.org/abs/hep-th/0108239) · [Klebanov and Witten, conifold field theory](https://arxiv.org/abs/hep-th/9807080)

## Equal flux and the quotient spin lift

At \(|N_1|=|N_2|=N\) the normalized radii are \(k_i=6\), \(s=2/(3N)\), and \(Y=T^{1,1}/\mathbb Z_N\) with the quotient along the usual fiber. The period of the standard coordinate \(\psi_{\rm std}\) is \(4\pi/N\). For the unquotiented conifold the holomorphic three-form transforms by \(e^{i\delta\psi_{\rm std}}\), and the two conjugate Killing-spinor phases are \(e^{\pm i\delta\psi_{\rm std}/2}\). On the quotient the ordinary generator lift acts by \(e^{\pm2\pi i/N}\). A second lift is possible for even \(N\), and multiplies those phases by \(-1\). Therefore \(N=1\) has invariant spinors with the ordinary lift, and \(N=2\) has them with the alternative lift. For \(N>2\) neither allowed lift fixes the cover's Killing spinors. In cone coordinates the \(N=2\) action sends all four conifold coordinates to their negatives and preserves the residue holomorphic volume form. This agrees with the supersymmetric Type IIB \(T^{1,1}/\mathbb Z_2\) geometry in the literature. It specifies the available IIB spin choices, without choosing which global fermion and winding projection matches every M starting spin structure. The local eleven-dimensional product has no Killing spinors. [Gauntlett, Martelli, Sparks and Waldram, the supersymmetric \(T^{1,1}/\mathbb Z_2\) solution](https://arxiv.org/abs/hep-th/0402153) · [Wulff, eleven-dimensional supersymmetry classification](https://arxiv.org/abs/1611.06139)

Two normalizations provide checks. For \(Y_{\rm unit}\) with \(\operatorname{Ric}=4g\), the normalized volume is \(32\pi^3 s/(k_1k_2)\), or \(16\pi^3/(27N)\) at equal flux. Five-form quantization gives \(L_{\rm string}^4/\alpha'^2=4\pi^4 g_s|N_0|/\operatorname{Vol}(Y_{\rm unit})\). The leading Weyl anomaly calculated gravitationally on either side is
\[
 a=c=\frac{\pi^3 N_0^2}{4\operatorname{Vol}(Y_{\rm unit})}
     =\frac{27}{64}N N_0^2\quad\text{at equal flux}.
\]
On the M side this follows from \(\pi L^3\operatorname{Vol}(S^2\times S^2\times T^2)/(8G_{11})\) and the three quantized periods. At \(N=1\) it is the leading Klebanov–Witten value. [Gubser, the \(T^{1,1}\) holographic central charge](https://arxiv.org/abs/hep-th/9807164)

## The finite-momentum instability lies in a winding sector

A pair of M torus momentum integers becomes IIB \((u,v)\) string winding on the fiber. From the constant-axiodilaton string tension and the fiber circumference, the squared bare winding mass in AdS units at equal flux is
\[
  \lambda=(m_{\mathrm{wind}} L)^2
   =\frac{3\pi|N_0|}{N}\frac{|u+v\tau|^2}{\operatorname{Im}\tau}.
\]
It is the same torus lattice eigenvalue that entered the eleven-dimensional mixing between the radius difference and the Maxwell field. The derived instability at \(0<\lambda<12\) involves the mixed modes, with masses \(\lambda-2\pm\sqrt{4+16\lambda}\) in AdS units. The tension times length determines the bare scale; the two-derivative IIB point-field spectrum omits these winding excitations. In particular if \(N,N_0\) grow together at fixed ratio and fixed \(\tau\), the local IIB curvature radius grows in string units but \(R_f/\sqrt{\alpha'}\) shrinks as \(N^{-1/2}\). This separates the regimes behind the preceding IIB supergravity and eleven-dimensional stability statements. For \(N=1\) at large \(N_0\) and fixed shape the winding scale instead grows, and the supersymmetric IIB frame is controlled at weak string coupling. [Schwarz, the torus momentum and string winding charge map](https://arxiv.org/abs/hep-th/9601077)

## A backreacted planar realization of the marginal M5 channel

An M5 wrapping the original torus maps to a D3 wall in Type IIB. A classical planar solution with an internal-angle-independent D3 shell is available on the Ricci-flat cone over any of the \(Y_{\rm unit}\) above. In standard D3 variables the transverse unwarped cone metric is \(dr^2+r^2ds_Y^2\), and the warp factor satisfies \((r^5 H')'=0\) off the shell. With fixed exterior and interior D3 charges \(Q_+>Q_->0\), take
\[
 H_+(r)=Q_+/r^4,\qquad H_-(r)=Q_-/r^4+(Q_+-Q_-)/R^4 .
\]
These join continuously at any \(r=R\). The jump of \(r^5 H'\) is \(-4(Q_+-Q_-)\), precisely the charge of a positive smeared D3 shell in this convention. The ten-dimensional metric and self-dual form are the standard warped D3 solution. The inner region approaches the smaller-charge AdS throat as \(r\to0\). Thus the radial location is a free parameter of a backreacted planar solution at the classical order.

The same matching is visible in five-dimensional Einstein frame with a universal logarithmic breathing mode \(b\), \(G_{bb}=80/3\). For internal five-form density parameter \(Q\) at a reference volume, the potential \(-20e^{-16b/3}+Q^2 e^{-40b/3}/2\) is reproduced by \(V=(3/160)(\partial_b W)^2-W^2/3\) with \(W=10e^{-8b/3}-Qe^{-20b/3}\). On either harmonic branch \(b=\log(rH^{1/4})\), the five-dimensional warp logarithm is \(A=5b/3-\log H/4\), and its proper radial derivative is \(A'=W/6\). The scalar obeys \(b'=-G_{bb}^{-1}\partial_b W\), with \(Q=4Q_\pm\) in these reference units. The D3 jump has \(2\kappa_5^2 T=\Delta Q e^{-20b/3}=-[W]\) by charge and tension equality and reduction on \(Y\). It therefore satisfies both \([A']=-\kappa_5^2T/3\) and \([b']=2\kappa_5^2 G_{bb}^{-1}\partial_b T\). The result addresses the sourceful planar problem, with angular smearing and fixed fiber topology. It does not compute a finite-radius Euclidean bounce, a localized nonsymmetric wall spectrum, or quantum lifting of the force. [D3 distributions and harmonic warp factors](https://arxiv.org/abs/hep-th/9811120) · [Wrapped M5 bubbles in AdS5](https://arxiv.org/abs/2610.08939)

The [parallel Gysin audit](2026-11-16_sevenfront_IIB_topology_W33_ancilla_F8_photonic.md) independently checks the circle, spin, and winding normalizations and identifies the harmonic three-form for the Betti vector. The [circle-bundle cup-ring calculation](2026-11-16_circle_bundle_ring_winding_staircase.md) adds exact topological discriminants and counts the unstable winding labels. The [verifier here](toe_20261116_D9_iib_conifold_dual.py) checks the Ricci, charge and central charge normalizations, the homogeneous action and curvature-eigenvalue conversion, the Smith factors and allowed spin lifts, the winding mass factor, and the planar wall and breathing potential identities. See the [generated certificate](../data/toe_20261116_D9_iib_conifold_dual.json).
