# TOE74 — Five independently reproducible W33 validation fronts

**Date:** 14 October 2026. **Baseline:** TOE73 with all subsequent parallel commits preserved. **Method:** native \(\mathrm W(3,3)\) Levi graph construction, rigorous rational polynomial / block operator estimates, exact local-pairing combinatorics, a Dirac-type index control, and full finite canonical many-body matrices. **This is not a proof of a physical Theory of Everything.**

## Ownership and prior art

Compared current GitHub master and the parallel formula-search data commit; reread TOE69 gauge builder, TOE71–73 fixed-witness Hessian, TOE72 exact interface and Q complement, TOE71–73 20-octagon pairing/orbit results, TOE72 W33-squared topology and TOE73 eleven-site interacting fixed-\(\mathbb Z_2\) phase scan.

Relevant external theory: Ginsparg–Wilson/overlap Dirac constructions; Narayanan, *Phys. Rev. D* 58, 097501 (1998), doi:10.1103/PhysRevD.58.097501; generalized overlap/GW review Fujikawa, arXiv:hep-lat/0205024; 2026 *The index of lattice Dirac operators and K-theory*, doi:10.1007/s11005-026-02080-w. These are established methods. No W33 chirality or universal physical constant is inferred from them.

## Front 1 — Entire 3×3 Hessian of the fixed 17-edge adversary, without trusting floating eigenvalue ordering

TOE72–73 proved the exact anti-symmetric eigenaxis \(q=(0,-1,1)\) and its unique zero in the rational bracket \(\epsilon\in(24461518/10^8,24461519/10^8)\). To determine if this is a genuine first Hessian instability for **that witness** (rather than just a selected negative direction), write its exact integral-coefficient matrix in \(r=(1+\epsilon)/(1-\epsilon)\):

\[
H(r)=(1-\epsilon)^8
\begin{pmatrix}
 A(r)&B(r)&B(r)\\
 B(r)&C(r)&E(r)\\
 B(r)&E(r)&C(r)
\end{pmatrix}.
\]

The anti-symmetric eigenspace has eigenvalue \(C-E\); the complementary symmetric \(2\times2\) block is

\[
\begin{pmatrix}A&\sqrt 2B\\ \sqrt2 B&C+E\end{pmatrix}.
\]

**Necessary and sufficient symmetric-sector positivity:** \(A(r)>0\) and \(A(r)[C(r)+E(r)]-2B(r)^2>0\). These are integer polynomials. The producer converts each to **exact rational Bernstein coefficients** on 64 equal subintervals from \(r=1\) to \(r=(1+\epsilon_{\rm high})/(1-\epsilon_{\rm high})\). Positivity of all Bernstein coefficients is a rational checkable proof on the interval; the script records both the whole-interval outcome and the positivity near the bracket. Exact anti-symmetric endpoint signs establish a unique witness crossing. If subdivision proves the symmetric block positive throughout, that identifies the **first loss of PSD within the specified 17-edge witness family**. No all-160-edge minimax proof is claimed, and a failed Bernstein check is reported honestly rather than silently asserted.

