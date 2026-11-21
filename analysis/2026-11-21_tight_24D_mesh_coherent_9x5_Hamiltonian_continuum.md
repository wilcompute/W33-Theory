# Witting–Hermitian six-front continuation: optical meshes, exact 24D tight-frame tomography, coherent 9x5 channel, two-copy Hamiltonian, and continuum/memory falsifiers

**Date:** 21 November 2026. **Baseline:** W33-Theory `master` at commit `79704c11e3e669a43948ededf2f45ce9bc98426f`. **Files:** producer `analysis/toe_20261121_fivefront_tightframe_coherent_memory.py`, frozen machine-readable results `data/toe_20261121_optical_tightframe_coherent_Hamiltonian_causal.json`, tests `tests/test_toe_20261121_fivefront_tightframe_coherent_memory.py`.

**Provenance:** This investigation starts from the full previously committed native source `analysis/toe_20261121_hermitian45_pauli_sic_bridge.py`, `analysis/toe_20261121_27decks_fivefronts.py`, `analysis/toe_20261121_fivefront_physical_falsifiers.py` and audits existing geometry: 40 Witting ququart projectors \(P_i\), 45 GF4 Hermitian-point chart supports \(S_z\), 27 five-chart schedules, \(PGU(4,2)\cong PSp(4,3)\) projective symmetry. The abstract Witting/SRG/GQ group symmetries and the existence of projective 2-designs, generalized quadrangle eigenspaces, Reck/Clements decompositions, Naimark dilations, and quantum-memory fidelity thresholds are established classical or prior-repo facts. This run supplies **new explicit certificates and a combined experimental interface**, not new fundamental physics.

## Result 1 — All 45 eight-outcome Witting analyzers now have actual mesh descriptions

For each chart z, the previously validated \(8\times4\) Naimark isometry has rows \(V_{zi}=\langle r_i|/\sqrt2\), \(i\in S_z\), with \(V_z^\dagger V_z=I_4\). Compute a unitary \(U_z=[V_z\;C_z]\) where the four columns of \(C_z\) are an explicit orthonormal complement. Use adjacent-row complex Givens eliminations to decompose \(U_z\) into two-mode beam splitters and a diagonal phase layer. Reconstruct all 45 unitaries and check the maximum matrix residual below \(10^{-10}\).

**Measured in the script:** all 45 have **27 or 28 adjacent-rail two-mode unitaries**, including the trivial/degenerate gate simplifications of this particular Reck-style QR factorization. This is an explicit implementation sequence, *not* an optimized rectangular Clements circuit, hardware layout, control voltages, actual fabricated chip, or realistic thermal/power budget. Academic prior art: Reck et al., PRL 73 (1994); Clements et al., Optica 3 (2016), arXiv:1603.08788; open implementation https://github.com/clementsw/interferometer .

**Robust chart selector versus adversarial detection:** for nonorthogonal Witting inputs a,b and chart z, the two-copy matching probability is
\[
 p_z(a,b)=\tfrac14\sum_{i\in S_z}
 |\langle r_i|r_a\rangle|^2|\langle r_i|r_b\rangle|^2=\tfrac14 F_z(a,b).
\]
Each nonorthogonal pair has one ideal chart with \(F=8/9\); the next-best score is \(5/9\). If an arbitrary chart/output detector has efficiency \(\eta_{zi}\in[\eta_{\min},\eta_{\max}]\) and independent two-copy losses, the **unconditioned** matched-event probability is
\[
 p_z^\eta(a,b)=\tfrac14\sum_{i\in S_z}\eta_{zi}^2
 |\langle r_i|r_a\rangle|^2|\langle r_i|r_b\rangle|^2 .
\]
The true maximizing chart must survive arbitrary per-chart/per-port losses whenever
\[
 \boxed{\eta_{\min}/\eta_{\max}>\sqrt{5/8}=0.790569415\ldots}.
\]
This bound derives from lower-bounding the true score and upper-bounding all alternatives and is **uniform over all 540 nonorthogonal input pairs**. A fixed-seed experiment with 45x8 efficiencies chosen uniformly in [0.80,1] verifies all 540 maxima. The condition is close to sharp: setting all eight ports of the winner to .79 and all others to1 **reverses the winner** for input pair (0,5). This is not a guaranteed QKD security condition and does not include dark counts, correlated loss, drift or heralding.

## Result 2 — Exact tight frame; complete and sparse hidden-chart tomography

