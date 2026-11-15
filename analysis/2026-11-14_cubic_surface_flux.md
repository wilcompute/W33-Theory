# A non-product D9 magnetic vacuum on a cubic surface

Take source-free Einstein–Maxwell with action \(R-F^2/4\) in \(D=d+2N\), with no bare cosmological term. Let the compact internal factor be a positive Kähler–Einstein manifold \(M\) of complex dimension \(N\), with \(\mathrm{Ric}_M=\kappa g_M\), \(\kappa>0\), and Kähler form \(\omega\). The unwarped choice \(F=f\omega\) has closed and co-closed flux, \(F^2=2Nf^2\), and \(F_{iP}F_j{}^P=f^2g_{ij}\). The external block is AdS and trace reversal gives

\[
f^2=\frac{2(D-2)\kappa}{d+N-2},\qquad L^2\kappa=\frac{(d-1)(d+N-2)}{N}.
\]

The same flux, if held proportional to the Kähler form of a Kähler internal metric, already forces a constant external warp by Maxwell: \(d(e^{dA})\wedge *_M\omega=0\) and \(\omega\) is nondegenerate. Smooth complex cubic surfaces supply genuine non-product internal examples in D9. [Kähler–Einstein existence on smooth cubics](https://arxiv.org/abs/1807.08960)

With Dirac convention \([eF/(2\pi)]\) integral, \([\omega/(2\pi)]=c_1(M)/\kappa\). For a cubic surface \(c_1\) is primitive, so the aligned flux is \([eF/(2\pi)]=q c_1\), with nonzero integer \(q=ef/\kappa\). In D9, \(\kappa=14e^2/(5q^2)\). All 27 lines pair to one with \(c_1\), so each carries the same signed Maxwell period \(q\) and area \(2\pi/\kappa\). The negative-definite primitive lattice \(c_1^\perp\) is \(E_6(-1)\). In the marked blow-up basis \(H,E_1,\ldots,E_6\), the roots \(E_i-E_{i+1}\) for \(1\le i\le5\) and \(H-E_1-E_2-E_3\) give a basis: subtract a multiple of the latter to remove the \(H\) coefficient, then the remaining exceptional coefficients sum to zero. The lattice describes integral cohomology and marking changes. [Cubic-surface automorphisms and markings](https://arxiv.org/abs/1712.01167) · [Repo cubic-surface geometry](2026-11-09_yoshida_integral_fibers_and_chirality.md)

## Six massive primitive scalars at fixed flux

For any real primitive harmonic \((1,1)\)-form \(\eta\), the Hermitian tensor obtained by composing with the parallel complex structure is transverse traceless. The Kähler Weitzenböck identity identifies its internal Lichnerowicz Laplacian with the Hodge Laplacian on \(\eta\), so \(\Delta_L h=0\) for the convention \(\Delta_L=\nabla^*\nabla+2\kappa-2\mathring{R}\). In the higher-dimensional perturbation take \(\delta g_{ij}=\phi(x)h_{ij}(y)\) with \(\delta F=0\). The linearized Hodge-star change on \(F\) is proportional to the star of \(\eta\), which is co-closed, and \(\delta(F^2)=0\) because the perturbation is trace free. The external derivative of \(\phi\) in the Maxwell equation wedges with the full external volume form. The mixed and external Einstein equations have zero source by transversality and tracelessness. [Kähler curvature identities and harmonic tensor construction](https://arxiv.org/abs/1008.1023)

At fixed covariant \(F\), \(\delta(F_{iP}F_j{}^P)=-f^2\phi h_{ij}\) for a Hermitian \(h\). Thus the internal Ricci variation \(-\tfrac12\Box_d\phi\,h_{ij}\) equals \(-\tfrac12 f^2[1+N/(D-2)]\phi h_{ij}\). The scalar squared mass is strictly positive and satisfies

\[
m_{\rm prim}^2L^2=\frac{2(d-1)(d+3N-2)}{N}.
\]

A smooth cubic has \(h^{1,1}=7\), so its six primitive classes give six modes with **\(m^2L^2=36\)**. In complex dimension two the primitive forms are anti-self-dual, so their integrated Hodge inner product is minus their intersection form. The kinetic pairing of these metric modes is proportional to this inner product. The marked \(E_6\) lattice therefore controls the quadratic pairing in this sector. A Weyl action on this pairing alone gives no local \(E_6\) gauge bosons. The equal-sphere D9 shape mode provides the one-dimensional control with the same squared mass. [Equal-sphere radion calculation](2026-11-14_d9_radion_response.md)

## Spin-two gap and remaining spectrum

For the external transverse-traceless KK tower the first positive squared mass is the first scalar Laplacian eigenvalue \(\lambda_1(M)\). On a smooth cubic the automorphism group is finite, so the Kähler–Einstein Lichnerowicz bound gives \(\lambda_1>2\kappa\). The anticanonical embedding into \(\mathbb P^3\) uses four sections, and the Bourguignon–Li–Yau bound gives \(\lambda_1\le16\kappa/3\) in the normalization \([\omega]=2\pi c_1/\kappa\). Thus **\(20<m_1^2 L^2\le160/3\)** in D9. This exceeds the two-sphere bound's upper endpoint while remaining independent of the flux integer. The primitive-mode calculation gives only a protected sector of the coupled spectrum. Complex-structure deformations, other metric and Maxwell harmonics, and nonlinear couplings need separate analysis. [Kähler first eigenvalue and holomorphic vector fields](https://www.numdam.org/item/10.5802/aif.2415.pdf) · [Projective eigenvalue bound, Theorem 1.2](https://arxiv.org/abs/math/0511670)

Replay the tensor algebra and marked intersection checks with `py -3 analysis/toe_20261114_cubic_surface_flux.py`.
