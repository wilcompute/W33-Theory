# TOE Round 24 — the E6 tritangent frame weld, finite quantum response and protection gates

**9 October 2026.** Executed five separate directions inherited from Round23 on `wilcompute/W33-Theory`. All producer scripts, certificates and tests are explicitly scoped to `toe24` to preserve other agents' local work.

## Evidence provenance

Existing, previously established facts: the 81-dimensional complex irreducible W33 Steinberg representation (BT1688 and Pass 2026-09-01); the integral 81-cycle Levi isometry (Round20); Schläfli's 27-object SRG(27,10,1,5) and the 45 E6 tritangents reconstructed internally (Pass4659); the **45 protected 16-line supports and their PSp-equivariant tritangent mapping** (Pass4585, Pass4616, Pass4659); 1,620 apartments and their symplectic frames (Pass4474); 81 apartments through each selected chamber form the cycle basis (BT744); full two-boson and three-boson Bose-Hubbard spectra (Round22/23); the 45×36 connected-component census under exactly-three-ray frame hopping (Round23); and the standard E8 gradings (Pass11681 and prior art).

We distinguish these known results from the *new tested bridges/obstructions below*. Mathematical correspondences do not themselves provide a mechanism for gravity or a Standard Model action.

## 1. The genuine E8 intertwiner: a precise representation-theoretic obstruction

The W33 integral Levi cycle representation `St81` is an *irreducible* nontrivial 81-dimensional complex PSp(4,3) representation. Its space of invariant vectors is zero. The repository's E6 27-line carrier, in contrast, is a transitive 27-object PSp-set, so its 27-dimensional permutation representation `Perm27` contains a constant invariant vector.

The PSp-invariant meeting graph on that set has exact spectrum

`A_Schlaefli: 10^1, 1^20, (-5)^6`,

obtained from parameters `(27,10,1,5)`. These eigenspaces are nontrivial proper invariant subspaces of the permutation representation. Taking the **naive** E6×A2 matter 81 as `Perm27 tensor C3_trivial` yields **three** constant invariant vectors, whereas `St81` has none. Therefore

`Hom_{PSp(4,3)}(St81, Perm27 tensor C3_trivial) = 0.`

This is a decisive **NO** to the naive request that the 27-line permutation basis, copied three times with no nontrivial A2 action, is the W33 Steinberg-81. There is **no equivariant intertwiner for this specified candidate**. Equal dimension `81=27×3` and the successful 45 tritangent G-set bridge do not give a representation equivalence.

**Boundary:** We have *not* proved an obstruction for all possible E8 embeddings, nontrivial/projective factor actions, mixed brackets or non-permutation realizations of the E6 27. The actual E8-(E6×A2)-81 matter mapping remains open, and we do not claim otherwise.

Reproducer: `analysis/w33_20261009_toe24_e8_representation_obstruction.py`.

## 2. Strong exact identification: the 45 dynamically disconnected sectors ARE the existing protected E6 tritangents

Round23 discovered the graph on all **1,620 W33 point-C4 apartments** with an edge whenever two apartments share exactly three of their four point rays. It is 8-regular and has exactly **45 disconnected 36-apartment components**.

The prior work of Pass4585/4616/4659 reconstructed a different-looking `45 protected supports ↔ 45 E6 tritangents`, using four-**line** apartments. Direct comparison of point labels to line labels is WRONG because these are dual carriers and their point/line enumeration differs.

Here we construct an actual coordinate-independent comparison:
1. Map each of the 1,620 point C4 apartments to its **unique four-line Levi lift**: its four adjacent point pairs determine four totally isotropic GQ lines. This maps the 1,620 point apartments bijectively to the prior 1,620 dual four-line apartments.
2. For each dual apartment `a`, recover Pass4659's binary reduced XOR fiber label `f(a)=min(⊕_{L∈a} Astar_column(L), complement)`.
3. Important count correction: there are **135 distinct XOR labels**, each with **12** apartments, *not 45 labels with 36 each*. The **union of the four line indices within those 12 apartments** is one 16-line protected support. Exactly **three XOR labels share each protected support**, giving **45 supports × 36 apartments**.
4. Compare all 45 membership lists *as exact sets of original apartment indices*. They match **all 45 connected components**, not merely their size distributions. All component supports have 16 lines.

