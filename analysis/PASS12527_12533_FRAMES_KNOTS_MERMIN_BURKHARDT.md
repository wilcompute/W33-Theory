# Passes 12527–12533: orthonormal frames, knots, tricolourings, parafermions, Mermin squares and the Burkhardt quartic

Claude track. Producer: `analysis/w33_pass12527_to_12533_frames_knots_burkhardt.py`. Test: `tests/test_w33_pass12527_to_12533.py`. Drivers in `analysis/search_drivers_12466`: `frame_orbits.py`, `verify_frame_set.py`, `frame_family.py`, `knots_w33.py`, `knots_overlap.py`,
`mermin_even.py`, `burkhardt_totals.py`, `tomography_subset.py`, `tomography_orbits.py`, `hyperoval_dfs.c`, `export_dfs.py`, `recheck_highs.py`, `highs_control_q9.py`, `heavy_highs.py`, `fox_w33.py`, `fox_general_p.py`, `parafermion_w33.py`, `kauffman_golden.py`, `magic_colour.py`, `tl_module_even_weil.py`, `colour_patterns.py`. Continues `PASS12518_12525_HYPEROVAL_FLOOR_HESSE_DICTIONARY.md`.

Labels: **[E]** exact computation or proof, **[N]** numerical with a stated tolerance, **[I]** interpretation. Nothing here derives particles, forces or constants.

## 12527: q = 5 is an orthonormal frame, and q = 13 has an even set of 160 lines

Work in Q(4,q) as Σ xᵢ² = 0, dual to W(3,q). The monomial group 2⁴:S₅ stabilises the frame.

**[E] q = 5.** Since 1² + 2² = 0 over F₅, the Hamming-weight-2 singular points number 2·C(5,2) = 20, in 10 pairs, and they meet every singular line in 0 or 2. By the uniqueness of 12525 this is the minimal set. That explains the W(D₅) stabiliser of 12525 and its block system of 10 pairs: **the minimal set of W(3,5) is the weight-2 shell of an orthonormal frame.**

**[E] q = 13.** The orbit of (0, 1, 1, 1, t) with t² = −3 has 5 · 4 · 8 = **160** points, and it is an even set. `verify_frame_set.py` carries it by the Klein correspondence into the separately built W(3,13) and re-checks there: 160 lines, every point on 0, 2 or 4 of them (1340, 960, 80 points). Pass 12482's best was 168. It is **not a hyperoval**, and 160 is only an upper bound on the minimum.

**[E] Other q** (`frame_orbits.py`; the minimum over unions of orbits of a monomial subgroup, with 2⁴:C₅, D₅, F₂₀, A₅, S₅, A₄, S₄):

| q | frame minimum | best known | beats it? |
|---|---|---|---|
| 3 | 20 | 10 | no |
| 5 | **20** | 20 (exact) | equals |
| 7 | 60 | 40 (exact) | no |
| 9 | 80 | 48 (exact) | no |
| 11 | 112 | 84 | no |
| 13 | **160** | 168 | **yes** |
| 17 | 320 | 288 | no |
| 19 | 560 | none recorded | |
| 23 | 640 | none recorded | |

`frame_family.py` scanned the monomial orbits that are themselves even, for primes to 23, and found some at each. There is no formula yet, and q = 13's improvement is a single data point. So frames are the right object at q = 5 and useful at q = 13, and **they are not the general "double-six" object I was looking for**: they miss the minima at q = 3, 7, 9.

## 12528: W(3,3) is the mod-3 homology of a genus-2 surface, and Jones at e^{iπ/3} reads it

**Classical ingredients, not mine.** Birman–Hilden: B₆ acts on a genus-2 surface as its double branched cover, by Dehn twists along a chain a₁…a₅ with a₁ + a₃ + a₅ = 0 in homology. Lickorish–Millett: |V_L(e^{iπ/3})| = √3^{dim H₁(M_L; F₃)} for M_L the double branched cover. Dunfield–Thurston: H₁ of a Heegaard splitting is V/⟨J, φJ⟩ for a Lagrangian J. Corpus: `lickorish` and `dehn twist` have 0 hits, and Pass 11869 has W(3,3) as a level-3 structure on a genus-2 modulus. As far as I can find, what follows is the join with the TL₆ two-qutrit braid rep.

