# Five TOE fronts plus W33 ninth-root code obstruction and finite differential calculus

**Research date:** 2026-11-19. **Status:** executable algebraic and toy-physics results; precise limitations stated. **NOT** a theory of everything, a realistic E8/SM vacuum, a 4D chiral compactification, an experiment, or general-relativistic dynamics.

## Collision/provenance audit

We audited the newest parallel **22a122ec8** against **867f70b96**, **8dea889**, **84b0ad09c**, and earlier SIC/Dirac manuscripts. The parallel 22a122ec8 already derived an asymmetric W33 **[[40,19,4]]_3 CSS** code with (dX,dZ)=(4,6), and an independent nine-pair SIC gauge EFT (19 baryonic anchors + 27 meson constraints). Our prior 867f70b96 used a distinct ten-pair *renormalizable* cubic superpotential, 45 meson constraints + one baryon/mediator constraint. Do not confuse these classical SUSY models with a physical UV-complete compactification. The 215-page Forty Points paper already discusses a ninth-root qutrit non-Clifford gate. This report *extends* the W33 code with an exact restriction on its transversal gate family, a decoder and executable injection gadget.

We independently investigated the five requested fronts plus a shared mathematical interface across W33 and finite-spacetime field algebras.

## Front 1. Natural SIC vacuum: a one-loop UV constraint and insufficient low-order invariants

A SIC in C^N contains N^2 nonzero rays. Encoding each as a distinct chiral SU(N) fundamental field Q_i, and demanding that every fundamental be paired vectorlike with an antifundamental Qtilde_i (no higher representations), requires at least N_f=N^2 vectorlike pairs. The standard perturbative N=1 supersymmetric SU(N) coefficient is

    b_0 = 3 N - N_f <= N(3-N).

For N=2 the upper bound is +2, N=3 it is 0, and for all N>=4 it is strictly negative. Thus a fundamental-only **vectorlike elementary SIC** at N>=3 cannot have *strictly positive one-loop* asymptotic-freedom coefficient. Specifically the nine-pair EFT in 22a122ec8 has b0=0 and the ten-pair renormalizable model in 867f70b96 has b0=-1. This does not forbid asymptotic safety, different representations, a larger gauge group with SU3 emerging after Higgsing, composite SIC states, or other completions. Classical renormalizability is not, alone, a guarantee of a UV-complete quantum gauge theory.

**Exact counterexample to low-degree SIC selection:** Let Q_SIC be the unnormalized nine Hesse qutrit rays, each norm-square 2 and QQdag=6I3. Let Q_basis consist of three copies of sqrt(2) e1, three sqrt(2)e2, and three sqrt(2)e3. Both obey exactly QQdag=6I3 and thus SU3 D-flatness; each of the nine columns has norm-square 2. Both have sum_{i<j}|Qi^dag Qj|^2=36. But for the SIC, all 36 squared overlaps are 1. For the repeated-basis frame, 27 overlaps are zero and 9 equal 4. The equiangular-dispersion invariant

    V = sum_{i<j} (4 |Qi^dag Qj|^2 - 4)^2

equals **0** for SIC and **1728** for the repeated-basis non-SIC. Therefore any purported SIC-selection argument using *only* fixed frame operator, equal norms, or that first overlap moment is insufficient: it admits another D-flat vacuum. Flavor-resolving higher invariants or genuinely dynamical selection are required.

Reproducibility: `analysis/toe_20261119_four_structural_frontier_tests.py`.

## Front 2. Chirality: a stronger no-go for torus-only magnetic flux

On the round R-radius S5 times a flat T2, the Dirac spectrum of S5 is

    Spec(D_S5) = { +/- (k+5/2)/R : k>=0 }.

For **any** unitary gauge connection pulled back entirely from T2, and a compatible H27-equivariant descent to the free quotient Y7=(S5 x T2)/H27, the standard product Dirac identity is

    D_7^2 = D_S5^2 tensor 1 + 1 tensor D_(T2,A)^2
          >= 25/(4 R^2).

Consequently even arbitrarily strong **torus-only magnetic flux** cannot create a massless ordinary Dirac zero mode: the S5 gap survives. Four spin structures and flat-gerbe/torsion labels do not, by themselves, change this inequality. A spherical-direction gauge coupling, singular ADE geometry, a different metric, a torsion/supercovariant Dirac operator, or some other physical ingredient is indispensable.

