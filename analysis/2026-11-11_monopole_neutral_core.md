# All neutral real profiles of the color-invariant W33 monopole

This calculation releases all thirty real matter entries in the neutral plane and all six real adjoint singlets, together with the real monopole triplet amplitude and its gauge profile. It solves the resulting 38-profile variational problem in radial gauge. The previous solve retained only two matter amplitudes and left a transverse equation sourced. [Independent matter calculation](2026-11-11_monopole_independent_matter.md)

## Field space and radial gauge

The joint fixed adjoint under residual color and the torus annihilating the monopole root contains the monopole triplet and six singlets. Commutation with the raising and lowering matrices constructs the six singlets exactly. Their real span includes the two root directions between neutral weight lines. The matter fields consist of three fundamentals and two duals, each a real 2-by-3 matrix in the neutral internal plane and the full family space. The neutral plane is annihilated by the embedded monopole generators. Only the adjoint triplet contributes an angular scalar gradient.

In radial gauge the real scalar kinetic term is the ordinary trace norm of the derivatives. The radial gauge equation must still hold. The internal real rotation in the neutral plane and the three real family rotations produce the four potentially nonzero radial scalar currents. For each such generator T, radial scalar stationarity and invariance of the potential give

    d/dr [r² <T phi, phi'>] = 0.

Regularity at the origin forces the conserved quantity to vanish. The numerical replay checks the four currents on the interpolated solution independently of the nodal Euler–Lagrange residual. The matter and adjoint phases and nonspherical fluctuations remain outside this calculation. [Symmetric criticality](https://doi.org/10.1007/BF01941322)

## Potential and numerical checks

The superpotential uses the adjoint trace polynomial, the three mixed cubics, and the centered meson trace squares. The other charged Yukawa terms vanish on the neutral plane under their equivariant insertions. The optional independent neutrino deformation is omitted. For arbitrary real adjoints on this slice the internal D moment includes the commutator of the adjoint with its transpose. The matter and conjugate matter differences add to that moment and to the separate traceless family moment. Both contributions enter with coefficient one quarter of their squared trace norm at unit couplings. The executable checks the F energy on the earlier paired configuration and the four gauge Ward identities away from it. [Auxiliary-field normalization](https://arxiv.org/abs/hep-ph/9709356)

Quadratic radial finite elements use five Gauss points per element. The monopole functions obey the regular Dirichlet values at the origin, the singlets and matter are varied freely there, and all fields match the reference vacuum at radius five. The energy includes the analytic exterior magnetic tail. The discrete stationarity equations are solved by damped Gauss–Newton with complex-step differentiation of the real-polynomial F and D residuals. The convergence records report energy, its components, the virial defect, the scaled nodal residual and the maximum sampled weighted gauge current. These records measure a finite-domain variational solution and its mesh convergence. They do not establish continuum uniqueness, stability, or physical scattering amplitudes.

## Asymptotic magnetic stability

In the faithful S(U(3) × U(2)) torus write the cocharacter as five integers, with total zero and with the sum of the three color entries fixed by the winding. Within either block an integer pair that differs by two or more can be replaced by a pair one unit closer without changing the sum, strictly reducing its squared norm. Thus balancing each block gives the unique minimum-norm cocharacter up to the block Weyl group. For winding one the solution is (1,0,0;−1,0), the primitive charge used here.

Every unbroken root therefore pairs with this cocharacter by 0 or ±1. The asymptotic Brandt–Neri angular index vanishes because the negative-root contribution of charge pairing n is twice max(|n|−1,0). This excludes that far-field instability and leaves the coupled core fluctuation spectrum to be computed. [Global cocharacters](2026-11-10_global_gauge_topology.md) · [Monopole-charge instability](https://arxiv.org/abs/0909.2523)

Run python analysis/toe_20261111_monopole_neutral_core.py from the repository root. [Frozen radial convergence and profiles](../data/toe_20261111_monopole_neutral_core.json)
