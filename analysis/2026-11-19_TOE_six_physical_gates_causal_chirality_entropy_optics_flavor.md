# Eight linked physical falsifiers: causal determinants, gauge anomalies, optics, gravity entropy, flavor, information geometry and diamond holonomy

**Research date: 2026-11-19. Status: five original physics fronts plus three independent cross-sector gates, 68 focused tests passed; a fundamental TOE is NOT derived.**

Project: wilcompute/W33-Theory. This is a new-to-repository pass building on latest master commit 25207be19702a32bdcd4a7623623b6efc0ddb1bf and immediately prior commits 4bf689c, 8f9ffe8, d1a3119. Both connected GitHub and remote Windows computer were reviewed. The physical targets are (I) a genuine causal Dirac operator, (II) gauge/matter consistency and a selected action, (III) implementable number-conserving photonic Bell gates, (IV) gravitational causal-history measure, (V) derived flavor strength and mass content, plus (VI) an independent information-theoretic cross-sector probe. Other agents' work is preserved; nothing here is claimed as discovery of the causal torus/overlap index, SU2 center breaking, two-copy Bell activation, or the Pascal SSR theorem, all already present on master.

## Timely outside research that changes our target

- **Lu and Shao, "On reflection positivity of lattice chiral fermions", Nov 15 2026, https://arxiv.org/abs/2611.20084.** The finite-lattice overlap *Weyl* fermion is not reflection positive in two and four dimensions, obstructing the ordinary Osterwalder-Seiler/Osterwalder-Schrader Hilbert reconstruction; the overlap *Dirac* fermion is different. Hence our previous Ginsparg-Wilson identity/index tests on the synthetic torus are not a proof of a consistent physical **chiral** theory. An actual Lorentzian causal spinor construction must address unitary evolution, appropriate positivity and global anomalies, not only an integer index. This is a source-derived result, NOT independently reproduced in the following tests.
- **Brod and Galvão, "Linear-optical nonlocality without postselection", Nov 14 2026, https://arxiv.org/abs/2611.19570.** They prove the two-photon passive-optics maximum 1+sqrt2 and construct a family of even-photon CHSH values approaching 2sqrt2. We compare those published passive circuits against our more permissive ideal SSR measurements. Our algebraic witness restricts the Hamiltonian generator, NOT all passive-interferometer-plus-detection measurements.
- **Carlip et al., "Path integral suppression of badly behaved causal sets", https://arxiv.org/abs/2209.00327.** Genuine oscillatory causal quantum actions CAN suppress KR-type nonmanifoldlike histories; our positive-weight determinant entropy calculations are deliberately NOT a no-go for such interference.
- **Witten SU2 global anomaly**, see David Tong Standard Model lecture notes https://davidtong.org/pdfs/teaching/standardmodel5.pdf: parity of left Weyl SU2 doublets; this is prior standard particle physics.

## Gate I: a retarded-only causal fermionic vacuum determinant is exactly graph blind

Let C be ANY finite DAG with N events, A_C its weighted strictly forward causal adjacency in a topological ordering, and m!=0. A_C is nilpotent (A_C^N=0). Consider the simple quadratic Grassmann kinetic matrix

    D_C(m,alpha)=m I - alpha A_C.

Since D_C is triangular with all diagonal entries m,

    *** det D_C = m^N ***,

for every edge arrangement and alpha. Under an arbitrary relabeling it is conjugated by a permutation and the determinant is unchanged.

This is not because the theory has no causal propagation. It has an exact retarded inverse

    D_C^(-1) = (1/m) sum_(k=0)^(N-1) (alpha A_C/m)^k,

and each power counts weighted causal paths. Distinct DAGs yield different Green functions even though their zero-source Grassmann determinants coincide.

We verified four N values, multiple masses/couplings, random relabelings, nilpotence, inverse path sums and explicit unequal propagators. A directed cyclic ring with holonomy U=e^(i theta) instead yields

    det(m I-alpha T)=m^N-alpha^N e^(i theta),

so closing a transport loop can make a vacuum determinant sensitive to global holonomy. The original chronology-based DAG itself has no directed closed walks; a physical cause of sensitive loop/holonomy information must be separately supplied, without sacrificing microcausality. Reciprocity, nonlinearities, boundary effects and matter interactions can evade the simple result.

**What this eliminates:** the assumption that *merely coupling a finite causal adjacency as a one-way kinetic term* makes the fermion determinant automatically select manifoldlike histories.

