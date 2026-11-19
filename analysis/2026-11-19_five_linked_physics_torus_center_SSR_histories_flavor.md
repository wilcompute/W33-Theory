# Five linked TOE physics calculations: causal torus flux, dynamical center breaking, operational photons, unlabeled history counting, and flavor constraints

**2026-11-19.** Independent executable follow-on to current `wilcompute/W33-Theory` master, including commit `7518edfe`, concurrent `d1a3119` (independent E8 Higgs source and four-layer BDG4 scalar controls), and prior 2D overlap calculation `analysis/toe_20261105_overlap_flux_chirality_index.py`. The complete d1a3119 GitHub diff was reviewed; its scalar d'Alembertian/GUT tests are distinct from the Burnside **history-measure** and lepton flavor graph calculations here. **No complete Theory of Everything is derived.** Each test is conditional on explicit assumptions and its claims are scoped to those assumptions. The objective is to find high-leverage *dependencies*: what additional information must be derived before several apparently independent pieces can become calculable rather than fitted.

## Five fronts and the new connections

### I. A higher-dimensional causal-to-fermion bridge: order-derived torus, then 2D overlap index

**Construction.** Begin with two artificial layers, each containing L×L labeled events whose past/future incidence is that of 3×3 periodic square neighborhoods. L=5,6,7,8 were investigated. Only the binary incidence matrix is passed to the reconstruction; the coordinates used to *generate* the incidence are not used in the recovery. Enumerate all Dowker nerve simplices through dimension three and perform exact GF(2) boundary-matrix reduction. Every tested size has

    (b0,b1,b2)=(1,2,1), Euler characteristic b0-b1+b2=0,

consistent with a two-torus. Each pair of future witnesses whose past shadows have maximal positive off-diagonal overlap becomes adjacent. The result is a **4-regular n=L² graph**, with **2L² edges** and maximum overlap six. From that graph alone, a coordinate chart can be reconstructed up to origin/axis/orientation choices: opposite neighbors share one common neighbor; perpendicular neighbors share two. Following straight cycles and completing squares yields an L×L toroidal chart. Independent permutations of the two layers preserve topology and allow chart reconstruction again.

Now insert a **specified** U(1) flux Q, gamma matrices and a Wilson regulator mass m, following the repository's existing 2D overlap implementation. Construct all hopping links in the recovered graph, not on a supplied coordinate adjacency. The finite Hermitian Wilson operator has a gapped sign, yields Ginsparg–Wilson relation to numerical precision (<1e-12), and its overlap index is:

| Q | index for Wilson m=1 | index for m=2.5 |
|---:|---:|---:|
| -1 | +1 | -1 |
| 0 | 0 | 0 |
| +1 | -1 | +1 |

This is standard overlap physics on an **order-recovered regulator graph**. It strengthens the previous 1D circle result, but does **not** derive a chiral interaction: the underlying two-layer causet was generated from a torus, and the gauge connection, **flux orientation**, gamma matrices, mass branch and Euclidean 2D Dirac rule remain supplied. It is also not a genuine Lorentzian 2+1 sprinkling or a four-dimensional chiral Standard Model.

**Dependency unlocked:** instead of choosing local 2D adjacency by hand, infer it from a causet; then test candidate dynamical rules on it. The unsolved keystone is **why a specific oriented flux, regulator branch and chiral matter content arise from the causal dynamics**. The numerical index cannot answer that without circular reasoning.

Sources: Tsilioukas, *Topology change and the Gauss–Bonnet term in causal set theory* (2026), https://arxiv.org/abs/2611.06102 ; original causal topology implementation https://github.com/stelios-tsilioukas/topology-change-in-causal-set-theory ; existing repo overlap code `analysis/toe_20261105_overlap_flux_chirality_index.py` (standard lattice result, not claimed novel).

### II. Gauge action AND matter together: a center-blind pure action acquires a center-sensitive expectation

A positive-transfer family `S_lambda=(1-cos phi)-lambda(1-cos phi)^2/2`, lambda in [0,1], from the previous pass has the same leading weak-field curvature. At lambda=1 it is the **center-blind adjoint SU(2) action**; a pure-glue Haar integral gives `<W_fund>=<cos phi>=0` exactly by phi↔pi-phi.

Now integrate an **inserted fundamental fermion loop** with positive one-dimensional Wilson-chain determinant

    D_b(U) = det[b I_2 - U] = b² - 2 b cos phi + 1,    b>1.

Weighted expectation over the SU(2) Haar measure is exactly

    <W>_with matter = [(b²+1)<W>_pure -2b<W²>_pure]
                       / [(b²+1)-2b<W>_pure].