**[E]** δ = √3 is exactly t = e^{iπ/3}, and p₀, p₂, p₄ commute pairwise, so they lie on one W(3,3) line L₀: this is the mod-3 shadow of a₁ + a₃ + a₅ = 0, and L₀ is the Lagrangian killed by plat caps.

> **Theorem (from the classical ingredients; 220/220 tested).** For β ∈ B₆ with plat closure L: |V_L(e^{iπ/3})| = √3^d, with d = dim(L₀ ∩ βL₀), which is 2, 1, 0 when L₀ and βL₀ share 4, 1, 0 points.

The bracket comes from an independent state sum with no W(3,3) input. The control of replacing L₀ by another line disagrees 88–137 times out of 220.

**[N] The amplitude itself** (`knots_overlap.py`, 160/160, worst error 6 × 10⁻¹²). With |cap⟩ the joint eigenstate of p₀, p₂, p₄:

> **⟨plat closure⟩ = 3 ⟨cap| U_β |cap⟩**, as a complex identity.

So at this root the Jones polynomial of a 3-bridge link is three times a two-qutrit stabiliser overlap, and the relative position of two lines is the rank-3 relation of W(3,3). This is why it is easy to compute at this root, by the same route as Gottesman–Knill.

**Prediction [E].** Long random words equidistribute on the rank-3 relation, so random 3-bridge closures have dim H₁(M; F₃) = 0, 1, 2 with probability 27/40, 12/40, 1/40. Observed over 20,000 words of length 60: 0.6754, 0.2995, 0.0250. The transvection walk mixes on the group, so this checks the action rather than a topological fact about knots.

**Standard closure.** dim coker(ψ(β) − I) over F₃ with reduced Burau at t = −1 agrees with the state sum on 90/90 for n = 3 and 5, but only 43/90 for n = 4 and 76/90 for n = 6. *Suspected cause, unverified:* the factor 1 + t + … + t^{n−1} vanishes at t = −1 for even n. Odd n only is established.

**Known knots.** Trefoil 1, figure-eight 0, connected sum of two trefoils 2, T(3,5) 0 (Poincaré sphere), Hopf 0 (RP³), unknot 0. My first "expected" value for Hopf was wrong.

**Open reading [I].** Lines of W(3,3) behave as mod-3 handlebodies, and disjoint lines as mod-3 homology spheres. A codeword's crown graph then reads as 10 handlebodies with 5 pairs giving F₃-homology spheres. I have not looked for a topological meaning of evenness.

## 12529: Mermin–Peres squares

**[E] q = 2.** The 6-line minimal even sets (10 of them) are the Mermin–Peres squares, and the exact linear system over F₂ agrees: **a word is contextual iff |S| ≡ 2 mod 4**, on all 31 nonzero words (6 and 10 contextual, 8 not). A single context is noncontextual, as it must be.

**[E] q = 4,** by field reduction to 4 qubits: one line and two meeting lines are noncontextual (controls). All 35 basis words sampled are contextual, including 8 of weight 10. But greedy reduction finds irreducible contextual cores as small as 6 lines with 9 meetings, in 2 of 6 trials, which **looks like** an embedded 3 × 3 square. So contextuality at q = 4 is **not specific to even sets**, and I am not claiming that minimal even sets are minimal parity proofs. q = 8 was not classified.

Odd q has no such obstruction, as symmetric Weyl operators multiply without phase on commuting pairs (cf. Gross). That is the known reason, not tested here. So "even set" is the shape of a parity proof, but it only carries a sign in characteristic 2.

## 12530: the 216 codewords are coordinates on the Burkhardt quartic

**Classical, rebuilt here.** The Burkhardt quartic has 45 nodes, 40 Jacobi planes with 9 nodes each in Hesse configuration, and 40 Steiner hyperplanes containing 18 nodes and splitting into 4 planes, with symmetry PSp(4,3), and G₃₃ is the reflection group. In P⁵ it is σ₁ = σ₄ = 0 in six coordinates. All of that comes from the literature.

