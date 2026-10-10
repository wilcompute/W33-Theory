# W33 Theory — Round 29: verified cat-layer hook firewall, graph-cover distance growth, E7 subgroup obstructions, finite-AdS chronology, C8 readout comparison

Date: 9 October 2026
Repo: wilcompute/W33-Theory, `master`.

## Scope and prior art

Executed the independent next steps from Round28: (1) correct qutrit hook errors, (2) pursue growing-distance W33-derived codes, (3) investigate exceptional E8 restrictions, (4) test Lorentzian causal emergence, (5) refine the eight-site experiment. Read incoming parallel Passes 11826–11833 before proposing any new physics. That work already established the exact finite-quadric 40 contexts/45 splits/36 Kramers classes, the observer-specific SL(2,9) stabilizer, 81 tangent vectors, the 20-null-vector cone and Brouwer–Haemers SRG(81,20,1,6). It expressly does not derive physical spacetime or Einstein's equations. The Z6-II flavour paper reports another failed Standard-Model Yukawa route. These are prior, parallel findings, NOT first discovered here.

Earlier Round26 established [[160,1,8]]_3 with 79 Gauss and 80 Wilson checks. Round27 gave an ideal Pauli decoder and bounded-distance all-q code existence theorem. Round28 implemented noisy sequential 956-SUM circuit (159 ancillas; hook errors), high-rate but fixed-distance HGP, E8 exceptional branching dimension screens, raw W33 wave no-go, and phase-referenced C8 numerical spectroscopy. They are starting points, not new claims below.

## Front I. Exhaustive transversal data-coupling / Shor-style cat-state hook certificate

Use the exact 80 weight-eight Wilson Z rows and 79 weight-four Gauss X rows of the native W33 code, 956 data-coupling positions per syndrome round. Enumerate all 80 nonidentity two-qutrit Pauli exponent combinations after **each** of those data-SUM gates: **76,480 single-fault locations/channels**. Propagate the Pauli frame exactly through subsequent sequential controlled qutrit SUM gates. With a shared ancilla per check, a single after-gate two-qutrit Pauli may leave **eight** data errors (one direct plus seven propagated from the ancilla); an ancilla-only fault has up to seven propagated on an eight-link Wilson check and up to three on a four-link Gauss check.

Replace *only the data-coupling layer* by a transversal Shor/GHZ-cat construction: one separate entangled ancilla per participating data link, with no ancilla interacting with more than one data link. A single two-qutrit fault **during data coupling** then touches at most ONE data link. This is an exact locality statement, independent of Pauli exponent, but consumes 956 ancillas per extraction round instead of 159 and requires a correctly prepared and verified eight-/four-qutrit cat resource.

**Crucial limitation:** cat-state PREPARATION and verification are not simulated or proved fault-tolerant. One bad cat preparation can correlate ancillas; there is no completed multi-round detector model, leakage calculation or threshold. Thus we have a mathematically checked hook-propagation repair *conditional on verified cat states*, not a final fault-tolerant hardware circuit. Comparisons with earlier 13/160 sequential failures at p=0.0001 cannot be converted into a cat logical failure probability without those missing faults.

Reproducer: `analysis/w33_20261009_toe29_cat_hook_certificate.py`. Prior literature shows why cat verification and flags are nontrivial: https://github.com/qBraid/Fault-Tolerant-Syndrome-Extraction and https://quantum-journal.org/papers/q-2025-01-30-1618/ .

## Front II. Strictly W33-derived COVER codes: nonzero rate AND unbounded distance, but noncanonical and logarithmic at best

The W33 Levi base graph G has V=80 vertices, E=160 edges, is simple connected 4-regular and has girth 8. Its fundamental group is a nonabelian free group of rank E−V+1=81. Standard residual finiteness of a free group implies that, for any prescribed L, there exists a finite-index NORMAL subgroup of pi1(G) containing none of the nontrivial conjugated reduced closed-walk words shorter than L. The associated finite connected regular graph cover G_L -> G has girth >=L. This proof is an existence statement and supplies neither small explicit covers nor a canonical PSp4(3)-equivariant quotient.

