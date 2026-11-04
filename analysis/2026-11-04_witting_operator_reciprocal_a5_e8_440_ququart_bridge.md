# The reciprocal A5 selection: W33 graph amplitudes versus Witting ququart observables

**November 4, 2026 UTC.** Baseline 1ccd113da6383d6d985acc886d2e2c0f1660a4be. Independently executed on an isolated worktree with the authorized Windows machine. Mathematical and ideal quantum control results, not an experimentally verified TOE or particle model.

## Source/priority audit

Witting's 40 projective rays, their 40 orthogonal tetrads, and the equivalence of their orthogonality graph with W(3,3) are established. Key references: Waegell and Aravind (2017), The Penrose dodecahedron and Witting polytope are identical in CP3, https://doi.org/10.1016/j.physleta.2017.03.039 ; A. Yu. Vlasov, Scheme of quantum communications based on Witting polytope (2025), https://arxiv.org/abs/2503.18431 ; and Vlasov, Quantum entanglement and contextuality with complexifications of E8 root system (2022), https://arxiv.org/abs/2210.15338. **The E8 to Witting connection itself predates these calculations.**

The repository already proves the Witting 40-ray complex projective 2-design in analysis/w33_20261015_toe90_vlasov_ququart_design.py. Native PSp4(3) has exactly two A5 conjugacy classes, proved by analysis/w33_pass999_a5_double_class_census.py. Prior work 2f3791d proves a full-H4-to-W33 graph-label action obstruction; 6816ebb builds 25-by-60 Reye packet incidence, its A4+A4 eight-dimensional kernel and two E8 index-five lattice glues. Commit 1ccd113 constructs a real isometric class0 25-to-40 graph-spectral bridge and an initial class1 rank20 obstruction. The specific NEW check here is whether those native graph-amplitude embeddings actually correspond to physical ququart Hermitian observables, and whether a reciprocal class1 physical state embedding can be constructed and measured.

## Reproduce

- analysis/toe_20261104_witting_operator_dark_spectral_A5_duality.py -> data/toe_20261104_witting_operator_dark_spectral_A5_duality.json
- analysis/toe_20261104_witting_A5_unitary_lift_and_fisher.py -> data/toe_20261104_witting_A5_unitary_lift_and_fisher.json
- analysis/toe_20261104_two_e8_root_to_witting_density_codebook.py -> data/toe_20261104_two_e8_root_to_witting_density_codebook.json
- tests/test_toe_20261104_witting_operator_e8_physical_bridge.py

Existing old repo sources and actual Witting ray vectors are imported. Every 8x8/40x8/4x4 matrix and all 440 root coordinates are serialized to JSON. No numerical output is fabricated or taken on trust from a name match.

## Finding 1: the successful graph25 bridge is physically dark

Let A be the W33 collinearity adjacency (equivalent here to Witting ray orthogonality), J the 40x40 all-ones matrix, and P_i the forty rank-one Witting ququart ray projectors. The Hilbert-Schmidt Gram of their linear operator synthesis is exactly:

    G_ij=Tr(P_i P_j)=(2I+J-A)/3.

W33 adjacency eigenvalues are 12(1), 2(24), -4(15). The optical real operator Gram therefore has eigenvalues 10(1), 0(24), 2(15). Its rank is16 (the full real dimension of 4x4 Hermitian matrices); its ENTIRE 24D kernel is W33 adjacency eigenvalue+2.

The previous real class0 graph25 spectral image is precisely the 25D W33 eig(12)+eig(2) subspace. Under the physical synthesis map from 40 real coefficients to 4x4 Hermitian matrices, all 24 eig(2) dimensions vanish; only the uniform component becomes an identity multiple. The E8 8D packet kernel in that previously successful 25D graph map is also optically invisible. Verified: Gram times its 40x25 isometry has rank1.

A second no-go: the graph projector onto eig(12)+eig(2) is Q=(16I+4A-J)/24, with diagonal5/8, adjacent offdiag1/8, and nonadjacent offdiag -1/24. Thus it cannot equal WW^T for any entrywise-nonnegative real orthonormal 40x25 W, since such a product is entrywise nonnegative. A signed/complex and physically nontrivial map is necessary. Neither result prohibits arbitrary quantum channels with ancillary systems.

## Finding 2: the A5 conjugacy class preference reverses at ququart observables

The source exact 25-by-60 packet incidence has eight real blind directions from zero-sum row/column potentials: A4+A4, which under diagonal A5 decomposes as 4+4. The physically traceless ququart operator coefficients span W33 eigenvalue-4 of dimension15.

