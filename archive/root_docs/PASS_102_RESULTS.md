# Pass 102: W(E6) Orbit Structure on Lambda_C Discriminant Cosets

## Result

The 255 nonzero discriminant cosets of the Construction-A lattice Lambda_C
(built from the binary code C_2(W(3,3)) = [40,16,8]) decompose into exactly
**three orbits under the code-induced \(W(E_6)\) embedding**:

| Orbit | Size | Q-value | |Stab| |
|-------|------|---------|--------|
| {0} (trivial) | 1 | - | 51840 |
| Isotropic | 135 | Q=0 | 384 = 2^7*3 |
| Anisotropic | 120 | Q=1 | 432 = 2^4*3^3 |

All 256 = 2^8 vectors accounted for.

Pass 125 repairs the original proof. The old Pass 102 witness counted the two
quadratic strata and incorrectly inherited transitivity from the containing
\(O_8^+(2)\). It now invokes the explicit
\(\operatorname{PGSp}(4,3)\cong W(E_6)\) coordinate action, whose faithful
order-\(51840\) quotient image directly measures the orbits above.

This action is not the Pass 117 ordered-anisotropic-pair stabilizer. That
nonconjugate \(W(E_6)\) embedding has isotropic orbits
\(27+36+36+36\) and anisotropic orbits
\(1+1+1+27+27+27+36\).

## The Complete E6/E8 Bridge

Every numerical constant in the W(3,3) arithmetic tower traces to one object:

| Quantity | Value | Source |
|----------|-------|--------|
| Local-axis endpoints | 240 | #E8 roots = 2x120 anisotropic cosets |
| W(3,3) vertices | 40 | dim(Lambda_C) |
| Discriminant rank | 8 | E8 rank = code min dist d=8 |
| Isotropic cosets | 135 | O+(8,2) polar graph vertices (GQ(2,4)) |
| |Aut(W(3,3))| | 51840 | |W(E6)| |
| Ihara amplitude | 78 | dim(E6) = 2*(24+15) |
| Code wt-8 words | 45 | #E6 tritangent planes |
| Dual code wt-6 words | 240 | #E8 roots |
| Theta series weight | 20 | 40/2 |

## Witnesses
- 135 isotropic vectors confirmed by explicit enumeration of O+(8,2) form Q(v)=v0v1+v2v3+v4v5+v6v7
- 120 anisotropic vectors confirmed
- Faithful code-induced quotient action of order 51840 explicitly enumerated
- Orbit sizes 135 and 120 measured, not inferred from the containing group
- Stabilizer orders 384=2^7*3 and 432=2^4*3^3 verified by orbit-stabilizer theorem
- All assertions PASS

## Verdict
For the code-induced embedding, the 255 nonzero cosets organize into the
isotropic/anisotropic split. Pass 125 also proves that \(O_8^+(2):2\) contains
a second, nonconjugate \(W(E_6)\) embedding with the finer
\(E_8\to E_6\times A_2\) branching fingerprint.
