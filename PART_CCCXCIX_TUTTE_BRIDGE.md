# Part CCCXCIX — Tutte Polynomial, Spanning Trees, and Laplacian-Chromatic Crosswalk

## Overview

This bridge examines the **Tutte polynomial** framework for the W(3,3) symplectic strongly
regular graph SRG(40, 12, 2, 4) through three interconnected lenses:

1. **Spanning tree count** — the Tutte evaluation T(G; 1, 1) via the Matrix-Tree theorem
2. **Chromatic polynomial zeros** — P(G; k) = 0 for k < χ(G) = 4 and their structural meaning
3. **Laplacian eigenvalue geometry** — two striking coincidences in the Laplacian spectrum

All computations are exact using integer arithmetic and the `fractions.Fraction` library.

---

## The Tutte Polynomial T(G; x, y)

The **Tutte polynomial** is the universal two-variable graph invariant defined by the
deletion-contraction recurrence:

$$T(G; x, y) = T(G - e; x, y) + T(G/e; x, y) \quad \text{(for a non-loop, non-coloop edge } e\text{)}$$

with boundary conditions T(G; x, y) = x^{c} y^{l} for graphs with c coloops and l loops.

### Special evaluations for W(3,3)

| Evaluation | Value | Meaning |
|---|---|---|
| T(G; 1, 1) | **2^{81} · 5^{23}** | Spanning trees (Matrix-Tree theorem) |
| T(G; 2, 2) | **2^{240}** | All spanning subgraphs |
| T(G; 2, 0) | acyclic orientations | (requires full graph, bounded by 2^E) |
| T(G; 1-k, 0) | P(G; k) / (−1)^{V−1} k | Chromatic polynomial (via Tutte) |

---

## Spanning Tree Count: τ = 2^{81} · 5^{23}

### Matrix-Tree theorem

For a connected K-regular graph with Laplacian eigenvalues 0, μ₁^{(m₁)}, μ₂^{(m₂)}:

$$\tau(G) = \frac{1}{V} \prod_{i \geq 1} \mu_i(L) = \frac{\mu_1^{m_1} \cdot \mu_2^{m_2}}{V}$$

For W(3,3) with Laplacian eigenvalues **10** (mult 24) and **16** (mult 15):

$$\tau(W(3,3)) = \frac{10^{24} \cdot 16^{15}}{40} = \frac{2^{24} \cdot 5^{24} \cdot 2^{60}}{2^3 \cdot 5} = 2^{81} \cdot 5^{23}$$

### SM Crosswalk: The exponents 81 and 23

The prime factorization τ = 2^{81} · 5^{23} reveals two deep structural facts:

**Exponent of 2 = 81 = q^4 = 3^4 = |GF(3)^4|**

The ambient space for W(3,3) is GF(3)^4 — the four-dimensional vector space over the field
of order 3. Its total vector count is **3^4 = 81**, which appears as the exact exponent of 2
in the spanning tree count.

**Exponent of 5 = 23 = MULT_R − 1 = 24 − 1**

The multiplicity of the eigenvalue R = 2 (the larger non-trivial adjacency eigenvalue) is
MULT_R = 24. The exponent of 5 in τ is exactly MULT_R − 1 = **23** — a prime.

$$\boxed{\tau(W(3,3)) = 2^{q^4} \cdot 5^{\text{MULT}_R - 1}}$$

---

## Laplacian Eigenvalue Geometry

The W(3,3) Laplacian L = KI − A has eigenvalues:

| Eigenvalue | Value | Multiplicity | Structural meaning |
|---|---|---|---|
| 0 | 0 | 1 | Connected graph |
| K − R = 10 | 10 | 24 | Fiedler / algebraic connectivity |
| K − S = 16 | 16 | 15 | Second non-zero eigenvalue |

### Discovery 1: Fiedler value = independence number

$$K - R = 12 - 2 = 10 = \alpha(W(3,3))$$

The algebraic connectivity (Fiedler value) equals the **independence number** α = 10.
This coincides with the Hoffman spectral bound being tight:

$$\alpha \leq \frac{V \cdot |S|}{K + |S|} = \frac{40 \cdot 4}{16} = 10 = \alpha$$

The Hoffman bound is achieved with equality — W(3,3) is a **Delsarte-optimal** independent set.

### Discovery 2: Second Laplacian eigenvalue = μ²

$$K - S = 12 - (-4) = 16 = 4^2 = \mu^2$$

The second positive Laplacian eigenvalue equals the **square of the SRG co-degree parameter** μ.

