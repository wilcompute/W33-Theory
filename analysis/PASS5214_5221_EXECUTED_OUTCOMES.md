# Pass5214–5221 executed outcomes

**Status:** executed 2026-08-14. This packet consumed the five requested continuation fronts without colliding with the separately executed Pass5206–5213 packet, then added three independent probes. The q=5 minimum-distance firewall is preserved: leader 36 and the footprint primal distance remain open.

## Pass5214 — fixed point footprint + connected L gluing gives exactly six stars

Fix one q=5 W-point footprint, consisting of 25 P components. Each component has 36 P-minimum atoms, so a P-heavy-free weight-625 candidate chooses one atom in each component. Evaluating the ten fundamental triangle checks in all 9750 connected L charts gives exactly 17,250 nontrivial unary and 7,500 binary constraints, with no higher-arity constraint on these 25 groups.

The unary constraints leave exactly six atoms in every component, namely the six atoms incident with the fixed W point. Label them by the six W-lines through that point. The 7,500 binary equations cover all C(25,2)=300 component pairs, and for every pair they allow exactly the six equal-label choices `(ell,ell)`. Hence all 25 components must select one common line label. There are exactly six global solutions, and direct apartment comparison identifies them with the six chamber stars based at the fixed point.

Therefore a point-footprint P-heavy-free q5 weight-625 word satisfying all L checks is necessarily a chamber star.

## Pass5215 — q3 provenance decoder has global guaranteed radius seven

The projective collineation stabilizer of apartment 0 was constructed directly from Sp(4,3): 51,840 symplectic matrices reduce to 25,920 projective point actions, of which 16 fix the base apartment. Canonical augmentation under these 16 actions gives connected-set orbit counts through the base

`1, 5, 57, 1043, 25929, 734414`

at sizes 1 through 6.

Every connected seven-set containing the base has a connected six-set parent containing the base; after mapping the parent to its stabilizer representative, the seven-set occurs among a one-vertex extension of that representative. An exact scan covers 64,439,500 such extensions. After maximum-vote and maximum-singleton provenance filtering—before tie-degree pruning—every candidate set is nonempty and contained in the true errors. The same stronger statement holds for every size-six representative.

Disconnected patterns lift cleanly by chart-sharing components. Thus the refined deterministic decoder has global guaranteed radius 7. Its first correction leaves weight at most 6, which Pass5176 clears in at most four more sweeps, so the global sweep bound is 5.

## Pass5216 — exact connected odd-q L spectra at q=3 and q=5

The L/opposite-line chart graph has one vertex per L chart and one edge per apartment. At q=3 it is connected, triangle-free, 6-regular on 540 vertices. Its exact spectrum is

`6^1, 3^60, 2^84, 1^81, (-1)^120, (-3)^116`,

plus both roots of `x^2-2x-9` with multiplicity 24 and both roots of `x^2+x-18` with multiplicity 15.

At q=5 it is connected, triangle-free, 15-regular on 9750 vertices. Its exact spectrum is

`15^1, 6^130, 5^1235, 3^520, 1^1899, 0^520, (-2)^520, (-3)^625, (-4)^520, (-5)^1534`,

plus roots of `x^2-3x-50` (multiplicity 90 each), `x^2+2x-75` (65 each), `x^2+2x-30` (104 each), and the three roots of `x^3-4x^2-12x+40` (576 each).

The certificate uses square-free integer annihilators and exact closed-walk traces, not floating eigensolvers.

## Pass5217 — the q5 root outer shell is an actual 4x4 P-atom torus

For the canonical U(5)-fixed chamber, order its 625 apartments by state coordinates

`u(a,b,c,d)=x0(a)x1(b)x2(c)x3(d)`.

Its 25 P-minimum atoms are exactly the fibers of

`(a,b,c,d) -> (a,c)`.

Thus an atom fixes `(a,c)` and contains all 25 `(b,d)` values. The 16 distance-four root states

`(a,b,c,d)=(a,b,2ab,2a^2 b)`, `a,b !=0`,

hit 16 distinct atoms, exactly `(a,c) in (F5^*)^2`. The remaining nine atoms are the coordinate cross `a=0 or c=0`. This is an explicit controller-to-equality-coordinate map rather than a cardinality coincidence.

## Pass5218 — the scalar quartic route is provably redundant at leader 36

Consider the complete nonnegative quartic minorant family