Let \(A\) denote the SRG(45,12,3,3) adjacency on Hermitian chart labels and \(J\) the all-one matrix. Let \(K\) denote the 45x27 binary incidence matrix of the complete five-chart schedules. Its 24-dimensional nullspace is exactly the \(-3\) eigenspace of A. Set
\[
 M=15I-5A+J,\qquad M^2=30M,\qquad P_{24}=M/30.
\]
The explicit integer matrix has trace720, and \(K^\top M=0\), so \(P_{24}\) is the **exact rational spectral projector** onto \(\ker K^\top\), rank24.

For each distinct unordered ray pair a,b, let \(F_{ab}\in\mathbb R^{45}\) be the raw 45-chart matched-coincidence profile and \(c_{ab}=F_{ab}-\overline F_{ab}{\bf1}\). Their overlaps take exactly values0,1/3,1. Therefore define \(W_{ai}=3|\langle r_a|r_i\rangle|^2\in\{0,1,3\}\), \(T_{z,ab}=\sum_{i\in S_z}W_{ai}W_{bi}=9F_z(a,b)\), and integer centered vectors \(X_{ab}=5T_{ab}-(\sum_zT_{z,ab}/9){\bf1}=45c_{ab}\).

The original count/rank arguments can now be strengthened to exact **full covariance identities**, all checked by literal integer multiplication:
\[
\boxed{
X_{\perp}X_{\perp}^\top=540M,\quad
X_{\not\perp}X_{\not\perp}^\top=360M,\quad
XX^\top=900M.
}
\]
Equivalently,
\[
\sum_{a<b,\,a\perp b}c_{ab}c_{ab}^\top=8P_{24},\quad
\sum_{a<b,\,a\not\perp b}c_{ab}c_{ab}^\top=\frac{16}{3}P_{24},\quad
\sum_{a<b}c_{ab}c_{ab}^\top=\frac{40}{3}P_{24}.
\]
Thus both the 240 orthogonal probes and the 540 nonorthogonal probes **separately form tight frames on the same 24D sector**. This is much stronger than finite rank: the full-set inversion is explicitly isotropic on that sector.

**An operational, carefully scoped tomography example:** Assume an *unknown classical probability distribution* \(w_z=1/45+x_z\), describing which of the 45 chart analyzers a controller selects, with \(x\in\ker K^\top\), \(x\ne0\), and all \(w_z>0\). Then every one of the 27 complete-deck totals has the same probability as uniform chart selection, because \(K^\top x=0\); the hidden bias is undetectable by such totals.

Now prepare two Witting states a,b, let the controller select a hidden chart, and discard its label after recording whether the two double-SIC outcomes match. The input-pair-dependent excess probability is
\[
 y_{ab}=\frac14\,c_{ab}^\top x=R_{ab}^\top x,\quad
 R_{ab}=c_{ab}/4.
\]
For **just the 540 nonorthogonal pairs**, the tight-frame identity gives \(RR^\top=\frac13P_{24}\) and hence the **exact closed-form decoder**
\[
 \boxed{x=3R\,y\ \ \text{(noiseless)}}.
\]
A fixed-seed nonuniform yet positive \(w\) passes all 27 deck-indistinguishability checks and is recovered to numerical precision. Pivoted QR selects **24 nonorthogonal probe pairs** whose 45x24 profile matrix is full-rank (certified mod7) and has 2-norm condition number **5.4068**; these 24 suffice in the *noiseless* synthetic model.

**Shot budget is the obstacle.** With independently calibrated Bernoulli matching observations, n trials per nonorthogonal pair (540n total), the analytic tight-frame decoder has
\[
\mathbb E\|\hat x-x\|_2^2\le 18/n,\qquad
{\rm RMS}\le\sqrt{18/n}.
\]
For RMS error guaranteed by this conservative bound below .001, one would need at least18 million trials per pair, or **9.72 billion trials total**. Synthetic binomial draws at n=1000, 100000, 1000000 per pair yield measured L2 reconstruction errors approximately .0881, .00943, .00265 respectively. These are *simulations*, not observations. Clever correlated probes or constrained priors could improve efficiency, but no such improvement is claimed. The 24-probe sparsity result is noiseless and should not be presented as a free experimental speedup.

## Result 3 — Genuine coherent channel with a 9-level output and a 5-level environment

