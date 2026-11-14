# Fixed-charge radial response of the 42 E6 attractor scalars

Consider the equal-charge member of the [static electric STU family](2026-11-14_e6_stu_radial.md), with the scalars at their balanced values throughout the radial domain. For linear spherically symmetric scalar perturbations at fixed electric charges, the 14 positive directions of the [native Hessian](2026-11-14_e6_attractor_hessian.md) all obey the fixed-scalar equation. The 28 flat directions obey the massless equation. The result uses two-derivative ungauged supergravity.

## Physical normalization

In isotropic radius r the metric is -W^(-2) dt squared + W (dr squared + r squared dOmega_3 squared), with W=1+q/r^2 and positive q. For canonical STU scalars phi the gauge kinetic coefficients are X_i^(-2)=exp(w_i dot phi), with weights (2/sqrt(6),sqrt(2)), (2/sqrt(6),-sqrt(2)), and (-4/sqrt(6),0). Their sum vanishes and their squared outer products sum to 4I.

For a purely electric s-wave the Maxwell constraint fixes the radial displacement. The resulting scalar source uses the inverse gauge kinetic matrix. At the constant scalar point the common orthonormal electric magnitude is 2q/(r^3 W^(3/2)), from the radial derivative of H_i^(-1) with H_i=W. The Hessian of the fixed-flux scalar term is one half of this magnitude squared times the sum of the weight outer products. Hence the fixed-scalar mass squared is 8q^2/(r^6 W^3). The coefficient agrees with the equal-charge extremal limit of the fixed-scalar wave equation of Callan et al. A second independent check is the linearization of the exact harmonic solution under H_i = W + epsilon_i with sum epsilon_i zero, keeping electric charges fixed to first order. This gives delta log X_i = -epsilon_i/W. [Fixed scalar absorption calculation](https://arxiv.org/abs/hep-th/9610172) · [Five-dimensional harmonic solution](https://arxiv.org/abs/hep-th/9708103)

The 42-dimensional scalar kinetic metric on the simple symmetric space is proportional to the trace metric. In the spherically symmetric electric reduction the Maxwell variables have only constrained fluxes, and the scalar source depends on the single fixed-charge potential. The background scalar derivatives and the first derivative of that potential vanish. Thus metric perturbations do not source the linearized scalar equations, and the flux term has the same radial prefactor for each Hessian direction. The two STU modes calibrate this universal prefactor on the 14 equal positive eigenvalues. The other 28 have zero flux mass.

## Exact static response

For static scalars the radial operator is d/dr(r^3 d/dr) minus r^3 W times the mass squared. The verifier substitutes the exact basis solutions and factors their indicial polynomials.

| Directions | Multiplicity | Static solutions | Horizon powers in r | m squared times L_AdS2 squared |
| --- | ---: | --- | --- | ---: |
| Fixed | 14 | W^(-1), W^2 | 2, -4 | 2 |
| Flat | 28 | 1, r^(-2) | 0, -2 | 0 |

The AdS2 coordinate is proportional to r squared and its radius is sqrt(q)/2. In standard quantization the corresponding dimensions are 2 and 1. The horizon-regular solution with given static value at infinity retains the flat component and suppresses the fixed component to zero at the horizon. This is a linear response on the equal-charge background. Unequal charges introduce running scalars and require the coupled radial perturbation equations.

Replay with py -3 analysis/toe_20261114_e6_scalar_radial.py.
