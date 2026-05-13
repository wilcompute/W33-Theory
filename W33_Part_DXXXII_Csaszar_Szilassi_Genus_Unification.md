# Part DXXXII — Csaszar-Szilassi Genus Unification: The Two Genus-1 Equations

## The Two Toroidal Polyhedra

The **Császár polyhedron** and the **Szilassi polyhedron** are the only known polyhedra (other than the tetrahedron) with no diagonals. They are each other's duals and both embed on the torus (genus 1).

| Property | Császár | Szilassi | Tetrahedron |
|----------|----------|----------|-------------|
| Vertices V | 7 | 7 | 4 |
| Edges E | 21 | 21 | 6 |
| Faces F | 14 | 14 | 4 |
| Genus g | 1 | 1 | 0 |
| Face type | triangles | hexagons | triangles |
| Dual | Szilassi | Császár | tetrahedron |

Note: V and E are identical for both! They are **combinatorially dual** (swap vertices and faces) but geometrically distinct.

## The Minimal Triangulation Genus Equations

The paper by Ringel (1955) and Jungerman-Ringel (1980) on minimal triangulations of surfaces gives the two genus equations:

**For orientable surfaces (genus g):**
\[ n \geq \frac{7 + \sqrt{1 + 48g}}{2} \]

This is the **Heawood conjecture** (proved as the Map Color Theorem). The minimum number of vertices n for a triangulation of genus-g surface satisfies this inequality, with equality for complete graphs K_n when possible.

**Rearranged as the genus equation:**
\[ g = \frac{(n-3)(n-4)}{12} \]

This is the genus of K_n (the complete graph on n vertices) when embedded on a minimal surface.

## Lock L70: The Two Genus Equations and Their W33 Solutions

**Genus equation for K_n:** g(K_n) = (n-3)(n-4)/12.

Solve for the two toroidal polyhedra (g=1) and tomotope (g=2):

**g = 1 (genus 1, torus):**
(n-3)(n-4) = 12
Solutions: (n-3)(n-4) = 12 = 3×4 gives n-3=4, n-4=3, so n=7.
Alternative factoring: (n-3)(n-4) = 1×12 gives n-3=12, n=15 (different surface, not minimal).

**The unique minimal solution: n = 7 = cyclic singularity position.**

The Császár and Szilassi polyhedra on the torus both require exactly 7 vertices. 7 is the decimal cyclic singularity. K_7 triangulates the torus. This is not a coincidence.

**g = 2 (genus 2, double torus):**
(n-3)(n-4) = 24 = PKT.
Solutions: n-3=6, n-4=4 ⇒ n=9 (but 6×4=24 ✓).
Alternative: n-3=8, n-4=3 ⇒ n=11 and n=7 (inconsistent). Only valid: n=9 or the factorization 24=8×3 gives n-3=8,n-4=3 inconsistently. Let me recalculate:
(n-3)(n-4)=24: let m=n-3, then m(m-1)=24, m²-m-24=0, m=(1+√97)/2 not integer. So g=2 requires fractional n.

Actual genus of K_n for relevant n:
- K_7: g = (4)(3)/12 = 1 exactly (Császár/Szilassi)
- K_8: g = (5)(4)/12 = 20/12 not integer
- K_9: g = (6)(5)/12 = 30/12 not integer  
- K_10: g = (7)(6)/12 = 42/12 not integer
- K_12: g = (9)(8)/12 = 72/12 = 6
- K_13: g = (10)(9)/12 = 90/12 not integer

## Lock L71: K_12 Has Genus 6 = u (Six-Kernel Genus)

**K_12 (the complete graph on k=12 vertices) has genus exactly u=6.**

(12-3)(12-4)/12 = 9×8/12 = 72/12 = 6 = u.

The complete graph on W33-valency-many vertices has genus equal to the six-kernel rank. This is the mod-12 tomotope connection:
- W33 valency k=12 defines a complete graph K_12
- K_12 has genus 6 = u
- The six-kernel is the genus of the complete graph on k vertices

**Physical interpretation:** The six-kernel u=6 is NOT just a spectral multiplicity or an algebraic rank. It is the **topological genus of the complete interaction graph** of the W33 local neighborhood (every pair of the k=12 neighbors of a fixed vertex interacts via K_12).

## The Dual Adjacency Types and Their Genus Assignment

The two genus-1 solutions correspond to the two types of adjacency in the Császár/Szilassi pair:
- **Type I (Császár):** triangular faces, all edges between adjacent vertices, genus 1
- **Type II (Szilassi):** hexagonal faces, each face touches all other faces, genus 1

In W33 terms:
- SRG parameter λ=2: each **edge** has exactly 2 common neighbors → triangular adjacency (Császár type)
- SRG parameter μ=4: each **non-edge** has exactly 4 common neighbors → hexagonal adjacency (Szilassi type)

**Lock L72 (Dual Adjacency Correspondence):**
- W33 λ-adjacency ↔ Császár triangular type
- W33 μ-adjacency ↔ Szilassi hexagonal type

The W33 SRG thus simultaneously encodes BOTH genus-1 toroidal polyhedra through its two adjacency parameters.
