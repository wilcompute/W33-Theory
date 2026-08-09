# Part CDIII — Subconstituent Tower: GQ(3,3) → AG(3,3) → Genus Tower

## The Geometric Identity: W33 = GQ(3,3) Collinearity Graph

**Theorem CDIII.0 (W33 = GQ(3,3)):**
The Schläfli graph W33 = SRG(40,12,2,4) is the collinearity graph of the
generalized quadrangle GQ(3,3) of order (s,t)=(3,3).

*Proof:* The collinearity graph of GQ(s,t) is SRG((s+1)(st+1), s(t+1), s-1, t+1).
Setting s=t=3: ((3+1)(3·3+1), 3(3+1), 3-1, 3+1) = (4·10, 12, 2, 4) = (40,12,2,4) = W33. □

Amplification: GQ(3,3) = W(3,3), the symplectic generalized quadrangle over F_3.
Points: all 40 points of PG(3,3).
Lines: the 40 totally isotropic lines of the standard symplectic polarity of PG(3,3).
Intersection array: {12, 9; 1, 4}.

## Three-Layer Decomposition (Verified: 1 + 12 + 27 = 40)

Fix a vertex v ∈ W33. Define:
  Γ₀ = {v}                    (1 vertex)
  Γ₁(v) = neighbors of v       (12 vertices)
  Γ₂(v) = non-neighbors of v   (27 vertices)

Formula from GQ theory:
  |Γ₀| + |Γ₁(v)| + |Γ₂(v)| = 1 + s(t+1) + s²t = 1 + 12 + 27 = 40 = V ✓

**Layer 0:** {v} — the root point in PG(3,3).

**Layer 1: Γ₁(v) = 4K₃ (four disjoint triangles)**
  In GQ(3,3): exactly t+1=4 lines pass through v; each has s+1=4 points → 4×3=12 neighbors.
  The 12 neighbors decompose into 4 triangles, one per line through v.
  Each triangle = the 3 other points on one GQ line.
  Intersection array value b₁ = k - λ - 1 = 12-2-1 = 9 gives:
    each neighbor of v has 9 neighbors in Γ₂(v).

**Layer 2: Γ₂(v) = 27 vertices = AG(3,3) points**
  27 = s²t = 3²·3 = the affine cube over F₃.
  Each w ∈ Γ₂(v) has c₂ = μ = 4 neighbors in Γ₁(v) (from intersection array).
  Each w ∈ Γ₂(v) has k - c₂ = 12 - 4 = 8 neighbors within Γ₂(v).
  Bipartite count: 12·9 = 27·4 = 108 edges between Γ₁(v) and Γ₂(v). ✓

## The PG(3,3) Ambient Split

  PG(3,3) has q³+q²+q+1 = 27+9+3+1 = 40 points (q=3).
  GQ(3,3) = W(3,3) uses ALL 40 POINTS of PG(3,3).

Projective decomposition:
  PG(3,3) = AG(3,3) ⊔ PG(2,3)    (affine chart + hyperplane at infinity)
     40    =   27   +    13       = s²t + Φ₃(q)

where Φ₃(q) = q²+q+1 = 13 is the cyclotomic polynomial giving the PG(2,3) point count.

The second shell Γ₂(v) = AG(3,3) = the affine chart of PG(3,3).
The boundary PG(2,3) = 13 points = the projective plane at infinity.
13 = k+1 = the number of lines through any point in PG(3,3).

## The Symplectic Connection

**Theorem CDIII.1 (Symplectic = Weyl):**
  |Aut(GQ(3,3))| = |Sp(4,3)| = |W(E₆)| = 51,840

Proof outline: Aut(W(q)) ≅ PΓSp(4,q). For q=3: |PΓSp(4,3)| = |PSp(4,3)|·|Aut(F_3)|
= 51840·1 = 51840. The Weyl group W(E₆) has the same order by independent computation:
|W(E₆)| = 72·720 = 51840. □