## Gate II: one additional constraint for chirality — the global SU2 anomaly

Four-dimensional SU2 has pi4(SU2)=Z2. A nontrivial large gauge transformation changes the sign of the functional measure for an odd number of left Weyl SU2 doublets; such a spectrum is inconsistent unless additional physics resolves the anomaly. A Dirac doublet contributes two equivalent Weyl doublets and is NOT subject to this odd-doublet veto.

We reproduce the anomaly/parity ledger:
- one isolated left Weyl SU2 doublet: sign -1, FAIL;
- a vectorlike SU2 Dirac doublet: 2 Weyl, sign +1, PASS this test;
- one complete SM generation: three color copies of the quark doublet + one lepton doublet = 4, PASS;
- three SM generations: 12, PASS;
- adding just one extra Weyl doublet to the 3-gen SM: 13, FAIL;
- adding a vectorlike pair: 14, PASS.

Separately the familiar left-Weyl multiplet integer hypercharges y=6Y pass the ordinary SU3²Y, SU2²Y, gravitational-Y and Y³ anomaly sums. The SM quotient condition 2t+3s+y=0 (mod6) also passes for the supplied multiplets. The elementary parity sign and integer anomaly computations DO NOT independently establish a 5D mod-2 index on a proposed causal spacetime, or derive the representations.

**Tension for earlier toy models:** a "single fundamental" in a center-breaking determinant may represent a VECTORLIKE Dirac particle and can be UV consistent; replacing it with a single genuinely chiral Weyl doublet changes the anomaly problem. A singlet does not cancel the Witten SU2 doublet anomaly. Deriving chirality and counting chiral matter must precede any claim of a physical 4D gauge theory.

## Gate III: a specific four-copy CHSH optimal observable needs more than a one-body generator

The previous pass derived the ideal unconstrained-collective-number-SSR formula

    S_n=2+(2sqrt2-2)[1-2^(popcount(n)-n)]

and explicitly implemented one set of local binary observables. At n=4 consider Alice's two-photon hard-core basis with bit masks

    [3,5,6,9,10,12].

A1 pairs the lexicographic masks into (3,5), (6,9), (10,12). The middle pair is 0110 <->1001: BOTH occupied modes must change. For ANY quadratic, number-conserving one-body bosonic Hamiltonian

    H_1 = sum_(i,j) h_ij a_i^dagger a_j,

the matrix element between these occupation states is ZERO, since one-body hopping changes only one occupied mode. The desired A1 entry is +1. We construct the entire projected real one-body generator basis (occupations and real symmetric hopping), project the target into it, and obtain a Frobenius residual exactly sqrt2.

This is a rigorous **generator-algebra witness for the specific A1 operator**, not a no-go on passive optical *measurements*: nonlinear output binning and photon-number-resolving detectors can produce observables not equal to a quadratic Hamiltonian, and arbitrary optical circuits/ancillas may synthesize the target by other means. It is a physical-gate synthesis hurdle, not a demonstration that photonic Bell tests are impossible.

Published Brod/Galvao passive first-success ladder, for even n=2k:

    S_passive(2k)=2sqrt2-(2sqrt2-2)/2^k

compares with our ideal unrestricted number-SSR maximum. Scores:
- n=2: both 2.414214;
- n=4: passive 2.621320 vs ideal 2.724874;
- n=6: passive 2.724874 vs ideal 2.77665;
- n=8: passive 2.77665 vs ideal 2.821955.

The passive construction is a lower bound achievable with their stated resources, not claimed to be globally optimal above two photons. This comparison is about **available control algebra**, not graph-based BQP by itself.

## Gate IV: positive gapped local determinants cannot beat quadratic causal-history entropy against one reference

The prior Burnside calculation studied marked-layer incidence orders of size N with populations N/4,N/2,N/4, M=N²/4 independent adjacent-layer links. The number of layer-preserving unlabeled orbits obeys

    H_orbits >= 2^(N²/4) / [ (N/4)!² (N/2)! ].

This quotient is specifically by layer permutations, NOT all unlabeled finite partial orders.

Add a deliberately strict, explicit determinant condition: every bad-history fermion matrix has qN singular values at least a>0, and one stipulated good-history reference fermion matrix has qN singular values at most b, and all histories carry identical positive bare factors. Hadamard/product of singular values gives

    total_bad_weight / weight_one_good
      >= H_orbits * (a/b)^(qN).

