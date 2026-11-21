# Six Witting research fronts: relational chart dynamics, detector design and optical recovery

**Date:** November 21, 2026. **Source:** analysis/toe_20261121_relational_reference_pareto.py. **Tests:** tests/test_toe_20261121_relational_reference_pareto.py. **Results:** data/toe_20261121_relational_reference_pareto.json.

## Research integrity and access

The independent calculation rebuilt the 40 complex Witting rays and 45 GF(4) Hermitian chart supports using the existing repo generator, verifying H H^T = 6I - 2A + 2J, A^2 = 9I+3J and the rank 1+20+24 spectral decomposition. The numerical results were independently reproduced in a separate sandbox environment before the new GitHub source was written. The new source and tests have been committed, but a dedicated GitHub CI run has not been observed. Do not confuse independently passing finite mathematical checks with a physical demonstration.

Remote Desktop Commander remains out of monthly calls. The exact prior workstation-only source analysis/toe_20261121_calibrated_sdp_fourqubit_symmetry_pareto.py and its full JSON and test suite remain unretrieved; this new module is a distinct, independently authored replacement of some results, NOT a verbatim copy. The local Windows checkout also contains unrelated parallel edits and has not been synchronized. No reset, fetch, rebase or conflict resolution was performed on it during this pass.

Parallel commits inspected: 83b736e8371abc7f7ab885105a928c50eda82881 (Witting defect and gauge-ring model), and 850e85d2b189f108e4956db5129463f6eebe2cc4 (Witting oriented triangle phases). The latter's phase census is prior repository research, not claimed as a fresh discovery.