A weaker complementary Lichnerowicz estimate for a general twisted standard Dirac on this scalar-curvature-20/R^2 background says the curvature endomorphism (1/2)c(F_A) must have operator norm at least 5/R^2 *somewhere* to allow a zero mode. This is a necessary estimate only, not a sufficient condition. A smooth closed odd-dimensional spin operator has no conventional net chiral index, and three torus orbifold fixed points do not prove three chiral families. A complete localized Dirac index and anomaly inflow remain OPEN.

Classical background: Acharya–Witten, *Chiral Fermions from Manifolds of G2 Holonomy*, https://arxiv.org/abs/hep-th/0109152 ; standard twisted Dirac/Lichnerowicz. The flux-independent product observation is this report's specific no-go extension of prior sphere gaps.

## Front 3. Three-time qutrit memory: arbitrary Kraus interventions and event-ready loss

As previously explored, initialize R:S maximally entangled and E in |0>; SWAP S,E, intervene arbitrarily on S, SWAP S,E back, discard E. We now test **six generic, non-projective, nonunitary Kraus branches** with sum_b K_b^dag K_b=I3. For every branch the exact unnormalized terminal R:S state is

    rho_RS,b = p_b |Phi_3><Phi_3|,
    p_b = ||K_b |0>||^2.

The largest numeric branch residual is near machine epsilon. More generally the identity holds analytically for every arbitrary completely positive instrument, since the stored entanglement lives in E and the intervention affects only S=|0>. This is an intervention-complete **toy process formula**, not a tomography result for actual hardware.

Add depolarizing storage noise p and event-ready retrieval/detection efficiency eta. Score **every** prepared trial: lost/no-click events are failures, never excluded in postselection. The unconditional maximally entangled Bell-projection success probability is

    q = eta * F,    F=1 - 8p/9.

An entanglement-breaking channel cannot exceed unconditional F=1/3 against a trustworthy isolated qutrit reference. Therefore the conservative sufficient criterion eta F>1/3 yields

    eta > 1/[3(1-8p/9)].

At p=.20, F=.822222..., requiring eta>0.4054. At eta=.50 and 6000 seeded event-ready trials, the simulated one-sided Hoeffding 99.9% lower confidence bound exceeds 0.38>1/3. This is a **conditional-on-physical-assumptions witness design**, not an actual experiment; a hidden coherent bypass, invalid reference independence, misidentified loss events, or unrestricted quantum side channels invalidate the classical comparator. A real process tensor and causal interventions must still be independently characterized.

Background: *A Guide to Higher-Order Quantum Operations*, https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs .

## Front 4. Finite-state dynamics: a hard Leibniz obstruction and a precise escape

Let F=C^n be complex-valued vertex functions with pointwise multiplication. Every linear derivation D:F->F satisfying ordinary Leibniz D(fg)=D(f)g+f D(g) is **zero**. Proof: the n point indicators e_i are idempotent, e_i^2=e_i, hence D e_i=2e_i D e_i. The operator (1-2e_i) is invertible pointwise (entries +/-1), so D e_i=0, for all i. This precludes exact nonzero continuum-like pointwise derivations on **any finite vertex algebra**, independent of the graph or choice of spectral derivative. Refinement or an altered codomain/product is needed.

**Noncommutative graph differential calculus** is a rigorous alternative: with W33 adjacency A and a vertex function f represented by F=diag(f), define d f=[A,F], a matrix with edge entries A_ij(f_j-f_i). It maps vertex functions into an edge/matrix bimodule, NOT back into F. The matrix Leibniz identity is EXACT:

    d(fg)=(d f) diag(g)+diag(f)(d g).

Furthermore its nonnegative action is

    E(f)=1/2 Tr((d f)^dag (d f))
        =f^T(12I-A)f
        =sum_{undirected W33 edges}(f_i-f_j)^2.

The W33 Laplacian has eigenvalues 0^1, 10^24, 16^15 (verified directly). The spectral gap 10 is an immediate caveat: **one fixed 40-vertex graph is not a continuum** and cannot supply arbitrarily low nonzero momenta. Its exact heat trace is 1+24 exp(-10t)+15 exp(-16t), yielding a scale-dependent spectral dimension, not automatically the physical spacetime dimension.

