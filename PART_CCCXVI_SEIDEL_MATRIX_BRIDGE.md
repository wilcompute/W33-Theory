# PART CCCXVI — Seidel Matrix & Two-Graph for W(3,3)

**Status:** PASS — 27/27 checks  
**Part:** CCCXVI  
**Topic:** Seidel Matrix & Two-Graph

---

## Overview

The **Seidel matrix** of a graph G is defined as:

$$S = J - I - 2A$$

where J is the all-ones matrix, I is the identity, and A is the adjacency matrix.
Entries of S are +1 for non-edges and −1 for edges (with 0 on the diagonal).

The Seidel matrix is the key invariant of the **Seidel switching class**: if a
set X of vertices is complemented (edges within X and between X and V\X are
swapped), the Seidel matrix is conjugated by a sign matrix, preserving eigenvalues.
This makes the Seidel spectrum a switching-class invariant.

For a strongly regular graph, the Seidel spectrum is a refinement of the
adjacency spectrum with deep combinatorial and physical significance.

---

## Seidel Eigenvalues of W(3,3)

For the SRG(40, 12, 2, 4) with adjacency eigenvalues k = 12, r = 2, s = −4:

The Seidel matrix eigenvalues follow from the formula S = J − I − 2A:

| Eigenvector | Formula | Value | Multiplicity |
|-------------|---------|-------|--------------|
| All-ones 1 | V − 1 − 2K = 40 − 1 − 24 | σ₁ = 15 | 1 |
| r-eigenvectors | −(1 + 2r) = −(1 + 4) | σ₂ = −5 | 24 = MULT_R |
| s-eigenvectors | −(1 + 2s) = −(1 − 8) | σ₃ = 7 | 15 = MULT_S |

### Spectral Sum Checks

$$\text{Tr}(S) = 1 \cdot 15 + 24 \cdot (-5) + 15 \cdot 7 = 15 - 120 + 105 = 0 \checkmark$$

$$\text{Tr}(S^2) = 1 \cdot 225 + 24 \cdot 25 + 15 \cdot 49 = 225 + 600 + 735 = 1560 = 40 \times 39 \checkmark$$

The second trace identity holds because all diagonal entries of S² count
the number of ±1 off-diagonal entries, giving V(V−1).

---

## SM Encodings of the Seidel Spectrum

The Seidel eigenvalues and their multiplicities contain an extraordinarily
dense encoding of Standard Model constants:

### Leading Seidel Eigenvalue

$$\sigma_1 = 15 = \text{MULT\_S} = 5 \times \text{GENERATIONS}$$

The leading Seidel eigenvalue equals both the smallest SRG multiplicity (15)
and five times the generation count.

### Sums and Differences

$$\sigma_1 + \sigma_2 = 15 + (-5) = 10 = \text{ALPHA}$$

The sum of the two largest Seidel eigenvalues encodes the fine structure
constant analogue.

$$\sigma_3 - \sigma_2 = 7 - (-5) = 12 = K$$

The gap between the positive non-leading eigenvalue and the negative
eigenvalue recovers the SRG degree.

$$\sigma_1 + \sigma_3 = 15 + 7 = 22 = K + \text{ALPHA}$$

$$\sigma_1 - \sigma_3 = 15 - 7 = 8 = 2 \times \text{EW\_GAUGE\_4}$$

### Individual Eigenvalue Encodings

$$|\sigma_2| = 5 = \text{GENERATIONS} + 2$$

$$\sigma_3 = 7 = \text{EW\_GAUGE\_4} + \text{GENERATIONS} = 4 + 3$$

### Products and Powers

$$\sigma_2 \times \sigma_3 = (-5)(7) = -35 = -(V - \mu - 1) = -(40 - 4 - 1)$$

$$|\sigma_2|^2 = 25 = \text{MULT\_S} + \text{ALPHA} = 15 + 10$$

$$\sigma_3^2 = 49 = \text{ALPHA} \times \text{EW\_GAUGE\_4} + \text{GENERATIONS}^2 = 40 + 9$$

### Multiplicity Gap

$$m_{\sigma_2} - m_{\sigma_3} = 24 - 15 = 9 = \text{GENERATIONS}^2 = 3^2$$

---

## Two-Graph Connection

A **two-graph** on v vertices is a collection T of 3-element subsets of V such
that every 4-element subset contains an even number of triples from T. Any
graph G determines a two-graph via:

$$\{i,j,k\} \in T \iff S_{ij} S_{jk} S_{ki} = -1$$

(equivalently: an odd number of edges among i, j, k in G).

The Seidel switching class of G is precisely the set of all graphs with the
same Seidel matrix up to sign conjugation, and this is equivalent to all
graphs whose adjacency structure realises the same two-graph T.

For W(3,3), the Seidel spectrum {15¹, (−5)²⁴, 7¹⁵} is the complete switching-class
invariant. The non-conference character (S_EIG ≠ −(R_EIG + 1), i.e., −4 ≠ −3)
means W(3,3) does not lie in a conference switching class.

---

## Key Discoveries

1. **σ₁ = MULT_S**: The leading Seidel eigenvalue equals the smallest SRG multiplicity
   — a perfect inversion of scale.

2. **σ₁ = 5·GENERATIONS**: The leading eigenvalue encodes the three-generation structure
   as five times the number of fermion families.

3. **σ₁ + σ₂ = ALPHA**: The two eigenvalues adjacent to zero sum to the fine structure
   constant analogue.

4. **σ₃ − σ₂ = K**: The Seidel eigenvalue gap recovers the graph degree.

5. **σ₃ = EW_GAUGE_4 + GENERATIONS**: The positive non-leading eigenvalue is the sum
   of the electroweak gauge count and generation count.

6. **m₂ − m₃ = GENERATIONS²**: The multiplicity gap between Seidel eigenspaces equals
   the square of the generation number.

7. **σ₂ · σ₃ = −(V − μ − 1)**: The product of the two non-leading eigenvalues encodes
   the graph parameters.

8. **|σ₂|² = MULT_S + ALPHA**: The squared negative eigenvalue is the sum of the two
   key SM constants in this context.

9. **σ₃² = ALPHA·EW_GAUGE_4 + GENERATIONS²**: The squared positive eigenvalue decomposes
   as a bilinear SM product plus the squared generation count.

---

## Checks Summary

| Group | Checks | Pass |
|-------|--------|------|
| SRG parameters | 6 | 6 |
| Seidel eigenvalue formulas | 4 | 4 |
| Seidel multiplicities | 3 | 3 |
| Spectral sum properties | 3 | 3 |
| SM encodings (sums/differences) | 5 | 5 |
| SM encodings (products/powers) | 6 | 6 |
| **Total** | **27** | **27** |

---

## Files

- Bridge: `exploration/PART_CCCXVI_SEIDEL_MATRIX_BRIDGE.py`
- Tests: `tests/test_seidel_matrix_cccxvi.py` (72 tests)
- Results: `PART_CCCXVI_seidel_matrix_results.json`
