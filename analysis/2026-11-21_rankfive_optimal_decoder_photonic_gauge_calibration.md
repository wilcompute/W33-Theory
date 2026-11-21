# Rank-five quantum recovery and Witting five-front optical falsifiers

**Date:** 2026-11-21. **Mathematical baseline:** commit bd33fa2fb813aff72fc776c4ae42e55968de8fbb and the Witting 40-ray/GF(4) geometry. **Producer:** analysis/toe_20261121_fivefront_rank5_optical_noise.py. **Dedicated tests:** tests/test_toe_20261121_fivefront_rank5_optical_noise.py. **Frozen independent certificate:** data/toe_20261121_rank5_optical_noise_verified.json. **CI:** .github/workflows/witting-rank5-optical-falsifiers.yml.

This pass executed five independent finite-dimensional mathematical/simulation investigations in a separate sandbox, then committed a repository-native reproducer. The new CI workflow was queued at the time of writing, not reported as passed. Desktop Commander still reports zero remaining calls; the Windows checkout was not inspected or synchronized. The earlier workstation-only SDP/MILP producer remains unretrieved and unrelated parallel changes were not reset. No experimental photonic result, fundamental physical constant, gravitational equation, or Theory of Everything has been established.

## 1 — Near-optimal decoder with five Kraus operators and a ten-mode dilation

Restrict the previously committed Witting 4→9 quantum channel to the seeded best 4×2 qubit encoder. For every CPTP decoder R: C9→C2, entanglement fidelity is linear in the unnormalized decoder Choi matrix J. The primal SDP maximizes Tr(MJ) over J positive semidefinite with Tr_logical J=I9. The dual minimizes Tr(Y) subject to I2 tensor Y >= M.

Using a SciPy-only analytic dual log-determinant barrier, Newton continuation, a rank-five Choi spectral truncation and exact trace-preservation normalization, an explicit five-Kraus recovery was obtained. Independent numerical checks gave:

| Recovery or certificate | Entanglement fidelity |
|---|---:|
| Previous Petz map | 0.903497206720065 |
| New feasible rank-five CPTP map | **0.916585973507150** |
| Feasible SDP dual upper bound | **0.916586005507176** |
| Numerical primal–dual gap | **3.20e-8** |

Five recovery Kraus matrices of shape 2×9 stack into a 10×9 isometry, satisfying the isometry equation to max residual approximately 2.33e-15. A sixth orthogonal column completes it to a 10×10 unitary. The auxiliary level dimension five is minimal by input-output dimensions, because 2*4 < 9. **The higher-fidelity decoder therefore does not require a larger Stinespring environment than the Petz recovery.** This is a numerical rather than interval-rigorous SDP certificate, for the specified fixed qubit encoder. A separate sandbox NPZ stores the exact complex unitary, the five Kraus matrices and the encoder; the GitHub producer regenerates them.