**The construction** (`burkhardt_totals.py`). For a sentinel H ∪ H⊥, Π_H = ⅓ Σ_{x∈H} D_x is the parity on one tensor factor. On the 5-dim even Weil sector it is a reflection, and its mirror v_H is a product of the two factors' odd states. **[N]**, tolerance 10⁻⁸ or better throughout:

- |⟨v, v′⟩| = 0 for disjoint sentinels and ½ otherwise, and the 45 reflections have **exactly one** quartic invariant F.
- F is singular at all 45 v_H (gradient ≤ 10⁻¹⁵, control at a random point 0.2).
- A point of W(3,3) ↦ the span of its 9 sentinels, rank 3, on which F vanishes: **Jacobi planes**. So the Hesse dictionary of 12521 is the classical Hesse configuration on a Jacobi plane.
- A line ↦ the span of its 4 planes, rank 4, containing 18 nodes, on which F is the product of those 4 planes (spread 3 × 10⁻¹³): **Steiner hyperplanes**.

**The new statement.** For all 216 totals, the five mirrors have rank 5 and can be rephased to Gram matrix (I + J)/2, i.e. **an A₅ root star** e₀ − eᵢ. They generate a reflection group of order 720, with 15 mirrors, and there are 36 distinct such subsystems. A control of 3000 other pairwise non-orthogonal 5-sets has rank 3, 4 or 5 and Gram determinant 0 or 1/16, against 3/16 here. And:

> **Under vᵢ ↦ e₀ − eᵢ, F becomes const · σ₄ on σ₁ = 0, for all 216 totals (spread 10⁻¹³).**

So **a minimal even line set of W(3,3) = a six-coordinate S₆-symmetric presentation of the Burkhardt quartic + one distinguished coordinate**, and 216 = 36 × 6 counts these. I did not find this stated, but I have not read Burkhardt or Hunt in full, so it may well be classical.

## 12531: subsets of the simplex frame

**Negative, within what was tried.** Rank 24 needs k ≥ 6 double-sixes in my samples (58 of 1500 at k = 6; none at k = 5, though the lower bound is only ⌈24/5⌉ = 5). No subset tested is tight on E₂ or detects exactly the collinear triples by cubic moment: 600 subsets per k for k up to 12 (all of them for k = 1, the first 600 for k = 2, 3, random otherwise), and every proper union of orbits of the stabilisers of a point, a line, a spread and a codeword. So the 36 simplices do not obviously reduce the other track's measurement count, by this route. This is not a theorem about all subsets.

## 12532: second solvers

- **HiGHS** (`recheck_highs.py`), an unrelated MILP solver: q = 3 and 5 reproduced; **q = 7, W = 38: all 24 star classes infeasible, 0 unknown (726 s); q = 9, W = 46: all 511 infeasible, 0 unknown (607 s).** Control: class 24380's optimum is exactly 48, proved in 1.6 s. The LP relaxation is trivial (11 in every class sampled), so this is not a Farkas certificate.
- **Heavy cases with HiGHS** (`heavy_highs.py`, same case list): q = 3, 5 reproduced, and **q = 7, W = 38: all 34 infeasible**. q = 9 and q = 7, W = 40 are reported under `heavy_status`.
- **`hyperoval_dfs.c`,** a from-scratch exhaustive search with no solver code, reproduces q = 3 and 5 **including the exact solution counts** (1 and 5). At q = 7 it finished no case in hours, so I stopped it. A Mantel-based pruning bound I added did not change node counts at q = 5. It is sound and it does not help.
- **CaDiCaL** also stalled at q = 7.

So the hyperoval floors at q = 7 and q = 9 now rest on **two unrelated solvers**. Neither produces a checked proof certificate.

## 12533: W(3,3) points are Fox tricolourings of 6 points, and Z₃ parafermion monomials

This is the most elementary reading of 12528, and it needs no topology.

