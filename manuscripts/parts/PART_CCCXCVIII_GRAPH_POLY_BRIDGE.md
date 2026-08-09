# Part CCCXCVIII — Graph Polynomial Suite and SM Crosswalk for W(3,3)

## Overview

This part computes the **clique polynomial**, **independence polynomial seeds**, and
**matching polynomial seeds** for the W(3,3) = Sp(4,3) symplectic graph,
SRG(40,12,2,4), using only exact arithmetic derived from the SRG parameters and the
known f-vector. All 27 verification checks pass.

---

## Graph Polynomial Definitions

For a graph G = (V, E) with vertex set V and edge set E:

| Polynomial | Definition |
|---|---|
| Clique polynomial | C(G; x) = Σ_{k≥0} c_k x^k, where c_k = number of k-cliques |
| Independence polynomial | I(G; x) = Σ_{k≥0} i_k x^k, where i_k = number of independent k-sets |
| Matching polynomial | M(G; x) = Σ_{k≥0} m_k x^k, where m_k = number of k-matchings |

The **Hosoya index** is Z(G) = Σ m_k (total matchings). The **hard-core lattice gas**
partition function at fugacity λ equals I(G; λ).

---

## W(3,3) SRG Parameters

| Symbol | Value |
|---|---|
| V (vertices) | 40 |
| K (valency) | 12 |
| λ (common neighbours, adjacent pair) | 2 |
| μ (common neighbours, non-adjacent pair) | 4 |
| E (edges) | 240 |
| ω (clique number) | 4 |
| α (independence number) | 10 |
| q (field order, GF(3)) | 3 |

---

## Clique Polynomial

The f-vector of W(3,3) — counting cliques by size — is exact from the SRG structure
and symplectic geometry:

```
C(G; x) = 1 + 40x + 240x² + 160x³ + 40x⁴
```

| Coefficient | Value | Source |
|---|---|---|
| c₀ | 1 | empty clique |
| c₁ | 40 = V | vertices |
| c₂ | 240 = E | edges |
| c₃ | 160 = V·K·λ/6 | triangles |
| c₄ | 40 = V | tetrahedra (K₄ subgraphs) |

**Remark:** c₁ = c₄ = V = 40. The number of vertices equals the number of tetrahedra —
a self-referential property of the symplectic geometry.

### Key Evaluations

| x | C(G; x) | Significance |
|---|---|---|
| 0 | 1 | empty clique only |
| 1 | 481 = V·K + 1 | total clique count |
| −1 | **81 = q⁴ = 3⁴** | alternating sum = ambient space order |
| 2 | 2961 | — |
| q = 3 | 9841 | evaluation at field order |

The evaluation **C(G; −1) = 81 = 3⁴ = |GF(3)⁴|** is the central discovery of this
part: the alternating clique count equals the cardinality of the ambient 4-dimensional
symplectic vector space GF(3)⁴ in which W(3,3) is constructed.

---

## Independence Polynomial Seeds

Exact values computed via inclusion-exclusion from SRG parameters:

| k | i_k | Formula |
|---|---|---|
| 0 | 1 | empty set |
| 1 | 40 | V |
| 2 | 540 | C(V,2) − E = 780 − 240 |
| 3 | 3240 | C(V,3) − T₁ − T₂ − T₃ (see below) |

where the triple-counting decomposition uses the SRG wedge-counting identities:
- T₃ = 160 (triangles)
- T₂ = V·C(K,2) − 3T₃ = 2640 − 480 = 2160 (P₂ paths)
- T₁ = E(V−2) − 2T₂ − 3T₃ = 9120 − 4320 − 480 = 4320 (single-edge triples)

**SM crosswalk — independence seeds:**

```
i₃ = 3240 = q⁴ · V = 81 · 40
i₃ / i₂ = 3240 / 540 = 6 = q! = 3!
```

The ratio of consecutive independence seeds equals the **factorial of the field order**.
In the Standard Model context: 3! = 6 counts the quark flavours in one generation (u, d,
s, c, b, t), or equivalently the order of permutation symmetry on three generations.

---

## Matching Polynomial Seeds

| k | m_k | Formula |
|---|---|---|
| 0 | 1 | empty matching |
| 1 | 240 = E | single edges |
| 2 | 26040 | C(E,2) − V·C(K,2) = 28680 − 2640 |

The matching number ν = V/2 = 20 (W(3,3) admits a perfect matching). The partial Hosoya
index over the first three terms is H₃ = 1 + 240 + 26040 = 26281.

---

## SM Crosswalk and Polynomial Relations

| Identity | Value | SM / Geometric Meaning |
|---|---|---|
| C(G; −1) = q⁴ | 81 | ambient GF(3)⁴ space order |
| i₃ = q⁴·V | 3240 | field order⁴ × vertex count |
| i₃/i₂ = q! | 6 | factorial of field order |
| C(G; 1) = V·K + 1 | 481 | total cliques = vertex-valency product + 1 |
| c₁ = c₄ = V | 40 | vertex count = tetrahedra count |
| c₄/c₃ = 1/μ | 1/4 | K₄-to-triangle ratio = inverse μ |
| α·ω = V | 40 | independence number × clique number = V |
| T = V·μ | 160 | triangle count = vertices × μ |

The identity **α·ω = V** (10·4 = 40) is a strong structural property: the graph can be
viewed as partitioned into α = 10 maximal independent sets, each of complementary
clique size ω = 4.

---

## Statistical-Mechanical Interpretation

The independence polynomial I(G; λ) is the grand partition function of the **hard-core
lattice gas** on W(3,3) at fugacity λ. The partial sum of the first four terms at λ = 1
is 1 + 40 + 540 + 3240 = 3821.

The clique polynomial C(G; λ) = I(Ḡ; λ), the hard-core gas on the complement graph
Ḡ = SRG(40, 27, 18, 18). The Lee–Yang theorem on the zeros of I(G; z) governs the
phase transitions of this gas model.

---

## Verification

All 27 checks pass across 5 groups:

| Group | Checks | Subject |
|---|---|---|
| 1 | 5 | Clique polynomial coefficients |
| 2 | 5 | Clique polynomial evaluations |
| 3 | 5 | Independence polynomial seeds |
| 4 | 5 | Matching polynomial seeds |
| 5 | 7 | SM crosswalk and polynomial relations |

**Result: 27/27 PASS**

---

## References

- Harary, F., "Graph Theory", 1969.
- Gutman, I., "The matching polynomial and the Hosoya index", *Discrete Applied Mathematics*, 1977.
- Arocha, J. & Llano, B., "The number of independent k-sets in a graph", 2000.
- Brylawski, T. & Oxley, J., "The Tutte polynomial and its applications", 1992.
- Taylor, D. E., "Two-graphs and doubly transitive groups", *J. Combin. Theory Ser. A*, 1992.
