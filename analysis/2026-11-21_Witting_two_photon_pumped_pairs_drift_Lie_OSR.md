# Witting five-front physical continuation: optical Kraus-gauge refinement, two photons, pumped 24D pairs, detector drift and operator-Schmidt complexity

**Date:** November 21, 2026. **Starting commit:** 076a1ea8bc91f60e8f7f75b30aaece6d3cd64c5f on wilcompute/W33-Theory master. **New analytic sources:** analysis/toe_20261121_kraus_gauge_lie_refinement.py, analysis/toe_20261121_two_photon_pair_pump.py, analysis/toe_20261121_detector_drift_calibration.py and analysis/toe_20261121_chart_operator_schmidt_lower_bound.py. **Regression suites:** tests/test_toe_20261121_two_photon_drift_pump_lie.py (15 tests authored) and tests/test_toe_20261121_chart_operator_schmidt_lower_bound.py (5 tests authored). **Independent result summary:** data/toe_20261121_post_Kraus_fivefronts_verified.json. **CI:** .github/workflows/witting-two-photon-drift-covariant.yml.

**Operational integrity:** Remote Desktop Commander reports the authorized Windows device online but zero remaining monthly tool calls. This pass did **not** read or modify its checkout and did not reconcile the still-local prior SDP/MILP code. The GitHub connector was used to add these new files directly to master. A separate sandbox independently executed closely matching numerical scripts and exact invariance checks. The new path-scoped GitHub Actions workflow was **queued**, not known to have passed. No physical quantum apparatus, photon-on-chip experiment, emergent gauge force or Theory of Everything is claimed.

## Front 1 — Loss-aware Kraus gauge refinement produces a stronger implemented decoder

The earlier mathematical Witting channel was a CPTP map from nine retained rails to a logical two-dimensional output. Its approximate optimum is a five-Kraus recovery with ideal entanglement fidelity 0.91658597, versus 0.90349721 for Petz. Both have exact 10-by-9 Stinespring isometries extending to 10-by-10 optical mode unitaries.

The defining **physical synthesis freedom** is that G in U(5) rotates the five environment/Kraus indices, R'_j=Σ_k G_jk R_k, without changing the lossless recovery channel on any input. But an exact ten-mode Reck mesh for the resulting isometry changes which rails encounter loss. In the deliberately narrow model of 2% **power** loss after every active two-mode coupler (idle rails do not lose power), we previously sampled 200 independent Haar U(5) gauges. This pass starts from each best sampled gauge and applies 400 seeded greedy local Lie-algebra perturbations of the form exp(i ε H) with H a normalized random Hermitian 5-by-5 matrix.

| Recovery and physical gauge | Unconditional entanglement fidelity at assumed 2% per active gate |
|---|---:|
| Original Petz basis | 0.758234 |
| Original rank-five optimal basis | 0.756208 |
| Best earlier 200-sample Petz gauge | 0.781324 |
| Best earlier 200-sample optimal gauge | 0.790548 |
| **Refined Petz gauge** | **0.790182** |
| **Refined optimal gauge** | **0.802272** |

The refined optimal compiler has survival probability approximately **0.874612** for maximally mixed encoded logical input, while the refined Petz compiler survives approximately 0.872590. This is a constructive **local** numerical search, not globally optimal over all U(5), optical layouts, completion columns, coupler constraints, or correlated errors. The photon-loss model is hypothetical. The result is a reproducible computational benchmark for co-designing decoder recovery and interferometer synthesis.

## Front 2 — Deterministic, data-preserving passive optical entangling gates are impossible in the specified two-photon model

Consider **two physical photons**, one occupying a single mode from A={0,1,2,3} and the other one from B={4,5,6,7}. Let U be an arbitrary 8-by-8 unitary passive linear-optical transformation. The amplitude of ending with one photon in each output block is

K_(a,b),(i,j) = U_(a,i) U_(4+b,4+j) + U_(a,4+j) U_(4+b,i).

This is the appropriate bosonic permanent formula, accounting for indistinguishable exchange. It produces a generally trace-decreasing 16-by-16 logical map K when two-photon bunching outcomes are excluded.

**No-bunching rigidity proof for this model:** Split U into four 4-by-4 blocks [[A,B],[C,D]]. For every input mode i in A and j in B, absence of output with both photons in output block A requires sym(A_i tensor B_j)=0. Over complex Hilbert space, the symmetric tensor of two nonzero vectors cannot vanish. Thus for every i,j at least one of A_i,B_j is zero. Either A=0 or B=0; the square 8-by-8 unitarity of U then forces the other off-diagonal or diagonal block to vanish, giving U=[[A,0],[0,D]] or U=[[0,B],[C,0]]. These induce only local U_A tensor U_B gates, or local gates followed by swapping the two photons. Therefore no such **deterministic, computational-subspace-preserving passive 8-mode unitary** can implement an entangling two-ququart gate.

