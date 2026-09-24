# 2026-09-24 — Single-photon qutrit head: fixed-interaction universality

## Status

**PASS — exact circuit theorem and architecture breakthrough; physical interface remains open.**

This packet changes the interpretation of the Photonic Holonet's "single photon."

A scalable machine should not ask one particle's mode Hilbert space to be the entire
tensor-product quantum memory. Instead, a flying photonic qutrit is the programmable
ancilla/head and network bus, while long-lived qutrit nodes hold the scalable quantum state.

This is a real architectural change from the repo's dominant universality story. It does
not depend on closing the unresolved M36 ququart-to-qutrit injection map.

## 1. Existing frontier

The repo already has a finite programmable Holonet ABI, qutrit Clifford transport,
an 81-state Pauli frame, exact remote qutrit SUM, and explicit Hesse/T and M36
non-Clifford frontiers. Pass 10941 now closes a seven-qutrit Clifford/stabilizer
instruction set but correctly leaves universal quantum computation open.

The new packet changes where the missing resource lives rather than discarding those results.

## 2. Scaling no-go for one-particle memory

If n independent qutrits are encoded only as orthogonal modes of one particle,
their Hilbert space has dimension 3^n. Therefore the particle needs at least 3^n
mutually orthogonal modes. This is a dimension lower bound, not a hardware estimate.

Representative costs are 81 modes for four qutrits, 729 for six, 6561 for eight,
and 531441 for twelve.

Single-photon path/time/frequency/OAM encodings remain excellent finite processors.
They are not a polynomial-resource tensor-product memory model by themselves.

## 3. Fixed qutrit interaction

Let omega=exp(2*pi*i/3), let F be the qutrit Fourier transform, and let

    CZ |a,r> = omega^(a r) |a,r>.

Use one fixed flying-ancilla / memory interaction

    E_AR = (F_A^dagger tensor F_R) CZ_AR

with every ancilla prepared in |+>=F|0>. No algorithm-specific two-body gate
is required.

## 4. Programming local gates in the analyzer

For R(theta)=diag(exp(i theta_0),exp(i theta_1),exp(i theta_2)), measure the
photon in the orthonormal basis

    |b_m(theta)> = (1/sqrt(3)) sum_j omega^(-m j) exp(-i theta_j) |j>.

The exact memory Kraus operator is

    K_m = (1/sqrt(3)) X^(-m) F R(theta).

Every outcome therefore has probability exactly 1/3 for every memory input.
Randomness changes only a known Pauli byproduct.

The executable checks 17 phase programs, including 16 deterministic pseudorandom
triples. Analyzer-unitarity, gate, and input-independent-probability errors are
at machine precision.

The coherent interaction is frozen; the analyzer carries the program; the
classical controller updates the Pauli frame. This is unusually well matched to
the Holonet's existing measurement and frame machinery.

## 5. Same head, two memories: deterministic entangler

Let the ancilla interact first with R1 and then R2 through the same E, followed
by a computational-basis ancilla measurement. Then

    K_m = (1/sqrt(3)) (X^m tensor I) (F tensor F) CZ.

Again all outcomes occur with probability 1/3 independently of the input.
Since F^dagger=F^3 is already available from the local primitive, CZ is recovered
by local frame-compatible Fourier gates.

## 6. T power is a measurement resource

Take the standard qutrit gate

    T = diag(1,zeta,zeta^8),  zeta=exp(2*pi*i/9).

Programming theta=(0,2*pi/9,16*pi/9) gives

    K_m = (1/sqrt(3)) X^(-m) F T.

The executable confirms that T X T^dagger is not projectively any qutrit Pauli:
its nearest-Pauli matrix distance is about 1.5924504340. Thus T is non-Clifford.

The three T-program analyzer vectors are themselves non-stabilizer. Their maximum
squared overlap with the twelve pure single-qutrit stabilizer states is about
0.7123860142, strictly below one.

This is the resource-theory statement that matters:

> the non-Clifford resource has moved from memory-state injection into the
> photonic measurement basis.

It has not become free. A fault-tolerant implementation must still realize this
non-stabilizer analyzer below threshold. But that is a cleaner photonic target
than distilling a memory magic state and injecting it through an unresolved
qutrit/ququart map.

With local F, local T, and entangling CZ, the stationary qutrit register has an
approximately universal Clifford+T gate set.

## 7. One photon flight compiles a graph entangler

The two-memory identity generalizes. Let one |+> ancilla visit

    R1, R2, ..., R_(2n)

through the same fixed E and then be measured in Z.

Define

    a_j = sum_(h=1)^j (-1)^(j-h) r_(2h-1)  mod 3.

The branch phase is

    q_m(r) = sum_(j=1)^n a_j r_(2j) - m a_n  mod 3.

The measurement-independent quadratic part is a weighted qutrit graph phase:

    edge (2h-1,2j) has weight (-1)^(j-h) mod 3,  1 <= h <= j <= n.

The number of weighted edges is n(n+1)/2. The m-dependent term becomes only
local X-frame corrections after commuting linear Z phases through F.

Independent ancilla-path summation verifies random matrix elements for sweeps
through 2, 4, 6, and 8 memories. The corresponding edge counts are

    1, 3, 6, 10

and maximum sampled amplitude errors are respectively

    2.36e-16, 1.19e-16, 5.00e-17, 2.36e-17.

