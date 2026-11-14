# 2026-11-14: Four-copy quantum design witness, ExFT interface, noisy decoder, one fixed radian, and independent SAT audit

## Starting point and status

Source: GitHub wilcompute/W33-Theory master at 0e9235db5bf35416d1c62a0eb0d583b567c9dd60. Original certified results used: 180 signed E6 minimal charge vectors forming an HP3 3-design (not 4), 12-axis optimum over 135 logical Pauli cosets, all 288 maximal ExFT coordinate sections, 45-segment continuously tunable USp8 state compiler, and the single-solver-family 433,517,130-node no-size-eight Pauli-MUB computation. The new source computes new physical and combinatorial consequences, independently and with explicit falsifiers. This is mathematics and simulation, not a physical TOE.

## 1. Real four-copy measurement witness for the 180-point HP3 3-design

For one of the 27 J-even Pauli observables P, let z=Tr(rho P). Uniformly sampled integral positive-cubic charges obey E_finite[z^4]=1/9; quaternionic Haar on HP3 obeys E_Haar[z^4]=1/33. Haar follows from z = 2 Beta(4,4)-1 for an eight-dimensional Haar pure state.

Protocol: draw one random pure state from the declared ensemble; prepare four independent identical copies; measure P on each and multiply the four signs. Repeat independently. The quartet product is a single ±1 outcome with mean eta^4 E[z^4], where eta is a calibrated per-copy Pauli measurement visibility. This gives an unbiased estimator without raising a noisy sample mean to the fourth power.

Using exact binomial tails at at most 5% false-positive rate under Haar and at least 90% statistical power under the finite ensemble, round upward in increments of 100 quartets:
- eta=1.0: 1,400 quartets = 5,600 prepared states.
- eta=0.9: 3,200 quartets = 12,800 prepared states.
- eta=0.8: 7,900 quartets = 31,600 prepared states.

Assumptions: independence between quartets, four copies of the SAME latent ensemble state inside each quartet, calibrated visibility, unbiased random state draws, no drift, no hardware measurement errors beyond the scalar visibility model. No experiment has yet been executed.

## 2. Complete ExFT cross-branch obstruction, not a section-selection law

For all 216 maximal coordinate-supported 5D sections S and 72 maximal 6D sections T, compute the strong-constraint cross cost B(S,T)=sum_{u in S, v in T, k} C_uvw^2, with the canonical signed E6 cubic tensor. Exact 15,552-pair histogram:

| Cross cost | Number of 5D-vs-6D pairs |
|---:|---:|
| 2 | 1,080 |
| 6 | 4,320 |
| 10 | 432 |
| 11 | 4,320 |
| 16 | 4,320 |
| 22 | 1,080 |

No zero cases. Unrestricted derivative dependence in two distinct such maximal coordinate sections simultaneously violates the strong constraint. A toy mixing penalty V_gamma(t)=gamma B t(1-t), gamma positive, was differentiated and integrated by numerical gradient descent; it has two stable, degenerate endpoints. This shows how a cross-branch interface barrier could arise, but it proves that the penalty ALONE cannot favor 5D over 6D. It is not derived from the ExFT action and no gravitational vacuum selection follows.

Published context: Hohm and Samtleben, E6(6) Exceptional Field Theory I, https://arxiv.org/abs/1312.0614 ; review https://pos.sissa.it/231/133/pdf . The two inequivalent section families are prior art.

## 3. Physical shot noise for the hidden CP1 logical qubit

A known charge selects one of 180 quaternionic two-planes; three local J-odd Pauli expectations, selected using the previously solved 12-axis menu, determine a pure logical Bloch state. We sampled 24 random pure Bloch states per charge, 4,320 states total; per-axis outcomes follow independent binomial distributions with visibility eta=(1-depolarizing fraction)(1-2 classical readout bit-flip fraction).

At eta=.81 (10% depolarization, 5% classical readout bit flips), normalized Bloch reconstruction gives:
- 20 shots/axis: 0.9673711 mean target fidelity
- 80 shots/axis: 0.9916298
- 240 shots/axis: 0.9972246

The certificate also stores fifth-percentile results and other visibilities .65 and 1.0, an actual 12-shot-per-axis pilot-adaptive allocation vs equal shots for a total budget of 360, and the conservative simultaneous Hoeffding bound. Adaptive performance is measured rather than assumed superior. This is an ideal independent-measurement statistical simulator, not hardware data; it presupposes the correct known charge and no state leakage.

## 4. Fixed one-radian physical gate words: exact construction, large depth

