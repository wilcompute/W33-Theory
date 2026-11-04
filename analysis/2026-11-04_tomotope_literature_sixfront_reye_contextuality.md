# The tomotope: primary-paper audit, Reye bridge, six TOE falsification fronts, and Peres contextuality

**Date:** November 4, 2026 UTC. **Scope:** exact finite geometry, independent integer-algebra witnesses, numerical closed-system toy Hamiltonians, selected close reading of older repository material and external papers. **Not:** a discovered quantum computer, an observed contextuality experiment, a derived E6 vacuum, four-dimensional spacetime, nonlinear Einstein gravity, or an experimentally calibrated photon circuit.

## Provenance and reproducible artifacts

Producers:
- analysis/toe_20261104_tomotope_reye_flux_invariants.py
- analysis/toe_20261104_tomotope_fivefront_controls.py
- analysis/toe_20261104_reye_peres_critical_ks.py

Data:
- data/toe_20261104_tomotope_reye_flux_invariants.json
- data/toe_20261104_tomotope_fivefront_controls.json
- data/toe_20261104_reye_peres_critical_ks.json

Tests: tests/test_toe_20261104_tomotope_sixfronts.py; tests/test_toe_20261104_reye_peres_ks.py.

**Primary original:** Barry Monson, Daniel Pellicer and Gordon Williams, *The tomotope*, Ars Mathematica Contemporanea **5** (2012), 355–370, DOI https://doi.org/10.26493/1855-3974.189.e64 . Read the group action in sections 3–4, minimal regular covers and Theorem 5.9 in section 5, medial Reye embedding and incidence in section 6.

**Subsequent or related literature checked:**
- Monson, Pellicer, Williams, *Mixing and monodromy of abstract polytopes*, Trans. Amer. Math. Soc. **366** (2014), 2651–2681, https://doi.org/10.1090/S0002-9947-2013-05954-5 . Public abstract and bibliographic information checked. The AMS full text was not accessible in this run, so no unverified claims about internal theorems.
- Gabe Cunningham, Mark Mixer, Gordon Williams, *Reflexible Covers of Prisms*, Contributions to Discrete Mathematics **19** (2024): the unique-minimal-regular-cover result for prisms of polyhedra contrasts with the tomotope's nonunique case.
- Brigitte and Herman Servatius, *The generalized Reye configuration*, Ars Math. Contemp. **3** (2010), https://doi.org/10.26493/1855-3974.108.423 . **Important:** classical Reye (12_4,16_3) must not be mistaken for the generalized (20_3,15_4).
- Monson and Weiss, *Medial layer graphs of equivelar 4-polytopes* (2007), https://doi.org/10.1016/j.ejc.2005.10.001 .
- P. K. Aravind, *How Reye's configuration helps in proving the Bell-Kochen-Specker theorem: a curious geometrical tale*, Foundations of Physics Letters **13** (2000), 499–519, https://users.wpi.edu/~paravind/Publications/REYE.pdf . Full published ray coordinate table and proof in sections IV–VI reviewed.
- P. K. Aravind, *Quantum Kaleidoscopes and Bell's theorem* (2005/2006), https://arxiv.org/abs/quant-ph/0508130 , public abstract consulted: 15-observable, 24-state and 60-state kaleidoscopes, ten interlinked Reye configurations plus duals for 60-state apparatus, 1120 apparitions. That construction is **pre-existing**, not a novel W33 claim.

### Repo archaeology and explicit claim correction

