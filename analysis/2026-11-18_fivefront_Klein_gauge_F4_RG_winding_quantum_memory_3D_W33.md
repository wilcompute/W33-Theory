# Five orthogonal W33 / TOE falsifiers: Klein gauge moduli, F4 running, winding, quantum memory, local 3D graph continuum

Date: November 18, 2026. Status: reproducible mathematical and explicitly model-dependent calculations. No laboratory measurement, full string spectrum, observed Standard Model vacuum, or theory of everything.

## Precedent and parallel checks

Starting local and GitHub master: 9c87d3c1cce0ae657aab3bb6ce38d64d245d9deb. Reviewed the parallel Klein cubic and exceptional-algebra commits: 39c68b4 (Weil/PSL2(11) finite gauge strata), d84e57a (quadric A4/C4), 0d80b77 (quadric gauge monodromy), and 9c87d3c (nested Albert qubit/qutrit F4 selector and failure of automatic chiral matter). During this pass master advanced to 2766572, which implements the complex bi-Cayley Peirce16 and native E6 action with the correct Standard Model family hypercharges and SU5-like kinetic normalization, while still lacking physical chiral zero modes and family multiplicity. This later result provides a more promising alternative to the real F4 boundary tested below. Their existing producers and fields are not modified.

The original W33 Levi cycle rank 81 and shortest cycle bases are already established in analysis/2026-11-01_five_plus_three_w33_physics_continuation.md and other prior work. We do not claim the number 81 as a discovery. New to this packet are three periodic edge voltages, a closed-form rational low-energy diffusion matrix and connected 3D covering graphs. Parent BF and photon work is also explicitly distinguished below.

## 1. Exact rational cohomology of the full Klein A1 gauge stratum

Parent analysis/2026-11-18_Klein_Weil_ADE_and_real_Spin7.md establishes an involution S in PSL2(11), order-12 centralizer, a fixed Sasaki-Einstein seven-link locus Q that is a principal circle bundle over an elliptic plane cubic E with Euler number three, and H1(Q,Z)=Z^2 plus Z3. The generic transverse A1 singularity is a potential local su2 source, NOT the Standard Model by itself.

The independently reproduced 660-element Weil representation reduced modulo 23 contains a second involution T commuting with S. Their V4 simultaneous positive eigenspace has dimension two; the S-positive, T-negative eigenspace has dimension one. Restricting the Klein cubic to the common positive 2-plane gives a binary cubic with nonzero discriminant modulo 23, hence nonzero in characteristic zero. On the elliptic plane E in the projective S-positive 3-space, T fixes exactly three projective points on the plus-line and one on the isolated minus-line (the latter lies in E by odd-cubic T-invariance).

A nonidentity holomorphic involution on an elliptic curve with a fixed point is z -> a-z. It has four fixed points and induces -identity on H1(E,R). The nonzero circle Euler number makes H1(E,R) -> H1(Q,R) an isomorphism (Gysin). Thus T acts -I on the entire b1(Q)=2 space. Since T lies in C(S)/<S>, the rational first cohomology of the full quotient Q/(C(S)/<S>) is ZERO. Orientation preservation and rational Poincare duality give b2=0 and b0=b3=1: the quotient has the rational Betti numbers of a 3-sphere, not necessarily its smooth topology or integral homology.

The existing parent reports the order-six residual quotient and A1 volume pi^2/4; those are inputs, not new outputs. New output: that order-six symmetry projects away the two continuous untwisted one-form moduli of each parent Q. In the standard torsion-free G2 ADE model b1(Q) would count adjoint chiral multiplets. Here the compactification instead has weak G2/Sasaki-Einstein geometry with AdS flux and higher-isotropy intersections; this topological projection alone does NOT calculate the physical localized spinor/adjoint spectrum, charged matter or anomalies. Twisted adjoint local systems could also behave differently. There is a second important consequence, not a free benefit: on a compact gauge locus with b1=0, every smooth source-free Abelian one-form obeying d(phi)=0 and d*(phi)=0 vanishes by Hodge theory. Thus the simplest globally harmonic Abelian Higgs-one-form localizer of the Pantev-Wijnholt construction cannot operate nontrivially on this specific untwisted quotient. Sources, non-Abelian Higgs backgrounds, singular boundary conditions or twisted bundles could evade this conditional obstruction, and the torsion-free G2 Pantev-Wijnholt equations cannot be transplanted unchanged into weak-G2 AdS flux. See Acharya/Gukov https://arxiv.org/abs/hep-th/0409191 and Pantev-Wijnholt https://arxiv.org/abs/0905.1968 and parent source.

## 2. One-loop Standard Model running falsifies an uncorrected F4 single-scale boundary

