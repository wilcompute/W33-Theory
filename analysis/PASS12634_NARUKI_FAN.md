# Pass 12634: W(3,3) inside the tropical moduli space of cubic surfaces; the same 40 cusps as the Siegel level-3 moduli space

Claude track. Producer: `analysis/w33_pass12634_naruki_fan.py`, writing `data/w33_pass12634_naruki_fan.json`. Test: `tests/test_w33_pass12634.py`. All results are exact combinatorics on the E6 root system.

**Not a theory of everything.** This connects two moduli spaces the corpus already uses. It derives no physics.

## The object

The tropical moduli space of marked cubic surfaces, trop(Y⁰), is the *Naruki fan* (Ren, Shaw and Sturmfels, Adv. Math. 300 (2016), arXiv:1402.5651, building on Hacking, Keel and Tevelev):
- a 4-dimensional fan in R⁴⁰/R·1, from the valuations of the 40 Yoshida functions;
- f-vector (1, 76, 630, 1620, 1215);
- two ray types, (a) and (b);
- maximal cones: 135 of type aaaa and 1080 of type aaab.

Its cones are the combinatorial types of tropical (maximally degenerate) cubic surfaces. Computational geometry has nowhere appeared in the corpus beyond numerology (`PART_CCV_TROPICAL_BRIDGE.py` matches numbers only).

## Results (all checks pass, with controls)

1. **Reconstruction.** Take the type-(a) rays to be the 36 positive roots of E6 and the type-(b) rays to be the 40 A2×A2×A2 subsystems. Take the cones to be sets of mutually orthogonal roots, plus one A2³ subsystem with roots from distinct A2 factors. This reproduces the f-vector exactly, (76, 630, 1620, 1215), with 135 aaaa and 1080 aaab, and there are no orthogonal 5-sets. *This is a count match, not a cone-by-cone comparison with the paper's 40×36 matrix.*
2. **W(3,3) is the cusp structure of the fan.** Two A2³ subsystems share either no positive root (240 pairs) or exactly three (540).
   - The root-disjoint graph is **SRG(40,12,2,4)**, and its complement is SRG(40,27,18,18).
   - In fan terms: **two cusp rays are collinear iff their stars share no type-(a) ray.**
   - Control: a non-invariant relation on the same labels is not even strongly regular.
3. **It is the dual GQ: the 40 cusp rays are the 40 *lines* of W(3,3), i.e. the points of Q(4,3).**
   - The double perp of every non-collinear pair, |{x,y}^⊥⊥|, has size 2, so no point is regular.
   - In W(3,3) every point is regular and the size would be 4.
   - Controls built independently: W(3,3) from PG(3,3) with the symplectic form gives {4: 540}; Q(4,3) from the parabolic quadric gives {2: 540}. Both are SRG(40,12,2,4).
4. **Both maximal-cone types are corpus objects.**
   - aaab cones (1080) = a W(3,3) line (an A2³) × one root from each of its three A2 factors (40 × 27).
   - aaaa cones (135) = **45 D4 subsystems × 3 orthogonal frames** each (12 positive roots per D4). These are the corpus's "135 splits = 45 factorisations × 3" (Pass 12052).

## The bridge this makes

Pass 11899 found that the 40 zero-dimensional cusps of the Siegel level-3 genus-2 moduli space are the 40 lines of W(3,3), the maximal commuting two-qutrit Pauli sets. That space is the corpus's flavour modulus (Passes 11869–11883). **The 40 cusp rays of the tropical moduli space of cubic surfaces are the same 40 lines.**
- The cubic-surface moduli space is a 4-ball quotient over the Eisenstein integers (Allcock, Carlson and Toledo), and the Burkhardt quartic (A₂(3)) is related to a 3-ball quotient over the same ring (Hunt). Both are level-√−3 Eisenstein objects.
- The cusp match fits the classical picture, in which the cusps of the cubic-surface ball quotient are the isotropic points of a 5-dimensional quadratic space over F₃ = Z[ω]/(√−3), i.e. the points of Q(4,3).
- This pass realises that picture inside the tropical fan, where it becomes checkable combinatorics.

## Corrections to the corpus

