# Mixed metric–Maxwell vectors and first mixed scalars in the D9 flux background

The repo's [quantized magnetic branch](2026-11-14_nextfive_flux_cursor_frame_optical_results.md) is the classical \(R-F_{MN}F^{MN}/4\) theory on \(\mathrm{AdS}_5(L)\times S^2(r_1)\times S^2(r_2)\). Write \(k_i=L^2/r_i^2\) and use \(\kappa=4\) for the magnitude of the external Ricci curvature in AdS units. The background equations give \(k_1+k_2=20\) and \(L^2 f_i^2=2(k_i+\kappa)\), where \(F_i=f_i\,\mathrm{vol}_{S^2_i}\). We compute the complete physical spin-one sector and both scalar parity sectors at the first mixed harmonic. All squared masses below are in units \(L^{-2}\). The underlying action and magnetic ansatz match the \(p=5,q=2,N=2,\Lambda=0\) case of the product-manifold analysis. [Brown and Dahlen](https://arxiv.org/abs/1310.6360)

## Complete physical vector blocks

For a normalized product scalar harmonic \(Y=Y_1Y_2\), put \(\lambda_i=k_i\ell_i(\ell_i+1)\) and \(\lambda=\lambda_1+\lambda_2\). Use the [product Hodge decomposition](2026-11-15_nextfive_W33_fourcopy_genus_D9_F8_photonic.md). For each active sphere there is one normalized metric one-form proportional to \((*_i dY_i)Y_j\). With both spheres active there is also one relative gradient, the linear combination of \((dY_1)Y_2\) and \(Y_1dY_2\) orthogonal to \(dY\). These span the co-closed internal one-forms. The total gradient belongs to the massive spin-two Stückelberg system. The independent transverse Maxwell vector is the coefficient of the single scalar \(Y\) in \(A_\mu\). Terms containing external gradients can shift longitudinal Stückelberg fields and drop out of these transverse vector equations.

For metric vector profiles \(v\), the Einstein contribution to the mass quadratic form is \(\frac12\|\mathcal L_v g\|^2=\langle v,(\Delta_H-2\mathrm{Ric})v\rangle\) after choosing orthonormal profiles with positive canonical kinetic terms. The equality follows by integration by parts using the co-closed condition. The horizontal mixed Maxwell field strength contributes the square of \(dY\) times the transverse Maxwell vector plus \(\iota_vF\) times the metric vector. On each factor \(\iota_vF\) is \(f_i\) times a rotation of \(v\), so the metric diagonal after adding the magnetic term is \(\lambda-2k_i+L^2 f_i^2=\lambda+2\kappa\). The same diagonal applies to the normalized relative gradient. Its mixing with \(dY\) vanishes by exact–coexact orthogonality on each sphere. The two coexact directions instead mix with the single Maxwell vector with squared entries \(b_i^2=2(k_i+\kappa)\lambda_i\). Orientation choices can make the \(b_i\) nonnegative.

Consequently for \(\ell_1,\ell_2>0\) the physical symmetric block in order (Maxwell, coexact 1, coexact 2, relative gradient) is
\[
 \begin{pmatrix}
 \lambda&b_1&b_2&0\\
 b_1&\lambda+2\kappa&0&0\\
 b_2&0&\lambda+2\kappa&0\\
 0&0&0&\lambda+2\kappa
 \end{pmatrix}.
\]
For just one active sphere there is a two-by-two block, and at \((0,0)\) only the massless Maxwell vector remains. Thus the two mixed eigenvalues at every nonconstant harmonic are
\[
  \lambda+\kappa\ \pm\sqrt{\kappa^2+2\sum_i(k_i+\kappa)\lambda_i}.
\]
There are two further eigenvalues \(\lambda+2\kappa\) when both spheres are active. All carry harmonic multiplicity \((2\ell_1+1)(2\ell_2+1)\). In particular the two single-sphere mixing problems share one \(A_\mu\) when both spheres are excited.