Parallel Albert/F4 selector commit 9c87d3c computed conditional tree boundary g3^2=2*g2^2 and gY^2=3*g2^2; physical sin^2(thetaW)=3/4 at that boundary, with Y normalized by its proposed matter charges. The nested algebra stabilizer is a published result of Baez and Schwahn (https://arxiv.org/abs/2606.15235); the particular kinetic ratios are specific to the repo's representation.

Independent benchmark: use Standard Model b=(41/6,-19/6,-7) for ordinary U1Y, SU2, SU3, with d[1/g_i^2]/d ln(mu)=-b_i/(8pi^2), and fixed illustrative near-MZ MSbar inputs alpha_em^-1=127.952, sin^2thetaW=0.23129, alpha_s=0.1179, MZ=91.1876 GeV.

Solve the TWO required crossing equations independently. The color-vs-weak condition g3^2=2g2^2 holds at mu=138472.9594 GeV. The weak-vs-hypercharge condition gY^2=3g2^2 would hold only at log10(mu/GeV)=32.56961486, far above the Planck domain. At the first crossing, the second mismatch 1/g2^2-3/gY^2 is approximately -18.93. There is no common matching scale under unextended SM one-loop evolution.

This is NOT a no-go for F4 gauge theories: threshold states, alternative kinetic operators, hypercharge embeddings, new light matter, and full higher-loop running may change the test. It quantifies the burden for the specific parent F4 proposal. It does not repair the parent real-26 absence of a chiral SM family. PDG benchmark: https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf.

## 3. Winding tachyon window is sharp and cannot be cured globally by a finite flux ratio

Reuse the exact parent conditional equal-flux mixed winding/radion dispersion from analysis/2026-11-16_D9_iib_conifold_dual.md: lambda=3pi r |u+v tau|^2/Im(tau), r=N0/N>0, (u,v) nonzero integers, and m_minus^2 L^2=lambda-2-sqrt(4+16lambda). The AdS5 BF bound m2 L2>=-4 is violated exactly for 0<lambda<12.

The two-dimensional Hermite bound (shortest lattice-vector norm <=2/sqrt3 at unit covolume) implies that if r<2sqrt3/pi=1.10265779084, EVERY tau has a BF-violating mode in this particular branch. At r>=2sqrt3/pi, stable tau DOES exist for that branch, namely the hexagonal torus that saturates Hermite. Nevertheless, NO FINITE positive r guarantees stability for ALL tau: along the cusp tau=i y, shortest normalized norm=1/y and lambda_min=3pi r/y<12 for y>pi r/4. This is a sharper and genuinely two-sided phase-diagram criterion than the previous sufficient instability inequality.

For r=1, both the square and hexagonal examples violate BF. The lowest possible mass within the formal branch is -25/4 at lambda=15/4, a BF deficit of 9/4. This is not a full KK/string mass bound; it follows from the parent mixed truncation. Winding sectors in IIB require alpha-prime and brane consistency checks. It is distinct from unequal-flux homogeneous Tpq instability. Literature: https://arxiv.org/abs/hep-th/0108239.

## 4. A quantum rather than merely non-Markovian photonic-memory experiment

The repo's earlier causal-break SWAP process stores and returns an arbitrary qutrit. That establishes temporal memory but not that the memory is quantum. To discriminate, prepare an external reference qutrit maximally entangled with the input. Measure the normalized Choi state's fidelity F to |Phi3>=(|00>+|11>+|22>)/sqrt3. Any entanglement-breaking (measure-and-prepare) channel has F<=1/3 because every product state overlaps with |Phi3> by at most 1/3 and convex combinations preserve the bound.

For a depolarizing return channel E(rho)=eta rho+(1-eta)I/3, normalized Choi state=eta |Phi3><Phi3|+(1-eta)I9/9. Its fidelity F=eta+(1-eta)/9, and its partial transpose has three negative eigenvalues if eta>1/4. At explicitly SIMULATED eta=0.4, F=7/15 and entanglement negativity 0.2. Direct nine-by-nine matrix diagonalization verifies both.

An exact one-sided binomial test for independently accepted Bell-projector trials, composite entanglement-breaking null p<=1/3 versus assumed alternative p=7/15, reaches alpha<=0.01 and beta<=0.01 at its smallest deterministic n=292, threshold 117 plus outcomes. Exact numerical errors 0.00934901696 and 0.00997203845. This is not a claim of experimental observation. Requires an independent entangled reference, physically coherent joint Bell measurement, random causal-break interventions, realistic loss/systematics and a preregistered stopping plan. Pure classical serial memory is not equivalent to an entanglement-breaking quantum channel without a specified experimental boundary. Operational process-tensor review: https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs.

## 5. Exact W33 three-periodic local graph and a 3-dimensional low-energy torus

Construct W(3,3) independently from all 40 projective points in F3^4 and 40 totally isotropic projective lines. Its point-line Levi graph is 80 vertices, 160 edges, degree four and connected, with cycle rank 81 (known prior work). Build a deterministic BFS spanning tree. Its sorted chords numbered 0,27,54 are exactly (1,45),(16,45),(28,46). Assign directed voltage vectors e1,e2,e3 to those three edges, zero to the other 157. The resulting Z_n^3 cover is connected for every n because the three fundamental chord cycles generate all three deck directions. It has V=80n^3, E=160n^3, constant degree four, cycle rank=80n^3+1, and girth at least eight. Directly constructed and independently checked n=2 (640 vertices,1280 edges,b1=641) and n=3 (2160 vertices,4320 edges,b1=2161).

For Bloch momentum theta=(theta1,theta2,theta3), put e^(i theta_j) on those three directed chord hoppings and conjugates on reverse edges. The Hermitian finite-cell Laplacian is L(theta)=4I-A(theta). At theta=0 the base graph has simple eigenvalue zero and the first positive eigenvalue 4-sqrt6, so analytic lowest-band perturbation applies.

Let B be the 80x160 integer oriented incidence matrix and W the 160x3 edge voltage matrix. The quadratic energy is K=W^T(I-B^T Lplus B)W and D=K/80. Rather than trust a floating pseudoinverse, we evaluated the following exact INTEGER polynomial identity for the base Levi Laplacian L=BB^T:

H=-L^3+20L^2-138L+376I, and L H=320I-4J.

Because each edge incidence vector has zero total sum, Lplus B=H B/320. Pure integer 80x80 and 3x3 matrix arithmetic therefore proves

K = (1/160) times [[81,-27,9],[-27,81,-3],[9,-3,81]]
D = (1/12800) times the same integer matrix.

All eigenvalues of K are positive (approximately 0.333233,0.495080,0.690437). Independent numpy pseudoinverse agrees to 1e-11. Each edge effective resistance is exactly 79/160, giving a nontrivial 81/160 single-edge cycle conductance; the integer identity checks this directly and Foster's theorem supplies a conceptual explanation.

For each fixed Fourier integer m in Z^3, the n-fold toroidal Bloch momenta theta=2pi*m/n give
n^2 lambda_low(theta) -> (2pi)^2 m^T D m,
the eigenvalues of -div(D grad) on the unit three-torus. Numerical independent lowest-band checks at momentum magnitudes 0.25,0.125,0.0625 show relative errors about 0.00676,0.00169,0.000424. The low band is a genuine scalar THREE-DIMENSIONAL spectral continuum while every microscopic graph retains fixed degree four; this escapes the previous raw dense-point-graph nonconvergence obstruction.

This is NOT yet spacetime. Three voltages were selected by choice, not dynamically forced. The graph remains a one-dimensional CW complex, no Lorentzian causal order, Einstein action, 3+1 metric, physical energy scale or Standard Model field equation was derived. This is a mathematically constructive route worthy of a dynamical selection test. Periodic-graph Bloch theory is standard: https://www.sciencedirect.com/science/article/pii/S0024379523002914.

## Reproduction and evidence firewall

Owned new files:
- analysis/toe_20261118_W33_triperiodic_Levi_homogenization.py
- analysis/toe_20261118_fivefront_Klein_F4_winding_memory.py
- data/toe_20261118_W33_triperiodic_Levi_homogenization.json
- data/toe_20261118_fivefront_Klein_F4_winding_memory.json
- tests/test_toe_20261118_fivefront_Klein_F4_winding_W33_memory.py
- analysis/2026-11-18_fivefront_Klein_gauge_F4_RG_winding_quantum_memory_3D_W33.md (this report).

Run both producers as standalone Python scripts and the focused unittest discover for pattern test_toe_20261118_fivefront_Klein_F4_winding_W33_memory.py. The producer checks direct parent group representations, arithmetic graph identities, connected finite covers, 9x9 Choi matrix eigenvalues and exact accepted-shot binomial probabilities. Mathematical arguments above provide the conditional bridge from arithmetic to geometry and physics; PASS is not an observed experiment. The project has not derived a complete theory of everything.

## Five independent next steps

1. Derive the full flux-coupled A1 gauge-locus operator, twisted local systems and intersection chirality/anomaly index, rather than rely on rational b1.
2. Formulate a dynamical voltage action on W33's 81-cycle space that selects exactly three independent dimensions and produces Lorentzian causal gravity, with other voltage ranks as nulls.
3. Construct a complete E6 or F4 gauge-Higgs-matter theory with actual threshold spectra, known hypercharges, proton-lifetime predictions and UV consistency.
4. Calculate the complete finite-N string and M-theory winding mass matrices, charge lattices and higher-curvature corrections across the new modular phase diagram.
5. Build an experimental entangled-reference causal-break qutrit memory witness and calibrate detector bias and nonlinear loss against classical memory controls.
