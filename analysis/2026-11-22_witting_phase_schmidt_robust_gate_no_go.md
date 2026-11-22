# Exact all-phase Witting gate resource witness: approximate synthesis ceilings

**Date:** 2026-11-22. **Status:** exact finite-dimensional theorem, independently reproduced in SymPy; no photonic experiment or Theory of Everything established.

## Source and independence

This packet builds on the November 21 canonical two-ququart chart gate in
[relational reference and phase circuit](toe_20261121_relational_reference_pareto.py),
and the 45-chart operator-Schmidt-rank-eight numerical witness
[chart OSR certificate](toe_20261121_chart_operator_schmidt_lower_bound.py).
The earlier certificate established the fixed-phase singular spectrum and the exact
three-entangler necessary bound. This work independently reconstructs its 16x16
canonical unitary in SymPy, proves the **complete variable-phase spectrum**, and
derives operational approximation bounds not present in that fixed-phase certificate.
The other 44 charts inherit the statement via the pre-existing local S tensor S
conjugacy; that 45-chart geometry is a cited prior computation, not rerun here.

## Exact phase-spectrum theorem

Let P be the canonical rank-six Hermitian chart projector and let

    U(theta) = I_16 + (exp(i theta)-1) P.

Rearrange the 16x16 matrix in the bipartition C^4 tensor C^4 to its
16x16 operator realignment R(U). Define

    a = sin^2(theta/2) = (1-cos(theta))/2, 0<=a<=1.

The exact characteristic polynomial of R(U)R(U)^dagger is

    x^8 [x-(16-15a)] [x-9a] [x-a]^6.

Consequently its squared operator-Schmidt singular values are

    16-15a, 9a, a, a, a, a, a, a, 0 (8 times).

The OSR is eight whenever theta is nonzero modulo 2pi; it collapses to one
for theta=0. There is a crossing of the two largest eigenvalues exactly at

    16-15a=9a => a=2/3 => cos(theta)=-1/3.

This angle is sometimes called the tetrahedral angle. Here it is an exact
crossing in a finite-dimensional unitary spectrum and is **not** a derivation
of a physical tetrahedron, spacetime, a coupling constant or a new force.

The polynomial was computed symbolically with the physically valid
z-bar=1/z substitution for z=exp(i theta). The special-phase theta=-pi/2
recovers 17/2, 9/2, (1/2)^6, 0^8 exactly.

## Resource theorem for approximate unitary synthesis

Let V be any bipartite unitary on C^4 tensor C^4, constructed with arbitrary
local unitaries and at most k primitives of operator-Schmidt rank <=2.
Submultiplicativity gives OSR(V)<=2^k.

With squared Schmidt singular values sigma_j^2 sorted decreasing,
Cauchy-Schwarz after rank-r truncation of the realigned matrix gives

    |Tr(U^dagger V)|^2 <= 16 sum_{j<=r} sigma_j^2, r=2^k.

The normalized process fidelity is F_pro=|Tr(U^dagger V)|^2/256.
Average unitary gate fidelity in total Hilbert-space dimension 16 is

    F_avg=(16 F_pro+1)/17.

For k=1, the largest two squared weights sum to 16-6a:

    F_avg <= 1-6a/17.

For k=2, the largest four weights sum to 16-4a:

    **F_avg <= 1-4a/17**.

At theta=pi/2 this gives 15/17=0.882352941..., and
at theta=pi it gives 13/17=0.764705882...
The general k=0 ceiling is (1+max(16-15a,9a))/17.

For unitary channels, the normalized Choi states are pure, so the
channel diamond norm difference is at least twice their trace distance.
Therefore any OSR<=4 unitary V also obeys

    **||U_channel - V_channel||_diamond >= sqrt(a)
                                              = |sin(theta/2)|**.

These are **necessary upper bounds** on fidelity and lower bounds on
channel distance. We have NOT optimized over the physically admissible
rank-r unitaries to show the bounds are tight. They do NOT apply unchanged
when ancillary entanglement, adaptive measurement, postselection, CPTP noise,
or a primitive with OSR>2 is permitted.

## External physics anchors and experimental distinction

