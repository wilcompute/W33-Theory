# Pass 12635: the two tropical moduli spaces of the corpus see the two halves of W(3,3)

Claude track. Producer: `analysis/w33_pass12635_burkhardt_fan.py`, writing `data/w33_pass12635_burkhardt_fan.json`. Test: `tests/test_w33_pass12635.py`. Continues Pass 12634.

**Not a theory of everything.** This is exact combinatorics over F₃⁴ that reproduces a published theorem in W(3,3) language.

## The object

The Burkhardt quartic compactifies A₂(3), the moduli space of principally polarised abelian surfaces with level-3 structure. That is the corpus's genus-2 level-3 flavour modulus (Passes 11869–11899).

Its tropicalisation (Ren, Sam, Schrader and Sturmfels, arXiv:1303.1132, Thm 4.3) is the fan over a 2-dimensional simplicial complex:
- 85 vertices: 40 of type (a), indexed by the lines through 0 in F₃⁴, and 45 of type (b), indexed by pairs {b, b⊥} of orthogonal non-isotropic planes;
- 600 edges: 240 aa and 360 ab;
- 880 triangles: 160 aaa and 720 aab.

## Reconstruction (every count matches the theorem)

In F₃⁴ with the symplectic form:

| fan element | W(3,3) / two-qutrit object | count |
|---|---|---:|
| (a) rays | the 40 **points** of W(3,3) | 40 |
| (b) rays | the 45 **splits** {b, b⊥}: tensor factorisations of two-qutrit space | 45 |
| aa edges | collinear (commuting) point pairs, the W(3,3) edges | 240 |
| aaa triangles | three points on an isotropic line (a maximal commuting set) | 160 = 40 × 4 |
| ab edges | a point lying in one tensor factor, b or b⊥ | 360 = 45 × 8 |
| aab triangles | one point in each factor, together with the split | 720 = 45 × 16 |

Checks:
- Within each split, every point of b is orthogonal to every point of b⊥, and the points within b are pairwise non-orthogonal.
- The aa graph is W(3,3)'s **point** graph: |{x,y}^⊥⊥| = 4 for all 540 non-collinear pairs, so it is not the dual Q(4,3).

## The duality

| | tropical Burkhardt = trop A₂(3) (genus-2 level-3; flavour modulus) | tropical moduli of cubic surfaces (Naruki fan; Pass 12634) |
|---|---|---|
| dimension of fan | 3 | 4 |
| W(3,3) half on the rays | **40 points** (type a) | **40 lines** (type b, cusps) |
| the other rays | 45 splits (type b) | 36 positive E6 roots (type a) |
| how the 45 splits appear | as rays | as the 45 D4 classes of the 135 aaaa cones |
| W(3,3) relation | collinear = shared cone | collinear (in Q(4,3)) = disjoint stars |

**Reading.**
- The two moduli spaces in the corpus, genus-2 level-3 abelian surfaces (flavour) and marked cubic surfaces (E6), tropicalise to fans carrying the two halves of the generalised quadrangle W(3,3): its points and its lines.
- Both fans share the 45 tensor splits. In two-qutrit language, the tropical flavour moduli space is the complex of commuting Pauli sets together with tensor factorisations.

**Prior art.** The fan and its counts are Ren, Sam, Schrader and Sturmfels's. That the 40 index points of F₃⁴ and the isotropic planes carry W(3,3) is implicit in their indexing. **New here:** the reconstruction in two-qutrit terms, the point-graph-versus-line-graph decision against Pass 12634's Naruki result, and the duality table. No novelty claimed beyond that.

## The E7 next rung (literature, not computed)

- Degree-2 del Pezzo surfaces correspond to E7. Their real moduli space has 60,480 regions: 6-dimensional homology balls with f-vector (579, 1737, 2000, 1105, 297, 34) and stabiliser of order |W(E7)|/60480 = 48. Their positive-geometry status is conjectured (Early, Geiger, Panizzut, Sturmfels and Yun).
- W(E7)/±1 ≅ Sp(6,2), so the E7 rung's polar space is W(5,2), with 63 points matching the 63 positive roots.
- Testing whether the E7 pezzotope's 34 facets are a W(5,2) configuration, as the E6 pezzotope's 15 facets are a W(3,3) S5-pentad, is the natural next computation.

