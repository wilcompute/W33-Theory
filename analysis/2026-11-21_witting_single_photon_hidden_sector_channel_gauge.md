# Witting theory follow-up: single-photon 24D decoder, compressed 25 outcomes, positive-capacity channel and synthetic gauge dynamics

**Date:** 2026-11-21. **Repository:** `wilcompute/W33-Theory` master. **Audited baseline:** `4b5547b61f9052d2fd37e79592137b2214b4b7af`. This document summarizes **seven completed finite-dimensional mathematical/simulation fronts** and a literature/repository audit. Executable: `analysis/toe_20261121_single_photon_gauge_capacity_followup.py`. Frozen output: `data/toe_20261121_onephoton_chart_channel_gauge_sevenfronts.json`. Regressions: `tests/test_toe_20261121_single_photon_gauge_capacity_followup.py`.

## Executive finding — replace two-photon coincidence tomography with labeled single photons

Earlier work identified a 24-dimensional Witting chart sector that is invisible to 27 five-chart deck averages, yet accessible via **two-photon** matched-coincidence profiles. The representation-theoretic fact is sound; the implicit **measurement-resource inference was too pessimistic**. There is a simpler one-photon estimator, provided each eight-port analyzer outcome is relabeled with its **global Witting-ray identity**, not an anonymous local output-port number.

Let \(A\) denote adjacency on the 45 Hermitian chart labels, \(K\) the 45x27 five-chart incidence, and \(H\) the **45x40 chart-to-Witting-ray incidence** (\(H_{zi}=1\) iff ray i belongs to chart z). The existing projectors are \(\{P_i=|r_i\rangle\langle r_i|\}\), and each 8-outcome double-SIC chart is the POVM \(E_{zi}=P_i/2\) for i in that chart. Every chart has eight rays; each ray occurs in **nine charts**. Integer computation gives the exact identity
\[
\boxed{HH^\top=6I-2A+2J}.
\]
The eigenvalues are \(72^{(1)},12^{(24)},0^{(20)}\). Thus H has rank25, its nonuniform image is **exactly** the hidden 24D \(-3\)-eigenspace, and \(K^\top P_{24}=0\), with \(P_{24}=(15I-5A+J)/30\).

### The one-photon experiment and its closed-form inverse

Prepare a **maximally mixed ququart**, \(\rho=I_4/4\), achievable by classical randomization over an orthonormal basis. Let a controller choose one of the 45 calibrated analyzer charts, with *unknown* distribution \(w\). The chart ID is not supplied to the estimator, but the detector outcome i is reported in a **calibrated common dictionary of 40 Witting-ray labels**. Then
\[
\Pr(i\mid w)=p_i=\frac18\sum_z w_z H_{zi}
=\frac18(H^\top w)_i,\qquad \sum_i p_i=1.
\]
Under the **restricted hidden-sector model** \(w={\bf1}_{45}/45+x\), \(x=P_{24}x\) and w positive, this implies
\[
\boxed{p={\bf1}_{40}/40+H^\top x/8,\qquad
x=\frac23 H(p-{\bf1}_{40}/40).}
\]
This has no numerical matrix-inversion condition problem: the inverse is the adjoint of the exact incidence tight frame. The code verifies an explicit nonuniform positive w whose **27 complete-deck totals are identical to uniform** and reconstructs its hidden bias to machine precision from the 40 one-photon probabilities.

**Estimator and finite-sample guarantee:** For N independent detected photons, let \(n_i\) be the count for global ray label i. Set \(\widehat p_i=n_i/N\) and \(\widehat x=(2/3)H(\widehat p-{\bf1}_{40}/40)\). One outcome i contributes the length-fixed vector \(X_i=(2/3)(H_{:i}-(1/5){\bf1}_{45})\) with \(\|X_i\|^2=3.2\) for every i; \(\mathbb E[X_i]=x\) under the model. Hence **exactly**,
\[
\boxed{\mathbb E\|\widehat x-x\|_2^2
=\frac{3.2-\|x\|_2^2}{N}\le\frac{3.2}{N}.}
\]
This is an *RMS expectation guarantee*, not a high-probability 99% confidence interval. A sufficient ideal detected-photon count for RMS ≤0.001 is **3.2 million**.