Every degree-m connected cover has V_m=80m vertices and E_m=160m edges. Its ternary vertex–edge incidence check H_m, with a redundant row removed, has size (80m−1)×(160m), full row rank, classical code ker H_m distance = girth(G_m). Using the ordinary odd-characteristic HGP checks (critical minus sign in Z part), the quantum code has exact

    [[ (160m)^2+(80m−1)^2, (80m+1)^2, girth(G_m) ]]_3.

A HGP lower bound supplies d>=girth, and a simple nontrivial graph-cycle tensored with a nonbridge edge supplies a logical witness of that weight, so equality holds. The rate tends to 1/5. Both X and Z HGP check weights are bounded by 6, because every covering graph remains 4-regular.

Hence **some W33-derived (noncanonical) finite-cover HGP family has simultaneously positive rate and UNBOUNDED distance**. But by the degree-4 Moore bound girth cannot grow faster than O(log number of covering graph vertices), giving at most O(log physical code length) distance. This is NOT a family with linear distance or asymptotically good relative distance, and no efficient cover selection, syndrome decoder, physical interactions or noise threshold was found.

Finite experiment: random cyclic voltage covers of degrees 1,2,3,5,7,11 (three seeded samples each) all retained girth exactly eight. This negative sample emphasizes that arbitrary small covers do not deliver the abstract existence theorem's improvement.

Reproducer: `analysis/w33_20261009_toe29_cover_hgp_growth.py`. HGP reference: https://arxiv.org/abs/0903.0566 . General code distance/threshold context: https://doi.org/10.1103/prxquantum.2.040101 .

## Front III. E8 exceptional branch search: three new E7-chain NO-GO classes, not fabricated subgroup embeddings

Round28 narrowed any candidate Steinberg-81 constituent inside E8's E7xA1 branch to the **E7 adjoint 133**, since the simple group PSp4(3) cannot have a nontrivial projective two-dimensional A1 factor representation and the E7xA1 adjoint decomposes as 133+56+56+1+1+1. Test three standard maximal-rank subgroup families *within* E7:

1. E7 -> E6 x U1: 133=78+27+27bar+1, 56=27+27bar+1+1. All the G-invariant blocks in the FULL E8 adjoint have dimension at most **78**, so an irreducible Steinberg-81 cannot occur.
2. E7 -> SL8: 133=sl8(63)+Λ4(C8)(70), 56=Λ2(C8)(28)+dual(28). Max invariant block **70**. This excludes an E8 Steinberg81 irrespective of how PSp acts via SL8, even if the 8-dimensional carrier representation is irreducible.
3. E7 -> SO12 x SL2: 133=(66,1)+(1,3)+(32,2), 56=(32prime,1)+(12,2). The PSp SL2 projection must be trivial; split (32,2) into 32+32 and (12,2) into12+12. Max G-invariant block **66**. Steinberg81 cannot occur.

All three full E8 branching tests reproduce 248 total dimensions and all blocks are <81; complex Maschke semisimplicity proves the no-go statements. This does not classify PSp4(3) embeddings in all E7, F4xG2, Spin16 or E8, and does not compute a character restriction for an actual surviving embedded finite subgroup. **The user-requested full explicit exceptional embedding remains open.** The new result is to exclude three broad subgroup chains with exact branching, preserving the valuable remaining search space.

Reproducer: `analysis/w33_20261009_toe29_e7_branch_obstructions.py`. External E7 branching reference: https://cds.cern.ch/record/1282603/files/JHEP11.083.pdf and https://ncatlab.org/nlab/show/E%E2%82%87 .

## Front IV. Respect parallel finite-AdS4 breakthroughs; exact obstruction to emergent global chronological time

Incoming Pass11831–11833 reconstructs a 5D F3 Clifford bivector quadric from two qutrits: 40 null contexts, 45 square factorisations, 36 nonsquare Kramers reversals. Choosing a Kramers reversal leaves an 81-element 4-dimensional F3 tangent module with 20 nonzero null vectors, stabilizer isomorphic in the manuscript to SL2(F9), and light-cone Cayley graph SRG(81,20,1,6) = Brouwer–Haemers.

