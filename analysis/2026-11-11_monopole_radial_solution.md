# A radial W33 monopole solution with a transverse matter force

The primitive W33 monopole has a numerical solution of the seven radial equations on the D-flat trial manifold. Its energy at unit gauge and adjoint kinetic normalizations is 574.2415673. The earlier rational trial gives a certified upper bound below 635. The radial solve uses the same canonical action and charged Yukawa completion, with the optional independent neutrino deformation omitted. [Separate-radius trial and action](2026-11-11_monopole_variational_core.md)

## Radial equations and convergence

The seven profiles are the gauge function K, the normalized triplet amplitude h, four independent diagonal adjoint singlets and one real matter amplitude u. The matter change is u e0 tensor f2 in X[0], accompanied by the same change in Z[0]. The latter relation keeps the two matter marginal Gram matrices equal, so the D terms vanish along the profile.

The numerical fields are (sqrt(6) K, sqrt(75) h, C1, C2, C3, C4, sqrt(2) u), with the four C coordinates orthonormal in the adjoint trace metric. Let q denote the six numerical scalar fields, H = sqrt(75) h and V the full F potential evaluated on this submanifold. The radial energy divided by 4π is the integral of

    6 K'^2 + 3(1−K²)^2/r² + r² |q'|² + 2 K² H² + r² V(q).

The potential gradient is computed from the adjoint and centered-meson F terms, including their kinetic metrics. The gauge equation is K'' = K[(K²−1)/r²+25h²]. Each scalar equation is q''+2q'/r = grad(V)/2 with the extra term 2K²H/r² in the triplet coordinate.

A damped Gauss–Newton finite-element solve supplies the initial profile for collocation. The inner boundary conditions use the regular expansions K = 1+O(r²), h = O(r) and q_singlet' = O(r). The outer fields are fixed at the asymptotic vacuum. The energy quadrature adds the magnetic exterior tail 12π/r_outer and uses the leading regular energy density inside the inner cutoff. [Non-BPS radial monopole equations](https://arxiv.org/abs/2602.17583)

| Inner cutoff | Outer cutoff | Mesh nodes | Max collocation residual | Energy |
| ---: | ---: | ---: | ---: | ---: |
| 0.002 | 3 | 792 | 1.99e−6 | 574.24156709 |
| 0.001 | 4 | 1168 | 4.99e−7 | 574.24156726 |
| 0.0005 | 5 | 1881 | 1.00e−7 | 574.24156726 |

On the finest mesh the gauge, scalar-gradient and potential energies are approximately 311.5312171, 238.2999167 and 24.4104334. The Derrick scaling residual E_gauge−E_scalar−3E_potential is about −3.8e−9. These are numerical convergence diagnostics for the stated submanifold and cutoffs.

## A direction that must be released

An independent variation with opposite increments to the e0 tensor f2 components of Z[0] and X[0] is orthogonal to the shared u direction in the scalar kinetic metric. Its covariant kinetic force vanishes on the shared profile. The D energy also has zero first derivative there because all the D terms vanish. The replay differentiates the original mixed and centered-meson invariants before imposing the shared relation. At radius 0.1 the potential derivative along the unit variation is approximately +2.19927. It has the same sign across the sampled core from 0.002 to 0.2. A compactly supported variation in the opposite direction therefore lowers the energy of this profile. The full radial calculation needs independent matter profiles and the D potential away from the paired relation.

## Electric phase on the numerical profile

The electric Gauss equation remains (r²p')' = 2K²p. The regular inner condition is matched to p = 1−c/r outside the numerical gauge profile. The result is c = 0.12245673 and phase inertia 24πc = 9.23302 at unit gauge coupling. This is the classical response of the computed profile. A quantized spectrum depends on the stationary core and its interaction with the massless fields.

Run python analysis/toe_20261111_monopole_radial_solution.py from the repository root. [Frozen profile samples and convergence checks](../data/toe_20261111_monopole_radial_solution.json)