These are finite geometric identities; the graph differential calculus does not yet realize a Lorentzian causal action, Hamiltonian constraints or Einstein equations. A suitable refinement family plus metric-dependent hypersurface-deformation closure is a clear next falsifier.

Background on discrete derivative/no-go and noncommutative graph differential: standard algebra of derivations / commutator differential calculus; this code implements the W33-specific identity.

## Front 5. W33 40-qutrit quantum code: exact diagonal T9 no-go, decoder, injection

We adopt the **parallel** code at 22a122ec8, using W33 collinearity matrix A:

    H_X = A+I (mod3),  rank 11
    H_Z = A+I-J (mod3), rank 10
    H_X H_Z^T=0 (mod3)
    n=40, k=19, (d_X,d_Z)=(4,6).

### A. A code-specific theorem restricting ninth-root transversal phases

Define the *genuine* qutrit non-Clifford T9=diag(1,zeta9,zeta9^8), where zeta9=e^(2 pi i/9). It has local phase exponent f(j)=j^3 in integers modulo 9, for j=0,1,2. Consider a depth-one diagonal layer U consisting of arbitrary independent site powers T9^(lambda_i), multiplied by arbitrary single-qutrit diagonal Clifford phases. The latter are generated (up to overall phase) by q(j)=j(j-1)/2 and j, with exponent multiples of 3.

Necessary code-preservation condition: U must send the logical computational zero-coset codeword

    |0_L> = (1/sqrt(|C_X|)) sum_{h in C_X} |h>

back into the CSS code space, where C_X=row(H_X) in F3^40. Because U is diagonal, every basis amplitude inside that one coset must acquire the *same* phase. At h=0 phase=1. Hence for **every** h in C_X:

    sum_i lambda_i f(h_i) + 3 sum_i mu_i q(h_i)
            + 3 sum_i nu_i h_i = 0 (mod9).

Reducing modulo 3 first forces lambda mod3 into ker(H_X). Let R be a canonical 11x40 RREF basis of C_X and K a canonical 40x29 F3 kernel basis. Thus lambda = K t + 3s (mod9), where t in F3^29. Since f(h)K vanishes modulo 3 for h in C_X, divide those terms by 3 to obtain a homogeneous **F3** equation on s in F3^40, mu in F3^40 and t in F3^29:

    E(h) = [ f(h) mod3 | q(h) mod3 | (f(h) K /3) mod3 ].

The script selects **exactly 70 explicit codewords** h, each generated by one or two rows of R, sufficient to provide these exact finite-field ranks:

    rank E_first40 = 11,
    rank E_first80 = 41,
    rank E_all109  = 70.

Because adding the 29 t-columns raises rank by exactly 29, the only allowed t is ZERO. Thus every lambda_i is divisible by 3 and T9^(lambda_i) is itself just a qutrit Pauli-Z phase. The entire code-preserving layer belongs to the local diagonal Clifford family. In this precise family **no genuinely non-Clifford logical diagonal gate is possible**.

The script records all 70 short certificate witnesses (22 single-generator, 48 two-generator) and SHA256 of the exact 70x109 matrix. This does NOT forbid non-diagonal local conjugations, entangling or multi-block transversal circuits, code switching, magic injection, or a different CSS code. It is a code-specific no-go, not a claim of new general mathematics; transversal non-Clifford obstructions/triorthogonality are well-studied in the literature.

### B. A bias-aware bounded-distance decoder

A pure X error is detected by H_Z, and a pure Z error by H_X. Thanks to (dX,dZ)=(4,6), unique minimal syndromes exist for X weight<=1 and Z weight<=2, respectively.

- Pure-X dictionary: 1+40*2 = **81** syndromes.
- Pure-Z dictionary: 1+40*2+C(40,2)*2^2 = **3201** syndromes.
- Their independent Cartesian product gives 81*3201 correctable X/Z component patterns (including Y-like errors where components occur on the same physical qutrit).
- 2500 seeded independently sampled low-weight component combinations were decoded exactly.

For independent per-site ternary X, Z error components with nonidentity probabilities pX,pZ, the **exact event probability** of falling within these correction radii, and hence a *lower bound* on the total decoder success probability, is

    B(40,pX,1)*B(40,pZ,2),
    B(n,p,t)=sum_{j=0}^t C(n,j) p^j (1-p)^(n-j).

