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