Mathematical precedent: Choi rank equals minimum Stinespring environment dimension in a finite-dimensional quantum channel (e.g. https://www.nature.com/articles/s41534-022-00550-2).

## 2 — A physically meaningful phase-noise benchmark, and a deliberately trivial control

Apply independent, unknown Gaussian phase shifts to the nine retained output rails before a **fixed** decoder. For phase standard deviation sigma, the exact ensemble-mean fidelity is

E[F_e(sigma)] = exp(-sigma^2)*F_e(0) + (1-exp(-sigma^2))*F_e(fully rail-dephased).

This is an exact averaging identity from pairwise phase differences, not one random simulation. The results:

| sigma radians | Petz | New rank-five decoder |
|---:|---:|---:|
| 0 | 0.903497 | **0.916586** |
| 0.1 | 0.897319 | **0.910303** |
| 0.2 | 0.879149 | **0.891828** |
| 0.5 | 0.766141 | **0.776920** |
| 1.0 | 0.510973 | **0.517462** |

The fully dephased fidelities are 0.282534 (Petz) and 0.285181 (new). In contrast, a complete output-replacement noise model N_p=(1-p)N+p Tr(.) I9/9 has fidelity F_e(p)=(1-p)F_e(0)+p/4 for **every** CPTP qubit decoder. That noise family cannot change which decoder is optimal; using it alone as a robustness test would be uninformative. Correlated phase drift, loss and cross-rail leakage remain open.

## 3 — A real physical encoding distinction: single-photon 16 modes vs two four-mode photons

The two-logical-ququart chart gate is a 16×16 matrix U_z=I+(-1-i)*3Q_z/4. It can act on one photon spanning 16 distinct optical modes, using a universal passive multiport, without interacting independent photons. Its exact adjacent-two-mode Reck-type decomposition was constructed for all45 charts:

| Transform family | Minimum nontrivial Givens | Mean | Maximum |
|---|---:|---:|---:|
| One local ququart basis change (4 modes) | 4 | 5.689 | 6 |
| One direct 16-mode chart gate | **45** | **93.6** | **113** |

The general Reck upper bound for a 16-mode unitary is120 rotations. These are ideal gate counts; no fabrication tolerances, physical depth, energy, source losses or detector costs were included.

**Crucial limitation:** A single 16-mode photon represents two *logical* ququarts, not two *physical* photons undergoing an entangling interaction. Encoding n logical ququarts solely in the mode amplitudes of one photon needs 4^n modes, exponentially many in n. Thus fixed-small-n deterministic one-photon gate simulation cannot establish scalable BQP with polynomial physical resources. This limitation is established in prior art, including https://www.nature.com/articles/s41467-017-00580-x and https://www.nature.com/articles/s42254-023-00583-2.

## 4 — Covariant transfer of an externally prepared Witting 24D resource

The 45-chart adjacency spectrum decomposes as 1+20+24, with projectors P1,P20,P24. Every closed-system Hamiltonian in the chart adjacency algebra span{I,A,J} preserves these sectors separately, as previously verified.

Now use a 45D chart C and 45D quantum reference R, with a joint unitary U(theta)=cos(theta)I-i sin(theta)SWAP_C,R. For any actual Witting chart automorphism g, SWAP commutes with U(g) tensor U(g), so joint covariance holds; a concrete GF(4) chart automorphism is given by swapping coordinates 0 and1. Prepare chart rho_C=P1 and reference rho_R=P24/24. The reduced chart state after tracing R is

rho'_C = cos(theta)^2 P1 + sin(theta)^2 P24/24,

so p24=sin(theta)^2. At theta=pi/8,pi/4,pi/2, this is 0.146447, 0.5 and1.

This is a valid symmetry-covariant **resource transfer**, not a violation of the closed-chart adjacency-algebra no-go. It is not a novel emergent gauge interaction: the reference state was deliberately prepared in the very 24D sector whose population is transferred, and no gravitational metric or gauge field dynamics was generated.

## 5 — Unknown efficiencies plus 25-bin pooling: an achievable identifiability model

The 25-output sensor resolves 24 Witting ray labels and pools the remaining16. Including no-click gives26 mutually exclusive report outcomes. Treat all40 individual raw-ray detector efficiencies as independently unknown nuisance parameters, with a trusted uniform-chart calibration run and a target run. At the uniform chart operating point with eta=.75 true efficiency and f=.5 calibration share, the Fisher nuisance block is singular because the 16 pooled efficiencies are not individually identifiable.

However, the 24 selected resolved labels have independently calibrated reference/target count ratios. Their 24D hidden-chart response matrix remains full rank. The Moore–Penrose nuisance Schur complement yields

| Measurement scheme | tr(F_profile^-1) coefficient per total launch | Necessary launches for RMS <=0.001 |
|---|---:|---:|
| Previous compressed 25-output labeling | 63.004444 | 63.00 million |
| **Improved compressed labeling** | **60.385185** | **60.39 million** |
| Fully resolved 40-ray labeling | 17.066667 | 17.07 million |

These are *local Cramér–Rao necessary conditions*, NOT sufficient finite-shot guarantees. They depend on a stable efficiency model, trusted reference chart distribution and no unmodeled confusion. Exactly25 linearly independent efficiency combinations are identifiable under pooled readout, versus40 when all ray labels are separately resolved. The hidden chart coordinates remain locally identifiable even though the pooled 16 individual efficiencies do not.

## Five orthogonal follow-ups

1. **Manufacturer-specific decoder mesh:** optimize the extracted ten-mode unitary for a Clements rectangular interferometer, include coupler tolerances, phase stability and photon loss, and compare actual hardware cost against Petz.
2. **Physical two-carrier chart gate:** construct the same chart interaction on two independent four-mode photons using realistic measurement-assisted or nonlinear interactions; report heralding probability and energy explicitly.
3. **No hand-inserted 24D quantum reference:** test coupled chart-indexed gauge fields under the full Witting symmetry generators with explicit Gauss laws and representation-charge conservation.
4. **Detector identifiability stress:** simulate arbitrary stable efficiency asymmetry, time drift and cross-talk, with finite-shot inference and reference-data budget; identify experimentally falsifiable failure thresholds.
5. **Reconcile workstation and CI:** when Desktop Commander access returns, compare and safely merge the old Windows-only SDP/MILP code with the new GitHub rank-five producer; keep parallel files untouched.

The value of these results is in the **computable boundary between finite mathematical channels, implementable small photonic networks and scalable physical claims**. No interpretation as observed quantum behavior or a validated TOE is warranted.