For actual class0, this -4 submodule decomposes as 3+3prime+4+5 and contains ONE 4: maximal rank from 4+4 is4.
For actual class1, it decomposes as 1+3+3prime+4+4 and contains TWO 4s: full rank8 is possible.

Group-average an actual seeded 40x8 matrix over all60 native A5 permutations, project to W33 eig(-4), then polar normalize: independently seeded ranks are [4,4,4] for class0 and [8,8,8] for class1. For class1 explicitly store an 40x8 real E satisfying E^TE=I8, A E=-4E, and full native A5 covariance. Via the exact Witting-to-symplectic 40-label map define O_a=sum_i E_ia P_i. These are eight real-linearly independent traceless Hermitian 4x4 operators with Tr(O_a O_b)=2 delta_ab. The 16 test states I4/4 +/- .1 O_a are trace-one PSD and differ under Witting measurement.

This is a faithful embedding of **8 REAL parameters** near a mixed-ququart state. It is NOT eight Hilbert-space basis states, eight qubits, an E8 particle representation or physical self-entanglement.

## Finding 3: actual physical projective-unitary A5 covariance

The 40 complex Witting rays supply more than graph labels: their triple Bargmann invariants record physical phases. For all60 native W33 permutations in each actual A5 class, transport the permutations through the known explicit Witting/symplectic graph isomorphism and check all complex triple products <i|j><j|k><k|i>. ALL60 elements in each class preserve the complex products, not just their magnitudes, and none requires antiunitary conjugation. From order-5 and order-3 generators of each class, solve exact ray phase consistency to construct 4x4 unitary representatives and verify their conjugation on each of 40 ray projectors.

Crucially for class1, these generators also satisfy U_g O_a U_g^dagger = sum_b V_g(ba) O_b, where V_g is the source eight-real-parameter A5 action. Thus the class1 physical encoding is A5 covariant under genuine ququart U4 conjugation, not merely graph symmetry or output relabeling. The representation is projective up to global phases. No full H4 extension follows.

## Finding 4: 40-outcome Witting tomography, Fisher and erasure calibration

Use Witting effects P_i/10, summing to I4. For rho(theta)=I4/4 +sum_a theta_a O_a the 40 probabilities are EXACT on the positivity domain:

    p_i(theta)=1/40 + (1/5)sum_a E_ia theta_a.

Witting Fisher information at theta=0 is (8/5)I8 per DETECTED photon. The linear estimator theta_hat=5 E^T(counts/N) attains its local Cramer-Rao covariance (5/8N)I8. For independent rail-independent survival eta and a 41st vacuum/no-click effect, the Fisher block for eight theta coordinates and eta is diag((8eta/5)I8, 1/[eta(1-eta)]); the cross terms vanish at theta0. With N=10000 incident photons and eta=.85 the predicted per-coordinate variance is5/(8Neta). A 1000-repetition seeded multinomial simulation finds eight sample variances within20% of theory. Calibration errors, dark counts, correlated losses and state preparation errors remain unmodeled.

## Finding 5: 440 root-derived mixed states, exact metric and an information-cost warning

The two incompatible index-five E8 completions from the prior packet A4+A4 kernel contain 240 roots each, sharing exactly40 roots, hence440 distinct embedded roots. They do NOT form one integral E8 lattice. Every root r is a real eight-vector of squared norm2. With epsilon=.1 construct:

    rho_r=I4/4+(epsilon/sqrt2) sum_a r_a O_a.

All440 explicit matrices are PSD trace-one and pairwise distinct. Minimum eigenvalue0.1526751, purity0.27. A uniform analytical PSD ball of radius1/sqrt24 in the eight real theta coordinates guarantees positivity for any state within it. The **full 440x440 matrix** of Hilbert-Schmidt state overlaps satisfies the exact original root metric identity:

    Tr(rho_r rho_s)=1/4+epsilon^2(r dot s).

It includes exactly40,000 mixed-sheet root pairs with noninteger Euclidean inner product, preserving the earlier arithmetic incompatibility instead of silently identifying their E8 sheets. The Witting40 POVM distributions are all distinct and invert all eight theta coordinates. The minimum pairwise distribution total-variation distance is 0.0306071208.

**Capacity falsifier:** uniform 440-label entropy is log2(440)=8.7813597135 bits. Our chosen weak epsilon=.1 Witting measurement yields only 0.0116177573 bits MUTUAL INFORMATION per detected photon for the uniform label prior. Under repeated independent known-label preparations and fixed POVM, a Fano lower bound for <=5% classification error requires at least694 detected copies, or816 incident photons at independent eta=.85. These are necessary, NOT sufficient, sample counts. The one-copy ququart Holevo accessible information is at most log2 4=2 bits, regardless of how many nonorthogonal states are on the codebook. Neither the codebook nor the information bound proves a physical E8 clock.