This pass independently reconstructs the 81 tangent matrices from the native Pass11831 Clifford representation **without enumerating its group**, recovers 1+20+30+30 quadratic-type census, adjacency spectrum `20^1 + 2^60 + (-7)^20`, graph diameter2, and exact normalized Laplacian spectrum `0^1 + 0.9^60 + 1.35^20`. Consequently the heat trace is

    H(t)=[1+60 exp(-0.9t)+20 exp(-1.35t)]/81.

The effective spectral dimension is transient (e.g. ~3.504 at t=2, ~4.682 at t=4, ->0 as t->infinity), not a sustained 3+1D continuum. The projective finite Lorentz geometry is mathematically rich, but its 'light cone' is an **undirected finite graph of diameter two**.

**Chronology theorem:** No finite additive group V=(F3)^4 admits a nontrivial, translation-invariant STRICT causal partial order. If 0 precedes v≠0, translation invariance and transitivity imply 0 < v < 2v < 3v =0, contradicting irreflexivity. Hence no orientation of the native symmetric null set produces a globally translation-invariant, unbounded future. Real chronological physics requires an additional nonperiodic clock/cover, broken translation invariance or dynamical causal organization. The finite causal skeleton alone does not define an Einstein spacetime, a physical metric, energy or c.

This proof is new to this pass; **the finite AdS4/Kramers/Lorentz/Brouwer-Haemers dictionary itself belongs to the parallel Pass11831–11833 work**.

Reproducer: `analysis/w33_20261009_toe29_ads_causality.py`. Previous parallel writeup: `analysis/PASS11831_11833_FINITE_ADS4_OF_TWO_QUTRITS.md`.

## Front V. C8 prototype experimental alternatives and competing geometry fingerprint

Round28 supplied 601 delay points x two complex IQ quadratures x8192 shots = **9,846,784 synthetic samples** for a hypothetical 60us, T2=100us, t/h=5MHz, U/t=32 experiment; not a built device. Here compute a **conditional direct frequency-scan spectroscopy** alternative with a genuinely independently addressable two-boson transition:

- 361 points spanning −0.9 to +0.9 MHz, step 0.005MHz, 8192 binomial shots each = **2,957,312 shots** (~30.0% of the prior IQ plan).
- Assume ideal Lorentzian line response and width set by T2=100us; the seeded synthetic frequency-scan finds five C8 peaks at approximately -0.620,-0.440,0,+0.440,+0.625 MHz in a rotating frame, maximum discrepancy ≈0.00197MHz from exact model centers.
- Independently compare the graph `Q_3` eight-vertex cube, 12 links, with native C8 ring, eight links, through FULL 36D two-boson Hamiltonian diagonalization. Native C8 has bound doublon multiplicities `[1,2,2,2,1]` (five bands); cube Q3 has `[1,3,3,1]` (four bands). Calibrated link tomography should already distinguish connectivity, and the spectrum provides a physics cross-check.

**Critical feasibility condition:** nothing yet demonstrates the device supplies a pair-selective coherent transition with the assumed Lorentzian response and signal contrast. The 30% synthetic shot ratio excludes device reset/measurement overheads and does not establish less physical experiment time. The actual option remains to arrange hardware operations with a laboratory collaborator, not to infer a complete 80-site machine from spectral numerology.

Reproducer: `analysis/w33_20261009_toe29_c8_spectroscopy_comparator.py`.

## Bottom line, acceptance tests, next discriminators

Five research producers and five frozen JSON certificates; `tests/test_w33_20261009_toe29_five_fronts.py` crosschecks the old/new geometric representations and all calculations. The strongest constructive outcome is a mathematical **positive-rate, unbounded-distance W33 Levi-cover/HGP existence theorem**, albeit only logarithmic distance in block size and dependent on arbitrary noncanonical covering choices. The strongest physics conclusion is a precise, independent **finite chronology obstruction** completing the parallel finite-AdS4 kinematic picture: the finite cone does not itself give a time-oriented physical spacetime. The cat hook firewall and direct spectroscopy are preliminary design validations, **not physical experiments or universal fault-tolerance proofs**.

No Standard Model mass/coupling derivation, full E8 embedded matter operator, Lorentzian 3+1D continuum, Einstein equation, physical c, complete fault-tolerance threshold, or fabricated hardware is claimed.
