# A lower-energy W33 monopole trial with a charged phase

For the primitive W33 monopole, a smooth trial configuration with moving adjoint and matter fields has energy strictly below 1038 at unit gauge and adjoint kinetic normalizations. Moving the scalar fields lowers the trial energy from 4490.87 to 1420.62. A subsequent gauge variation lowers it to 1036.63. The rational certificate bounds the infimum in the charge-one sector. The trial uses prescribed radial shapes, and stationarity and stability remain open. [Frozen trial and normalization](2026-11-10_monopole_core_channels.md)

## Color symmetry and an exactly D-flat family

Impose the rank-three torus that annihilates the monopole root and the residual color SU(2) on the equal-flux colors. Their joint fixed fields are thirty complex matter components and nine complex adjoint components. The adjoint contains one monopole triplet and six monopole singlets. The restricted holomorphic Hessian has rank 25 and the broken complex gauge orbit has rank 14. This leaves no uneaten flat directions in this sector near the asymptotic vacuum. Compact symmetry gives a consistent reduction because the action and monopole transition function preserve the subgroup. [Symmetric criticality](https://doi.org/10.1007/BF01941322)

In diagonal gauge define s = r/sqrt(r²+R²) and K = 1−s². The scalar is A = A_perp−(5/2) s m + K v, where v is a real diagonal Cartan singlet orthogonal to the coroot and commuting with both SU(2)s. The replay retains all four such diagonal singlets. The triplet and gauge field use the usual regular hedgehog. Change X[0] by u e0 tensor f2 and set Z[0] = X[0]+X[1] and Z[1] = X[2], with u proportional to K. The two marginal Gram matrices of the X and Z sets agree at every u because X[0] and X[1] have disjoint internal and family support. The adjoint is Hermitian. Thus all D terms vanish along the trial, including in the core.

On the torus-fixed matter plane the signed bracket vanishes identically. The split-mass terms and the dressed Yukawa operators also restrict to zero, since each covariant insertion preserves the fixed matter space. Their first derivatives outside the fixed space vanish by torus invariance. The spectator stays zero. The trial uses the canonical action with the charged Yukawa completion and omits the optional independent neutrino deformation.

The remaining F terms come from the adjoint trace polynomial, the three mixed cubics, and the fourteen centered meson trace squares. In the neutral plane the mixed adjoint source is the symmetric matrix with entries (2u,u;u,0). The replay contracts the entire trace covector with the inverse adjoint trace Gram, retaining its off-diagonal projections. The matter F calculation differentiates the centered invariants with respect to each of the thirty independent neutral coordinates before inserting the trial. [Canonical action](2026-11-09_canonical_sm_flatness.md) · [Charged Yukawa completion](2026-11-10_light_yukawa_completion.md)

## Exact energy and the phase equation

The radial energy takes the form 4π(a/R + b R + c R³). Here a = 63π/32 and b = π[225/16+(Tr(v²)+2u0²)/8], with u = u0 K. The potential is an even polynomial in s divisible by (1−s²)². After removing that factor the potential integrals are the moments of s²/sqrt(1−s²) on [0,1]. Their values are rational multiples of π. The baseline calculation reproduces the earlier exact coefficient c = 449843766875π/196608. A numerical search suggested the amplitudes, which were then rounded and fixed as rationals for the replay. The certificate uses R = 747/10000 and π < 22/7 to prove the strict upper bound without numerical integration.

The gauge profile itself can also vary. Keeping the same scalar shapes and coefficients, set K_gauge = (1−s²)(1+4s²/3) while the singlet scalar and matter corrections still use 1−s². The exact gauge coefficient a/π becomes 1039/864 and the scalar-gradient coefficient b/π becomes 8249503679/240000000. With R = 647/10000 the rational certificate gives energy about 1036.63 and a strict bound below 1038. The analytic electric phase below uses the first gauge profile.

The collective phase has generator m/2 at infinity, normalized to give the embedded raising step unit phase charge. Write its regular Gauss field as p(r) times the radially rotated generator. The scalar commutators and matter action of this generator vanish along the trial. Gauss's equation is

    (r² p')' = 2 K² p,     p(0) = 0,    p(infinity) = 1.

With x = arctan(r/R), p = U/sin(x) reduces the equation to U''+[3−2/sin²(x)]U = 0. The regular solution is proportional to sqrt(3) cos(sqrt(3)x)−cot(x) sin(sqrt(3)x), with normalization fixed by p(infinity). The gauge kinetic norm is a surface term. In the convention T = I times phase velocity squared divided by two it gives

    I = (24πR/g²) [−2 tan(sqrt(3)π/2)/sqrt(3)].

This is the classical phase inertia of the specified trial profile. Computing physical dyon energy levels requires the stationary core, quantization and the coupling to massless fields. [Non-BPS dyon equations](https://doi.org/10.1103/fhhl-sj3z)

Run python analysis/toe_20261111_monopole_variational_core.py from the repository root. [Frozen rational coefficients](../data/toe_20261111_monopole_variational_core.json)