The prior \(\mathbb C^4\to\mathbb C^9\) measure-and-prepare bridge was entanglement-breaking. The new channel uses a **different, coherent Naimark construction**:
\[
 B:\mathbb C^4\longrightarrow\mathbb C^{45}
 \cong\mathbb C^9\otimes\mathbb C^5,\qquad
 B_{i,*}=\langle r_i|/\sqrt{10}\quad(i=1,\dots,40),
\]
with five extra zero rows. The full isometry satisfies \(B^\dagger B=I_4\) and measuring the first 40 computational-basis outputs gives **exactly** the Witting informationally complete POVM \(\{P_i/10\}\). Its pure Choi state has four Schmidt coefficients1/2, so it preserves all coherent input entanglement when the total 9x5 output remains available.

For a simultaneous **one-shot 40-orthogonal-click Naimark realization** with a nine-dimensional output factor, the auxiliary factor needs at least \(\lceil 40/9\rceil=5\) dimensions. This is a factorization/resource count, **not** a general lower bound on all possible adaptive or sequential devices.

Discard the five-dimensional factor to obtain a CPTP map \(\mathcal N:\mathbb C^4\to\mathbb C^9\) with five explicit 9x4 Kraus operators (one per environment index). Its normalized 36x36 Choi matrix is positive and **rank5**, but its partial transpose has negative eigenvalues with negativity **0.5420426628**. Therefore \(\mathcal N\) is **not entanglement-breaking**, sharply unlike the previous interface. This proves that coherent two-qutrit-Hilbert-space output is possible with an auxiliary environment. The 40 clicked mode assignments to C9xC5 are arbitrary and break the projective Pauli symmetry. **No Pauli covariance, intrinsic two-qutrit encoding, unassisted quantum-capacity positivity, photonic chip, or reversible reduced nine-dimensional decoder has been established.**

General Naimark/Stinespring constructions are standard; relevant sources include https://sirui-lu.com/QICLean/docs/QICLean/Channel/POVM/RankOneNaimark.html and https://www.nature.com/articles/s41566-026-02035-6 (hardware context, not evidence for our device).

## Result 4 — A genuine, explicitly computable two-copy quantum Hamiltonian

The earlier 'selector' was a programmed scalar score. Define a real Hermitian positive **two-ququart** observable
\[
 Q_z=\sum_{i\in S_z}P_i\otimes P_i,\quad H_z=-Q_z,
 \qquad Q_z\in\operatorname{Herm}(\mathbb C^4\otimes\mathbb C^4).
\]
Each chart z has two orthogonal rank2 subspaces with projectors \(\Pi_{z,L},\Pi_{z,R}\), and its eight Witting rays form two qubit tetrahedral SICs. Their projective 2-design identity gives the **exact operator law**
\[
\boxed{Q_z=\frac43\left[\Pi_{\mathrm{sym}}(\Pi_{z,L}^{\otimes2})
+\Pi_{\mathrm{sym}}(\Pi_{z,R}^{\otimes2})\right].}
\]
The two projectors on the right have rank3 each and mutually orthogonal support. Hence each \(Q_z\) has eigenvalues \(4/3\) (multiplicity6) and \(0\) (multiplicity10), verified for all45. Averaging over charts,
\[
 \sum_{z=1}^{45}Q_z=36\,\Pi_{\mathrm{sym}}(\mathbb C^4\otimes\mathbb C^4).
\]
A chart-controlled Hamiltonian on \(\mathbb C^{45}\otimes\mathbb C^4\otimes\mathbb C^4\) is
\[
 H=-\sum_z |z\rangle\langle z|\otimes Q_z
\quad(\text{Hilbert dimension }720).
\]
For externally prepared nonorthogonal product inputs \(|r_a\rangle|r_b\rangle\), its conditional energies \(\langle H_z\rangle=-F_z(a,b)\) select exactly one chart with a universal energy gap1/3 relative to the runner-up. A norm-bounded Hermitian perturbation \(\|\delta H_z\|\le\epsilon=.1\) cannot close this expectation gap: it remains at least \(1/3-2\epsilon=2/15\).

The conditional two-copy unitary \(e^{-itQ_z}\) is explicitly unitary. For ray inputs0 and5 and generic \(t=3\pi/8\), the selected chart produces an output with Schmidt rank2. This is a **real, mathematically local two-copy Hermitian interaction**, not merely a scalar postprocessing score. Crucially, the 45-valued chart register and projectors are *engineered controls* and independently supplied copies; this is **not a derived microscopic optical nonlinearity** or a self-organizing fundamental Hamiltonian.

