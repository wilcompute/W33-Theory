# Nonlinear W33 monopole continuation in the adjoint heavy phase

The finite-radius W33 monopole follows a complex stationary branch from zero adjoint phase to π at ten positive-phase checkpoints. The π endpoint is real and agrees in energy with an independent minimization. The conjugated scattering samples give total adjoint reflection winding +3. The background retains the same asymptotic vacuum used to define the light fermion states. [First-order complex response](2026-11-13_monopole_complex_response.md)

## Complex radial energy and connection equation

The continuation varies the real and imaginary parts of the seven adjoint and thirty matter coordinates. The magnetic coordinate K remains real in radial gauge. Its angular and magnetic energies depend on its squared modulus, so the imaginary magnetic equation vanishes on this real-K slice even for complex scalar profiles. The phase multiplies the holomorphic adjoint trace term. The D moments use Hermitian conjugation. The primitive magnetic charge and asymptotic vacuum remain fixed, with the vacuum imposed at r=5.

The numerical solve uses quadratic finite elements and five-point quadrature. It assembles the damped Gauss–Newton blocks from the local residual Jacobian. The F derivative is holomorphic, with the imaginary columns obtained from the real-direction derivative by multiplication by i. The D derivative is differentiated as a Hermitian quadratic moment map. The producer checks directional Jacobians and evaluates the converged energy again through the complex-field energy routine.

After each solve the radial currents are computed in all fourteen neutral compact generator directions. These are the four real skew generators and ten imaginary symmetric generators. The angular magnetic phase also has zero radial current on the real-K slice. In the continuum the weighted currents are constant by the scalar equations and gauge invariance, and regularity makes them zero. In the numerical replay they measure the accuracy of the radial connection equation. [Neutral core and radial gauge](2026-11-11_monopole_neutral_core.md) · [Odd scalar gauge generators](2026-11-11_monopole_phase_hessian.md)

## Continuation checks

The phase-0.05 energy increments are 0.0001264042 and 0.0001264406 on the 60- and 100-element meshes. They give effective curvatures of 0.1011234 and 0.1011525, consistent with the independent derivatives at zero. At phase 0.8, the imaginary part of the gauge-invariant meson trace for the second dual and second fundamental reaches about 0.304 on the 60-element mesh.

The accelerated predictor uses the conjugation variables 1−cos φ for the real displacement and sin φ for the imaginary displacement. At phase 0.8 the predictor reduces the nonlinear correction count from 16 to two and reproduces the energy to about 10⁻⁹. At φ=π the independently minimized real core has energy 574.192680436 and scaled residual 1.74×10⁻⁷ on the 60-element mesh. The real solver uses the same trace polynomial with coefficient −1.

All ten continuation points have scaled stationarity residual below 3×10⁻⁷ and weighted radial current below 3.06×10⁻⁶. The energy excess above the real reference reaches 0.19644733 at π in the repo normalization. At the π endpoint of the continued solution, the largest imaginary scalar entry is below 2×10⁻¹⁷ and the energy agrees with the independent real solve within 1.5×10⁻⁹. The maximum difference of their nodal coordinates is about 6.32×10⁻⁶. An endpoint solve seeded by the unconstrained secant of the previous complex profiles also converges, with imaginary entries below 4.8×10⁻⁷ and energy within 2.6×10⁻⁹ of the independent real solution.

| Phase | Core energy | Largest imaginary scalar entry |
| ---: | ---: | ---: |
| 0 | 573.996233109 | 0 |
| 0.8 | 574.026656651 | 0.101405 |
| 1.65 | 574.102875254 | 0.139829 |
| 2.55 | 574.176019525 | 0.077740 |
| π | 574.192680437 | <2×10⁻¹⁷ |

At phase 1.65 the 100-element control gives an energy excess of 0.10667136, within 2.93×10⁻⁵ of the 60-element value. Its largest imaginary scalar entry is 0.139792 and its maximum weighted radial current is below 9.72×10⁻⁷.

## Reflection and conjugation

At each frozen phase the two-sided shooting code uses the full nonlinear adjoint profile and the unchanged asymptotic vacuum. The residual color symmetry identifies the two color partners, so one representative color block and the weak block suffice. The match tests the regular and exponentially decaying subspaces separately from the light reflection amplitude. [Reference shooting](2026-11-13_monopole_adjoint_shooting.md)

The negative-phase bosonic energy equals the positive-phase energy evaluated on conjugated fields. For the fermion transfer equations this conjugation combines with a sign on the right chirality. In the fixed light-state frame, the reflected amplitude on the conjugate branch is therefore `R(−φ)=−conj(R(φ))`. If the two endpoint cores at 0 and π are real and belong to the same continuous stationary branch, its conjugate completes a closed loop. This gives an endpoint parity check independent of a numerical phase integral. Put `r(φ)=R(φ) exp(−iφ)/R(0)`. It obeys `r(−φ)=conj(r(φ))` and has `r(0)=1`. For continuous reflection on the entire conjugate loop the reduced winding has even parity if `r(π)=1` and odd parity if `r(π)=−1`. A sampled polygon winding can additionally resolve the integer at the tested phase resolution. A rigorous continuous winding still requires control of the subspace gap between checkpoints. The determinant of unitary reflection supplies the scattering invariant here. Relating it to a physical pumped charge requires the time-dependent gauge and rotor dynamics. [Scattering theory of adiabatic pumps](https://arxiv.org/abs/1107.2215)

The direct negative-phase replay at −0.8 agrees with the conjugation relation for both amplitudes and matching gaps. The π endpoint flips the real reference amplitudes to +i for color and −i for weak. The independent real endpoint gives the same signs. Each sampled loop has winding +1. Counting the two color partners gives total winding +3. The maximum step of the sampled reflection phase is 0.451 radians or less. After dividing out the explicit adjoint phase, the largest sampled reflection deviation is 0.000981 radians for color and 0.000345 radians for weak. The smallest sampled matching singular values are 0.549667 and 0.583414 respectively. At phase 1.65, refining the core mesh from 60 to 100 elements changes the two reflection phases by less than 2.2×10⁻⁶ radians and leaves both gaps open.

The finite-radius treatment uses a constant vacuum exterior beyond r=5. The infinite-domain nonlinear core and a bound on the slow scalar tail remain open. [Neutral exterior modes](2026-11-11_monopole_neutral_tail.md)

Run the first three angles with `python analysis/toe_20261113_monopole_nonlinear_phase.py --angles 0.05 0.2 0.45`, then continue with `python analysis/toe_20261113_monopole_nonlinear_phase.py --resume --periodic-predictor`. Run `python analysis/toe_20261113_monopole_phase_loop_shooting.py` to replay scattering. For the real endpoint use `--real-endpoint --output <control-path>`. For the middle refinement use `--elements 100 --angles 1.65 --seed-branch data/toe_20261113_monopole_nonlinear_phase.json --output <control-path>`. [Nonlinear profiles](../data/toe_20261113_monopole_nonlinear_phase.json) · [Scattering checkpoints](../data/toe_20261113_monopole_phase_loop_shooting.json) · [Independent controls](../data/toe_20261113_monopole_nonlinear_phase_controls.json)
