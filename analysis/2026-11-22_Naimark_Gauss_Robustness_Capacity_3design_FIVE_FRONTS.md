# Five independently reproduced Witting/W33 physical-continuation fronts

**Research date:** 2026-11-22. **Repository:** wilcompute/W33-Theory, master. This report distinguishes exact geometry, finite-dimensional simulation, engineering approximations and physical evidence. Nothing below constitutes an experimentally established Theory of Everything or a demonstrated photonic quantum processor.

**Context:** (1) Stelea et al., 2026, real-time dynamical (2+1)D Z2 string simulations, https://arxiv.org/abs/2611.14484; (2) Z2 lattice gauge simulations on nontrivial topology, JHEP July 2026, https://doi.org/10.1007/JHEP07(2026)067; (3) the Witting/Penrose 40-ray identity, https://arxiv.org/abs/1701.06512; (4) the **already known** Hoggar 40-point CP3 projective 3-design, cited in *Designs Related Through Projective and Hopf Maps* (2025), https://doi.org/10.1007/s00454-025-00805-7; and (5) positivity of coherent information as a quantum-capacity lower-bound method, https://www.nature.com/articles/s41534-022-00550-2. Prior repository 2-design, tomography, gauge and quantum-control work remains acknowledged; novelty claims here concern the operational combinations and explicit resource tests, not rediscovery of those mathematical objects.

## A. Fabrication-oriented 40-outcome optical POVM

The normalized Witting rows give the exact Naimark isometry V_(i,a)=conjugate(v_ia)/sqrt(10), shape 40×4, with V†V=I4. A column-restricted adjacent Givens decomposition uses **150 two-mode rotations** plus a four-mode input unitary; the exact reconstructed matrix agrees entrywise to numerical precision. This is smaller than a generic 40×40 Reck rotation upper bound of 780; neither is a fabricated chip or proven minimum.

In a hypothetical *active-two-mode-only* power loss model, mean input-mixed photon survival is 97.8379%, 89.7454%, 80.7657%, or 65.9652% for 0.1%, 0.5%, 1%, or 2% element loss respectively. At 1% per element the worst input state survives with about 78.7561% probability. The loss is state-dependent and cannot be silently substituted into a state-independent detector model.

For the trusted **ideal POVM** same-label separability bound P_same<=.04, and *independent state-independent* detector efficiencies 0.8 on each ququart, an exact one-sided binomial tail of significance 2.8665e-7 with at least 90% power can be achieved with (visibility v, launches N, count threshold k): (.25,177517,4882), (.50,5788,213), (1,1006,55). These are **constructive sufficient N under that specified idealized model**, not proven minimal due discrete count thresholds; the 150-rotation interferometer's path-dependent losses are **not included**.

**Reproducer:** analysis/toe_20261122_witting_40mode_naimark_finite_shots.py.

## B. Two adjacent W33 plaquettes with dynamical matter creation

Choose two 4-cycles from the W(3,3) 40-point collinearity graph: (0,36,9,37) and (0,36,3,6). They share one edge, producing 6 matter-spin sites and 7 dynamic Z2 link qubits. The unconstrained basis dimension is 2^13=8192. Enforcing six local Gauss laws G_v=(-1)^n_v product_e X_e=+1 leaves **128 physical basis states**, indexed exactly by the 7 link electric X bits (matter occupancy is then their incidence parity).

The gauge-preserving Hamiltonian contains explicit edge pair-creation/matter-motion terms sigmaX_u Z_e sigmaX_v, electric terms X_e, two Wilson plaquette products and an onsite matter mass. All terms preserve the physical Gauss sector. With static charges and no magnetic dynamics, the minimum electric energy cost relative to vacuum is **2h times shortest-path distance** on this particular patch, checked across all 15 distinct charge pairs. In a finite quench with h=.6, B=.2, m=.7 at t=1.5, raising matter-pair coupling from J=.15 to J=.7 changes mean matter occupancy from 0.161680 to **1.955817**; the latter has individual Wilson-loop expectations near 0.875514.

This is a quantum finite graph simulator, **not** a thermodynamic string tension, continuum gauge field, QCD confinement result or replication of experimental 2D string breaking.

**Reproducer:** analysis/toe_20261122_w33_two_plaquette_pair_creation.py.

## C. New constrained detector: statistical gain has a price in drift robustness

Earlier full40 ideal maximally-entangled fidelity-score standard deviation is 1.25 per shot. The old 25-output detector has standard deviation 7.70822, chart mutual information 1.435918 bits, and local worst-case detector-drift gain 1.012836. The newer privacy/Fisher 25-output detector has standard deviation 5.12845, chart MI 1.412155 and drift gain 1.197348.

A seeded **50,000-proposal** search using one-, two-, and three-ray moves, and an objective penalizing MI above 1.46 bits and drift gain above 1.65, finds an additional full-rank 24-plus-16 layout:

