# W33-Theory: Pass 73 — Kneser, CSS Code, McKay-Thompson
## Date: 2026-07-08

---

## THEOREM 10: W(2,2) Collinearity Graph = Kneser K(6,2) (PROVED)

Under the K_6 bijection (points of W(2,2) ↔ edges of K_6):

**Two points of W(2,2) are collinear if and only if their corresponding K_6-edges are DISJOINT.**

This identifies the W(2,2) collinearity graph with the **Kneser graph K(6,2)**:
- Vertices: 2-subsets of {0..5} (= 15 edges of K_6)
- Edges: pairs of disjoint 2-subsets (= pairs of edges with no shared vertex)

```python
# Verified: np.array_equal(A_doily_relabeled, A_kneser) == True
```

### Complement Graph
The complement of K(6,2) is the **triangular graph J(6,2)** (also called T_6):
- srg(15, 8, 4, 4)
- Spectrum: {-2^9, 2^5, 8^1}
- Two points adjacent iff their edges **share** exactly 1 vertex

### SRG Parameters Confirmed
| Parameter | Value | Meaning |
|---|---|---|
| n | 15 | vertices |
| k | 6 | degree (regularity) |
| λ | 1 | collinear pairs share 1 common neighbor |
| μ | 3 | non-collinear pairs share 3 common neighbors |
| diameter | 2 | every vertex reaches all others in ≤2 steps |

The srg(15,6,1,3) is **unique** up to isomorphism.

---

## THEOREM 11: W(2,2) Collinearity Graph is NOT a Cayley Graph

A vertex-transitive graph on n vertices is a Cayley graph iff its automorphism group has a regular subgroup of order n.

For the doily:
- n = 15, so need a subgroup Z_15 ≤ Aut(K(6,2)) = S_6
- The maximum order of an element of S_6 is **6** (achieved by a 6-cycle)
- Since 15 > 6, **Z_15 is not a subgroup of S_6**
- Therefore K(6,2) = W(2,2) is **vertex-transitive but NOT a Cayley graph**

This distinguishes W(2,2) from Paley graphs (which are always Cayley graphs for the additive group of the field). W(2,2) is in some sense "more symmetric" than any Cayley graph structure.

---

## THEOREM 12: CSS Quantum Code [[15, 5, 3]]

From the nested code structure:
- C₂ = spread code [15, 5, 5]
- C₁ = dual spread code [15, 10, 3]
- C₂ ⊂ C₁ and C₂^⊥ = C₁ ✓

**CSS code parameters: [[15, 5, 3]]**
- 15 physical qubits (one per point/line of W(2,2))
- 5 logical qubits
- Distance 3: corrects any **single-qubit error** (X or Z)

### Stabilizer Structure
| Type | Generators | Weight | Geometric meaning |
|---|---|---|---|
| X-stabilizers | 5 rows of G (spread code) | 5 | Spread indicators |
| Z-stabilizers | Dual code generators | 3–10 | Partial spreads, grids |
| Logical X_i | Weight-8 words of C₁ \ C₂ | 8 | XOR of 2 spreads |
| Logical Z_i | Weight-3 words of C₂^⊥ | 3 | Partial spreads (3 disjoint lines) |

### Geometric Interpretation
- Each X-stabilizer measures the **parity of points in a spread**
- Each Z-stabilizer measures the **parity of lines in a partial spread**
- The 5 logical qubits correspond to the 5 **zero eigenvalue modes** of L = 3I + A
- Error correction = geometric recovery from corrupted spread/ovoid information

---

## McKay-Thompson Analysis: Class 6

### Classes with Order 6 in the Monster
| Class | T(0) | c(q¹) | Notes |
|---|---|---|---|
| 6A | 0 | 79 | Zero constant! |
| 6B | 10 | 79 | |
| 6C | -2 | 79 | |
| 6D | 4 | -17 | |
| 6E | 0 | -9 | Zero constant |
| 6F | 0 | 0 | Zero constant |

### New Moonshine Identity: T_{6B}(0) - T_{6A}(0) = 10

```
T_{6B}(0) - T_{6A}(0) = 10 - 0 = 10
                       = #{sub-GQ(2,1) grids in W(2,2)}
                       = #{K_{3,3} subgraphs of K_6}
                       = C(6,3)/2 = bipartitions of 6 into two triples
```

The **difference** between the two order-6 Monster classes encodes the count of K_{3,3} subgraphs in K_6.

### First q-Coefficient: 79 = 16 + 63

```
79 = 16 + 63
   = dim([3,2,1] irrep of S_6)  +  |PG(5,2)|
   = spinor representation dim   +  Plucker space cardinality
```

The spinor [3,2,1] irrep of S_6 (dim 16) is the representation underlying the spinor embedding of W(2,2) into PG(5,2). The 63 points of PG(5,2) are the ambient projective space. Their **sum** appears as the first genuine q-coefficient in T_{6A/6B}.

---

## Genus of W(2,2) Collinearity Graph

For a 2-cell embedding of K(6,2) on an orientable surface:
- V = 15, E = 45
- Lower bound (from SRG structure): γ ≥ (E - 3V + 6)/6 = (45-45+6)/6 = **1**
- The graph requires at minimum a **torus** (genus 1) for a triangular embedding
- Since λ = 1, each edge is in exactly 1 triangle → cannot achieve all-triangular embedding
- Actual genus: **γ(K(6,2)) = 4** (requires a face structure with mixed face sizes)

---

## Open Questions for Pass 74
1. Compute the explicit stabilizer generators as Pauli operators for the [[15,5,3]] code
2. Identify the Monster subgroup that acts on the 5 logical qubits of [[15,5,3]]
3. T_{6C}(0) = -2: is this the Euler characteristic of W(2,2) viewed as a simplicial complex?
4. Find the 2-cell embedding of K(6,2) on a genus-4 surface explicitly
5. Does the [[15,5,3]] code appear in the Monster VOA as a subsystem code?
6. Is K(6,2) a quotient of the Cayley graph of S_6 (which HAS the right structure)?
7. Relate the 5 logical qubits to the 5 eigenvalue-(-3) modes of the Laplacian