This is a special, explicit restatement of well-known passive optical constraints, **not** a universal no-go for extra ancillas, nonlinearities, a different encoding or heralded measurement. See the established no-go literature: https://www.nature.com/articles/srep01394 and https://arxiv.org/abs/2307.11478.

**Constructive postselection contrast:** Coupling only modes A0 and B0 by a tunable passive beam splitter and conditioning on one photon in each 4-mode block yields a nonunitary diagonal logical map. At a full mode swap θ=π/2, for input |+>_A |+>_B supported on two modes per photon, the accepted output is a maximally entangled two-qubit Bell state with probability 1/2. But some computational basis inputs leave the logical output subspace with probability **one**. This is an entangled, postselected output **not an actual nondestructive heralded gate**; counting the data photons destroys them.

**Contemporary experimental comparator:** Liu et al., *Heralded high-dimensional photon-photon quantum gate*, Nature Photonics **20**, 460–467 (2026), https://doi.org/10.1038/s41566-026-01846-x, reported a four-dimensional two-photon controlled-phase-flip experiment in OAM modes, with abstract process-fidelity range around 0.71±0.01 to 0.85±0.01. This is a **different gate** with a different physical resource and cannot be identified with our U_z or assigned its success probability. Also see Arlt, Krenn and Gu, *Automated discovery of nonlocal photonic gates*, Phys. Rev. Research 8, L022031 (May 2026), https://doi.org/10.1103/f415-kgwr, for experimentally motivated nonlocal gates using path identity.

## Front 3 — Joint symmetry can permit **energy-funded 24D pair creation** from vacuum-sector chart states

The 45-chart graph has adjacency eigenvalues 12 (dim1), 3 (dim20), -3 (dim24). Let u be the uniform normalized 45-vector and P24=(15I-5A+J)/30 the 24-dimensional spectral projector. Define the two-chart correlated normalized state

|Ω24> = vec(P24) / sqrt(24).

Every chart-graph automorphism acts by an orthogonal permutation matrix Q preserving A, hence Q P24 Q^T=P24 and (Q tensor Q)|Ω24>=|Ω24>. The paired state is invariant under joint symmetry even though each reduced chart state is P24/24. We numerically checked all **24 coordinate permutations S4** of the original GF(4) Hermitian model and verified their exact invariance.

Choose an explicit single-chart free Hamiltonian h0=Δ(12I-A), with Δ=0.1. The uniform state has energy0; each component in P24 has energy15Δ=1.5. The pair |Ω24> costs30Δ=3.0 total energy. Add an excited two-level pump carrying that much energy, with states |e> and |g>. A deliberately engineered rank-two Hamiltonian

H_int = g(|Ω24,g><u,u,e| + h.c.), with g=0.07,

commutes both with all simultaneously acting chart automorphisms and the total free Hamiltonian h0(A)+h0(B)+H_pump because the two coupled states have **identical total energy**. Starting from |u,u,e>, its exact evolved state is

|ψ(t)> = cos(gt)|u,u,e> − i sin(gt)|Ω24,g>.

Tracing the pump and other chart yields ρ_chart=cos²(gt)P1+sin²(gt)P24/24, so **p24(t)=sin²(gt)** and the pump expends energy3 sin²(gt). This avoids an *initial* prepared 24D reference, and shows how two nontrivial sector excitations can appear as a **joint symmetry singlet while total energy and covariance are preserved**.

**Essential limitation:** the pump and the rank-two interaction were chosen by hand, and the interaction explicitly uses P24 and is nonlocal over chart labels. There are no local Gauss constraints, no dynamical gauge field, no continuum limit and no physical Witting particle-production demonstration. It is a countermodel and engineering research direction, NOT emergent Standard Model dynamics.

## Front 4 — Finite-shot detector stress: privacy/Fisher improvement can worsen systematic drift robustness

Prior 25-outcome detector designs resolve 24 globally labeled rays and pool 16; no-click launches are recorded separately. The nominal compromise subset reduces chart information leakage and improves the local Fisher A-criterion, **assuming a known stable symmetric confusion and efficiency model**.

This pass sampled 40 unequal detector efficiencies between0.65 and0.85, a hidden 24-dimensional chart bias with Euclidean norm0.003, and 128 independent multinomial calibration/target pairs at each total launch budget. We constructed a deliberately simple **ratio-based 24-coordinate inverse**, not the globally efficient maximum-likelihood estimator, and compared it with fully resolved ray detection.