Literature precedents: Petz optimality (Phys. Rev. Lett. 134, 200602, 2025, https://doi.org/10.1103/PhysRevLett.134.200602); one-shot Petz recovery (J. Math. Phys. 67, 102203, 2026, https://pubs.aip.org/aip/jmp/article/67/10/102203/3405676); relative quantum reference frames and invariant operators (Communications Physics 8, 187, 2025, https://www.nature.com/articles/s42005-025-02036-x); programmable photonic nonlinear circuits (Nature Communications 2025, https://www.nature.com/articles/s41467-025-66205-w); and robust experiment design with noisy observations (2026, https://orbi.umons.ac.be/handle/20.500.12907/55812). These contextualize, but do not validate experimentally, our Witting-specific models.

## Front 1 — Reference-calibrated 24D Fisher matrix and cost

The unknown chart law contains 24 independent hidden coordinates x, while 40 independently unknown but stable detector efficiencies eta_i are nuisance parameters. With a *trusted known-uniform reference chart distribution* and a maximally mixed input, the target/reference no-click multinomial model gives a locally profiled Fisher matrix

I_eff/N = 7.5 eta f(1-f) I_24,

where f is the fraction of launches spent on the reference, N is the number of launched photons and eta is the common true efficiency at the operating point (all 40 efficiencies remain free nuisance parameters in the fit). The optimum is f=1/2 under equal launch costs.

For eta=0.75, the local Cramer-Rao inverse trace is 17.0666667/N. Consequently a locally unbiased estimator with RMS norm error <=0.001 needs N >=17.07 million total launches as a **necessary local condition**, not a guaranteed finite-shot budget.

**Additional resource-cost extension:** if reference and target launches have costs c_R and c_T, the optimal *fraction of total money/resources* spent on reference is sqrt(c_R)/(sqrt(c_R)+sqrt(c_T)). If reference launches cost four times as much, spend two thirds of the total on reference but conduct only one third of total launches as reference shots.

## Front 2 — A new 25-outcome privacy–Fisher Pareto improvement

Consider 24 globally resolved Witting ray labels plus one bin pooling the other 16. The old 24 labels were [31,7,21,28,22,30,3,15,4,23,26,25,8,1,32,20,19,29,14,38,16,39,11,37].

The new resolved 24 labels (zero-indexed) are

[0,1,2,9,6,8,14,11,12,13,15,16,19,21,23,18,27,28,30,32,34,35,37,39].

The detector is full rank on the 24 hidden chart coordinates. For a uniformly random chart and independently calibrated symmetric raw-ray label confusion, lower leakage and lower Fisher trace-inverse are preferable:

| Wrong-ray label probability | Old MI bits | New MI bits | Old Fisher trace inverse | New Fisher trace inverse |
|---|---:|---:|---:|---:|
| 0% | 1.435918 | **1.412155** | 11.813333 | **11.322222** |
| 5% | 1.234326 | **1.212836** | 13.124967 | **12.579328** |
| 15% | 0.953451 | **0.936179** | 16.499614 | **15.813682** |

This is a **verified constructive Pareto improvement**, not a global optimum. The earlier one-shot minimum-leakage design gives MI 1.404889 bits but has far worse Fisher criterion 30.4. The present noise model assumes known chart-independent symmetric mislabeling; unknown detector cross-talk brings back nuisance-identifiability problems.

## Front 3 — A relational symmetry-preserving open-system mechanism

The earlier correct adjacency-algebra no-go applies to closed-chart Hamiltonians F(A) in span{I,A,J}. Introduce an explicitly chosen 45-state quantum reference R and a 45-state chart system C. The **joint** Hamiltonian

H_int = Sum_{r=0}^{44} |r><r|_R tensor |r><r|_C

is invariant under simultaneous permutations of the two 45-element bases. With the reference initially maximally mixed I/45 and the chart in the uniform pure state, evolve for phase pi and trace out reference. The Kraus operators K_r=exp(-i pi|r><r|)/sqrt(45) dephase offdiagonal chart amplitudes by kappa=41/45. With fresh references at each step, the exact 24D population is

p24(n) = (24/45) [1-(41/45)^n].

It is 4.74% after one interaction, 19.85% after five, 45.05% after twenty, and 53.33% after one hundred. This is an explicit **open-system density-matrix sector population transfer** despite joint covariance.

**Boundary:** It is NOT a coherent transition from one chart irrep to another under a chart-only invariant Hamiltonian. The reference and coupling are imposed, and the full S45 relabeling symmetry is a mathematical symmetry of the abstract basis—not necessarily a physical unitary symmetry of Witting rays. This is a falsifier of an overly broad no-go assertion, **not a derivation of physical gauge dynamics, Lorentz invariance, Einstein gravity, or the Standard Model**.

## Front 4 — Exact noncircular chart gate compilation

Each chart splits the input ququart into two mutually orthogonal tetrahedral-SIC qubit blocks. In canonical four-qubit coordinates (block1, spin1, block2, spin2), the unitary

U_z=I_16 + (-1-i)*(3Q_z/4)

applies phase -i to the same-block spin-triplet subspace. A block-parity CNOT, a Bell-basis transform of the spin pair, a three-bit compensating phase, and uncomputation compile it without a pre-prepared U-rotated resource state.

All 45 explicit full 16x16 Witting chart-gate matrices agree to worst element error 1.33e-15. The **canonical** gate-count bound is 14 CNOTs plus two Hadamards and suitable phase rotations, **not counting chart-specific SU4 basis changes**. Realizing those CNOTs in passive photonics is not established and generally needs nonlinearity, measurement-assisted gates or another resource.

## Front 5 — A dimension-minimal 10-mode Stinespring Petz decoder

The committed routed 4-to-9 Witting channel has five 9x4 Kraus operators. Repeating the previously defined seeded search of 300 two-dimensional input code subspaces recovers the best candidate at index 261 and Petz entanglement fidelity 0.90349720672; the corresponding pure logical qubit average fidelity is 0.93566480448.

The Petz recovery has five 2x9 Kraus matrices. Stacking them gives a 10x9 isometry with ||V†V-I9||_max=3.06e-15. Completing its columns produces a 10x10 unitary, embedding input dimension 9 into a logical C2 times auxiliary C5. Since 2*4 < 9, a 5-dimensional auxiliary is **dimensionally minimal** for a deterministic 9-to-2 recovery-channel dilation. This is a concrete idealized 10-mode optical-network objective, *not the higher-fidelity SDP-optimized decoder*, which still lacks a stored explicit optimized Choi/Kraus reconstruction.

A 10-mode unitary can mathematically be compiled into an interferometer, but correct qubit–auxiliary factorization, disposal of auxiliary information and optical losses remain implementation tasks.

## Front 6 — An operational conjugation-odd Witting triangle-phase witness

An independent census confirms the parallel repository finding across all 9880 unordered ray triples: 6640 zero Bargmann loops, 2880 loops with absolute phase pi/6, and 360 loops with absolute phase pi/2. One representative triple (5,14,35) has

Tr(P5 P14 P35) ~ +0.19245008973 i.

The **Hermitian commutator observable** O=i[P14,P35] then has expected value Tr(P5 O)=-0.38490017892. Complex conjugation reverses this signed expectation relative to a fixed external phase convention, while all pairwise ray overlap magnitudes remain unchanged. This provides an experimentally distinguishable target only with phase-sensitive measurement against a calibrated reference; no passive pairwise coincidence count alone suffices.

## Reproduction and five independent research priorities

From a synchronized W33 checkout, run the producer Python analysis/toe_20261121_relational_reference_pareto.py and tests Python tests/test_toe_20261121_relational_reference_pareto.py. The analysis producer writes the JSON certificate. All results remain mathematical or numerical until a physical device or independently executed CI validates them.

1. **Recover and reconcile workstation-only source** when the Desktop Commander monthly quota resets. Retrieve and diff the original SDP/MILP producer and its test suite, then merge deliberately without staging parallel work.
2. **Extract the SDP-optimal 9-to-2 decoder** as a Choi eigensystem, minimal Kraus list and unitary dilation; compare to Petz's exactly 10-mode realization.
3. **Engineer the actual four-qubit gate** including SU4 basis changes and the photon-photon entanglement resource; report physical gate success, noise, heralding and energy costs.
4. **Move from abstract relational dephasing to group-covariant dynamics**, using real PSp4(3) chart permutations, dynamical reference fields and physical Gauss constraints; avoid declaring dephasing to be an emergent force.
5. **Calibrate the new 25-bin detector** with a nonuniform measured confusion matrix, detector drift and asymmetric experiment costs; optimize actual identifiability and total loss-aware photon resources, not only ideal Fisher information.
