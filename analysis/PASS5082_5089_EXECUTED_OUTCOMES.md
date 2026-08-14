# Passes 5082–5089 — Fourier extremizers, sharp q=3 expansion, q=4 panel kernel, completed rank-two sharbly dictionary, decoder, and three outside-box theorems

**Status:** EXECUTED 2026-08-14. These passes continue Passes 5074–5081 and are collision-reconciled against the already-landed Passes 5090–5097. Statements below are finite graph/code/representation theorems or explicit solver certificates. The all-q minimum-distance theorem and the complete q=4 heavy-chart minimum shell remain open.

## 5082 — Fourier extremizer attack closes exactly at q=2,3,4
For the uniform measure on apartment boundaries, every cohomology character satisfies

`wt(c_y)=N_A(1-muhat(y))/2`.

Using the already-certified exact distances gives the exact maximum nontrivial Fourier coefficients

- q=2: `29/45`, gap `16/45`;
- q=3: `9/10`, gap `1/10`;
- q=4: `409/425`, gap `16/425`.

These are exactly

`1-16/((q+1)^2(q^2+1))`.

At q=2 the complete equality shell is the 45 chamber stars; at q=3 it is the 160 chamber stars. The q=4 maximum value is exact because d=256 is exact, but its full equality shell remains open. Pass5097 independently identifies this Fourier energy with the chart-coarea energy, so the harmonic and active-chart attacks are two coordinate systems on the same functional.

## 5083 — q=3 active-chart expansion theorem closes sharply
An exact MILP uses 1620 apartment bits, 4320 theta parity auxiliaries, and 1080 opposite-pair activity bits. A valid q=3 chart restriction is a K4 cut of weight 0,3,4, so activity is encoded exactly by

`3 z_O <= sum_{A in O} x_A <= 4 z_O`.

Fixing one selected apartment by transitivity, HiGHS returns the exact optimum

`A_min=108=4*3^3`

with zero MIP gap; an optimum witness is a chamber star of weight 81. Hence every nonzero q=3 apartment-code word activates at least 108 opposite-pair charts. Combining with the local cut inequality gives

`wt >= 3 A/4 >= 81`.

This proves the sharp active-chart tester theorem at q=3 and independently recovers the distance lower bound. It is not an all-q expansion theorem.

## 5084 — q=4 four-star wall exposes a new [425,169,5] panel-dependency code
Fix one q=4 chamber star. Exhausting all `C(424,3)=12,614,424` four-star representatives gives minimum output weight 256. Exactly eight fixed-star representatives attain 256, and every one is another chamber star; there are no exotic minima in the four-star shell.

Adjoining the target chamber star turns each equality into a five-star zero relation. The eight representations collapse to exactly two five-star dependencies through the fixed chamber. They are precisely the point-panel and line-panel relations. By chamber transitivity, the complete minimum shell of the chamber-generator kernel consists of

`85 point panels + 85 line panels = 170`

weight-five relations. Pass5076 excludes dependencies of weight at most three and this four-star census excludes weight four, so the dependency code is exactly

`[425,169,5]_2`, with `A_5=170`.

Thus any hypothetical exotic q=4 weight-256 codeword must require at least five distinct chamber stars in every literal representation. This complements Pass5090: any exotic minimum must also contain a heavier 2|3 local K5 cut.

## 5085 — Pal V1,2 completes the rank-two point/line theta dictionary
Pal's symplectic sharbly presentation has V0 apartment-type generators, V1,1 genus-one three-line relations, and V1,2 genus-two split relations. Pass5075 identified V1,1 with point-side theta. The previously firewalled V1,2 side is now explicit.

For a symplectic basis `e1,f1,e2,f2` and nonzero scalar a, the three standard rank-two V0 split terms may be represented projectively by

`A0={e1,f1,e2,f2}`,

`A1={e2+a e1,f2,e1,f1-a f2}`,

`A2={f1,e2+a e1,e2,f1-a f2}`.

All three contain two points on `L=<e1,e2>` and two on the disjoint line `M=<f1,f2>`. Exact W(3,3) and W(3,5) checks for every nonzero a place these three apartments on one triangle of the line-side local K_(q+1). Hence the standard V1,2 boundary is exactly a line-theta relation. With ordered geodesic roots `R0,R1,R2`, choose oriented apartments `Aij=Ri-Rj`; then the relation is already integral:

`A01 + A12 - A02 = 0`,

and becomes the binary theta parity after reduction mod 2. Combined with the V1,1 point-theta identification, the two first-relation types in rank two match the point/line theta families. Pass5066 remains the actual finite-GQ presentation proof; this is an external-presentation dictionary, not a replacement for it.

## 5086 — the eight-entry local ROM becomes an exact global q=3 decoder
Every q=3 apartment lies in four opposite-pair charts, and no pair of distinct apartments lies in more than one chart. The decoder applies the Pass5078 eight-entry nearest-cut ROM to every affected K4 chart, accumulates correction votes, and flips all coordinates of maximum positive vote.