Resolved zero-based Witting labels:
0, 1, 24, 14, 6, 8, 32, 13, 12, 5, 22, 16, 38, 21, 23, 18, 11, 28, 26, 30, 27, 35, 37, 39.

It achieves **single-shot fidelity-score SD 4.70980**, **chart MI 1.414735 bits**, and **worst-case drift gain 1.495684**. Its fidelity-score variance improves ~15.6% over the earlier privacy/Fisher layout, but its minimax linear-drift sensitivity becomes ~24.9% worse. Thus there is no free detector upgrade. These are ideal target-state Moore–Penrose tomography figures, not globally optimal estimators or measured detector specifications. This search finds a feasible witness, **not global optimality**.

**Reproducer:** analysis/toe_20261122_witting_multicriteria_dualframe_search.py.

## D. Separating positive capacity, antidegradability and entanglement breaking

The explicitly defined **proxy** ququart channel Lambda_lambda=(1-lambda)Identity+lambda WittingMeasureReprepare equals a depolarizing map with state shrinkage alpha=1-4lambda/5. It is not the actual previously studied Witting coherent 4-to-9 photonic channel.

The maximally mixed-input **single-use coherent-information lower bound** becomes zero at lambda≈**0.3862257487**. Its negativity does NOT prove zero quantum capacity.

For lambda=.5, the shrinkage is alpha=.6. The standard universal symmetric ququart 1-to-2 cloner has joint output C(rho)=(2/5)Pi_sym(rho tensor I4)Pi_sym, and both marginals equal exactly .6rho+.4I4/4. This explicitly gives a symmetric broadcast extension; the channel is antidegradable and has quantum capacity **Q=0**. Further depolarization retains this property, proving Q=0 for every **lambda>=.5**. Yet the channel remains non-entanglement-breaking for all lambda<1. Hence the strict region .5<=lambda<1 preserves some Choi entanglement while transmitting no quantum information. The .3862-to-.5 region is not decided by these tests. This is standard cloning/channel mathematics used as a project-specific falsifier, not a newly discovered quantum channel theorem.

**Reproducer:** analysis/toe_20261122_witting_coherence_cloning_capacity.py.

## E. Witting third-order design gives direct state spectral-moment measurements

The 40 rays are a known CP3 projective 3-design. The independently evaluated exact third-moment matrix identity is sum_i P_i tensor P_i tensor P_i = 2 Pi_sym^3; numerical maximum element residual ~1.3e-15. Its normalized frame potentials at orders 2,3,4 are 0.1, 0.05 and 1/30, versus Haar lower bounds 0.1,0.05 and1/35. Thus it is **not a 4-design**.

The explicit 20-ray complete five-ququart-MUB negative control is a 2-design, but its third frame potential is 1/16=0.0625, greater than 1/20=0.05. The equality of Witting's third moment is therefore more selective than the generic 2-design Schmidt witness, although not unique among all possible 3-designs.

**New operational consequence:** For two or three independent identical state preparations rho measured with the same complete 40-outcome Witting POVM, the probabilities that every reported ray label matches are

C2=(1+Tr(rho²))/50,
C3=(1+3Tr(rho²)+2Tr(rho³))/3000.

These determine purity Tr(rho²)=50 C2−1 and the **third spectral moment** Tr(rho³)=[3000 C3−1−3Tr(rho²)]/2 without full ququart state tomography. Every pure input gives C2=.04, C3=.002. The MUB control exhibits input-dependent C3. This triple-collision approach needs a stable 40-output instrument, independent identical preparations, and loss/calibration controls; no hardware data has been observed.

**Reproducer:** analysis/toe_20261122_witting_3design_collision_moments.py.

## Reproducibility and scientific boundaries

The independent research producer in the sandbox executed all five fronts, including exact matrix residuals and stochastic detector optimization. Five repository-native Python producers, a frozen numeric witness summary, **19 authored regression tests** and a dedicated path-scoped GitHub Actions workflow were committed to master; the workflow must actually finish before we claim GitHub-side CI success. No reset, forced update or blanket git staging was used, preserving parallel researcher commits.

These calculations do not derive Einstein gravity, fundamental constants, Lorentz invariance, a quantum advantage, measured photon heralding or a Theory of Everything. The right scientific next move is a counterexample-rich experimental design, not stronger rhetoric.

## Five best independent follow-ups

1. Implement the **40-mode Naimark network** with nonuniform real component losses and recompute rigorous Schmidt-number confidence thresholds after calibration.
2. Extend the **128D gauge patch** to three or more plaquettes, and measure Wilson and 't Hooft operator algebra, charge screening and locality against non-W33 controls.
3. Test **two- and three-copy collision moments** with experimentally known ququart mixed states, including MUB, Haar-random and Witting negative controls.
4. Replace the identity-to-EB capacity proxy with an **environment-resolved noise interpolation on the actual Witting 4-to-9 coherent channel**, deriving upper/lower capacity bounds.
5. Search **hardware-aware detector Pareto fronts** using empirical asymmetric cross-talk and drift and optimize launch resources, not a single ideal weighting.
