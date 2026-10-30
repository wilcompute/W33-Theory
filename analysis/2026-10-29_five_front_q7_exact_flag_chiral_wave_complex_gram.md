# 2026-10-29: five-front deep continuation — exact W(3,7) localized kernels, one-flag circuit, K-even chiral ground manifold, Heisenberg wave, arbitrary complex-Gram photonic minimax

**Research status.** This work is an independent, reproducible continuation of the W33-Theory repository and its existing \([[40,8,6]]_2\) adjacency CSS code, W(3,7) \([[400,48,d]]_2\) with \(10\le d\le14\), finite H27 group, and fixed-input/fixed-output W33-versus-dual optical witness. It presents **new deductions, exact computations and falsifiers**, not a proven Theory of Everything, emergent Standard Model, cosmic vacuum or physical photonic device.

## Front 1. An exact locality theorem covering every pair and triple of q7 lines

Program: \`analysis/cpp/w33_20261029_q7_three_line_support.cpp\`. Independently rebuild every one of the 400 normalized points in \(\mathbf F_7^4\), every symplectic collinearity adjacency vector and all 400 isotropic eight-point lines. For a union \(U\) of \(m\) distinct lines, compute the rank of the 400-by-\(|U|\) adjacency submatrix over \(\mathbf F_2\). The supported binary adjacency-kernel dimension is \(|U|-\operatorname{rank}_{2}(A_{\cdot,U})\).

Exhaustive **79,800 line pairs**:
- 68,600 skew pairs, \(|U|=16\), supported kernel dimension **1**;
- 11,200 intersecting pairs, \(|U|=15\), supported kernel dimension **1**.

Exhaustive **10,586,800 line triples**:
- 571,200 unions of 22 points, supported kernel dimension **2**;
- 3,292,800 unions of 23 points, supported kernel dimension **2**;
- 6,722,800 unions of 24 points, supported kernel dimension **2**;
- **zero exceptions**.

Each isotropic line incidence vector has the same nonzero adjacency syndrome, the all-ones vector, because every external point has exactly one collinear point on the line and every point of that line has \(q=7\) collinear points within it. Therefore differences of line vectors lie in the kernel, and the two independent differences among three distinct line indicators supply a 2D subspace. The rank computation proves these generators exhaust **all** supported kernel vectors; all nonzero words in a union of up to three lines are pairwise symmetric differences, of weight 14 (meeting lines) or 16 (skew lines).

**New rigorous exclusion:** any W(3,7) kernel codeword of weight 10 or 12 cannot be contained in **any** union of up to three isotropic lines. This does **not** exclude arbitrary non-line-local support and does not close exact \(d\); the independently certified distance interval remains \(10\le d\le14\). The C++ enumerator checks the full \(400\choose3\) universe rather than random samples. The result is a structural finite-geometric theorem, not a physical prediction.

## Front 2. Explicit one-flag extraction, and what it does not prove

Program: \`analysis/w33_20261029_flag_one_fault_certificate.py\`, using the previous exact 132-coupling, 16-check W33 CSS basis (\(15\) weight-eight and \(1\) weight-twelve; maximum incidence \(4\)). For measurement of each *Z*-type generator \(h\), consider the circuit
\[
\operatorname{CNOT}(\text{flag}\to\text{syndrome}),\ 
\prod_{j\in \operatorname{supp} h}\operatorname{CNOT}(\text{data}_j\to\text{syndrome}),\
\operatorname{CNOT}(\text{flag}\to\text{syndrome})
\]
with syndrome ancilla initially \(|0\rangle\), measured in Z, and flag ancilla initially \(|+\rangle\), measured in X. Conjugate each of the 15 nonidentity Pauli faults inserted after each two-qubit gate through all remaining CNOTs by **exact binary symplectic Pauli propagation**. Also analyze all single-ancilla Pauli preparation faults.

Number of fault insertions across the sixteen Z-check circuits:
\[
15\left[(15\cdot8+12)+2\cdot16\right]=2460.
\]
For each final data Pauli \(E\), compute the smaller physical support of \(E\) and \(Eh\), because the measured generator itself acts trivially on codespace. Every case of residual weight at least three has a nontrivial Z flag on the flag ancilla. **Zero dangerous unflagged cases** under this precise single-Pauli-fault model. The X sector is related by the Hadamard-dual circuit, but a full schedule of concurrent X/Z checks, repeated rounds, realistic leakage, measurement faults, correlated errors, and recovery is **not** simulated. A single-flag capture is a diagnostic **building block**, not a proof of distance-six fault tolerance or a threshold. Published flag ideas are prior art, e.g. Chao–Reichardt, *Flag Fault-Tolerant Error Correction for any Stabilizer Code*, PRX Quantum 1, 010302 (2020), https://doi.org/10.1103/PRXQuantum.1.010302 .

The parallel naive single-ancilla circuit without flags demonstrably allows weight-three hook errors. The flag result explains which new circuit resource catches them.

## Front 3. A K-even H27 Hamiltonian with opposite chiral ground sectors

Program: \`analysis/w33_20261029_K_even_chiral_ground_doublet.py\`. Use the actual 27-element H27 group law
\[
(a,b,c)(x,y,z)=(a+x,b+y,c+z+ay)\pmod3
\]
and its unitary regular left-translation generators \(X,Y,Z\), with \(XY=ZYX\) and central \(Z\). Put \(O=i(Z-Z^{-1})\), a Hermitian *K-odd* chirality operator, and consider the **real, K-even** Hamiltonian
\[
H_g=X+X^{-1}+Y+Y^{-1}-gO^2
=X+X^{-1}+Y+Y^{-1}+g(Z+Z^{-1})-2gI.
\]
Here the positive central hopping \(g\) is **an explicitly chosen free coupling**, not a predicted physical constant. At \(g=\tfrac14\), exact diagonalization (unitary residuals below \(10^{-11}\)) certifies:
- Six ground states at energy \(-2-3g=-11/4\);
- Three states with \(O=+\sqrt3\), three with \(O=-\sqrt3\);
- The remaining spectrum starts at \(-2\), giving gap \(3g=3/4\).

Thus a microscopic Hamiltonian with no explicit K-breaking term admits **degenerate, K-exchanged chiral ground sectors**. The finite system does not spontaneously select either orientation: a K-invariant mixture has zero chirality. An actual infinite-volume symmetry-breaking theorem, selection rule, mechanism of observed chirality, or physical scale is still missing. The result is a finite, exact illustrative mechanism, not a cosmological vacuum solution.

## Front 4. Exact graph-causal propagation from intrinsic H17 addresses

Program: \`analysis/w33_20261029_Hp_exact_causal_wave.py\`. On the four-regular Cayley graph of H_p (two generators \(X^{\pm1},Y^{\pm1}\)), set \(B=A/4\) and define a discrete wave recurrence \(u_{n+1}=2Bu_n-u_{n-1}\) with \(u_0=\delta_e,\ u_1=B\delta_e\). The normalized adjacency \(B\) is real self-adjoint with spectrum in \([-1,1]\). It has an exact invariant quadratic energy
\[
E(u_n,u_{n-1})=\|u_n\|^2+\|u_{n-1}\|^2-2\langle u_n,Bu_{n-1}\rangle.
\]
Using *exact rational arithmetic* (no floating-point tolerance), the producer checks \(E=3/4\) for six steps on H17 with 4,913 vertices and the sharp graph-local support restriction \(\operatorname{supp}u_n\subseteq B_n(e)\). Cayley ball sizes through radius six are \(1,5,17,53,135,299,593\). This is a working **finite graph light cone**, not a physically calibrated light speed, a Lorentzian metric, relativity principle or dynamically curved geometry. The H_p family remains sub-Riemannian.

## Front 5. New exact photonic minimax under *different*, arbitrary complex Gram states

Program: \`analysis/w33_20261029_adversarial_complex_gram_optical.py\`.

For the prior W33-versus-dual interferometers with the same three *fixed input ports* (0,7,9) and the same event of any three of four *fixed output ports* (4,14,23,32), denote the normalized photon internal Gram variables
\(x=|g_{01}|^2,\ y=|g_{02}|^2,\ z=|g_{12}|^2,\ R=\mathrm{Re}(g_{01}g_{12}g_{20})\). Prior repo exact scattering enumerations yielded
\[
15^6 P_W=17496(1+x+y+z+2R),\qquad
15^6 P_D=3376(1+x)-1024(y+z)-2048R.
\]
Previously, the repo had a bound comparing these at **the same** arbitrary complex Gram \(G\), and separate uniform-real-overlap minimax tests. This packet permits the internal Gram state to vary **independently between hypotheses** and even between independent trials. Because \(x,y,z\in[0,1]\),
\[
R\ge-\sqrt{xyz},\quad \sqrt{xyz}\le(x+y+z)/3,\quad 2\sqrt{xyz}\le y+z.
\]
It follows analytically, universally, and **sharply** that
\[
P_W\ge17496/15^6,\qquad P_D\le6752/15^6.
\]
The W lower bound is attained by *three mutually orthogonal internal states*. The D upper bound is attained by *two identical internal states, third orthogonal*. Both are valid positive semidefinite Gram matrices, so the gap is the **true worst-case across separately chosen Grams**, not merely a loose sufficient bound.

By convexity of independently prepared product-state mixtures, the same two bounds also hold for independently mixed photon states. They are *not* asserted for arbitrary entangled input photons or correlated trial sequences.

Under independent events with each of the two classification error tails strictly below \(0.001\), a globally exhaustive integer threshold search yields the **minimum \(N=43{,}047\), decision cutoff \(43\)** with no loss, compared with the earlier calibrated-real-overlap \(20,333\) or fixed-distinguishable \(19,427\). Even if photon internal Grams vary arbitrarily trial by trial, the same binomial endpoint tails dominate the independent Poisson-binomial tails (stochastic monotonicity). Per-hypothesis unknown *full-threefold survival* bounded by \(\eta^3\le r_h\le1\), with no false registrations, gives:
- \(\eta=0.98\): \(N=50,833\)
- \(\eta=0.95\): \(N=66,814\)
- \(\eta=0.90\): \(N=115,319\)
- \(\eta=0.85\): \(N=235,421\).

Conservative separate unitary calibration: a per-device one-particle unitary operator-norm error \(\epsilon\) perturbs any three-photon event probability by at most \(3\epsilon\). Hence two devices remain separated for \(6\epsilon<10744/15^6\), or \(\epsilon<0.0001572053\). This is an **assumed sufficient certification margin**, not a measured instrument tolerance or complete model of mode-dependent loss and dark counts.

Scientific prior art: three-particle distinguishability and mixedness cannot generally be reduced to pairwise HOM overlap, as demonstrated in *Distinguishability and mixedness in quantum interference*, Phys. Rev. A **108**, 053701 (2023), https://doi.org/10.1103/PhysRevA.108.053701 ; and recent Gram-matrix tomography proposals such as arXiv:2610.06736. This packet is a specifically W33-versus-dual fixed-port result within standard quantum optics. It is **not** a beyond-QM or TOE signature.

## Reproduce

- \`g++ -O3 -std=c++20 analysis/cpp/w33_20261029_q7_three_line_support.cpp -o q7three && ./q7three\`
- \`python analysis/w33_20261029_flag_one_fault_certificate.py\`
- \`python analysis/w33_20261029_K_even_chiral_ground_doublet.py\`
- \`python analysis/w33_20261029_Hp_exact_causal_wave.py\`
- \`python analysis/w33_20261029_adversarial_complex_gram_optical.py\`
- \`python -m unittest discover -s tests -p test_w33_20261029_five_front_deep_continuation.py -v\`

All assertions deliberately fail on a false certificate. The numerical optical threshold scans require NumPy/SciPy; the chiral solver NumPy; the q7 program only a C++20 compiler. Preserve the shared Windows repo's preexisting modifications; use the previously prepared isolated sparse worktree or GitHub-connected writes.

## Top five independent remaining gaps

1. Prove absence or construct a genuine weight-10/12 W(3,7) kernel word with support **not contained in any three-line union**; this is the new reduced falsifier.
2. Compose flagged checks into repeated full X/Z syndrome rounds and prove fault recovery for *two arbitrary faults*, including readout/ancilla preparation/leakage and a real logical magic-state gadget.
3. Generalize the K-even H27 chiral doublet to a local thermodynamic lattice with a controlled symmetry-breaking transition, and explain why observed chirality rather than its conjugate is selected.
4. Find an intrinsic Lorentzian continuum from a W33/H27 tower with dynamical metric; the graph-causal wave model is an intentionally explicit *control*, not the solution.
5. Integrate the optical worst-case Gram bound with laboratory-calibrated complex transfer matrices, nonuniform loss and correlated dark-count intervals; run a realistic detection simulation and experimental protocol.


## Independent follow-through: exact two-fault no-go for the one-flag candidate

Producer: \`analysis/w33_20261029_one_flag_two_fault_no_go.py\`. The positive single-fault result above was never a full two-fault extraction theorem. Enumerating all pairs of distinct faulty CNOT locations **within each of the sixteen Z-check circuits**, with all 15 nonidentity two-qubit Pauli faults at each location, gives **26,112** cases in which both faults' syndrome-to-flag parity cancels yet the final data error has **weight at least three even modulo the measured stabilizer**. The first explicit certificate is on check \`0x40201010b8\`: a syndrome-\(Z\) fault at the first flag CNOT and another syndrome-\(Z\) fault at the third data CNOT yield unflagged data-\(Z\) support \`0x38\`, residual weight three. Both faults occur at different CNOTs. This proves the **specific one-flag schedule is inadequate for arbitrary two-fault recovery**, without implying that verified cats, larger flag registers or repeated rounds cannot work. Because no full syndrome decoder or noisy extraction is present, a positive quantum threshold is **not** established.