**Classical ingredients.** Przytycki: the number of Fox tricolourings of a link is 3|V(e^{iπ/3})|². Fradkin–Kadanoff: Z₃ parafermions, αᵢαⱼ = ωαⱼαᵢ for i < j. Hutter–Loss: parafermion braiding generates the qudit Clifford group and is not universal. Corpus: `tricolo`, `przytycki` and `fox color` have 0 hits, and `parafermion` has one, a May audit marking this as not computed.

**[E] The dictionary** (`fox_w33.py`). Colour 6 strands by F₃. The crossing rule (a, b) → (b, 2b − a) preserves constants and the alternating sum, so it acts on

> V = {c ∈ F₃⁶ : Σ(−1)ⁱcᵢ = 0} / ⟨(1,…,1)⟩, of dimension 4.

On V: the rule is a B₆ representation with a **unique invariant alternating form up to scale**, which is non-degenerate, and each σᵢ is a transvection. A linear similitude V → F₃⁴ intertwines all five generators with the W(3,3) transvections T_{pᵢ}, with the same sign. The colourings with c₁ = c₂, c₃ = c₄, c₅ = c₆ map exactly onto the line L₀ of 12528.

**The closed form (`parafermion_w33.py`).** With uᵢ = (−1)ⁱcᵢ,

> ω(c, c′) = Σ_{i<j} (uᵢu′ⱼ − uⱼu′ᵢ),

which is Fox-invariant with constants in its radical. This is the commutation rule of six parafermions. **[N]** With explicit Fradkin–Kadanoff matrices on 27 dims: gᵢgⱼ = ω^e gⱼgᵢ for i < j with one constant e; zero-charge monomials M_c = Π gᵢ^{uᵢ} commute with the total charge Q; commutators match the closed form; the constant colouring is a scalar on each 9-dim charge sector, so **"mod constants" is "fixed total charge"**; and the 81 classes are unitary and trace-orthonormal on a sector, a two-qutrit Pauli group.

**The triangle [N].** The TL₆ generator Rᵢ = A + (√3/A)Πᵢ, with Πᵢ any eigenprojector of the neighbouring bilinear M(aᵢ), acts on monomials by the Fox rule (the inverse convention; the same mirror issue as Cui–Wang in 12520), for all 5 generators and all 3 eigenprojector choices. The Πᵢ satisfy TL. So:

> **SU(2)₄ braid generators = Z₃ parafermion exchanges = Fox tricolouring moves, and W(3,3) points = colourings = Pauli operators.**

Since the caps are L₀ and constants are always colourings, this proves the count directly: a colouring of a plat closure is a boundary colouring extending over both caps, so **#colourings = 3^(1 + dim(L₀ ∩ βL₀))**, with no Birman–Hilden or Lickorish–Millett needed. Through Przytycki this recovers |V| = √3^d. Tested on the diagram by independent arc linear algebra: 150/150 at 6 strands, and colourings versus Jones 60/60 at each of 2, 4, 8 strands.

**[E] Other primes** (`fox_general_p.py`, p = 3, 5, 7, 11). The form is invariant and non-degenerate, the caps are isotropic, and #p-colourings = p^(1 + dim(L₀ ∩ βL₀)) on 120/120 words at each p. A control Lagrangian disagrees 41–54 times. So W(3,p) is the Fox p-colouring space of 6 points for each odd prime. The Jones link is special to p = 3, since at p = 5 the analogue would involve the Kauffman polynomial (Jones, Rong), which I did not test.

**Honest scope.** The ingredients are classical, and this may be folklore among people who work on these invariants. I did not find it stated, and the join to W(3,3) and its 216 codewords is what is added. It is Clifford-only: braiding here is classically simulable and **not universal**. Nothing here shows that W(3,3) describes physical anyons.

## 12537: the same space, three more ways

**[N] p = 5 and the golden ratio** (`kauffman_golden.py`). The Brandt–Lickorish–Millett–Ho polynomial Q, by its skein relation on descending diagrams with no colouring input. **|Q((√5 − 1)/2)| = √5^r with r from Fox 5-colourings, 150/150**, and **Q(−1) = (−3)^s with s from Fox 3-colourings, 150/150**. These are classical theorems (Jones, Rong, Lickorish–Millett), used here as a check that links W(3,5) to the golden-ratio evaluation as W(3,3) is linked to Jones at e^{iπ/3}. I first recalled the F₃ formula at x = 1. The trefoil refutes that, and I corrected the point rather than the data.

