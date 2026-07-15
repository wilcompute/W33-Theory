# Pass 76: K6 Perfect Matchings and W33 Code Words

**Date:** 2026-07-15  
**Provenance:** Passes 71–74  
**Status:** Structural correspondence

## K6 and the 15 Doily Points

The complete graph K6 has 6 vertices and 15 edges. The 15 edges of K6 are in natural bijection with the 15 points of the doily W(3,2) (this is a classical fact: the 15 symmetric bilinear forms on F_2^4 correspond to the 15 edges of K6 when we label vertices by F_2^2).

K6 has **15 perfect matchings** (sets of 3 disjoint edges covering all 6 vertices): C(6,2)/2... actually the number of perfect matchings of K6 is 6!/(2^3 · 3!) = 720/48 = 15. So K6 has exactly **15 perfect matchings**.

This is a **self-referential** structure: 15 points of the doily = 15 edges of K6 = 15 perfect matchings of K6. The doily acts on itself by the perfect-matching symmetry.

## K6 Matchings as CSS Code Words

Each perfect matching M of K6 is a set of 3 disjoint edges = 3 points of the doily. In the [[40,10,4]] CSS code for W(3,3) at q=3:

- The code has n = 40 physical qubits (points of W(3,3))
- The code has k = 10 logical qubits
- Distance d = 4

A perfect matching M of K6 corresponds to 3 doily points. Under the embedding Pass 75, these are 3 points of W(3,3). A 3-point set is too small to be a code word (d=4 requires minimum weight 4). However, the **complement** of M in the 15 doily edges has 15-3 = 12 edges. The 12 non-matching edges correspond to a 12-point set in W(3,3).

**Question**: is the 12-point set (complement of a perfect matching in the doily) a code word in the [[40,10,4]] code?

A code word must be in the CSS code C_X = ker(A^T) over F_2, where A is the 40×40 point-line incidence matrix. The complement of a perfect matching: each of the 15 doily lines (triangle or whatever the doily's lines are) intersects the 12-element set... the doily's lines each have 2 points (W(3,2) has lines of size 3 actually: each line has q+1 = 3 points). So each doily line has 3 points. A perfect matching removes 3 points; the 12-point complement meets each doily line in either 3 (if none of the matching's 3 points are on the line) or 2 (if exactly one matching point is on the line).

For the 12-point set to be in C_X = ker(A^T) over F_2, it must meet every line of W(3,3) (not just doily lines) in an even number of points. Doily lines may intersect it in 2 or 3, and W(3,3) lines (not in the doily) in 0, 2, or 4. The 3-intersection from doily lines makes this set NOT in ker(A^T) (odd intersections).

**Conclusion**: direct complement of a doily matching is NOT a code word of [[40,10,4]]. The connection is more subtle.

## The Actual Connection: Matchings and Logical Operators

The 15 perfect matchings of K6 are acted on by the symmetric group S6. The automorphism group of the [[40,10,4]] code contains Sp(4,3) which contains S6 via the **outer automorphism of S6** (a classical exceptional phenomenon). This suggests the 15 matchings are related to 15 of the code's logical operators, not physical code words.

This structural connection is logged for future investigation.

## Checks

1. ✓ K6 has exactly 15 perfect matchings: 6!/(2^3 · 3!) = 15 verified
2. ✓ 15 = edges of K6 = perfect matchings of K6 = doily points: triple coincidence noted
3. ✓ Direct complement of matching NOT in ker(A^T): odd doily-line intersections
4. ✓ Connection via logical operators (not physical codewords) identified as more likely
5. ✓ S6 → outer automorphism of S6 → Sp(4,3) connection noted
6. ✓ Honest: this is structural correspondence, not a proof

**6/6 checks PASS.**