The producer exhausts all 1620 single errors and all `C(1620,2)=1,311,390` double errors. Every one is corrected in one sweep. Of the double errors, 1,295,190 share no chart and receive maximum vote 4; 16,200 share one chart, splitting into 15,120 cases with maximum vote 3 and 1,080 with maximum vote 4. There are zero failures.

The first local trapping-set census is also exact. There are 21,600 three-error patterns contained in one six-coordinate chart. Exactly 17,280 clear in one sweep. The remaining 4,320 are the four weight-three K4 cut words in each chart; each first sweep leaves residual weight two, and every such residual clears on the second sweep. Thus every chart-contained triple clears within two sweeps. The global guaranteed radius promoted here is still only two; this is a finite hard-decision code result, not a physical noise threshold.

## 5087 — BONKERS 1: a global 30-dimensional sqrt(17) theta channel and the missing conductor-two order
Let A_theta be the degree-16 graph on the 1620 q=3 apartments obtained by joining two apartment coordinates when they share a theta check. Let N be the 40x40 point-line incidence matrix. Its line-side kernel has dimension 15. Lift an integral basis of ker(N) to apartment functions by summing over the four line vertices of each apartment, giving a 1620x15 matrix V.

Exact integer arithmetic gives

`(A_theta^2 - 2 A_theta - 16 I)V=0`

and

`rank[V,A_theta V]=30`.

Therefore the generated invariant 30-space has characteristic polynomial

`(x^2-2x-16)^15`

and exact eigenchannels `1+sqrt(17)` and `1-sqrt(17)`, each multiplicity 15 inside this space. This gives the Pass5069 T6 quadratic eigenvalues an explicit global apartment-function carrier.

There is also an arithmetic synthesis with Pass5091. If `lambda=(1+sqrt(17))/2`, the maximal order is `O_K=Z[lambda]`. The theta eigenvalue is `alpha=1+sqrt(17)=2 lambda`, so this global theta channel realizes

`Z[alpha]=Z+2 O_K`,

the conductor-two order of discriminant 68. Together with Pass5091's maximal-order T10 block and conductor-four q=3 recurrence order, the exact order ladder is

`conductor 1 -> 2 -> 4`, `discriminant 17 -> 68 -> 272`.

## 5088 — BONKERS 2: the code synthesizes its own decoder charts
Pass5081 says the theta triples are exactly the complete weight-three dual shell, so begin with the code alone. Build the intersection graph on its 4320 minimum dual words. It is 21-regular. The graph contains 114,480 K4 cliques.

Filter those K4s by a purely support-theoretic rule: the four triples must have union of six apartment coordinates, and every one of the six coordinates must occur exactly twice. Exactly 1080 K4s survive. Their six-coordinate unions agree exactly with the 1080 opposite-pair charts of W(3,3).

Thus the code intrinsically reconstructs not only its building (Pass5062) and theta hypergraph (Pass5081), but also the local K4-cut chart decomposition required by the eight-entry decoder. The decoder placement can therefore be synthesized from the code's minimum dual shell without external point/line labels.

## 5089 — BONKERS 3: the theta presentation lifts integrally for every finite generalized quadrangle
Let Gamma be the incidence graph of any finite generalized quadrangle. Use one generator for each oriented apartment, with orientation reversal identified with negation. For three length-four geodesic roots between the same opposite vertices, orient

`Aij=Ri-Rj`.

Then the local relation is the integer chain identity

`Aij + Ajk - Aik = 0`.

The base-vertex fan proof of Pass5066 works over Z, not only F2. Choose one geodesic from a base vertex to every graph vertex. For an oriented edge, closing the two chosen paths produces a reduced closed walk of length at most eight; girth eight makes it either zero or one oriented apartment. Summing these fan apartments around an integral cycle cancels the chosen paths. Changing a distance-four geodesic changes the fan only by an oriented theta relation. This gives inverse maps and proves

`Z[oriented apartments]/Theta_Z ~= Z_1(Gamma;Z)`.

Hence the quotient is torsion-free. For W(3,q) its rank is `q^4`. As a separate exact q=2 certificate, the 120 signed theta relations on 90 apartments have rank 74 and Smith form `1^74`, leaving the torsion-free quotient `Z^16`.

## Synthesis and remaining wall
This packet closes the q=3 active-chart inequality exactly, completes the rank-two sharbly relation dictionary, promotes a global two-error decoder and its first local traps, identifies the q=4 chamber-generator kernel as `[425,169,5]` with panel minimum shell, reconstructs decoder charts intrinsically, and lifts the theta presentation integrally. The all-q distance theorem remains open. For q=4, Pass5090 and Pass5096 reduce a hypothetical exotic minimum to the heavy-chart defect sector; the new five-generator wall is an independent representation constraint on the same unresolved shell.
