# October 29, 2026 — continuation: four-line q7 exclusion, seven-flag W33 recovery, chirality no-go, intrinsic anisotropy, optical laboratory budget

**Scientific status.** All findings below are finite mathematical, computational-code, or conditional conventional-quantum-optics results. None derives a theory of everything, the Standard Model, emergent physical spacetime, a measured photonic effect, or a new fundamental constant. Distinguish repository-established results from the incremental certificates below.

## 1. W(3,7) exact adjacency-kernel obstruction on EVERY four-line union

**Producer:** \`analysis/cpp/w33_20261029_q7_four_line_fixed.cpp\`. Earlier repository work certified binary adjacency CSS \([[400,48,d]]_2\), \(10\le d\le14\), \(\operatorname{rank}_{\mathbf F_2}A=176\), even sums of isotropic-line indicators generate \(\ker A\), and exact supported-kernel ranks for every union of at most three isotropic lines.

The group \(\operatorname{Sp}(4,7)\) is transitive on the 400 isotropic lines. Thus to exhaust **all** four-line unions, it suffices to fix one line \(L_0\) and take all choices of three others: \(\binom{399}{3}=10,507,399\). The fully compiled C++20 producer constructs PG(3,7), all 400 symplectic lines, all 400 adjacency rows, and computes the exact rank of the 400-by-\(|U|\) binary submatrix for each union \(U=L_0\cup L_i\cup L_j\cup L_k\).

**Exhaustive result: zero exceptions; nullity exactly 3 in every case.** Detailed counts:

| \(|U|\) | \(\dim \ker(A_{\cdot,U})\) | Count |
|---:|---:|---:|
| 28 | 3 | 9,604 |
| 29 | 3 | 340,536 |
| 30 | 3 | 1,775,368 |
| 31 | 3 | 4,148,928 |
| 32 | 3 | 4,232,963 |
| **All** | **3** | **10,507,399** |

Every line vector has adjacency image the all-ones vector. The four line vectors are independent (each line has at least five private points, since it intersects each of the other three at most once). Therefore their **three-dimensional even-sum subspace** lies in the supported kernel; the exhaustive rank count proves this subspace **is** the supported kernel. Any nonzero even sum of these four lines has weight at least 14 (two intersecting lines have weight 14; two disjoint lines 16; four-line XOR has weight at least \(4\cdot8-2\binom42=20\)). Hence **no binary kernel word of weight 10 or 12 is contained in any union of at most FOUR isotropic lines**. This is an exact, symplectic-orbit-complete exclusion, but it does not prove global \(d=14\): supports outside all such unions remain.

**Reproduce:** \`g++ -O3 -std=c++20 analysis/cpp/w33_20261029_q7_four_line_fixed.cpp -o q7four && ./q7four\`. Server Linux compilation and exhaustive execution completed in approximately 9.25 seconds before adding redundant histogram assertions.

## 2. W33 improved flagged two-fault *single-check* recovery: seven flags, 394 two-qubit gates

**Producer:** \`analysis/w33_20261029_seven_flag_sidon_fault_recovery.py\`. Previous round:
- CSS W33 16 independent Z checks, fifteen weight 8, one weight 12, with exactly **132 data CNOTs** and no data qubit in more than four checks.
- Naive unflagged hook errors; one-flag schedule detects all dangerous single faults, **but 26,112 two-fault combinations escape**.
- First eight-flag 16-check candidate verified **4,730,706** within-check fault histories and no recovery-class ambiguity.

This round improves the construction using nonlinear labels in \(\mathbf F_2^7\):
\[
\{0,30,84,113,109,43,67\}
\]
(binary integer representation), which have **minimum pairwise Hamming distance 3** and **21 distinct unordered pairwise XORs** (Sidon property). Distribute data CNOTs into groups of two. Between groups, switch flag-to-syndrome CNOTs corresponding to the bitwise XOR between successive labels. Finish with flag resets in the CNOT parity sense. The minimum-Hamming-path orders among this fixed seven-label set are:
- weight 8: \(0\to30\to84\to113\to67\to0\), **16 flag CNOTs + 8 data = 24 total**;
- weight 12: \(0\to30\to84\to113\to109\to43\to67\to0\), **22 flag CNOTs + 12 data = 34 total**.

Across 16 Z checks, **\(15\cdot24+34=394\) CNOTs**, vs 524 in the first eight-flag implementation, with seven rather than eight flag ancillas per check (reusable when checks are measured sequentially). These are physical gate counts **before** X-check duplication, ancilla preparation, reset, readout or scheduling overhead.

**Fault model and proof:** For each check, enumerate every history with zero, one or two distinct fault locations from: all 15 nonidentity Pauli faults after each CNOT; all three single-qubit Pauli faults immediately after each flag/syndrome preparation; a readout flip on any flag or syndrome; and all three Pauli faults on any data qubit before and after the circuit. Every data qubit participates in at most one data CNOT *in a single check*, so its intermediate idle fault is equivalent to one of those before/after insertions. Conjugate Pauli errors through the full CNOT schedule. The observed recovery key contains the current check-Z readout, all seven flag-X readouts, and an **ideal subsequent full 40-bit X/Z syndrome**. Final data errors are compared **modulo both rank-16 CSS stabilizer row spaces**, not merely by physical bit masks. No observation key may correspond to two inequivalent final data Pauli classes.

Exact enumeration: \(15\cdot632+782=10,262\) elementary faults, \(\sum n(n+1)/2=3,306,573\) at-most-two-fault histories, **0 ambiguous recovery records**, for all sixteen independent checks. The test checks class uniqueness, not just whether a dangerous hook raised a flag. Initial independent Python implementation gave PASS; the repository producer has its own assertions and regression test.

**Boundary is critical:** This is **within one check at a time** and presumes a perfect subsequent full syndrome; it is **not** a proof that two faults distributed across multiple check circuits are distinguishable, nor a noisy repeated-round decoder, leakage-tolerant circuit, logical magic-state operation, or threshold. The use of classical error-correcting codes to build fault-tolerant flag gadgets is **published prior art**, notably Anker et al., *Flag Gadgets Based on Classical Codes*, PRX Quantum 5, 040340 (2024), https://doi.org/10.1103/PRXQuantum.5.040340. The concrete W33 support basis, label scheduling and exhaustive scope are the computational contribution.

**Six-flag boundary within this exact Sidon design:** The compiled \`analysis/cpp/w33_20261029_six_flag_sidon_obstruction.cpp\` exhausts all seven-point subsets of \(\mathbf F_2^6\) up to translation, requiring mutual Hamming distance at least three and unique pair XORs. **No six-bit seven-label set exists**; a five-label set does exist. Thus seven flags are minimal **for this particular 7-label distance-3 Sidon scheduling strategy**, not for all possible quantum error-correction gadgets.

## 3. H27 chiral finite-range interaction: symmetry-breaking channel vs physical selection

**Producer:** \`analysis/w33_20261029_K_even_chiral_chain_no_go.py\`. The previous exact H27 single-cell real Hamiltonian \(H_0-gO^2\), \(O=i(Z-Z^{-1})\), has two opposite-chirality central sectors, each with three degenerate local ground states, at \(E=-2-3g\), while \(k=0\) has minimum \(-2\).

Now **explicitly introduce** a 1D nearest-neighbor interaction \(-J\sum_i O_iO_{i+1}\). Each commuting central-sign sector \(s_i\in\{-1,0,+1\}\) has minimum energy
\[
E(s)=-2N-3g\sum_i[s_i\ne0]-3J\sum_i s_i s_{i+1}
\]
with periodic boundary. With free, externally chosen dimensionless \(g=1/4\), \(J=1/10\), exhaustive \(3^N\) sector checks for rings \(N=3,\ldots,8\) give **precisely two globally aligned sign sectors** at energy \(N(-2-3g-3J)\), each with local degeneracy \(3^N\). The first distinct sector energy is \(12J=1.2\) above the ground sector minimum. Positive/negative infinitesimal symmetry-breaking fields select opposite signs.

**Rigorous limitations:** Since the finite Hamiltonian is K-even, it cannot pick between two K-conjugate ground sectors without an external selection, and any nondegenerate K-even ground state has vanishing K-odd observable expectation. The assumed **one-dimensional finite-range** model has no finite-temperature symmetry breaking: the associated projected three-state transfer matrix has strictly positive entries and thus a simple analytic Perron eigenvalue for finite temperature. There is no spontaneously selected *physical* chirality, cosmological vacuum, or unassumed spacetime. This supports a precise **selection-problem diagnostic**, not a TOE solution.

## 4. Intrinsic Heisenberg graph: exactly why its continuum is *not* Lorentzian

**Producer:** \`analysis/w33_20261029_Hp_intrinsic_subriemannian_obstruction.py\`. For the integer Heisenberg product \((x,y,z)(a,b,c)=(x+a,y+b,z+c+xb)\), take local right-Cayley steps \(X^{\pm1},Y^{\pm1}\) and graph Laplacian \(Lf(g)=\sum_{s\in S} f(gs)-4f(g)\). Exact polynomial tests at 147 integer sample points certify
\[
L(x^2)=L(y^2)=2,\qquad L(z^2)=2x^2,\qquad L(yz)=2x.
\]
And \([X,Y]=Z\), a central shift achieved by a four-step plaquette. This is precisely the horizontal continuum sub-Laplacian
\[
\partial_x^2+(\partial_y+x\partial_z)^2
\]
with anisotropic weights \((1,1,2)\), total homogeneous growth dimension four. A reversible lattice wave constructed from this operator has a finite graph cone but **no** canonical Lorentzian 3+1 geometry; vertical dispersion depends on position and no independent Euclidean \(z\)-direction kinetic term appears at the same scaling order. These are standard Heisenberg/Carnot facts applied to the explicit H27 address tower, not a new theorem of sub-Riemannian analysis.

## 5. Optical laboratory falsifier: complex Gram plus three simultaneously bounded imperfections

**Producer:** \`analysis/w33_20261029_photon_adversarial_loss_calibration_budget.py\`. Previous certified four-port W33-vs-dual three-photon event bounds for **separately adversarial arbitrary complex Gram states**:
\[
P_W\ge17496/15^6=0.001536,\quad
P_D\le6752/15^6\approx0.0005927682.
\]

Assume independent emitted trials; under either hypothesis, unknown but bounded per-photon survival probability \(\eta\le\eta_{\rm true}\le1\), a passive 40-mode transfer-unitary operator-norm error \(\epsilon\) for each device, and an additive false-threefold event probability bounded \(0\le b\le\beta\) but potentially different under each hypothesis. The conservative *sufficient* event-rate certificate is
\[
p_W\ge \eta^3(P_W-3\epsilon),\qquad
p_D\le P_D+3\epsilon+\beta.
\]
The model presumes uniform survival on the relevant events and independent detections; no mode-dependent loss or correlated dark counts. **Separability** requires
\[
\boxed{\eta^3P_W-P_D>3(1+\eta^3)\epsilon+\beta.}
\]
With zero \(\epsilon,\beta\), the minimal guaranteed survival is \(\eta>(P_D/P_W)^{1/3}\), approximately 0.728, just for event-rate separation (not for any finite-shot significance). At fixed \(\eta,\beta\), the strict calibration requirement is
\[
\epsilon<\frac{\eta^3P_W-P_D-\beta}{3(1+\eta^3)}.
\]

The producer exhaustively scans **every integer emitted-trial count up to the optimum** to ensure a fixed-binomial-count decision threshold with false-positive and false-negative upper bounds each strictly below \(0.001\).

| Per-photon survival floor \(\eta\) | \(\epsilon\) | Background ceiling \(\beta\) | Minimum emitted trials | Decision cutoff |
|---:|---:|---:|---:|---:|
| 1.00 | 0 | 0 | 43,047 | 43 |
| 0.95 | \(10^{-5}\) | \(5\cdot10^{-5}\) | **95,513** | **91** |
| 0.90 | 0 | \(10^{-4}\) | 187,342 | 167 |
| 0.98 | \(2\cdot10^{-5}\) | \(10^{-4}\) | 98,767 | 103 |

The Poisson-binomial outcome counts from independent, non-identical but pointwise bounded trials are stochastically bounded by the two endpoint binomial counts, so the decision-error guarantee holds for independent per-trial drifting internal Gram states **within those bounds**. It does not hold under arbitrary temporal correlations or uncontrolled hypothesis-dependent detector effects. Comparable real-world multiphoton distinguishability experiments explicitly model higher-order emissions, transfer-unitary errors and device loss (e.g. *Semi-Device-Independent Characterization of Multiphoton Indistinguishability*, PRX Quantum 6, 020340 (2025), https://doi.org/10.1103/PRXQuantum.6.020340). Gram-matrix tomography is also addressed in Kotowski et al. (2026), https://arxiv.org/abs/2610.06736.

## Reproduction and integrity

- \`g++ -O3 -std=c++20 analysis/cpp/w33_20261029_q7_four_line_fixed.cpp -o q7four && ./q7four\`
- \`g++ -O3 -std=c++20 analysis/cpp/w33_20261029_six_flag_sidon_obstruction.cpp -o sidon6 && ./sidon6\`
- \`python analysis/w33_20261029_seven_flag_sidon_fault_recovery.py\`
- \`python analysis/w33_20261029_K_even_chiral_chain_no_go.py\`
- \`python analysis/w33_20261029_Hp_intrinsic_subriemannian_obstruction.py\`
- \`python analysis/w33_20261029_photon_adversarial_loss_calibration_budget.py\`
- \`python -m unittest discover -s tests -p 'test_w33_20261029_seven_flag_q7_optical_dynamics.py' -v\`

Use the isolated Windows research worktree, not the shared main checkout with tracked modified files and other live sessions; no destructive merge or force push.

## Five independent best next directions

1. Distance: prove or exhibit binary weight-10/12 q7 kernel supports **outside all unions of four lines**, via finite-geometry orbit reduction or certified XOR SAT.
2. Quantum hardware: compose the seven-flag gadgets across all 32 X/Z checks and **simulate two arbitrary faults spanning checks and noisy syndrome rounds**; extract an implementable fully fault-tolerant logical non-Clifford gadget.
3. Chirality: derive a **microscopic coupling** and a genuine thermodynamic K-breaking phase in an internal geometry model without externally positing a spatial lattice, then confront anomalies and physical observations.
4. Geometry: seek a **dynamical causal metric** and calibrated local propagation with Lorentzian signatures; the present Heisenberg sub-Laplacian is a negative control.
5. Optics: measure or rigorously bound the actual **unitary operator-norm errors, mode-resolved efficiencies, false-threefold statistics and temporal correlations** in a candidate device, then compare to the tabulated certified trial budgets.