Thus the explicitly chosen one-ray-change Hamiltonian `H=-t A_overlap3` realizes the PREVIOUSLY PROVEN protected 45-object E6-tritangent G-set **as exactly its dynamically disconnected sectors**. From the prior equivariant dictionary the component setwise PSp stabilizer is order `25920/45=576`; this 576 is not inferred from number coincidence alone.

This is a real new dynamical-to-established-geometric bridge. But it does **not** produce physically protected superselection sectors: the previously computed, also-symmetry-invariant two-ray-change hopping `-epsilon A_overlap2` couples different components and for any epsilon>0 restores a unique positive symmetric ground state.

Reproducer: `analysis/w33_20261009_toe24_apartment_tritangent_fiber.py`.

## 3. Collective quantum selection: actual finite-N source susceptibilities

On the native 80-site W33 incidence lattice use the explicit attractive Bose-Hubbard Hamiltonian at N=2 and N=3,

`H=-t ∑_(ij edge)(b_i†b_j+h.c.)-U∑_i n_i(n_i-1)/2-h n_0`,

with t=1. Diagonalize the complete N=2 Hilbert space **3,240** and N=3 Hilbert space **88,560** in a small pinning field `h=±0.001`, and independently compare density finite differences with energy curvature:

`chi_0=[<n0>_(+h)-<n0>_(-h)]/(2h)`,
`chi_0= -d²E0/dh².`

For two bosons, computed source susceptibilities at `U/t=0,3,8,16,32` are approximately

`0.01677, 0.01878, 0.12803, 0.27111, 0.53825`.

For three bosons at `U/t=0,4,8`:

`0.02515, 0.75058, 3.20318`.

The independently computed curvature agrees to finite-step tolerance. Attraction causes a large enhancement in the response to a symmetry-breaking source, but at **exactly h=0** the finite-connected stoquastic graph has a unique PSp-invariant ground state for every finite boson number. Its local occupation is `N/80`.

These response numbers do not establish a phase transition. A true spontaneous selector requires a specified system-size/occupancy sequence and a noncommuting order of limits `lim_(h→0)lim_(size→∞)`; finite W33 by itself does not define that thermodynamic limit.

Reproducer: `analysis/w33_20261009_toe24_quantum_order_parameter_susceptibility.py`.

## 4. The 1- and 3-logical-qutrit partial-flatness codes have distance EXACTLY ONE

Round23 used the native 160-link qutrit Gauss/Wilson CSS stabilizers with vertex Gauss X rank79 and selected 8-cycle Wilson Z constraints:

- Avoid all eight-cycles touching a specified incidence edge: 1,539 chosen Wilson loops, rank80, **one** logical qutrit.
- Avoid all eight-cycles touching a specified vertex: 1,458 chosen loops, rank78, **three** logical qutrits.

These logical counts were already established. The new gate is to look for a *physical-weight-one nontrivial logical Pauli*. For the edge-avoidance code, **X on that excluded edge** commutes with all chosen Wilson loops (none contains that edge) and all vertex Gauss X checks. It is not an X stabilizer: an edge basis vector is not a vertex cut, since that edge belongs to an 8-cycle and is not a graph bridge. Therefore **distance d=1 exactly**.

For the vertex-avoidance code, the **four incident link X's** similarly commute with all chosen Wilson loops. Their signed product is the single vertex Gauss stabilizer, leaving **three independent weight-one logical X's**; thus its code distance is also **d=1**.