The product of the two mixed eigenvalues is
\[
 \lambda^2-2\sum_i k_i\lambda_i
 =\lambda_1(\lambda_1-2k_1)+\lambda_2(\lambda_2-2k_2)+2\lambda_1\lambda_2.
\]
Each term is nonnegative for spherical harmonics. It vanishes precisely at \((1,0)\) and \((0,1)\) among nonconstant modes. In those blocks the null direction is \((-\sqrt{2(k_i+\kappa)},\sqrt{2k_i})\), the canonical realization of the [magnetic moment-map compensator](2026-11-15_nextfive_270mode_affine24_D9_F8_drift.md). The three rotations per sphere and the constant Maxwell harmonic give exactly seven massless vectors. These are physical modes after the gauge constraint, with positive transverse kinetic terms. All the other vector masses are strictly positive.

## The light vector gap switches angular representation

Let \(k=\min(k_1,k_2)\in(0,10]\) and \(\ell_{\rm loose}\) label the larger sphere. For a fixed active set the lower branch increases with each excited \(\lambda_i\), since the square root in that branch exceeds \(k_i+\kappa\). After removing the Killing modes, the first positive squared mass is the minimum of
\[
 \begin{split}
 V_{20}(k)&=6k+4-\sqrt{16+12k(k+4)},\\
 V_{11}(k)&=44-\sqrt{1936-8k(20-k)} .
 \end{split}
\]
These come from \((\ell_{\rm loose},\ell_{\rm tight})=(2,0)\) and \((1,1)\). The massive partner of a single-sphere Killing mode exceeds that sphere's \(\ell=2\) lower branch. The additional mixed eigenvalues exceed the mixed lower branch. Each candidate increases with \(k\), so the largest attainable first gap is \(44-4\sqrt{71}\) at equal radii.

The crossing is at the unique root in \((2,2.1)\) of \(k^3+44k^2-480k+800=0\). This follows by eliminating the common eigenvalue from the two quadratics. On \((0,5)\) the cubic decreases and then increases at most once and has one root there, with its value at \(5\) still negative. For \(k\ge5\), \(V_{20}(5)>V_{11}(10)\), excluding a lower-branch crossing there. The ratio of magnetic flux integers on the larger and smaller spheres in absolute value is
\[
 \rho=\frac{20-k}{k}\sqrt{\frac{k+4}{24-k}} .
\]
The transition occurs at \(\rho\simeq4.5\). The cubic is irreducible modulo 13. At its root the numerator and denominator of \(\rho^2\) reduce to \(800+720k-80k^2\) and \(800-480k+68k^2\). They are not rational multiples, so the equality is unavailable for integer fluxes. Actual quantized branches select one of the two harmonic representations.

In the large-\(\rho\) limit \(k\sim20/(\sqrt6\,\rho)\). The first vector gap is \(V_{20}\sim3k^2\sim200/\rho^2\), while the first spin-two squared mass is \(2k\), as follows from the [spin-two tower](2026-11-14_late_fivefronts_exact_geometry_locality_and_photon_report.md). More generally each fixed \(\ell_{\rm loose}\ge2\) has lower-branch mass \(\ell(\ell+1)[\ell(\ell+1)-2]k^2/8+O(k^3)\). For any fixed budget \(B>0\) on \(m^2L^2\) the number of loose-sphere lower-branch vector fields with \(\ell\ge2\) below that budget is asymptotic to \((B+\sqrt{8B})/k\), including the harmonic multiplicity. This follows by solving the exact inequality for \(\lambda\) and summing \(2\ell+1\). The vector sector therefore gives an explicit additional obstruction to isolating a finite light spectrum by extreme flux anisotropy.

## First mixed even scalars from trace-reversed Einstein equations

The \((\ell_1,\ell_2)=(1,1)\) even scalar block can be calculated directly in addition to the vectors. Even here refers to simultaneous antipodal transformations on the spheres combined with Maxwell charge conjugation, which preserves the background. The internal traceless Hessians vanish on \(\ell=1\). Use scalar diffeomorphisms to remove the external Hessian and the two external–internal scalar shifts. Write the remaining external trace perturbation as \(H g_{\mu\nu}\), internal traces as \(U_i g_i\), cross metric profiles as \(C\,dY_1\,dY_2 +D(*_1dY_1)(*_2dY_2)\), and Maxwell internal profiles as \(b_i(*_i dY_i)Y_j\). All include a common AdS scalar profile. The trace profiles also include \(Y_1Y_2\). Use AdS units here, and write \(F_i=f_i^2=2(k_i+\kappa)\).

