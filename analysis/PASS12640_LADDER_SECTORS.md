# Pass 12640: the doily S6 is the other track's nine 5D blocks; two ququints; three qubits at degree 8

Claude track. Continues Pass 12639. Independent exact replay by the other track: 7332f3b48 (`analysis/2026-11-09_exact_mub_sym2_blocks.md`). It certifies all 603 maximal partial spreads of W(3,3) in Z[ω] and credits Pass 12639 with the exact proof. Its finite-shot witness is d03221905, and its Q8 eight-MUB classification is a839fb66a and following.

## Item 2 + 4: two proofs, one structure (`w33_s6_sectors.py`)

The other track splits Sym²(C⁹) into nine 5-dimensional centre-of-mass sectors (s = z + w), permuted by translations.
- The five sentinel swaps of Pass 12639 **preserve every sector** (5/5).
- On a sector, their character is **3 on a transposition and 2 on a 3-cycle: the standard representation (5,1) of S6.**

So the other track's nine identical 5D cyclotomic blocks are the nine copies of (5,1) in Sym²(C⁹) = 9·(5,1). On each block the Jucys–Murphy element J₆ has the content eigenvalues 4 (×4) and −1 (×1). The exact-integer proof and the symmetric-group proof describe the same decomposition.

## Item 1: two ququints (d = 25): the sentinel principle predicts the certified sets (`w33_ququint_umub.py`)

- **Basis-free certificate.** By the twirl identity, M = (1/d) Σ_{u covered, u≠0} W_u⊗W_u† and δ* = λ_min on Sym²(C^d). The control reproduces the d = 9 pentad's 1/9.
- **Sample.** 24 random greedy maximal partial spreads of W(3,5) (156 lines, 325 splits), of sizes 14–24.

**The certified sets (δ* > 0) are exactly those whose uncovered points are uniformly covered by splits:**

| size | uncovered | split cover | δ* | closed form |
|---:|---:|---|---:|---|
| 24 | 12 | 1 split, covered once | **16/25** | M = (26 − 10S)/25 on Sym², S = ±1 |
| 22 | 24 | 2 splits, covered once | **8/25** | M = (28 − 10(S₁ + S₂))/25 |
| 14–22, all others | 24–72 | not uniform | ≤ 0 | — |

For the single-split case the proof is one line. On Sym², the local Pauli sums give T_U = 2p·S − 2 with S² = 1, so M = (d + 1 − 2pS)/d ≥ (d + 1 − 2p)/d = 16/25.

**So two-ququint sets of 24 MUBs leaving one factorisation uncovered are strongly unextendible**, as are 22-sets leaving two. The general statement for p² dimensions: a maximal partial spread whose uncovered set is one split is strongly unextendible, with F ≥ (p − 1)²|v|⁴/p². This gives 4/9 at p = 3 (the size-8 sets) and 16/25 at p = 5. The random sample found no pentad-like small sets in d = 25; whether they exist is open.

## Item 3: three qubits at degree 8

The degree-8 Hermitian bound (Sym⁴(C⁸), dimension 330) is **−0.164**, the same value as at degree 6. The Hermitian hierarchy appears stuck, consistent with the absence of any split cover. A non-Hermitian or symmetry-reduced certificate would be needed.

## Item 5: E8

Not attempted, for the reason given in Pass 12639.