For q=4, a=.5, b=2, we get:
- N=8: log10 ratio lower bound -16.4 (inconclusive);
- N=32: -22.5 (inconclusive);
- N=64: +92.066 (bad class dominates the single comparator by at least 10^92);
- N=128: +764.82.

This does NOT show bad orders dominate the WHOLE manifoldlike class or any physical oscillatory causal quantum measure. It does show why a **uniformly gapped, bounded local matter determinant** changes positive weights by at most exp(O(N)) and cannot on its own remove exp(O(N²)) combinatorial entropy when only one reference geometry is compared.

A potentially powerful escape is **geometry-selective exact fermion zero modes**, for which singular lower bound a>0 fails. The zero-source determinant of a bad geometry may then vanish, producing a near-projector rather than merely mild reweighting. But zero modes on all histories (e.g. m=0 for an upper triangular retarded operator) would erase all vacuum terms rather than select physical geometry; zero-mode-saturating insertions and a correctly normalized quantum measure are additional requirements. Oscillatory BDG gravity remains another well-established possible route.

This is an especially testable dependency: instead of trying to solve gravity with arbitrary fermion weights, first derive a chiral, gauge-consistent operator and **measure its singular-value distribution as a function of intrinsic causal geometry**.

## Gate V: graph connectivity is weaker than robust flavor-symmetry breaking

Prior work proved that a connected Yukawa graph eliminates exact independent family-charge U1 directions in an imposed one-Higgs model. But a tiny edge does not make the symmetry strongly broken.

For three flavor vertices with two weighted edges a and b and charge-mismatch quadratic penalty

    E(X)=a(X1-X2)²+b(X2-X3)² = X^T L X,

the graph Laplacian has eigenvalues

    0, (a+b)-sqrt(a²-ab+b²), (a+b)+sqrt(a²-ab+b²).

The first nonzero eigenvalue lambda2 measures stiffness against the least-constrained family-difference direction. For a<<b,

    lambda2 ≈ 3a/2.

Even if a>0 and the graph is CONNECTED, an arbitrarily small a leaves an almost conserved family charge. Numeric exact agreement was verified for a=1, .1, .01, 1e-4 and 1e-6 with b=1.

Thus charged-lepton interactions can algebraically forbid an exotic flavor U1 without physically making its breaking appreciable. This is not a PMNS prediction: charge-mismatch penalty weights and physical Yukawa matrices are distinct objects until a microscopic model relates them.

## Gate VI (outside-box): an information metric on the toy spin/gauge-sector weights

Use the PREVIOUS spin/SU2-center compensation toy on a periodic circle. Its equal-prior, doublet-plus-singlet zero-source determinant weights lead to four normalized sectors

    P=(r³,r,1,r²)/[(1+r)(1+r²)],   r=tanh(mu/2),

where mu=m_phys * circumference.

This special distribution factorizes into two binary odds (r and r²). Its **classical Fisher information** for mu is exactly

    I(mu)=[(1-r²)/2]² [1/(r(1+r)²)+4/(1+r²)²].

We derived it analytically by differentiating log probabilities and confirmed it against independent centered finite differences over seven mass-length values.

Examples:
- mu=.05: I(mu)=10.5058, one sector dominates strongly;
- mu=.1: I(mu)=5.5067;
- mu=1: I(mu)=.57649;
- mu=5: I(mu)=.000227;
- mu=10: I(mu)=1.0306e-8.

For mu>>1, I(mu)~5 exp(-2mu). Heavy matter makes these four spin-center toy-sector probabilities practically indistinguishable. This is a precise **information-theoretic expression of matter decoupling from global topology** in the supplied toy model. It does NOT create a fundamental information metric of spacetime, quantify experimentally measurable spin structures, or derive the Born rule.

The cross-connection to the photonic problem is structural: *a sector can exist mathematically while an allowed observer lacks resources to distinguish it*. In the photon case this is a local particle-number SSR and an optical control limit; in the spin case it is an assumed mass-dependent probability family. This analogy is suggestive only until an actual common microscopic operational law is produced.

## Gate VII (additional outside-angle): zero modes may weight the WRONG topology

The Gate IV conditional entropy result identified geometry-specific zero modes as one possible escape from a uniform lower singular-value bound. Before relying on that escape, we implemented a counterexample using **combinatorial Hodge theory**.

