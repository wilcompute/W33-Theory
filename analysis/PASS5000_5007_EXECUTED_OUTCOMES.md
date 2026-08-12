# Passes 5000–5007 — executed outcomes

**Date:** 2026-08-12  
**Status:** EXECUTED in committed exact producers/certificates; remote replay reported separately.

## Pass 5000 — octahedral-local radius ILP reaches a hard barrier

The 270-cell octahedral sign model was pushed together with the full degree-7 radial moment/localizing constraints. The strongest local relaxation tested is still feasible at the distance-173 frontier.

An exact integral witness takes every octahedron's four sigma-even A3 signs to `(-1,-1,-1,-1)` and its three residual equator signs to `(-1,-1,+1)`. Globally this gives

- `T3=-1080`,
- residual `U4=-270`,
- restricted `U6=1620`, `U8=-270`, `U9=-1080`, `U12=270`.

It can be attached to the Pass4960 degree-7 radial witness

`(T3,T4,T5,T6,T7)=(-1080,-1936,75316,830590,-37193040)`

with parity-compatible complementary A4/A6 shell sums. The ordinary and `(X+7)` localizing moment matrices remain positive definite.

The witness is nevertheless impossible as a **global dual character**. Since `T3=-A3` and the 1080 A3 checks span all of `K^perp`, every generator has sign `-1`, forcing `chi(h)=(-1)^wt(h)` on the whole dual code and therefore `T4=+A4=10530`, contradicting the local witness `T4=-1936`.

So the lesson is exact: octahedron-local sign constraints plus independent shell complements and degree-7 radial moments cannot lower 173. The next radius attack must encode cross-octahedron/global character closure. The rigorous interval remains `134 <= rho(K) <= 173`.

## Pass 5001 — the 20-dimensional kernel is exactly the binary tritangent V20

Pass4997 produced the canonical binary map from the 30-dimensional triangle/square quotient to a ten-dimensional Q43 target, with a 20-dimensional kernel. Pass5001 constructs the full PSp generator actions on that kernel and on the rank-20 binary tritangent-selector code `rowspan_F2(M)`.

The complete intertwiner system has one-dimensional Hom space. Its unique nonzero intertwiner has rank 20, so it is an isomorphism. The same matrix also commutes with the outer PGSp generator.

Hence there is an explicit full-group exact sequence

`0 -> V20_trit -> Q30 -> Q10 -> 0`

over F2.

This is an actual equivariant identification, not a dimension match.

## Pass 5002 — correction: the global 85-reader erasure distance is six

The previous Pass4993 global value eight was wrong. The missed relations live entirely in the 40-line sensor block.

For W33 point-line incidence, every W33 point gives a centered relation among the four line sensors through that point. If two W33 points are collinear, their four-line pencils share one line. Subtracting the two pencil relations cancels that common line and yields a raw dependency supported on exactly six line sensors.

There are exactly 240 such supports, one for every edge of the W33 point graph. Exact rank checks find no raw line or raw tritangent dependency of support 2 through 5. Therefore

`d_erasure(R)=6`

and the guaranteed arbitrary-erasure tolerance is five sensors.

The centered line and tritangent sensor spaces are orthogonal. Any mixed dependency projects to a nonzero centered dependency in each block; their exact support minima are 4 and at least 5, respectively. Thus no mixed line/tritangent support-eight cocircuit exists. Pass4998 remains correct as the pure-tritangent support-eight `2K4` classification, but support eight is not the global minimum.

The old Pass4993 certificate, manuscript insert, public page, homepage-card source, regression test and replay workflow were all hardened to this correction.

## Pass 5003 — the real octahedron frame is `1 + 20 + 15 + 84`

The graph on the 270 octahedra joining pairs sharing three H36 edges has spectrum

`32^1, 14^20, 8^15, 2^84, (-4)^150`.

The octahedron-edge incidence frame has real rank 120, so its active real row space is exactly

`1 + 20 + 15 + 84`.

A natural 270x36 matrix marking the six double-sixes missed by each tritangent pair has real rank 36 and projects with ranks `1,20,15` precisely onto eigenvalues `32,14,8`, with zero projection to `2,-4`. Thus its image is exactly the `1+20+15` part.

A second natural map, incidence of the 270 intersecting tritangent pairs with their two endpoint tritangents, has rank 45. Projection onto the eigenvalue-14 space has rank 20, giving an explicit tritangent-carrier map into the active 20.