**[N] Where the Clifford picture stops** (`magic_colour.py`). Parity is colour negation on one factor. Its unitary is Clifford, but measuring it is not: the odd sector of a qutrit is (|1⟩ − |2⟩)/√2, with Wigner function −1/3 at one point and ⅙ at the other eight, sum-negativity ⅓, the "strange state" of Veitch et al. Its 9 Weyl images have overlap ¼: it is the Hesse SIC fiducial of 12521. All 12 stabiliser states have W ≥ 0 (control), and a stabiliser state that is not a parity eigenstate reaches it with probability ½. So **one parity measurement leaves the stabiliser polytope**, and braiding alone cannot. I did not show that this resource is enough for universality here; for qutrits that is what magic-state distillation results suggest.

**[N] The TL₆ vacuum module is the even Weil sector** (`tl_module_even_weil.py`). The module generated from the cap has dimension 5 = C₃ and is invariant under all braid generators. **Exactly one of the 81 displaced parities acts as +1 on it**, it commutes with all TL projectors, and its +1 eigenspace has dimension 5. So the module is the C⁵ of the Burkhardt quartic of 12530: the knot, parafermion and Burkhardt threads live on one space.

**[E] Colour patterns: mostly negative** (`colour_patterns.py`). The 40 points by colour-class sizes: (3,2,1) 18, (4,2) 9, (4,1,1) 6, (2,2,2) 6, (3,3) 1. Codeword profiles over these types show no simple rule, which is expected, since colour-class type is not braid-invariant. Only 6 of the 36 parity-preserving strand permutations preserve commutation. Of the 6 bipartite matchings of the strands, **exactly the 5 non-crossing ones are lines**, the TL basis, and 2 codewords contain all 5. I did not establish what those 2 codewords mean.

## Heavy runs, and the q = 9 theorem

CP-SAT's chain was stopped after 2 of 42 cases in hours. HiGHS (`heavy_highs.py`, same case list, positive control via q = 3, 5): **q = 9, W = 46: all 42 infeasible (3108 s). q = 9, W = 48: all 42 infeasible (4434 s).** So:

> **The minimum even line set of W(3,9) has 48 lines, on two solvers for each half, and every minimal even set is a hyperoval, in a single orbit of 3,586,680 sets.**

The uniqueness half combines HiGHS (no heavy set at W = 48) with CP-SAT (one star class at W = 48). No proof certificate exists. q = 7, W = 40 is still running, so the same statement for q = 7 covers hyperovals only; status under `heavy_status`.

## Sources

- J. S. Birman, H. M. Hilden, on isotopies of homeomorphisms of Riemann surfaces, Ann. Math. 97 (1973).
- W. B. R. Lickorish, K. C. Millett, *Some evaluations of link polynomials*, Comment. Math. Helv. 61 (1986).
- N. M. Dunfield, W. P. Thurston, *Finite covers of random 3-manifolds*, Invent. Math. 166 (2006), arXiv:math/0502567.
- Jost, Lewark, *Signs of knot polynomial evaluations from a topological perspective*, arXiv:2601.16588.
- J. H. Przytycki, *3-coloring and other elementary invariants of knots*, Banach Center Publ. 42 (1998).
- A. Hutter, D. Loss, *Quantum computing with parafermions*, Phys. Rev. B 93 (2016), arXiv:1511.02704.
- E. Fradkin, L. P. Kadanoff, Nucl. Phys. B 170 (1980).
- V. Veitch, S. A. H. Mousavian, D. Gottesman, J. Emerson, *The resource theory of stabilizer quantum computation*, New J. Phys. 16 (2014).
- Burkhardt quartic: arXiv:2308.15271; B. Hunt, *The geometry of some special arithmetic quotients*, not read in full.
- Corpus: Pass 11869; Pass 12507–12526; `2026-11-02_route_minimum_cubic_tomography.md`.