Local git grep over current analysis/papers/tests/docs found 824 paths mentioning *tomotope*; git log --all by commit subject found 259 historical matches. Neither count means 824 semantic discoveries. Selected older actual code read:
- analysis/bt831_tomotope_minimal_cover_architecture.py (published cover arithmetic and ambiguity).
- analysis/bt1363_q4_clock_tomotope_medial_descent.py (antipodal Q4 edge/face classes, Reye medial data, clock).
- analysis/w33_pass5309_hoffman_tomotope_degree12_action.py (W(D4)/Z order96, published generators via explicit conjugator).
- analysis/w33_pass5310_tesseract_rotation_d4_tomotope_doublecovers.py (two nonisomorphic order192 covers with same quotient).
- analysis/w33_pass5488_5491_the_tomotope_is_inside_w33_twice.py (two copies of the Reye configuration in W33 12+16 incidence and Aut576).
- analysis/w33_pass5492_5495_the_tomotope_is_the_q3_member_of_a_family.py (larger W(3,q) tactical-configurations; parameters alone are not identification).
- analysis/w33_pass5643_5650_the_tomotope_w33_bridge_is_wf4_mod_centre.py (W(F4)/center 576 Reye graph automorphism; corrected false W(F4) 16-face graph claim).
- analysis/w33_pass1376_tomotope_published_generators.g (the published group generators are present and already tested; **historical introductory comment incorrectly says Gamma(T) fails the string C-group intersection condition and that the tomotope is not an abstract polytope**).

**Correction of last older comment:** The tomotope is an **abstract uniform rank-four polytope** with a non-string Wythoff action by Gamma(T). Its **monodromy group** is an sggi of type {3,12,4} but fails the string C-group intersection property. These are different groups. Gamma(T) is order96, Mon(T) order18432, and R2's automorphism group order36864. The literature explicitly separates them.

**Prior-art firewall:** Order96/192, Q4 antipodal-Reye, Aut576, W(D4)/Z and full tomotope covers are **known in the paper and repo**. New here is the independent graph-spectral/flux/metric-graph/cross-C3-equivariance *check*, not credit for establishing the older geometry.

## Exact re-creation of the original rank-two medial geometry

The paper's section 6 encodes twelve tomotope edges by pairs (X,+/-) with X any two-element subset of J={1,2,3,4}, and sixteen triangular faces by ordered pairs (a,-b) in J x J. Incidence:
- minus: a in X and b in X;
- plus: a in X and b not in X.

The 12 x 16 integer incidence B has four entries per edge and three per triangle; total 48 incidences. Connected Levi bipartite graph V=28,E=48 has first Betti E-V+1=**21**, girth **6**, and every incidence link lies in exactly six shortest 6-cycles.

Independent construction from Q4: 32 cube edges/24 square faces, quotient by antipodal translation x↦x xor1111 gives sixteen edge classes and twelve face classes with 48 incidences. NetworkX graph-isomorphism verifies the two colored bipartite graphs.

**Exact Gram polynomial** by SymPy:

    det(z I - B B^T) = z² (z-4)^9 (z-12).

So rank(B)=10, rank A_bipartite=20 and adjacency spectrum

    {-2sqrt(3) (1), -2 (9), 0 (8), 2 (9), 2sqrt(3) (1)}.

The Reye graph has 28 vertices, not the abstract tomotope's 4 vertices. The 48 medial incidence flags become **192 full tomotope flags by a fourfold refinement**, but no single color-preserving Reye graph symmetry is automatically a full rank-four tomotope automorphism.

## Symmetry selection: Gamma96, extra Reye576, and a new no-go for a direct C3 map

The published four involutions r0,r1,r2,r3 on twelve edge labels generate Gamma(T) order96 with derived subgroup48. They implement a forked Wythoff diagram, not a string Coxeter C-group presentation. Independently, Q4's even signed coordinate symmetry W(D4) of order192 acts on antipodal classes with center kernel2; the induced action is order96. The published and induced degree-12 actions have the same verified element-order histogram; the explicit conjugating map between these specific labels is NOT reproduced in this producer, although Pass5309 already supplies one.

The full **colored Reye incidence graph** has 576 automorphisms via explicit graph isomorphism enumeration: a factor six larger than Gamma(T). Do not mistake those extra 480 graph symmetries for abstract tomotope automorphisms.

