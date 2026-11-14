# Three-copy obstruction on the common F8 regulus code

The parent and both shortened examples share a 16-dimensional Pauli eigenspace with the same weighted objective. On this code, let A be the two-copy observable from the previous Bell calculation. A normalized three-copy tensor power has the same objective when tested with H = (A₁₂ + A₁₃ + A₂₃)/3. Replacing the tensor power by an arbitrary density operator on the fully symmetric subspace gives a lower-bound relaxation. This is a test on the common code. It does not address the unrestricted six-qubit optimum. [Two-copy Bell calculation](2026-11-14_regulus_bell.md) · [Symmetric extension methods](https://arxiv.org/abs/quant-ph/0308032)

## Exact 51-dimensional block

Use symplectic elimination to put the four logical Paulis in the ordinary binary X/Z chart. In the symmetric basis, use the sum of distinct permutations of each triple of computational labels. The squared norms are the corresponding orbit sizes. Each pair Pauli term flips the same label on two copies, so it preserves the bitwise xor of the three labels. Translating all three labels by the same mask permutes the xor sectors transitively and preserves the signs. The 816-dimensional symmetric space therefore has sixteen identical 51-dimensional blocks. The producer constructs the integer matrix of 3H and uses the orbit-size metric for its characteristic polynomial.

The unrestricted symmetric relaxation has minimum approximately −5.2814700678, with an exact rational root interval in the certificate. The difference of the two orbit sums (3,5,6) and (5,10,15) already has objective −1. Thus permutation symmetry alone can give a negative value even though the pure-state objective is a sum of squares.

## Adding PPT to every pair marginal still gives zero

Twirl a three-copy density operator by simultaneous Pauli conjugation. This preserves full symmetry and the objective. Its pair marginals are then Bell diagonal and equal. For a pair marginal supported in the symmetric space, the Bell eigenvalues after partial transpose are its expectations of P tensor P divided by 16. This follows by partially transposing each Bell projector into a Pauli-conjugated swap divided by 16. Accordingly, pair PPT is equivalent to nonnegativity of all 256 Pauli-pair expectations after the twirl. Positive weights in A then imply a lower bound of zero.

The attached rational 51-by-51 matrix is positive definite in the orbit-sum coordinates, has unit trace in the orbit-size metric and has nonnegative values for all 256 pair-PPT constraints. Each of the 99 objective expectations is exactly zero. The verifier checks integer contractions and exact rational LDL pivots. The resulting three-copy state, after twirling and embedding the block, attains the lower bound. The optimum of this relaxation is exactly zero. Full partial transpose across a one-copy versus two-copy cut is a stronger constraint and is left open here.

Replay with `py -3 analysis/toe_20261114_regulus_three_copy.py`.