## Result 6 — Stronger independent operator-level complementarity and an exact full-45 decoder

A **post-commit research extension** goes beyond the 24D coincidence profiles: the two-copy operator-valued chart measurements themselves carry precisely the 24-dimensional sector that the 27 schedules cannot see. Denote by G_Q the 45x45 Hilbert–Schmidt Gram matrix of the exact two-ququart operators \(Q_z=\sum_{i\in S_z}P_i\otimes P_i\).

**Exact integer arithmetic:** Because \(W_{ij}=3|\langle r_i|r_j\rangle|^2\in\{0,1,3\}\), and \(H\) is the binary 45x40 chart-versus-ray incidence, \(9G_Q=H(W\circ W)H^\top\) is an integer matrix. All 2025 entries obey
\[
\boxed{9G_Q=36I-12A+60J},\quad
G_{Q,zz}=32/3,\quad
G_{Q,zw}=\begin{cases}16/3 & z\sim w\\20/3 & z\not\sim w,\ z\ne w.\end{cases}
\]
Therefore
\[
{\rm spec}(G_Q)=288^{(1)},\quad8^{(24)},\quad0^{(20)}.
\]
Thus the 45 Hermitian chart observables span exactly a **25-dimensional subspace** of the complex Hermitian operators on two ququarts, the uniform component plus the 24D hidden chart sector. The remaining 20D chart-label sector is annihilated exactly.

Let the three mutually orthogonal chart-label projectors be
\[
P_1=J/45,\qquad
P_{20}=(9I+3A-J)/18,\qquad
P_{24}=(15I-5A+J)/30.
\]
The original complete-deck matrix \(K\) obeys \(KK^\top=15P_1+6P_{20}\), while the two-copy operator Gram is \(G_Q=288P_1+8P_{24}\). These are therefore **complementary** on the two nonuniform sectors. Every five-chart Hermitian line sums to the same operator:
\[
\sum_{z\in\text{any complete deck}}Q_z=
\sum_{i=1}^{40}P_i\otimes P_i
=4\Pi_{\rm sym}(\mathbb C^4\otimes\mathbb C^4).
\]
Defining \(\bar Q=\frac1{45}\sum_zQ_z=\frac45\Pi_{\rm sym}\), the centered operator Gram is
\[
\operatorname{Tr}\bigl[(Q_z-\bar Q)(Q_w-\bar Q)\bigr]=8(P_{24})_{zw}.
\]
An independent *integer-only certificate* is \(5(9G_Q)-288J=12(15I-5A+J)\). Consequently the map \(x\in{\rm im}P_{24}\mapsto O_x=\sum_zx_zQ_z\) is a scaled Hilbert–Schmidt isometry:
\[
\|O_x\|_{\rm HS}^2=8\|x\|_2^2,\qquad
x_z=\frac18\operatorname{Tr}[(Q_z-\bar Q)O_x].
\]
By contrast, an \(x\in{\rm im}P_{20}\) always gives \(O_x=0\). Both statements are verified with seeded 45-component probes and exact spectral projectors.

**Combined completeness:** The pair of *mathematical data types* (all27 deck totals plus chart-resolved two-copy operator overlaps) spans every one of the 45 chart-label dimensions:
\[
\boxed{KK^\top+G_Q=303P_1+6P_{20}+8P_{24}\succ0.}
\]
Given an arbitrary real coefficient vector x, deck totals \(y=K^\top x\), and operator-overlap data \(q_z=\operatorname{Tr}(Q_z\sum_wx_wQ_w)\), an **exact joint decoder** is
\[
\boxed{x=\frac{P_1Ky}{15}+\frac{P_{20}Ky}{6}+\frac{P_{24}q}{8}.}
\]
The 45-dimensional inverse passes an independent seeded numerical test. This resolves the apparent information loss in each individual family at the *abstract operator* level.

**Physical boundary:** obtaining the 45 operator overlaps q requires a real calibrated **two-ququart measurement/tomography** program. It is not the same thing as 27 cheap scalar deck counts, and no hardware-cost, experimental advantage, security or gravitational theory follows solely from a full-rank information matrix. This theorem is a concrete new synthesis of existing generalized-quadrangle and Witting SIC structures, not a new exception to quantum measurement theory.

## Result 5 — Generalized-quadrangle graph continuum obstruction and multitime memory witness