**Fisher benchmark:** At \(w={\bf1}/45\), all40 outcomes have probability1/40 and the local Fisher information per detected photon is exactly
\[
\mathcal I_{\rm one-photon}=7.5\,I_{24},\qquad
\operatorname{tr}(\mathcal I_{\rm one-photon}^{-1})=3.2.
\]
The earlier 540 nonorthogonal **two-photon binary matched-event** ensemble had coefficient4492.8 per *pair trial* for this same 24D classical hidden-chart model. Therefore the Fisher Cramér–Rao coefficients differ by a factor4492.8/3.2 = **1404** per ideal *launch/trial*; since a pair consumes two photons, the physical photon resource comparison is even more favorable in the ideal detection model. The older 9.72-billion-pair-trial **conservative upper shot bound** versus the new 3.2-million-single-photon **conservative upper bound** differ by factor3037.5 in counted trials, but they are not identical hardware/noise models. **Do not confuse these conditional mathematical statements with a realized photonic advantage.**

**One fixed pure ray input is not enough.** For each individual pure Witting ray preparation, the 24D Fisher matrix has rank21, due to its 12 orthogonal zero-probability outcomes. A mixed-state preparation with known randomization has full rank24. The model does not use entangled source photons.

**Important identification limits:** This method recovers **the 24D projection of chart weights**, not arbitrary 45 independent unknown weights; the 20D schedule-visible sector remains in \(\ker H^\top\). If chart IDs are directly logged, w could instead be estimated from the control records; the point here is **black-box/chart-anonymous calibration**. However globally labeling an outcome from eight possible ports typically requires chart-aware classical electronics or a chart-programmed photonic router; if *only* anonymous local port numbers are available, the 40-label result is not operationally applicable. Unknown per-ray detector efficiencies or confusion can mimic the 24D signal. This is an independently programmed sensor model, not a new quantum state tomography theorem.

### Compressed physical readout: 24 resolved rays plus one bucket

The rank of the 24D response is24; hence at least25 distinguishable detection outcome bins are required for **local full-rank classical multinomial tomography** (because probabilities sum to one). A deterministic 24-element subset of the 40 Witting-ray labels and one additional coarse detector pooling the other16 labels suffice. The file freezes the subset and checks rank24 and an exact noiseless inverse. For this particular subset, the local Fisher A-criterion is
\[
\operatorname{tr}(\mathcal I^{-1})\approx11.8133333
\]
per launch, versus3.2 with all40 resolved labels. This is an **identifiability-versus-shot-efficiency tradeoff**; optimality among 24-ray subsets is not claimed. The subset was refined by greedy exchange after pivoted QR.

## Front 2 — a hardware-constrained coherent channel still has positive quantum capacity

Previous producer: `analysis/toe_20261121_capacity_fisher_schmidt_locality.py`, which verified the 4→9⊗5 Witting Naimark isometry and a 9D channel with coherent information1.08670849 bits for \(\rho=I_4/4\) under a row permutation of 45 ideal output amplitudes.

Now impose **all five zero-padded Naimark rows into a single 5-mode output group**. Thus the actual quantum output support occupies at most **8 retained rails** while the environment remains 5-level: the kept physical information channel is effectively **4→8**. Search rows using a seeded adjacent group/swap ascent while keeping this zero-rail constraint. An explicit frozen 45-entry permutation yields
\[
\boxed{I_c(I_4/4,\mathcal N_{\rm constrained})=1.03597634898\ \text{qubits/use}>0.}
\]
The full isometry and original 40 ray-click effects remain exact after output relabeling. This supplies a *more hardware-parsimonious positive-rate capacity witness* with one unused 9th output rail, but no A5/PGU covariance or globally optimal routing.

A stronger **separate** optimization of the unrestricted prior 9D routed channel varies the *input state* over full-rank \(\rho=\exp(\sum_{j=1}^{15}\theta_jG_j)/\operatorname{Tr}\exp(\cdots)\), where \(G_j\) are an explicit normalized Hermitian traceless SU4 basis and the rounded15 coefficients are frozen in the JSON. This achieves
\[
\boxed{I_c(\rho_*,\mathcal N_{\rm routed})
=1.09712781140\ \text{qubits/use}.}
\]
The witness is full rank, with eigenvalues approximately (0.19449,0.23131,0.26816,0.30604); it strictly improves the prior maximally mixed value1.08670849. The optimized \(\rho_*\) is a *constructive input witness*, not a proof of global optimality or higher capacity than physically realistic channels. By standard Lloyd–Shor–Devetak coding, these positive single-letter coherent informations rigorously lower-bound the asymptotic unassisted capacity of the **specified mathematical channels**, provided memoryless identical independent uses of those channels.

## Front 3 — two-use coherent information: no observed superadditivity in ten structured inputs

