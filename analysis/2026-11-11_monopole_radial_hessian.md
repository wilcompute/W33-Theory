# Static radial Hessian of the real W33 monopole

This replay computes the second variation of the static energy for the magnetic gauge profile and all thirty-seven real neutral scalar profiles. It uses the previously constructed color-invariant radial ansatz with the linear scalar exterior, unit internal and family gauge couplings, and the canonical action with its charged Yukawa completion. The optional independent neutrino deformation is omitted. [Neutral core](2026-11-11_monopole_neutral_core.md) · [Linear exterior](2026-11-11_monopole_neutral_tail.md)

## Second variation

Let F(q) be the vector of F and D residuals with the kinetic normalizations already absorbed. Half the Hessian of the potential is the sum of J^T J and the residual-weighted second derivatives of F. Both terms enter this calculation. The second term can have either sign on the monopole profile. Complex-step polarization evaluates the mixed derivatives of the real polynomials, and the angular gauge and triplet terms are differentiated explicitly. The replay repeats the calculation at two differentiation steps.

The radial derivative terms and the exterior boundary Hessian are included in the same quadratic finite-element space used for the background. The test takes the quadratic form against the positive norm with density 1 for the normalized gauge coordinate and r² for each scalar coordinate. Banded Cholesky tests the inertia at zero and brackets the lowest generalized eigenvalue by shifting the stiffness by multiples of this norm. The norm provides a static test and does not include the time-dependent Gauss reduction needed for oscillation frequencies. [Gauge-constrained fluctuation equations in a related monopole problem](https://arxiv.org/abs/2602.01921)

The frozen fixture records two finite domains, their background stationarity residuals, and the bottom of each discrete quadratic form. Positive finite-domain forms constrain this real radial sector. The slow modes, the linear exterior approximation, the other angular channels and the complex scalar sector leave an infinite-domain stability question open. [Light neutral masses](2026-11-11_monopole_neutral_tail.md)

Run python analysis/toe_20261111_monopole_radial_hessian.py from the repository root. [Frozen spectral brackets](../data/toe_20261111_monopole_radial_hessian.json)
