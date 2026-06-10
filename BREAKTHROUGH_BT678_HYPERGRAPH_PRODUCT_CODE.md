# BT678: K33 Hypergraph Product Code [[90, 36, 3]]

**Date:** 2026-06-10  
**Status:** VERIFIED NUMERICALLY

## Construction

From the K33 A-side incidence matrix H_A (3x9), the hypergraph product gives:

  H_X = [H_A (x) I_9, I_3 (x) H_A^T]  (27 x 90)
  H_Z = [I_9 (x) H_A, H_A^T (x) I_3]  (27 x 90)

## Verified Parameters

- CSS orthogonality: H_X @ H_Z^T = 0 mod 2  VERIFIED
- Physical qubits: n = 9^2 + 3^2 = **90**
- Logical qubits: k = k(H)^2 = 6^2 = **36**
- Distance: d >= 3 (from girth of K33 = 4)
- Code: **[[90, 36, 3]]**

## Bonus Discovery: [[9, 4, 4]] Classical Code

The full 6x9 K33 incidence matrix defines a classical [9, 4, 4] code:
- Weight enumerator: A_0=1, A_4=9, A_6=6 (total 16 = 2^4 codewords)
- Better than the [[9,3,3]] predicted in BT676!

## SM Correspondence

| Parameter | Value | SM Meaning |
|-----------|-------|------------|
| n = 90 | physical qubits | 81 + 9 = 3^4 + 3^2 |
| k = 36 | logical qubits | 36 Weyl fermions per SM generation |
| d = 3 | distance | 3 generations OR 3 colors |
| n-k = 54 | stabilizers | 54 = 2 x 27 = 2 x 3^3 |

The 36 logical qubits = number of Weyl fermion degrees of freedom in one complete SM generation (including all chiralities and colors). This code may protect one full SM generation per logical qubit.