The Hermitian 45-chart SRG has adjacency \(A\) satisfying \(A^2=9I+3J\). Its point-collinearity graph has diameter2, and the normalized nearest-neighbor random walk has
\[
 P=A/12,\qquad P^2=I/16+J/48.
\]
In particular, after precisely two hops any initial vertex has positive probability of reaching *every* vertex. **For any family of generalized quadrangle point graphs**, their shortest-path diameter remains2 (even as field size tends to infinity). If the edge length \(\ell_n\to0\), the physical diameter is at most \(2\ell_n\to0\): the metric-space Gromov–Hausdorff limit is a **single point**, not a nondegenerate spatial manifold, let alone Lorentzian spacetime. Thus the naive GQ graph shortest-path metric cannot generate our required continuum. This is an obstruction to a *specific naive route*, not a no-go against all discrete emergent-gravity theories. Alternative weighted/tensor/causal embeddings and genuinely dynamical geometry remain open. Background mathematics: Godsil's and Brouwer's classical generalized-quadrangle graph formulas; https://www.sciencedirect.com/science/article/pii/S0097316520300261 .

Independently, a 12-state complete qutrit MUB 2-design is an exact test ensemble for average channel fidelity. Under a verified middle-time causal break and assuming the only input-dependent information carrier is the intermediate quantum memory, a channel whose Choi state has Schmidt number at most k satisfies \(F_{\rm avg}\le(k+1)/4\) for k=1,2,3. Therefore >1/2 excludes entanglement-breaking storage, while >3/4 witnesses at least three-dimensional quantum coherence across the memory cut. Source precedent: *Schmidt-number benchmark for genuine quantum memories and gates*, https://arxiv.org/abs/1202.0346, and *Quantifying the fidelity of a quantum memory*, https://arxiv.org/abs/2610.08445 .

For a calibrated qutrit depolarizing channel \(\mathcal E_p(\rho)=(1-p)\rho+pI_3/3\), the ideal average fidelity is \(1-\frac{2p}3\). Thus the k=2 witness survives precisely for \(p<3/8=.375\). Under **strictly independent and ideal Bernoulli trial assumptions**, a test distinguishing null mean<=.75 from an alternative mean>=.80 using threshold .775 needs n>=**3685** total trials for both error risks to be bounded by1% via Hoeffding. Seeded numerical examples at p=.30,.375,.50 reproduce appropriate test classifications. Not a device experiment; uncalibrated SPAM, heralding, adaptive stopping and temporal side channels can void these performance claims.

## Reproduction and limitations

Run, from repo root, in PowerShell:
```powershell
python analysis/toe_20261121_fivefront_tightframe_coherent_memory.py
python tests/test_toe_20261121_fivefront_tightframe_coherent_memory.py
python tests/test_toe_20261121_fivefront_physical_falsifiers.py
python tests/test_toe_20261121_27decks_fivefronts.py
python tests/test_toe_20261121_hermitian45_pauli_sic_bridge.py
```
No network calls or destructive worktree edits are required to regenerate the certificate. This is **six completed finite-mathematical and ideal quantum-computation fronts**, not five working optical devices, an observed time-dependent quantum channel, an Einstein field theory or a proven theory of everything. All external cited studies establish only their own documented statements; no claim was made to have read all the papers on finitegeometry.org during this follow-up. The user-visible site mirror previously recovered at https://m759.github.io/map.html remains a separate bibliographic resource.

## Top five independent follow-ups

1. **Loss-tolerant experimental protocol:** optimize chart-mesh decomposition jointly with port-dependent efficiency, dark counts, temperature drift and event-ready detector calibration; measure whether the mathematically robust \(\sqrt{5/8}\) threshold survives physical resources.
2. **24-probe compressed tomography:** derive optimal Fisher information for hidden chart-selection distributions with nonuniform priors; seek the minimum total photon budget rather than minimum probe count.
3. **Coherent encoding symmetry audit:** optimize the assignment of 40 Witting outcomes to \(9\times5\) output rails under canonical Pauli conjugations and test whether any nontrivial subgroup intertwines exactly.
4. **Two-copy Hamiltonian compilation:** decompose each \(Q_z\) into physically available entangling interactions and test the controls/noise necessary to realize the 1/3 energy-selection gap.
5. **Non-collapsing causality and memory:** derive a growing-distance localized graph family with finite propagation speed and an event-ready multi-slot qutrit process-tensor experiment, keeping the geometric Lorentzian and quantum-information tests logically separate.
