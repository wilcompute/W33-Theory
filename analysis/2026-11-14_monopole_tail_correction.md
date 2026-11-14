# Infinite-radius first variation of the projected monopole scattering

At energy 0.002 this calculation extends the [projected scattering replay](2026-11-13_monopole_far_tail.md) on the same radius-nine Robin background. It uses the native mass operator and the existing four incoming and four outgoing vacuum channels. The core match remains at radius 36.

Write the projected equation as y' = (i E J + V)y, with J diagonal and entries +1 in the four outgoing coordinates and -1 in the four incoming coordinates. Use the interaction picture based at the cutoff T. A contribution G exp[-m(r-R)]/r to V then has integral matrix entries

    G_ij exp[mR - i omega_ij T] E1[(m - i omega_ij)T],

where omega_ij = E(J_jj - J_ii) and R = 9 is the profile join. This accounts for the oscillating signs and phases in the open-channel interaction. The implementation checks an off-diagonal entry against independent real and imaginary quadrature. [NIST exponential integral](https://dlmf.nist.gov/6.2.E1)

Let S be the unitary reflection graph at T and K the interaction-picture generator integral. The first variation of its reflection is

    delta S = [I, -S] K [S; I].

The corresponding first variation of the conversion probability is twice the real inner product of the converted outgoing amplitude with its variation. The verification uses direct propagation with the nonlinear reflection graph through radius 36864 and strips its free common phase before comparing the matrices. [Bellman, Kalaba and Wing on invariant imbedding](https://doi.org/10.1073/pnas.46.12.1646)

There is also a remainder inequality for this first variation. If the full projected generator has norm integral A over the remaining tail, the unitary graph moves by at most 2A. The vector field at two unitary graphs differs by at most 2 sqrt(2) ||V|| times their separation, by expanding the difference of the two rectangular factors in the graph equation. Integrating gives an error at most 2 sqrt(2) A^2 in the first-order reflection with the full generator. If the first variation instead uses a linearized generator and the difference has norm integral B, the reflection error is at most 2B + 2 sqrt(2) A^2. The producer reports a square-of-integral diagnostic using the retained linearized terms. A certified bound for the native projected model requires uniform coefficient bounds for A and B.

The computation uses real finite differences of the native fermion generator at vacuum with Richardson refinement for the linear coefficients. The linearized model omits the massless direction by the gauge-tangent cancellation in the prior proof. It omits positive masses with mT >= 220 in the first variation, while direct propagation retains the full fitted profile and nonlinear mass evaluation. The comparison tests tail truncation for this projected model at one energy. Uniform derivative bounds, interior discretization error and feedback from the massive modes remain open.

Run the default 32-shells-per-octave replay with py -3 analysis/toe_20261114_monopole_tail_correction.py. Set --cells-per-octave 64 and --output to a new JSON path for the refinement.

## 32-shell control

| Quantity | Result |
| --- | ---: |
| Probability at radius 4608 | 0.807418656491 |
| Probability at radius 36864 | 0.807418632107 |
| Direct finite-radius probability change | -2.43839826e-8 |
| First-order infinite-radius probability change | -2.46223123e-8 |
| Operator norm of direct minus first-order matrix change | 1.57743530e-9 |

The earlier 16-to-32 mesh difference at radius 4608 was about 3.14e-6 in probability. This exceeds the observed change from increasing the radius beyond 4608. The finite-radius comparison supports prioritizing shell discretization and channel feedback over a longer projected integration at this energy.