Use the earlier 9D routed channel's five 9x4 Kraus matrices, and form the 25 81x16 Kraus matrices \(K_a\otimes K_b\) for two uses. Evaluate the **complete** output density matrices on C81 and C25 and their entropy difference. For input \((I_4/4)^{\otimes2}\), the explicit two-use calculation equals twice the single-use coherent information within numerical tolerance. Next try ten correlated input density matrices: the convex mixtures of the fully mixed C16 state with (i) a maximally entangled 4x4 Bell state or (ii) a classical maximally correlated four-level diagonal mixture, at five mixture fractions each.

None of these ten trials improved on the product-maximally-mixed **per-use** benchmark 1.08670849; the best was approximately1.08281729 qubits/use. More strongly, the independent optimized single-letter input already gives1.09712781 per use, so these ten structured states fall further below a known single-letter achievable rate. This is a **failed search for superadditivity**, explicitly **not** a no-superadditivity theorem. Research precedent includes dephrasure channels where multi-letter coherent information *is* superadditive: https://doi.org/10.1103/PhysRevLett.121.160501.

## Front 4 — exact SWAP/projector compilation of all 45 chart Hamiltonians

For each Hermitian chart z, let \(L_z,R_z\) be its two orthogonal rank2 Witting-SIC block projectors on \(\mathbb C^4\), \(S\) the SWAP on two ququarts, and \(D_z=L_z\otimes L_z+R_z\otimes R_z\). Then \(D_z^2=D_z\), \(S^2=I\), and \([D_z,S]=0\). By the qubit SIC 2-design identity already established, the exact rank6 chart interaction is
\[
\boxed{Q_z=\sum_{i\in S_z}P_i\otimes P_i
=\frac43 D_z\frac{I+S}{2}.}
\]
For any time t, the full unitary is an exact product of **two commuting nonlocal exponentials**:
\[
\boxed{e^{-itQ_z}
=e^{-i(2t/3)D_z}\ e^{-i(2t/3)D_zS}.}
\]
Numerical reconstruction verifies this identity and unitarity for all45 charts at t=3π/8, maximum residual below \(2\times10^{-15}\).

This removes the apparent need to compile 8 arbitrary product Hamiltonian pieces one by one: there is a more structured **same-block + swap** primitive. It **does not** mean two standard optical gates suffice; a fully coherent SWAP-conditioned projector phase requires engineered interactions/ancillas. Heralded success rates and energy budgets require an actual physical design. Literature: a controlled-SWAP photonic implementation https://www.nature.com/articles/srep45353, with a reported fully heralded alternative needing nine photons, is a hardware **analogy, not a quantitative estimate for our ququart-specific gate**. The 2026 linear-optics heralding no-go paper https://doi.org/10.1103/fzjk-8w3m constrains facile implementation claims.

## Front 5 — finite 45-state fiber, non-Abelian synthetic links, and nontrivial Wilson loop

Use an **externally constructed** 3-torus lattice \(C_L^3\) with 45 internal Hermitian chart states. The internal adjacency graph A is a known SRG(45,12,3,3). At each spatial link choose unitary \(45\times45\) matrices
\[
U_x(L)=\exp(i\alpha A/(12L)),\qquad
U_y(L)=\exp(i\beta |0\rangle\langle0|/L),\qquad U_z=I,
\]
with fixed dimensionless \(\alpha=1.1,\beta=0.7\). The generators do not commute. The plaquette Wilson loop \(W_L=U_xU_yU_x^\dagger U_y^\dagger\) is nonidentity for L=8,16,32,64, with \(L^2\|W_L-I\|_2\) converging toward a nonzero finite quantity, numerically0.222277 at L=64.

The 45-band Bloch operator
\[
H_L(k)=(12I-A)+L^2\sum_{d=x,y,z}
[2I-e^{ik_d}U_d-e^{-ik_d}U_d^\dagger]
\]
is explicitly Hermitian. Its internal mass operator has spectrum \(0^{(1)},9^{(20)},15^{(24)}\); nontrivial gauge coupling mixes these sectors and moves the bands. The graph still has \(45L^3\) lattice-site/internal-state combinations and finite **spatial** diameter under metric rescaling. Unlike the bare GQ chart graph, it does not collapse to a point. But all the extra spatial and gauge data were chosen manually, not derived from W33.