## Physics claims and five independent next gates

No physical state-preparation circuit, genuine time-entanglement measurement, causal multi-time interventions, full-H4 ququart operator action, Lorentzian Einstein gravity or new Standard Model parameter is derived. The strongest new bridge is the actual 8-real-parameter A5-covariant class1 ququart observable construction, with a formal 440-root mixed-state image and exact tomography.

1. **Optical implementation:** compile the actual class1 eight Hermitian density preparations and A5 U4 generators into native MZI/beam-splitter unitary and ancilla/mixing channels; calibrate all40 output effects and channel drift.
2. **Temporal experiment:** couple those physical ququart probes to a real three-time qutrit process with interventions and compare to an explicit classical hidden-memory null, not ordinary flux fringes or unheralded postselection.
3. **Two-glue dynamics:** derive a microscopic action connecting the two 240-root intersheet hopping networks with the Z2 gauge plaquette, and test whether sheet order remains gauge-invariant and stable without hand-selecting flux.
4. **Full symmetry:** prove or falsify whether the class1 A5 real-density representation extends to a CP-covariant full-H4 quantum process with auxiliary space. The existing 40 GRAPH-label order-five theorem alone does not decide that broader question.
5. **Real gravity:** upgrade the prior Lorentzian one-interior-vertex deficit-branch control to a consistent causal multi-simplex Regge boundary action, and explicitly test nonlinear Hamiltonian and momentum constraint brackets.

**Provenance and scope:** the core Witting 2-design, E8 glue roots, W33 spectrum, native A5 subgroup census and quantum tomography formulas have published/repo precedents. This executable computation integrates those known ingredients into an explicit branch-selective physical density-state bridge and discovers hard limitations that must be satisfied before any TOE claim.


## Follow-up capacity falsifier: ensemble Holevo bound and 4-outcome readout

Additional reproducible producers:
- analysis/toe_20261104_two_e8_witting_holevo_capacity_scan.py -> data/toe_20261104_two_e8_witting_holevo_capacity_scan.json
- analysis/toe_20261104_two_e8_witting_basis_information_search.py -> data/toe_20261104_two_e8_witting_basis_information_search.json
- tests/test_toe_20261104_witting_holevo_basis_readout.py

The previous generic log2(d)=2-bit Holevo ceiling was weak. Under the SPECIFIC uniform 440-root mixed-state ensemble, rho_bar=I4/4 exactly by antipodal symmetry and the ensemble-dependent Holevo upper bound is chi=2-440^(-1) sum_r S(rho_r), a standard known formula (Fuchs and Caves PRL73 3047 1994; Preskill lecture notes https://www.preskill.caltech.edu/ph219/quantum-capacities-2011.pdf). At epsilon0.1, chi=0.059060128698335435 bits per copy while the fixed Witting40 POVM attains only 0.011617757280846361 bits (19.6711% of this UPPER bound, not a proven fraction of attainable optimum). At epsilon0.2 all 440 states remain strictly PSD, the Witting40 information reaches 0.04748117085608069 bits, and Fano's NECESSARY 5%-error copy count falls from694 to170 detected copies. The true optimal POVM and sufficient decoder copy count are unknown; calibration and state-preparation errors are omitted.

For actual photonic readout, compute mutual information for EACH of the forty orthonormal tetrads (four-output projective bases) forming the Witting40 construction. Every one yields identical mutual information within 1e-12 at epsilon0.1 and epsilon0.2, and each equals the full uniform Witting40 POVM. This is a SPECIAL property of the uniform 440-root ensemble and these verified measurements, not a universal statement about arbitrary quantum states. The uniform mixture over labeled tetrads gives the 40-outcome Witting POVM after forgetting which of the four bases contained each ray, and retains the same information when basis labels are logged.

Search 320 independent, seeded, Haar-distributed ququart orthonormal bases (each checked unitary). The best sampled basis gives 0.01443977804 bits at epsilon0.1 and 0.05938471748 bits at epsilon0.2, about24% more information than a Witting tetrad or the full Witting POVM. The full complex 4x4 matrix for each best candidate is frozen to JSON for possible hardware Givens compilation. This is a finite random candidate search, NOT a numerical/global proof of the optimal POVM, and the candidate itself is ordinary quantum measurement physics, not new emergent time or gravity.

**Important research lesson:** the eight-dimensional A4+A4 kernel has a real physical ququart density representation under a compatible reduced A5, and the 440-state codebook preserves a formal E8 root metric; however, its communicated information is modest. Even the 2-bit ququart bound is overly permissive relative to this actual weak mixed-state ensemble. Hardware and causal process witnesses are independent next gates.