Gamma(T) acts transitively on each set of 12 edge classes, 16 triangle classes and 48 medial incidences. A representative order-three element has four triples on 12 edge classes; **one singleton plus five triples** on sixteen triangle classes; sixteen triples on forty-eight medial incidences. The 32 nonidentity order-three elements in Gamma96 have **zero fixed points on the 48 medial incidences**.

In contrast the explicitly chosen symplectic C3 transvection in the W33 160-flag Levi graph fixes **16** of 160 flags. Any total C3-equivariant map 160 W33 flags →48 medial incidences would send fixed flags to fixed flags, an impossibility for a target carrying any nonidentity order-three Gamma96 action. **Theorem (specified actions): no such total intertwiner exists.** The theorem does not preclude maps using larger covers/fibers, different actions, set-valued maps or a different direction. No direct 3-generation choice exists invariant under full Gamma96 because its action on sixteen triangles is transitive. Selected C3 produces five interchangeable triples rather than a physically unique three-family selection.

## Dimension: actual biregular metric-graph finite-size law, not Lorentzian 4D

Subdivide all forty-eight incidence edges into L equal graph segments. The 28-vertex Reye graph has degrees four and three on the two bipartition sides. Write lambda=2(1-cos theta). At interior vertices eliminate chain amplitudes. The first small positive eigenvalue satisfies the exact secular equation

    [4 cos(Ltheta)+2 tan(theta/2)sin(Ltheta)]
    *[3 cos(Ltheta)+tan(theta/2)sin(Ltheta)] = 4.

Set alpha=acos(1/sqrt(3)); alpha²≈0.912629840864. Then asymptotically

    L² lambda1(L)=alpha²[1+5/(12L)+O(L^-2)].

Verified with direct sparse Laplacian eigenvalues at L=1,2,4,8 and high-precision scalar root L through 128; at L=128 the rescaled value is ≈0.91560517. Betti remains 21; continuum remains a **one-dimensional metric graph**. "Rank four" of an abstract incidence polytope, "four coordinates" of a two-qubit Hilbert ray, and "4D spacetime" are different concepts.

## Gravity: the correct reduced cycle rank is 21; no native ADM closure from the medial graph

The signed 28x48 node-edge incidence D has rank27 and a 48x21 fundamental integer cycle basis C with rank21, DC=0. Every edge appears in the chosen basis support. The earlier candidate positive local constraints, interpreted as zero,

    h_i=(c_i.x)^2/2 + sum_{e in supp(ci)} p_e²/2,

have only p=0, x=D^T phi as the simultaneous zero set, thus one gauge orbit. This no-go applies only to **these** positive quadratic constraints.

The source graph has cycle rank21 rather than the original W33 Levi graph's 81. A direct rank-preserving identity between entire H1 cycle sectors cannot exist without adding extra fibers, cover data, or higher-dimensional cells. This does not rule out proper action-derived gravity or a physically motivated higher lift.

## Hardware: signed flux changes flat zero-mode multiplicity and selects real Ramsey quadrature

Take real zero-onsite bipartite tight binding Hamiltonian H+ whose offdiagonal blocks are B and B^T. Flip sign of one incidence hopping to make Hpi. Its signed 12x16 incidence matrix has **rank11**, up from10, hence the bipartite Hamiltonian's zero-energy multiplicity drops from 8 to **6**. Its topological Betti number remains21; band zero modes are NOT homology generators.

At a vertex incident to the flipped link, exactly six shortest 6-cycles contain the link, yielding

    [(H+)^n - (Hpi)^n]ii =0 for n=0,1,...,5,
    [(H+)^6 - (Hpi)^6]ii =24.

Thus the diagonal time-return amplitude difference has leading real term

    [exp(-itH+)-exp(-itHpi)]ii = -t^6/30 + O(t^8).

The imaginary return quadrature vanishes **identically for every real t** since chiral bipartite Hamiltonians have zero odd diagonal moments. A triangle's imaginary t^3 flux witness is *not* portable unchanged to this geometry. The new measurement is a **real-quadrature coherent Ramsey** reference or matched return-population interference. Simulations t=0.2,0.4,0.8 in certificate; no Lindblad noise or hardware gates on the 28-site architecture were compiled.