A local perturbation `-h(X_e+X†_e)` acts WITHIN the encoded ground subspace at first order; an affected logical qutrit splits as `-2h,+h,+h` with gap `3|h|`. Neither code is fault-tolerant or topologically protected. Even perfect commuting Wilson and Gauss stabilizer checks do not cure this failure.

Reproducer: `analysis/w33_20261009_toe24_css_distance_firewall.py`.

## 5. Experimental falsification protocol: FIVE W33 doublon bands and explicit noise tolerance

In a synthetic bosonic W33 Levi graph with **80 sites and 160 hopping links**, the Round23 strong-attraction N=2 pair effective Hamiltonian is

`H_eff=-U I-(t²/U)(8I+2A_Levi)+O(t^4/U^3)`.

Since the exact adjacency eigenvalues are `4, sqrt6, 0, -sqrt6, -4` with multiplicities `1,24,30,24,1`, the **five bound-pair bands relative to the lowest band** have *parameter-independent* frequencies in units of `(2t²/U)(4-sqrt6)`:

`0, 1, 4/(4-sqrt6) ≈ 2.579796, (4+sqrt6)/(4-sqrt6) ≈ 4.159592, 8/(4-sqrt6) ≈ 5.159592.`

A localized two-boson doublon prepared on any single native incidence vertex has EXACT integrated band projector weights

`(1,24,30,24,1)/80`.

Proof: PSp is transitive on the 40 points and separately on the 40 lines. Because the Levi adjacency is bipartite, each nonzero ±singular-value eigenspace has exactly half its projector trace on each of the two 40-vertex halves; the zero eigenspace has two equally dimensional 15D kernels. Hence each spectral projector diagonal is uniformly rank/80 on BOTH types. The source explicitly checks all 80 projector diagonals to 1e-11; no point–line swapping automorphism is assumed. This is stronger than a ratio alone: measure a **five-band return/interferometric spectrum with those spectral weights**, not just two gaps.

Protocol: build or simulate an 80-node synthetic lattice realizing exactly the point-line Levi edges; calibrate single-boson hopping t; prepare a local bound pair; scan pair return/coincidence against delay and Fourier-transform; resolve band centers, integrated weights, widths, and dependence on calibrated U/t; extrapolate toward large U/t. Reject the particular Hamiltonian model if observed five bands or normalized frequency/weight fingerprints disagree beyond independently calibrated corrections.

Quantified noise: 50 seeded on-site disorder trials at each normalized disorder amplitude 0,0.01,0.03,0.05,0.1 were simulated on the exact 80×80 effective pair matrix. For disorder amplitude ±0.05 in *adjacency eigenvalue units*, the maximal simulated deviation of the second/first band-center ratio from 2.579796 was **below 1e-4**. An independent conservative Weyl perturbation bound is around 0.247, so the random-sample precision must NEVER be presented as a worst-case guarantee. Real hardware additionally suffers photon/boson loss, inhomogeneous links, finite-U leakage, readout calibration and dephasing.

**No physical realization has been built or measured.** This is a falsification plan for a specific engineered-graph Bose-Hubbard Hamiltonian, not a falsification protocol for the fundamental Standard Model or general relativity.

Reproducer: `analysis/w33_20261009_toe24_pair_spectroscopy_protocol.py`.

## Final physical boundary

These five investigations deliver two necessary representation/coding **obstructions**, one **exact dynamical-to-E6 G-set identification**, an independently checked **source-field quantum susceptibility**, and an **experimentally testable simulator-specific spectrum**. They do not establish E8 interaction compatibility for the true 81 matter representation, spontaneous quantum vacuum selection, protected topological quantum storage, Lorentzian 3+1D spacetime, physical mass scales, or a Theory of Everything.

Companion tests `tests/test_w33_20261009_toe24_five_fronts.py` and five machine-readable `data/w33_20261009_toe24_*.json` certificates reproduce and audit each result. Prior E6 and Hodge work is credited explicitly, never relabeled as new.
