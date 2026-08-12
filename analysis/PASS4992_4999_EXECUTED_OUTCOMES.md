# Passes 4992–4999 — executed outcomes

**Date:** 2026-08-11  
**Status:** EXECUTED exactly in committed producers/certificates. The original global Pass4993 erasure-distance claim is corrected below by Pass5002.

## Pass 4992 — octahedral shell algebra

The 270 tritangent-pair octahedra carry four edge-disjoint sigma-even weight-three checks, four edge-disjoint sigma-odd Steiner triangles, and three edge-disjoint residual weight-four equators on the same twelve H36 edges. Their character products agree. The 1080 even triangle checks occur exactly once across the octahedra; the 120 Steiner-odd triangles occur nine times each; the 810 residual equators occur once each. Restricted subshells have sizes 1620,1080,810,270 at weights 6,9,8,12. A hypothetical distance-173 coset obeys `T3 <= -704`, hence the octahedral bounds `U12 >= -106` and residual `U4 >= -646`. The rigorous radius remains `134 <= rho(K) <= 173`.

## Pass 4993 — CORRECTED by Pass5002

The original statement `d_erasure=8` was wrong globally. The error was a line-sector carrier mismatch: it analyzed a dark spectral mode rather than the left-null relations of the raw 40-line reader.

Pass5002 found the exact correction. Each W33 point gives a centered relation among its four incident line sensors. For collinear W33 points the two four-line pencils share one line; subtracting the pencil relations cancels that shared coordinate and yields a raw six-line dependency. There are exactly 240 distinct support-six failures, indexed by the 240 W33 point-graph edges. Exact rank checks find no raw line or tritangent dependency of support 2 through 5. Therefore

`d_erasure(R)=6`,

and the guaranteed arbitrary-erasure tolerance is five sensors.

The 135 support-eight tritangent star-difference witnesses from the original pass remain correct only as a pure-tritangent family. Pass4998 still classifies that pure sector exactly as `2K4`.

## Pass 4994 — residual affine ambiguity is a C3 torsor

After choosing one of the four point-indexed completion packets, the PSp line-and-point stabilizer has order 162 and acts on the residual triple as `C3`, kernel 54. The full PGSp stabilizer has order 324 and acts as `S3`, again with kernel54. Thus the residual triple is a canonical C3 torsor, while the finite outer quotient is the reflection parity `S3/C3=C2`. Pass5004 strengthens this to a no-go theorem: no intrinsic equivariant origin exists; a compiler that names states `0,1,2` must supply an external C3-breaking reference.

## Pass 4995 — residual-equator chain complex

Over F2, H36 has cycle-space dimension325. Residual-square boundaries have rank294; sigma-even triangle boundaries have rank324. The square complex has `(H0,H1,H2)=(1,31,516)` and the triangle-filled complex `(1,1,756)`, giving the invariant filtration

`294 < 324 < 325`

with quotient dimensions `30,1`. Pass5001 identifies the 20-dimensional kernel of the later `30->10` projection exactly with the binary tritangent V20, and Pass5005 proves the resulting sequence is nonsplit.

## Pass 4996 — stale-claim firewall

The firewall blocks recurrence of the already-retracted SRG33, Ihara-discriminant, point/line-correlation, Witting ambient/Steiner, and outer-eigenspace-swap claims while positively asserting their corrected replacements. Pass5002 adds the reader-distance correction to the authoritative frontier.

## Pass 4997 — H36 checks project canonically onto Q43

Each H36 edge maps to the unique W33 line shared by its endpoint spreads. The 1080 sigma-even triangles map bijectively to the 1080 zero-center independent Q(4,3) triads. The 810 residual squares map three-to-one to the 270 size-four intersections of overlap-four spread pairs. Their image has rank30 and equals the orthogonal complement of the `[40,10,12]` Q43 adjacency code, giving a canonical `30->10` map with kernel20. Pass5001 proves that kernel is exactly the binary tritangent V20 under the full PGSp/W(E6) action.

## Pass 4998 — pure-tritangent support-eight cocircuits are exactly 2K4

The tritangent SRG contains exactly 135 relevant `K4` pairs. For every intersecting pair of cubic lines, remove the one common tritangent from their two five-tritangent stars; the remaining eight tritangents induce two disjoint `K4`s with no cross edges. Conversely all such disjoint nonadjacent `K4` pairs arise this way. This remains correct after the Pass5002 global-distance correction: it is the exact pure-tritangent support-eight classification, not the global reader minimum.

## Pass 4999 — the 270 octahedra form a rank-120/rank-90 edge frame

The octahedron-edge incidence matrix has row weight12, column weight9, real rank120 and GF2 rank90. Its squared singular spectrum is `108^1,54^20,36^15,18^84,0^150`; two octahedra share either zero or three edges. Pass5003 resolves the real active space by explicit natural maps as `1+20+15+84`, and Pass5006 resolves the binary carrier by the exact shared-line sequence `0->60->90->30->0`.

## Corrected packet synthesis

1. **Fault tolerance:** global reader erasure distance is **6**, with 240 minimum pure-line failures indexed by W33 edges. The pure-tritangent minimum remains support8 and is exactly `2K4`.
2. **Local qutrit gauge:** `12 -> 4 x 3` refines to a point-selected C3 torsor; the outer finite sign supplies reflection parity but not an origin.
3. **Code topology:** `294 < 324 < 325`; the 30-layer maps to Q43 with exact `0->V20_trit->Q30->Q10->0`, and Pass5005 shows the extension is nonsplit.
4. **Octahedron frame:** real `1+20+15+84`, binary `60->90->30`; neither the real rank120 nor binary rank90 is identified with unrelated Hodge/degree90 carriers by dimension alone.
5. **Covering radius:** the octahedral character algebra is stronger than radial moments, but the rigorous interval remains `134 <= rho(K) <= 173`.

Pass4959 was not touched. Finite-group signs are not promoted to spacetime CP/CPT, and equal dimensions are not promoted to representation isomorphisms without explicit maps.
