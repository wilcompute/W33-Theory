# Bosonic index of the capped M5 probe

The [localized M5 cap](2026-11-16_Tpq_M5_finite_stripe.md) has worldvolume \(S^5\times S^1\) at a polar or equatorial warp minimum. Its internal quadratic action contains a Wess–Zumino mixing term absent on the uniformly wrapped round probe. A weighted square completion retains that term and proves positivity of the internal block for all spectator momenta on the near-resonant branch. The capped probe has one bosonic negative mode when the spectator circumference satisfies the bound below. The result uses the Abelian leading-derivative M5 action with zero background worldvolume three-form and compatible flat data. [M5 action](https://arxiv.org/abs/1308.2231) · [Chiral Hamiltonian](https://arxiv.org/abs/hep-th/9805065)

## Position-dependent mass and electric mixing

Use local AdS units at the base position of the cap. Let \(s\) be arclength along the meridian, \(z(s)\) its longitudinal torus coordinate on the cover, and \(w\) the proper spectator coordinate. The induced metric is \(ds^2+\sinh^2r(s)\,d\Omega_4^2+dw^2\); the profile has \((r_s)^2+(z_s)^2=1\). Put \(S=\sinh^4r\), \(V(r)=\int_0^r \sinh^4v\,dv\), and \(c=4/\alpha\). The cap first integral gives \(z_s=cV/S\) oriented from one tip to the other.

The derivatives of \(A\) and \(C\) vanish at both possible wrapping locations, so the AdS warp \(W=A+\tfrac13\log\rho\) and torus length exponent \(T_{\rm len}=-\tfrac23\log\rho\) are also stationary there, with \(\rho=e^{C-5A/3}\). For a transverse displacement \(\xi\) in the four-dimensional internal base, the DBI derivative terms are positive. Its potential is the Hessian of the log induced density in those directions. Four angular tangents are external, one tangent lies along the spectator torus, and the meridian has squared torus projection \(\nu=z_s^2\). With all norms taken at the background location, the mass matrix is therefore
\[
 \begin{aligned}
 M_{\rm DBI}
 &= (5-\nu)\nabla^2 W+(1+\nu)\nabla^2 T_{\rm len}\\
 &=\left(\frac{10}{3}+\frac{2\nu}{3}\right)\nabla^2 A+(1-\nu)\nabla^2 C .
 \end{aligned}
\]
There is no mixed quadratic derivative with the geometric normal, because the ambient base metric is orthogonal to the external and torus directions and the two warp gradients vanish. The torus electric pressure in the [probe action](2026-11-16_Tpq_M5_probe_action.md) is base-independent, so it adds no internal potential or mixed geometric-normal term. The second-sphere displacement directions are exact flat position modes. The first-sphere positive Hessian directions of \(A\) are of order the quadrupole amplitude, while the Hessian of \(C\) is quadratic in that amplitude. Symmetry gives the same null space from the equatorial orbit when it is present. This makes \(M_{\rm DBI}\) nonnegative sufficiently near resonance; the numerical checks verify both endpoints \(\nu=0,1\) of this affine matrix at three actual warped backgrounds.

The remaining Wess–Zumino term comes from the sphere-plane blocks of the closed pressure two-form. Denote the signed pressure coefficient for one orthonormal base plane by \(g\), in local AdS units with the torus pressure \(c\). For its two normal components, the quadratic term is proportional to
\[
 -\int ds\,dw\,d\Omega_4\; g\,V(r)
    (\partial_s\xi_1\partial_w\xi_2-\partial_w\xi_1\partial_s\xi_2).
\]
The coefficient is evaluated at the fixed base position. Integrating by parts gives the antisymmetric Fourier mixing \(g\,r_s\,J\partial_w\), in the quadratic operator with density \(S\,ds\). Here \(J\) is the rotation matrix of the normal plane. The integration is regular at the tips, where \(V\) vanishes. This term can affect the spectrum and is retained below.

## Weighted factorization including the Wess–Zumino term

At signed spectator momentum \(k\), diagonalize the Hermitian matrix \(iJ\). The two scalar operators involving the potentially adverse mixing are
\[
 {\cal H}_{\pm}=-S^{-1}\partial_s(S\partial_s)+k^2\pm gk r_s .
\]
They are supplemented by the nonnegative angular Laplacian and \(M_{\rm DBI}\). At the relevant polar or equatorial minimum, the DBI matrix preserves each sphere plane. Its positivity suffices even if it is not diagonal in the same complex polarization basis. Use \(\mathcal D_\pm=\partial_s\pm gk\,V/S\). Its adjoint in \(S\,ds\) gives
\[
 {\cal H}_{\pm}=\mathcal D_\mp^\dagger\mathcal D_\mp
                     +k^2\left(1-g^2 V^2/S^2\right),
\]
since \(\partial_s V=S r_s\). Regularity removes the tip boundary terms. On the cap \(c V/S=z_s\le1\). Thus \(|g|<c\) makes all \(k\ne0\) internal modes strictly positive, independent of spectator length. At \(k=0\), the remaining nonnegative Laplacian and mass leave only the constant displacements along the symmetry orbit. The sphere pressure coefficients are less than the torus pressure near resonance by the warped pressure formula. In the three verified examples their largest magnitudes are below \(0.58c\), and the minimum positive DBI coefficient is above \(3.32\) times the corresponding Hessian eigenvalue of \(A\).

## Chiral field and geometric index

Contracting one transverse displacement into \(G_4\) still leaves a base leg in both the horizontal and mixed flux components. Its pullback vanishes at first order, so the linear variation of pulled-back \(C_3\) is exact and is absorbed by the chiral gauge potential. In the compatible flat sector the chiral field thus decouples at quadratic order. Continuing its Lorentzian positive Hamiltonian gives nonnegative kinetic operators in the physical Euclidean contour. Equivalently, the spectator-circle zero mode gives the Maxwell operator on the capped \(S^5\); the massive chiral modes obey the corresponding Hodge equation with positive circle mass after squaring the first-order self-duality equation. Both \(H^2(S^5\times S^1)\) and \(H^3(S^5\times S^1)\) vanish, so there is neither a flat two-form modulus nor a harmonic three-form sector.

The earlier Sturm argument gives one negative eigenvalue in the geometric normal sector on the cap before adding the spectator circle. The short-circle bound can be strengthened. Differentiating \(S\tanh r/5\) and \(S\tanh r/4\) gives
\[
 S\tanh r/5\le V\le S\tanh r/4 .
\]
Hence the four equal angular curvatures \(cV\coth r/S\) lie in \([c/5,c/4]\). The remaining curvature is \(c-4k_\theta\). The squared norm \((c-4k_\theta)^2+4k_\theta^2\) is convex with endpoint maximum \(c^2/4\); the ambient Ricci contribution to the Jacobi potential is nonpositive. Therefore a spectator circumference \(\ell_\perp<4\pi/c\) guarantees that all its nonzero Fourier contributions in the geometric block are positive. Under this sufficient bound the full bosonic physical probe index is one. There are six geometric center zero modes, five from hyperbolic translations and one longitudinal translation, and two polar or three equatorial internal position modes. The coefficient of the chiral determinant phase, the fermionic spectrum, and bulk backreaction are outside this calculation. [Rotational cap Jacobi problem](https://arxiv.org/abs/2301.11038)

Reproduce the [JSON checks](../data/toe_20261116_Tpq_M5_cap_probe_index.json) with `py -3 -B analysis/toe_20261116_Tpq_M5_cap_probe_index.py`.