The previous 45-rotation USp8 pure-state compiler used arbitrary real-valued Pauli angles. We now implement the one-fixed-angle version: finite quarter-turn compact-Clifford conjugations transport a single fixed R_0=exp(i 1 rad P_0) to every signed one of the 36 compact Pauli directions (72 signed axes; exact BFS). For each target angle theta_j choose an integer k_j between -B and B closest to theta_j modulo pi. Then the legal word is C_j R_0^{abs(k_j)} C_j^-1, with the conjugation sign chosen to match sign(k_j).

We directly apply all 45 words to the 8-component state vector for each of five target preparations and compare with the original continuously optimized state. A Fubini-Study triangle inequality gives a certified lower bound to fidelity with the TRUE original target. With bound B=4000, the worst guaranteed target fidelity exceeds 0.99970 but requires about 165,000 one-radian pulses per target on average; B=250 uses about 4,560 pulses with worst guaranteed fidelity >0.99963. This is a constructive but very inefficient synthesis, not an experimental photonic circuit or efficient Solovay-Kitaev algorithm.

## 5. New exact single-measurement-failure optimum: 20 axes

Every 45 signed tritangent supports requires three logical Pauli classes; 135 classes have four candidate J-odd Pauli axes each and each of the global 36 candidate axes appears in 15 classes. A globally chosen menu survives failure of any ONE included axis exactly when each class has at least two chosen representatives.

Two independent 0-1 solvers (SciPy HiGHS MILP and OR-Tools CP-SAT) establish the optimum 12 for one-fold hitting and 20 for two-fold hitting. CP-SAT proved 19 axes cannot cover all classes twice. All 20 single-axis dropout scenarios pass the raw integer incidence checks. One optimal 20-axis menu in signed six-bit Pauli labels is [1,3,12,13,14,15,21,22,24,25,36,38,40,41,42,43,49,50,62,63]. This is robust measurement scheduling, NOT quantum error correction or immunity to correlated hardware faults.

## 6. Independent five-qubit MUB CDCL reformulation: unresolved, never a false proof

Prior Pass12654 complete DFS reports no maximal size-eight Pauli-MUB set over eight O(5) representative branches (433,517,130 nodes), but not a portable independently checked UNSAT proof. We created a different solver formulation in PySAT/CaDiCaL, with a deterministic hash of each generated CNF clause.

For each of the two S3-class representatives 692 and 694, choose exactly four remaining symmetric GF(2) rank-codes from 2,336 candidate codes after fixing 0,infinity,I,S2. All 2,336 potential extensions must be covered (killed by singular sum or equality), and every chosen pair must have nonsingular sum. This yields 1,685,712 clauses per representative. Both branches were actually built and searched under a 30,000-conflict budget, reporting UNDECIDED_BOUNDED_CONFLICTS, not UNSAT. The source also executes n=3 positive and negative controls. The process showed a nonzero Windows termination status after writing the JSON certificate, so no standalone n=5 UNSAT proof log is claimed. The exact CNF constructor and clause digest are reproducible; no full external proof checker has validated a new n=5 no-go. The earlier DFS result remains the strongest exhaustive evidence. Scope is maximal Pauli MUBs, not unrestricted MUBs.

Relevant literature: William Kantor, On maximal symplectic partial spreads, https://pages.uoregon.edu/kantor/PAPERS/maxPartial.pdf .

## Reproducer and tests

- Four physical fronts producer: analysis/toe_20261114_physical_falsifiers_section_noise_fixed_radian.py
- Failure-tolerant measurement producer: analysis/toe_20261114_dropout_resilient_12axis_tomography.py
- Independent bounded MUB CDCL: analysis/toe_20261114_fivequbit_MUB_CaDiCaL_sat_attempt.py
- Machine-readable certificates: data/toe_20261114_witness_selection_decoder_fixedangle.json, data/toe_20261114_pauli_global_dropout_resilient_tomography.json, data/toe_20261114_fivequbit_MUB_independent_CaDiCaL_SAT.json
- Reproducible regression: tests/test_toe_20261114_physical_fiveplus_continuation.py

No theory of everything has been derived. Distinguish mathematical identities, resource estimates under stated noise assumptions, toy phenomenological potentials, and hardware observations.

## Five independent next falsifiers

1. Perform the four-copy randomized-state design discrimination on an actual three-qubit platform, with preparation and detection calibration.
2. Derive a covariant variational potential from an ExFT action and test whether it selects the five- or six-coordinate branch; a handcrafted t(1-t) penalty does not.
3. Test the 20-axis menu under correlated readout noise, optical loss and erroneous charge labels; look for failure of the assumed fixed-fiber decoder.
4. Replace the ~165,000 one-radian-tick compiler with a checked short-word Solovay-Kitaev or number-theoretic synthesis, benchmarking fidelity and two-port optical cost.
5. Generate and externally verify a true unsatisfiability proof for both n=5 size-eight MUB class encodings; timeouts and the existing one-family exhaustive DFS are not that proof.