- **Pass 84** (`2026-07-15_pass84_e6_w33_explicit_iso.md`) says "the 40 tritangent planes ↔ 40 isotropic points". A smooth cubic surface has **45** tritangent planes. The W(E6) orbit of size 40 (stabiliser of order 1296) is the set of A2³ subsystems, the 40 triads of Steiner trihedral pairs. They correspond to W(3,3) **lines**, not points. Pass 84's dictionary rows about "lines per tritangent plane" therefore do not hold as written.
- **BT810** lists "40 + 40 Steiner trihedra ↔ points / lines of W(3,3)". This pass pins the classical 40 Steiner triads (the A2³ subsystems) to the **lines**.

## Prior art and novelty

- The identification of the 40 A2³ subsystems with a 40-set acted on by PSp(4,3) is classical and is in the corpus (BT810; `w33_e6_120_steiner_trihedral_pairs.py`).
- The ball-quotient cusp picture is classical (Allcock, Carlson and Toledo).
- The Naruki fan is due to Naruki, Hacking, Keel, Tevelev, Ren, Shaw and Sturmfels.
- **New here:** the computational bridge (the f-vector reconstruction, the cusp-graph type decided against controls, aaaa = 45 D4 × 3) and its link to the corpus's Siegel cusps.
- I did not find the statement "collinear iff disjoint stars in the Naruki fan" in one web search plus the corpus. It may well be implicit in Hacking, Keel and Tevelev, so no novelty is claimed.

## Next

1. Compute the fan's actual rays from the 40×36 Yoshida matrix (Ren, Shaw and Sturmfels Thm 6.1 / Hacking, Keel and Tevelev) and compare cone by cone, upgrading the count match to an identity.
2. Do the same for the Burkhardt side: tropicalise A₂(3) (or its ball-quotient model) and test whether its cusp rays carry W(3,3)'s point graph or line graph.
3. Use the fan as a phase diagram: the 1080 + 135 maximal cones are the tropical limits of cubic surfaces. Ask whether the two-qutrit context labels (line × root triple) give a degeneration-indexed basis for the 27-dimensional representation.

## Addendum: the positive-geometry regions (E6 pezzotopes) are S5-pentads of W(3,3) lines (`w33_pezzotope_check.py`)

The real moduli space of marked cubic surfaces has 432 W(E6)-equivalent regions. Each is a simple 4-polytope, the **E6 pezzotope**, with f-vector (45, 90, 60, 15) and 15 facets: 10 of root (A1) type, which are associahedra, and 5 of A2³ type, which are cubes. Each region is a positive geometry in Arkani-Hamed's sense (Early, Geiger, Panizzut, Sturmfels and Yun, arXiv:2306.13604; Sturmfels and Telen, arXiv:2605.11909).

**Derived from the fan.**
- No cone contains two cusp rays, so the 5 cube facets are pairwise disjoint.
- Hence each cube meets 6 root facets, and each root facet meets 3 cubes and 6 roots.
- With S5 labels (cubes T₁…T₅, roots r_ab), r_ab lies in T_i iff i ∉ {a, b}.

**Search over all 5-sets of pairwise disjoint W(3,3) lines** (13,824 of them):
- **Exactly 432** satisfy "every three share exactly one positive root, and the 10 roots are distinct". That is the number of pezzotope regions.
- For **all 432**, the subfan of the reconstructed Naruki fan on those 15 rays has face numbers **[15, 60, 90, 45]**: the pezzotope's f-vector read in reverse.
- The root facets meet as the line graph of K5: r_ab ⊥ r_cd iff {a,b} ∩ {c,d} ≠ ∅, giving 30 adjacent pairs and 15 non-adjacent.

**W(3,3) reading.** A pezzotope is a pentad of pairwise disjoint W(3,3) lines (5 maximal commuting two-qutrit contexts) in which every three have a unique common root. In the finite-AdS₄ language of Pass 11831 (121 = 40 contexts + 45 splits + 36 Kramers), the root facets are 10 Kramers points.
- **None of the 432 pentads extends to a spread.** W(3,3) has 36 spreads, one per double-six (BT810). The pezzotope pentads are partial spreads that cannot be completed.
- So the positive-geometry regions of cubic-surface moduli are *not* built from the double-six/spread structure. They come from a separate S5 configuration, and 13,824 = 432 × 32.

