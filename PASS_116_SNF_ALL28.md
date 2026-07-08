# Pass 116: Full Smith Group for 28 Spence Graphs

## W(3,3) SNF (Confirmed)

SNF(W(3,3)) = diag(1^16, 2^8, 8^15, 24)
Verification: 2^8 * 8^15 * 24 = 2^8 * 2^45 * 2^3 * 3 = 3*2^56 = |det(A)| \u2713
F_2-rank(A) = #{odd diagonals} = 16
F_2-nullity(A) = #{even diagonals} = 8 + 15 + 1 = 24

## {17,8,2,1} Interpretation

The proposed ladder partition is not established by this pass. For an SNF,
the number of entries divisible by 2 is the F_2-nullity, not the rank.
W(3,3) has F_2-rank 16 and nullity 24.

## Status: OPEN

Full SNF for all 28 Spence graphs requires GAP.
GAP command: `SmithNormalFormIntegerMat(adj_mat)` for each of the 28 graphs.

## Impact on Paper

The all-28 classification and any theorem depending on its class
multiplicities remain open. Full SNF closes Open Problem 2.