The traceless external Einstein equation sets \(H=-2(U_1+U_2)/3\). The external–internal constraints set \(s_i=f_i b_i=H-U_i+\lambda_j C\), \(j\ne i\). With \(P=\sum_i(\lambda_i s_i-F_i U_i)\), the external trace checks \((m-\lambda-2\kappa)H=2P/7\), where \(m\) denotes the squared mass in AdS units. It follows from the internal trace equations. For the four dynamical amplitudes use \(D'=f_1f_2D\). The trace and two cross projections give
\[
 \begin{split}
 m U_i&=(48+F_i)U_i-\lambda_i s_i+\tfrac{2}{7}P,\\
 m C&=48C+D',\\
 m D'&=48D'+F_1s_2+F_2s_1+F_1F_2C .
 \end{split}
\]
These follow from \(\delta R_{MN}=\tfrac12(-\nabla^2 h_{MN}-2R_{MPNQ}h^{PQ}+R_{MP}h^P{}_N+R_{NP}h^P{}_M+\nabla_M B_N+\nabla_N B_M)\), with \(B_N=\nabla^P h_{PN}-\tfrac12\nabla_N\operatorname{tr}h\). In the chosen gauge the internal divergence coefficient on \(dY_i\,Y_j\) is \(-s_i\). The cross term in the trace-reversed Maxwell stress maps the gradient–gradient metric profile into the coexact–coexact profile and conversely. Direct projection of the internal Maxwell equations gives \((m-\lambda-F_i)s_i+F_iU_i-\lambda_jD'=0\), which the Einstein block satisfies identically. In particular the coexact–coexact metric perturbation sources the Maxwell equation on factor 2 through \(-f_1\lambda_1D\,Y_1(*_2dY_2)\), so it participates in the coupled spectrum. The external Maxwell scalar equation is odd under the combined parity.

With \(p=k_1k_2\), the characteristic polynomial is
\[
 (m-96)\left[m^3-176m^2+
         \frac{45760+108p}{7}m-544p\right].
\]
The cubic roots lie in \((0,16),(16,80),(96,128)\) for \(0<p\le100\), by sign tests at the endpoints, which are affine in \(p\). Thus none approaches the AdS scalar Breitenlohner–Freedman bound \(-4\) in this branch. Each eigenvalue has harmonic multiplicity nine. At equal radii the four even masses squared are approximately \(8.09409,\ 65.86583,\ 96,\ 102.04008\).

## Odd scalar at the same harmonic

For odd parity the internal metric has cross amplitudes \(J_1(*_1dY_1)dY_2\) and \(J_2dY_1(*_2dY_2)\), while the Maxwell internal profiles have amplitudes \(a_i dY_iY_j\). The two internal coexact diffeomorphisms remove the scalar external–internal shifts. The Maxwell scalar gauge sets the external longitudinal potential to zero. The external–internal Einstein constraints then give \(f_i a_i=-\lambda_j J_i\), and the external Maxwell equation imposes \(\lambda_1a_1+\lambda_2a_2=0\). The remaining line can be parametrized by \(J_1=f_1 A,\ J_2=-f_2 A,\ a_1=-\lambda_2 A,\ a_2=\lambda_1 A\).

The first cross Einstein equation is \((\lambda_1-m)J_1=f_1(a_1-a_2)+f_1f_2J_2-2\kappa J_1\). The second is its exchanged version with the Maxwell curl sign reversed. They give the same \(m=2\lambda+4\kappa=96\). Direct internal Maxwell projection also gives \(m=\lambda+F_1+F_2=96\). Thus the entire \((1,1)\) scalar spectrum has five polarizations per harmonic, with \(96\) occurring in both parity sectors. The sign proof and both Maxwell checks use the whole positive-radius branch. The general product-manifold stability result covers the other angular sectors of this classical model. An independent model-specific diagonalization of those scalar blocks, boundary-condition variants, and higher-derivative or quantum corrections are separate from these certificates. [Brown and Dahlen, scalar analysis and stability table](https://arxiv.org/abs/1310.6360)

Run the [verifier](toe_20261116_D9_mixed_vector_spectrum.py) to regenerate the [certificate](../data/toe_20261116_D9_mixed_vector_spectrum.json). It checks vector multiplicities and null directions, the continuous and quantized gap crossover, the anisotropic tower count, and the scalar characteristic polynomial.