For the adjoint endpoint this reduces to

    <W>_adj+fund = -[2b/(b²+1)] <cos² phi>_pure_adj,

which is **nonzero and negative** for finite b, despite the pure adjoint action remaining center-invariant. At bare beta=2: with b=2 the result is ~-0.256105, and with b=1000 it is ~-0.000640. Thus heavy matter decouples and center sensitivity fades. These are exact SU(2) Haar quadratures, with no experimental fitting.

**Physical connection:** global representations and matter can constrain which line operators are physical, and their determinants can break the pure-gauge center selection rule. But **this does not uniquely select the microscopic gauge action**, since various bare lambda still pass simple positivity criteria. An adjoint bare gauge action is not in itself an argument forbidding fundamental fermions when the underlying gauge group is SU(2).

Prior art: center symmetry is explicitly broken by dynamical fundamental quarks in lattice QCD; e.g. https://doi.org/10.1103/PhysRevD.103.014513 and https://www.scholarpedia.org/article/Lattice_gauge_theories . This is a newly tested cross-sector calculation within W33, **not a new confinement mechanism**.

### III. The photon must include the *operational reference budget*: two copies activate a Bell test

One delocalized single photon `(|1_A0_B>+|0_A1_B>)/sqrt2` is formally mode-entangled but cannot violate CHSH using **strictly local number-conserving operations** with no external phase reference. The two-copy state has an SSR-twirled decomposition into local A number sectors:

    Pr(n_A=0,1,2)=(1/4, 1/2, 1/4).

In the one-photon-per-party sector there is a two-mode Bell state; in the other two sectors there are local product states. Construct explicit local dichotomic block-diagonal observables with Pauli X,Z actions in the one-particle sector, +1 in both other sectors. Every local observable commutes with the local number operator. The total **unconditional** CHSH value is exactly

    S = (1/2)·2sqrt2 + (1/2)·2 = 1+sqrt2 = 2.414213562373...

No local particle-number SSR is violated, and no detection events have been discarded. This is a known *two-copy activation* mechanism, not original quantum theory. Independent published two-copy linear-optical experiments/theory also obtain `1+sqrt2` without postselection: https://doi.org/10.1088/1367-2630/18/4/043036 (Dasenbrook et al 2016); general SSR-Bell discussion https://www.nature.com/articles/s41598-018-20034-8 and https://doi.org/10.1103/PhysRevA.82.042116 .

**New-to-repo operational loss budget:** If each photon independently survives with probability eta and all vacuum/single-photon/loss outcomes are retained, these **fixed local observables** give

    S(eta) = 2 - 4 eta + (3+sqrt2) eta².

The fixed-setting Bell violation occurs only above

    eta > 4/(3+sqrt2) ≈ 0.90616.

This is **not an optimized efficiency threshold**, nor a loophole-free experimental guarantee: preparation, dark counts, independent settings, reference synchronization and mode-resolved detectors matter. It is a falsifiable engineering resource accounting that any proposed universal single-photon quantum computer should supply, rather than declaring a graph capable of BQP with no resource model.

### IV. Genuine unlabeled-history correction: Burnside enumeration does not remove the entropic problem

Earlier tests summed **labeled** three-layer causal configurations. A natural objection is that physically unlabeled causal sets should be divided by relabeling symmetry. Here we test that objection with a finite **marked-layer incidence** family of populations (2,4,2), M=2×4+4×2=16 possible adjacent-layer links. The layer-preserving group is

    G = S2 × S4 × S2,    |G|=96.

Using Burnside's lemma with the *cycle action on all 16 link positions*, calculate the exact polynomial in link count z over **unweighted orbits**:

    P_orbit(z) = (1/96) sum_{g in G} product_{cycles c of g} (1+z^{|c|}).

Its coefficients are (degree 0..16):

    [1,2,8,18,50,86,152,190,226,190,152,86,50,18,8,2,1].

Therefore there are precisely **1,240** inequivalent marked-layer incidence patterns at N=8, compared with 2^16=65,536 labeled patterns. This is not the number of all unlabeled 8-element causal sets, as the layer structure is retained.

