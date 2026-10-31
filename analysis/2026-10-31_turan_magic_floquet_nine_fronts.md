# Eight W33 physics fronts plus a compiled anomalous chiral Floquet edge
**2026-10-31 | Reproducible mathematics and conditional physics | NOT a TOE**

**Programs:** \`analysis/w33_20261031_turan_mub_magic_and_topology.py\` (eight experiments), \`analysis/w33_20261031_native_floquet_chiral_edge.py\` (new physical chiral implementation). Frozen data have matching \`data/*.json\`; regression \`tests/test_w33_20261031_turan_magic_floquet.py\`.

**Provenance:** continued from concurrent \`ccbd086d1f5b1cc204547766baced5449981d020\` (eight falsifiers, some overlapping front headings), which already demonstrated the 8-site *distinct-color* 27/28 bound, 81-mode optical losses, parity 5+4 split, Wigner positivity of Clifford gate, and 1D GNVW obstruction. These are not claimed as new here. Prior native TLJ construction was \`ad8846e599812d2327821521c53dacd6058bba06\`. Existing local uncommitted agent files were preserved.

## I. All-system-size exact clock ground energy and degeneracy

For the supplied **complete spatial interaction graph K_n** with n arbitrary and tick labels among all 120 Pauli spectral projectors, use the previously established bond energy \`E_ab=J(3-Tr Pi_aPi_b)-K||[Pi_a,Pi_b]||_F^2\` with J>0, K>3J/2. Same tick costs zero. Distinct commuting directions cost 2J, different outcomes of same direction cost 3J. Distinct noncommuting directions cost epsilon=2J-4K/3 <0.

The negative-energy edge graph of any tick assignment is K8-free, because the noncommutation graph of the forty Pauli directions has clique number seven. By **Turán's theorem**, it contains at most \`t_7(n)\` negative edges. The other bonds are nonnegative, so total energy is bounded below by \`epsilon*t_7(n)\`. Pick any one of 2880 seven-direction cliques and a balanced seven-way partition of sites, assigning a fixed spectral tick within each part. Every inter-part edge is negative and every intra-part edge zero, saturating the bound:

    E_min(n)=epsilon t_7(n),
    n=7a+r, 0<=r<7,
    t_7(n)=(n² - (7-r)a² - r(a+1)²)/2.

For n>=7, Turán **equality** implies a balanced complete 7-partite negative-bond graph, while every non-negative intra-part edge must have zero cost, hence all intra-part ticks identical. Seven distinct directions form one of exactly 2880 unordered maximal seven-cliques; each direction has 3 possible spectral ticks. Therefore the exact number of **site-labeled zero-temperature ground configurations** is

    2880 * 3^7 * binomial(7,r) * n! / (a!^(7-r) (a+1)!^r).

n=7: 31,744,742,400. n=8: 888,852,787,200. In particular n=8 and (J,K)=(1,2) has exact unrestricted \`Emin=-18\`, not -16 for distinct directions. For n<7 every pair can be noncommuting and the energy formula remains exact, though the displayed degeneracy formula is only for n>=7. If the supplied all-to-all couplings are Kac-scaled by \`1/(n-1)\`, then energy per site tends to \`(3/7)epsilon\`. None of these statements derives a real vacuum, time direction, equilibrium temperature transition or dimensionful parameters.

## II. Exact MUB spread and chromatic optimality

The graph of noncommuting W33 directions has eigenvalues \`27^1, 3^15, (-3)^24\`. Hoffman's bound gives \`chi>=1-27/(-3)=10\`. Backtracking among the forty commuting W33 four-cliques finds an actual **spread of ten pairwise-disjoint lines** covering all forty directions; each line defines an independent color class in the noncommutation graph, proving \`chi<=10\`. Therefore \`chi=10\`.

Diagonalize the four native two-qutrit Pauli operators in each context to obtain ten nine-dimensional orthonormal bases. Verify across every pair of bases all 81 squared overlaps equal \`1/9\`, maximum numerical deviation 2.37e-14. This is the standard known finite-dimensional complete MUB phenomenon in dimension9, here explicitly certified in the native W33 labeling. Crucially, clique number 7 and chromatic number 10 are different constraints: K_n clock frustration is ruled by clique, while arbitrary spatial-graph colorability is not exhausted by seven-coloring.

## III. Rank-one Jones–Wenzl f4 equals a Strange-state projector

The native five-generator TLJ representation has idempotent ranks \`(f2,f3,f4,f5)=(6,3,1,0)\` for delta=sqrt3. Compute f4 by the Jones–Wenzl recursion and compare its entire 9x9 matrix to the computational-basis projector:

    f4 = |0><0| tensor |S><S|,
    |S>=(|1>-|2>)/sqrt(2).

The maximum Frobenius discrepancy is below 1e-10, without fitting a Clifford or local basis rotation. Its unique ket is a PRODUCT (Schmidt values 1,0,0) with parity -1; the second factor is **exactly the canonical qutrit Strange state**. All 81 Gross phase-space Wigner entries yield min -1/9, total absolute mass 5/3, mana log(5/3)=0.510825623766. The second qutrit alone has negative Wigner entry -1/3 and the first qutrit is |0> stabilizer. The repository already contained Strange-to-Norell/metaplectic magic factory work (Pass10942-10943); the concrete *Jones–Wenzl f4 equals local Strange-projector* identity links it to the native quantum-group carrier.

**Major resource accounting:** f4 is a specified *non-Pauli projective measurement*. It is not automatically implemented by a finite Clifford braid circuit; the projector itself supplies a nonstabilizer operation. Its separability means it is not a nonlocal topological fusion sector, and it does not create magic for free. A physical instrument, energy penalty, success probability and noise threshold must be supplied/derived separately.

## IV. Optical phase dephasing destroys the 3-mode Helstrom advantage

The earlier directed 3-port states \`psi+/-=(I+F²/14 +/- F/sqrt14)|0>\` have overlap -3/7 and error 0.0482460 with ideal collective-basis Helstrom one-shot analyzer. A supplied Gaussian waveguide phase channel acts as \`D(theta)=diag(1,e^{i theta},e^{-i theta})\` on each injection, theta normal(0,sigma²). Ensemble averaging is analytic:

    rho_ij(sigma)=psi_i conj(psi_j) exp[-sigma²(a_i-a_j)²/2],
    a=(0,1,-1).

From the exact density matrices, calculate Helstrom error \`(1 - .5 ||rho+-rho-||_1)/2\`. For sigma=0,0.1,0.5,1,2,4,10 radians, the optimum errors are approximately \`0.048246,0.052438,0.124590,0.204785,0.266794,0.27091891,0.27091894\`. At full dephasing the optimal quantum readout is no better than fixed-port classical counting (error 0.2709189355). This is a clearly specified noise mechanism, not measured performance. Mode-by-mode loss and dark-count tests already exist in the previous parallel packet.

## V. Characteristic-five modular torsion is canonical at p=5

The actual W(3,9) 48-line graph biadjacency B is 24x24, rank18 over Q, and has mod5 kernel dimension13. The six integer columns formed from individually primitive rational nullvectors satisfy B L=0 and **rank(L mod5)=6**. That last condition proves the index of their sublattice in the full *saturated integral kernel* is **coprime to 5**. Therefore their mod5 span equals reduction of the canonical integer kernel, even if the chosen six columns do not form a saturated integral basis at other primes. The quotient

    ker(B mod5)/red(ker_Z B)

is the canonical \`Tor_1^Z(coker B, F5)\` by tensor exact-sequence algebra, with dimension7. This closes the earlier ambiguity about mod5 *canonicity*. The induced ambient PGSp(4,9) order-five action from the previous work has Jordan partition (3,3,1), compatible with that canonical quotient. It still does not classify the full A5 module, ambient stabilizer's full action or any physical gauge flux.

## VI. Quantum-gravity metric-signature falsifier

The formerly used native acoustic matrix has numerical eigenvalues \`1.3270485,1.5,9,10.1729515\`, all positive. The previous coupled scalar model only rescales by positive factor \`g_x=exp(2alpha phi_x)Q\`. **Sylvester's law of inertia** therefore makes every 4x4 metric positive-definite at all finite phi: no Lorentzian (3,1) signature can emerge by this ansatz. With separate externally supplied Hamiltonian time, the model has four positive spatial directions PLUS a supplied temporal parameter, rather than deriving physical 3+1 spacetime. A signed tetrad/spin-connection or a different signature-changing mechanism is indispensable. This is a useful *no-go* preventing overinterpretation of successful backreaction simulations.

## VII. Outside-box quantum category test: native SU(2)_4 != D(S3)

The native Jones root-of-unity parameter matches the \`SU(2)_4\` TLJ category, whose simple quantum dimensions are \`1,sqrt3,2,sqrt3,1\`. Their squares sum to 12, Gauss sum equals \`i sqrt12\`, and chiral central charge is \`c=2 mod8\`. Independently, the quantum double D(S3) has eight simple objects with quantum dimensions \`1,1,2,3,3,2,2,2\`: total dimension squared 36 and chiral central charge 0 mod8. They are **not braided equivalent**, by any of these invariants.

This prevents incorrectly importing the July 2026 *Nature* experimental D(S3) 54-qubit universal braiding/fusion result as a direct hardware realization of native W33 \`SU(2)_4\`. It remains excellent evidence that **fusion measurements and magic preparation** can supplement nonuniversal braid gates, but the anyon category is different. Published experiment: Lo et al., *Universal gates from braiding and fusing anyons on quantum hardware*, Nature 655, 591–597 (2026), https://doi.org/10.1038/s41586-026-10709-y .

## VIII. Outside-box spectral-geometry negative control

The fixed W33 collinearity graph has graph-Laplacian spectrum \`{0^1,10^24,16^15}\`, so its exact heat trace is

    K(t)=1+24 exp(-10t)+15 exp(-16t).

The effective spectral dimension \`d_s(t)=-2 d log K/d log t\` tends to **zero** as both t->0 and t->infty. There is no true four-dimensional small-t Weyl asymptotic on this fixed forty-point graph. A growing/refining family of operator modules remains possible, but simply identifying eigenvalue counts with spacetime dimension is not evidence of emergence. Compare the spectral action approach of Chamseddine–Connes, https://doi.org/10.1007/S002200050126 (background only; none of its field content derived here).

## IX. Outside-box constructive chiral 2D Floquet edge compiled from native Jones ticks

The previous \`ccbd086\` packet correctly proved a bounded-depth **1D boundary-only** Clifford circuit cannot yield nontrivial GNVW transport. Construct the standard 2D exchange-drive escape route explicitly:

A square open LxL qutrit lattice with checkerboard A sites. Apply four matchings, each swapping every A site with its B neighbor in turn EAST, NORTH, WEST, SOUTH, skipping absent open-boundary links. Each stage consists of commuting disjoint nearest-neighbor SWAPs. On even periodic tori the four-stage whole-site permutation is the identity exactly. On open L=4,5,6,7,8,9,12 all **interior sites are fixed**; exactly **2L-1 active edge sites** form one cyclic translated orbit, and the other boundary rails are inert. Consequently the straight-edge GNVW transport index for the active qutrit rail is exactly3 (log index log3). This construction is a standard anomalous Floquet SWAP exchange loop, not a newly discovered Floquet phase.

**Native compilation test:** Choose the existing TLJ generator path [0,4,2,13,1]. Represent the actual Clifford conjugation action over Sp(4,3), not only its projective PSp quotient; BFS enumerates exactly all **51,840** Sp elements using 5 native tick generators and their inverses. The two-qutrit SWAP symplectic matrix is reachable with a **shortest directed-generator word of length13**:

    [0,1,0,3,7,3,6,2,5,1,9,8,7]

where labels 0..4 are U_i and 5..9 are U_(i-5)^dagger, and words apply left-to-right in time. Multiplying actual 9x9 matrices proves the resulting unitary equals SWAP **up to a global scalar**, with Frobenius residual below 1e-11. The shorter length-nine word found only in projective PSp actually gives SWAP times the central parity operator: keeping the full 51840 double-cover was essential.

Thus a four-step 2D exchange loop can be compiled into **52 parallel native Jones/tick layers**, assuming the required nearest-neighbor local 9D gates are physically available. This is a concrete compiled *anomalous chiral edge information pump*, not by itself a W33-derived lattice, chiral Standard Model particle, or gravitational time arrow.

Prior quantum cellular automata context: Fidkowski–Haah–Hastings, *A quantum cellular automaton for every symmetry protected topological phase*, PRB 112,035123 (2025), https://doi.org/10.1103/kw68-mkkd ; *Clifford Quantum Cellular Automata from Topological Quantum Field Theories and Invertible Subalgebras*, PRX Quantum 7,010362 (2026), https://doi.org/10.1103/4519-v15s .

## Scope and criteria

- PASS means the exact finite statements or chosen simulations pass; **not** experimental verification or a completed TOE.
- Turán, Hoffman, Gross Wigner, Jones–Wenzl, spinor metaplectic parity, dimensional quantum double, chiral QCA and the four-step Floquet exchange drive are all established general methods. The repo increment consists of **native operator identities**, frozen certificates, exact combinatorial formulas, and a full 13-tick gate compile.
- A physical TOE still requires observed chiral matter, correct gauge sectors and interactions, Lorentzian 3+1 dynamics, continuum/refinement limit, reproducible constants with look-elsewhere tests, and physical observations beyond the postulates.

## Top five independent next investigations

1. **Full icosahedral torsion action:** lift and classify all order2/3/5 stabilizer generators over GF9 on canonical \`Tor(coker B,F5)\`; prove modular composition factors and identify group action, not just cyclic Jordan.
2. **Optical metrology:** design a calibration-adaptive POVM under correlated phase noise, include detector non-IID effects, and derive shot-number uncertainty bounds, then test a real 81-mode device.
3. **Local clock physics:** put native tick interactions on a locality-constrained growing lattice, derive a quantum Hamiltonian with a gap or rigorously falsify a claimed spontaneous phase; compare to the exact complete-graph Turán benchmark.
4. **Physical Floquet topology:** couple the compiled 52-layer Jones/SWAP drive to local perturbations, open-boundary disorder, noise and edge readout; test robustness and finite-size transport before any topological protection claim.
5. **Constrained quantum geometry:** replace the positive conformal scalar with a Lorentzian tetrad/spin connection and check discrete first-class constraints and refinement Ward identities, not merely a numerical smooth scalar limit.