**Status.** The face-number identity is a count match on every region. It is not yet a facet-by-facet identification with the paper's explicit regions. The identification of facets with roots and A2³ subsystems follows Early, Geiger, Panizzut, Sturmfels and Yun's labels (10 of type A1, 5 of type A2^×3). The W(3,3) reading and the "no spread" property are this pass's.

## Addendum 2: the E6 Bergman fan maps into the reconstructed fan (`w33_bergman_to_naruki.py`)

Ren, Shaw and Sturmfels: the rays of trop(Y⁰) are the images of the 750 rays of the E6 Bergman fan Berg(E6) under a 40×36 matrix.
- **The 750 rays are recomputed** as the proper connected flats of the E6 root arrangement: A1 36, A2 120, A3 270, A4 216, D4 45, A5 36, D5 27.
- **Map used:** the root / A2³ incidence matrix (M[T, r] = 1 iff r ∈ T), on the hypothesis that it is equivalent to the Yoshida map.

**All 750 images lie in the reconstructed Naruki fan** (non-negative least squares over its 1215 maximal cones, modulo R·1):
- A1 goes to its own type-(a) ray.
- **A2 goes to the type-(b) ray of its unique A2³, the W(3,3) line.**
- A3 goes to the interior of the 2-cone of two orthogonal roots, one-to-one with the 270 such cones.
- A4 and A5 go to type-(a) rays.
- D4 and D5 go to 0, the lineality direction.

The rays produced are exactly the 36 + 40. A random 0/1 matrix with 9 ones per row produces 750 distinct images instead (control).

**Status.** The image is *contained in* the reconstructed fan and produces exactly its rays. Not shown here: that the images of Bergman cones cover all 1215 maximal cones (that needs the 142,560 maximal nested sets), and that this incidence matrix equals the Yoshida matrix rather than merely being equivalent to it.

## Addendum 3: each pezzotope is a double-six with a synthematic total; the 432 regions double-cover the corpus's 216 codewords (`w33_pezzotope_gosset.py`)

The 27 lines of the cubic surface are built in the same E8 model: E8 roots of a fixed A2 class, projected to E6. Meeting pairs (135) and skew pairs (216) are told apart by the inner product. Against a pentad's 10 roots, the 27 lines **always split 12 + 15**. For **all 432** pentads:
1. **The 12 lines form a double-six.**
2. Each of those 12 lines pairs non-trivially with 5 roots r_ab, and these 5 duads form a **Hamiltonian 5-cycle of K5**. The 12 lines are the 12 Hamiltonian cycles.
3. **The two sixes are the two A5-orbits of 5-cycles.** The pentad's S5 is the exotic, transitive S5 inside S6, the structure behind S6's outer automorphism, and it swaps the two sixes.
4. Each of the other 15 lines sees a 4-cycle of K5 (missing vertex m, one of 3 four-cycles). Grouped by the missing vertex m, the 15 lines give 5 triples of duads of the six. **They are 5 synthemes forming a synthematic total**, and the m-th syntheme belongs to the m-th cube facet.
5. **The (double-six, total) pairs number exactly 216, each carried by exactly 2 pezzotopes:** 432 = 2 × 216, and each double-six carries 12 = 2 × 6.

**Reading.** The 432 positive-geometry regions of the moduli space of marked cubic surfaces (the E6 pezzotopes of Early, Geiger, Panizzut, Sturmfels and Yun) double-cover the 216 synthematic totals of the 36 double-sixes. Pass 12523 identified these with the corpus's **216 q = 9 even-set codewords**, which fibre over the Hesse SIC and MUB structure (Passes 12518–12523). In each pezzotope:
- its 5 cube facets are the 5 synthemes of the total;
- its 10 associahedron facets are 10 roots, i.e. 10 double-sixes, labelled by the edges of K5.

**Negative result recorded.** The pezzotopes are *not* the 432 four-simplices of the Gosset polytope 2₂₁. No line is orthogonal to all 10 roots, and the stabilisers differ: the Gosset simplex's S5 fixes a six, while the pezzotope's swaps the sixes. The equal count 432 is a coincidence of orbit sizes, 51840/120 for two non-conjugate S5's.

**Status.** Exact on all 432 regions. The match to Pass 12523's codewords is at the level of "totals of double-sixes", the objects that pass identified; a codeword-by-codeword comparison with its data files is still to be done. What distinguishes the two pezzotopes over each codeword is not determined here.