So a coherent photon flight can synthesize a multi-node Clifford entanglement
pattern, not merely carry a gate request. Odd-length sweeps do not produce a
full-rank unitary branch under the same terminal Z measurement, giving an exact
even/odd routing boundary.

## 8. External architecture cross-check

Proctor et al., Phys. Rev. A 95, 052317 (2017), prove universal ancilla-driven
qudit computation from one fixed ancilla-register interaction, one ancilla
preparation, local ancilla measurements, and feed-forward. The present packet
specializes this philosophy to d=3 and freezes the Holonet-facing matrices.

Romanova and Dür, Quantum Sci. Technol. 11 015054 (2026), show that qudit
stabilizer MBQC can use alternative Clifford entanglers whose intrinsic
single-qudit gate is driven by measurement. Their universality condition requires
the intrinsic Clifford to map Z to a Pauli direction with nonzero X component.
Our local branch F R(theta) is precisely in that family.

Cohen and Molmer, Phys. Rev. A 98, 030302(R) (2018), propose a scalable network
where a single photon traverses stationary cavity nodes, mediates controlled
phases across selected qubits, and disentangles at gate completion. Their device
is qubit-based; our qutrit memory-photon interface remains an open physical step.

Bartolucci et al., Nature Communications 14, 912 (2023), build fault-tolerant
photonic computation around constant-size resource states and entangling fusion
measurements. This is a parallel route in which measurement, not a deterministic
two-body gate library, is native.

Takeda and Furusawa, Phys. Rev. Lett. 119, 120504 (2017), use time-bin modes in
one spatial channel and a programmable nested loop for universal measurement-
induced optical gates. Ferreira et al., Nature Physics 20, 865-870 (2024),
demonstrate deterministic multidimensional photonic cluster generation from one
emitter using delayed feedback.

These models must not be conflated: one photon, one photon at a time, one
emitter, and one spatial mode are four different resource statements.

Two recent device results sharpen the physical target. Jiao et al., Phys. Rev.
Research 7, 033267 (2025), coherently store a single photonic qutrit as a
collective Rydberg polariton, control arbitrary superpositions across three
collective Rydberg states, and map the state back to a photonic time-bin qutrit.
Holzapfel, Ortu and Afzelius, Phys. Rev. Applied 19, 024074 (2023), develop a
readout-integrated time-bin qutrit analyzer for echo-based quantum memories and
implement projections spanning a complete MUB set. Saha et al., Nature
Communications 16, 2533 (2025), demonstrate 97% remote trapped-atom entanglement
mediated by time-bin photons and explicitly discuss extension to memories with
more than two states.

These results do not supply our fixed E_AR gate, but they make the missing
component much more specific: coherent flying-qutrit / stationary-qutrit
interaction, not qutrit storage or analysis in the abstract.

## 9. Holonet reinterpretation

Existing exact assets now have a cleaner role:

| Holonet object | proposed computational role |
|---|---|
| qutrit photon | mobile ancilla / programmable head |
| W33 points | candidate memory-node/address layer |
| W33 edges/routes | candidate photon interaction paths |
| 36 spread frames | stabilizer analyzer/calibration programs |
| 81 Pauli frames | measurement feed-forward state |
| 72-tick microframe | interact -> measure -> frame-update transaction |

The last table is an architecture proposal, not yet a theorem. In particular,
the T-program analyzer is outside the stabilizer measurement atlas, so the
36 spreads organize/calibrate the Clifford layer but do not secretly contain
the non-Clifford measurement.

The architecture no longer needs the statement "M36 must be converted into a
qutrit magic state before the machine can be universal." M36 can remain a
valuable candidate fault-tolerant resource without sitting on the abstract
universality critical path.

The new critical path is:

    qutrit memory + fixed photon-memory E + programmable 3-mode analyzer
    + classical qutrit Pauli-frame controller.

## 10. Honest boundary

This packet does not prove a physical realization of the exact qutrit E_AR,
nondestructive reuse of one literal photon, acceptable survival across long
multi-node sweeps, or a fault-tolerance threshold for the non-stabilizer analyzer.

A detected photon is consumed. "Single photon" in the new architecture means
one flying photonic ancilla active per interaction cycle unless a separate
nondestructive measurement/reset interface is supplied.

Nor does this prove that W33's 40 points are the optimal memory topology or
derive any Standard-Model or TOE physics. Those questions remain separate.

## 11. Executable artifacts

- analysis/w33_20260924_single_photon_adqc_qutrit_universality.py
- data/w33_20260924_single_photon_adqc_qutrit_universality.json
- analysis/w33_20260924_single_photon_multipass_graph_entangler.py
- data/w33_20260924_single_photon_multipass_graph_entangler.json
- analysis/w33_20260924_photonic_universality_architecture_atlas.py
- data/w33_20260924_photonic_universality_architecture_atlas.json
- tests/test_w33_20260924_single_photon_adqc_qutrit_universality.py
- tests/test_w33_20260924_single_photon_multipass_graph_entangler.py

The next device-level question is now sharply stated: can a flying photonic qutrit
and one long-lived three-level memory realize the fixed E_AR interaction, followed
by an arbitrary unbiased three-outcome analyzer, with errors low enough that the
predicted Pauli-frame identities remain visible?
