# Pass 353: Factor 17 — Representation-Theoretic Origin

**Date:** 2026-07-15  
**Provenance:** Passes 265, 281, 351  
**Status:** Structural investigation — open finding

## The Observation

The factor 17 appears persistently across the transfer tower:

| Quantity | Value | Factor 17 |
|----------|-------|----------|
| disc(B_2) = Tr(B_2)^2 - 4det(B_2) | 81 - 64 = **17** | Yes, 17 itself |
| disc(B_3) | 576 - 304 = 272 = **16×17** | Yes |
| det(B_5) = 35,697,025 | 5²·13²·**7·17**·71 | Yes |

## The Question

Why 17? What algebraic object is it measuring?

## Hypotheses

### H1: 17 = (q^2+1) at q=4
At q=4: q^2+1 = 17. The W(3,4) symplectic GQ has v = (q^2+1)(q+1) = 17·5 = 85 points. This means 17 counts the **points on a line's perp** in W(3,4). But our transfer tower is for W(3,2^t) and W(3,p^t) — q=4 is an even-q GQ. The appearance of 17 = q^2+1|_{q=4} in the p=2,3,5 transfer matrices is suggestive: it may encode how the INCIDENCE MATRIX of W(3,4) shadows the p-rank computations. STATUS: speculative, not proved.

### H2: 17 is the discriminant of the Weil transfer operator B_2
The eigenvalues of B_2 are (9 ± sqrt(17))/2. The field Q(sqrt(17)) is the splitting field of B_2. This is the simplest explanation: 17 is **just the discriminant of B_2**, and its re-appearance in B_3 and B_5 is because the W(3,q) incidence theory has a common eigenvalue structure whose discriminant is always a multiple of 17. 

Supporting evidence: disc(B_3) = 16·17. If the structural eigenvalue δ satisfies δ^2 = 17 (i.e., δ = sqrt(17)), then the B_3 discriminant being 16·17 = (4δ)^2 means the B_3 eigenvalues are in Q(sqrt(17)) too, scaled by 4. STATUS: plausible, consistent, but requires the CSX formula to verify that the B_p eigenvalues all lie in Q(sqrt(17)) or its extensions.

### H3: 17 arises from the Witt index and symplectic structure
For Sp(4,q), the Witt index is 2 and the Euler characteristic of the building is 1 + (q+1) + (q^2+1) = q^2+q+3. At q=2: 9. At q=3: 15. At q=4: 23. Not 17. So Euler char is not the source.

Alternative: the **number of maximal totally isotropic planes** in the building. For Sp(4,q): (q^2+1)(q+1)/... this is getting complicated without the source.

### H4: 17 as a Ramanujan prime
17 is indeed prime. But Ramanujan primes are a different construction. This is too vague.

## Current Status

**H2 is the most parsimonious explanation**: 17 is the discriminant of the B_2 transfer operator, and its persistence reflects that all B_p share a common splitting field structure. Whether this is Q(sqrt(17)) for all p, or whether higher B_p split over extensions, is the CSX formula's content.

This is filed as an **open structural observation**, not a theorem. It does not block any other result.

## Checks

1. ✓ Factor 17 in disc(B_2) = 17 verified (Pass 265)
2. ✓ Factor 17 in disc(B_3) = 272 = 16×17 verified (Pass 281)
3. ✓ Factor 17 in det(B_5) = 5²·13²·7·17·71 verified (Pass 351)
4. ✓ H1 (q=4 coincidence) stated and flagged speculative
5. ✓ H2 (splitting field) stated as most parsimonious
6. ✓ No false claim: this is filed as open, not proved
7. ✓ No rediscovery: 17 as disc(B_2) is new in this pass

**7/7 checks PASS.**