**Source:** \`analysis/w33_20261014_toe74_exact_gates.py\`.

## Front 2 — An unconditional exact-rational unbounded-rotor E0 interval

Previous TOE71–73 numerical lower gaps used ordinary Ritz estimates for the two lowest ordered eigenvalues of a finite \(22{,}638\times22{,}638\) block; a Ritz residual does not certify that ordering.

Here the native 11-site, 12-link, 5-fermion, two-electric-coordinate Hamiltonian is split into P for \(|m_i|\le3\) and its infinite Q complement. **No numeric eigenvalue input is used.** Enumerate the exact 462 occupations and 49 P flux pairs, including exact allowed fermion and Wilson hopping row sums, to obtain a rational Gershgorin \(P\succeq pI\). Reproduce TOE72's exact \(Q\succeq (2833/200)I\) and \(\|PHQ\|^2\le6411/3200\).

Choose an integer fraction \(t<p\) obeying the exact Schur inequality

\[
(p-t)(2833/200-t)\ge6411/3200.
\]

Then the full **unbounded-electric-flux** ground energy obeys \(E_0\ge t\), with an unconditional variational **upper** bound from exact rational 1- and 2-basis Rayleigh trial states inside P. Both sides are computed with Python \`Fraction\` (no eigenvalue ordering premise). The interval may be broad and is **not** a spectral-gap proof, but it replaces an important conditionality with an independently reproducible nonperturbative ground-energy bound.

**Source:** \`analysis/w33_20261014_toe74_unconditional_gauge_bound.py\`.

## Front 3 — Actual beyond-star 2-local pairing geometry

TOE72 proved seven disjoint \(PGSp(4,3)\) exact 20-octagon cover orbits; TOE73 transported six inter-orbit perfect matchings and computed a deliberately compressed seven-star quantum transition model, not a full induced graph.

This pass reconstructs the exact 3-choice local edge pairings and exhaustively tests **all 12,640 two-site alternative pairings** from each of **seven orbit seed configurations**: the original and its six second-order neighbors. Every resulting exact 20-loop configuration is reconstructed to its canonical 20-cycle key; their full local loop-count histograms, genuine second-order neighbor counts, overlaps with the seven seed covers, and distinct two-hop cover keys are recorded. The total census is **88,480 local flip tests**.

This independently probes target-to-target links and additional adjacent covers; it never assumes that a cover differing from the original seven seeds lies in a new symmetry orbit. Orbit membership and closure of the full effective \(3^{80}\)-state model remain open.

**Source:** \`analysis/w33_20261014_toe74_quantum_neighbors.py\`.

## Front 4 — A concrete native Euler–Dirac stencil, and a rigorous no-confusion check against spin chirality

Build the **actual oriented \(80\times160\)** native Levi incidence matrix \(B\) and the finite graph Dirac–Kähler / Euler–Dirac cochain operator

\[
D_{\mathrm{Euler}}=
\begin{pmatrix}0&B\\ B^\top&0\end{pmatrix},
\quad \Gamma=\mathrm{diag}(+I_{80},-I_{160}).
\]

The integral rank of \(B\) is 79 because the graph is connected, so the graded kernels have dimensions \(b_0=1\) and \(b_1=81\), with graded index \(1-81=-80\). The exact nonzero squared singular spectrum follows the W33 Levi graph Laplacian: \(8^1\), \((4-\sqrt6)^{24}\), \((4+\sqrt6)^{24}\), \(4^{30}\). This has an executable numerical spectral reconstruction plus combinatorial proof.

**It is NOT the four-dimensional spin Dirac operator.** In TOE72–73's closed W33-squared manifold \(\Sigma_{81}\times\Sigma_{81}\), the 4D **de Rham/Euler** graded index equals \(\chi=25{,}600\), whereas the **untwisted spin Dirac** index is \(\hat A=-\sigma/8=0\). Claiming chirality 25,600 by confusing these two indices is wrong. The source explicitly enforces this distinction; a local admissible four-dimensional overlap spin discretization remains unsolved.

**Source:** \`analysis/w33_20261014_toe74_exact_gates.py\`.

## Front 5 — Beyond four \(\mathbb Z_2\) corners: interacting continuous \(U(1)^2\) phases and canonical finite-temperature traces

Use the actual 11-native-site/12-edge patch with both spanning-tree-chord phases continuous, all \(\binom{11}{5}=462\) spinless fermionic basis states, exact Jordan–Wigner signs and local repulsion \(V\). Build a complex Hermitian matrix for arbitrary chord phases \((\phi_1,\phi_2)\), rather than inserting only \(\{0,\pi\}^2\).

At \(V=0,.2,1,4\), solve the lowest two eigenpairs for each of **25 sample phases** \(\phi_i/\pi\in\{0,1/4,1/2,3/4,1\}\). Full diagonalization at the four corners independently computes the canonical Helmholtz free energies

\[
F_N(\beta;\phi)=-\beta^{-1}
\log\operatorname{Tr}_{N=5}e^{-\beta H_N(\phi)}
\]

for inverse temperatures \(\beta=.5,1,2,8\). Complex Hermiticity, consistency against TOE73's signed real \(\mathbb Z_2\) Hamiltonian, local sitewise \(U(1)\) gauge-rephasing invariance, and time-reversal spectral symmetry are tested directly. The source computes and freezes any *sampled* interior-phase preference instead of presupposing all minima at corners.

A five-by-five grid is **not continuous global optimization**; a finite-size canonical free energy is **not a dynamical Gauss-constrained partition function** or evidence of the observed Standard Model.

**Source:** \`analysis/w33_20261014_toe74_u1_manybody_finite_t.py\`.

## Verification

Dedicated \`tests/test_w33_20261014_toe74_five_fronts.py\` covers the five fronts (six tests including distinct exact Dirac and disorder gates). A dedicated on-push GitHub Actions workflow runs those tests and independently regenerates four JSON certificates. Check live CI status before declaring success.

## Five independent highest-value follow-ups

1. Produce a machine-verifiable exact-rational **all-160-link and all-Hessian-direction** global minimax certificate, exploiting native cycle symmetries and interval branch pruning.
2. Certify the **two lowest ordered** \(22{,}638\)-dimensional finite Gauss block eigenvalues by checked inertia/interval arithmetic to turn the existing *conditional* rotor gap into a rigorous gap.
3. Build and classify the **actual full seven-orbit induced quantum adjacency** (not only seven representatives or chosen perfect matchings), and extend to any newly encountered inequivalent exact covers.
4. Equip a genuine local four-dimensional **spin** cellulation with metric, Clifford action, admissible gauge connection and overlap-Dirac operator, separating spin index from graph Euler index throughout.
5. Trace **continuous and finite-temperature interaction-dependent flux transitions** on larger native patches, match against graph controls, and identify a genuinely W33-specific falsifiable physical quantity.

**Scientific status:** finite mathematical and model-physics advances; no complete experimentally established Theory of Everything.


## Verified outcomes, symmetry corrections, and reproducible evidence

**Verification:** [TOE74 Actions run 38633744989](https://github.com/wilcompute/W33-Theory/actions/runs/38633744989) completed successfully on 14 October 2026, **6/6 tests passed in 33.31 s**. The producers independently regenerated all exact, operator, quantum-cover, static-U1 and combined \(\Theta/F_3\) certificates. Full result ZIP artifact: \`toe74-five-front-certificates\` (GitHub artifact ID 11927821790).

The source-regenerated **exact rational Bernstein signs** were all positive on 64 subintervals for the 17-high/143-low witness's symmetric Hessian sector from \(\epsilon=0\) through \(\epsilon_{\rm upper}=24461519/10^8\). Its antisymmetric exact eigenaxis changes sign once within \(24461518/10^8<\epsilon_*<24461519/10^8\). **Therefore this is the *first* Hessian loss of PSD for that one witness family**, not necessarily for any other native 160-link assignment. The exact P/Q Schur computation supplied the **unconditional** (coarse) native unbounded-rotor ground energy bracket **\([-9.983,-0.001]\)**, without assigning an ordered Ritz eigenvalue. **No unbounded spectral gap has been proved.**

### New exact theorem: the three nontrivial \(\mathbb Z_2\) sectors are equivalent

The TOE73 11-site/12-link native subgraph is a \(\Theta(4,4,4)\): precisely **three internally vertex-disjoint paths of length four** between two degree-three hubs. The six permutations of the three arms preserve vertices, edges, bipartition, nearest-neighbor density repulsion, and canonical particle number. Each of the three nontrivial \(\mathbb Z_2^2\) flux-corner assignments produces exactly **two \(\pi\)-flux octagons and one trivial-flux octagon**, with the zero-flux octagon different for each assignment. Arm permutations transitively permute those three classes. They are therefore **unitarily isospectral at every interaction \(V\)** and have exactly equal canonical finite-temperature partition functions. The Python producer checks all six arm automorphisms and all four sector parities.

**This corrects TOE73:** reported changes of which of \((\pi,0),(0,\pi),(\pi,\pi)\) was labeled the *winner* were only floating numerical tie-breaking within an exactly degenerate orbit; they did **not** establish an interaction-driven transition between distinct \(Z_2\) ground-flux sectors.

The \(5\times5\) *continuous* phase grid shows a different effect. With full 462-dimensional, fixed-five-fermion interacting Hamiltonians and phase coordinates in units of \(\pi\):

| \(V\) | 5×5 U(1) phase-grid best-orbit (within numerical tolerance) | improvement below all three degenerate nontrivial Z2 corners |
|---:|:---|---:|
| 0 | nine tied points on \(\phi_1=\pi\) or \(\phi_2=\pi\) | ~2.4×10^-14 (numerical zero) |
| 0.2 | (1,1/2) and (1/2,1) | 0.0003193686 |
| 1 | (1,1/2) and (1/2,1) | 0.0007909717 |
| 4 | (1,1/2) and (1/2,1) | 0.0000040651 |

**Interpretation:** weak interaction-sensitive preference for certain non-\(Z_2\) backgrounds in the sampled finite grid, *not* a proven global minimum over the continuous torus, nor spontaneous symmetry breaking, nor an all-80-site W33 prediction. In the noninteracting theta graph, the equal-arm single-particle Schur complement depends only on the modulus of the sum of three arm phases, \(|e^{i\alpha_1}+e^{i\alpha_2}+e^{i\alpha_3}|\). When two arm phases differ by \(\pi\), those contributions cancel, and that modulus equals one independent of the third phase; this algebraically explains the observed free-fermion flat one-dimensional minima. Nearest-neighbor interactions are not invariant under the arm-*mixing* one-particle transformation, allowing the numerical degeneracy to lift for \(V>0\).

### New exact combinatorial quantum-cover compression: \(51,840\) friendship graphs \(F_3\)

A full two-flip census around each of the **seven known \(PGSp(4,3)\) orbit representatives** (7×12640=88480 trials) gives exact 20-loop outgoing degrees \((6,6,8,8,8,8,6)\). Of the 7 representative covers, besides the six original center-leaf edges, the exact target-target links are **(1,2), (3,4), (5,6)**. Thus the seven-representative graph is the **friendship graph \(F_3\)**: three triangles meeting at one central vertex; nine edges, cycle rank three.

Because every one of these **seven specific group orbits is regular** (trivial stabilizer), the *nine selected* group-equivariant matching types each transport to 51,840 distinct edges. The **deliberately compressed** quantum adjacency contains 466,560 edges and decomposes into 51,840 disjoint \(F_3\)'s, with exact adjacency eigenvalues per component
\[
 3,\quad -2,\quad 1,\quad1,\quad -1,\quad-1,\quad-1.
\]
This strictly enlarges the previous six-matching star compression and introduces three configuration-space cycles. **It is not the entire induced seven-orbit quantum graph**, since additional possible target-target and outward links are not classified. The coincidence of three independent configuration-space cycles with the three *selected* native W33 holonomy directions is a question to test, not a derived identification.

## Source files and certificate paths

* \`analysis/w33_20261014_toe74_exact_gates.py\` — 17-link exact Hessian/Sylvester and Euler–spin index separation
* \`analysis/w33_20261014_toe74_unconditional_gauge_bound.py\` — exact-rational unbounded-rotor ground-energy bound
* \`analysis/w33_20261014_toe74_quantum_neighbors.py\` — 7×12,640 complete two-flip seed census
* \`analysis/w33_20261014_toe74_u1_manybody_finite_t.py\` — continuous finite-grid U1 and fully traced canonical corner free energies
* \`analysis/w33_20261014_toe74_quantified_findings.py\` — tied minimum and quantitative tolerance controls
* \`analysis/w33_20261014_toe74_theta_friendship.py\` — exact arm-\(S_3\) flux-corner theorem and nine matching \(F_3\) certificate
* \`tests/test_w33_20261014_toe74_five_fronts.py\` — six independently passing regression gates
* \`.github/workflows/w33_toe74_five_fronts.yml\` — reproducible CI and uploaded JSON certificates

**Limits unchanged:** there is no mathematically verified all-160-edge minimax; no rigorously enclosed *ordered* finite 22,638-dimensional eigenvalue pair; no all-state quantum pairing ground solution; no native admissible 4D overlap-spin lattice index; and no parameter-independent experimental derivation of the physical Standard Model.