`odd(r) >= r-2 C(r,2)+a C(r,3)+b C(r,4)-c C(r,8)`, `0<=r<=8`.

Its feasible coefficient polytope has exactly five vertices:

`(0,0,0)`, `(6/7,0,0)`, `(0,24/35,0)`, `(36/35,0,48/5)`, `(0,36/35,24)`.

The currently certified aggregate fourth-order input is `S4>=5 P4`, because every selected four-edge path has five common apartments at q=5. Evaluating all five vertices against every Pass5205 critical leader-36 profile N1=54..64, with the exact S3 lower bound and A8 cap, gives an optimum with `b=0` every time. N1=54,55 choose the old 6/7 cubic; N1=56..64 choose the old full-apartment-corrected cubic.

Therefore no scalar tuning of the exact quartic moment using only `S4>=5P4` can improve the current leader-36 bounds. A successful fourth-order attack must retain configuration-resolved quadruple information, correlate the occupancy >=5 remainder, or use an independent quotient/residual constraint.

## Pass5219 — outside-box: root torus and coordinate cross carry the same connected-L syndrome

Inside the canonical q5 chamber star, let T be the 16 nonzero `(a,c)` P atoms and X the nine coordinate-cross atoms. They are disjoint with weights 400 and 225 and satisfy `T xor X = Star`.

Their L-restriction histograms are very different:

- T: `9530*0 + 80*3 + 140*4`;
- X: `9500*0 + 140*1 + 80*2 + 30*5`;
- Star: `9500*0 + 250*5`.

Yet T and X have exactly the same fundamental connected-L triangle syndrome: weight 664, distributed over charts as syndrome weights `1^40, 2^16, 3^64, 4^100`. Their XOR cancels to the zero star syndrome. This identifies a nontrivial 16/9 root-controller decomposition inside the L compatibility operator.

## Pass5220 — outside-box: all-q P-atom presentation and exact L-glue rank

Let `C_q=Cut(K_{q+1}) tensor Cut(K_{q+1})` be one P component. Its `(q+1)^2` minimum simple-tensor atoms span its q^2-dimensional component code, so each component has `2q+1` internal atom relations.

There are `q^2(q^2+1)/2` P components. Therefore the complete P-triangle solution space has dimension

`q^4(q^2+1)/2`.

The full apartment code is the intersection with the L-theta kernel and has dimension q^4. Hence the connected L compatibility operator has exact rank

`q^4(q^2-1)/2`

on the P-side space.

At q=5 this is

`11700 atom variables -> /3575 internal relations -> 8125 P-side dimensions -> /7500 independent L conditions -> 625 apartment-code dimensions`.

This is an all-q linear presentation of the apartment code by minimum P atoms plus L gluing.

## Pass5221 — outside-box: exact modular ranks of the connected L graph

The characteristic-zero spectrum does not describe the binary modules by simple parity reduction. Direct GF(2) elimination gives:

- q3: `rank A=440`, `null A=100`; `rank(A+I)=360`, `null(A+I)=180`;
- q5: `rank A=7074`, `null A=2676`; `rank(A+I)=6891`, `null(A+I)=2859`.

These large modular radicals provide concrete binary L-side submodules for future equality/residual analysis and establish a firewall against naively reducing Pass5216's real eigenspaces modulo two.

## Parallel-frontier reconciliation and evidence boundary

The independently executed Pass5206–5213 packet remains authoritative for the q5 leader/footprint front. Pass5206 proves the first degree-class aggregation of full cut-coset constraints is redundant at leader 36. Pass5207 shows a P-heavy weight-625 exotic would force nonzero footprint weight at most 24. Pass5209 narrows the primal footprint code to `[325,65,d<=25]` with a 64-dimensional hull and strict mod-4 weight classes, but d=25 is still open. Pass5213 proves the dual footprint code `[325,260,8]`.

Accordingly, the strict q5 sub-625 barrier remains chamber leader >=36 and leader 36 is open. The full weight-625 equality shell is also not yet globally closed: Pass5214 handles the point-footprint P-heavy-free slice, while footprint primal d=25 and P-heavy elimination remain open.

Primary arXiv work on association schemes of generalized-quadrangle flags provides relevant surrounding machinery, but targeted searches did not locate these specific connected opposite-line-chart spectra or fixed-footprint atom-gluing statements. This is recorded only as a literature-search boundary, not a novelty claim.
