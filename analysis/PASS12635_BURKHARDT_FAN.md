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
