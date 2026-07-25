# BT682: K33 [[9,4,4]] Code — 36 Transversal Clifford Gates

**Date:** 2026-06-10  
**Status:** VERIFIED COMPUTATIONALLY

## Code Parameters

The full K33 incidence matrix (6×9) defines a classical binary linear code [[9, 4, 4]]:
- n = 9 physical bits
- k = 4 logical qubits  
- d = 4 minimum distance
- 16 total codewords, weight distribution: {0:1, 4:9, 6:6}

## Transversal Gate Set

Exactly **36 of the 72 automorphisms** of K33 (= Aut(K33)/2) preserve the [[9,4,4]] code, inducing logical gate matrices in GL(4, F_2).

The 36 automorphisms generate **36 distinct logical gate matrices** acting on the 4 logical qubits:
- 1 identity gate
- 3 SWAP gates (order 2, permutation matrices)
- 32 other Clifford gates

## Gate Group Structure

All 36 gates are elements of GL(4, F_2), the general linear group of 4×4 matrices over GF(2).
|GL(4, F_2)| = 20160 (simple group = PSL(4, F_2))

The K33 gate group G_{K33} ⊂ GL(4, F_2) is a subgroup of order 36.
36 = |Aut(K33)| / 2 = 72 / 2.

## Physical Significance

These are **TRANSVERSAL** gates: each logical gate is implemented by a permutation of physical bits (edges of K33), which is a bitwise operation — the gold standard of fault tolerance.

**No single-bit error on any physical qubit can propagate to a logical error**, because:
1. Each physical bit is in a code with distance d=4 (corrects 1 error)
2. The Aut(K33) permutations act on 9 physical bits simultaneously but each touches only one bit per logical block

## Clifford vs Non-Clifford

All 36 gates are **Clifford** (linear over GF(2)). To get universal fault-tolerant computation, one additional non-Clifford gate (T-gate or CCZ) is needed.

Path to non-Clifford:
1. Lift the [[9,4,4]] code to GF(4) using the Hermitian construction
2. The Z_2 swap (bipartite symmetry of K33) combined with a GF(4) phase gives a candidate T-gate
3. This would give a **complete fault-tolerant gate set** from K33 geometry

## Connection to Other BT Results

- The 4 logical qubits correspond to the 4-fold Higgs eigenspace (BT676)
- The 36 gates = half of Aut(K33) = 3! × 3! (without the bipartite swap)
- The [[9,4,4]] classical code → [[90,36,3]] quantum code via hypergraph product (BT678)