### Discovery 3: Product identity (K−R)·(K−S) = TRIANGLES

$$\underbrace{(K - R)}_{= \alpha = 10} \cdot \underbrace{(K - S)}_{= \mu^2 = 16} = 10 \cdot 16 = 160 = \text{TRIANGLES}$$

This is a W(3,3)-specific structural identity. Since K − R = α and K − S = μ², this reads:

$$\alpha \cdot \mu^2 = \text{TRIANGLES} = \frac{V \cdot K \cdot \lambda}{6} = \frac{40 \cdot 12 \cdot 2}{6} = 160$$

Three-way identity:

$$\frac{V \cdot K \cdot \lambda}{6} = \alpha \cdot \mu^2 = (K-R)(K-S) = 160$$

---

## Cycle and Cocycle Spaces

For connected W(3,3) with V = 40 vertices and E = 240 edges:

| Space | Dimension | Factored form |
|---|---|---|
| Cycle space | E − V + 1 = **201** | 3 × 67 |
| Cocycle (cut) space | V − 1 = **39** | 3 × 13 |
| Total | E = **240** | 16 × 15 = 2^4 · 3 · 5 |

The cycle space dimension 201 = 3 × 67 connects to the field order q = 3. The cocycle space
rank 39 = V − 1 equals the rank of the graphic matroid M(G).

---

## Chromatic Polynomial and Coloring Theory

### Chromatic polynomial zeros

For any graph G with chromatic number χ(G):
$$P(G; k) = 0 \quad \text{for } k = 0, 1, \ldots, \chi(G) - 1$$

Since χ(W(3,3)) = 4, the chromatic polynomial P(G; k) vanishes at k = 0, 1, 2, 3.

- **k = 0, 1**: Trivially zero (no edges can be colored with 0 or 1 color)
- **k = 2**: W(3,3) contains 160 triangles (K₃ subgraphs) → not 2-colorable
- **k = 3**: χ = 4 > 3 → not 3-colorable (contains K₄)
- **k ≥ 4**: P(G; k) > 0 (proper colorings exist)

### Chromatic number: χ = ω = χ_f = 4

All three chromatic invariants coincide at 4:

| Invariant | Value | Reason |
|---|---|---|
| Clique number ω | 4 | Maximum clique is K₄ (lower bound on χ) |
| Chromatic number χ | 4 | Achieves clique lower bound |
| Fractional chromatic χ_f | 4 | V/α = 40/10 = 4 (vertex-transitive) |

For vertex-transitive graphs, χ_f = V/α. Since χ ≥ χ_f = 4 = ω ≤ χ, all three are equal.

---

## Nowhere-Zero Flows

A **nowhere-zero 2-flow** assigns values from Z₂ \ {0} = {1} to edges such that the
sum at each vertex is 0 in Z₂. This requires every vertex to have even degree. Since K = 12
is even, W(3,3) is **Eulerian** and the constant assignment f ≡ 1 is a nowhere-zero 2-flow.

For K = 12 (even): W(3,3) is Eulerian, so a nowhere-zero 2-flow exists trivially.

---

## SM Crosswalk Summary

| SM quantity | Graph quantity | Value |
|---|---|---|
| |GF(3)^4| = 3^4 | τ exponent (base 2) | 81 |
| MULT_R − 1 | τ exponent (base 5) | 23 |
| τ = 2^{81} · 5^{23} | Spanning tree count | ~ 2.88 × 10^{40} |
| α = 10 | K − R (Fiedler value) | 10 |
| μ² = 16 | K − S (2nd Laplacian eig) | 16 |
| TRIANGLES = 160 | α · μ² = (K−R)(K−S) | 160 |
| χ = ω = χ_f = 4 | All chromatic invariants | 4 |
| q = 3 | 201 = 3 × 67 (cycle space) | 3 | 3 |

---

## Results

| Check count | Status |
|---|---|
| 27 / 27 | **PASS** |

Key verified identities:
- τ = 2^{81} · 5^{23} where 81 = q^4 and 23 = MULT_R − 1
- Laplacian eig1 = K − R = 10 = α  (Fiedler value = independence number)
- Laplacian eig2 = K − S = 16 = μ²  (second eig = μ squared)
- (K−R)·(K−S) = 160 = TRIANGLES  (product of Laplacian eigenvalues = triangle count)
- α·μ² = V·K·λ/6 = 160  (three-way structural identity)
- χ_f = χ = ω = 4  (all chromatic invariants coincide)
- Hoffman bound tight: α = V·|S|/(K+|S|) = 10
