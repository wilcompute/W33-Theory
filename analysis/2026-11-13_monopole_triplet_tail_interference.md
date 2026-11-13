# Two-pole interference on the extended monopole background

The earlier radius-5 Dirichlet calculation approximated the singlet-to-triplet conversion by two rank-one unitary pole factors and a fixed unitary background. This replay tests that construction after releasing the scalar boundary values and propagating through the fitted, nonconstant scalar exterior. It uses the radius-9 background propagated to 36 and the radius-5 control propagated to 20. [Scalar-tail solver](2026-11-13_monopole_triplet_tail.md) · [Earlier two-pole model](2026-11-13_monopole_triplet_line_shape.md)

At each attachment radius, the producer refits both outgoing poles. It recomputes the physical flavor-frame residues on two concentric contours and compares them. It uses the existing ordered rank-one Blaschke–Potapov factors to strip the poles from the real-axis unitary reflection matrix. The constant model holds the stripped matrix at its zero-energy value. The second model fits an anti-Hermitian generator from the stripped matrices at E=−0.001 and +0.001 and exponentiates it from the zero-energy matrix. This keeps the fitted background unitary. The reported prediction errors exclude all three fit energies. They bound errors on the sampled holdout grid. [Matrix factorization](https://www.opuscula.agh.edu.pl/om-vol36iss6art1) · [Resonance interference](https://doi.org/10.1103/PhysRev.124.1866)

Replay with `py -3 analysis/toe_20261113_monopole_triplet_tail_interference.py`. For the radius-5 control use `--outer 5 --elements 100 --output data/toe_20261113_monopole_triplet_tail_interference_robin5.json`.

## Radius-20 control

The two contour estimates agree to a maximum relative error of 1.1e-11. At the sampled minimum E=0.002, the conversion is 79.46% and the additive pole–background cross term is −0.38541. The constant background gives a maximum holdout error of 0.297 percentage points. The unitary background with linear phase generator gives 0.0738 percentage points. The two incident projector directions have squared overlap 0.67968.

## Radius-36 result

The sampled conversion minimum is 80.215% near |E|=0.002, with a destructive cross term of −0.382812. The two residue estimates at each pole agree within 6e−12 relative. The maximum holdout error is 0.267 percentage points with a constant unitary background and 0.0823 percentage points with the fitted unitary generator. The same two-pole description therefore remains accurate on the tested energy grid through the larger finite attachment radius. The scattering limit at infinity and the full nonlinear exterior remain open.
