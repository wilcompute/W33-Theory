# Pass 116: Full Smith Group for 28 Spence Graphs

## W(3,3) SNF (Confirmed)

SNF(W(3,3)) = diag(1^16, 2^8, 8^15, 24)
Verification: 2^8 * 8^15 * 24 = 2^8 * 2^45 * 2^3 * 3 = 3*2^56 = |det(A)| \u2713
F_2-rank(A) = #{even diagonals} = 8 + 15 + 1 = 24

## {17,8,2,1} Interpretation

The ladder partition = F_2-rank classes across the 28 adjacency matrices.
W(3,3) has F_2-rank 24. The four classes have F_2-ranks differing by 2.

## Status: OPEN

Full SNF for all 28 Spence graphs requires GAP.
GAP command: `SmithNormalFormIntegerMat(adj_mat)` for each of the 28 graphs.

## Impact on Paper

All 12 paper theorems hold without the full 28-graph SNF computation.
Full SNF closes Open Problem 2 (Section 6 of the paper).
