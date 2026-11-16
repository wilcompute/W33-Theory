# The D9 flux background and its invariant eleven-dimensional alternatives

The [D9 Einstein–Maxwell calculation](2026-11-16_D9_all_scalar_harmonics.md) assumes a nine-dimensional metric and one Maxwell field. It has positive physical scalar squared masses for its whole magnetic branch. Here we test a source-free, two-derivative eleven-dimensional embedding allowing the two extra dimensions to be a principal \(T^2\) bundle and allowing every invariant internal four-form component in that ansatz. The D9 geometry fails the test. The related untwisted M-theory solution is already in the symmetric-space classification. Its quantized branch has a homogeneous instability at unequal flux and an additional torus-momentum instability in part of its equal-flux locus. [Wulff, solution 9 and Eq. 2.52](https://arxiv.org/abs/1611.06139)

## Torus twisting cannot hold the D9 fields fixed

Preserve the full external \(\mathrm{AdS}_5\) and base round-sphere isometries. Work with constant torus metric and orthonormal vertical forms \(e^1,e^2\); put \(\omega_i=\mathrm{vol}_{S_i^2}\). The geometric flux is \(de^a=g_1^a\omega_1+g_2^a\omega_2\) for two real two-component columns \(g_i\). Symmetry allows
\[
 G_4=u\,\omega_1\wedge\omega_2+
        (p\,\omega_1+q\,\omega_2)\wedge e^1\wedge e^2 .
\]
There is no invariant one-form on the base spheres, and a four-form cannot use an invariant volume form on the five-dimensional AdS factor. The Bianchi identity gives \(p g_2+q g_1=0\). The dual field strength is, up to overall orientation,
\[
 *G_4=\mathrm{vol}_{\mathrm{AdS}_5}
       \wedge(u\,e^1\wedge e^2+p\,\omega_2+q\,\omega_1).
\]
The Chern–Simons source \(G_4\wedge G_4\) vanishes on the six-dimensional internal space. If \(u\ne0\), \(d*G_4=0\) forces both \(g_i=0\). If \(u=0\), AdS requires at least one of \(p,q\) nonzero. The Bianchi identity then bounds the rank of the matrix with columns \(g_i\) by one. The vertical Ricci block for a constant flat fiber is \((g_1g_1^{\mathsf T}+g_2g_2^{\mathsf T})/2\), as follows from the connection metric. The four-form stress on the fiber is isotropic, so the vertical Ricci block must also be isotropic. A positive semidefinite rank-at-most-one isotropic matrix in dimension two vanishes. Thus the geometric flux vanishes in this case as well.

The base is simply connected, so a flat principal torus connection in this ansatz has no residual twisting. With product metric, write \(\mathcal S=u^2+p^2+q^2\). The eleven-dimensional Einstein equation gives
\[
 -4/L^2=-\mathcal S/6,\qquad
 0=(p^2+q^2)/2-\mathcal S/6,\qquad
 r_1^{-2}=(u^2+p^2)/2-\mathcal S/6,\quad
 r_2^{-2}=(u^2+q^2)/2-\mathcal S/6 .
\]
Consequently
\[
 L^2u^2=16,\qquad L^2(p^2+q^2)=8,\qquad
 L^2(r_1^{-2}+r_2^{-2})=12 .
\]
The corresponding D9 curvature sum is \(20\), a dimensionless mismatch unchanged by a constant frame rescaling. A pure two-form Maxwell flux descending from \(G_4\) with two torus legs sources the torus radius, and the missing horizontal four-form is compulsory. This obstruction concerns a constant-modulus source-free invariant torus uplift with the stated symmetry. Other internal geometries, warping with reduced symmetry and added sources are outside the ansatz. [Symmetric eleven-dimensional field equations and product solutions](https://arxiv.org/abs/1611.06139)

## Quantization and the accessible radii

Let \(\eta=p^2/(p^2+q^2)\), \(k_i=L^2/r_i^2\), and let \(\mathcal A\) be the flat torus area. The solution has \(k_1=4(1+\eta)\) and \(k_2=4(2-\eta)\); therefore \(1/2\le r_1^2/r_2^2\le2\). Let \(N_0,N_1,N_2\) be the four-form periods in units \((2\pi\ell_p)^3\) on \(S_1^2\times S_2^2,\ S_1^2\times T^2,\ S_2^2\times T^2\). The gravitational shift vanishes on this product because its internal first Pontryagin class is zero. For two nonzero mixed fluxes,
\[
 \left|\frac{N_1}{N_2}\right|=
 \sqrt{\frac{\eta}{1-\eta}}\,\frac{2-\eta}{1+\eta},\quad
 (L/\ell_p)^3=\frac{\pi}{8}|N_0|\,k_1k_2,\quad
 \frac{\mathcal A}{\ell_p^2}=
  \frac{2\pi^2|N_1| k_1}{\sqrt{8\eta}(L/\ell_p)} .
\]
The first function is strictly increasing from zero to infinity. Its logarithmic derivative has numerator \(5\eta^2-5\eta+2>0\) over the common positive denominator. A vanishing mixed flux gives the corresponding endpoint. These relations fix the scale, shape ratio of the spheres and torus area, while the torus complex structure remains free at this order. The horizontal period \(N_0\) cannot vanish. Multiplying all three periods by the same large integer preserves the mass eigenvalues in AdS units and makes all compact lengths and \(L\) large in Planck units at fixed torus shape. [Witten, M-theory flux quantization](https://arxiv.org/abs/hep-th/9609122)

## A homogeneous BF violation at every unequal ratio

At fixed periods vary the three logarithmic lengths \(\beta_1,\beta_2,\beta_T\). In five-dimensional Einstein frame, normalized to the background, the kinetic matrix in the convention \(-G_{ij}\partial\beta_i\partial\beta_j/2\) is \(G=4I+(8/3)\mathbf 1\mathbf 1^{\mathsf T}\). In AdS units the potential is
\[
 V=e^{-4(\beta_1+\beta_2+\beta_T)/3}
 \left[-2 k_1 e^{-2\beta_1}-2k_2 e^{-2\beta_2}
 +8e^{-4(\beta_1+\beta_2)}
 +4\eta e^{-4(\beta_1+\beta_T)}
 +4(1-\eta)e^{-4(\beta_2+\beta_T)}\right].
\]
The product volume-form ansatz solves the four-form equation for spacetime-dependent radii as well: the dual has all five external legs and \(G_4\wedge G_4=0\). The homogeneous radii therefore yield physical solutions of the linearized eleven-dimensional system. At the displayed vacuum \(V=-12\) and \(dV=0\). The eigenvalues of \(G^{-1}\mathrm{Hess}(V)\) are
\[
 32,\qquad 4\pm\sqrt{64+320(\eta-\tfrac12)^2}.
\]
The lower value is strictly below the AdS5 Breitenlohner–Freedman bound \(-4\) whenever \(|N_1|\ne|N_2|\), including the single-mixed-flux endpoints. The equal branch has \(m^2L^2=-4,12,32\), and its lowest mode is the sphere-size difference. These radius modes already disqualify the unequal-flux sibling as a perturbatively stable vacuum. The positive-mass spectrum of the nine-dimensional Einstein–Maxwell model belongs to a different action. [Breitenlohner and Freedman, AdS stability](https://www.sciencedirect.com/science/article/pii/0003491682901166)

## Equal flux still has an instability at nonzero torus momentum

For equal absolute flux choose orientations with \(p=q\). Reflections combined with the eleven-dimensional parity action on the four-form relate sign choices. Reduce on the two round spheres while keeping dependence on both torus coordinates. In the sphere-exchange odd sector, \(v=(\beta_1-\beta_2)/2\) mixes with a seven-dimensional odd Maxwell field from \(C_3\) on the difference of the sphere volume forms. The metric on \(\mathrm{AdS}_5\times T^2\) and the seven-dimensional three-form are even. They have no linear source in this sector. In particular the Chern–Simons source involving \(F_1\wedge F_2\) has no odd term about \(F_1=F_2\).

In units \(L=1\) set \(\phi=\sqrt8\,v\), \(F_b=2\,\mathrm{vol}_{T^2}\), and \(F_{1,2}=F_b\pm\delta F/\sqrt2\). The two kinetic terms are \(-[e^{-4v}F_1^2+e^{4v}F_2^2]/4\). Together with the curvature term \(24\cosh(2v)\) and the canonical kinetic term they give at quadratic order
\[
 \mathcal L^{(2)}=-\tfrac12(\partial\phi)^2+2\phi^2
                 -\tfrac14(\delta F)^2+\phi\,F_b^{MN}\delta F_{MN}.
\]
For a nonzero torus momentum with \(\lambda=L^2|k_T|^2\), the internal Maxwell component transverse to \(k_T\) is a physical AdS scalar. A sine/cosine choice gives its real mixing entry \(4\sqrt\lambda\) with \(\phi\). Its longitudinal partner and the external Maxwell vector have no source from this transverse subsystem. The two scalar masses are
\[
 m_\pm^2L^2=\lambda-2\pm\sqrt{4+16\lambda}.
\]
The lower mass is below \(-4\) precisely for \(0<\lambda<12\). Its minimum as a function of continuous \(\lambda\) is \(-25/4\) at \(\lambda=15/4\). For a square torus, write \(N=|N_1|=|N_2|\). Quantization gives \(\mathcal A/L^2=(4\pi/3)N/|N_0|\), so \(\lambda_1=3\pi|N_0|/N\). Hence the equal-flux square torus is unstable in this channel for \(N/|N_0|>\pi/4\). For a general shape the criterion is that its first positive scalar torus eigenvalue in AdS units be below 12. At fixed area the hexagonal lattice maximizes this eigenvalue, with normalized shortest squared length \(2/\sqrt3\). Therefore \(N/|N_0|>\pi/(2\sqrt3)\) forces an instability for every flat shape. Small-area tori can evade this particular band; the other eleven-dimensional sectors remain to be checked. The lattice bound follows by extending a shortest vector to a basis and reducing the other basis vector's projection to at most half the shortest length. The area is then at least \(\sqrt3/2\) times the shortest squared length, with equality for the hexagonal lattice.

The shape criterion can also be written in terms of the [repo's reduced modular height](2026-11-16_irrational_axion_towers.md). For torus complex structure \(\tau\), the shortest squared length of the covolume-one momentum lattice is \(1/h(\tau)\). In two dimensions its dual differs by a quarter turn, so the same invariant applies whether one starts from periods or momenta. The equal-flux band is absent precisely for \(h(\tau)\le\pi|N_0|/(4N)\). At every nonzero \(N/|N_0|\) this excludes the modular cusp of sufficiently elongated tori, even when a square torus of the same area passes.

## A marginal M5 probe channel

For an unfluxed M5 probe spanning four external directions and wrapping an internal two-cycle, the internal coupling in the dual seven-form is \(\alpha=u\,\mathrm{vol}_{T^2}+p\,\omega_2+q\,\omega_1\). Its comass, the maximum on an oriented unit tangent two-plane, is \(\max(|u|,|p|,|q|)=4/L\). This bounds the pullback to every such cycle by \(4/L\) times its area. A spherical wall in Euclidean AdS5 has a probe extremum at \(4\coth\chi = L|\int\alpha|/\mathrm{Area}\) in units of its wrapped M5 tension. The right side is at most four, with equality for a torus wrapping. Thus this channel is exactly marginal at the planar limit and gives no finite-radius probe bounce. Wrapped spheres are strictly subcritical. Backreacted walls with changing periods, more general worldvolume fluxes, and quantum corrections are beyond this probe test. [Menet, Tomasiello and Van Hemelryck, wrapped M5 bubbles](https://arxiv.org/abs/2610.08939)

The [verifier](toe_20261116_D9_mtheory_uplift.py) checks the background equations, fixed-flux Hessian, equal-flux Maxwell mixing and BF band, and quantized size conditions. The [certificate](../data/toe_20261116_D9_mtheory_uplift.json) records the exact identities and sample torus controls.