Construct n x n oriented periodic square-cell tori, n=3,4,5. Derive cellular boundary maps B1:C1->C0 and B2:C2->C1 directly from edges and oriented faces and verify B1 B2=0. The 1-form Hodge Laplacian is

    Delta_1 = B1^T B1 + B2 B2^T,

and by finite-dimensional combinatorial Hodge theory the dimension of its kernel is b1. Our periodic tori have (b0,b1,b2)=(1,2,1) and exactly two zero eigenvalues of Delta_1 at all three sizes. A filled square disk with four edges and one face has Betti vector (1,0,0) and no 1-form zero modes (its Laplacian eigenvalues are exactly 2,2,4,4).

For a positive regulator mu, det(Delta_1+mu I) contains a factor mu^b1. Removing all unrelated nonzero-eigenvalue factors, the **torus normalized determinant zero-mode factor** is mu^2, while the disk's is 1. Thus as mu->0 the naive positive unsaturated determinant SUPPRESSES the torus rather than the contractible disk.

The two complexes have different numbers of degrees of freedom, so these normalized kernel factors are not comparable full gravitational history weights. A 1-form Hodge Laplacian is also not the causal spinorial chiral Dirac operator, and it does not define a physical fermion measure. The value of this test is purely a **sign-of-selection falsifier**: topological zero modes do not by themselves guarantee that the supposedly physical spacetime histories dominate.

Reproduce:

    python analysis/toe_20261119_hodge_zero_modes_geometry_selector_control.py
    python -m pytest -q tests/test_toe_20261119_hodge_zero_modes_geometry_selector_control.py

Files: analysis/toe_20261119_hodge_zero_modes_geometry_selector_control.py ; tests/test_toe_20261119_hodge_zero_modes_geometry_selector_control.py ; data/toe_20261119_hodge_zero_modes_geometry_selector_control.json.

The revised first-priority experiment is to find an **actual anomaly-free Lorentzian causal spinorial kinetic operator** whose geometry-selective zero modes and interactions favor genuine manifoldlike geometries, rather than assuming any topological nullity will do.

## Gate VIII (new constructive link): gauge-invariant holonomy from two FORWARD causal paths

Gate I showed that a strictly forward causal kinetic matrix has a completely graph-blind zero-source determinant. One might mistakenly conclude that gauge curvature or quantum phase interference requires closed causal-time paths or an advanced term. That conclusion is too strong.

**Exact four-event counterexample.** Consider a directed acyclic diamond with arrows 0->1->3 and 0->2->3. Give each directed edge a unit U1 transport U_ij. Put the four weighted links in a strictly upper-triangular matrix T. For the same one-sided kinetic operator

    D=m I-alpha T,

the determinant is STILL m^4, independent of all link phases. But the inverse includes the two length-two forward paths:

    G_03=(D^-1)_03=(alpha²/m³)(U_01 U_13 + U_02 U_23).

Under a local gauge-frame change g_i at every event, each U_ij transforms as g_i U_ij conj(g_j). The relative phase

    W=(U_01 U_13)*conj(U_02 U_23)

is strictly gauge-invariant and equals the **Wilson loop comparison** of the two forward paths (the inverse of one path is a reference transport, NOT a particle travelling backward in causal time). Consequently,

    |G_03|²=(alpha^4/m^6)[2+2 Re(W)].

For mass m=1.3 and coupling alpha=.6, the intensity is 0.1074001478 at zero relative phase and essentially zero at pi; the determinant remains 2.8561 in both cases. The code verifies exact causal nilpotence, the path-sum identity, 40 independent random gauge-frame transformations, phase covariance of G and gauge invariance of W and |G|².

**What this newly closes:** a manifestly causal DAG can contain operationally meaningful gauge holonomy measured by two-path interference, without directed closed cycles or a graph-sensitive vacuum determinant. The quantum-interference response and vacuum statistical weight are distinct observables.

**What's still missing:** Why these complex link phases exist, why physical particles have the chosen U1 representation, where an actual Lorentzian unitary quantum state and Born-rule intensities originate, and how the same construction could yield nonabelian SM gauge curvature and dynamical Einstein spacetime. The proof is an ordinary known holonomy/interference phenomenon applied to the causal DAG; the novelty is only the connected, reproducible project calculation.

    python analysis/toe_20261119_causal_diamond_gauge_interference.py
    python -m pytest -q tests/test_toe_20261119_causal_diamond_gauge_interference.py

