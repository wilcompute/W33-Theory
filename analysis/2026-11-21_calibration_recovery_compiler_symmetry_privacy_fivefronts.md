# Five Witting research fronts: calibrated single photons, optimal recovery, a noncircular gate compiler, gauge symmetry, and privacy-optimal POVM pooling

**Date:** 2026-11-21. **Starting point:** \`ba6ab74b73bcb0be0926991fdb93c5bab88e3492\`, subsequently cross-checked against parallel commits \`83b736e8371abc7f7ab885105a928c50eda82881\` (Witting chart defect and a critical Gauss ring) and \`850e85d2b189f108e4956db5129463f6eebe2cc4\` (Witting triangle Bargmann phases). **Scope:** mathematical finite-model identities, ideal quantum-channel semidefinite programming and mixed-integer detector design. No chip, physical entangler, emergent gauge symmetry or theory of everything is claimed.

**Execution and environment:** The exact five-front producer \`analysis/toe_20261121_calibrated_sdp_fourqubit_symmetry_pareto.py\` was created and successfully executed on the authorized Windows workstation against the current project source. It emitted \`data/toe_20261121_calibrated_sdp_fourqubit_symmetry_privacy.json\` with status **FIVE FRONTS PASS** before Desktop Commander exhausted its monthly tool-call budget. Those two files and \`tests/test_toe_20261121_calibrated_sdp_fourqubit_symmetry_pareto.py\` are at present **workstation-local, not committed**; remote access stopped before they could be retrieved and the new regression suite could be executed. Accordingly the results here are **producer-validated, not independently CI-certified**, and local/GitHub sync cannot be claimed. This report was written through the GitHub connection separately. Preserve and manually reconcile the workstation's other dirty files rather than resetting or blindly staging them.

## 1 — A rigorous launch-budget correction for the 24-dimensional one-photon model

Let H be the previously certified 45-by-40 chart-ray incidence and let U span its 24-dimensional hidden chart subspace. At uniform chart weights the ideal global ray outcome distribution is \(\mathbf p=\mathbf1_{40}/40\). With *40 individually unknown but stable* ray efficiencies \(\eta_i\), the observable target probabilities are \(q_i=\eta_i(1/40+(H^\top U x)_i/8)\), with no-click outcome \(q_\emptyset=1-\sum_iq_i\).

A trusted reference measurement using a *known* uniform chart distribution produces \(q_i^{\rm ref}=\eta_i/40\). At the uniform operating point with all true efficiencies equal to \(\eta\), form both multinomial Fisher matrices on the 24 x-coordinates and 40 nuisance \(\eta_i\) parameters. For fraction f of the **total launches** assigned to reference, the Schur complement (profile Fisher information for x after eliminating detector nuisances) is exactly
\[
\boxed{\mathcal I_{x\mid\eta}/N=7.5\,\eta\,f(1-f)\,I_{24}.}
\]
The optimum in this *specific two-run model* is the balanced \(f=1/2\). For \(\eta=0.75\),
\[
\boxed{\operatorname{tr}(\mathcal I^{-1})=17.0666666667/N}
\]
for locally unbiased estimators. RMS \(\le 0.001\) therefore has a **Cramér–Rao necessary condition** \(N\gtrsim17.07\) million total launches. This is neither a finite-shot sufficiency bound nor a universal hardware count. If all efficiencies are already known, the coefficient becomes \(3.2/\eta=4.266667\), showing the cost of independent reference calibration. Exact numerical Schur-complement eigenvalues were checked for reference fractions 0.10, 0.25, 0.50, 0.75, 0.90, treating all40 nuisance efficiencies independently rather than constraining them equal in the fit.

**Identifiability restriction:** Without a trusted reference there is an exact gauge ambiguity \(\eta'_i=\eta_i t_i/t'_i\) between chart selection and detector response, as previously proved in \`analysis/toe_20261121_five_physical_gates_decoder_blinding_z2.py\`. This front measures the penalty of breaking that ambiguity, not self-calibration from more unknown-source states.

## 2 — SDP-optimal CPTP recovery surpasses Petz on the fixed encoded qubit

Reuse the previous 4→9 Witting-derived channel's five Kraus matrices and the explicitly stored 4×2 encoded qubit isometry. Petz/transpose recovery has maximally entangled fidelity
\[
F_e^{\rm Petz}=0.9034972067200646.
\]
For decoder Choi matrix \(J_{\mathcal R}\succeq0\), in output-logical × input-physical ordering, impose \(\mathrm{Tr}_{\mathrm{logical}}J_{\mathcal R}=I_9\). Let \(M=\sum_j|{\rm vec}(K_j^*)\rangle\langle{\rm vec}(K_j^*)|\), with the transposed index order specified by the script. Then \(\max_{J_{\mathcal R}}\mathrm{Tr}(M J_{\mathcal R})/4\) is a finite semidefinite program for the optimal trace-preserving completely positive recovery of the **fixed** qubit subcode.

The executed SCS solver returned approximately
\[
\boxed{F_e^{\mathrm{SDP}}=0.91658597168}
\]
(an improvement of **0.013088765**), equivalent to mean pure logical-qubit fidelity \((2F_e+1)/3=0.94439065\), versus Petz's \(0.93566480\). The computation explicitly checked the positive-semidefinite Choi constraint, trace preservation, and its independently reconstructed Petz Choi objective. Further SDP evaluations of 5% and 15% completely depolarizing output replacement passed the same optimizer-versus-Petz assertions; their detailed coefficients were written to the workstation-only JSON and are **not repeated here without direct retrieval**.

This is a numerical **global optimum over all CPTP decoders for the fixed encoder**, conditional on the solver tolerance—not over every 4×2 encoder, and not a hardware recovery. See *Optimality Condition for the Petz Map*, Phys. Rev. Lett. 134 200602 (2025), https://doi.org/10.1103/PhysRevLett.134.200602, and *Entanglement fidelity of the Petz decoder for one-shot entanglement transmission* (2026), https://pubs.aip.org/aip/jmp/article/67/10/102203/3405676/ .

## 3 — Noncircular four-qubit compilation of the 45 Witting chart unitaries

The chart ququart space splits into two orthogonal two-dimensional SIC blocks. For chart z, a local 4×4 unitary S_z maps the first block to canonical block qubit 0 and the second block to block qubit 1. Encode two ququarts into four computational qubits ordered \((b_1,s_1,b_2,s_2)\) (block, spin for each).

The exactly specified chart gate at \(t=3\pi/8\) is \(U_z=I_{16}+(-1-i)(3Q_z/4)\), which applies phase \(-i\) to the symmetric two-spin sector **only when the block bits agree**. In canonical coordinates, a noncircular circuit is:

1. CNOT \(b_1\to b_2\) computes the block parity in the second block bit.
2. CNOT \(s_1\to s_2\), then H on \(s_1\), maps the internal antisymmetric singlet to \(|11\rangle\).
3. Apply phase \(-i\) when the parity bit is zero; then a compensating \(+i\) phase only when parity=0 and the Bell-transformed internal bits equal11.
4. Reverse both transforms and conjugate by \((S_z\otimes S_z)\) on the input and output.

The three-bit conditional phase is itself a diagonal computational gate expressible through seven nonconstant Z-parity rotations and at most ten additional CNOTs. Hence a conservative **upper bound of 14 CNOTs and two Hadamards, plus one single-qubit phase, parity rotations and two local 4×4 basis changes**, follows with no entangled *resource state containing U_z*. All45 full 16×16 target unitaries were reconstructed in the executed producer with residual below \(10^{-10}\). It is **not** a passive-photonic gate: a physical apparatus must supply deterministic native qubit entanglers and the S_z basis changes. This route removes resource circularity *in a universal qubit circuit model*, not the photon-photon interaction bottleneck. Photonic entangling-gate resources remain nontrivial: https://www.nature.com/articles/s41467-022-32083-9.

## 4 — Exact symmetry barrier to 24D transitions in the chart adjacency algebra

Write the three chart spectral projectors
\[
P_1=J/45,\quad
P_{20}=(9I+3A-J)/18,\quad
P_{24}=(15I-5A+J)/30.
\]
For **every** real or complex linear combination \(F=aI+bA+cJ\), the algebraic identities show \([F,P_{24}]=0\) and \(P_\mu F P_\nu=0\) for distinct sectors \(\mu,\nu\in\{1,20,24\}\). The producer verified these identities numerically to \(\sim10^{-15}\). A chart-local rank-one defect \(D_z=|z\rangle\langle z|\) violates this block decomposition, but uniform group-orbit/twirl averaging over all45 chart sites yields exactly \(I/45\), removing the mixing.

Therefore a gauge-invariant operator of the form \(W\otimes F\), where W is any Wilson operator and \(F\in\mathrm{span}\{I,A,J\}\), **cannot drive transitions** among the internal 1+20+24 chart sectors. This is a *Bose–Mesner adjacency-algebra obstruction*, **not a no-go for every possible covariant tensor interaction with further dynamical fields**.

Symmetry-preserving energy ordering *can* be tuned without inserting \(P_{24}\) explicitly: the simple chart term \(\Delta(12I-A)+\lambda A\), with \(\Delta=0.01,\lambda=0.2\), assigns energies 2.4, 0.69 and -0.45 to the 1-, 20- and 24-dimensional sectors. This favors the 24D ground eigenspace but does not mix it with the others, and the coefficient choice is engineered. The parallel commit \`83b736e8\` already analyzed the rank-one defect's *three-component cyclic block* and a genuine gauge-ring benchmark; this pass examines the **opposite symmetric limit** rather than claiming their work.

## 5 — Optimal one-shot privacy of the 25-bin Witting detector, with Fisher cost

For a uniformly random chart, retain exactly 24 of the 40 ray identities as separate detector labels; pool the other16 into a single bin. The outcome entropy \(H(Y)\) is subset-independent (24 bins of marginal probability 1/40 and one of probability16/40). For each chart z let \(s_z\) be the number of its eight rays in the pooled bin. Then \(H(Y|z)=3-(s_z/8)\log_2s_z\). Therefore
\[
\boxed{I(Z;Y)=H(Y)-3+\frac1{45\cdot8}\sum_{z=1}^{45}s_z\log_2 s_z.}
\]
The s_z are integers 0..8 and \(s_z=8-\sum_{i}H_{zi}x_i\), where \(x_i\in\{0,1\}\) selects an individually labeled ray and \(\sum_i x_i=24\). Since \(s\log_2s\) is convex, its successive-integer secants yield an **exact mixed-integer linear epigraph at every feasible integer s**. The executed HiGHS MILP returned status0 and **reported zero optimality gap**. It also established that the perfectly balanced but unrealizable chart pooling pattern (36 charts containing3 pooled rays, 9 containing4) is infeasible.

One globally minimum-leakage witness is the **zero-indexed set of 24 resolved Witting rays**
\`\`\`
[0,1,2,5,6,8,10,11,12,13,15,16,19,21,23,24,27,28,30,32,34,35,37,39]
\`\`\`
with row-wise pooled count distribution \(\{2:4,\ 3:30,\ 4:9,\ 5:2\}\). It has
\[
\boxed{I(Z;Y)=1.40488894487\ \text{bits per chart choice},}
\]
compared with \(1.43591772774\) for the earlier 25-bin design and \(2.32192809489\) for all40 ray labels. Its 24D response has full rank; however its local Fisher A-criterion coefficient \(\mathrm{tr}(F^{-1})\) is **30.4** per detected photon, versus **11.8133333** for the previous 25-bin subset and **3.2** with all40 labels.

This is a **provable optimum in the stated one-shot, uniform-prior, exactly-24-plus-16 family, conditional on the numerical MILP solver's certificate**, not a general privacy protocol, cryptographic secrecy, or optimality among all physically implementable POVMs. The producer also ran local ray-swap Pareto refinement for privacy-penalty weights 0, 100, 400, and 1000; these full details remain in its workstation-only result JSON.

## Follow-up priorities

1. Calibrate stable ray efficiencies with an independently trusted chart reference, **including every no-click**, and compare a balanced calibration/target allocation against cost asymmetries.
2. Extract an explicit quantum circuit or approximate Kraus decomposition for the SDP-optimal 9→2 recovery; test whether practical gate counts erase its 1.3-point fidelity advantage.
3. Test the canonical four-qubit chart phase gate on an actual universal-qubit simulator with a standard-gate transpiler; count basis-change cost and verify which photonic resources could implement the nonlocal entanglers.
4. Replace the imposed \(W\otimes F(A)\) chart coupling with an equivariant *dynamical* chart-indexed field and test whether 24D transitions survive without symmetry breaking.
5. Optimize the **privacy-Fisher Pareto frontier** under calibration errors and realistic hardware grouping; use the global 1.40489-bit bound only as a restricted one-shot mathematical baseline.

**Operational status:** GitHub had advanced in parallel to \`850e85d2...\` while Desktop Commander reached its monthly quota. No existing code was overwritten, no local reset/rebase was attempted, and **this GitHub report does not synchronize the authorized Windows worktree**. The computational producer passed on Windows but its uncommitted files need reconciliation when remote tools are available. No claim is made that current CI validated this report.