**Crucial causality distinction:** the continuous-time Schrödinger Hamiltonian with coefficient L² does *not* imply an exact finite-speed relativistic causal cone in the scaling limit; a *different*, discrete-time nearest-neighbor coined walk with \(dx=dt=1/L\) has strict one-cell-per-step support by circuit locality. This is neither a Lorentzian continuum derivation nor a Yang–Mills action with dynamical gauge fields. Precedents: `Quantum walks and non-Abelian discrete gauge theory`, Phys. Rev. A 94,012335 (2016), https://doi.org/10.1103/PhysRevA.94.012335; Lieb–Robinson tails, https://www.scholarpedia.org/article/Lieb-Robinson_bounds; synthetic photonic non-Abelian walks, https://arxiv.org/abs/2412.03043.

## Front 6 — calibrated detector mislabeling and missed photons

The globally labeled 40-output one-photon scheme is maximally powerful **only when detector labels are reliable**. For an *independently calibrated symmetric label-confusion channel*, the correct label survives with probability \(1-\epsilon\), and with probability ε it is replaced uniformly by one of the other39 labels. The hidden-sector response is scaled by
\[
\gamma(\epsilon)=1-\frac{40\epsilon}{39}.
\]
At the uniform chart operating point the Fisher eigenvalues become \(7.5\gamma^2\). The explicit \(\epsilon=0.05\) model gives6.7504931, requiring more detected photons to maintain the same precision. With global uniform detection efficiency η, including a no-click event scales Fisher information per **launched** photon to \(7.5\eta\); at η=0.70 it is5.25.

A known confusion matrix can be inverted (with increased variance), but an **unknown arbitrary chart/ray-dependent confusion matrix can mimic chart-weight bias**. Additional calibration settings or trusted standards are required. Related recent work: *Precision bounds for characterising quantum measurements*, Nature Communications (2026), https://www.nature.com/articles/s41467-026-68529-7 ; *Fisher information of complete quantum measurements*, Phys. Rev. A 114,022465 (2026), https://doi.org/10.1103/9xzl-1xkp.

## Independent checks, provenance and limits

The earlier proof identified the **subspace** correctly and established exact 24D operator/coincidence identities, but **the resource claim “need two photons” did not logically follow**. The present 45x40 incidence identity is new **within this comparison**; its projective combinatorics is not being claimed as an original theorem of geometry. This code reuses the existing Witting/GF4 geometry producer and a separate exact H incidence computation. The integer identities, spectral ranks, optimized input witness, seeded multinomial simulation, controlled-SWAP decomposition and synthetic gauge Wilson loops are executable offline.

External references are prior art/context, not empirical confirmation of our Witting-specific predictions. These calculations say nothing by themselves about a verified photonic device, experimental quantum capacity, cryptographic key rate, energy benefit, emergence of the speed of light, the standard model or Einstein gravity.

PowerShell reproduction:
```powershell
python analysis/toe_20261121_single_photon_gauge_capacity_followup.py
python tests/test_toe_20261121_single_photon_gauge_capacity_followup.py
python tests/test_toe_20261121_capacity_fisher_schmidt_locality.py
python tests/test_toe_20261121_fivefront_tightframe_coherent_memory.py
python tests/test_toe_20261121_fivefront_physical_falsifiers.py
python tests/test_toe_20261121_27decks_fivefronts.py
python tests/test_toe_20261121_hermitian45_pauli_sic_bridge.py
```

The user has many unrelated local edits from parallel work; stage **only** this producer, this certificate, this report, and this dedicated test file. Check local HEAD matches origin/master before pushing, and never reset/rebase/discard unrelated files.

## Top five orthogonal next steps

1. **Experimental single-photon anonymized-chart protocol:** design a real globally ray-labeled 40-channel optical router, with a 25-bin compressed variant, calibrate it with nonuniform efficiency and verify the 24D inference without allowing classical chart-ID leakage.
2. **Coherent nine-mode quantum code:** implement an explicit small-error correcting code for the 1.0971-qubit-use mathematical channel, with physically constrained mode sorting, decoder benchmarks, and detector losses; compare to 8-rail constrained implementation.
3. **Meaningful two-letter capacity search:** optimize full-rank correlated 16x16 input states or carefully selected stabilizer-code states against the optimized 1.0971 single-letter baseline; a negative result on ten simple families alone is weak.
4. **Heralded rank6 projector primitive:** quantify the controlled-\(D_z\) and coherent SWAP gate decomposition in a specific photonic/hybrid architecture; prove success/fidelity lower bounds including vacuum and no-click outputs.
5. **Dynamic gauge-field falsifier:** replace fixed synthetic SU45 links with quantum link variables and a local gauge-invariant Hamiltonian; test whether the 24D internal sector has physical low-energy observables while retaining finite-speed transport.
