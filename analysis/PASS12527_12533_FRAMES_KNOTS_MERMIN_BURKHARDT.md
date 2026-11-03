# Passes 12527–12533: orthonormal frames, knots, Mermin squares and the Burkhardt quartic

Claude track. Producer: `analysis/w33_pass12527_to_12533_frames_knots_burkhardt.py`. Test: `tests/test_w33_pass12527_to_12533.py`. Drivers in `analysis/search_drivers_12466`: `frame_orbits.py`, `verify_frame_set.py`, `frame_family.py`, `knots_w33.py`, `knots_overlap.py`,
`mermin_even.py`, `burkhardt_totals.py`, `tomography_subset.py`, `tomography_orbits.py`, `hyperoval_dfs.c`, `export_dfs.py`, `recheck_highs.py`. Continues `PASS12518_12525_HYPEROVAL_FLOOR_HESSE_DICTIONARY.md`.

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

- **HiGHS** (`recheck_highs.py`) reproduces the star verdicts at q = 3 and 5.
- **`hyperoval_dfs.c`,** a from-scratch exhaustive search with no solver code, reproduces them too, **including the exact solution counts** (1 at q = 3, 5 at q = 5). At q = 7 it had not finished a case in the time I gave it, so that is still open; status under `second_solver`.
- A Mantel-based pruning bound I added made no difference to node counts at q = 5. It is sound and it does not help.

**So q = 7 and q = 9 still rest on CP-SAT alone**, except for the solver-free orbit count at q = 7.

## Heavy runs

The non-hyperoval case at q = 9, W = 48 and q = 7, W = 40 is still open; status under `heavy_status` in the 12518 producer. Each case at q = 9 is taking over 20 minutes, so uniqueness among *all* minimal sets is not settled.

## Sources

- J. S. Birman, H. M. Hilden, on isotopies of homeomorphisms of Riemann surfaces, Ann. Math. 97 (1973).
- W. B. R. Lickorish, K. C. Millett, *Some evaluations of link polynomials*, Comment. Math. Helv. 61 (1986).
- N. M. Dunfield, W. P. Thurston, *Finite covers of random 3-manifolds*, Invent. Math. 166 (2006), arXiv:math/0502567.
- Jost, Lewark, *Signs of knot polynomial evaluations from a topological perspective*, arXiv:2601.16588.
- Burkhardt quartic: arXiv:2308.15271; B. Hunt, *The geometry of some special arithmetic quotients*, not read in full.
- Corpus: Pass 11869; Pass 12507–12526; `2026-11-02_route_minimum_cubic_tomography.md`.
