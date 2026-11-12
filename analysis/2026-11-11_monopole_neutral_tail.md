# The light neutral tail of the W33 radial monopole

The real color-invariant scalar potential has four gauge tangent zero modes at the vacuum and four physical masses below 0.03 in the normalization of the radial solver. These masses are singular values of the Jacobian of the F and D residuals in the canonical kinetic coordinates. The smallest is approximately 0.001511. The finite-radius profile at radius 1.6 carries over ninety percent of its squared deviation in the physical mode with mass approximately 0.027506. This supports a matter tail extending well beyond the gauge core. [Real neutral radial profile](2026-11-11_monopole_neutral_core.md)

To test the outer cutoff, the replay replaces the scalar Dirichlet condition by the quadratic exterior energy from the linearized vacuum. For a normal coordinate of mass m and boundary value b at radius R, the decaying linear exterior is bR exp[−m(r−R)]/r. Its scalar energy divided by 4π is (R+mR²)b². Varying the combined energy gives the corresponding Robin condition at R. The gauge function is still fixed to zero at the boundary with its magnetic exterior energy included.

The replay compares two matching radii and records the scalar boundary displacement and exterior energy. The approximation treats the exterior as linear, including the zero masses of the gauge tangent directions. A fully nonlinear infinite-domain solution must also enforce the radial gauge constraint in the exterior. [Non-BPS far-field matching](https://arxiv.org/abs/2602.17583)

Run python analysis/toe_20261111_monopole_neutral_tail.py after generating the neutral-core fixture. [Frozen vacuum spectrum and matching checks](../data/toe_20261111_monopole_neutral_tail.json)