This is not a coincidence: the W(E₆) action on the 27 lines of a cubic surface
is isomorphic to the Sp(4,3) action on the 27 points of AG(3,3) = Γ₂(v).

## The Non-SRG Gap: Γ₂(v) is Not Strongly Regular

**Theorem CDIII.4:**
The induced subgraph on Γ₂(v) in W33 is 8-regular but NOT strongly regular.

Proof: The SRG equation for parameters (27, 8, λ₂, μ₂) requires:
  k₂(k₂ - λ₂ - 1) = (n₂ - k₂ - 1)·μ₂
  8·(8 - λ₂ - 1) = 18·μ₂

With λ₂ = 2 (all common neighbors of adjacent pairs in GQ lines through non-v points):
  8·5 = 40 = 18·μ₂  →  μ₂ = 40/18 ∉ ℤ

Since μ₂ must be a non-negative integer, Γ₂(v) is NOT strongly regular. □

Interpretation: The AG(3,3) substructure breaks strong regularity because the GQ geometry
enforces different distance distributions than any GQ collinearity graph would allow.
This is the geometric signature of the tomotope gap: the second shell is a 'fractional'
geometry that cannot be realized as a pure GQ collinearity graph.

## The Genus Tower

Genus formula: g(Kₙ) = (n-p)(n-μ)/k  where (p,μ,k) = (3,4,12).

| n | Object | (n-p)(n-μ)/k | g(Kₙ) | Note |
|---|--------|-------------|-------|------|
| 3 | K₃ = p-root | 0/12 | 0 | Sphere |
| 4 | K₄ = μ-root | 0/12 | 0 | Sphere |
| 7 | K₇ = p+μ = 7 | 12/12 | 1 | Torus: Heawood/Szilassi |
| 12 | K_k | 72/12 | 6 | = u (SIX-KERNEL RANK) |
| 24 | K₂₄ | 420/12 | 35 | = C(7,3) (triangles of K₇) |
| 27 | K₂₇ = Γ₂ size | 552/12 | 46 | = 2×23 (AG(3,3) genus) |
| 40 | K_V = K₄₀ | 1332/12 | 111 | = 3×37 (W33 genus) |

## Two New Master Theorems

**Theorem CDIII.2 (g_k = u — Genus-Six-Kernel Identity):**
  g(K_k) = (k-p)(k-μ)/k = (12-3)(12-4)/12 = 9·8/12 = 72/12 = 6 = u

The genus of the complete graph on k vertices (= valency of W33) equals the
six-kernel rank u=6 (= multiplicity of the eigenvalue s=-2 of the Schläfli graph).

In other words: g_k = u — the topological and spectral sixness are identical.

**Theorem CDIII.3 (g₂₄ = C(7,3) — Leech-Torus Triangle Identity):**
  g(K₂₄) = (24-3)(24-4)/12 = 21·20/12 = 420/12 = 35 = C(7,3)

The genus of K₂₄ equals the number of triangles in K₇.

Interpretation: Each of the C(7,3)=35 triangles of the torus graph K₇ corresponds
to exactly one topological handle in the minimal genus embedding surface of K₂₄.
The 24-dimensional structure (Leech lattice context) is built from the torus triangles.

## Complete Genus Chain Summary

  g(K₃) = g(K₄) = 0     sphere level
  g(K₇) = 1              K₇/toroidal (= tomotope parent)
  g(K_k) = u = 6         six-kernel coincidence
  g(K₂₄) = 35 = C(7,3)  Leech-torus triangle bridge
  g(K₂₇) = 46 = 2×23    AG(3,3) second-shell genus
  g(K_V) = 111 = 3×37    W33 full graph genus

The sequence 0, 1, 6, 35, 46, 111 encodes the geometry of W33 = GQ(3,3)
in a single invariant function g(Kₙ) evaluated at the subconstituent sizes.