12 new focused tests pass. File: analysis/toe_20261119_causal_diamond_gauge_interference.py; tests/test_toe_20261119_causal_diamond_gauge_interference.py; data/toe_20261119_causal_diamond_gauge_interference.json.

## Integrated dependency revision and next test

Our earlier proposed chain was: causal incidence -> spatial topology -> oriented spin/gauge transport -> chiral matter -> fermion determinants -> physical history measure -> Einstein dynamics. The new gates show that **each arrow has a sharper necessary test**:

- A causal forward link matrix gives nontrivial propagators but a graph-blind determinant; recover an operator with physics-sensitive loops/holonomies AND true Lorentzian causality.
- An integer overlap index is not a sufficient physical chiral completion; check quantum positivity and the Witten/global anomalies.
- A nonzero topological/quantum Bell witness may require non-one-body controls, mode resources, and high survival probabilities to implement.
- A positive gapped matter determinant cannot simply overwhelm quadratic bad-history entropy against a lone good reference; look for selective zero modes, oscillatory action, or richer measures.
- Yukawa graph connectivity is only a zero-vs-nonzero algebraic condition; its weighted spectral gap is the relevant robustness scale.
- Distinguishability metrics quantify how reliably observers could separate model sectors but cannot select those sectors without a dynamical principle.

**Therefore a higher-value immediate next research goal is the 3+1 Lorentzian, anomaly-free causal Dirac/operator construction with nontrivial closed transport and a physically valid Hilbert-space structure.** It would make the question "can fermionic zero modes select manifoldlike causal histories?" experimentally falsifiable in finite computations, without adjusting a free penalty for every geometry.

## Reproduction and caution

    python analysis/toe_20261119_causal_gauge_optics_entropy_flavor_info_v10.py
    python -m pytest -q tests/test_toe_20261119_causal_gauge_optics_entropy_flavor_info_v10.py

Output JSON: data/toe_20261119_five_physics_global_gates_and_fisher.json
Tests: 68 independent focused regressions across three new suites, all PASS (43 original, 13 Hodge control, 12 causal-diamond gauge interference). These calculations are finite mathematical results and scoped comparisons, not a complete TOE or independently observed physical predictions.

## Independent test and synchronization certificate

The complete related November 19 regression, consisting of **47 separate pytest modules**, passed **784 tests** in 127.31 seconds on the connected Windows machine. All three new producers were also run independently, including the 40-random-gauge-frame diamond certificate. The new three suites contribute **68 tests** (43 original frontiers, 13 Hodge selection controls, 12 gauge-interference checks). The regression success is finite software verification, not a derivation of physical laws or external experimental evidence. The local Git pre-commit hook may be unavailable; explicit pytest and git diff --cached --check are the enforced checks.

## Top five distinct next experiments

1. **Causal 3+1 spinor with a physical Hilbert space:** build a gauge-covariant Lorentzian Dirac operator on independently generated 4D causal sets, test exact retarded propagators, chiral index, no doublers and reflection-positive/alternative unitary reconstruction; check 2026 overlap-Weyl obstruction directly.
2. **Selective topological zero-mode entropy firewall:** construct manifoldlike and KR-like families of matched N, compute full fermion singular spectra and normalized relative weights, and see if the bad geometries acquire genuine protected zero modes without killing all vacuum sectors.
3. **Optical compiler and resource costs:** synthesize the n=4 optimal SSR Bell observable using actual passive interferometer, photon counting, adaptive feedforward or ancillary nonlinearity, and report the full source/energy/loss budget; compare with the November 2026 achievable ladder.
4. **Global chiral matter/gauge completion:** impose SU2 mod-two anomaly, local cubic/mixed anomalies, SM global Z6 quotient, dynamically breaking fundamental representations, RG, and realistic mass constraints **at once**, then search for action uniqueness rather than fitting them sequentially.
5. **Flavor dynamics and operational information selection:** derive the actual weighted Yukawa graph/PMNS matrix from a microscopic causal spin-gauge operator; measure the robust lambda2 and Fisher distinguishability of competing global sectors instead of treating their formal labels as predictions.

**Honest outcome:** Six executed conditional falsifiers and a sharpened dependency hierarchy. The Standard Model, full GR, physical quantum measure, Born rule and TOE remain unproved.