- Mathematical background: [Operator Schmidt ranks of bipartite unitary matrices](https://doi.org/10.1016/j.laa.2018.07.018).
- A rank-two bipartite unitary is locally equivalent to a controlled unitary:
  [Phys. Rev. A 87, 022329](https://doi.org/10.1103/PhysRevA.87.022329).
- A contemporary experimental context is the [heralded ququart–ququart photonic gate](https://www.nature.com/articles/s41566-026-01846-x)
  published February 2026. That photonic experiment is a different target
  channel and permits heralding; its reported fidelities must NOT be treated as
  measurements of our Witting unitary.
- Passive linear optics without suitable ancilla/measurement remains subject
  to known [single-rail no-go constraints](https://pmc.ncbi.nlm.nih.gov/articles/PMC3589727/).

## Falsifiable engineering consequence

If a calibrated **unitary** apparatus implements the target fixed-phase
Witting chart with independently verified average gate fidelity greater than
15/17, it cannot be described by a circuit of arbitrary local gates and at
most two operator-Schmidt-rank-two entanglers under the stated model.
Crossing the bound rejects the restricted architecture, **not quantum
mechanics**.

A related outcome is the exact spectral crossing at cos(theta)=-1/3.
Scanning the chart phase and measuring/inferring the nonlocal process
spectrum provides an operational target. Process tomography and loss
calibration must use the full trace-preserving channel rather than
postselected coincidence fidelity alone.

## Artifacts and replay

- [Fixed-phase verifier](toe_20261122_witting_approximate_gate_no_go.py)
- [Full-phase symbolic verifier](toe_20261122_witting_phase_schmidt_law.py)
- Regression tests: ../tests/test_toe_20261122_witting_approximate_gate_no_go.py
  and ../tests/test_toe_20261122_witting_phase_schmidt_law.py
- Machine-readable certificates:
  ../data/toe_20261122_witting_approximate_gate_no_go.json
  and ../data/toe_20261122_witting_phase_schmidt_law.json

Replay: python -m pytest -q tests/test_toe_20261122_witting_* and
python analysis/toe_20261122_witting_phase_schmidt_law.py.


## Additional independent theorem: the entanglement optima are not the spectral crossing

For U(theta), the normalized *operator-Choi* squared Schmidt weights are

    p=( (16-15a)/16, 9a/16, (a/16) repeated 6 times ).

The operator-state purity is

    Tr(rho_AA'^2)=(39a^2-60a+32)/32,

so the maximum *linear* operator entanglement is exact:

    a_linear=10/13, linear entropy=75/104.

In contrast, differentiating Shannon operator entanglement yields
the unique critical equation p0^15=p1^9*p2^6, or

    16-15a=3^(6/5)*a.

Strict concavity proves a **unique Shannon maximum** at

    a_Shannon=16/(15+3^(6/5)) approximately 0.853916600778459,
    theta_Shannon approximately 135.058891 degrees,
    H_op(theta_Shannon) approximately 2.32587792056819 bits.

Neither matches the two-dominant-eigenvalue crossing a_cross=2/3.
And the **strongest two-entangler fidelity separation** is at a=1
(theta=pi), where the upper bound is 13/17.

Thus there are four distinct operational objectives and no reason to
declare any one preferred without a physical task: crossing, linear
operator entropy, Shannon operator entropy, and resource-fidelity gap.
Operator entanglement here is the entanglement of the *vectorized unitary*
across AA'|BB', not in general the entangling power on product inputs.

Executable source:
[toe_20261122_witting_operator_entropy_stationary_phase.py](toe_20261122_witting_operator_entropy_stationary_phase.py),
regressions:
../tests/test_toe_20261122_witting_operator_entropy_stationary_phase.py,
certificate:
../data/toe_20261122_witting_operator_entropy_stationary_phase.json.

## TOE boundary

This is progress in a well-defined quantum-information engineering
subproblem: it quantifies the hardware nonlocality budget for a geometric
gate family. It does not supply quantum gravity, the observed fermion
spectrum, gauge couplings, cosmological dynamics, or an experimentally
established universal theory.