## Cover ambiguity: physical observable selection is a separate problem

The paper proves infinitely many mutually incomparable minimal regular covers (Theorem 5.9). From its quotient family for odd k, previously tabulated in BT831:

    |Mon(Qk)| = 36864*k^6.

The arithmetic for k=3,5,7 is reproduced, **not a new group-theoretic proof**. A local 48-incidence /192-flag packet and a chosen global regular cover need different records. Gauge-invariant physical hypotheses would require either cover-independent observables or an explicit dynamical rule selecting a cover. The subsequent work *Mixing and monodromy* elaborates the general method; the 2024 prism paper provides a contrasting unique cover family.

## EXTRA: the Peres/Aravind Reye link gives a published two-qubit contextuality route

Aravind (2000) shows two Reye configurations of twelve rays each arising as projective images of dual 24-cells, making a set of **24 Peres rays in four-dimensional real Hilbert coordinates**. Exact Fig.2 integer vectors are reproduced in analysis/toe_20261104_reye_peres_critical_ks.py and tested independently. The 24 rays form **24 complete orthogonal tetrads**: 6 pure and18 mixed; every ray is orthogonal to nine others and belongs to four tetrads. A 0/1 noncontextual assignment with exactly one 1 per complete tetrad is impossible.

More strongly, integer rank-two line testing identifies **16 projective triples in each of the two Reye configurations**. Each first triple has a unique second triple consisting of rays orthogonal to all three rays of the first. Removing the matched six yields a **critical 18-ray parity proof**: exactly nine complete orthogonal tetrads, each of the eighteen rays appears exactly twice, giving the contradiction "9 one-marks, counted twice." For all **16** published configurations the producer independently checks nine tetrads, double occurrence, noncolorability and that deletion of any further ray restores colorability. These are specifically Aravind's **already published** Theorems 3–7 and Fig.12, not new KS constructions.

The follow-up *Quantum Kaleidoscopes and Bell's theorem* (arXiv:quant-ph/0508130) describes still broader Reye systems, ten interlinked configurations and their duals, 60 rays and 1120 apparitions; this is a literature roadmap, not independently recomputed in this run.

**The key new integration task** is not to rediscover the 24-ray proof but to find a **physically valid, preparation-and-measurement-preserving map** from the protected W33 code/photonic modes into these orthogonal tetrads. The proven direct C3 flag-map obstruction above narrows naive candidates. A Hilbert dimension of four for two qubits does NOT derive four physical spacetime dimensions, and KS contextuality is a finite nonclassicality constraint, not a TOE.

## Five independent next research gates

1. **Spacetime:** Generate a Lorentzian 4D simplicial metric and causal cones from dynamics, not from a chosen graph refinement, polytope rank or Hilbert dimension.
2. **Symmetry selection:** Construct an action selecting Gamma96/C3 representations and a cover-independent local Hamiltonian; explicitly overcome or respect the fixed-point obstruction when coupling W33 flags.
3. **Gravity:** Form an action-based discrete ADM/Regge system using actual 4-simplex incidence, check nonlinear first-class closure; don't confuse Reye H1=21 with W33 H1=81.
4. **Flavor and quantum information:** Test covariant embeddings of the Peres orthogonal tetrads into the W33 protected carrier, count genuine independent Yukawa/family selectors and preserve previous strong-CP constraints.
5. **Hardware:** Compile Reye's 28-mode real-quadrature flux protocol and the Peres 24-ray orthogonal measurement bases into device-native beam splitters, phases, losses, confidence budgets and contextuality inequalities.

**Status firewall:** Exact graph/representation/incidence/ray combinatorics, conditioned one-dimensional continuum laws and ideal toy flux simulations have passed. No physical spacetime, gravitational action, three-generation selection, measured contextuality or demonstrated universal photonic processor is claimed here.