For the **groupoid weight** (one factor 1/|Aut(config)| per orbit) rather than one unit per orbit, orbit–stabilizer gives the exact distinct quantity

    sum_orbits [z^{#links}/|Aut|] = (1+z)^16/96.

At z=exp(2.5 i) the unweighted orbit amplitude is ~3.6615+8.1914i whereas the groupoid-weighted amplitude is ~2.66×10^-6+5.95×10^-6i. Thus automorphism weighting is a **physical path-measure choice**, not an inconsequential notation change.

For N divisible by four, labeled configurations are 2^(N²/4). The layer-permutation group has order (N/4)!² (N/2)!; any orbit has at most that many labeled members. Hence the number of orbits obeys

    #orbits >= 2^(N²/4) / [(N/4)!² (N/2)!].

At N=64 this lower bound is approximately **10^246**. Quotienting the labels by exp[O(N log N)] does not remove the exp[O(N²)] nonmanifoldlike entropy. A physical **oscillatory/decoherence measure that suppresses those sectors relative to manifoldlike histories** remains necessary.

Prior work has already demonstrated oscillatory suppression of certain badly behaved causal-set classes with nontrivial actions: https://doi.org/10.1088/1361-6382/acc50c . Our Burnside calculation does not refute that possibility, nor construct real 4D gravitational dynamics.

### V. Anomalies are constraints, but the *flavor interaction graph* determines whether exotic charge freedoms survive

Work with the familiar supplied three-generation SM multiplets, one neutral Higgs in the shifted family symmetry, and add three right-handed neutrinos. Let the family-dependent Abelian shift be

    X=(p,q,-p-q) on the three left lepton doublets,
    X=-X_i on e_i^c and nu_i^c,
    X=0 on quarks and Higgs.

The full local mixed/cubic/gravitational anomalies vanish symbolically for **all** p,q if three nu^c are included. Without nu^c, the generic cubic anomaly is (for `y=6Y`)

    A_U1³ = -648 p q(p+q),

which vanishes on particular axes (such as L_mu-L_tau) but not on the entire two-dimensional p,q plane.

Requiring a renormalizable **off-diagonal charged-lepton Yukawa** with only the given Higgs joins flavors i,j and demands X_i=X_j. Represent permitted flavor couplings as an undirected graph: its incidence linear constraints have rank corresponding to the number of connected components. For three generations with sum X_i=0:

- no interfamily edges: two arbitrary family-charge parameters survive;
- one interfamily edge: one arbitrary parameter survives;
- any connected spanning tree of **two** interfamily edges: no family-difference parameter survives.

For the specific X=L_mu-L_tau with charges (0,+1,-1), an unbroken one-Higgs dimension-five Weinberg Majorana mass operator `L_i L_j H H` permits only `(e,e)` and `(mu,tau)`. Its mass texture has no e–mu or e–tau entries, so nontrivial observed electron-neutrino mixing requires additional flavor breaking, a different origin of mixing, or an extended particle sector. That is a model-building bottleneck, **not** a proof that observed PMNS mixing requires off-diagonal charged-lepton Yukawas; it can originate in the neutrino sector.

Prior art: lepton flavor symmetries and neutrino mass textures are studied in https://doi.org/10.1103/PhysRevX.14.031033 and https://link.springer.com/article/10.1007/JHEP03%282020%29001 . Our rank test makes the dependency explicit: **the physical interaction connectivity**, not anomalies by themselves, may collapse an apparently continuous charge freedom.

## VI. Extra cross-sector gate: symmetry quotient, quantum twirl, and invariant projection differ

Burnside history counting and the photon-number SSR are both questions about symmetry actions. But **classical orbit quotienting, quantum density twirling and projection onto gauge-invariant vectors are three different operations**. Their distinction matters for any fundamental quantum history measure.

Consider two labeled histories |a>, |b> exchanged by a Z2 unitary U. Three normalized positive density matrices have the same classical probabilities Pr(a)=Pr(b)=1/2:
- symmetric pure state rho+ = |+><+|, where |+>=(|a>+|b>)/sqrt(2);
- antisymmetric pure state rho- = |-><-|, where |->=(|a>-|b>)/sqrt(2);
- incoherent mixture rho_mix=I/2.

All three are invariant under conjugation by U, so the quantum twirl T(rho)=(rho+U rho U-dagger)/2 leaves them untouched. But projection onto invariant *vectors*, P=(I+U)/2, has surviving traces Tr(P rho P) equal respectively to **1, 0, 1/2**. The antisymmetric density operator is invariant even though the underlying vector carries the sign representation.

Their unnormalized coherent-sum weights (1,1) rho (1,1)^T are **2, 0, 1** respectively. Thus two quantum models having identical labeled classical configuration probabilities can have entirely different interference when histories are coarse-grained. These are not automatically normalized path-integral probabilities.

The antisymmetric labeled amplitude assignment (+1,-1) does **not** descend to a single-valued scalar amplitude on the unlabeled orbit: choosing a different representative flips the sign. Before quotienting causet histories, a TOE must specify the allowed quantum representation of the relabeling group, any twisted local systems or boundary charges, and the actual positive normalized quantum measure. A U1 local-number superselection rule constrains allowed operations and coherences but is not identical to identifying classical histories or projecting all vectors onto a trivial gauge representation.

This is a standard finite group-representation distinction made into a concrete cross-sector falsifier, **not** a new quantum-gravity anomaly, a Born-rule derivation or a TOE. The new executable checks contain 12 independent tests:

    python analysis/toe_20261119_quantum_quotient_twirling_vs_projection.py
    python -m pytest -q tests/test_toe_20261119_quantum_quotient_twirling_vs_projection.py

JSON: data/toe_20261119_quantum_symmetry_orbit_coherence_extra.json. The five original gates plus this sixth passed **55 focused tests** on the connected workstation. The final **41-module** November 19 physics regression passed **620 tests in 111.08 seconds** on the Windows machine, and both producer scripts independently regenerated their JSON certificates successfully.

## Cross-connection: what single missing ingredient could unlock several fronts?

The strongest lesson of these five gates is a *dependency ordering* rather than a claim of unique emergence:

1. **Extract stable topology and local adjacency from a causal incidence algebra.** Done in two synthetic dimensions, conditional on an inserted background and thickening scale.
2. **Derive oriented local Clifford/Dirac transport and nonabelian representations** rather than supplying them. **Still missing.** On a 2D torus we can calculate a chiral index only after assigning flux and a Wilson branch. This is the first major dynamical bottleneck.
3. **Integrate dynamical matter before declaring a gauge-center sector forbidden.** A fundamental determinant breaks the center-even pure-gauge expectation; the matter content and mass determine its strength.
4. **Specify quantum operational resources and the state.** Two-copy photons violate CHSH under the local SSR, but fixed settings need >90% photon survival in this simple loss model. Graph universality alone does not establish physical BQP feasibility.
5. **Specify a fully gauge- and automorphism-consistent quantum-history measure and flavor interaction graph.** Naive unlabeled counting still leaves enormous nonmanifoldlike history entropy, while connected interactions can remove family charge degeneracies. Neither the gravitational action nor Yukawa graph is derived yet.

A promising candidate architecture is **one oriented causal spin/gauge transport operator whose determinant supplies sector weights, flavor constraints and corrections to the quantum-history measure**. This is a research hypothesis—not a proven master law. Its first hard falsifier is a genuinely intrinsic Lorentzian 3+1 operator with the correct index and local continuum scattering, not just a copied 2D lattice regulator.

## Reproduction and scientific firewall

The Python implementation and regression tests are maintained under `analysis/` and `tests/`; JSON data certificates include independent GF2 ranks, 2D overlap indices/Ginsparg–Wilson errors, SU2 Haar integrals, SSR valid CHSH and loss checks, exact Burnside orbit counts, and symbolic anomaly/graph ranks.

Run:

    python analysis/toe_20261119_five_linked_torus_center_SSR_histories_flavor.py
    python -m pytest -q tests/test_toe_20261119_five_linked_torus_center_SSR_histories_flavor.py

**What is NOT achieved:** no recovered physical 3+1 Lorentzian Einstein gravity; no derivation of the Born rule; no SM gauge/matter spectrum or chirality from the causal relations; no measured constants; no complete TOE. Every claimed advance above is a finite constructive benchmark or a conditional no-go with clear scope.

## Five best independent next moves

1. **Construct orientation and Lorentzian spin transport from actual 3+1 causal topology.** Recover a dynamical vierbein/Clifford structure and satisfy microcausality, index/anomaly and CPT constraints without importing the continuum operator.
2. **Close the center-sensitive dynamical gauge theory.** Add full fermion determinant, physical line-operator compatibility and gauge RG; test whether the previously continuous bare lambda family acquires a unique physical continuum theory.
3. **Quantify universal photonic resources.** Optimize Bell and elementary gate witnesses under number SSR, photon loss, finite reference modes and heralding; demand polynomial scaling before claiming single-photon BQP.
4. **Derive the quantum measure over truly unlabelled causal histories.** Combine automorphism weighting, oscillatory amplitudes, reflection positivity/unitary evolution, and explicit manifoldlike comparators; recover two gravitational polarizations instead of just tiny complex sums.
5. **Derive real lepton flavor connectivity and charges.** Obtain nonzero physical Yukawa and Majorana mass textures from the same spin/gauge topology; compare PMNS, neutral neutrinos, anomaly cancellation and charged-lepton flavor constraints with experiment.