At (pX,pZ)=(0.005,0.01), it equals ~0.97544; globally Fourier-swapping the two error labels (and the code orientation) gives ~0.93825. For equal rates the two orientations tie. This is **not** an erasure-aware/circuit-level threshold, not a full maximum-likelihood logical failure calculation, and not a quantum-memory hardware benchmark.

### C. An exact deterministic T9 injection *identity*, with the missing magic resource exposed

The single-qutrit resource |M>=T9|+> has flat computational amplitudes u_j/sqrt3, with u_j=zeta9^(j^3). For arbitrary input |psi>=sum_j psi_j|j>, apply inverse-SUM with data as control and resource as target, then measure the resource to outcome m. The uncorrected data branch has amplitudes

    psi_j * u_(j+m mod3)/sqrt3.

Every m occurs with probability 1/3. The correction C_m=diag(u_j/u_(j+m)) is, up to global phase,

    m=0: identity,
    m=1: diag(1,omega,1),
    m=2: diag(1,1,omega^2),

where omega=e^(2pi i/3); all are single-qutrit **Cliffords**. Correction leaves exactly T9|psi>, with 60 independently seeded arbitrary statevector/outcome checks and maximum numerical error ~3.5e-16.

By contrast, the original **Hesse SIC strange state** |S>=(0,1,-1)/sqrt2 has zero amplitude on one computational outcome. In the same injection gadget each Kraus branch diag(S_(j+m)) has rank 2, not rank 3, and cannot be a deterministic unitary T9 gate. A strange SIC state can still be a legitimate magic resource in *other* protocols, including multi-copy conversion; it is not a drop-in replacement for |M> here.

Between identical W33 CSS code blocks, physical quditwise SUM respects the stabilizer checks: each X-control check maps to X on *both* blocks; each Z-target check maps to Z^(-1) on control and Z on target. This establishes the logical SUM coupling **in principle**. Actual fault-tolerant T9 needs a high-fidelity **encoded** |M> on an appropriate logical mode, fault-tolerant logical measurement/correction, and a proper resource/noise analysis. The statevector test is unencoded; no FT threshold is claimed.

Related prior art: qutrit Clifford+T injection https://doi.org/10.4230/LIPIcs.TQC.2022.12 ; qutrit strange-state magic https://doi.org/10.1103/PhysRevA.102.042409 ; qudit transversal code families and triorthogonality https://arxiv.org/abs/2001.04887 . The code-specific 70-row test is derived here.

## Exact reproduction

    python analysis/toe_20261119_four_structural_frontier_tests.py
    python analysis/toe_20261119_w33_code_gate_and_decoder.py
    python -m unittest discover -s tests -p test_toe_20261119_five_front_research.py -v

Machine-readable outputs:

    data/toe_20261119_four_structural_frontier_tests.json
    data/toe_20261119_w33_code_gate_and_decoder.json

The test file contains **12 focused tests** covering each theorem, counterexample, code circuit, and declared performance metric. All calculations are deterministic, machine-generated and falsifiable at their specified scope. The full repository test suite and actual hardware trials are separate deliverables.

## Top five independent next investigations

1. **UV naturalness:** Can an asymptotically free parent group or composite sector derive SIC target couplings without injecting all 45/19 anchor constants? Demand beta functions, anomaly-free reps, vacuum selection and the full mass spectrum.
2. **Chiral geometry:** Write a bona fide singular internal space with non-torus/spherical gauge curvature, compute charged localized index, E6 multiplets, global/local anomaly inflow and 11D equations.
3. **Photonic memory:** Build full process-tensor tomography for input/intervention/output with a trusted reference, event-ready detection, loss and photon leakage, and a fully specified classical-memory exclusion protocol.
4. **Lorentzian continuum:** Couple graph-bimodule differential forms to a dynamical metric/refinement family, test the field-dependent Hamiltonian-diffeomorphism algebra, and reject models without the correct constraint closure.
5. **Encoded non-Clifford computing:** Build an encoded T9 resource using the W33 CSS logical coordinates and a complete magic-state distillation/injection circuit, including all error locations, decoder overhead and logical performance.