## Addendum: an explicit dictionary between the two fans (`w33_split_bridge.py`, `data/w33_split_bridge.json`)

The map is an explicit graph isomorphism φ (VF2) from the 40 A2³ subsystems, related by root-disjointness, to the 40 isotropic lines of W(3,3) in F₃⁴, related by meeting. Through φ:
- **36 roots ↔ the 36 spreads**, bijectively. For every root, the 10 A2³ containing it go to 10 pairwise disjoint lines covering all 40 points. This is the classical roots ↔ double-sixes ↔ spreads correspondence, made explicit.
- **40 points ↔ partitions of the 36 positive roots into four A2³ blocks.** For every point, the 4 lines through it are 4 pairwise root-disjoint A2³ whose roots partition all 36 positive roots.
- **45 D4 ↔ 45 splits**, bijectively.
  - Every D4 meets every A2³ in 3 roots: an A2 for 16 of them, an orthogonal triple for 24.
  - Every split {b, b⊥} is met by 16 lines in one point of b and one of b⊥, and missed by 24 lines.
  - Under φ, each D4's 16/24 partition equals exactly one split's.
  - The coarser invariant |D4 ∩ T| is constant (3) and separates nothing; it was recorded as the failed first attempt.

| cubic-surface (Naruki) fan | W(3,3) / two-qutrit | Burkhardt (flavour-modulus) fan |
|---|---|---|
| 36 positive roots (type-a rays) | 36 spreads = double-sixes | — |
| 40 A2³ (type-b rays, cusps) | 40 lines = maximal commuting sets | the 160 aaa triangles (4 per line) |
| 45 D4 (classes of the 135 aaaa cones) | 45 tensor splits | 45 type-(b) rays |
| partitions of the 36 roots into four A2³ | 40 points | 40 type-(a) rays |

Because φ is an isomorphism between strongly regular graphs, it is unique up to automorphisms. The bijections above are φ-dependent as maps but not as statements: they hold for every φ.

## Addendum: the level ladder explains the duality (`w33_level2_ladder.py`)

**Level 2** is the genus-2 level-2 moduli space, the Segre cubic and its dual Igusa quartic, with symmetry S6 = Sp(4,2) acting on the doily W(3,2): 15 points = duads, 15 lines = synthemes.
- Ren, Sam, Schrader and Sturmfels (arXiv:1303.1132, Thm 2.4) show the two tropical fans are **affinely isomorphic**, differing only in multiplicity (1 against 2). Both are trop M₀,₆ with 25 rays (15 duads + 10 three-three splits), 105 edges and 105 maximal cones; the Segre fan's coordinates are indexed by the 15 synthemes.
- **Reconstruction from split compatibility**: all counts match. The edges split as 45 duad–duad, which is **exactly the doily collinearity graph SRG(15,6,1,3)**, and 60 duad–split. The doily's point graph (duads) and line graph (synthemes) are **isomorphic**.

**Level 3** (Passes 12634–12635): the Burkhardt (genus-2 level-3) fan sees W(3,3)'s **points**, and the cubic-surface fan sees its **lines**. Their graphs have the same SRG parameters but are **not** isomorphic: the double-perp test gives 4 for W(3,3) against 2 for Q(4,3).

**Reading.** The doily W(3,2) ≅ Q(4,2) is self-dual, and at level 2 the two dual moduli spaces' tropical fans coincide. W(3,3) is not self-dual (W(3,q) ≅ Q(4,q) only for even q), and at level 3 the two moduli spaces' fans split into its two halves. The point/line duality of Passes 12634–12635 is therefore the level-3 shadow of W(3,q) failing to be self-dual for odd q.

At both levels, rays and coordinates are dual halves. At level 2 the rays are duads (points) and the coordinates synthemes (lines). At level 3 the Burkhardt rays are points and its coordinates the 40 isotropic planes (lines).