The remaining active real sector is the eigenvalue-2 space of dimension 84.

This also closes two tempting false analogies. The real rank-120 octahedron carrier is not the coexact `30+90` module because it contains a trivial one-dimensional constituent, while coexact does not. And binary rank 90 is not a real degree-90 spectral constituent.

## Pass 5004 — no intrinsic origin exists in the residual C3 torsor

After choosing one of the four point-indexed AG(2,3) completion packets, the residual three completions form the Pass4994 C3 torsor.

The PSp line-and-point stabilizer has order 162 and image `C3` acting regularly on the triple, with kernel 54. The full PGSp stabilizer has order 324 and image `S3`, again with kernel 54.

An intrinsic equivariant selector would have to be fixed by the stabilizer. No completion is fixed by the regular C3 action. Therefore no PSp- or PGSp-equivariant origin exists.

The Witting outer sign supplies the reflection parity `S3/C3=C2`; it orients the torsor but does not choose its zero. Naming the three states `0,1,2` therefore requires an external phase/time-bin/OAM reference or equivalent C3-breaking calibration datum.

## Pass 5005 — bonkers: the `20 -> 30 -> 10` sequence is nonsplit

The full affine section equations for

`0 -> V20_trit -> Q30 -> Q10 -> 0`

were solved over F2. An equivariant section would be a 30x10 matrix satisfying both `P S = I` and `g S = S g` for the PSp generators. The complete system has 300 variables and 1532 equations and is inconsistent.

Therefore the extension does not split PSp-equivariantly, hence cannot split under full PGSp either. The 30-dimensional carrier is not merely the direct sum `20+10`; it is a genuine modular extension.

## Pass 5006 — bonkers: the binary octahedron frame has exact `60 -> 90 -> 30`

Reduce the 270x360 octahedron-edge frame modulo two. Its rank is 90. Apply the canonical shared-line projection from an H36 edge to the unique W33 line shared by its endpoint spreads.

The 270 octahedron rows map to 270 distinct weight-four vectors. They are exactly the overlap-four spread-intersection family, and their span has rank 30, equal to the residual-square image and to the orthogonal complement of the Q43 binary adjacency code.

Thus the binary octahedron carrier has the exact sequence

`0 -> K60 -> O90 -> C_Q43^perp(30) -> 0`.

This geometrically resolves the modular rank 90 instead of identifying it by numerical resemblance to a real degree-90 carrier.

## Pass 5007 — bonkers: minimum reader failures form a 24-dimensional tight frame

Let `Z` be the 40x40 W33 point-line incidence matrix. For every one of the 240 W33 point-graph edges `{p,q}`, form the signed line-sensor relation

`D_(p,q)=Z_p-Z_q`.

Every row has support six. All 240 supports are distinct, and every row annihilates the raw 40-line reader. The matrix `D` has rank 24, exactly the full left nullity of the line reader.

Moreover

`D^T D` has spectrum `60^24, 0^16`.

So the 240 global minimum failure modes form an equal-bound tight frame for the complete 24-dimensional line-reader null sector; scaling by `1/sqrt(60)` gives a Parseval frame. The minimum cocircuits are literally the W33 edge-gradient realization of that nullspace.

## Packet synthesis

The eight fronts combine into four structural conclusions:

1. **Radius frontier:** local octahedral constraints are not enough; global dual-character closure is the missing ingredient. The theorem remains `134 <= rho(K) <= 173`.
2. **Binary module architecture:** the Q43 projection has the exact nonsplit extension `0 -> V20_trit -> Q30 -> Q10 -> 0`, while the binary octahedron frame has `0 -> K60 -> O90 -> C_Q43^perp(30) -> 0`.
3. **Readout correction and geometry:** the global 85-reader erasure distance is six, with exactly 240 canonical six-line failures indexed by W33 point-graph edges; those signed failures form a tight frame for the full 24-dimensional line-reader nullspace. The 135 tritangent `2K4` failures survive as a pure-sector support-eight family.
4. **Qutrit labeling:** the residual three-state object is a genuine C3 torsor. The outer sign supplies reflection parity but cannot supply an origin; named hardware states require explicit reference data.

Pass4959 remains untouched. Finite-group signs are not promoted to spacetime CP/CPT, and modular/real carriers are kept distinct unless an explicit equivariant map is constructed.