For an unknown fractional reference-to-target drift δ in the 24 separately resolved channel gains, at the uniform chart point the exact worst-case *linear response* gain is

||x_spurious||_2 ≤ [ sqrt(24)/(40 σ_min(D_24)) ] · RMS(δ),

where D_24=(H^T U24/8) restricted to the selected24 ray labels, and U24 is any orthonormal 24D chart hidden-sector basis. The bound is **tight** for a worst-aligned drift perturbation in the local regime. The 40-resolved scheme uses sqrt(40) and the rectangular pseudoinverse.

| Design | Response condition | Worst hidden bias with 0.5% RMS gain drift |
|---|---:|---:|
| Prior compressed25 | 3.580914 | 0.005064 |
| Newer privacy-Fisher compressed25 | **4.233266** | **0.005987** |
| All40 separately resolved | 1.000000 | 0.001826 |

These biases are **much larger** than the sought RMS chart-error target0.001. To bound the worst-case gain-drift bias below0.001, one needs fractional RMS drift below about **0.0987%**, **0.0835%** and **0.2739%** respectively for the three layouts under this linear model. The newer detector wins the ideal privacy–Fisher objective but is *worse* on this minimax gain-drift objective. Nominal information efficiency is not the same as actual adversarial calibration robustness.

One independent sandbox seeded 128-trial run (its random-number consumption order differs from the committed reimplementation, so use the latter for exact CI numbers) found hidden-coordinate RMSE at **20 million reference plus 20 million target launches** of about0.001226 (old compressed),0.001264 (new compressed),0.000656 (full40). This particular ratio estimator does not exploit all coarse outcome information and should not be conflated with Cramér–Rao-optimal inference. An infinite number of samples cannot by itself eliminate an unknown systematic target/reference gain drift.

## Front 5 — An exact operator-Schmidt lower bound on compiling Witting chart gates

For every one of 45 Witting chart supports, let Q_z=Σ_(i in chart z) P_i tensor P_i and Π_z=3Q_z/4, a rank-six projector. At chart phase t=3π/8, the two-ququart unitary is

U_z=I16+(-1-i)Π_z.

Realign its four operator indices into a 16-by-16 bipartite operator-Schmidt matrix with rows(input/output of ququart A) and columns(input/output of ququart B). Every one of the 45 unitaries has **rank8** and the same eight nonzero singular values:

sqrt(17/2), sqrt(9/2), and 1/sqrt(2) repeated six times.

For a rank-one two-ququart controlled-phase primitive V=I+(e^{iθ}-1)P tensor Q, operator-Schmidt rank is at most2; arbitrary single-ququart gates have rank1. Since the operator-Schmidt rank is submultiplicative, any circuit of k such rank-two controlled-phase primitives and arbitrary local gates has rank at most2^k. Therefore **k≥3 is necessary** to implement the Witting chart gate. Three gates are **not proven sufficient**, and the operator-Schmidt rank of a specific experimental high-dimensional CPF must be determined before assigning that experiment a comparable gate-count lower bound. The result is a precise resource obstruction, not a universal entanglement cost formula.

## Verification and next orthogonal fronts

All five mathematical/numerical fronts were independently tested in the container, with source and result files committed to GitHub. GitHub CI had not reported a pass at the time of writing. The Windows worktree remained **untouched** due to Desktop Commander quota 0.

Five independent proposals:

1. **Manifold-level local pair generation:** express the 45-chart P24 pair operator as a sum of strictly adjacency-local interactions with explicit gauge links and Gauss constraints, or prove a locality-depth lower bound against the exact singlet.
2. **Real optical rank-eight gate compilation:** compare measured four-dimensional two-photon controlled-phase primitives and implementable chart basis rotations against the strict k≥3 *rank-two* operator-Schmidt bound, with heralding and realistic loss modeled.
3. **Joint robust optical compilation:** optimize decoder, Kraus U5 gauge, unitary extension and mesh architecture jointly under fabrication-calibrated correlated loss, not the present uniform 2% active-gate idealization.
4. **Drift-aware experimental design:** minimize worst-case hidden-chart drift amplification simultaneously with one-shot mutual information leakage, Fisher trace and detector cost; include repeated trusted reference updates.
5. **Exact CI and workspace reconciliation:** observe the targeted GitHub Actions conclusion and fix any failed regression using logs. When Desktop Commander calls become available, compare old Windows-only SDP/MILP files without resetting the parallel worktree.
